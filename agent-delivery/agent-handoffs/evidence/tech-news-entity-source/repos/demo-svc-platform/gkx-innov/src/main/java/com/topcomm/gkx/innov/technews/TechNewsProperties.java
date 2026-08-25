/*
 *
 *      Copyright (c) 2018-2026, gkx All rights reserved.
 *
 *  Author: gkx
 *
 */

package com.topcomm.gkx.innov.technews;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

/**
 * 科技新闻抽取门面配置。
 *
 * @author gkx
 */
@Data
@Component
@ConfigurationProperties(prefix = "gkx.innov.tech-news")
public class TechNewsProperties {

	/** innov-py 基址（暴露 /internal/tech-news/*）。 */
	private String algoBaseUrl = "http://127.0.0.1:8000";

	/** HTTP 读超时毫秒（抽取含 LLM，建议 ≥30000）。 */
	private long readTimeoutMs = 30000L;

}
