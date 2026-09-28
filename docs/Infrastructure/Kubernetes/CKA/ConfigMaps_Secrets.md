# 2.4 설정 관리 (ConfigMaps & Secrets)

ConfigMap과 Secret은 애플리케이션 설정과 인증 정보를 컨테이너 이미지와 분리해 관리합니다. 환경변수 또는 볼륨 마운트로 컨테이너에 전달할 수 있습니다.

---

## 1. ConfigMap & Secret 개념

- **ConfigMap**: 일반 텍스트 형태의 설정값(포트, 환경명, 설정 파일 내용 등)을 Key-Value 형태로 저장합니다.
- **Secret**: 패스워드, API 토큰, TLS 인증서 등 민감한 데이터를 다루는 리소스입니다. `data`는 Base64 표현이며 암호화가 아닙니다. etcd 저장 암호화와 RBAC은 별도 설정입니다. (기본 타입: `Opaque`)

---

## 2. 생성 명령어 (Imperative Commands)

`kubectl create`로 리소스를 생성하거나 `--dry-run=client -o yaml`을 붙여 YAML을 만들 수 있습니다. 아래 Secret 값은 실습용입니다.

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
# nginx conf.d용 파일을 먼저 준비한다.
cat > default.conf <<'EOF'
server {
    listen 80;
    location / { return 200 "configmap demo\n"; }
}
EOF
kubectl create configmap nginx-conf --from-file=default.conf

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

2절에서 만든 `nginx-conf`의 `default.conf`와 `app-secret`을 마운트합니다. 참조 리소스와 Pod는 같은 namespace에 둡니다.

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
      name: nginx-conf
  - name: secret-vol
    secret:
      secretName: app-secret
```

---

## 4. 설정 변경의 반영

환경변수로 주입한 값은 원본 ConfigMap·Secret을 수정해도 실행 중인 컨테이너에 자동 반영되지 않습니다. 새 값으로 파드를 재생성합니다. 일반 볼륨 마운트는 지연 후 갱신될 수 있지만 `subPath` 마운트는 자동 갱신되지 않습니다. 파일이 바뀌어도 애플리케이션이 다시 읽는지는 별도이며 nginx 설정 변경에는 reload 또는 재시작이 필요합니다.

## 5. Secret 조회 및 디코딩 (Base64)

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

## 참고 자료

- [Kubernetes: ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Kubernetes: Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
