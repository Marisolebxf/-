-- tag_dict 三方真源企业标签码表补充（55 值全量对照）
-- 目标：MySQL gkxlumenx_dwd.tag_dict
-- 三方真源：gkx.dwd_org_tech_tag.org_tag（汉字标签，2026-10-30 全量 55 值）
-- JOIN 口径：org_tag = tag_dict.tag_name（GDF-ENT 09 §3.9，2026-10-22 拍板）
-- 现有基线：gkxlumenx_dwd_tag_dict_align.sql 17 行种子（零改动）
--          + dicts.py TAG_ZH 静态兜底占用码（避让）
-- 日期：2026-10-30
--
-- 规则（2026-10-30 用户裁定）：
--   1. 字面完全一致才复用：4 个三方值精确命中现有 tag_name → 复用不新增
--      （高新技术企业=high_tech / 瞪羚企业=gazelle / 独角兽企业=unicorn / 科技型中小企业=sme_tech）
--   2. 字不一样即独立标签，不考虑语义（如 专精特新中小企业 ≠ 专精特新/专精特新企业；
--      国家级科技型中小企业 ≠ 科技型中小企业；国家级高新技术企业 ≠ 高新技术企业；
--      专精特新小巨人企业 ≠ 小巨人）
--   3. 技术先进型服务企业：字面命中 dicts.py 已占用码 tech_advanced_service，沿用补行
--   4. 曾获 = 独立标签，全部统一前缀 former_；正常标签的码与名不得含「曾获」；
--      description 统一标「曾获历史标签」辅助识别（表无 is_former 列，前缀即标记）
--   5. tag_level 跟随三方字面：带「国家级」→ national，「省级」→ province，无层级字 → NULL（不猜）
--   6. 载体类 4 行（企业技术中心 / 工程技术研究中心 / 众创空间 / 孵化器）category=diy；禁用自造枚举（消费方白名单 enum_guards.ALLOWED_TAG_CATEGORIES 仅 qualification/honor/scale/industry/diy）
--   7. sort_order 接现有最大值 150，按 160 起步步进 10
--   8. 现有行零改动：plain INSERT（无 ON DUPLICATE KEY UPDATE）；撞唯一键 = 冲突，报错即停

INSERT INTO `gkxlumenx_dwd`.`tag_dict`
  (`tag_code`, `tag_name`, `tag_category`, `tag_level`, `ods_source`, `sort_order`, `is_active`, `description`)
VALUES
  ('gei_china_unicorn', 'GEI中国独角兽企业', 'qualification', NULL, 'dwd_org_tech_tag', 160, 1, '长城战略咨询(GEI)中国独角兽榜单'),
  ('specialized_sme', '专精特新中小企业', 'qualification', NULL, 'dwd_org_tech_tag', 170, 1, NULL),
  ('specialized_little_giant', '专精特新小巨人企业', 'qualification', NULL, 'dwd_org_tech_tag', 180, 1, '与预建小巨人(little_giant_pro)为不同标签'),
  ('china_unicorn', '中国独角兽企业', 'qualification', NULL, 'dwd_org_tech_tag', 190, 1, NULL),
  ('tech_center', '企业技术中心', 'diy', NULL, 'dwd_org_tech_tag', 200, 1, '创新平台'),
  ('maker_space', '众创空间', 'diy', NULL, 'dwd_org_tech_tag', 210, 1, '创新载体'),
  ('innovative_sme', '创新型中小企业', 'qualification', NULL, 'dwd_org_tech_tag', 220, 1, NULL),
  ('manu_single_champion', '制造业单项冠军企业', 'qualification', NULL, 'dwd_org_tech_tag', 230, 1, NULL),
  ('national_specialized_little_giant', '国家级专精特新小巨人企业', 'qualification', 'national', 'dwd_org_tech_tag', 240, 1, NULL),
  ('national_tech_center', '国家级企业技术中心', 'diy', 'national', 'dwd_org_tech_tag', 250, 1, NULL),
  ('national_manu_single_champion', '国家级制造业单项冠军企业', 'qualification', 'national', 'dwd_org_tech_tag', 260, 1, NULL),
  ('national_tech_innovation_demonstration', '国家级技术创新示范企业', 'qualification', 'national', 'dwd_org_tech_tag', 270, 1, NULL),
  ('national_ip_advantage', '国家级知识产权优势企业', 'qualification', 'national', 'dwd_org_tech_tag', 280, 1, NULL),
  ('national_ip_demonstration', '国家级知识产权示范企业', 'qualification', 'national', 'dwd_org_tech_tag', 290, 1, NULL),
  ('national_sme_tech', '国家级科技型中小企业', 'qualification', 'national', 'dwd_org_tech_tag', 300, 1, '三方原文标签，与科技型中小企业(sme_tech)为不同标签'),
  ('national_high_tech', '国家级高新技术企业', 'qualification', 'national', 'dwd_org_tech_tag', 310, 1, '三方原文标签，与高新技术企业(high_tech)为不同标签'),
  ('engineering_research_center', '工程技术研究中心', 'diy', NULL, 'dwd_org_tech_tag', 320, 1, '创新平台'),
  ('tech_advanced_service', '技术先进型服务企业', 'qualification', NULL, 'dwd_org_tech_tag', 330, 1, '码沿用静态字典 tech_advanced_service 补行'),
  ('tech_innovation_demonstration', '技术创新示范企业', 'qualification', NULL, 'dwd_org_tech_tag', 340, 1, NULL),
  ('former_national_specialized_little_giant', '曾获国家级专精特新小巨人企业', 'qualification', 'national', 'dwd_org_tech_tag', 350, 1, '曾获历史标签'),
  ('former_national_tech_center', '曾获国家级企业技术中心', 'diy', 'national', 'dwd_org_tech_tag', 360, 1, '曾获历史标签'),
  ('former_national_manu_single_champion', '曾获国家级制造业单项冠军企业', 'qualification', 'national', 'dwd_org_tech_tag', 370, 1, '曾获历史标签'),
  ('former_national_sme_tech', '曾获国家级科技型中小企业', 'qualification', 'national', 'dwd_org_tech_tag', 380, 1, '曾获历史标签'),
  ('former_national_high_tech', '曾获国家级高新技术企业', 'qualification', 'national', 'dwd_org_tech_tag', 390, 1, '曾获历史标签'),
  ('former_province_specialized_sme', '曾获省级专精特新中小企业', 'qualification', 'province', 'dwd_org_tech_tag', 400, 1, '曾获历史标签'),
  ('former_province_gazelle', '曾获省级瞪羚企业', 'qualification', 'province', 'dwd_org_tech_tag', 410, 1, '曾获历史标签'),
  ('former_province_tech_little_giant', '曾获省级科技小巨人企业', 'qualification', 'province', 'dwd_org_tech_tag', 420, 1, '曾获历史标签'),
  ('former_gazelle', '曾获瞪羚企业', 'qualification', NULL, 'dwd_org_tech_tag', 430, 1, '曾获历史标签'),
  ('former_hurun_global_gazelle', '曾获胡润全球瞪羚企业', 'qualification', NULL, 'dwd_org_tech_tag', 440, 1, '曾获历史标签'),
  ('private_tech_enterprise', '民营科技企业', 'qualification', NULL, 'dwd_org_tech_tag', 450, 1, NULL),
  ('province_specialized_sme', '省级专精特新中小企业', 'qualification', 'province', 'dwd_org_tech_tag', 460, 1, NULL),
  ('province_specialized_little_giant', '省级专精特新小巨人企业', 'qualification', 'province', 'dwd_org_tech_tag', 470, 1, NULL),
  ('province_innovative_sme', '省级创新型中小企业', 'qualification', 'province', 'dwd_org_tech_tag', 480, 1, NULL),
  ('province_tech_advanced_service', '省级技术先进型服务企业', 'qualification', 'province', 'dwd_org_tech_tag', 490, 1, NULL),
  ('province_private_tech_enterprise', '省级民营科技企业', 'qualification', 'province', 'dwd_org_tech_tag', 500, 1, NULL),
  ('province_gazelle', '省级瞪羚企业', 'qualification', 'province', 'dwd_org_tech_tag', 510, 1, NULL),
  ('province_ip_advantage', '省级知识产权优势企业', 'qualification', 'province', 'dwd_org_tech_tag', 520, 1, NULL),
  ('province_ip_demonstration', '省级知识产权示范企业', 'qualification', 'province', 'dwd_org_tech_tag', 530, 1, NULL),
  ('province_tech_little_giant', '省级科技小巨人企业', 'qualification', 'province', 'dwd_org_tech_tag', 540, 1, NULL),
  ('ip_advantage', '知识产权优势企业', 'qualification', NULL, 'dwd_org_tech_tag', 550, 1, NULL),
  ('ip_demonstration', '知识产权示范企业', 'qualification', NULL, 'dwd_org_tech_tag', 560, 1, NULL),
  ('tech_incubator', '科技企业孵化器', 'diy', NULL, 'dwd_org_tech_tag', 570, 1, '创新载体'),
  ('tech_little_giant', '科技小巨人企业', 'qualification', NULL, 'dwd_org_tech_tag', 580, 1, NULL),
  ('sci_reform_demonstration', '科改示范企业', 'qualification', NULL, 'dwd_org_tech_tag', 590, 1, '国企科改示范行动名单'),
  ('hurun_global_unicorn', '胡润全球独角兽企业', 'qualification', NULL, 'dwd_org_tech_tag', 600, 1, '胡润研究院国际榜单'),
  ('hurun_global_gazelle', '胡润全球瞪羚企业', 'qualification', NULL, 'dwd_org_tech_tag', 610, 1, '胡润研究院国际榜单'),
  ('recheck_national_specialized_little_giant', '过期待复核国家级专精特新小巨人企业', 'qualification', 'national', 'dwd_org_tech_tag', 620, 1, '过期待复核标签'),
  ('recheck_national_manu_single_champion', '过期待复核国家级制造业单项冠军企业', 'qualification', 'national', 'dwd_org_tech_tag', 630, 1, '过期待复核标签'),
  ('recheck_national_tech_innovation_demonstration', '过期待复核国家级技术创新示范企业', 'qualification', 'national', 'dwd_org_tech_tag', 640, 1, '过期待复核标签'),
  ('hidden_champion', '隐形冠军企业', 'qualification', NULL, 'dwd_org_tech_tag', 650, 1, NULL),
  ('eaglet', '雏鹰企业', 'qualification', NULL, 'dwd_org_tech_tag', 660, 1, NULL);
