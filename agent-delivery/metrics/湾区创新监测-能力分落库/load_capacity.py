"""粤港澳大湾区创新能力指数（M_INNOV_GBA_CAPACITY_INDEX）—— 落库脚本。

数源（用户裁定 2026-11-04）：直接落 metrics/repro/out/M_INNOV_GBA_CAPACITY_INDEX_out.json 四城结果，
不回算（我方仓库缺 dwd_zh_paper，无法自主重算，能力分依赖 gkx 三方库口径）。

诚实性约束：
- available 四城（广州/深圳/惠州/东莞）落全字段（能力分 + 四子指数 + 排名 + 原始计数）。
- missing 七城（珠海/佛山/中山/江门/肇庆/香港/澳门）只落原始计数，能力分字段一律 NULL（不补 0）。

用法：
    $env:GKX_MYSQL_PWD="GKX@Lumen2026"   # PowerShell
    python load_capacity.py
"""
import json
import os
import pathlib

import pymysql

HOST = "10.50.11.76"
PORT = 3306
USER = "gkxlumenx"
DB = "gkxlumenx_ads"

OUT_JSON = pathlib.Path(
    r"e:/work/上达通/项目/深圳GKX/gkx-lumen/gkx-orchestration/"
    r"agent-delivery/metrics/repro/out/M_INNOV_GBA_CAPACITY_INDEX_out.json"
)

DDL = """
CREATE TABLE IF NOT EXISTS `gkxlumenx_ads`.`ads_gba_capacity_index` (
  `id`            BIGINT NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `city`          VARCHAR(32) NOT NULL COMMENT '城市名（带市后缀，与 out.json 一致）',
  `city_short`    VARCHAR(16) DEFAULT NULL COMMENT '城市简称',
  `capacity_index` DOUBLE DEFAULT NULL COMMENT '综合创新能力指数（0-100，四城内 min-max）',
  `res_index`     DOUBLE DEFAULT NULL COMMENT '创新资源子指数',
  `org_index`     DOUBLE DEFAULT NULL COMMENT '创新机构子指数',
  `mech_index`    DOUBLE DEFAULT NULL COMMENT '创新机制子指数（仅技术转移一维，可信度低）',
  `env_index`     DOUBLE DEFAULT NULL COMMENT '创新环境子指数',
  `rank_no`       INT DEFAULT NULL COMMENT '能力分排名（1-4，仅四城）',
  `org_cnt`       BIGINT DEFAULT NULL COMMENT '机构底册数',
  `patent_cnt`    BIGINT DEFAULT NULL COMMENT '专利数（2021-2026 申请存量）',
  `paper_cnt`     BIGINT DEFAULT NULL COMMENT '论文数（署名机构精确匹配）',
  `rd_latest`     DOUBLE DEFAULT NULL COMMENT '研发投入（上市主体最新报告期求和，元）',
  `hightech_cnt`  INT DEFAULT NULL COMMENT '高企数',
  `institute_cnt` INT DEFAULT NULL COMMENT '科研院所数',
  `transfer_cnt`  INT DEFAULT NULL COMMENT '技术转移条数',
  `policy_cnt`    INT DEFAULT NULL COMMENT '有效政策数',
  `hightech_density` DOUBLE DEFAULT NULL COMMENT '高企密度（高企数/机构数）',
  `coverage_note` VARCHAR(255) DEFAULT NULL COMMENT '覆盖说明',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_city` (`city`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='粤港澳大湾区创新能力指数（数源=repro/out，四城 4/11，禁止把四城当湾区）';
"""

COVERAGE_NOTE = "可用样本 4/11；四城内 min-max，深圳=100/惠州=0 为端点效应非绝对评价；缺测维已剔除（MECH 仅转移一维）"


def main() -> None:
    pwd = os.environ.get("GKX_MYSQL_PWD")
    if not pwd:
        raise SystemExit("缺少环境变量 GKX_MYSQL_PWD")

    data = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    rows = data["rows"]
    available = {r["city"] for r in rows if "capacity_index" in r}

    conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=pwd, database=DB, connect_timeout=10)
    try:
        with conn.cursor() as cur:
            cur.execute(DDL)
            cur.execute("DELETE FROM `gkxlumenx_ads`.`ads_gba_capacity_index`")

            inserted = 0
            for r in rows:
                city = r.get("city")
                is_available = city in available
                cur.execute(
                    """
                    INSERT INTO `gkxlumenx_ads`.`ads_gba_capacity_index`
                      (city, city_short, capacity_index, res_index, org_index, mech_index, env_index,
                       rank_no, org_cnt, patent_cnt, paper_cnt, rd_latest, hightech_cnt,
                       institute_cnt, transfer_cnt, policy_cnt, hightech_density, coverage_note)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        city,
                        r.get("city_short"),
                        r.get("capacity_index") if is_available else None,
                        r.get("res_index") if is_available else None,
                        r.get("org_index") if is_available else None,
                        r.get("mech_index") if is_available else None,
                        r.get("env_index") if is_available else None,
                        None,  # rank_no 由查询侧按 capacity_index 排序派生
                        r.get("org_cnt"),
                        r.get("patent_cnt"),
                        r.get("paper_cnt"),
                        r.get("rd_latest"),
                        r.get("hightech_cnt"),
                        r.get("institute_cnt"),
                        r.get("transfer_cnt"),
                        r.get("policy_cnt"),
                        r.get("hightech_density"),
                        COVERAGE_NOTE if is_available else "暂无机构底册，不参与排名",
                    ),
                )
                inserted += 1
            conn.commit()

            # 排名回填（仅四城）
            cur.execute(
                """
                UPDATE `gkxlumenx_ads`.`ads_gba_capacity_index` t
                JOIN (
                  SELECT id, RANK() OVER (ORDER BY capacity_index DESC) AS rk
                  FROM `gkxlumenx_ads`.`ads_gba_capacity_index`
                  WHERE capacity_index IS NOT NULL
                ) s ON s.id = t.id
                SET t.rank_no = s.rk
                """
            )
            conn.commit()

            print(f"inserted={inserted} rows")
            cur.execute(
                "SELECT city, capacity_index, res_index, org_index, mech_index, env_index, rank_no "
                "FROM `gkxlumenx_ads`.`ads_gba_capacity_index` ORDER BY rank_no IS NULL, rank_no"
            )
            for row in cur.fetchall():
                print(row)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
