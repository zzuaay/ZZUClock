# coding:utf-8
import os

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

os.environ["webdriver.chrome.driver"] = '/usr/bin/chromedriver'
option = webdriver.ChromeOptions()
option.add_argument('--headless')  # 启用无头模式
option.add_argument('--ignore-certificate-errors')  # 无视SSL错误
option.add_argument("blink-settings=imagesEnabled=false")  # 禁用图片
pref = {"profile.default_content_setting_values.geolocation": 2}
option.add_experimental_option("prefs", pref)  # 禁用地理位置
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 启用开发者模式
driver = webdriver.Chrome(options=option, executable_path="/usr/bin/chromedriver")  # 启动浏览器

err = 0
account = os.environ.get('ACCOUNT').split(';')  # 字符串预处理
for acc in account:
    usr = acc.split('-')
    try:
        driver.get('https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0')  # 进入登陆界面
    except selenium.common.exceptions.WebDriverException:
        print("SSL错误")  # TODO:SSL错误处理
        err += 1
        continue
    driver.implicitly_wait(1)

    driver.find_element(by=By.NAME, value='uid').send_keys(usr[0])
    driver.find_element(by=By.NAME, value='upw').send_keys(usr[1])
    driver.find_element(by=By.NAME, value='myform52').submit()  # TODO:连续登录可能会出现验证码
    driver.implicitly_wait(1)

    if driver.current_url == 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/login':  # 登录错误
        res = driver.find_element(by=By.XPATH, value='//*[@id="bak_0"]/div[2]/div[2]/div[2]/div[2]').text
        print(res)
        err += 1
    else:
        iframe = driver.find_element(by=By.NAME, value='zzj_top_6s')  # 进入信息确认界面
        driver.switch_to.frame(iframe)  # 切换为子页面
        res = driver.find_element(by=By.XPATH, value='//*[@id="bak_0"]/div[5]/span')
        if res.text == "今日您已经填报过了":
            print(res.text)
        else: 
            driver.find_element(by=By.XPATH, value='//*[@id="bak_0"]/div[11]/div[3]/div[4]').click()  # 进入打卡界面
            driver.implicitly_wait(1)

            driver.find_element(by=By.XPATH, value='//*[@id="btn416a"]').click()  # 点击提交
            driver.implicitly_wait(1)

            res = driver.find_element(by=By.XPATH, value='//*[@id="bak_0"]/div[2]/div[2]/div[2]/div[2]')
            if "感谢你今日上报健康状况" not in res.text:
                err += 1
            print(res.text)
driver.close()
if err > 0:
    print("打卡共", err, "个异常")
    raise Exception
else:
    print("打卡完成，无异常")
