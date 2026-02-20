# Spring Boot OAuth2 Implementation

Spring Boot에서 **Spring Security**를 사용하여 OAuth 2.0 Login(Client) 및 Resource Server를 구현하는 방법을 설명합니다.

## 📦 의존성 추가 (build.gradle)

OAuth2 Client 기능을 사용하기 위해 `spring-boot-starter-oauth2-client` 의존성을 추가합니다. Resource Server라면 `spring-boot-starter-oauth2-resource-server`가 필요합니다.

```groovy
dependencies {
    // OAuth2 Client (로그인 등)
    implementation 'org.springframework.boot:spring-boot-starter-oauth2-client'
    
    // Spring Security
    implementation 'org.springframework.boot:spring-boot-starter-security'
    
    // Web
    implementation 'org.springframework.boot:spring-boot-starter-web'
}
```

## ⚙️ 설정 (application.yml)

Google, GitHub, Kakao 등 외부 Provider 정보를 설정합니다. `registration`에는 클라이언트 ID/Secret을, `provider`에는 토큰 발급/사용자 정보 조회 URI를 명시합니다. (Google, GitHub 등은 Spring Security가 기본 제공하므로 `provider` 설정 생략 가능)

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          google:
            client-id: "YOUR_GOOGLE_CLIENT_ID"
            client-secret: "YOUR_GOOGLE_CLIENT_SECRET"
            scope:
              - email
              - profile
          kakao:
            client-id: "YOUR_KAKAO_CLIENT_ID"
            client-secret: "YOUR_KAKAO_CLIENT_SECRET"
            authorization-grant-type: authorization_code
            redirect-uri: "{baseUrl}/login/oauth2/code/{registrationId}"
            client-authentication-method: POST
            client-name: Kakao
        provider:
          kakao:
            authorization-uri: https://kauth.kakao.com/oauth/authorize
            token-uri: https://kauth.kakao.com/oauth/token
            user-info-uri: https://kapi.kakao.com/v2/user/me
            user-name-attribute: id
```

## 🛡️ SecurityConfig 설정

`SecurityFilterChain` 빈을 등록하여 OAuth2 로그인을 활성화합니다.

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(authorize -> authorize
                .requestMatchers("/", "/login**", "/error").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2Login(oauth2 -> oauth2
                .defaultSuccessUrl("/home") // 로그인 성공 시 이동할 URL
                .failureUrl("/login?error") // 로그인 실패 시 이동할 URL
                .userInfoEndpoint(userInfo -> userInfo
                    .userService(customOAuth2UserService) // 사용자 정보 후처리 서비스 등록 (선택)
                )
            );

        return http.build();
    }
}
```

## 👤 사용자 정보 처리 (CustomOAuth2UserService)

로그인 성공 후 가져온 사용자 정보(attributes)를 기반으로 회원 가입이나 정보 업데이트 로직을 수행하려면 `DefaultOAuth2UserService`를 상속받아 구현합니다.

```java
@Service
public class CustomOAuth2UserService extends DefaultOAuth2UserService {

    @Override
    public OAuth2User loadUser(OAuth2UserRequest userRequest) throws OAuth2AuthenticationException {
        OAuth2User oAuth2User = super.loadUser(userRequest);
        
        // 제공자 정보 (google, kakao, ...)
        String registrationId = userRequest.getClientRegistration().getRegistrationId();
        
        // 사용자 정보 속성 맵
        Map<String, Object> attributes = oAuth2User.getAttributes();
        
        // TODO: DB 저장 또는 업데이트 로직 구현
        
        return new DefaultOAuth2User(
            Collections.singleton(new SimpleGrantedAuthority("ROLE_USER")),
            attributes,
            userRequest.getClientRegistration().getProviderDetails()
                .getUserInfoEndpoint().getUserNameAttributeName()
        );
    }
}
```
