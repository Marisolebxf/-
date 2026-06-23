#!/bin/bash
# ============================================================
# MySQL 表与注释查看脚本
# 用法: bash list_tables.sh
# ============================================================

MYSQL_HOST="183.240.141.251"
MYSQL_PORT="3318"
MYSQL_USER="gkx_reader_zp"
MYSQL_PASS="Zp_Use_Gkx_db@123456"
MYSQL_DB="gkx"

mysql -h"${MYSQL_HOST}" -P"${MYSQL_PORT}" -u"${MYSQL_USER}" -p"${MYSQL_PASS}" -D"${MYSQL_DB}" \
  --default-character-set=utf8mb4 \
  -e "
    SELECT
      TABLE_NAME    AS '表名',
      TABLE_COMMENT AS '表注释',
      TABLE_ROWS    AS '预估行数',
      ENGINE        AS '引擎',
      CREATE_TIME   AS '创建时间',
      UPDATE_TIME   AS '更新时间'
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = '${MYSQL_DB}'
    ORDER BY TABLE_NAME;
  "
