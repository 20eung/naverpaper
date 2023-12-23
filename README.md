# naverpaper
## 네이버 폐지 줍기 자동화 파이썬 스크립트 - 클리앙, 뽐뿌

```
원 글은 클리앙 강좌 게시판에서 보았으나 현재 사라진 상태임.

원 제작자 정보는 다음과 같음
author='stateofai'
author_email='tellme@duck.com'
github: https://github.com/stateofai/naverpaper/
```

1. 파이썬 버전: 3.9 이상

2. 파이썬 모듈 설치
```
sudo apt-get install python3-pip
sudo pip install requests BeautifulSoap4 lxml pyc rsa urllib3
```

3. 네이버 보안 설정
   - 네이버 ID > 보안설정 > 로그인 전용 아이디 생성
   - 네이버 ID > 보안설정 > 기본보안설정 > 2단계 인증 > 관리 > 애플리케이션 비밀번호 설정
   - 네이버 ID > 보안설정 > 로그인 차단 설정 > 타지역 로그인 차단 > 해제(OFF)
     
     ->  만약 Azure/AWS/Google Cloud에서 VM을 이용할 경우
  
4. 프로그램 실행 방법
   - 만약 파이썬 소스 파일이 /home/ubuntu/naverpaper/ 폴더에 있다면
```
ubuntu@vm:~/naverpaper$ python3 clien_getpaper.py

ubuntu@vm:~/naverpaper$ cat clien_visited_urls.txt
https://www.clien.net/service/board/jirum/18488036?od=T31&po=0&category=0&groupCd=
https://www.clien.net/service/board/jirum/18489805?od=T31&po=0&category=0&groupCd=
https://www.clien.net/service/board/jirum/18487461?od=T31&po=0&category=0&groupCd=
https://www.clien.net/service/board/jirum/18489001?od=T31&po=0&category=0&groupCd=
https://www.clien.net/service/board/jirum/18488168?od=T31&po=0&category=0&groupCd=

ubuntu@vm:~/naverpaper$ python3 ppomppu_getpaper.py
캠페인 URL : https://campaign2-api.naver.com/click-point/?eventId=cr_2023122301_2401_1_1048
캠페인 URL : https://ofw.adison.co/u/naverpay/ads/446319
캠페인 URL : https://ofw.adison.co/u/naverpay/ads/563984
캠페인 URL : https://ofw.adison.co/u/naverpay/ads/549505
캠페인 URL : https://ofw.adison.co/u/naverpay/ads/548556

ubuntu@vm:~/naverpaper$ cat ppomppu_visited_urls.txt
https://www.ppomppu.co.kr/zboard/view.php?id=coupon&page=1&divpage=16&no=88915
https://www.ppomppu.co.kr/zboard/view.php?id=coupon&page=1&divpage=16&no=88924
https://www.ppomppu.co.kr/zboard/view.php?id=coupon&page=1&divpage=16&no=88919
https://www.ppomppu.co.kr/zboard/view.php?id=coupon&page=1&divpage=16&no=88910
https://www.ppomppu.co.kr/zboard/view.php?id=coupon&page=1&divpage=16&no=88905
```
