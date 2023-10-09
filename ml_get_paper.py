from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import os
os.environ['HTTP_PROXY'] = "http://127.0.0.1:7890"
os.environ['HTTPS_PROXY'] = "http://127.0.0.1:7890"
# 启动浏览器
driver = webdriver.Chrome()
executable_path=chrome_path
# 打开目标页面
driver.get("https://openreview.net/group?id=NeurIPS.cc/2022/Conference#accepted-papers")

# 循环处理多个页面
for _ in range(10):
    # 获取当前页面的 HTML
    page_content = driver.page_source

    # 使用 BeautifulSoup 解析页面
    soup = BeautifulSoup(page_content, 'html.parser')

    # 处理当前页面的内容...

    # 定位下一页按钮并点击
    next_page_button = driver.find_element(By.CSS_SELECTOR, 'li[data-page-number="9"] a')
    next_page_button.click()

    # 等待页面加载完成（你可以根据实际情况调整等待时间）
    driver.implicitly_wait(10)

# 关闭浏览器
driver.quit()
