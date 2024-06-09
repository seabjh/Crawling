import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

base_url = 'https://series.naver.com/novel/detail.series?productNo=4961138' # 천산다객 '폐후의 귀환 링크'

def collect_data(url):
    service = Service('C:/c-d/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(3)
    driver.get(url)
    
    time.sleep(3)  # 페이지 로딩 대기

    try:
        all_comments_tab = driver.find_element(By.XPATH, "//span[contains(text(), '전체댓글')]")
        all_comments_tab.click()
        time.sleep(3)  # '전체댓글' 탭 클릭 후 데이터 로딩 대기
    except Exception as e:
        print("Failed to find or click '전체댓글' tab:", e)
        driver.quit()
        return None

    comments = []
    current_page = 1

    while True:
        # 페이지 번호 업데이트
        if current_page > 1:
            try:
                next_page = driver.find_element(By.XPATH, f"//span[@class='u_cbox_num_page' and text()='{current_page}']")
                next_page.click()
                time.sleep(2)  # 페이지 로딩 대기
            except Exception as e:
                print(f"Failed to navigate to page {current_page}:", e)
                break  # 해당 페이지가 없으면 루프 종료

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        content_wrap = soup.find('div', class_='u_cbox_content_wrap')
        
        # 예외 처리: 댓글을 포함하는 요소를 찾지 못했을 때
        if content_wrap is None:
            print("Failed to find comment container element.")
            break

        cmtList = content_wrap.find_all('li')

        for element in cmtList:
            name_element = element.find('span', class_='u_cbox_nick')
            review_element = element.find('span', class_='u_cbox_contents')
            date_element = element.find('span', class_='u_cbox_date')
            
            # 예외 처리: 필수 요소를 찾지 못했을 때
            if name_element is None or review_element is None or date_element is None:
                print("Failed to extract comment information from element.")
                continue
            
            name = name_element.text
            review = review_element.text
            date = date_element.text
            
            comment = {'Name': name, 'Review': review, 'Date': date}
            comments.append(comment)

        current_page += 1  # 다음 페이지로 번호 증가

        # '다음' 버튼 클릭 로직
        if current_page % 5 == 1 and current_page != 1:
            try:
                next_button = driver.find_element(By.XPATH, "//span[@class='u_cbox_cnt_page' and contains(text(), '다음')]")
                next_button.click()
                time.sleep(2)  # '다음' 버튼 클릭 후 페이지 로딩 대기
            except Exception as e:
                print("Failed to find or click 'Next' button:", e)
                break  # '다음' 버튼이 없으면 루프 종료

    data = pd.DataFrame(comments)
    driver.quit()
    return data

# 데이터 수집 및 저장
collected_data = collect_data(base_url)
if collected_data is not None:
    print('데이터 수집 완료')
    file_path = os.path.join(os.getcwd(), 'Total_collected_data.xlsx')  # 현재 폴더에 파일 저장
    collected_data.to_excel(file_path, index=False)
    print(f'데이터가 {file_path} 파일로 저장되었습니다.')
else:
    print('데이터 수집 실패')
