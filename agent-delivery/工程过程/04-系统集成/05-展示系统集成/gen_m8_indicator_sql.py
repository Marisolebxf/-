# -*- coding: utf-8 -*-
"""生成 M8 科技指数指标树落库脚本（DDL + 32 节点种子 + 赋权方法 1 行）。"""
import json
from openpyxl import load_workbook

# 真源已归档进后端仓：db/source/M8科技指标树-算法填写表-V3.xlsx（SHA256 87536A7A…17C0）
SRC = r"e:\work\上达通\项目\深圳GKX\gkx-lumen\repos\lumen-svc-platform\db\source\M8科技指标树-算法填写表-V3.xlsx"
OUT = r"e:\work\上达通\项目\深圳GKX\gkx-lumen\repos\lumen-svc-platform\db\9x_gkxlumenx_cms_tech_index_indicator.sql"

VERSION = "v2024-02"
wb = load_workbook(SRC)


def s(v):
    return "" if v is None else str(v).strip()


def num(v, d=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return d


def q(v):
    """SQL 字面量：空串 → NULL"""
    if v is None:
        return "NULL"
    t = str(v).strip()
    if t == "":
        return "NULL"
    return "'" + t.replace("\\", "\\\\").replace("'", "''") + "'"


ws = wb["指标树填写表"]
rows = []
for r in range(2, ws.max_row + 1):
    v = [ws.cell(r, c).value for c in range(1, 25)]
    if not s(v[4]):
        continue
    level = int(num(v[0]))
    rows.append({
        "version": s(v[7]) or VERSION,
        "node_id": s(v[4]),
        "parent_id": s(v[5]),
        "name": s(v[level]),
        "level": level,
        "weight": num(v[6]),
        "weight_basis": s(v[8]),
        "description": s(v[9]),
        "calculation": s(v[10]),
        "significance": s(v[11]),
        "metric_id": s(v[12]),
        "unit": s(v[13]),
        "data_type": s(v[14]),
        "domain": s(v[15]),
        "source_tables": s(v[16]),
        "source_systems": s(v[17]),
        "update_freq": s(v[18]),
        "mapping_status": s(v[19]),
        "pending_ref": s(v[20]),
        "bid_ref": s(v[21]),
        "acceptance_unit_id": s(v[22]),
        "remark": s(v[23]),
    })

# 3-3 政策环境分支：主表缺行，按《版本历史》补名称/权重/版本，其余留空待算法补填
for add in [
    ("3-3", "3", 2, "政策环境", 0.2),
    ("3-3-1", "3-3", 3, "科技政策数量", 0.6),
    ("3-3-2", "3-3", 3, "政策承接率", 0.4),
]:
    rows.append({
        "version": VERSION, "node_id": add[0], "parent_id": add[1], "name": add[3],
        "level": add[2], "weight": add[4],
        "weight_basis": "", "description": "", "calculation": "", "significance": "",
        "metric_id": "", "unit": "", "data_type": "", "domain": "",
        "source_tables": "", "source_systems": "", "update_freq": "",
        "mapping_status": "⚠️待确认", "pending_ref": "", "bid_ref": "", "acceptance_unit_id": "",
        "remark": "主表缺行：按版本历史/赋权说明补入名称与权重，口径字段待算法补填",
    })

# 版本历史（生效日期 / 变更说明）
wsh = wb["版本历史"]
hist = {}
for r in range(2, wsh.max_row + 1):
    nid = s(wsh.cell(r, 1).value)
    if nid:
        hist[nid] = {
            "version": s(wsh.cell(r, 3).value),
            "effective_date": s(wsh.cell(r, 4).value),
            "weight": num(wsh.cell(r, 5).value),
            "changes": s(wsh.cell(r, 6).value),
        }

rows.sort(key=lambda x: [int(p) for p in x["node_id"].split("-")])
for idx, row in enumerate(rows, 1):
    h = hist.get(row["node_id"], {})
    row["effective_date"] = h.get("effective_date", "")
    row["change_note"] = h.get("changes", "")
    row["sort_order"] = idx
    if h.get("version"):
        row["version"] = h["version"]

# 赋权方法说明
wsw = wb["赋权方法说明"]
wmap = {}
for r in range(2, wsw.max_row + 1):
    k = s(wsw.cell(r, 1).value)
    if k:
        wmap[k.split("(")[0].strip()] = s(wsw.cell(r, 2).value)

steps_raw = wmap.get("赋权步骤", "")
steps = []
for i in range(1, 10):
    m, n = f"{i}. ", f"{i + 1}. "
    if m in steps_raw:
        st = steps_raw.index(m) + len(m)
        en = steps_raw.index(n) if n in steps_raw else len(steps_raw)
        steps.append(steps_raw[st:en].strip())

head = f"""-- M8 科技指数 · 指标树配置落库（FE-TS-08A-INDICATOR-TREE-V3 / BE-TS-08A-INDICATOR-TREE）
-- 真源：《M8科技指标树-算法填写表-V3.xlsx》算法工程师（王慧）填写，2026-11-08 归档进本仓
--       归档路径：db/source/M8科技指标树-算法填写表-V3.xlsx
--       SHA256  ：87536A7AA7D6422CDB06EA714D0228A5680AAEA8B252D5CEFF56D6E2CC2517C0
--       生成脚本：gkx-orchestration/agent-delivery/工程过程/04-系统集成/05-展示系统集成/gen_m8_indicator_sql.py
-- 配置版本：{VERSION}（一级 3 → 二级 8 → 三级 21，共 {len(rows)} 节点）
-- 落库位置：业务库 gkxlumenx_cms（与 cfg_tech_layer 等 M10 配置表同库同机制）
-- 读取链路：gkxlumen-display TechIndexController → Feign → gkxlumen-cms TechIndexConfigService(JdbcTemplate)
-- 说明：
--   1) 指标树按 (indicator_version, node_id) 唯一，支持多版本并存；version_history 由同表按版本聚合得到。
--   2) 「指标树填写表」主表 29 节点 + 「版本历史」多出 3-3/3-3-1/3-3-2 政策环境分支 = 32 节点。
--      该分支主表缺行，名称/权重取自版本历史，口径字段留 NULL；不补则该父级 3 的子权重和仅 0.8（不闭合）。
--   3) 3 的 calculation 文案写「人才队伍×0.60 + 机构载体×0.40」，与子权重 0.5/0.3/0.2 不一致，保留原文待复核。
--   4) 本脚本可重复执行：先清空两张配置表再全量写入（配置表只读消费，无业务写入方）。

CREATE DATABASE IF NOT EXISTS `gkxlumenx_cms` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `gkxlumenx_cms`;

-- ---------------- cfg_tech_index_indicator（指标树节点，按版本唯一） ----------------
CREATE TABLE IF NOT EXISTS `cfg_tech_index_indicator` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '行键',
  `indicator_version` varchar(32) NOT NULL COMMENT '配置版本，如 v2024-02',
  `node_id` varchar(32) NOT NULL COMMENT '节点层级编码 1 / 1-1 / 1-1-1',
  `parent_id` varchar(32) DEFAULT NULL COMMENT '父节点编码，一级为 NULL',
  `node_name` varchar(128) NOT NULL COMMENT '指标名称',
  `node_level` tinyint NOT NULL COMMENT '层级 1/2/3（3=叶节点）',
  `weight` decimal(6,4) NOT NULL DEFAULT 0.0000 COMMENT '同级权重（同父节点子项和=1）',
  `weight_basis` text COMMENT '固定赋权依据',
  `description` text COMMENT '指标描述/口径',
  `calculation` text COMMENT '计算公式或算法步骤',
  `significance` text COMMENT '指标意义',
  `metric_id` varchar(64) DEFAULT NULL COMMENT '指标 8 件套 id（仅叶节点）',
  `unit` varchar(16) DEFAULT NULL COMMENT '计量单位',
  `data_type` varchar(16) DEFAULT NULL COMMENT '数据类型 int/float/string',
  `domain` varchar(16) DEFAULT NULL COMMENT '所属领域 COMP/TECH/ENT/CHAIN/POLICY/ORG/SVC/TALENT',
  `source_tables` text COMMENT '数据源表与字段血缘',
  `source_systems` varchar(255) DEFAULT NULL COMMENT '源系统',
  `update_freq` varchar(16) DEFAULT NULL COMMENT '更新频率 daily/weekly/monthly/quarterly/annual',
  `mapping_status` varchar(16) DEFAULT NULL COMMENT '就绪状态',
  `pending_ref` varchar(64) DEFAULT NULL COMMENT '待确认项编号',
  `bid_ref` varchar(64) DEFAULT NULL COMMENT 'BID 章节引用',
  `acceptance_unit_id` varchar(64) DEFAULT NULL COMMENT '验收单元 ID',
  `remark` text COMMENT '备注',
  `effective_date` date DEFAULT NULL COMMENT '版本生效日期',
  `change_note` varchar(255) DEFAULT NULL COMMENT '版本变更说明',
  `sort_order` int NOT NULL DEFAULT 0 COMMENT '同级排序',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '审计',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '审计',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_version_node` (`indicator_version`,`node_id`),
  KEY `idx_version_parent` (`indicator_version`,`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='M8 科技指数指标树配置（算法/治理产物，只读消费）';

-- ---------------- cfg_tech_index_weight_setting（赋权方法，按版本唯一） ----------------
CREATE TABLE IF NOT EXISTS `cfg_tech_index_weight_setting` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '行键',
  `indicator_version` varchar(32) NOT NULL COMMENT '配置版本',
  `method` varchar(128) NOT NULL COMMENT '赋权方法名称',
  `method_detail` text COMMENT '方法说明',
  `steps_json` json DEFAULT NULL COMMENT '赋权步骤（JSON 数组）',
  `overall_basis` text COMMENT '总体依据',
  `note` text COMMENT '注意事项',
  `weight_composite` text COMMENT '权重合成口径',
  `levels` varchar(255) DEFAULT NULL COMMENT '指标层级构成',
  `params` text COMMENT '计算参数约定',
  `dedup` text COMMENT '去重与同源规则',
  `computability` text COMMENT '可计算性约束',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '审计',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '审计',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_version` (`indicator_version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='M8 科技指数赋权方法配置（按版本唯一）';

-- ---------------- 种子：{len(rows)} 个指标节点 ----------------
-- 先清空再全量写入（2026-11-08 按新提交的 V3 表格重建；配置表只读消费，无业务写入方）
TRUNCATE TABLE `cfg_tech_index_indicator`;
TRUNCATE TABLE `cfg_tech_index_weight_setting`;

INSERT INTO `cfg_tech_index_indicator`
(`indicator_version`,`node_id`,`parent_id`,`node_name`,`node_level`,`weight`,`weight_basis`,`description`,`calculation`,`significance`,
 `metric_id`,`unit`,`data_type`,`domain`,`source_tables`,`source_systems`,`update_freq`,`mapping_status`,`pending_ref`,`bid_ref`,
 `acceptance_unit_id`,`remark`,`effective_date`,`change_note`,`sort_order`) VALUES
"""

vals = []
for row in rows:
    vals.append(
        "({v},{nid},{pid},{name},{lv},{w},{wb},{desc},{calc},{sig},{mid},{unit},{dt},{dom},{st},{ss},{uf},{ms},{pr},{bid},{au},{rm},{ed},{cn},{so})".format(
            v=q(row["version"]), nid=q(row["node_id"]), pid=q(row["parent_id"]), name=q(row["name"]),
            lv=row["level"], w=f"{row['weight']:.4f}",
            wb=q(row["weight_basis"]), desc=q(row["description"]), calc=q(row["calculation"]),
            sig=q(row["significance"]), mid=q(row["metric_id"]), unit=q(row["unit"]),
            dt=q(row["data_type"]), dom=q(row["domain"]), st=q(row["source_tables"]),
            ss=q(row["source_systems"]), uf=q(row["update_freq"]), ms=q(row["mapping_status"]),
            pr=q(row["pending_ref"]), bid=q(row["bid_ref"]), au=q(row["acceptance_unit_id"]),
            rm=q(row["remark"]), ed=q(row["effective_date"]), cn=q(row["change_note"]),
            so=row["sort_order"],
        )
    )

steps_json = json.dumps(steps, ensure_ascii=False).replace("'", "''")
tail = f""";

-- ---------------- 种子：赋权方法（1 行） ----------------
INSERT INTO `cfg_tech_index_weight_setting`
(`indicator_version`,`method`,`method_detail`,`steps_json`,`overall_basis`,`note`,`weight_composite`,`levels`,`params`,`dedup`,`computability`) VALUES
({q(VERSION)},{q(wmap.get('赋权方法名称'))},{q(wmap.get('方法说明'))},'{steps_json}',{q(wmap.get('总体依据'))},{q(wmap.get('注意事项'))},
 {q(wmap.get('权重合成'))},{q(wmap.get('指标层级'))},{q(wmap.get('计算参数约定'))},{q(wmap.get('去重与同源规则'))},{q(wmap.get('可计算性约束'))});
"""

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(head + ",\n".join(vals) + tail)

print("生成:", OUT)
print("节点数:", len(rows), "步骤:", len(steps))
