# K8s 환경에서의 Spring 프로파일 및 설정 우선순위 이슈

Spring Boot 애플리케이션을 Kubernetes(K8s)에 배포할 때, 로컬 환경과 달리 설정(Property)이 의도하지 않은 순서로 덮어씌워져 장애가 발생하는 경우가 있습니다. 이는 Spring Boot의 '외부 설정 우선순위' 메커니즘에 대한 이해 부족에서 기인합니다.

---

## 1. 이슈 배경: "왜 내가 설정한 프로파일이 안 먹히지?"

**상황**:
애플리케이션 내부 `application.yaml`에는 `test` 프로파일이 활성화되어 있으나, K8s Deployment의 환경 변수(Environment Variable)로 `prod`를 주입했을 때 특정 설정값이 꼬이는 현상 발생.

**핵심 원인**:
Spring Boot는 설정을 읽어올 때 정해진 **우선순위(Hierarchy)**가 있으며, K8s의 ConfigMap, Secret, Env Var 방식에 따라 이 순서가 달라집니다.

---

## 2. Spring Boot 외부 설정 우선순위 (요약)

우선순위가 높은 순서대로 나열하면 다음과 같습니다 (높을수록 아래 설정을 덮어씀):

1. **Command Line Arguments**: `--spring.profiles.active=prod`
2. **Java System Properties**: `-Dspring.profiles.active=prod`
3. **OS Environment Variables**: `SPRING_PROFILES_ACTIVE=prod`
4. **Application Properties (Jar 외부)**: `application-{profile}.yaml`
5. **Application Properties (Jar 내부)**: `application-{profile}.yaml`
6. **Default Properties**: `application.yaml`

---

## 3. K8s 배포 시 주요 충돌 사례

### 3.1 Env Var vs Command Line

* **문제**: Dockerfile의 `ENTRYPOINT`에 `--spring.profiles.active=dev`를 고정해두고, K8s YAML의 `env` 섹션에서 `SPRING_PROFILES_ACTIVE=prod`를 주입하는 경우.
* **결과**: **Command Line Arguments가 우선순위가 더 높기 때문에** K8s에서 주입한 `prod`는 무시되고 `dev`로 실행됩니다.

### 3.2 ConfigMap 마운트 위치에 따른 차이

* **상황**: ConfigMap을 파일로 마운트하여 `/config/application.yaml`에 위치시키는 경우.
* **결과**: 이는 'Jar 외부의 설정 파일'로 인식되어 'Jar 내부의 프로파일 전용 설정(`application-prod.yaml`)'보다 우선순위가 낮을 수 있습니다. (Spring Boot 2.4 미만 버전에서 특히 혼동됨)

---

## 4. 해결 방법 및 권장 사항

### 4.1 우선순위 명확화
가장 확실한 방법은 K8s Deployment의 `args` 섹션을 사용하여 명시적으로 우선순위를 부여하는 것입니다.
```yaml
spec:
  containers:
  - name: my-app
    image: my-app:latest
    args: ["--spring.profiles.active=$(PHASE)"] # 환경 변수를 인자로 전달 (최고 순위)
    env:
    - name: PHASE
      value: "prod"
```

### 4.2 Spring Boot 2.4+ `spring.config.import` 활용
최신 버전에서는 설정 파일 내에서 외부 설정을 명시적으로 가져올 수 있습니다.
```yaml
# application.yaml
spring:
  config:
    import: "optional:configtree:/etc/config/" # K8s ConfigMap 마운트 경로
```

### 4.3 고급 해결책: 프로그래밍 방식의 설정 제어 (BeanPostProcessor & Ordered)
설정 우선순위가 너무 복잡하여 휴먼 에러가 발생할 가능성이 높다면, **`BeanPostProcessor`**를 사용하여 특정 빈(Bean)의 속성을 프로파일에 따라 강제로 주입하거나 검증할 수 있습니다.

#### 🛠 구현 예시: 프로파일별 Bean 속성 강제 교정
```java
@Component
public class ProfileSpecificSettingPostProcessor implements BeanPostProcessor, PriorityOrdered {

    @Autowired
    private Environment env;

    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        // 특정 프로파일(예: prod)에서 절대 허용하면 안 되는 설정을 강제로 교정하거나 검증
        if (Arrays.asList(env.getActiveProfiles()).contains("prod")) {
            if (bean instanceof DataSource) {
                // 실 운영 환경에서 로컬/테스트 DB 연결 시도를 원천 차단하는 로직 등
            }
        }
        return bean;
    }

    @Override
    public int getOrder() {
        // 우선순위를 가장 높게 설정하여 다른 설정보다 먼저 혹은 나중에 적용되도록 제어
        return Ordered.HIGHEST_PRECEDENCE;
    }
}
```

* **`BeanPostProcessor`**: 빈의 초기화 단계에 개입하여 프로파일에 따른 커스텀 로직을 수행합니다.
* **`Ordered` / `PriorityOrdered`**: 여러 설정 로직이 충돌할 때, 이 프로세서가 실행될 정확한 순서를 보장하여 우선순위 역전을 방지합니다.

---

## 5. 교훈

* K8s 환경에서는 **환경 변수(Env)**보다 **실행 인자(Args)**가 우선순위가 높음을 항상 인지해야 합니다.
* 배포 로그 상단에 출력되는 `The following profiles are active: ...` 메시지를 반드시 확인하여 의도한 프로파일이 로드되었는지 검증해야 합니다.
