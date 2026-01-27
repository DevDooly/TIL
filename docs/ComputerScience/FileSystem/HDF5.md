# HDF5 (Hierarchical Data Format version 5)

**HDF5**는 대용량 데이터를 저장하고 관리하기 위해 설계된 파일 형식(File Format)이자 라이브러리입니다. The HDF Group에서 관리하고 있으며, 복잡한 데이터 구조를 효율적으로 저장할 수 있어 과학 계산, 시뮬레이션, 딥러닝(데이터셋 저장) 등 고성능 컴퓨팅 분야에서 널리 사용됩니다.

## 1. 주요 특징

*   **계층적 구조 (Hierarchical):** 파일 시스템처럼 폴더(Group)와 파일(Dataset) 개념을 사용하여 내부 데이터를 트리 구조로 정리할 수 있습니다.
*   **대용량 처리:** 기가바이트(GB)에서 테라바이트(TB) 단위의 거대한 데이터도 하나의 파일에 담을 수 있으며, 필요한 부분만 빠르게 읽고 쓰는(I/O) 성능이 뛰어납니다.
*   **이기종 호환성:** 다양한 운영체제(Windows, Linux, Mac)와 프로그래밍 언어(C, C++, Python, Java, MATLAB 등)를 지원하여 데이터 공유가 용이합니다.
*   **메타데이터 지원:** 데이터 자체뿐만 아니라 데이터에 대한 설명(Attributes)을 함께 저장할 수 있어 데이터 관리가 수월합니다.

## 2. HDF5 파일 구조

HDF5 파일은 크게 두 가지 핵심 객체로 구성됩니다.

### 2.1 Group (그룹)
*   파일 시스템의 **디렉토리(폴더)** 와 같은 역할을 합니다.
*   다른 그룹이나 데이터셋을 포함할 수 있는 컨테이너입니다.
*   루트 그룹(`/`)에서 시작하여 트리 구조를 형성합니다.

### 2.2 Dataset (데이터셋)
*   파일 시스템의 **파일**과 같은 역할을 하며, 실제 데이터가 저장되는 곳입니다.
*   **다차원 배열(Multidimensional Array)** 형태로 데이터를 저장하는 데 최적화되어 있습니다. (NumPy 배열과 매우 유사)
*   데이터 타입(Integer, Float, String 등)과 차원(Shape) 정보를 가집니다.

### 2.3 Attribute (속성)
*   Group이나 Dataset에 붙일 수 있는 메타데이터입니다.
*   예: "센서 ID: A-123", "실험 날짜: 2024-01-01" 등의 부가 정보를 기록할 때 사용합니다.

## 3. 활용 예시 (Python)

Python에서는 `h5py` 라이브러리를 통해 HDF5 파일을 쉽게 다룰 수 있습니다. 특히 NumPy와 완벽하게 호환되어 딥러닝 모델의 가중치 저장(Keras `.h5`)이나 거대한 학습 데이터를 저장하고 로딩할 때 자주 사용됩니다.

```python
import h5py
import numpy as np

# 1. HDF5 파일 생성 및 쓰기
with h5py.File('my_data.h5', 'w') as f:
    # 그룹 생성
    grp = f.create_group("experiment_1")
    
    # 데이터셋 생성 (100x100 랜덤 행렬)
    data = np.random.random((100, 100))
    dset = grp.create_dataset("readings", data=data)
    
    # 메타데이터 추가
    dset.attrs['sensor_type'] = 'thermal'

# 2. HDF5 파일 읽기
with h5py.File('my_data.h5', 'r') as f:
    # 데이터 접근
    data_read = f['experiment_1/readings'][:]
    print(data_read.shape)  # (100, 100)
    print(f['experiment_1/readings'].attrs['sensor_type']) # 'thermal'
```

## 참고
*   [The HDF Group 공식 사이트](https://www.hdfgroup.org/)