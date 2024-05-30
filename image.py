from selenium.webdriver import Chrome
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib.request
import os

url = "https://www.google.com/"

opt = Options()
opt.add_experimental_option('detach', True)
# opt.add_argument("headless")


# 이미지 저장 폴더 생성
save_dir = "saved_images"
os.makedirs(save_dir, exist_ok=True)

# 검색
driver = Chrome(options=opt)
driver.get(url)
time.sleep(0.5)
keyword = "고양이 무료 png"

search = driver.find_element(By.ID, "APjFqb")
search.send_keys(keyword)
search.submit()
time.sleep(0.5)


# 이미지 탭 클릭
driver.find_element(By.LINK_TEXT, "이미지").click()
time.sleep(0.5)

""" 이미지 가져오기 : img src 주소 -> 마우스 오른쪽 클릭 -> 저장 """
"""이미지 검색 개수 및 다운로드"""
# 이미지 검색 개수
images = driver.find_elements(By.CSS_SELECTOR, "g-img.mNsIhb>img.YQ4gaf")
# print(images)
# print(len(images))  # => 97 개

# 이미지 링크 주소 (소스) 가져오기
links = []
for img in images:
    try:
        links.append(img.get_attribute('src'))
    except Exception as e:
        print(e)

print(f"이미지 개수: {len(links)}")
time.sleep(0.5)

# 이미지 저장 (다운로드)
# url_img = images[1].get_attribute('src')
# urllib.request.urlretrieve(url_img, "test.jpg")

scroll = driver.find_element(By.TAG_NAME, "body")
for i in range(10):
    scroll.send_keys(Keys.PAGE_DOWN)

for i in range(len(links)):
    url_img = images[i].get_attribute('src')
    if url_img is not None:
        urllib.request.urlretrieve(url_img, f"./{save_dir}/cat_image_{i+1}.png")
        print(f"image {i+1} downloaded")
        time.sleep(0.5)
    else:
        print("image url doesn't exist")

print("image download completed")
driver.quit()