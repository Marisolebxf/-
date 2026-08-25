/*
 *
 *      Copyright (c) 2018-2026, gkxlumen All rights reserved.
 *
 *  Author: gkxlumen
 *
 */

package com.topcomm.gkxlumen.innov.technews;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import jakarta.annotation.PostConstruct;
import java.time.Duration;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * 科技新闻抽取门面：RestTemplate 透传 Python /internal/tech-news/*。
 * <p>
 * 不引入 Feign，避免改动 innov 模块依赖边界；算法仍只在 Python。
 *
 * @author gkxlumen
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class TechNewsExtractService {

	private final TechNewsProperties properties;

	private final RestTemplateBuilder restTemplateBuilder;

	private RestTemplate restTemplate;

	@PostConstruct
	void init() {
		this.restTemplate = restTemplateBuilder
			.setConnectTimeout(Duration.ofMillis(properties.getConnectTimeoutMs()))
			.setReadTimeout(Duration.ofMillis(properties.getReadTimeoutMs()))
			.build();
	}

	@SuppressWarnings("unchecked")
	public Map<String, Object> extract(Map<String, Object> body, boolean persist, String requestId) {
		String rid = (requestId == null || requestId.isBlank()) ? UUID.randomUUID().toString() : requestId;
		String url = UriComponentsBuilder.fromHttpUrl(trimSlash(properties.getAlgoBaseUrl()))
			.path("/internal/tech-news/extract")
			.queryParam("persist", persist)
			.toUriString();
		HttpHeaders headers = new HttpHeaders();
		headers.setContentType(MediaType.APPLICATION_JSON);
		headers.set("X-Request-Id", rid);
		try {
			ResponseEntity<Map> resp = restTemplate.exchange(url, HttpMethod.POST, new HttpEntity<>(body, headers),
					Map.class);
			return resp.getBody() != null ? resp.getBody() : Map.of();
		}
		catch (RestClientException ex) {
			return upstreamError("extract", ex);
		}
	}

	@SuppressWarnings("unchecked")
	public Map<String, Object> list(int limit, int offset) {
		String url = UriComponentsBuilder.fromHttpUrl(trimSlash(properties.getAlgoBaseUrl()))
			.path("/internal/tech-news/extractions")
			.queryParam("limit", limit)
			.queryParam("offset", offset)
			.toUriString();
		try {
			ResponseEntity<Map> resp = restTemplate.exchange(url, HttpMethod.GET, HttpEntity.EMPTY, Map.class);
			return resp.getBody() != null ? resp.getBody() : Map.of();
		}
		catch (RestClientException ex) {
			return upstreamError("list", ex);
		}
	}

	@SuppressWarnings("unchecked")
	public Map<String, Object> get(String requestId) {
		String url = UriComponentsBuilder.fromHttpUrl(trimSlash(properties.getAlgoBaseUrl()))
			.path("/internal/tech-news/extractions/{requestId}")
			.buildAndExpand(requestId)
			.toUriString();
		try {
			ResponseEntity<Map> resp = restTemplate.exchange(url, HttpMethod.GET, HttpEntity.EMPTY, Map.class);
			return resp.getBody() != null ? resp.getBody() : Map.of();
		}
		catch (RestClientException ex) {
			return upstreamError("get", ex);
		}
	}

	@SuppressWarnings("unchecked")
	public Map<String, Object> entityExtract(Map<String, Object> body, boolean persist, String requestId) {
		String rid = (requestId == null || requestId.isBlank()) ? UUID.randomUUID().toString() : requestId;
		String url = UriComponentsBuilder.fromHttpUrl(trimSlash(properties.getAlgoBaseUrl()))
			.path("/internal/tech-news/entity-extract")
			.queryParam("persist", persist)
			.toUriString();
		HttpHeaders headers = new HttpHeaders();
		headers.setContentType(MediaType.APPLICATION_JSON);
		headers.set("X-Request-Id", rid);
		try {
			ResponseEntity<Map> resp = restTemplate.exchange(url, HttpMethod.POST, new HttpEntity<>(body, headers),
					Map.class);
			return resp.getBody() != null ? resp.getBody() : Map.of();
		}
		catch (RestClientException ex) {
			return upstreamError("entity-extract", ex);
		}
	}

	@SuppressWarnings("unchecked")
	public Map<String, Object> listEntityExtractions(int limit, int offset, String q) {
		UriComponentsBuilder b = UriComponentsBuilder.fromHttpUrl(trimSlash(properties.getAlgoBaseUrl()))
			.path("/internal/tech-news/entity-extractions")
			.queryParam("limit", limit)
			.queryParam("offset", offset);
		if (q != null && !q.isBlank()) {
			b.queryParam("q", q);
		}
		String url = b.toUriString();
		try {
			ResponseEntity<Map> resp = restTemplate.exchange(url, HttpMethod.GET, HttpEntity.EMPTY, Map.class);
			return resp.getBody() != null ? resp.getBody() : Map.of();
		}
		catch (RestClientException ex) {
			return upstreamError("entity-extractions", ex);
		}
	}

	@SuppressWarnings("unchecked")
	public Map<String, Object> getEntityExtraction(String requestId) {
		String url = UriComponentsBuilder.fromHttpUrl(trimSlash(properties.getAlgoBaseUrl()))
			.path("/internal/tech-news/entity-extractions/{requestId}")
			.buildAndExpand(requestId)
			.toUriString();
		try {
			ResponseEntity<Map> resp = restTemplate.exchange(url, HttpMethod.GET, HttpEntity.EMPTY, Map.class);
			return resp.getBody() != null ? resp.getBody() : Map.of();
		}
		catch (RestClientException ex) {
			return upstreamError("entity-extractions/" + requestId, ex);
		}
	}

	private Map<String, Object> upstreamError(String label, Exception ex) {
		log.warn("[tech-news] {} failed: {}", label, ex.getMessage());
		Map<String, Object> fallback = new LinkedHashMap<>();
		fallback.put("error", Map.of("code", "upstream_unavailable", "message",
				"科技新闻抽取服务暂不可达: " + ex.getMessage()));
		fallback.put("events", List.of());
		fallback.put("entities", List.of());
		return fallback;
	}

	private static String trimSlash(String base) {
		if (base == null || base.isBlank()) {
			return "http://127.0.0.1:8000";
		}
		return base.endsWith("/") ? base.substring(0, base.length() - 1) : base;
	}

}
