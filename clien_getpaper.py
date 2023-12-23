import clien_naverpaper
import time

base_url = "https://www.clien.net/service/board/jirum"

s = clien_naverpaper.naver_session('20eung','R8F3PTQ8UL8C')

# 여기서 s가 None인지 확인합니다.
if s is None:
    print("로그인 실패: 세션을 생성할 수 없습니다.")
    exit()

campaign_links = clien_naverpaper.find_naver_campaign_links(base_url)

if(campaign_links == []):
    print("모든 링크를 방문했습니다.")
for link in campaign_links:
    response = s.get(link)
    #print(response.text) # for debugging
    #response.raise_for_status() # for debugging
    time.sleep(5)
    print("캠페인 URL : " + link)
