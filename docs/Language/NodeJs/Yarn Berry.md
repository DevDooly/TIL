# Yarn Berry (Yarn v2+)

**Yarn Berry**는 Yarn 패키지 매니저의 v2 이상 버전을 의미하며, 기존 Node.js 패키지 관리 시스템(`node_modules`)의 한계를 극복하기 위해 **Plug'n'Play (PnP)** 전략을 도입했습니다.

## 1. 기존 `node_modules`의 문제점
*   **비효율적인 탐색:** 파일을 찾기 위해 상위 디렉토리를 계속 타고 올라가며 I/O가 많이 발생합니다.
*   **유령 의존성 (Phantom Dependency):** 내가 설치하지 않은 의존성의 의존성(하위 패키지)을 `require` 할 수 있는 문제가 있습니다.
*   **무거운 용량:** 프로젝트마다 거대한 `node_modules` 폴더가 생성되어 디스크 공간을 많이 차지합니다.

## 2. Plug'n'Play (PnP)
Yarn Berry는 `node_modules` 폴더를 생성하지 않습니다. 대신 **`.pnp.cjs`** 라는 파일에 패키지의 위치와 의존성 정보를 매핑하여 저장합니다.
*   **Zip 아카이브:** 패키지들을 압축 파일(`.zip`) 형태로 캐시(`bucket`)에 저장하여 용량을 줄이고 로딩 속도를 높입니다.
*   **Zero-Install:** 의존성 파일(Zip)까지 git에 포함시켜, `yarn install` 없이 바로 프로젝트를 실행할 수 있게 하는 전략도 가능합니다.

## 참고
*   [Yarn 공식 사이트](https://yarnpkg.com/)
*   [Toss Tech - node_modules로부터 우리를 구원해 줄 Yarn Berry](https://toss.tech/article/node-modules-and-yarn-berry)