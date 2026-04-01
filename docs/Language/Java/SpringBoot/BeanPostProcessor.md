# 빈 후처리기 (BeanPostProcessor)

Spring 프레임워크에서 `BeanPostProcessor`는 스프링 컨테이너가 빈(Bean) 객체를 생성하고 초기화하는 라이프사이클 중간에 개입하여 **빈 객체를 조작하거나 완전히 다른 객체(주로 프록시)로 바꿔치기할 수 있는 강력한 확장 포인트**입니다.

## 1. 역할과 위치

`BeanPostProcessor`는 빈의 **초기화(Initialization) 단계 전후**에 동작합니다.

> 빈 인스턴스화(생성) ➡️ 의존성 주입 ➡️ **[초기화 전 후처리]** ➡️ 초기화 콜백(`@PostConstruct` 등) ➡️ **[초기화 후 후처리]** ➡️ 빈 사용 가능

이 메커니즘은 스프링 내부의 '마법'같은 기능들의 핵심입니다. 예를 들어, 어노테이션 기반의 설정 처리(`@Autowired`, `@Required`), 그리고 가장 중요하게는 **AOP(Aspect-Oriented Programming) 프록시 생성**이 모두 이 빈 후처리기를 통해 이루어집니다.

---

## 2. 주요 메서드

`BeanPostProcessor` 인터페이스는 두 개의 디폴트 메서드를 제공합니다.

### 2.1 `postProcessBeforeInitialization`
```java
default Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
    return bean;
}
```

*   **시점**: 빈 생성자와 의존성 주입이 완료된 후, 초기화 콜백(`@PostConstruct`, `InitializingBean.afterPropertiesSet` 등)이 **호출되기 직전**에 실행됩니다.
*   **용도**: 초기화 전에 빈의 상태를 확인하거나 프로퍼티를 변경할 때 주로 사용됩니다.

### 2.2 `postProcessAfterInitialization`
```java
default Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
    return bean;
}
```

*   **시점**: 빈의 초기화 콜백이 모두 **완료된 직후**에 실행됩니다.
*   **용도**: **AOP의 핵심**입니다. 이 시점에 생성된 실제 원본 빈(Target)을 감싸는 **프록시(Proxy) 객체를 생성하여 반환**하면, 스프링 컨테이너에는 원본 빈 대신 프록시 객체가 빈으로 등록됩니다.

> 💡 **참고**: 두 메서드 모두 반환값(`return`)이 중요합니다. 여기서 반환한 객체가 최종적으로 스프링 컨테이너에 빈으로 등록됩니다. `null`을 반환하면 다음 후처리기가 실행되지 않고 해당 빈의 초기화 작업이 중단될 수 있으므로, 조작할 필요가 없는 빈이라도 그대로 `return bean;` 을 해주어야 합니다.

---

## 3. AOP와 BeanPostProcessor의 관계

Spring AOP가 동작하는 원리가 바로 이 빈 후처리기, 그 중에서도 **`AnnotationAwareAspectJAutoProxyCreator`**라는 특수한 빈 후처리기 덕분입니다.

1.   스프링 컨테이너는 등록된 모든 빈 후처리기를 찾습니다.
2.   일반적인 빈들이 생성되고 초기화 단계에 돌입합니다.
3.   `postProcessAfterInitialization` 단계에서 `AutoProxyCreator`가 동작합니다.
4.   이 빈 후처리기는 컨테이너 내의 모든 어드바이저(Advisor: Pointcut + Advice)를 조회합니다.
5.   현재 생성된 빈이 Pointcut의 대상이 되는지(즉, AOP 적용 대상인지) 확인합니다.
6.   대상이 맞다면, 원본 객체 대신 **프록시 객체를 생성하여 반환**합니다. 대상이 아니라면 원본 객체를 그대로 반환합니다.
7.   결과적으로 컨테이너에는 (AOP 대상인 경우) 프록시 객체가 빈으로 등록되어, 클라이언트가 빈을 호출할 때 프록시를 거쳐 부가 기능(Advice)이 실행됩니다.

---

## 4. 예제: 커스텀 BeanPostProcessor 만들기

특정 어노테이션이 붙은 빈의 동작을 가로채서 프록시를 씌우는 아주 간단한 커스텀 후처리기 예시입니다.

```java
import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.stereotype.Component;

import java.lang.reflect.Proxy;

@Component
public class MyCustomBeanPostProcessor implements BeanPostProcessor {

    // 1. 초기화 전 처리 (여기서는 원본 그대로 통과)
    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        return bean;
    }

    // 2. 초기화 후 처리 (프록시 씌우기)
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        
        // 대상 빈이 내 패키지의 클래스인지 확인 (모든 빈을 건드리면 시스템 오류 발생 가능)
        String packageName = bean.getClass().getPackageName();
        if (!packageName.startsWith("com.myapp")) {
            return bean;
        }

        // 대상 빈에 로깅 프록시를 적용하여 반환
        return Proxy.newProxyInstance(
                bean.getClass().getClassLoader(),
                bean.getClass().getInterfaces(),
                (proxy, method, args) -> {
                    System.out.println("👉 [Log] Method call: " + method.getName());
                    Object result = method.invoke(bean, args);
                    System.out.println("👈 [Log] Method end: " + method.getName());
                    return result;
                }
        );
    }
}
```

> **주의**: BeanPostProcessor는 스프링 컨테이너의 핵심 라이프사이클에 관여하므로, 구현 시 실수(예: 엉뚱한 타입 반환, `null` 반환, 무한 루프 등)를 하면 컨테이너 부팅 자체가 실패할 수 있습니다. 특히 `postProcessAfterInitialization`에서 프록시를 생성할 때는 대상 빈이 인터페이스를 구현했는지(JDK Dynamic Proxy), 아니면 구체 클래스인지(CGLIB)를 고려해야 합니다.
