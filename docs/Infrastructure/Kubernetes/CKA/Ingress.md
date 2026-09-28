# 3.2 인그레스 라우팅 (Ingress)

**인그레스(Ingress)**는 HTTP·HTTPS 트래픽을 호스트와 경로에 따라 Service로 보내는 규칙을 정의하는 리소스입니다. 실제 프록시·로드밸런싱은 Ingress Controller가 수행합니다.

---

## 1. Ingress와 Ingress Controller의 관계

- **Ingress Resource**: 어떤 트래픽을 어느 서비스로 보낼지 정의한 규칙(YAML)입니다.
- **Ingress Controller**: 실제로 트래픽을 프록시하고 규칙을 실행하는 소프트웨어입니다. 컨트롤러가 클러스터에 설치되어 있어야 Ingress 리소스가 동작합니다.

---

## 2. Ingress YAML 기본 구조 (networking.k8s.io/v1)

`kubectl get ingressclass`로 사용할 클래스를 확인하고 아래 `example`을 실제 이름으로 바꿉니다. 백엔드 Service와 Ingress는 같은 네임스페이스에 있어야 합니다.

!!! important

    CKA 시험에서는 `networking.k8s.io/v1` API를 사용합니다. `pathType`을 명시해야 하며, 백엔드 서비스 지정 형식이 `backend.service.name`과 `backend.service.port.number` 구조입니다.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  ingressClassName: example
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /wear
        pathType: Prefix
        backend:
          service:
            name: wear-service
            port:
              number: 80
      - path: /watch
        pathType: Prefix
        backend:
          service:
            name: watch-service
            port:
              number: 80
```

이 예제는 `/wear`, `/watch` 경로를 그대로 백엔드에 전달하므로 애플리케이션도 해당 경로에 응답해야 합니다. 경로 재작성은 컨트롤러별 기능과 설정을 확인합니다.

---

## 3. 명령형 커맨드로 빠르게 Ingress 생성하기

`kubectl create ingress` 명령어를 사용하면 복잡한 Ingress YAML을 뼈대로 생성할 수 있습니다.

```bash
# 기본 단일 경로 인그레스 생성
kubectl create ingress test-ingress \
  --rule="myapp.example.com/api*=api-service:8080" \
  --class=example \
  --dry-run=client -o yaml > ingress.yaml
```

---

## 4. 실전 검증 방법

외부 DNS 등록이 되어 있지 않은 로컬/시험 환경에서는 `curl` 명령에 `-H` 옵션으로 Host 헤더를 주어 라우팅을 검증합니다.

```bash
# 실제 Ingress Controller의 노출 주소와 포트로 요청한다.
curl -H "Host: myapp.example.com" http://<ingress-address>:<port>/wear
curl -H "Host: myapp.example.com" http://<ingress-address>:<port>/watch
```

---

## 💡 CKA 시험 실전 팁

1. **공식 문서 검색어**: `ingress`
2. 공식 예제에서 `host`, `path`, `pathType`, Service 이름·포트와 클래스를 요구사항에 맞게 수정합니다. 생성 후 `kubectl describe ingress <name>`과 실제 요청으로 확인합니다.
3. 문제에서 `ingressClassName`을 지정하라고 하면(예: `spec.ingressClassName: example`), YAML의 `spec` 바로 아래에 기재해야 합니다.

## 참고 자료

- [Kubernetes: Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Gateway API 학습](https://gateway-api.sigs.k8s.io/guides/): CKA 범위에 포함되므로 Ingress와 함께 실습합니다.
