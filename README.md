# Toy-shop



## Infrastructure(AWS)

<img width="1346" alt="스크린샷 2024-02-23 08 49 18" src="https://github.com/navill/toy-shop/assets/25294465/7e0e7efc-ced7-4eab-8e96-16b4db43b7b8">

- Available Zone: ap-northeast-2a, ap-northeast-2c
- ECS: 서비스 컨테이너 구축
  - ECS Cluster
    - EC2: Blue/Green 배포 시 최소한의 네트워크(ENI) 수를 충족시키기 위해 t2.small 사용
  - CodeDeploy: 서비스 배포(수동)
- CloudFormation: 반복적으로 자주 사용되는 서비스(네트워크 구성) 구축

- Secret manager: RDS 및 어플리케이션 키값 보관
- Network
  - Ingress ALB: 외부 요청 전달
  - Internal ALB: 서비스 컨테이너 라우팅(테스트 컨테이너 포함)
  - Interface Endpoint(Egress): AWS 서비스 요청(PrivateLink). 이미지 외에 ECS(ecs, telemetry, agent) 서비스도 포함



## Application

- Application: python 3.10, django 4.0, drf 3.14
- User, Item, Order 앱으로 구성된 온라인 샵 토이 프로젝트

### Libraries
  - django-mptt: 카테고리 모델을 트리 형태로 구성하기 위해 사용
  - django-concurrency: optimistic-lock을 위한 version field 제공
  - django-safedelete: 모델의 soft-delete 기능
  - djangorestframework-simplejwt: jwt 토큰 인증
  - drf-spectacular: api 문서 작성
  - cryptography: 데이터 암호화(AES)
  - funcy: 함수, 컬렉션 등 편의 기능 제공
  - pydantic: DTO 클래스
  - pytest-django: 테스트 코드 작성

## 개발 공통 내용
  - db 식별 id, 외부 식별 uuid 사용(product, category 제외)
  - 모든 관계 옵션은 `on_delete=DO_NOTHING`으로 통일(safedelete 모델 적용)
  - serializer 분리를 위한 generics 오버라이딩([commons.generics](https://github.com/navill/toy-shop/blob/main/commons/views/generics.py), [commons.mixins](https://github.com/navill/toy-shop/blob/main/commons/views/mixins.py)): request & response serializer 분리
    - 서로 다른 요청/응답 형태
    - API 문서 자동화
  - Service layer 적용: view & serializer에서 비즈니스 로직을 분리. 계층별 데이터 전송은 DTO 이용
    - [users.services](https://github.com/navill/toy-shop/blob/main/users/services.py)
    - [orders.services](https://github.com/navill/toy-shop/blob/main/orders/services.py)

## App & Model
  - users: 유저 정보 관리
    - [User](https://github.com/navill/toy-shop/blob/main/users/models.py)
      - [비식별화(commons.deidentifications)](https://github.com/navill/toy-shop/blob/main/commons/deidentifications.py): 유저 개인 정보 데이터는 암호화하여 저장, 응답값은 마스킹, 복호화된 데이터 사용
  - items: 판매 관련 정보 관리
    - [Product](https://github.com/navill/toy-shop/blob/main/items/models.py#L34): 제품 정보
      - 물품 제고(product.stock) 동시성 문제를 위한 version control 적용
    - Category: 카테고리 정보
      - 카테고리 상/하위 관계 트리 구조 구성(django-mptt)
  - orders: 물품 주문
    - [Order](https://github.com/navill/toy-shop/blob/main/orders/models.py#L17): 주문 시 배송 정보 및 거래 상태 저장
    - [ProductOrder](https://github.com/navill/toy-shop/blob/main/orders/models.py#L35): 물품 정보 기록
      - 거래 시점 이후 변경될 수 있는 정보를 직접 관리(product_name, price)
