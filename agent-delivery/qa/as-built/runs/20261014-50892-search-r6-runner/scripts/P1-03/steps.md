# P1-03 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=ZZQXNOHIT99999xyz ✓
3. **click** 搜索 ✓
4. **wait** 零命中空态 ✓
5. **snapshot**  ✓

## expect 逐条

- ✓ 空态提供改词、清空条件、打开高级筛选等纠错动作之一
- ✓ 空态不出现「推荐企业」分区

判定：**pass**
