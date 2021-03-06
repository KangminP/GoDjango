# README

### 1. final_pjt

- 프로젝트 소개

  - 영화 정보 기반 추천 서비스와 커뮤니티 서비스 구성

- 개발 환경

  1. Python Web Framework

     A. Django 2.1.15

     B. Python 3.7+

  3. 개발 아키텍쳐

     A. Django

     B. Vanila JS

  4. 서비스 배포 환경

     A. MySQL / SQLite

- 팀원 정보 및 업무 분담 내역

  
   |담당자| 담당업무(정) | 담당업무(부) |사용언어/툴|
   |-| ------------ | ------------ |-|
   |박강민|UI/UX design<br />Website construction<br />Database construction|API managerment<br />Recommendation algorithm<br />Database management|Python<br />JavaScript<br />HTML/CSS<br />Bootstrap<br />django<br />SQlite<br />c9<br />GitHub|
   |이지은|Project management<br />API managerment<br />Recommendation algorithm<br />Database management|Website construction<br />Database construction|Python<br />JavaScript<br />HTML/CSS<br />Bootstrap<br />django<br />SQlite<br />GitHub|



### 2. 목표 서비스 구현 및 실제 구현 정도

|앱|목표 서비스 구현|실제 구현 정도|
|-|-|-|
|accounts|관리자만이 영화 등록, 수정, 삭제 권한을 가지고 있어야 함<br />관리자는 유저들을 관리할 수 있음<br />유저 회원가입, 로그인, 로그아웃 기능|목표 서비스<br />+<br />회원가입시 이름과 관심 있는 영화 장르를 선택할 수 있음<br />모든 영화 리뷰에 'like' 가능<br />유저 본인이 'like'를 누른 영화, 리뷰 목록을 프로필에서 조회 가능<br />리뷰를 작성한 유저와 메세지를 주고 받을 수 있음|
|movies|영화 정보를 제공해주는 사이트에서 data를 가져와서 사용<br />data를 바탕으로 모델링을 하여 db에 저장<br />로그인 한 유저만 영화 평점 등록 및 삭제 기능이 가능|목표 서비스<br />+<br />네비바의 검색 칸을 활용해 영화를 검색할 수 있음<br />랜덤, 인기, 평점, 최신 순으로 영화 목록을 보여줌<br />영화 디테일 페이지에서 예고편, 오버뷰 등 상세 정보를 확인 가능함<br />해당 영화와 관련된 리뷰 목록을 조회할 수 있음|
|reviews|로그인 한 유저만 리뷰 조회 및 생성 기능이 가능<br />작성자 본인만 리뷰를 수정 및 삭제 할 수 있음<br />게시글 댓글 생성 기능과 삭제가 가능하고 이 역시 작성자 본인에게만 권한이 주어짐<br />각 게시글 및 댓글은 생성 및 수정 시각 정보가 포함되어야 함|목표 서비스<br />+<br />검색 기능을 통해 관련 게시글 조회 가능<br />상세 정보를 통해 내용을 확인할 수 있고, 좋아요 기능이 가능함|
|recommends|평점 등록한 유저 정보를 기반으로 한 영화 추천 알고리즘|목표 서비스<br />+<br />카카오 API '비전'을 활용하여 영화 사진을 분석하여 사용자에게 추천해줌<br />네이버 API '얼굴인식'을 활용하여 사용자가 제출하는 사진으로 감정을 분석해 적절한 장르를 추천함|



### 3. 초기 데이터베이스 모델링(ERD)

![초기ERD](C:\Users\kangmin\Desktop\Dev\GitHub\GoDjango\초기ERD.jpg)



### 4. 배포 서버 URL

http://fast-chamber-77905.herokuapp.com/



### 5. 느낀 점

- 데이터베이스를 받아오는거에 헤맸지만 한 번 받고 나니 API 받아오는 방법을 알게돼서 유용하게 사용할 수 있어서 좋았습니다.
- CSS를 하면서 웹사이트가 뜻대로 움직이지 않아 고충을 겪었습니다. 수많은 구글링과 여러가지 방법을 써가면서 그래도 결국엔 구현된 걸 보면 뿌듯했습니다.
- 초반에 방향을 정해놨지만 프로젝트를 진행하다보니 뜻대로 안되는 부분이 있어서 중간에 방향이 달라지기도 했습니다. 처음 시작할 때는 jira나 git 등 활용을 활용하려고 했으니 데이터 받아오는 부분에서 이틀이 걸리니 마음이 급해져 계획한 만큼 실천하기가 어려웠습니다.
- 배운 내용이지만 기억이 나지 않아 검색 해본 부분이 많았습니다. 그래서 무엇을 놓쳤는지 깨달을 수 있었습니다.
- 프로젝트를 구현하는데 바빠서 사용자의 입장에서는 생각을 많이 못한 것 같아 아쉬움이 남습니다.
- 개발은 역시 혼자 하는게 아니란걸 느꼈습니다. 코딩 능력도 중요하지만 기획과 아이디어 또한 중요했고, 소통할 수 있는 개발자가 좋은 개발자라고 생각하게 되었습니다. 좋은 팀원 덕분에 서로 피드백하며 수시로 직접 만나 편하게 진행할 수 있었던 것 같습니다. 
- 정말 저의 부족한 점을 많이 느꼈지만, 동시에 그래도 한 학기만에 이런걸 만들어 낼 수도 있구나 하는 생각에 뿌듯함도 함께 느꼈습니다.