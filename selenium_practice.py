# from selenium import webdriver
from selenium.webdriver import Chrome
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By         # STEP 3
from selenium.webdriver.common.keys import Keys     # STEP 3

"""
STEP 2
"""
# 브라우저 꺼짐 방지 - 옵션 설정
opt = Options()
opt.add_experimental_option('detach', True)   # 꺼짐 방지 옵션
# opt.add_argument('headless')    # STEP 3: 실행화면 보지 않음


""" 
STEP 1
"""
url = "https://www.naver.com"

# 크롬 드라이버 개체 생성
# driver = webdriver.Chrome()
driver = Chrome(options=opt)    # STEP 2: options=opt 추가
driver.get(url)
time.sleep(1)                 # STEP 2: remark    /   STEP 3: timesleep 중간 중간 넣기


"""
STEP 3
"""
# 검색
search_box = driver.find_element(By.ID, 'query')
search_box.send_keys("인공지능")
search_box.send_keys(Keys.RETURN)
time.sleep(1)

# 뉴스 탭 클릭 : XPATH
# driver.find_element(By.XPATH, '//*[@id="lnb"]/div[1]/div/div[1]/div/div[1]/div[3]/a').click()
driver.find_element(By.LINK_TEXT, "뉴스").click()     # LINK_TEXT는 a 태그일 때 가능!
time.sleep(1)

# 화면 스크롤 : 전체페이지(body) 안에서 스크롤 내리거나 올릴 수 있게!
scroll = driver.find_element(By.TAG_NAME, "body")


# 스크롤 다운
for i in range(5):
    scroll.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)


# 뉴스 제목 텍스트 추출
news_titles = driver.find_elements(By.CLASS_NAME, "news_tit")
# print(news_titles[0].text)
## href 추출


count = 1
for title in news_titles:
    print(f"{count}. {title.text}")
    print(title.get_attribute('href'))
    count += 1

# for link in links:
#     print(link.text)


"""
STEP 4: 파일 생성
"""
cn = 1
for i in news_titles:
    with open("news.csv", 'a', encoding='utf-8') as f:
        f.write(f"{cn}. {i.text}")
        f.write("\n")
        cn += 1

driver.quit()   # 메모리 안에서 없애기
