/*
 *
 *      Copyright (c) 2018-2026, gkx All rights reserved.
 *
 *  Author: gkx
 *
 */

package com.topcomm.gkx.innov.technews;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.function.Supplier;

/**
 * 科技新闻抽取门面：纯透传 Python /internal/tech-news/*。
 *
 * @author gkx
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class TechNewsExtractService {

	private final TechNewsAlgoClient techNewsAlgoClient;

	public Map<String, Object> extract(Map<String, Object> body, boolean persist, String requestId) {
		String rid = (requestId == null || requestId.isBlank()) ? UUID.randomUUID().toString() : requestId;
		return passthrough("tech-news/extract", () -> techNewsAlgoClient.extract(body, persist, rid));
	}

	public Map<String, Object> list(int limit, int offset) {
		return passthrough("tech-news/extractions", () -> techNewsAlgoClient.list(limit, offset));
	}

	public Map<String, Object> get(String requestId) {
		return passthrough("tech-news/extractions/" + requestId, () -> techNewsAlgoClient.get(requestId));
	}

	public Map<String, Object> entityExtract(Map<String, Object> body, boolean persist, String requestId) {
		String rid = (requestId == null || requestId.isBlank()) ? UUID.randomUUID().toString() : requestId;
		return passthrough("tech-news/entity-extract", () -> techNewsAlgoClient.entityExtract(body, persist, rid));
	}

	public Map<String, Object> listEntityExtractions(int limit, int offset, String q) {
		return passthrough("tech-news/entity-extractions",
				() -> techNewsAlgoClient.listEntityExtractions(limit, offset, q));
	}

	public Map<String, Object> getEntityExtraction(String requestId) {
		return passthrough("tech-news/entity-extractions/" + requestId,
				() -> techNewsAlgoClient.getEntityExtraction(requestId));
	}

	private Map<String, Object> passthrough(String label, Supplier<Map<String, Object>> call) {
		try {
			return call.get();
		}
		catch (Exception ex) {
			log.warn("[tech-news] passthrough {} failed: {}", label, ex.getMessage());
			Map<String, Object> fallback = new LinkedHashMap<>();
			fallback.put("error", Map.of("code", "upstream_unavailable", "message",
					"科技新闻抽取服务暂不可达: " + ex.getMessage()));
			fallback.put("events", List.of());
			fallback.put("entities", List.of());
			return fallback;
		}
	}

}
