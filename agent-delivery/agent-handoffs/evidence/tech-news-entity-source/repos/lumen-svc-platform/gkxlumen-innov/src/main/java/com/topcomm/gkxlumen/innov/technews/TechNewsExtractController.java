/*
 *
 *      Copyright (c) 2018-2026, gkxlumen All rights reserved.
 *
 *  Author: gkxlumen
 *
 */

package com.topcomm.gkxlumen.innov.technews;

import com.topcomm.gkxlumen.common.core.util.R;
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
 * 网关：{@code /api/innov/v1/tech-news/**} → 本服务 {@code /v1/tech-news/**}。
 * Java 不写抽取算法，仅鉴权后转发 Python。
 *
 * @author gkxlumen
 */
@RestController
@RequestMapping("/v1/tech-news")
@RequiredArgsConstructor
public class TechNewsExtractController {

	private final TechNewsExtractService techNewsExtractService;

	@PostMapping("/extract")
	public R<Map<String, Object>> extract(@RequestBody Map<String, Object> body,
			@RequestParam(name = "persist", defaultValue = "true") boolean persist,
			@RequestHeader(name = "X-Request-Id", required = false) String requestId) {
		return R.ok(techNewsExtractService.extract(body, persist, requestId));
	}

	@GetMapping("/extractions")
	public R<Map<String, Object>> list(@RequestParam(name = "limit", defaultValue = "20") int limit,
			@RequestParam(name = "offset", defaultValue = "0") int offset) {
		return R.ok(techNewsExtractService.list(limit, offset));
	}

	@GetMapping("/extractions/{requestId}")
	public R<Map<String, Object>> get(@PathVariable String requestId) {
		return R.ok(techNewsExtractService.get(requestId));
	}

	/**
	 * 实体扩展抽取（E-TECH-NEWS-ENTITY-M2-L02）：转发 Python /internal/tech-news/entity-extract。
	 */
	@PostMapping("/entity-extract")
	public R<Map<String, Object>> entityExtract(@RequestBody Map<String, Object> body,
			@RequestParam(name = "persist", defaultValue = "true") boolean persist,
			@RequestHeader(name = "X-Request-Id", required = false) String requestId) {
		return R.ok(techNewsExtractService.entityExtract(body, persist, requestId));
	}

	/**
	 * 实体扩展历史列表（E-TECH-NEWS-ENTITY-M3-L02）。
	 */
	@GetMapping("/entity-extractions")
	public R<Map<String, Object>> listEntityExtractions(
			@RequestParam(name = "limit", defaultValue = "20") int limit,
			@RequestParam(name = "offset", defaultValue = "0") int offset,
			@RequestParam(name = "q", required = false) String q) {
		return R.ok(techNewsExtractService.listEntityExtractions(limit, offset, q));
	}

	@GetMapping("/entity-extractions/{requestId}")
	public R<Map<String, Object>> getEntityExtraction(@PathVariable String requestId) {
		return R.ok(techNewsExtractService.getEntityExtraction(requestId));
	}

}
