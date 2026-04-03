package com.example.logging;

import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.LayoutBase;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.Map;

public class CustomEcsJsonLayout extends LayoutBase<ILoggingEvent> {

    // Spring Boot에 기본 내장된 Jackson ObjectMapper 재사용
    private static final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public String doLayout(ILoggingEvent event) {
        // 순서를 보장하기 위해 LinkedHashMap 사용
        Map<String, Object> logMap = new LinkedHashMap<>();

        // 1. 기본 로그 정보 맵핑 (원하는 ECS 스키마 형태에 맞게 수정 가능)
        logMap.put("@timestamp", Instant.ofEpochMilli(event.getTimeStamp()).toString());
        logMap.put("log.level", event.getLevel().toString());
        logMap.put("message", event.getFormattedMessage());
        logMap.put("logger.name", event.getLoggerName());
        logMap.put("thread.name", event.getThreadName());

        // 2. 핵심! 유동적인 키 (MDC) 처리
        Map<String, String> mdcMap = event.getMDCPropertyMap();
        if (mdcMap != null && !mdcMap.isEmpty()) {
            // MDC 안에 있는 유동적인 key-value를 JSON 최상위에 동적으로 모두 추가
            logMap.putAll(mdcMap); 
        }

        try {
            // Map을 JSON 문자열로 변환하고 줄바꿈 추가
            return objectMapper.writeValueAsString(logMap) + "\n";
        } catch (Exception e) {
            // 파싱 실패 시 대비책 (일반적으로 발생하지 않음)
            return "{ \"log.level\": \"ERROR\", \"message\": \"Failed to parse log to JSON\" }\n";
        }
    }
}

