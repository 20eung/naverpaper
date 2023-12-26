import ppomppu_naverpaper
import time

base_url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=coupon"

s = ppomppu_naverpaper.naver_session('##네이버 로그인 전용 아이디##','##네이버 애플리케이션 패스워드')

# 여기서 s가 None인지 확인합니다.
if s is None:
    print("로그인 실패: 세션을 생성할 수 없습니다.")
    exit()

campaign_links = ppomppu_naverpaper.find_naver_campaign_links(base_url)

if(campaign_links == []):
    print("모든 링크를 방문했습니다.")

for link in campaign_links:
    print("캠페인URL: " + link)

    response = s.get(link)

    # 응답 텍스트를 줄 단위로 분할
    lines = response.text.splitlines()

    desired_text = "alert"

    # 각 줄을 순회하며 'alert' 문자열이 포함된 줄 찾기
    for line in lines:
        if desired_text in line:
            print(line)

    response.raise_for_status() # for debugging
    time.sleep(5)
