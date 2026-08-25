/*
 *
 *      Copyright (c) 2018-2026, gkx All rights reserved.
 *
 *  Author: gkx
 *
 */

package com.topcomm.gkx.innov.technews;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.Map;

/**
 * 科技新闻四要素抽取 Python 客户端（demo-algo-science /internal/tech-news/*）。
 * <p>
 * 架构铁律：算法只在 Python；Java 仅 Feign 透传，不写 NLP / LLM / 抽取逻辑。
 *
 * @author gkx
 */
@FeignClient(contextId = "techNewsAlgoClient", name = "tech-news-algo",
		url = "${gkx.innov.tech-news.algo-base-url:${gkx.innov.chain.algo-base-url:http://127.0.0.1:8000}}")
public interface TechNewsAlgoClient {

	@PostMapping("/internal/tech-news/extract")
	Map<String, Object> extract(@RequestBody Map<String, Object> body,
			@RequestParam(name = "persist", defaultValue = "true") boolean persist,
			@RequestHeader(name = "X-Request-Id", required = false) String requestId);

	@GetMapping("/internal/tech-news/extractions")
	Map<String, Object> list(@RequestParam(name = "limit", defaultValue = "20") int limit,
			@RequestParam(name = "offset", defaultValue = "0") int offset);

	@GetMapping("/internal/tech-news/extractions/{requestId}")
	Map<String, Object> get(@PathVariable("requestId") String requestId);

	@PostMapping("/internal/tech-news/entity-extract")
	Map<String, Object> entityExtract(@RequestBody Map<String, Object> body,
			@RequestParam(name = "persist", defaultValue = "true") boolean persist,
			@RequestHeader(name = "X-Request-Id", required = false) String requestId);

	@GetMapping("/internal/tech-news/entity-extractions")
	Map<String, Object> listEntityExtractions(@RequestParam(name = "limit", defaultValue = "20") int limit,
			@RequestParam(name = "offset", defaultValue = "0") int offset,
			@RequestParam(name = "q", required = false) String q);

	@GetMapping("/internal/tech-news/entity-extractions/{requestId}")
	Map<String, Object> getEntityExtraction(@PathVariable("requestId") String requestId);

}
