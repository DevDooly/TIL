# Oracle Cloud Free Tier (오라클 클라우드 프리티어)

Oracle Cloud Infrastructure (OCI) Free Tier는 클라우드 서비스를 무료로 체험하거나 평생 무료로 사용할 수 있는 프로그램입니다. 특히 **ARM 기반 인스턴스(Ampere)**를 넉넉하게 제공하여 가성비 좋은 개인 서버나 학습용 환경으로 인기가 높습니다.

## 🎁 주요 무료 혜택 (Always Free)

### 1. 컴퓨트 인스턴스 (VM)
- **AMD Compute VM:** 2개 (각각 1/8 OCPU, 1GB RAM) - *성능이 매우 낮음*
- **ARM Ampere A1 Compute:**
  - **최대 4 OCPU, 24GB RAM** (이 리소스를 최대 4개의 인스턴스로 나누어 사용 가능)
  - 예: 4 OCPU / 24GB RAM 인스턴스 1개 생성 가능 (매우 강력함)

### 2. 스토리지
- **Block Volume:** 총 200GB
- **Object Storage:** 10GB
- **Archive Storage:** 10GB

### 3. 네트워크
- **Outbound Data Transfer:** 월 10TB

### 4. 데이터베이스
- **Oracle Autonomous Database:** 2개 (각 20GB 스토리지)

> **참고:** 가입 시 $300 크레딧(30일 유효)을 제공하여 유료 서비스도 체험해 볼 수 있습니다.

---

## 🚀 가입 및 인스턴스 생성 가이드

### 1. 회원가입
1. [Oracle Cloud Free Tier 페이지](https://www.oracle.com/kr/cloud/free/) 접속.
2. **무료로 시작하기** 클릭.
3. 국가(South Korea), 이름, 이메일 입력.
4. **Home Region (홈 영역) 선택:**
   - **중요:** 한 번 선택하면 변경할 수 없으며, Always Free 인스턴스는 홈 리전에서만 생성 가능합니다.
   - 'Korea, South (Seoul)' 또는 'Korea, South (Chuncheon)' 선택. (단, 서울 리전은 ARM 인스턴스 재고가 부족할 수 있음)
5. 주소 입력 및 휴대폰 인증.
6. **결제 수단 등록:** 신용/체크카드 등록 (본인 확인 용도, 실제 결제는 유료 전환 전까지 안 됨).

### 2. VCN (가상 클라우드 네트워크) 생성
인스턴스를 만들기 전에 네트워크 환경을 구성해야 합니다.

1. 메뉴 -> **Networking** -> **Virtual Cloud Networks**.
2. **Start VCN Wizard** 클릭.
3. **Create VCN with Internet Connectivity** 선택 -> **Start VCN Wizard**.
4. VCN Name 입력 (예: `my-vcn`) -> **Next** -> **Create**.

### 3. 인스턴스 생성 (VM 만들기)
1. 메뉴 -> **Compute** -> **Instances**.
2. **Create Instance** 클릭.
3. **Name:** 인스턴스 이름 입력 (예: `my-server`).
4. **Image and Shape:** [Edit] 클릭.
   - **Image:** `Ubuntu 22.04` 또는 `Oracle Linux` 선택.
   - **Shape:** `Ampere` 시리즈 선택 (예: `VM.Standard.A1.Flex`).
   - **OCPU & Memory:** 원하는 만큼 할당 (최대 4 OCPU, 24GB RAM).
5. **Networking:** 앞서 생성한 VCN과 Public Subnet 선택.
6. **Add SSH keys:**
   - **Generate a key pair for me:** 키 쌍을 새로 생성하고 **반드시 Private Key를 다운로드** 받아야 합니다. (.key 파일)
   - **Upload public key files:** 기존에 사용하는 공개키가 있다면 업로드.
7. **Create** 클릭.

### 4. 접속하기
인스턴스가 `Running` 상태가 되면 **Public IP Address**를 확인합니다.

```bash
# 다운로드 받은 키 권한 변경 (필수)
chmod 600 ssh-key-2023-xx-xx.key

# SSH 접속 (기본 사용자: ubuntu 또는 opc)
ssh -i ssh-key-2023-xx-xx.key ubuntu@<Public-IP>
```

---

## ⚠️ 주의사항

1. **장기 미사용 시 회수:** 일정 기간(약 7일) 동안 CPU 사용률이 10% 미만인 상태가 지속되면, 유휴 자원으로 간주하여 인스턴스가 중지되거나 회수될 수 있다는 경고 메일이 올 수 있습니다. (적당한 부하를 주는 스크립트를 돌리거나 유료 계정으로 업그레이드하여 방지 가능 - Pay As You Go 전환 시에도 무료 범위 내에서는 과금 안 됨)
2. **ARM 아키텍처 호환성:** Ampere 인스턴스는 ARM 기반(aarch64)이므로, x86_64 전용으로 빌드된 일부 도커 이미지나 소프트웨어는 실행되지 않을 수 있습니다. (대부분의 모던 소프트웨어는 멀티 아키텍처를 지원함)
