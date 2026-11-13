# 三域 op_id 总清单

设计稿；不是调用回执。共 21 个独立操作：TECH 9，PERSON 6，RESEARCH 6。

| 域 | op_id | Java 网关入口 | diagram_id | 实测状态 |
|---|---|---|---|---|
| tech | TECH_ENTITY_SEARCH | POST `/topic/v1/tech/graph/ops/TECH_ENTITY_SEARCH` | TECH-GRAPH-TRIPLE | not_run |
| tech | TECH_ENTITY_DETAIL | POST `/topic/v1/tech/graph/ops/TECH_ENTITY_DETAIL` | TECH-GRAPH-TRIPLE | not_run |
| tech | TECH_RE_NEIGHBORS | POST `/topic/v1/tech/graph/ops/TECH_RE_NEIGHBORS` | TECH-GRAPH-TRIPLE | not_run |
| tech | TECH_RE_SUBGRAPH | POST `/topic/v1/tech/graph/ops/TECH_RE_SUBGRAPH` | TECH-GRAPH-TRIPLE | not_run |
| tech | TECH_RE_PAPER | POST `/topic/v1/tech/graph/ops/TECH_RE_PAPER` | TECH-GRAPH-TRIPLE | not_run |
| tech | TECH_RE_PATENT | POST `/topic/v1/tech/graph/ops/TECH_RE_PATENT` | TECH-GRAPH-TRIPLE | not_run |
| tech | TECH_RE_PERSON | POST `/topic/v1/tech/graph/ops/TECH_RE_PERSON` | TECH-GRAPH-TRIPLE | not_run |
| tech | TECH_RE_INSTITUTION | POST `/topic/v1/tech/graph/ops/TECH_RE_INSTITUTION` | TECH-GRAPH-TRIPLE | not_run |
| tech | TECH_GRAPH_BROWSE | POST `/topic/v1/tech/graph/ops/TECH_GRAPH_BROWSE` | TECH-GRAPH-TRIPLE | not_run |
| person | PERSON_ENTITY_SEARCH | POST `/topic/v1/person/graph/ops/PERSON_ENTITY_SEARCH` | PERSON-GRAPH-TRIPLE | not_run |
| person | PERSON_ENTITY_DETAIL | POST `/topic/v1/person/graph/ops/PERSON_ENTITY_DETAIL` | PERSON-GRAPH-TRIPLE | not_run |
| person | PERSON_RE_NEIGHBORS | POST `/topic/v1/person/graph/ops/PERSON_RE_NEIGHBORS` | PERSON-GRAPH-TRIPLE | not_run |
| person | PERSON_RE_SUBGRAPH | POST `/topic/v1/person/graph/ops/PERSON_RE_SUBGRAPH` | PERSON-GRAPH-TRIPLE | not_run |
| person | PERSON_RE_RESEARCH | POST `/topic/v1/person/graph/ops/PERSON_RE_RESEARCH` | PERSON-GRAPH-TRIPLE | not_run |
| person | PERSON_GRAPH_BROWSE | POST `/topic/v1/person/graph/ops/PERSON_GRAPH_BROWSE` | PERSON-GRAPH-TRIPLE | not_run |
| research | RESEARCH_ENTITY_SEARCH | POST `/topic/v1/research/graph/ops/RESEARCH_ENTITY_SEARCH` | RESEARCH-GRAPH-TRIPLE | not_run |
| research | RESEARCH_ENTITY_DETAIL | POST `/topic/v1/research/graph/ops/RESEARCH_ENTITY_DETAIL` | RESEARCH-GRAPH-TRIPLE | not_run |
| research | RESEARCH_RE_NEIGHBORS | POST `/topic/v1/research/graph/ops/RESEARCH_RE_NEIGHBORS` | RESEARCH-GRAPH-TRIPLE | not_run |
| research | RESEARCH_RE_SUBGRAPH | POST `/topic/v1/research/graph/ops/RESEARCH_RE_SUBGRAPH` | RESEARCH-GRAPH-TRIPLE | not_run |
| research | RESEARCH_RE_PROJECT | POST `/topic/v1/research/graph/ops/RESEARCH_RE_PROJECT` | RESEARCH-GRAPH-TRIPLE | not_run |
| research | RESEARCH_GRAPH_BROWSE | POST `/topic/v1/research/graph/ops/RESEARCH_GRAPH_BROWSE` | RESEARCH-GRAPH-TRIPLE | not_run |
