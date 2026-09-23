# 2.4 설정 관리 (ConfigMaps & Secrets)

애플리케이션의 설정 정보(Configuration)와 민감한 인증 정보(Credentials)를 컨테이너 이미지와 분리하여 관리하는 쿠버네티스 핵심 오브젝트입니다. CKA 시험에서는 환경변수(ENV) 주입 또는 볼륨 마운트 방식으로 빈번하게 출제됩니다.

---

## 1. ConfigMap & Secret 개념

- **ConfigMap**: 일반 텍스트 형태의 설정값(포트, 환경명, 설정 파일 내용 등)을 Key-Value 형태로 저장합니다.
- **Secret**: 패스워드, API 토큰, TLS 인증서 등 민감한 정보를 Base64로 인코딩하여 저장합니다. (기본 타입: `Opaque`)

---

## 2. 생성 명령어 (Imperative Commands)

YAML을 직접 작성하지 않고 `kubectl create`를 사용하면 오타 없이 몇 초 만에 생성할 수 있습니다.

### 2.1 리터럴(Literal) 값으로 생성
```bash
# ConfigMap 생성
kubectl create configmap app-config \
  --from-literal=APP_ENV=production \
  --from-literal=MAX_THREADS=8

# Secret 생성
kubectl create secret generic app-secret \
  --from-literal=DB_PASSWORD=supersecret \
  --from-literal=API_KEY=xyz123
```

### 2.2 파일로부터 생성
```bash
# 설정 파일 내용 전체를 ConfigMap으로 저장
kubectl create configmap nginx-conf --from-file=nginx.conf

# 디렉터리 내의 모든 파일을 Secret으로 저장
kubectl create secret generic certs-secret --from-file=/path/to/certs/
```

---

## 3. 파드(Pod)에 주입하는 3가지 방법

### 방법 1: 특정 키를 개별 환경변수(`valueFrom`)로 주입
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: env-single-pod
spec:
  containers:
  - name: app
    image: nginx
    env:
    - name: MY_APP_ENV
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: APP_ENV
    - name: MY_DB_PW
      valueFrom:
        secretKeyRef:
          name: app-secret
          key: DB_PASSWORD
```

### 방법 2: 모든 키를 한 번에 환경변수(`envFrom`)로 주입
ConfigMap/Secret의 모든 Key-Value를 컨테이너 내부의 환경변수로 통째로 등록합니다.
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: env-all-pod
spec:
  containers:
  - name: app
    image: nginx
    envFrom:
    - configMapRef:
        name: app-config
    - secretRef:
        name: app-secret
```

### 방법 3: 볼륨으로 마운트 (`volumes` & `volumeMounts`)
설정 파일 형태(예: `nginx.conf`)로 컨테이너 내부 특정 경로에 파일로 주입할 때 사용합니다.
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: volume-mount-pod
spec:
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: config-vol
      mountPath: /etc/nginx/conf.d
      readOnly: true
    - name: secret-vol
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: config-vol
    configMap:
      name: app-config
  - name: secret-vol
    secret:
      secretName: app-secret
```

---

## 4. Secret 조회 및 디코딩 (Base64)

Secret의 값은 Base64로 인코딩되어 있으므로 평문 확인 시 디코딩이 필요합니다.
```bash
# Secret 값 확인
kubectl get secret app-secret -o jsonpath='{.data.DB_PASSWORD}' | base64 -d
echo ""
```

---

## 💡 CKA 시험 실전 팁

1. **공식 문서 검색어**: `configmap`, `secret`
2. **빠른 뼈대 생성**:
   ```bash
   kubectl run test-pod --image=nginx --dry-run=client -o yaml > pod.yaml
   ```
   생성된 `pod.yaml`의 컨테이너 섹션 아래에 `env` 또는 `volumeMounts`를 추가합니다.

3. Secret 생성 시 `--from-literal` 옵션을 쓰면 알아서 Base64 인코딩이 되므로 별도로 `base64` 변환을 거칠 필요가 없습니다.
