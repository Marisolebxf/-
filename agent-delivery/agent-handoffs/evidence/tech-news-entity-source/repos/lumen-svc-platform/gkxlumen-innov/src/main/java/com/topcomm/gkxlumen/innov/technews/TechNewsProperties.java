/*
 *
 *      Copyright (c) 2018-2026, gkxlumen All rights reserved.
 *
 *  Author: gkxlumen
 *
 */

package com.topcomm.gkxlumen.innov.technews;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

/**
 * 科技新闻抽取门面配置（E-TECH-NEWS-IE-M1-L02）。
 *
 * @author gkxlumen
 */
@Data
@Component
@ConfigurationProperties(prefix = "gkxlumen.innov.tech-news")
public class TechNewsProperties {

	/** innov-py 基址。 */
	private String algoBaseUrl = "http://127.0.0.1:8000";

	/** 连接超时毫秒。 */
	private long connectTimeoutMs = 5000L;

	/** 读超时毫秒（抽取含 LLM，建议 ≥30000）。 */
	private long readTimeoutMs = 30000L;

}
