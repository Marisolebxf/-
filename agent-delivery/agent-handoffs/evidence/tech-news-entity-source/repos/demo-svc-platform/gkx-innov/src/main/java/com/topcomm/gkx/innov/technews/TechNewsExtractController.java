/*
 *
 *      Copyright (c) 2018-2026, gkx All rights reserved.
 *
 *  Author: gkx
 *
 */

package com.topcomm.gkx.innov.technews;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * 科技新闻四要素抽取 REST 门面（E-TECH-NEWS-IE-M1-L02 Phase B）。
 * <p>
 * 对内路径：{@code /v1/tech-news/**}；网关：{@code /innov/v1/tech-news/**}。
 * 仅转发 Python，不写抽取算法。
 *
 * @author gkx
 */
@RestController
@RequestMapping("/v1/tech-news")
@RequiredArgsConstructor
public class TechNewsExtractController {

	private final TechNewsExtractService techNewsExtractService;

	@PostMapping("/extract")
	public Map<String, Object> extract(@RequestBody Map<String, Object> body,
			@RequestParam(name = "persist", defaultValue = "true") boolean persist,
			@RequestHeader(name = "X-Request-Id", required = false) String requestId) {
		return techNewsExtractService.extract(body, persist, requestId);
	}

	@GetMapping("/extractions")
	public Map<String, Object> list(@RequestParam(name = "limit", defaultValue = "20") int limit,
			@RequestParam(name = "offset", defaultValue = "0") int offset) {
		return techNewsExtractService.list(limit, offset);
	}

	@GetMapping("/extractions/{requestId}")
	public Map<String, Object> get(@PathVariable String requestId) {
		return techNewsExtractService.get(requestId);
	}

	/**
	 * 实体扩展抽取（E-TECH-NEWS-ENTITY-M2-L02）：7 类实体 + event_type。
	 */
	@PostMapping("/entity-extract")
	public Map<String, Object> entityExtract(@RequestBody Map<String, Object> body,
			@RequestParam(name = "persist", defaultValue = "true") boolean persist,
			@RequestHeader(name = "X-Request-Id", required = false) String requestId) {
		return techNewsExtractService.entityExtract(body, persist, requestId);
	}

	/**
	 * 实体扩展历史列表（E-TECH-NEWS-ENTITY-M3-L02）：转发 Python entity-extractions。
	 */
	@GetMapping("/entity-extractions")
	public Map<String, Object> listEntityExtractions(
			@RequestParam(name = "limit", defaultValue = "20") int limit,
			@RequestParam(name = "offset", defaultValue = "0") int offset,
			@RequestParam(name = "q", required = false) String q) {
		return techNewsExtractService.listEntityExtractions(limit, offset, q);
	}

	@GetMapping("/entity-extractions/{requestId}")
	public Map<String, Object> getEntityExtraction(@PathVariable String requestId) {
		return techNewsExtractService.getEntityExtraction(requestId);
	}

}
