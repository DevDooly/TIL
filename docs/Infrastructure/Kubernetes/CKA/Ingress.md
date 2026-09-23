# 3.2 인그레스 라우팅 (Ingress)

**인그레스(Ingress)**는 클러스터 외부에서 내부 서비스로 들어오는 HTTP 및 HTTPS 트래픽을 호스트(도메인) 또는 경로(URL Path)를 기준으로 라우팅해주는 L7 로드밸런서 역할을 수행합니다.

---

## 1. Ingress와 Ingress Controller의 관계

- **Ingress Resource**: 어떤 트래픽을 어느 서비스로 보낼지 정의한 규칙(YAML)입니다.
- **Ingress Controller**: 실제로 트래픽을 프록시하고 규칙을 실행하는 소프트웨어입니다(예: Ingress-NGINX, Traefik). 컨트롤러가 클러스터에 설치되어 있어야 Ingress 리소스가 동작합니다.

---

## 2. Ingress YAML 기본 구조 (networking.k8s.io/v1)

> [!IMPORTANT]
> CKA 시험에서는 `networking.k8s.io/v1` API를 사용합니다. `pathType`을 명시해야 하며, 백엔드 서비스 지정 형식이 `backend.service.name`과 `backend.service.port.number` 구조입니다.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
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

---

## 3. 명령형 커맨드로 빠르게 Ingress 생성하기

`kubectl create ingress` 명령어를 사용하면 복잡한 Ingress YAML을 단 1초 만에 뼈대로 생성할 수 있습니다.

```bash
# 기본 단일 경로 인그레스 생성
kubectl create ingress test-ingress \
  --rule="myapp.example.com/api*=api-service:8080" \
  --class=nginx \
  --dry-run=client -o yaml > ingress.yaml
```

---

## 4. 실전 검증 방법

외부 DNS 등록이 되어 있지 않은 로컬/시험 환경에서는 `curl` 명령에 `-H` 옵션으로 Host 헤더를 주어 라우팅을 검증합니다.

```bash
# Ingress Controller 파드나 노드 IP로 요청을 보내며 Host 헤더 전달
curl -H "Host: myapp.example.com" http://<node-ip-or-ingress-ip>/wear
curl -H "Host: myapp.example.com" http://<node-ip-or-ingress-ip>/watch
```

---

## 💡 CKA 시험 실전 팁

1. **공식 문서 검색어**: `ingress`
2. 공식 문서 페이지에서 **"The Ingress resource"** 항목의 예제 YAML을 찾아 복사한 뒤, 문제에서 요구하는 `host`, `path`, `service.name`, `service.port.number`만 바꿔 끼우면 가장 안전합니다.
3. 문제에서 `ingressClassName`을 지정하라고 하면(예: `spec.ingressClassName: nginx`), YAML의 `spec` 바로 아래에 기재해야 합니다.
