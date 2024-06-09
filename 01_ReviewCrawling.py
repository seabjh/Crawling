import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 파일 저장명 변경을 위해 크롤링 작품의 제목을 적어주자.
Novel_Title = '천산다객-여장성' 

# 네이버 시리즈의 웹소설 중 크롤링 하고 싶은 페이지 링크를 복사해서 붙여넣자.

# base_url = 'https://series.naver.com/novel/detail.series?productNo=4141828'  # 폐후의 귀환
# base_url = 'https://series.naver.com/novel/detail.series?productNo=4223426'  # 화비, 환생
# base_url = 'https://series.naver.com/novel/detail.series?productNo=5294332'  # 적가천금
base_url = 'https://series.naver.com/novel/detail.series?productNo=5572811'  # 여장성

# K O R E A N O V E L
# base_url = 'https://series.naver.com/novel/detail.series?productNo=3528535'  # 간택-왕들의향연(9,311)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=3428778'  # 소공녀 민트(8,078)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=3152728'  # 돌아온 여기사(4,450)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=8410037'  # 황궁에 핀꽃은 미쳤다(929)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=5041906'  # 네가 죽기를 바랄 때가 있었다(16,728)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=4295130'  # 곱게 키웠더니 짐승(16,708) ////// CHECK
# base_url = 'https://series.naver.com/novel/detail.series?productNo=3990680'  # 남주의 첫날밤을 가져가 버렸다(14,372)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=4579233'  # 남편을 만렙으로 키우려 합니다(4,918)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=4502291'  # 시한부인 줄 알았어요(6,949)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=5693874'  # 언니 이번생엔 내가 왕비야(71,075)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=4880420'  # 하렘의남자들(128,045)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=5191948'  # 문제적 왕자님(34,644)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=6256126'  # 황후를 훔친 이는 누구인가(11,725)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=5779614'  # 대리 황후지만 첫날밤을 보내버렸다(8,975)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=5788724'  # 전남편의 미친개를 길들였다(18,178)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=5980361'  # 흔한 빙의물인 줄 알았다(8,732)

# C H I N A  N O V E L
# base_url = 'https://series.naver.com/novel/detail.series?productNo=3606109'  # 천재소독비(12,310)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=4275210'  # 서녀명란전(13,728)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=4541108'  # 교량의경(10,153)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=4508053'  # 제왕연(2,798)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=4612954'  # 천월연가(3,805)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=4365219'  # 대당여법의(3,371)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=5761571'  # 적녀의비(4.361)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=5145470'  # 지존신의(7,277)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=5107316'  # 서녀공략(14,711)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=5418678'  # 석화지(5,511)
# base_url = 'https://series.naver.com/novel/detail.series?productNo=5693162'  # 천월서금(5,188)

# 대기 시간을 상수로 설정하여 코드에서 사용하자(대기시간 3초)
WAIT_TIME = 3

def collect_data(url):
    driver_path = 'C:/c-d/chromedriver.exe'  # ChromeDriver의 경로를 설정.
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(WAIT_TIME)
    driver.get(url)
    time.sleep(WAIT_TIME)  # 페이지 로딩을 위한 대기 시간

    try:
        # 전체댓글 탭을 클릭.
        all_comments_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), '전체댓글')]")
            )
        )
        all_comments_tab.click()
        time.sleep(WAIT_TIME)
    except Exception as e:
        print("Failed to find or click '전체댓글' tab:", e)
        driver.quit()
        return None

    comments = []
    current_page = 1

    while True:
        if current_page > 1:
            try:
                # 다음 페이지로 이동.
                next_page = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//span[@class='u_cbox_num_page' and text()='{current_page}']")
                    )
                )
                next_page.click()
                time.sleep(WAIT_TIME)
            except Exception as e:
                print(f"Failed to navigate to page {current_page}:", e)
                break

        # 현재 페이지의 HTML을 가져오자.
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        content_wrap = soup.find('div', class_='u_cbox_content_wrap')

        if content_wrap is None:
            print("Failed to find comment container element.")
            break

        # 댓글 요소를 찾자.
        cmtList = content_wrap.find_all('li')

        for element in cmtList:
            name_element = element.find('span', class_='u_cbox_nick')
            review_element = element.find('span', class_='u_cbox_contents')
            date_element = element.find('span', class_='u_cbox_date')

            if name_element is None or review_element is None or date_element is None:
                print("Failed to extract comment information from element.")
                continue

            # 댓글 정보를 추출.
            name = name_element.text
            review = review_element.text
            date = date_element.text
            comment = {'Name': name, 'Review': review, 'Date': date}
            comments.append(comment)

        current_page += 1

        # '다음' 버튼을 클릭하여 다음 페이지로 이동.
        if current_page % 5 == 1 and current_page != 1:
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//span[@class='u_cbox_cnt_page' and contains(text(), '다음')]")
                    )
                )
                next_button.click()
                time.sleep(WAIT_TIME)
            except Exception as e:
                print("Failed to find or click 'Next' button:", e)
                break

    data = pd.DataFrame(comments)
    driver.quit()
    return data

collected_data = collect_data(base_url)

if collected_data is not None:
    print('데이터 수집 완료')
    # 파일 경로를 설정하여 데이터를 저장.
    file_path = os.path.join(
        os.getcwd(), f'{Novel_Title}-Total_collected_data.xlsx'
    )
    collected_data.to_excel(file_path, index=False)
    print(f'데이터가 {file_path} 파일로 저장되었습니다.')
else:
    print('데이터 수집 실패')
