# OAuth 2.0 (Open Authorization 2.0)

**OAuth 2.0**은 리소스 소유자(사용자)가 클라이언트(애플리케이션)에게 자신의 리소스에 접근할 수 있는 권한을 위임하는 개방형 표준 프로토콜입니다.

## 📌 주요 역할 (Roles)

1.  **Resource Owner (리소스 소유자)**
    *   보호된 자원의 소유자이며, 클라이언트에게 접근 권한을 부여하는 사용자입니다.
2.  **Client (클라이언트)**
    *   사용자를 대신하여 보호된 자원에 접근하려는 애플리케이션입니다.
3.  **Authorization Server (권한 서버)**
    *   사용자의 신원을 인증하고, 권한이 확인되면 Access Token을 발급하는 서버입니다. (예: Google, Kakao, Keycloak 등)
4.  **Resource Server (리소스 서버)**
    *   Access Token을 검증하고, 유효한 요청에 대해 보호된 자원을 제공하는 서버입니다.

## 🔄 주요 권한 부여 방식 (Grant Types)

1.  **Authorization Code Grant (권한 코드 방식)**
    *   가장 널리 사용되는 방식입니다.
    *   사용자가 권한 서버에서 로그인 후, `Authorization Code`를 받아 클라이언트에게 전달하고, 클라이언트는 이 코드로 다시 `Access Token`을 요청합니다.
    *   토큰이 사용자 브라우저에 직접 노출되지 않아 보안성이 높습니다.
2.  **Implicit Grant (암시적 승인 방식)**
    *   SPA(Single Page Application)와 같이 백엔드 서버가 없는 환경에서 주로 사용되었습니다. (현재는 PKCE를 적용한 Authorization Code 방식을 권장합니다.)
3.  **Resource Owner Password Credentials Grant**
    *   사용자의 ID/Password를 직접 받아 토큰을 발급받습니다. 클라이언트를 전적으로 신뢰할 수 있는 경우에만 사용합니다.
4.  **Client Credentials Grant**
    *   사용자 개입 없이, 클라이언트 자신이 리소스에 접근할 때 사용합니다. (서버 간 통신 등)

## 🔑 토큰 (Tokens)

*   **Access Token**: 리소스 서버에 접근하기 위한 열쇠입니다. 유효 기간이 짧습니다.
*   **Refresh Token**: Access Token이 만료되었을 때, 새로운 Access Token을 발급받기 위해 사용합니다. 유효 기간이 깁니다.
