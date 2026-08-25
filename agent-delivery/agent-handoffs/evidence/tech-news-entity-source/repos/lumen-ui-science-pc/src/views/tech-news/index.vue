<template>
  <div class="tech-news-page">
    <div class="tech-news-header">
      <a-typography-title :heading="5" :style="{ margin: 0 }">
        科技新闻抽取复核
      </a-typography-title>
      <a-tag size="small" color="arcoblue">仅调 Java /innov/v1/tech-news</a-tag>
      <MockBadge v-if="showMockBadge" />
      <div class="header-metrics">
        <span class="header-metric">
          事件数
          <MetricSpecHint
            metric-id="M_TNIE_EVENT_COUNT"
            title="抽取事件条数"
            definition="单次抽取响应中 events 数组长度；Wave0 来自 mock/llm 管线，经 Java 透传。种子：cfg_metric-TNIE-seed.yaml"
          />
          <strong>{{ events.length }}</strong>
        </span>
        <span class="header-metric">
          实体数
          <MetricSpecHint
            metric-id="M_TNIE_ENTITY_COUNT"
            title="抽取实体条数"
            definition="实体扩展响应中 entities 数组长度；仅 entity-extract 模式有值。种子：cfg_metric-TNIE-seed.yaml"
          />
          <strong>{{ entities.length }}</strong>
        </span>
      </div>
    </div>

    <div class="tech-news-grid">
      <a-card title="输入新闻" :bordered="true" class="panel">
        <a-form :model="form" layout="vertical" size="medium">
          <a-form-item label="标题">
            <a-input v-model="form.title" allow-clear placeholder="可选" />
          </a-form-item>
          <a-form-item label="正文" required>
            <a-textarea
              v-model="form.content"
              :auto-size="{ minRows: 8, maxRows: 16 }"
              placeholder="粘贴科技新闻正文"
            />
          </a-form-item>
          <a-row :gutter="12">
            <a-col :span="12">
              <a-form-item label="发布时间">
                <a-input v-model="form.published_at" allow-clear placeholder="如 2024-06-15" />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item label="来源">
                <a-input v-model="form.source" allow-clear placeholder="可选" />
              </a-form-item>
            </a-col>
          </a-row>
          <a-form-item label="抽取模式">
            <a-radio-group v-model="extractMode" type="button" size="small">
              <a-radio value="four">四要素</a-radio>
              <a-radio value="entity">实体扩展</a-radio>
            </a-radio-group>
          </a-form-item>
          <a-form-item>
            <a-checkbox v-model="persist">落库 persist=true</a-checkbox>
          </a-form-item>
          <a-space>
            <a-button type="primary" :loading="extracting" @click="onExtract">抽取</a-button>
            <a-button :disabled="extracting" @click="loadSample">填入样例</a-button>
            <a-button :loading="listing" @click="refreshHistory">刷新历史</a-button>
          </a-space>
        </a-form>
      </a-card>

      <a-card class="panel" :bordered="true">
        <template #title>
          <span>抽取结果</span>
          <span v-if="resultMeta" class="result-meta">{{ resultMeta }}</span>
        </template>
        <a-empty v-if="!payload && !extracting" description="尚未抽取" />
        <a-spin v-else :loading="extracting" style="width: 100%">
          <a-alert
            v-if="payload?.error"
            :type="isDocumentGated ? 'warning' : 'error'"
            :title="errorAlertTitle"
            :content="payload.error.message || (isDocumentGated ? '文类门控，未进入科技成果抽取' : '抽取失败')"
            style="margin-bottom: 12px"
          />
          <a-empty
            v-if="isDocumentGated && !events.length"
            description="文类已拦截，无科技成果事件"
          />
          <div v-for="(ev, idx) in events" :key="idx" class="event-block">
            <div class="event-title">
              事件 #{{ idx + 1 }}
              <a-tag
                v-if="ev.event_type"
                size="small"
                color="arcoblue"
                style="margin-left: 6px"
              >
                {{ ev.event_type }}
              </a-tag>
              <a-tag
                v-for="f in ev.flags || []"
                :key="f"
                size="small"
                :color="flagColor(f)"
                style="margin-left: 4px"
              >
                {{ f }}
              </a-tag>
            </div>
            <div v-if="ev.news_source" class="field">
              <div class="k">资讯来源</div>
              <div class="v">{{ ev.news_source }}</div>
            </div>
            <div class="field">
              <div class="k">公司名称</div>
              <div class="v">{{ (ev.company_name || []).join('、') || '（空）' }}</div>
              <a-collapse :default-active-key="[]" :bordered="false">
                <a-collapse-item key="company" header="company 证据">
                  <ul>
                    <li v-for="(s, i) in ev.evidence?.company || []" :key="i">{{ s }}</li>
                    <li v-if="!(ev.evidence?.company || []).length">（无）</li>
                  </ul>
                </a-collapse-item>
              </a-collapse>
            </div>
            <div class="field">
              <div class="k">完成时间</div>
              <div class="v">
                {{ ev.completion_time?.raw || '（空）' }}
                <a-tag v-if="ev.completion_time?.normalized" size="small" color="gray">
                  {{ ev.completion_time.normalized }}
                </a-tag>
              </div>
              <a-collapse :default-active-key="[]" :bordered="false">
                <a-collapse-item key="time" header="time 证据">
                  <ul>
                    <li v-for="(s, i) in ev.evidence?.time || []" :key="i">{{ s }}</li>
                    <li v-if="!(ev.evidence?.time || []).length">（无）</li>
                  </ul>
                </a-collapse-item>
              </a-collapse>
            </div>
            <div class="field">
              <div class="k">完成事项</div>
              <div class="v">{{ ev.completed_matter || '（空）' }}</div>
              <a-collapse :default-active-key="[]" :bordered="false">
                <a-collapse-item key="matter" header="matter 证据">
                  <ul>
                    <li v-for="(s, i) in ev.evidence?.matter || []" :key="i">{{ s }}</li>
                    <li v-if="!(ev.evidence?.matter || []).length">（无）</li>
                  </ul>
                </a-collapse-item>
              </a-collapse>
            </div>
            <div class="field">
              <div class="k">作用与影响</div>
              <div class="v">{{ formatImpact(ev.impact) }}</div>
              <a-collapse :default-active-key="[]" :bordered="false">
                <a-collapse-item key="impact" header="impact 证据">
                  <ul>
                    <li v-for="(s, i) in ev.evidence?.impact || []" :key="i">{{ s }}</li>
                    <li v-if="!(ev.evidence?.impact || []).length">（无）</li>
                  </ul>
                </a-collapse-item>
              </a-collapse>
            </div>
          </div>
          <a-empty v-if="payload && !events.length && !payload.error" description="无事件" />

          <div v-if="extractMode === 'entity' || entities.length" class="entities-panel">
            <div class="entities-title">实体表 entities[]</div>
            <a-empty v-if="!entities.length" description="暂无实体" />
            <a-table
              v-else
              row-key="rowKey"
              size="small"
              :pagination="false"
              :columns="entityColumns"
              :data="entityRows"
            />
          </div>
        </a-spin>
      </a-card>
    </div>

    <a-card :bordered="true" class="history-card" style="margin-top: 16px">
      <template #title>
        <span>{{ historyTitle }}</span>
        <a-tag size="small" color="gray" style="margin-left: 8px">
          {{ extractMode === 'entity' ? 'GET …/entity-extractions' : 'GET …/extractions' }}
        </a-tag>
      </template>
      <div v-if="extractMode === 'entity'" class="history-toolbar">
        <a-input-search
          v-model="historyQuery"
          allow-clear
          placeholder="按标题/来源筛选"
          style="max-width: 320px"
          @search="onHistorySearch"
          @clear="onHistorySearch"
        />
        <a-button :loading="listing" @click="refreshHistory">刷新</a-button>
      </div>
      <a-table
        row-key="id"
        :loading="listing"
        :columns="historyColumns"
        :data="history"
        :pagination="false"
        size="small"
      >
        <template #action="{ record }">
          <a-button type="text" size="mini" @click="onOpenHistory(record.id)">回看</a-button>
        </template>
      </a-table>
      <div v-if="extractMode === 'entity'" class="history-pager">
        <a-pagination
          :total="historyTotal"
          :current="historyPage"
          :page-size="historyPageSize"
          show-total
          show-page-size
          :page-size-options="[10, 20, 50]"
          @change="onHistoryPageChange"
          @page-size-change="onHistoryPageSizeChange"
        />
      </div>
    </a-card>
  </div>
</template>

<script setup lang="ts" name="tech-news-review">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { Message } from '@arco-design/web-vue'
import type { TableColumnData } from '@arco-design/web-vue'
import {
  extractTechNews,
  extractTechNewsEntities,
  getTechNewsEntityExtraction,
  getTechNewsExtraction,
  listTechNewsEntityExtractions,
  listTechNewsExtractions,
} from '@/api/tech-news'
import type {
  ExtractionListItem,
  TechNewsExtractResponse,
  TechNewsEvent,
  TechNewsEntityMention,
} from '@/types/tech-news'
import MockBadge from '@/components/lineage/MockBadge.vue'
import MetricSpecHint from '@/components/lineage/MetricSpecHint.vue'
import { buildTempoExploreUrl } from '@/utils/observability'

/** 触达 observability 模块（trace 深链能力随请求链路可用） */
void buildTempoExploreUrl

const SAMPLE = {
  title: '示例科技完成企业视觉平台',
  published_at: '2024-03-18',
  source: 'wave0-ui',
  content:
    '示例科技股份有限公司今日宣布完成一款企业视觉巡检平台。该平台于 2024 年 3 月通过内部验收，可自动识别产线缺陷，显著提升质检效率并降低人工复核成本。',
}

const form = reactive({
  title: '',
  content: '',
  published_at: '',
  source: '',
})
const extractMode = ref<'four' | 'entity'>('entity')
const persist = ref(true)
const extracting = ref(false)
const listing = ref(false)
const payload = ref<TechNewsExtractResponse | null>(null)
const history = ref<ExtractionListItem[]>([])
const historyQuery = ref('')
const historyPage = ref(1)
const historyPageSize = ref(20)
const historyTotal = ref(0)

const events = computed<TechNewsEvent[]>(() => payload.value?.events ?? [])
const entities = computed<TechNewsEntityMention[]>(() => payload.value?.entities ?? [])
const entityRows = computed(() =>
  entities.value.map((e, i) => ({
    ...e,
    rowKey: `${e.type}-${e.name}-${i}`,
    evidenceText: (e.evidence || []).slice(0, 2).join('；') || '—',
  })),
)
const entityColumns: TableColumnData[] = [
  { title: '类型', dataIndex: 'type', width: 120 },
  { title: '名称', dataIndex: 'name', ellipsis: true, tooltip: true },
  { title: '归一', dataIndex: 'normalized', width: 120, ellipsis: true, tooltip: true },
  { title: '置信度', dataIndex: 'confidence', width: 90 },
  { title: '证据', dataIndex: 'evidenceText', ellipsis: true, tooltip: true },
]
const GATE_CODES = new Set([
  'opinion_or_commentary',
  'policy_or_legal_noise',
  'consumer_retail_noise',
])
const isDocumentGated = computed(() => {
  const code = payload.value?.error?.code || ''
  return GATE_CODES.has(code) || code.startsWith('gated_') || (payload.value?.error?.message || '').includes('document gated')
})
const errorAlertTitle = computed(() => {
  if (!payload.value?.error) return ''
  if (isDocumentGated.value) {
    return `文类已拦截（${payload.value.error.code || 'gated'}）`
  }
  return payload.value.error.code || 'error'
})
const showMockBadge = computed(() => {
  const mode = payload.value?.meta?.mode
  return !mode || mode === 'mock'
})
const resultMeta = computed(() => {
  if (!payload.value) return ''
  const p = payload.value
  return `request_id=${p.request_id || '-'} · model=${p.model || '-'} · mode=${p.meta?.mode || '-'} · persisted=${String(p.meta?.persisted)}`
})

const historyTitle = computed(() =>
  extractMode.value === 'entity' ? '实体扩展历史（ADS）' : '四要素历史',
)

const historyColumns = computed<TableColumnData[]>(() => {
  const cols: TableColumnData[] = [
    { title: 'ID', dataIndex: 'id', width: 220, ellipsis: true, tooltip: true },
    { title: '标题', dataIndex: 'title', ellipsis: true, tooltip: true },
    { title: '来源', dataIndex: 'source', width: 100 },
    { title: '模型', dataIndex: 'model', width: 140 },
    { title: '事件数', dataIndex: 'event_count', width: 80 },
  ]
  if (extractMode.value === 'entity') {
    cols.push({ title: '实体数', dataIndex: 'entity_count', width: 80 })
  }
  cols.push(
    { title: '创建时间', dataIndex: 'created_at', width: 180 },
    { title: '操作', slotName: 'action', width: 80 },
  )
  return cols
})

function formatImpact(impact: string | null | undefined): string {
  if (impact == null || impact === '') return '暂无'
  return impact
}

function flagColor(flag: string): string {
  if (flag.startsWith('gated_') || flag.includes('finance_matter')) return 'orangered'
  if (flag.includes('impact')) return 'arcoblue'
  return 'gray'
}

function loadSample() {
  form.title = SAMPLE.title
  form.content = SAMPLE.content
  form.published_at = SAMPLE.published_at
  form.source = SAMPLE.source
}

async function onExtract() {
  if (!form.content.trim()) {
    Message.warning('请填写正文')
    return
  }
  extracting.value = true
  try {
    const requestId =
      typeof crypto !== 'undefined' && crypto.randomUUID
        ? crypto.randomUUID()
        : `tn-${Date.now()}`
    const data =
      extractMode.value === 'entity'
        ? await extractTechNewsEntities(
            {
              title: form.title || undefined,
              content: form.content,
              published_at: form.published_at || undefined,
              source: form.source || undefined,
            },
            { persist: persist.value, requestId },
          )
        : await extractTechNews(
            {
              title: form.title || undefined,
              content: form.content,
              published_at: form.published_at || undefined,
              source: form.source || undefined,
            },
            { persist: persist.value, requestId },
          )
    payload.value = data
    const code = data?.error?.code || ''
    const gated =
      GATE_CODES.has(code) ||
      code.startsWith('gated_') ||
      (data?.error?.message || '').includes('document gated')
    if (gated) {
      Message.warning(data?.error?.message || '文类已拦截')
    } else if (data?.error) {
      Message.error(data.error.message || '抽取返回错误')
    } else {
      Message.success('抽取完成')
    }
    await refreshHistory()
  } catch {
    /* request 已 Message.error */
  } finally {
    extracting.value = false
  }
}

async function refreshHistory() {
  listing.value = true
  try {
    if (extractMode.value === 'entity') {
      const offset = (historyPage.value - 1) * historyPageSize.value
      const data = await listTechNewsEntityExtractions(
        historyPageSize.value,
        offset,
        historyQuery.value.trim() || undefined,
      )
      history.value = data?.items ?? []
      historyTotal.value = Number(data?.total ?? history.value.length)
    } else {
      const data = await listTechNewsExtractions(20, 0)
      history.value = data?.items ?? []
      historyTotal.value = history.value.length
    }
  } catch {
    history.value = []
    historyTotal.value = 0
  } finally {
    listing.value = false
  }
}

function onHistorySearch() {
  historyPage.value = 1
  void refreshHistory()
}

function onHistoryPageChange(page: number) {
  historyPage.value = page
  void refreshHistory()
}

function onHistoryPageSizeChange(size: number) {
  historyPageSize.value = size
  historyPage.value = 1
  void refreshHistory()
}

async function onOpenHistory(id: string) {
  try {
    const stored =
      extractMode.value === 'entity'
        ? await getTechNewsEntityExtraction(id)
        : await getTechNewsExtraction(id)
    if (stored?.response) {
      payload.value = stored.response
      Message.success(`已回看 ${id}`)
    } else {
      Message.warning('详情无 response 字段')
    }
  } catch {
    /* handled */
  }
}

watch(extractMode, () => {
  historyPage.value = 1
  historyQuery.value = ''
  void refreshHistory()
})

onMounted(() => {
  void refreshHistory()
})
</script>

<style scoped>
.tech-news-page {
  background: #fff;
  border-radius: 8px;
  padding: 16px 24px 24px;
  min-height: calc(100vh - 130px);
}
.tech-news-header {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 16px;
}
.header-metrics {
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  gap: 16px;
}
.header-metric {
  color: var(--color-text-2, #4e5969);
  font-size: 13px;
  display: inline-flex;
  align-items: center;
  gap: 2px;
}
.entities-panel {
  margin-top: 16px;
  border-top: 1px solid var(--color-border-2, #e5e6eb);
  padding-top: 12px;
}
.entities-title {
  font-weight: 600;
  margin-bottom: 8px;
}
.tech-news-grid {
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: 16px;
}
@media (max-width: 1100px) {
  .tech-news-grid {
    grid-template-columns: 1fr;
  }
}
.panel :deep(.arco-card-body) {
  padding-top: 12px;
}
.result-meta {
  margin-left: 12px;
  font-size: 12px;
  color: var(--color-text-3, #86909c);
  font-weight: 400;
}
.event-block {
  border: 1px solid var(--color-border-2, #e5e6eb);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 12px;
}
.event-title {
  font-weight: 600;
  margin-bottom: 8px;
}
.field {
  margin-bottom: 8px;
}
.k {
  color: var(--color-text-3, #86909c);
  font-size: 12px;
  margin-bottom: 2px;
}
.v {
  color: var(--color-text-1, #1d2129);
  font-size: 14px;
  line-height: 1.5;
}
.history-toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}
.history-pager {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
}
.field ul {
  margin: 0;
  padding-left: 18px;
  color: var(--color-text-2, #4e5969);
  font-size: 13px;
}
</style>
