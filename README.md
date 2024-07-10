# 라이브 스트리밍 리스트 프로젝트 Version 1

![project_img](https://github.com/Scanf-s/live_streaming_lists/assets/105439069/c90b22b5-9422-47a2-b6e0-71e550fd80f9)

## 프로젝트 소개

`라이브 스트리밍 리스트` 프로젝트는 다양한 실시간 방송 플랫폼에서 실시간 스트리밍 데이터를 수집하고 이를 사용자에게 제공하는 웹 애플리케이션입니다.
현재 구현된 내용은 실시간 방송 플랫폼으로부터 데이터를 수집하여, 시청자 순으로 데이터를 제공하는 기능만 구현되어 있습니다.
추후 태그, 관심도에 따른 실시간 방송 리스트를 보여주는 기능을 추가할 예정입니다.

## 구현 기능

## Version 1

### 플랫폼 별 시청자 순 정렬
![image](https://github.com/Scanf-s/live_streaming_lists/assets/105439069/ddaff456-3b8e-47fa-84de-1f39eb81e9f9)

### 간단한 로그인 기능 구현

![image](https://github.com/Scanf-s/live_streaming_lists/assets/105439069/f16efc67-4591-46dd-bdda-00d7e3a1a914)

### API 호출 페이지네이션 기능

https://github.com/Scanf-s/live_streaming_lists/assets/105439069/307ca6ff-fffe-4c3a-8ae6-3500f518c711

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
  - **MSW(Mock Service Worker)를 이용한 Mocking API 개발하기** : API 요청 기능을 테스트하고 화면을 구성
  - **로그인/ 회원가입 페이지 생성 및 UI 디자인** : 로그인 및 회원가입 페이지를 생성하고 페이지 UI를 디자인
  - **실제 API 요청 코드로 수정 및 무한 스크롤 기능 구현** : 기존 MSW 코드를 일부 수정하고 페이지네이션 기능 구현에 따른 무한스크롤 로직을 일부 수정
  - **페이지 UI 개선 및 다크 모드 적용** : 실제 데이터를 받아봄에 따른 UI 개선 및 다크모드를 적용
  - **GitHub Actions를 통한 S3에 파일 자동 업로드 설정** : GitHub Actions를 사용하여 프론트엔드 빌드 파일을 AWS S3에 자동 배포하는 CI/CD 설정
  - **스켈레톤 로딩 적용** : 데이터 비동기 처리에 따른 스켈레톤 로딩 애니메이션 적용

- **황두나 : Frontend**
  - **페이지 라우터 설정**: React Router를 사용하여 페이지 간 내비게이션 설정.
  - **데이터 화면 배치**: 가공된 데이터를 화면에 배치하고 UI 컴포넌트 작성.


## 개발 환경
Docker

- Django API
  - WSL2 Ubuntu
  - Docker python:3.12-alpine3.20
  - Pycharm

- Data scraper
  - MacOS
  - Docker python:3.12-slim
  - VScode
 
- Frontend
  - MacOS
  - VScode

## 사용 기술

### Frontend
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Tailwind](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Zustand](https://img.shields.io/badge/zustand-%23000000.svg?style=for-the-badge&logo=zustand&logoColor=white)

### Backend
#### API Server
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

#### Data Scraper
![BeautifulSoup4](https://img.shields.io/badge/beautifulsoup4-4B8BBE?style=for-the-badge&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/playwright-2E2E2E?style=for-the-badge&logo=microsoft-edge&logoColor=white)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Crontab](https://img.shields.io/badge/crontab-23A97A?style=for-the-badge&logo=linux&logoColor=white)

### Database
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![AWS RDS](https://img.shields.io/badge/amazonrds-%23527FFF.svg?style=for-the-badge&logo=amazon-rds&logoColor=white)

### CI/CD
![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/githubactions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

### Cloud
![AWS Route53](https://img.shields.io/badge/aws-route53-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![AWS CloudFront](https://img.shields.io/badge/aws-cloudfront-F2B400?style=for-the-badge&logo=amazon-aws&logoColor=white)
![AWS ALB](https://img.shields.io/badge/aws-alb-FF4F8B?style=for-the-badge&logo=amazon-aws&logoColor=white)
![AWS S3](https://img.shields.io/badge/aws-s3-569A31?style=for-the-badge&logo=amazon-s3&logoColor=white)
![AWS EC2](https://img.shields.io/badge/aws-ec2-FF9900?style=for-the-badge&logo=amazon-ec2&logoColor=white)
![AWS ACM](https://img.shields.io/badge/aws-acm-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)

## 브랜치 전략

![image](https://github.com/Scanf-s/live_streaming_lists/assets/105439069/ea9420bf-97fb-4341-a282-659c7f841099)

## 어플리케이션 아키텍쳐

### Version 1
![image](https://github.com/Scanf-s/live_streaming_lists/assets/105439069/868007f2-7db3-40de-8032-c924e506a736)

## ERD

### Version 1
![image](https://github.com/Scanf-s/live_streaming_lists/assets/105439069/43d15070-0128-439d-9e8d-df376c2842a7)
