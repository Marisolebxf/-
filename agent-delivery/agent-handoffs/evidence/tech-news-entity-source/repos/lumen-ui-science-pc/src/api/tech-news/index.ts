import request from '@/utils/request'
import type {
  ExtractionListResponse,
  StoredExtractionResponse,
  TechNewsExtractRequest,
  TechNewsExtractResponse,
} from '@/types/tech-news'

/**
 * 科技新闻四要素 / 实体扩展抽取 API（仅调 Java，禁止直连 Python /internal/*）。
 *
 * 网关：/api/innov/v1/tech-news/** → gkxlumen-innov /v1/tech-news/**
 * 响应包络 { code:0, data } 由 request 解包。
 */
const BASE = '/innov/v1/tech-news'

/** LLM + impact / entity 可能较慢，与 Java 读超时对齐 */
const EXTRACT_TIMEOUT_MS = 120_000

export function extractTechNews(
  body: TechNewsExtractRequest,
  opts?: { persist?: boolean; requestId?: string },
) {
  return request({
    url: `${BASE}/extract`,
    method: 'post',
    params: { persist: opts?.persist ?? true },
    data: body,
    headers: opts?.requestId ? { 'X-Request-Id': opts.requestId } : undefined,
    timeout: EXTRACT_TIMEOUT_MS,
  }) as Promise<TechNewsExtractResponse>
}

/** 实体扩展：7 类实体 + event_type（E-TECH-NEWS-ENTITY-M2-L03） */
export function extractTechNewsEntities(
  body: TechNewsExtractRequest,
  opts?: { persist?: boolean; requestId?: string },
) {
  return request({
    url: `${BASE}/entity-extract`,
    method: 'post',
    params: { persist: opts?.persist ?? true },
    data: body,
    headers: opts?.requestId ? { 'X-Request-Id': opts.requestId } : undefined,
    timeout: EXTRACT_TIMEOUT_MS,
  }) as Promise<TechNewsExtractResponse>
}

/** 四要素历史列表 */
export function listTechNewsExtractions(limit = 20, offset = 0) {
  return request({
    url: `${BASE}/extractions`,
    method: 'get',
    params: { limit, offset },
  }) as Promise<ExtractionListResponse>
}

export function getTechNewsExtraction(requestId: string) {
  return request({
    url: `${BASE}/extractions/${encodeURIComponent(requestId)}`,
    method: 'get',
  }) as Promise<StoredExtractionResponse>
}

/** 实体扩展历史列表（E-TECH-NEWS-ENTITY-M3-L03 / M4-L03 → Java entity-extractions） */
export function listTechNewsEntityExtractions(
  limit = 20,
  offset = 0,
  q?: string,
) {
  return request({
    url: `${BASE}/entity-extractions`,
    method: 'get',
    params: { limit, offset, ...(q ? { q } : {}) },
  }) as Promise<ExtractionListResponse>
}

export function getTechNewsEntityExtraction(requestId: string) {
  return request({
    url: `${BASE}/entity-extractions/${encodeURIComponent(requestId)}`,
    method: 'get',
  }) as Promise<StoredExtractionResponse>
}
