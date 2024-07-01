# 라이브 스트리밍 리스트 프로젝트

![project_img](https://github.com/Scanf-s/live_streaming_lists/assets/105439069/c90b22b5-9422-47a2-b6e0-71e550fd80f9)

## 프로젝트 소개

`라이브 스트리밍 리스트` 프로젝트는 다양한 실시간 방송 플랫폼에서 실시간 스트리밍 데이터를 수집하고 이를 사용자에게 제공하는 웹 애플리케이션입니다.
현재 구현된 내용은 실시간 방송 플랫폼으로부터 데이터를 수집하여, 시청자 순으로 데이터를 제공하는 기능만 구현되어 있습니다.
추후 태그, 관심도에 따른 실시간 방송 리스트를 보여주는 기능을 추가할 예정입니다.

## 팀원 구성

<div align="center">

| **양의종** | **조규재** | **이희주** | **황두나** |
| :------: |  :------: | :------: | :------: |
| [<img src="https://avatars.githubusercontent.com/u/105439069?v=4" height=150 width=150> <br/> @Scanf-s](https://github.com/Scanf-s) | [<img src="https://avatars.githubusercontent.com/u/66784492?v=4" height=150 width=150> <br/> @im-niber](https://github.com/im-niber) | [<img src="https://avatars.githubusercontent.com/u/164333745?s=64&v=4" height=150 width=150> <br/> @h22jul22](https://github.com/h22jul22) | [<img src="https://avatars.githubusercontent.com/u/123640595?v=4" height=150 width=150> <br/> @Skyler85](https://github.com/Skyler85) |

</div>

<br>

### 역할 분담

- **양의종 : Backend**
  - **AWS 인프라 구성**: 전반적인 프로젝트 클라우드 환경 설정
  - **Docker 환경 구성**: Dockerfile 작성 및 Docker Compose 설정.
  - **Data scraping 소스코드 개발**: 다양한 플랫폼에서 데이터를 스크래핑하는 코드 작성.
  - **Django Backend API 설계 및 구현**: RESTful API 엔드포인트 설계 및 구현.

- **조규재 : Backend**
  - **AWS 인프라 구성**: EC2, VPC peering 설정 및 관리.
  - **Docker 환경 구성**: Docker 이미지 최적화 및 컨테이너 관리.
  - **Data scraping 소스코드 개발 및 개선**: 스크래핑 코드 작성 및 성능 최적화.
  - **Crontab을 사용한 주기적인 데이터 스크래핑**: cron 작업 설정 및 자동화.
  - **AWS RDS에 스크래핑 데이터 전달**: 스크래핑한 데이터를 AWS RDS에 저장.

- **이희주 : Frontend**
  - **API 데이터 요청 코드 작성**: 더미 데이터를 사용한 초기 API 요청 코드 작성.
  - **실제 API 요청 코드 작성**: 백엔드 API와의 통신을 통해 실제 데이터 요청 코드 작성 및 연동.

- **황두나 : Frontend**
  - **페이지 라우터 설정**: React Router를 사용하여 페이지 간 내비게이션 설정.
  - **데이터 화면 배치**: 가공된 데이터를 화면에 배치하고 UI 컴포넌트 작성.


## 1. 개발 환경
Docker

- Django API
  - WSL2 Ubuntu
  - Docker python:3.12-alpine3.20

- Data scraper
  - MacOS
  - Docker python:3.12-slim
 
- Frontend
  - ...

## 2. 사용 기술
- Docker
- Javascript
- Python
- Django
- React
- Selenium
- AWS EC2
- AWS RDS
- Crontab

### Frontend
- React

### Backend
- Django
- BeautifulSoup4
- Playwright
- Selenium
- Crontab

### Database
- AWS RDS Postgres

### CI/CD
- Docker
- Github Actions

### Cloud
- AWS Route53
- AWS CloudFront
- AWS ALB
- AWS S3
- AWS EC2
- AWS ACM


## 3. 브랜치 전략

사진 첨부 해야함

## 4. 프로젝트 구조

```yml

```

## 5. 기능 소개


## 6. 추가....
