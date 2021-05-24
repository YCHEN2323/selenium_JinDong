#-*- coding = utf-8 -*-
#@Time : 2021/5/22 22:23
#@Author : ChenY
#@File : Chrome_test1.py
#@Software : PyCharm

'''
==========================
京东定时任务限时秒杀商品抢购程序
==========================
    ps：这几天学了python爬虫和selenium库之后，没地方发挥，因此有了这个脚本，耗时一天
    
    用到的库：
        1、schedule：一个可以设置定时任务的功能库。
        2、time、sleep：本项目主要用于函数休眠。
        3、json：用于保存cookie文件时的文本类型控制
        4、webdriver：属于selenium库下，负责操纵浏览器，不了解的话一定要去百度学习一下这个库，才能看懂后面的代码
'''
import schedule
import time
import json
from time import sleep
from selenium import webdriver


#获取cookie信息函数：免登录
def getCookie():

    browser = webdriver.Chrome(r'E:\chromedriver.exe')  #根据路径获得本地已下载驱动

    url = 'http://cart.jd.com'     #指定要打开的路径

    browser.get(url=url)        #根据路径打开网页
    sleep(15)               #休眠15s，以便第一次登录
    cookies = browser.get_cookies()     #获取cookie信息
    # 将 cookies 写入文件
    with open("cookies.txt", "w")  as f:
        json.dump(cookies, f)

    print('cookie写入成功！')


#根据cookie免登录
def setUp():

    browser = webdriver.Chrome(r'E:\chromedriver.exe')  #指定驱动
    browser.maximize_window()           #全屏显示
    url = "https://cart.jd.com/cart_index/#none"    #京东登录链接，可以不修改
    # 访问网站，清空旧cookies信息
    browser.get(url)
    browser.delete_all_cookies()

    # 加载 cookies信息
    with open("cookies.txt", "r") as f:
        cookies = json.load(f)
        for cookie in cookies:
            browser.add_cookie(cookie)

    # 验证是否登录成功
    browser.get(url)
    #将购物车宝贝全选，下单，提交订单
    sleep(57)
    joinAndPay(browser)


#将购物车宝贝全选，下单，提交订单
def joinAndPay(browser):

    #找到第一个checkBox（全选），查看是否选中
    if browser.find_element_by_xpath('//input[@class="jdcheckbox"]').is_selected():
        #如选中
        ele = browser.find_elements_by_class_name('common-submit-btn')
        for i in ele:
            sleep(0.1)
            i.click()
            sleep(0.1)
        browser.find_element_by_id('order-submit').click()
        #未选中
    else:
        browser.find_element_by_xpath('//input[@class="jdcheckbox"]').click()
        ele = browser.find_elements_by_class_name('common-submit-btn')
        for i in ele:
            sleep(0.1)
            i.click()
            sleep(0.1)
        browser.find_element_by_id('order-submit').click()
    sleep(2000)     #执行后不关闭页面，等待操作，保证有时间可以手动操作


#这是定时函数
def schedule_run():
    schedule.every().monday.at("00:15").do(setUp)   #设置定时任务日期和时间
    while True:         #通过循环暴力查看时间，保证执行
        schedule.run_pending()
        time.sleep(0.5)


'''运行步骤如下：
    1、先将‘步骤2’函数注释掉，保留‘步骤1’函数，运行主函数，
    然后15s内在弹出的界面进行扫码登录京东，程序会保存记录你的cookie信息，后面用于免登录
    2、将‘步骤1’函数注释掉，保留‘步骤2’函数，然后找到定时函数，设置周几的什么时候执行函数，
    然后在设置的时间之前启动主程序等待到时间即可。
'''

if __name__ == "__main__":

    #这是步骤1函数：获取cookie信息
    # getCookie()
    #这是步骤2函数：定时任务启动
    schedule_run()




