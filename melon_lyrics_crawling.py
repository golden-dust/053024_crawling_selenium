from selenium.webdriver import Chrome
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

url = "https://www.melon.com/index.htm"

opt = Options()
# opt.add_experimental_option('detach', True)
opt.add_argument('headless')


driver = Chrome(options=opt)
driver.get(url)
time.sleep(0.3)

# 검색어 입력
input = input("검색어를 입력하세요: ")
search = driver.find_element(By.ID, "top_search")
search.send_keys(input)
search.send_keys(Keys.RETURN)
time.sleep(0.2)

# 앨범 탭 클릭
driver.find_element(By.LINK_TEXT, "앨범").click()
time.sleep(0.3)

# 앨범 이미지 클릭
driver.find_element(By.CLASS_NAME, "thumb").click()
time.sleep(0.3)

album_name = driver.find_element(By.CLASS_NAME, "song_name").text
print(album_name)
artist = driver.find_element(By.CLASS_NAME, "artist_name").text
songs = driver.find_elements(By.XPATH, '//*[@id="frm"]/div/table/tbody/tr')
time.sleep(0.3)

lyrics_list = []
titles = []
song_data = pd.DataFrame()
for i in range(len(songs)):
    try:
        # 가사 버튼 클릭
        xpath = f'//*[@id="frm"]/div/table/tbody/tr[{i+1}]/td[3]/div/a'
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(0.3)

        # 노래 제목 크롤링
        song_name = driver.find_element(By.CLASS_NAME, "song_name").text
        titles.append(song_name)

        try:
            # 펼치기
            driver.find_element(By.XPATH, '//*[@id="lyricArea"]/button/span').click()
            time.sleep(0.3)

            # 가사 크롤링
            lyrics = driver.find_element(By.ID, "d_video_summary").text
        except Exception as e:
            print("가사 정보가 없거나 성인 인증이 필요합니다")
            lyrics = ""
        finally:
            lyrics_list.append(lyrics)
            print(f"{song_name} 입력 완료")
            # 뒤로 가기
            driver.back()
            time.sleep(0.5)

    except Exception as e:
        print("에러!")

driver.quit()

song_data['song_title'] = titles
song_data['lyrics'] = lyrics_list

song_data.to_excel(f"{artist}_{album_name}_lyrics.xlsx", engine='openpyxl')
