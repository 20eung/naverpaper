import re
import uuid
import requests
import rsa
import lzstring
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def encrypt(key_str, uid, upw):
    def naver_style_join(l):
        return ''.join([chr(len(s)) + s for s in l])

    sessionkey, keyname, e_str, n_str = key_str.split(',')
    e, n = int(e_str, 16), int(n_str, 16)

    message = naver_style_join([sessionkey, uid, upw]).encode()

    pubkey = rsa.PublicKey(e, n)
    encrypted = rsa.encrypt(message, pubkey)

    return keyname, encrypted.hex()


def encrypt_account(uid, upw):
    key_str = requests.get('https://nid.naver.com/login/ext/keys.nhn').content.decode("utf-8")
    return encrypt(key_str, uid, upw)


def naver_session(nid, npw):
    encnm, encpw = encrypt_account(nid, npw)

    s = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504]
    )
    s.mount('https://', HTTPAdapter(max_retries=retries))
    request_headers = {
        'User-agent': 'Mozilla/5.0'
    }

    bvsd_uuid = uuid.uuid4()
    encData = '{"a":"%s-4","b":"1.3.4","d":[{"i":"id","b":{"a":["0,%s"]},"d":"%s","e":false,"f":false},{"i":"%s","e":true,"f":false}],"h":"1f","i":{"a":"Mozilla/5.0"}}' % (
    bvsd_uuid, nid, nid, npw)
    bvsd = '{"uuid":"%s","encData":"%s"}' % (bvsd_uuid, lzstring.LZString.compressToEncodedURIComponent(encData))

    resp = s.post('https://nid.naver.com/nidlogin.login', data={
        'svctype': '0',
        'enctp': '1',
        'encnm': encnm,
        'enc_url': 'http0X0.0000000000001P-10220.0000000.000000www.naver.com',
        'url': 'www.naver.com',
        'smart_level': '1',
        'encpw': encpw,
        'bvsd': bvsd
    }, headers=request_headers)

    finalize_url = re.search(r'location\.replace\("([^"]+)"\)', resp.content.decode("utf-8")).group(1)
    s.get(finalize_url)

    return s


def find_naver_campaign_links(base_url, visited_urls_file='ppomppu_visited_urls.txt'):
    try:
        with open(visited_urls_file, 'r') as file:
            visited_urls = set(file.read().splitlines())
    except FileNotFoundError:
        visited_urls = set()

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all span elements with class 'list_subject' and get 'a' tags
    list_subject_links = soup.find_all('td', class_='list_vspace')

    page_links = []
    for span in list_subject_links:
        a_tag = span.find('a', href=True)

        if a_tag and '네이버' in a_tag.text:
            full_link = urljoin(page_url, a_tag['href'])
            page_links.append(full_link)
#           print("뽐뿌링크추가:", full_link)  # 디버깅 출력

    # Initialize a list to store campaign links
    campaign_links = []

    # Check each page_links
    for link in page_links:
#       print("뽐뿌링크:", link)  # 디버깅 출력

        if link in visited_urls:
#           print("이미 있는 링크")  # 디버깅 출력
            continue  # Skip already visited links

        res = requests.get(link)
        inner_soup = BeautifulSoup(res.text, 'html.parser')

        campaign_a_tags = inner_soup.find_all('a', href=True)

        for a_tag in campaign_a_tags:
            campaign_link = a_tag.get_text().strip()

#           print("네이버링크:", campaign_link)  # 디버깅 출력

            if ('campaign2-api.naver.com' in campaign_link or 'ofw.adison.co' in campaign_link) and campaign_link not in campaign_links:
                campaign_links.append(campaign_link)
#               print(f"캠페인링크: {campaign_link}")  # 디버깅 출력
#           else:
#               print("적절한 게시글 본문을 찾지 못함")  # 디버깅 출력


        # Add the visited link to the set
        visited_urls.add(link)


    # Save the updated visited URLs to the file
    with open(visited_urls_file, 'w') as file:
        for url in visited_urls:
            file.write(url + '\n')

    return campaign_links



# The base URL to start with
base_url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=coupon"
page_url = "https://www.ppomppu.co.kr/zboard/zboard.php?"
