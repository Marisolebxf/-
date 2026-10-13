# P0-13 · 地图放大与缩小按钮可改变地图视野（00394）

1. goto `/enterprise/key-enterprise-analysis?view=type`（默认地图视图）。
2. CDP 读取初始瓦片层级：天地图 WMTS `TILEMATRIX=9`。
3. 点击工具栏「放大」按钮（snapshot ref e12）。
4. CDP 复读：`TILEMATRIX=10` → 视野放大 ✔。
5. 点击工具栏「缩小」按钮（ref e13）。
6. CDP 复读：`TILEMATRIX=9` → 视野回退 ✔。

判定：两条预期（放大后视野放大 / 缩小后视野回退）均成立 → Pass。
