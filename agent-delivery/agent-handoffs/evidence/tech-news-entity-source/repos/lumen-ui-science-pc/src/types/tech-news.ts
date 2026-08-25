/** 科技新闻四要素抽取（Java 门面解包后的业务体） */

export interface TechNewsExtractOptions {
  max_events?: number
  require_evidence?: boolean
  enable_impact_pass?: boolean
  language?: string
}

export interface TechNewsExtractRequest {
  request_id?: string
  title?: string
  content: string
  published_at?: string
  source?: string
  options?: TechNewsExtractOptions
}

export interface CompletionTime {
  raw?: string | null
  normalized?: string | null
  granularity?: string | null
}

export interface Evidence {
  company?: string[]
  time?: string[]
  matter?: string[]
  impact?: string[]
}

export interface Confidence {
  company_name?: number
  completion_time?: number
  completed_matter?: number
  impact?: number
  overall?: number
}

export interface TechNewsEvent {
  company_name?: string[]
  completion_time?: CompletionTime
  completed_matter?: string | null
  impact?: string | null
  /** 实体扩展：事件类型 */
  event_type?: string | null
  news_source?: string | null
  entity_refs?: string[]
  evidence?: Evidence
  confidence?: Confidence
  flags?: string[]
}

export interface TechNewsEntityMention {
  type: string
  name: string
  normalized?: string | null
  evidence?: string[]
  confidence?: number
}

export interface ResponseMeta {
  used_candidate_sentences?: boolean
  candidate_count?: number
  impact_pass_applied?: boolean
  ner_applied?: boolean
  persisted?: boolean
  latency_ms?: number
  token_usage?: { prompt?: number; completion?: number }
  mode?: string
}

export interface EntityExtractMeta extends ResponseMeta {
  schema_version?: string
  entity_count?: number
  event_count?: number
  notes?: string[]
}

export interface TechNewsExtractResponse {
  request_id?: string
  model?: string
  events?: TechNewsEvent[]
  /** 实体扩展顶层表 */
  entities?: TechNewsEntityMention[]
  meta?: EntityExtractMeta
  error?: { code?: string; message?: string } | null
}

export interface ExtractionListItem {
  id: string
  created_at?: string
  title?: string | null
  source?: string | null
  published_at?: string | null
  model?: string
  event_count?: number
  /** 实体扩展历史（entity-extractions） */
  entity_count?: number
  mode?: string
  schema_version?: string
}

export interface ExtractionListResponse {
  items?: ExtractionListItem[]
  limit?: number
  offset?: number
  total?: number
  q?: string | null
}

export interface StoredExtractionResponse {
  id: string
  created_at?: string
  title?: string | null
  source?: string | null
  published_at?: string | null
  content?: string
  model?: string
  mode?: string
  schema_version?: string
  entity_count?: number
  event_count?: number
  /** ADS 规范化行（回看时可作辅证；主展示仍用 response） */
  entities?: unknown[]
  events?: unknown[]
  response?: TechNewsExtractResponse
}
