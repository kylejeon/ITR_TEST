# -*- coding: utf-8 -*-

#from testlink import TestlinkAPIClient, TestLinkHelper
from doctest import TestResults
from unittest import TestResult, TextTestResult
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
#from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
#import ITR_Admin_Common
import json

## User: kyle
#URL = 'http://testserver-win:81/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
#DevKey = 'adcb86843d0c77e6e0c9950f80a143c0'
## testlink 초기화
#tl_helper = TestLinkHelper()
#testlink = tl_helper.connect(TestlinkAPIClient) 
#testlink.__init__(URL, DevKey)
#testlink.checkDevKey()

# 브라우저 설정
baseUrl = 'https://stagingworklist.onpacs.com'
#url = baseUrl + quote_plus(plusUrl)
driver = webdriver.Chrome()
driver.get(baseUrl)
#ITR_Admin_Common.close_popup()
# Notice 창 닫기
popup = driver.window_handles
while len(popup) != 1:
    driver.switch_to.window(popup[1])
    #driver.close()
    driver.find_element(By.ID, "notice_modal_cancel_week").click()
    popup = driver.window_handles
driver.switch_to.window(popup[0])
html = driver.page_source
#soup = BeautifulSoup(html)

# TestPlanID = AutoTest 버전 테스트
testPlanID = 2996
buildName = 1
 
class signInOut:
    def admin_sign_in(id, password):
        driver.find_element(By.ID, 'user-id').clear()
        driver.find_element(By.ID, 'user-id').send_keys(id)
        driver.find_element(By.ID, 'user-password').clear()
        driver.find_element(By.ID, 'user-password').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)
    def admin_sign_out():
        driver.find_element(By.CSS_SELECTOR, '.pull-right > span').click()

    # 정상적인 계정으로 로그인 한다.
    def normal_login():
        signInOut.admin_sign_in('yhjeon','1')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)
        # 인증서 비밀번호 입력 닫기
        driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div[2]/button[1]").click()

class windowSize:
    driver.set_window_size(1920, 1080)

class Login:
    def sign_InOut():
        testResult=""

        # 잘못된 user ID를 입력하고 sign in을 클릭한다
        signInOut.admin_sign_in('administrator','Server123!@#')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        # User not found
        try:
            assert driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/form/label").text=="Please confirm the password by retyping it in the confirm field."
        except:
            testResult = 'failed'

        ## 정상적인 계정으로 로그인 한다.
        #signInOut.admin_sign_in('yhjeon','1')
        #driver.find_element(By.CSS_SELECTOR, '.btn').click()
        #driver.implicitly_wait(5)
        ## 인증서 비밀번호 입력 닫기
        #driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div[2]/button[1]").click()
        # 정상적인 계정으로 로그인 한다.
        signInOut.normal_login()
        try:
            assert driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[7]/a/span").text == "Logout"
        except:
            testResult = 'failed'

        # 로그아웃 후, 로그인 페이지를 확인한다.
        driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[7]/a/span").click()
        driver.implicitly_wait(5)
        try:
            assert driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/form/div[1]").text == "Sign in to start your session"
        except:
            testResult = 'failed'

        ## sign_InOut 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2309, testPlanID, buildName, 'f', "Sign In/Out Test Failed")            
        #else:
        #    testlink.reportTCResult(2309, testPlanID, buildName, 'p', "Sign In/Out Test Passed")
    
    def Remember_me():
        testResult=""
        remember_id = "yhjeon"

        # Remember Me 클릭 후, 정상적인 계정으로 로그인 한다.
        driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/form/div[4]/div[1]/label").click()
        signInOut.normal_login()
        # 로그아웃 후, Remember Me와 id를 확인한다.
        driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[7]/a/span").click()
        driver.implicitly_wait(5)
        try:
            assert (driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/form/div[2]/div/input').get_property('defaultValue'), 
                    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/form/div[4]/div[1]/input').get_property("checked")) == (remember_id, True)
        except:
            testResult = 'failed'

        ## Remember_me 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2316, testPlanID, buildName, 'f', "Remember me Test Failed")            
        #else:
        #    testlink.reportTCResult(2316, testPlanID, buildName, 'p', "Remember me Test Passed")

class TOPMENU:
    def Badge_Emergency(cmr):
        testResult=""
        # badge 클릭
        driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/div[1]/div/div[2]/div[1]').click()
        # waiting loading
        try:
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            print("waitng 1.5 s")

        # worklist record Total 획득
        request = driver.wait_for_request('.*E&JobStatus=200&JobStartDate.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        recordTotal = data['recordsTotal']

        # 비교
        try:
            assert (cmr == recordTotal)
        except:
            testResult = 'failed'

        ## Badge_Emergency 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2351, testPlanID, buildName, 'f', "Badge Emergency Test Failed")            
        #else:
        #    testlink.reportTCResult(2351, testPlanID, buildName, 'p', "Badge Emergency Test Passed")

    def Badge():
        # 정상적인 계정으로 로그인
        signInOut.normal_login()
        # waiting loading
        try:
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            print("waitng 1.5 s")

        # 각 Badge의 표시 갯수 획득
        driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[6]/ul/li[9]/a").click()
        request = driver.wait_for_request('.*AllInstitutionList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        TotalPriorityCount = data['TotalPriorityCount']
        TotalReferCount = data['TotalReferCount']
        TotalAutoReferCount = data['TotalAutoReferCount']
        TotalScheduleReferCount = data['TotalScheduleReferCount']
        TotalReportedCompletedCount = data['TotalReportedCompletedCount']

        TOPMENU.Badge_Emergency(TotalPriorityCount)


TOPMENU.Badge()