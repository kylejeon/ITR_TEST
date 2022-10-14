# -*- coding: utf-8 -*-

#from testlink import TestlinkAPIClient, TestLinkHelper
from ast import Try
from calendar import month
from doctest import TestResults
from mailbox import Babyl
from pickle import NONE
from tkinter import FALSE
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
from selenium.webdriver.common.keys import Keys
import json, math, time
from datetime import datetime, timedelta
#pip install python-dateutil
from dateutil.relativedelta import relativedelta
## User: kyle
#URL = 'http://testserver-win:81/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
#DevKey = 'adcb86843d0c77e6e0c9950f80a143c0'
## testlink 초기화
#tl_helper = TestLinkHelper()
#testlink = tl_helper.connect(TestlinkAPIClient) 
#testlink.__init__(URL, DevKey)
#testlink.checkDevKey()

# 브라우저 설정
WorklistUrl = 'http://vm-onpacs'
AdminUrl = 'http://vm-onpacs:8082'
#WorklistUrl = 'https://stagingworklist.onpacs.com'
#AdminUrl = 'http://stagingadmin.onpacs.com/'

#id password
worklist_id = "testInfReporter"
worklist_pw = "Server123!@#"
remember_id = "testInfReporter"
admin_id = "testSubadmin"
admin_pw = "Server123!@#"
#worklist_id = "yhjeon"
#worklist_pw = "1"
#remember_id = "yhjeon"
#admin_id = "INF_JH"
#admin_pw = "Server123!@#"

#url = baseUrl + quote_plus(plusUrl)
driver = webdriver.Chrome()
driver.get(WorklistUrl)
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
        signInOut.admin_sign_in(worklist_id,worklist_pw)
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)
        # 인증서 비밀번호 입력 닫기
        try:
            driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div[2]/button[1]").click()
        except:
            print("no cert")

class windowSize:
    driver.set_window_size(1920, 1080)

class Login:
    def sign_InOut():
        testResult=""
        Result_msg = "failed at "

        # 잘못된 user ID를 입력하고 sign in을 클릭한다
        signInOut.admin_sign_in('administrator','Server123!@#')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        # User not found
        try:
            assert driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/form/label").text=="Please confirm the password by retyping it in the confirm field."
        except:
            testResult = 'failed'
            Result_msg+="#3 "

        # 정상적인 계정으로 로그인 한다.
        signInOut.normal_login()
        try:
            assert driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[7]/a/span").text == "Logout"
        except:
            testResult = 'failed'
            Result_msg+="#2 "

        # 로그아웃 후, 로그인 페이지를 확인한다.
        driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[7]/a/span").click()
        driver.implicitly_wait(5)
        try:
            assert driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/form/div[1]").text == "Sign in to start your session"
        except:
            testResult = 'failed'
            Result_msg+="#4 "

        ## sign_InOut 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2309, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2309, testPlanID, buildName, 'p', "Sign In/Out Test Passed")
    
    def Remember_me():
        testResult=""
        Result_msg = "failed at "

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
            Result_msg+="#1 "

        ## Remember_me 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2316, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2316, testPlanID, buildName, 'p', "Remember me Test Passed")

class TOPMENU:
    def Badge_Emergency():
        testResult=""
        Result_msg = "failed at "

        # 캡처 초기화
        del driver.requests
        # badge 클릭
        driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/div[1]/div/div[2]/div[1]').click()
        # waiting loading
        try:
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Badge의 표시 갯수 획득
        request = driver.wait_for_request('.*AllInstitutionList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        cmr = data['TotalPriorityCount']

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
            Result_msg+="#1 "

        ## Badge_Emergency 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2351, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2351, testPlanID, buildName, 'p', "Badge Emergency Test Passed")

    def Badge_Refer():
        testResult=""
        Result_msg = "failed at "

        # 캡처 초기화
        del driver.requests
        # badge 클릭
        driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/div[2]/div/div[2]/div[1]').click()
        # waiting loading
        try:
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Badge의 표시 갯수 획득
        request = driver.wait_for_request('.*AllInstitutionList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        cmr = data['TotalReferCount']

        # worklist record Total 획득
        request = driver.wait_for_request('./GetReferCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        recordTotal = data['recordsTotal']

        # 비교
        try:
            assert (cmr == recordTotal)
        except:
            testResult = 'failed'
            Result_msg+="#1 "

        ## Badge_Refer 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2354, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2354, testPlanID, buildName, 'p', "Badge Refer Test Passed")

    def Badge_AutoRefer():
        testResult=""
        Result_msg = "failed at "

        # 캡처 초기화
        del driver.requests
        # badge 클릭
        driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/div[3]/div/div[2]/div[1]').click()
        # waiting loading
        try:
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Badge의 표시 갯수 획득
        request = driver.wait_for_request('.*AllInstitutionList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        cmr = data['TotalAutoReferCount']
        TotalScheduleReferCount = data['TotalScheduleReferCount']
        TotalReportedCompletedCount = data['TotalReportedCompletedCount']

        # worklist record Total 획득
        request = driver.wait_for_request('.*NotRefered=true.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        recordTotal = data['recordsTotal']

        # 비교
        try:
            assert (cmr == recordTotal)
        except:
            testResult = 'failed'
            Result_msg+="#1 "

        ## Badge_AutoRefer 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2357, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2357, testPlanID, buildName, 'p', "Badge AutoRefer Test Passed")

    def Badge_Schedule():
        testResult=""
        Result_msg = "failed at "

        # 캡처 초기화
        del driver.requests
        # badge 클릭
        driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/div[4]/div/div[2]/div[1]').click()
        # waiting loading
        try:
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Badge의 표시 갯수 획득
        request = driver.wait_for_request('.*AllInstitutionList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        cmr = data['TotalScheduleReferCount']
        TotalReportedCompletedCount = data['TotalReportedCompletedCount']

        # worklist record Total 획득
        request = driver.wait_for_request('./GetScheduleReferCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        recordTotal = data['recordsTotal']

        # 비교
        try:
            assert (cmr == recordTotal)
        except:
            testResult = 'failed'
            Result_msg+="#1 "

        ## Badge_Schedule 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2360, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2360, testPlanID, buildName, 'p', "Badge Schedule Test Passed")

    def Badge_Today():
        testResult=""
        Result_msg = "failed at "

        # 캡처 초기화
        del driver.requests
        # badge 클릭
        driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/div[5]/div/div[2]/div[1]').click()
        # waiting loading
        try:
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Badge의 표시 갯수 획득
        request = driver.wait_for_request('.*AllInstitutionList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        cmr = data['TotalReportedCompletedCount']

        # worklist record Total 획득
        request = driver.wait_for_request('./GetCompletedReportedJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        recordTotal = data['recordsTotal']

        # 비교
        try:
            assert (cmr == recordTotal)
        except:
            testResult = 'failed'
            Result_msg+="#1 "

        ## Badge_Today 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2363, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2363, testPlanID, buildName, 'p', "Badge Today Test Passed")

    def Badge():
        # 정상적인 계정으로 로그인
        signInOut.normal_login()

        TOPMENU.Badge_Emergency()
        TOPMENU.Badge_Refer()
        TOPMENU.Badge_AutoRefer()
        TOPMENU.Badge_Schedule()
        TOPMENU.Badge_Today()

    def Home():
        testResult=""
        Result_msg = "failed at "

        # 정상적인 계정으로 로그인
        signInOut.normal_login()

        
        # Direct Message 접속 및 Home 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/a").click()
        try:
            WebDriverWait(driver, 1.5).until(EC.presence_of_element_located((By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/ul/li[4]/a/div/p")))
        except:
            pass
        element = driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/ul/li[4]/a/div/p")
        driver.execute_script("arguments[0].click();", element)
        #driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/ul/li[4]/a/div/p").send_keys(Keys.ENTER)
        driver.implicitly_wait(5)
        driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[1]/a").click()
        driver.implicitly_wait(5)
        # Home 화면 확인
        try:
            assert driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[2]/div[1]/div[1]/div/div[1]/div/h2").text == "All Hospital"
        except:
            testResult = 'failed'
            Result_msg+="#1 "

        try:
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/nav/div/div[2]/ul/li[5]/a")))
        except:
            pass
        # Settings 접속 및 Home 버튼 클릭
        #driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[5]/a").send_keys(Keys.ENTER)
        element = driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[5]/a")
        driver.execute_script("arguments[0].click();", element)
        driver.implicitly_wait(5)
        driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[1]/a").click()
        driver.implicitly_wait(5)
        # Home 화면 확인
        try:
            assert driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[2]/div[1]/div[1]/div/div[1]/div/h2").text == "All Hospital"
        except:
            testResult = 'failed'
            Result_msg+="#1 "

        try:
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/nav/div/div[2]/ul/li[6]/a")))
        except:
            pass
        # Statistics 접속 및 Home 버튼 클릭
        element = driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[6]/a")
        driver.execute_script("arguments[0].click();", element)
        driver.implicitly_wait(5)
        driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[1]/a").click()
        driver.implicitly_wait(5)
        # Home 화면 확인
        try:
            assert driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[2]/div[1]/div[1]/div/div[1]/div/h2").text == "All Hospital"
        except:
            testResult = 'failed'
            Result_msg+="#1 "

        ## Home 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2367, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2367, testPlanID, buildName, 'p', "Home Test Passed")

    def new_message():
        testResult=""
        Result_msg = "failed at "

        # 정상적인 계정으로 로그인
        signInOut.normal_login()
        
        # waiting loading
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # READ_FLAG T or F 확인 (파란색 회색 확인) 및 읽지 않은 메시지 수 확인 #2
        element = driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/a/span")
        driver.execute_script("arguments[0].click();", element)
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]/span")))
        except:
            pass
        request = driver.wait_for_request('.*/GetDirectMessageList')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        read_count=0
        for n in data:
            if(n['READ_FLAG'] == 'F'):
                read_count = read_count + 1
            elif(n['READ_FLAG']=='T'):
                pass
            else:
                testResult="failed"
                Result_msg+="#2 "

        # 메인화면 읽지 않은 메시지 수 존재 확인 #1
        try:
            assert (int(driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/a/sup/span").text) == read_count)
        except:
            testResult = 'failed'
            Result_msg+="#1 "
        

        # 캡처 초기화
        del driver.requests

        # new message 접속 및 패킷에서 정보 획득 #3
        element = driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/ul/li[2]/div/ul/li/a")
        driver.execute_script("arguments[0].click();", element)
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[1]")))
        except:
            pass

        # msg_Center
        request = driver.wait_for_request('.*/GetAccessCenterList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)['data']
        msg_center = data[0]['CENTER_CODE']

        # msg_Institution
        request = driver.wait_for_request('.*/GetAccessInstitutionList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)['data']
        msg_insti = []
        for n in data:
            msg_insti.append(n['INSTITUTION_NAME'])

        # msg_Reporter
        request = driver.wait_for_request('.*/GetAccessReporterList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)['data']
        msg_reporter = []
        for n in data:
            msg_reporter.append(n['USER_NAME'])

        # Admin에서 정보 획득 시작
        # 새로운 탭 + 전환
        driver.execute_script("window.open()")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(AdminUrl);

        # admin 사이트 로그인
        driver.find_element(By.ID, 'user-id').clear()
        driver.find_element(By.ID, 'user-id').send_keys(admin_id)
        driver.find_element(By.ID, 'user-password').clear()
        driver.find_element(By.ID, 'user-password').send_keys(admin_pw)
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)

        # Configuration
        element = driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[2]/div[1]/ul/li[5]/a')
        driver.execute_script("arguments[0].click();", element)
        driver.implicitly_wait(5)

        # 캡처 초기화
        del driver.requests

        # 아이디 검색 및 패킷에서 center 정보 습득
        driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[3]/div/div/input').send_keys(worklist_id)
        driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[6]/div/button').click()
        driver.implicitly_wait(5)
        request = driver.wait_for_request('.*/GetUserList.*')
        body = request.response.body.decode('utf-8')
        data = (json.loads(body))['data']
        adm_center = ""
        for n in data:
            if n['UserID'] == worklist_id:
                adm_center = n['CenterCode']
                break

        # Download Control 에서 ID 검색
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/button[3]").click()
        driver.implicitly_wait(5)
        # 캡처 초기화
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[3]/div/div/input").send_keys(worklist_id)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[5]/button").click()
        # 캡처 및 institution 정보 획득
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/div[1]/a[2]/span")))
        except:
            pass
        request = driver.wait_for_request('.*/GetDownloadControlByInstList.*'+worklist_id+'.*')
        body = request.response.body.decode('utf-8')
        data = (json.loads(body))['data']
        adm_insti = []
        for n in data:
            if worklist_id in n["UserName"]:
                adm_insti.append(n['InstitutionName'])

        # Direct Message Setting, reporter 정보 획득
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[7]/a").click()
        driver.implicitly_wait(5)
        element = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/button[3]")
        driver.execute_script("arguments[0].click();", element)
        driver.implicitly_wait(5)
        # 첫 페이지 캡처
        request = driver.wait_for_request('.*/GetDirectMessageAuthorizedReporter.*')
        body = request.response.body.decode('utf-8')
        data = (json.loads(body))
        adm_reporter = []
        for n in data['data']:
            adm_reporter.append(n['USER_NAME'])

        # 복수 페이지 확인 및 캡처 진행
        total = math.trunc(data['recordsTotal'] / data['Length'])
        for repeat in range(0,total):
            request = driver.wait_for_request('.*/GetDirectMessageAuthorizedReporter.*')
            body = request.response.body.decode('utf-8')
            data = (json.loads(body))['data']

            for n in data:
                    adm_reporter.append(n['USER_NAME'])

            # 캡처 초기화 및 다음페이지
            del driver.requests
            try:
                WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div[3]/div/div/div[4]/ul/li[3]/a")))
            except:
                pass
            element = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div[3]/div/div/div[4]/ul/li[3]/a")
            driver.execute_script("arguments[0].click();", element)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        # Admin에서 정보획득 종료
   
        #insti & reporter > List > sorting
        msg_insti.sort()
        msg_reporter.sort()
        adm_insti.sort()
        adm_reporter.sort()

        # 비교
        try:
            assert((msg_center == adm_center) and (msg_insti == adm_insti) and (msg_reporter == adm_reporter))
        except:
            testResult = 'failed'
            Result_msg+="#3 "

        # 체크 및 체크 해제 #4
        # Institution
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
        except:
            testResult = 'failed'
            Result_msg+="#4 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = 'failed'
            Result_msg+="#4 "
        except:
            pass

        # Center
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[2]/a").click()
        WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr/td[1]/label").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
        except:
            testResult = 'failed'
            Result_msg+="#4 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr/td[1]/label").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = 'failed'
            Result_msg+="#4 "
        except:
            pass

        # Reporter
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[3]/a").click()
        WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
        except:
            testResult = 'failed'
            Result_msg+="#4 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = 'failed'
            Result_msg+="#4 "
        except:
            pass

        # 체크 및 삭제아이콘 선택 #5
        # Institution
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[1]/a").click()
        WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
        except:
            testResult = 'failed'
            Result_msg+="#5 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = 'failed'
            Result_msg+="#5 "
        except:
            pass

        # Center
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[2]/a").click()
        WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr/td[1]/label").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
        except:
            testResult = 'failed'
            Result_msg+="#5 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = 'failed'
            Result_msg+="#5 "
        except:
            pass

        # Reporter
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[3]/a").click()
        WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
        except:
            testResult = 'failed'
            Result_msg+="#5 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = 'failed'
            Result_msg+="#5 "
        except:
            pass

        # Recipient를 선택하지 않고, 다음 버튼을 클릭 #7
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[4]").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[13]/div[7]/div/button")))
            driver.find_element(By.XPATH, "/html/body/div[13]/div[7]/div/button").click()
        except:
            testResult = 'failed' 
            Result_msg+="#7 "
      
        # Recipient 선택 후, 다음 버튼 클릭 #6
        # Institution
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[1]/a").click()
        WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[4]").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]")))
            driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]").click()
        except:
            testResult = 'failed' 
            Result_msg+="#6 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i").click()
        
        # Center
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[2]/a").click()
        WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr/td[1]/label").click()
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[4]").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]")))
            driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]").click()
        except:
            testResult = 'failed'
            Result_msg+="#6 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i").click()

        # Reporter
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[3]/a").click()
        WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[4]").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]")))
            driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]").click()
        except:
            testResult = 'failed'
            Result_msg+="#6 "

        # Message 입력창에 메시지를 입력하지 않고, 전송 버튼을 클릭 #10
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[4]").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]")))
            driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[3]").click()
            try:
                WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[13]/div[7]/div/button")))
                driver.find_element(By.XPATH, "/html/body/div[13]/div[7]/div/button").click()
            except:
                testResult='failed'
                Result_msg+="#10 "
        except:
            testResult = 'failed' 
            Result_msg+="#10 "

        # 임의의 메시지를 입력하고, 이전 버튼을 클릭, 그리고 다시 다음 버튼 클릭 #8
        if(testResult == ''):
            rnd_msg = "rnd_msg"
            driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[2]/div/div/div[2]/textarea").send_keys(rnd_msg)
            driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]").click()
            try:
                WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[4]")))
                driver.find_element(By.XPATH,"/html/body/div[8]/div/div/div[3]/div/div/button[4]").click()
                try:
                    WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[3]")))
                    assert(driver.find_element(By.XPATH,"/html/body/div[8]/div/div/div[2]/section[2]/div/div/div[2]/textarea").get_property("value")==rnd_msg)
                except:
                    testResult = 'failed'
                    Result_msg+="#8 "
            except:
                testResult = 'failed'
                Result_msg+="#8 "
        
        # Message 입력창에 메시지를 입력하고, 전송 버튼을 클릭 #9
        if(testResult == ''):
            driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[3]").click()
            try:
                WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[12]/div[7]/div/button")))
                driver.find_element(By.XPATH,"/html/body/div[12]/div[7]/div/button").click()
            except:
                testResult = 'failed'
                Result_msg+="#9 "
        
        # Message 입력창에 메시지를 입력하고, 취소 버튼을 클릭 #11
        if(testResult == ''):
            driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/a/span").click()
            try:
                WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/ul/li[2]/div/ul/li/a")))
                driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/ul/li[2]/div/ul/li/a").click()
                # new message

                try:
                    WebDriverWait(driver, 0.3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[1]/div/div/div/div[4]/ul/li[1]/a")))
                except:
                    pass
                driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[3]/a").click()                
                WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label")))
                driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label").click()

                WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
                driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[4]").click()

                WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[1]")))
                rnd_msg="rnd_msg"
                driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[2]/div/div/div[2]/textarea").send_keys(rnd_msg)
                driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[1]").click()
            except:
                testResult = 'failed'
                Result_msg+="#11 "

        ## new_message 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2371, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2371, testPlanID, buildName, 'p', "new_message Test Passed")

    def Message():
        testResult=""
        Result_msg = "failed at "

        # 정상적인 계정으로 로그인
        signInOut.normal_login()
        
        # waiting loading
        try:
            WebDriverWait(driver, 0.25).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass
        
        # 1,2는 new_message와 동일

        # Direct Message 아이콘을 클릭 및 리스트 확인 #3
        driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[3]/a/span").click()
        # waiting loading
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]/span")))
        except:
            pass
        
        # 10개 이상인 경우 확인
        request = driver.wait_for_request('.*/GetDirectMessageList')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        read_count=0
        for n in data:
            if(n['READ_FLAG'] == 'F'):
                read_count = read_count + 1

        if(read_count >= 10):
            try:
                WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/ul/li[3]/div/ul/li[10]/a")))
            except:
                testResult = 'failed'
                Result_msg+="#0 "

        # View more messages확인 
        try:
            assert(driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[3]/ul/li[4]/a/div/p").get_property("outerText")=="View more messages")
        except:
            testResult = 'failed'
            Result_msg+="#3 "

        # 임의의 메시지를 클릭 #4
        # 패킷에서 정보 획득
        sender = data[0]["WRITER_NAME"]
        sender_time = data[0]["WRITE_DTTM"]
        sender_time = sender_time.replace('T',' ')
        sender_msg = data[0]["MESSAGE_TEXT_LOB"]

        driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/ul/li[3]/div/ul/li[1]/a/div[1]/i").click()
        # waiting loading
        try:
            WebDriverWait(driver, 0.25).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass
        # 비교
        try:
            assert(sender == driver.find_element(By.XPATH, "/html/body/div[9]/div/div/div[2]/div[1]/div[2]/span").get_property("value") and
                   sender_time == driver.find_element(By.XPATH, "/html/body/div[9]/div/div/div[2]/div[2]/div[2]/span").get_property("value") and
                   sender_msg == driver.find_element(By.XPATH, "/html/body/div[9]/div/div/div[2]/div[3]/textarea").get_property("value"))
        except:
            testResult = 'failed'
            Result_msg+="#4 "
        driver.find_element(By.XPATH, "/html/body/div[9]/div/div/div[3]/button").click()

        ## message 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2384, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2384, testPlanID, buildName, 'p', "Message Test Passed")

    def View_More_Messages():
        testResult=""
        Result_msg = "failed at "

        # 정상적인 계정으로 로그인
        signInOut.normal_login()
        
        # waiting loading
        try:
            WebDriverWait(driver, 0.25).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # View more messages 접속
        driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[3]/a/span").click()
        # waiting loading
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]/span")))
        except:
            pass
        element = driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[3]/ul/li[4]/a/div/p")
        driver.execute_script("arguments[0].click();", element)
        # waiting loading
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[4]/div/div[1]/div/div[1]/div")))
        except:
            pass

        # 리스트 및 아이콘 확인 / 읽지 않은 메시지 클릭 #1 #2
        # 1 - 리스트 확인
        try:
            assert(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[4]/div/div[1]/div/div[2]/button").get_property("id") == "direct_message_all_list_tab")
        except:
            testResult = 'failed'
            Result_msg+="#1 "

        # 2 - read unread_count at icon
        unread_count = driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/a/sup/span").text

        # 1 - Read 정보 획득 (패킷)
        request = driver.wait_for_request('.*/GetDirectMessageList')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        read_flag = []
        list_len = len(data)
        for n in data:
            read_flag.append(n["READ_FLAG"])

        # 2 - 
        non_read_index = read_flag.index('F')
        non_read_name_pack = data[non_read_index]["WRITER_NAME"]
        non_read_dtm_pack = (data[non_read_index]["WRITE_DTTM"]).replace('T', ' ')
        non_read_msg_pack = data[non_read_index]["MESSAGE_TEXT_LOB"]

        # 1 - 아이콘 정보 획득
        request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total_list = data["recordsFiltered"] 
        remain_list = total_list 
        max_length = data["Length"]

        # 2 -
        first_non_read_loc = (non_read_index) % max_length
        first_non_read_page = (int)((non_read_index) / max_length) + 1
        current_page = 1

        # 1 - 
        icon=[]
        if remain_list <= max_length:
            for i in range(1,remain_list+1):
                icon.append(driver.find_element(By.XPATH, ("/html/body/section[1]/div/div/div/section[4]/div/div[2]/div/div/div/div/table/tbody/tr["+str(i)+"]/td[1]/span/i")).value_of_css_property("color"))
        # 2 - Get First Non Read Msg Info at First Page
        if first_non_read_page == 1:
            driver.find_element(By.XPATH, ("/html/body/section[1]/div/div/div/section[4]/div/div[2]/div/div/div/div/table/tbody/tr["+str(int(first_non_read_loc)+1)+"]/td[1]/span/i")).click()
            # waiting loading
            try:
                WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[4]/div/div[3]/div/div[3]/textarea")))
            except:
                testResult = 'failed'
                Result_msg+="#2 "
            non_read_name = data["data"][first_non_read_loc]["WRITER_NAME"]
            non_read_dtm = (data["data"][first_non_read_loc]["WRITE_DTTM"]).replace('T', ' ')
            non_read_msg = data["data"][first_non_read_loc]["MESSAGE_TEXT_LOB"]
            read_flag[non_read_index] = 'T'

        # waiting loading
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[4]/div/div[2]/div/div/div/div/div[3]")))
        except:
            pass

        # 1 - Get Icon Info
        while (1):
            for i in range(1,15):
                icon.append(driver.find_element(By.CSS_SELECTOR, "#message_list_group > tbody > tr:nth-child("+str(i)+") > td:nth-child(1) > span > i").value_of_css_property("color"))

            # 2 - 캡처 초기화
            del driver.requests

            # Next 클릭
            element = driver.find_element(By.CSS_SELECTOR, "#message_list_group_next > a")
            driver.execute_script("arguments[0].click();", element)
            # waiting loading
            time.sleep(0.5)

            # 2 - Get First Non Read Msg Info at First(X) Page
            current_page += 1
            if(current_page == first_non_read_page):
                request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)
                driver.find_element(By.XPATH, ("/html/body/section[1]/div/div/div/section[4]/div/div[2]/div/div/div/div/table/tbody/tr["+str(int(first_non_read_loc)+1)+"]/td[1]/span/i")).click()
                try:
                    WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[4]/div/div[3]/div/div[3]/textarea")))
                except:
                    testResult = 'failed'
                    Result_msg+="#2 "
                non_read_name = data["data"][first_non_read_loc]["WRITER_NAME"]
                non_read_dtm = (data["data"][first_non_read_loc]["WRITE_DTTM"]).replace('T', ' ')
                non_read_msg = data["data"][first_non_read_loc]["MESSAGE_TEXT_LOB"]
                read_flag[non_read_index] = 'T'

            remain_list = remain_list - max_length
            if (remain_list - max_length) <= 0:
                break
        for i in range(1,remain_list+1):
            icon.append(driver.find_element(By.CSS_SELECTOR, "#message_list_group > tbody > tr:nth-child("+str(i)+") > td:nth-child(1) > span > i").value_of_css_property("color"))

        # style="color:grey" - rgba(128, 128, 128, 1) / style="color:orange" - rgba(255, 165, 0, 1)
        # 1-아이콘 비교
        for i in range(0,list_len):
            if(read_flag[i]=='T'):
                if(icon[i] != "rgba(128, 128, 128, 1)"):
                    testResult = 'failed'
                    Result_msg+="#1 "
            else:
                if(icon[i] != "rgba(255, 165, 0, 1)"):
                    testResult = 'failed'
                    Result_msg+="#1 "

        # 2 & 3 - 
        try:
            assert(int(driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[3]/a/sup/span").get_property("textContent")) == (int(unread_count)-1) and
                   non_read_name == non_read_name_pack and 
                   non_read_dtm == non_read_dtm_pack and
                   non_read_msg == non_read_msg_pack and
                   int(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[4]/div/div[1]/div/div[2]/button/span[2]").text) == (int(unread_count)-1))
        except:
            testResult = 'failed'
            Result_msg+="#2 #3 "

        # Direct Message 리스트에서 Next를 클릭 #3
        # View more messages 접속
        driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[3]/a/span").click()
        # waiting loading
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]/span")))
        except:
            pass
        element = driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[3]/ul/li[4]/a/div/p")
        driver.execute_script("arguments[0].click();", element)
        # waiting loading
        try:
            element = driver.find_element(By.CSS_SELECTOR, "#message_list_group_next > a")
            driver.execute_script("arguments[0].click();", element)
        except:
            testResult = 'failed'
            Result_msg+="#3 "

        ## View_More_Message 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2390, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2390, testPlanID, buildName, 'p', "View_More_Message Test Passed")
        
    def Setting():
        testResult=""
        Result_msg = "failed at "

        # 정상적인 계정으로 로그인
        signInOut.normal_login()
        
        # waiting loading
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-setting > i")
        driver.execute_script("arguments[0].click();", element)

        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting_user_profile"))) 
        except:
            testResult = 'failed'
            Result_msg+="#1 "

        ## Setting 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2404, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2404, testPlanID, buildName, 'p', "Setting Test Passed")

    def Report_Search_Filter():
        testResult=""
        Result_msg = "failed at "

        # 정상적인 계정으로 로그인
        signInOut.normal_login()
        
        # waiting loading
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # 캡처 초기화
        del driver.requests

        # Setting 접속
        element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-setting > i")
        driver.execute_script("arguments[0].click();", element)

        # waiting loading
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting_user_profile"))) 
        except:
            testResult = 'failed'
            Result_msg+="#0 "

        # Select Group 코드 #1
        request = driver.wait_for_request('.*/GetGroupCode.*')
        body = request.response.body.decode('utf-8')
        data = (json.loads(body))
        # 2 - 준비
        search_group = data[0]

        for n in range(0, len(data)):
            if(data[n]==None):
                data[n]='ETC-Group'

        gr_list = []
        driver.find_element(By.CSS_SELECTOR, "#stdreport-group-code").click()
        for n in range(2,len(data)+2):
            temp_group = driver.find_element(By.CSS_SELECTOR, "#stdreport-group-code > option:nth-child("+str(n)+")").text
            if temp_group not in gr_list:
                gr_list.append(temp_group)
        
        data.sort()
        gr_list.sort()

        try:
            assert (data == gr_list)
        except:
            testResult="failed"
            Result_msg+="#1 "
        
        # 3 - 준비
        request = driver.wait_for_request('.*/GetReportCode.*')
        body = request.response.body.decode('utf-8')
        report_list_pk = (json.loads(body))
        
        # Group Code Search #2
        if(len(data) < 2):
            testResult="failed"
            Result_msg+="#2-pre_condition "

        if(testResult == ''):
            # 캡처 초기화
            del driver.requests

            driver.find_element(By.CSS_SELECTOR, "#stdreport-group-code").click()
            driver.find_element(By.CSS_SELECTOR, "#stdreport-group-code > option:nth-child(2)").click()
            driver.find_element(By.CSS_SELECTOR, "#stdreport_search_btn > span").click()
            time.sleep(0.3)

            request = driver.wait_for_request('.*/GetStandardReportForTable.*')
            body = request.response.body.decode('utf-8')
            data = (json.loads(body))["data"]

            for n in data:
                if(n["StdReportGroup"] != search_group):
                    testResult="failed"
                    Result_msg+="#2 "

            # Report ALL Search #3
            driver.find_element(By.CSS_SELECTOR, "#stdreport-report-code").click()

            report_list = []
            for n in range(2,len(report_list_pk)+2):
                temp_report= driver.find_element(By.CSS_SELECTOR, "#stdreport-report-code > option:nth-child("+str(n)+")").text
                if temp_report not in report_list:
                    report_list.append(temp_report)
            
            # 4 - 준비
            select_report = report_list_pk[0]
            # 3
            report_list_pk.sort()
            report_list.sort()

            try:
                assert (report_list_pk == report_list)
            except:
                testResult="failed"
                Result_msg+="#3 "

            # Report Search #4
            # 캡처 초기화
            del driver.requests

            driver.find_element(By.CSS_SELECTOR, "#stdreport-report-code > option:nth-child(2)").click()
            driver.find_element(By.CSS_SELECTOR, "#stdreport_search_btn > span").click()
            time.sleep(0.3)

            request = driver.wait_for_request('.*/GetStandardReportForTable.*')
            body = request.response.body.decode('utf-8')
            data = (json.loads(body))["data"]

            try:
                assert(data[0]["StdReportCode"]==select_report)
            except:
                testResult="failed"
                Result_msg+="#4 "

            # 캡처 초기화
            del driver.requests

            # Clear #7
            driver.find_element(By.CSS_SELECTOR, "#stdreport_search_clear_btn > span").click()
            try:
                request = driver.wait_for_request('.*/GetStandardReportForTable.*')
                body = request.response.body.decode('utf-8')
                data = (json.loads(body))["data"]
            except:
                testResult="failed"
                Result_msg+="#7 "


        if testResult == '':
            # ALL Hot Key #5
            driver.find_element(By.CSS_SELECTOR, "#stdreport_search_hotkey").click()
            origin_hot_key_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'E', 'F','G', 
                                  'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'T', 'U', 'V', 'W','X', 
                                  'Y', 'Z']

            # 6 - 준비
            hotkey_select = None
            for n in data:
                if n["HotKey"] != None:
                    hotkey_select = n["HotKey"]
                    break

            #5+ 6 - 준비
            hot_key_list = []
            for n in range(2,36):
                hotkey = driver.find_element(By.CSS_SELECTOR, "#stdreport_search_hotkey > option:nth-child("+str(n)+")").text
                hot_key_list.append(hotkey)
                if hotkey == hotkey_select:
                    hotkey_number = n

            try:
                assert(origin_hot_key_list == hot_key_list)
            except:
                testResult="failed"
                Result_msg+="#5 "

            # Hot Key Search #6
            if hotkey_select == None:
                testResult="failed"
                Result_msg+="#6-pre_condition "

            # 캡처 초기화
            del driver.requests
            
            driver.find_element(By.CSS_SELECTOR, "#stdreport_search_hotkey > option:nth-child("+str(hotkey_number)+")").click()
            driver.find_element(By.CSS_SELECTOR, "#stdreport_search_btn > span").click()
            time.sleep(0.3)

            request = driver.wait_for_request('.*/GetStandardReportForTable.*')
            body = request.response.body.decode('utf-8')
            data = (json.loads(body))["data"]

            for n in data:
                if(n["HotKey"]!=hotkey_select):
                    testResult="failed"
                    Result_msg+="#6 "

        ## Report_Search_Filter 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2407, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2407, testPlanID, buildName, 'p', "Report_Search_Filter Test Passed")

    def Report_Add():
        testResult=""
        Result_msg = "failed at "

        # 정상적인 계정으로 로그인
        signInOut.normal_login()
        
        # waiting loading
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Setting 접속
        element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-setting > i")
        driver.execute_script("arguments[0].click();", element)

        # waiting loading
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting_user_profile"))) 
        except:
            testResult = 'failed'
            Result_msg+="#0 "

        # Add Click #1
        driver.find_element(By.CSS_SELECTOR, "#stdreport_add_btn > span").click()
        
        # 탭 전환
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[1])
        try:
            assert(driver.find_element(By.CSS_SELECTOR, "#add-stdreport-creator").get_property("value")==worklist_id)
        except:
            testResult = 'failed'
            Result_msg+="#1 "

        if testResult == '':
            # new Group Code, Auto Expand, Report Code, Des, Hot Key, Report, Conclusion #2 & 3 & 5 & 6 & 7 & 9 & 10
            # 2 - input (rnd_gr_code)
            driver.find_element(By.CSS_SELECTOR, "#add-stdreport-groupcode-input").send_keys("rnd_gr_code")
            # 3 - input (CT)
            driver.find_element(By.CSS_SELECTOR, "#add-stdreport-auto-expand").send_keys("CT")
            # 5 - input (rnd_rp_code)
            driver.find_element(By.CSS_SELECTOR, "#add-stdreport-report-code").send_keys("rnd_rp_code")
            # 6 - input (rnd_desc)
            driver.find_element(By.CSS_SELECTOR, "#add-stdreport-desc").send_keys("rnd_desc")
            # 7 - input (z)
            driver.find_element(By.CSS_SELECTOR, "#add_stdreport_hotKey_chosen > a > span").click()
            time.sleep(0.3)
            driver.find_element(By.CSS_SELECTOR, "#add_stdreport_hotKey_chosen > div > div > input[type=text]").send_keys("Z")
            driver.find_element(By.CSS_SELECTOR, "#add_stdreport_hotKey_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            # 9  - input (a1!)
            driver.find_element(By.CSS_SELECTOR, "#add-stdreport-report-text").send_keys("a1!")
            # 10 - input (a1!)
            driver.find_element(By.CSS_SELECTOR, "#add-stdreport-report-conclusion").send_keys("a1!")
            #save click
            driver.find_element(By.CSS_SELECTOR, "#add-stdreport-save-btn").click()
            #waiting loading
            try:
                WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"))
            except:
                pass
            #text check
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text == 
                       "Are you sure to save new standard report?")
            except:
                testResult = 'failed'
                Result_msg+="#2 #3 #5 #6 #7 #9 #10 "
            
            #cancel click & check
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#add-stdreport-creator").get_property("value")==worklist_id)
            except:
                testResult = 'failed'
                Result_msg+="#2 #3 #5 #6 #7 #9 #10 "

            #save click
            driver.find_element(By.CSS_SELECTOR, "#add-stdreport-save-btn").click()
            try:
                WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"))
            except:
                pass

            #ok click
            element = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.3)

            #탭 전환
            driver.switch_to.window(driver.window_handles[0])

        if testResult == '':
            # 3 - 
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-home").click()
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "#search-job-modality").send_keys("CT")
            driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
            # 캡처 초기화
            del driver.requests
            time.sleep(0.25)

            driver.find_element(By.CSS_SELECTOR, "#job-report").click()
            
            # 탭 전환
            time.sleep(2.5)
            driver.switch_to.window(driver.window_handles[1])
            # AutoExpand check through packet
            request = driver.wait_for_request('.*/GetStdReportExFolderAutoExpand.*'+'CT')
            body = request.response.body.decode('utf-8')
            data = (json.loads(body))
            if 'rnd_gr_code' not in data:
                testResult = 'failed'
                Result_msg+="#3 "
                

            #탭 전환
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
            # already, close  #4 & 8 & 11
            # Setting 접속
            element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-setting > i")
            driver.execute_script("arguments[0].click();", element)
            
            # waiting loading
            try:
                WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting_user_profile"))) 
            except:
                testResult = 'failed'
                Result_msg+="#4&#8#11_pre-condition "

            # Add Click 
            driver.find_element(By.CSS_SELECTOR, "#stdreport_add_btn > span").click()
        
            # 탭 전환
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[1])
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#add-stdreport-creator").get_property("value")==worklist_id)
            except:
                testResult = 'failed'
                Result_msg+="#4&#8#11_pre-condition "

            # 4- input (rnd_rp_code)
            driver.find_element(By.CSS_SELECTOR, "#add-stdreport-report-code").send_keys("rnd_rp_code")

            # 4 - save click
            driver.find_element(By.CSS_SELECTOR, "#add-stdreport-save-btn").click()
            #waiting loading
            try:
                WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"))
            except:
                pass
            # 4 - ok click
            element = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.1)
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#toast-container > div > div.toast-message").text == "Report Code Already Exist.")
            except:
                testResult = 'failed'
                Result_msg+="#4 "

            # 8 - input (z)
            driver.find_element(By.CSS_SELECTOR, "#add_stdreport_hotKey_chosen > a > span").click()
            time.sleep(0.3)
            driver.find_element(By.CSS_SELECTOR, "#add_stdreport_hotKey_chosen > div > div > input[type=text]").send_keys("Z")
            driver.find_element(By.CSS_SELECTOR, "#add_stdreport_hotKey_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            if driver.find_element(By.CSS_SELECTOR,"#add_stdreport_hotKey_chosen > a > span").text=='z':
                testResult = 'failed'
                Result_msg+="#8 "

            # 11 - Close
            # close and text check
            element = driver.find_element(By.CSS_SELECTOR, "#add-stdreport-close-btn")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.1)
            if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "Are you sure to close?":
                testResult = 'failed'
                Result_msg+="#11 "
            
            # cancel
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#add-stdreport-creator").get_property("value")==worklist_id)
            except:
                testResult = 'failed'
                Result_msg+="#11 "
            
            # ok
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add-stdreport-close-btn")))
            driver.find_element(By.CSS_SELECTOR, "#add-stdreport-close-btn").click()
            time.sleep(0.1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 탭 전환
            driver.switch_to.window(driver.window_handles[0])

        ## Report_Add 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2870, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2870, testPlanID, buildName, 'p', "Report_Add Test Passed")

    def Report_Modify():
        testResult=""
        Result_msg = "failed at "

        # 정상적인 계정으로 로그인
        signInOut.normal_login()
        
        # waiting loading
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Setting 접속
        element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-setting > i")
        driver.execute_script("arguments[0].click();", element)

        # waiting loading
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting_user_profile"))) 
        except:
            testResult = 'failed'
            Result_msg+="#0 "

        # 캡처 초기화
            del driver.requests

        # Clear
        driver.find_element(By.CSS_SELECTOR, "#stdreport_search_clear_btn > span").click()
        # waiting loading
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting_user_profile"))) 

        # rnd_rp_code 순서 확인
        request = driver.wait_for_request('.*/GetStandardReportForTable.*')
        body = request.response.body.decode('utf-8')
        data = (json.loads(body))["data"]
        rnd_num = 0
        for n in data:
            rnd_num+=1
            if(n['StdReportCode']=="rnd_rp_code"):
                break

        # 2 - 준비
        if rnd_num == 1:
            exist_report_code = driver.find_element(By.CSS_SELECTOR, "#stdreport-hotkey-list > tbody > tr:nth-child("+str(rnd_num+1)+") > td.align-center.modify-stdreport > a").text
        else:
            exist_report_code = driver.find_element(By.CSS_SELECTOR, "#stdreport-hotkey-list > tbody > tr:nth-child("+str(rnd_num-1)+") > td.align-center.modify-stdreport > a").text

        # Report Code Click #1
        driver.find_element(By.CSS_SELECTOR, "#stdreport-hotkey-list > tbody > tr:nth-child("+str(rnd_num)+") > td.align-center.modify-stdreport > a").click()
        # waiting loading
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modify-stdreport-save-btn")))
        try:
            assert(driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-view-label").text == "Modify Standard Report")
        except:
            testResult = 'failed'
            Result_msg+="#1 "

        
        if testResult == '':
            # already existed report code #4
            # modify report code
            driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-code").clear()
            driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-code").send_keys(exist_report_code)
            # Save Click
            driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-save-btn").click()
            # waiting loading
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button")))
            # message check
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text == "Are you sure to modify report?")
            except:
                testResult = 'failed'
                Result_msg+="#4 "
            # no
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-view-label").text == "Modify Standard Report")
            except:
                testResult = 'failed'
                Result_msg+="#4 "
            # Save Click
            driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-save-btn").click()
            # waiting loading
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button")))
            # Yes
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            # waiting loading
            time.sleep(0.5)
            # message check
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text == "This report code is already used.")
            except:
                testResult = 'failed'
                Result_msg+="#4 "
            # ok
            element = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")
            driver.execute_script("arguments[0].click();", element)
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modify-stdreport-save-btn")))

            # Group code, Report Code, Description, Hot Key, Report, Conclusion  #2 & 5 & 6 & 7 & 8 & 9
            # re-write
            driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-group").send_keys("2")
            element = driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-code")
            element.clear()
            element.send_keys("rnd_rp_code2")
            driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-desc").send_keys("2")
            element = driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-hotKey")
            element.click()
            element.send_keys(Keys.UP)
            element.send_keys(Keys.ENTER)
            element = driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-view-report-text")
            element.clear()
            element.send_keys("w2@")
            element = driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-view-conclusion")
            element.clear()
            element.send_keys("w2@")
            # Save Click
            driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-save-btn").click()
            # waiting loading
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button")))
            # Yes
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            # waiting loading
            time.sleep(0.5)
            # message check
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.visible.showSweetAlert > h2").text == "You have modified standard report.")
            except:
                testResult = 'failed'
                Result_msg+="#2 #5 #6 #7 #8 #9 "
            # Ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.5)

            # close #10
            driver.find_element(By.CSS_SELECTOR, "#stdreport-hotkey-list > tbody > tr:nth-child("+str(rnd_num)+") > td.align-center.modify-stdreport > a").click()
            # waiting loading
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modify-stdreport-save-btn")))
            # close
            driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-close-btn").click()
            # waiting loading
            time.sleep(0.25)
            # message check
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text == "Are you sure to close?")
            except:
                testResult = 'failed'
                Result_msg+="#10 "
            # no
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            # waiting loading
            time.sleep(0.25)
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-view-label").text == "Modify Standard Report")
            except:
                testResult = 'failed'
                Result_msg+="#10 "
            # close
            driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-close-btn").click()
            # waiting loading
            time.sleep(0.25)
            # yes
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.25)
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#setting_stdreport_searching_card > div.header > h4").text == "Search Filter")
            except:
                testResult = 'failed'
                Result_msg+="#10 "

        ## Report_Modify 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2416, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2416, testPlanID, buildName, 'p', "Report_Modify Test Passed")

    def Report_delete():
        testResult=""
        Result_msg = "failed at "

        # 정상적인 계정으로 로그인
        signInOut.normal_login()
        
        # waiting loading
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Setting 접속
        element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-setting > i")
        driver.execute_script("arguments[0].click();", element)

        # waiting loading
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting_user_profile"))) 
        except:
            testResult = 'failed'
            Result_msg+="#0 "

        # 캡처 초기화
            del driver.requests

        # Clear
        driver.find_element(By.CSS_SELECTOR, "#stdreport_search_clear_btn > span").click()
        # waiting loading
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting_user_profile"))) 

        # rnd_rp_code 순서 확인
        request = driver.wait_for_request('.*/GetStandardReportForTable.*')
        body = request.response.body.decode('utf-8')
        data = (json.loads(body))["data"]
        rnd_num = 0
        for n in data:
            rnd_num+=1
            if(n['StdReportCode']=="rnd_rp_code2"):
                break

        # Report Code select #1
        # slot
        driver.find_element(By.CSS_SELECTOR, "#stdreport-hotkey-list > tbody > tr:nth-child("+str(rnd_num)+") > td:nth-child(1) > label").click()
        # delete
        driver.find_element(By.CSS_SELECTOR, "#stdreport_delete_btn > span").click()
        # waiting loading
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"))) 
        # message check
        try:
            assert(driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text == "Are you sure to delete selected standard report?")
        except:
            testResult = 'failed'
            Result_msg+="#1 "
        # cancel
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        time.sleep(0.25)
        try:
            assert(driver.find_element(By.CSS_SELECTOR, "#setting_stdreport_searching_card > div.header > h4").text == "Search Filter")
        except:
            testResult = 'failed'
            Result_msg+="#1 "
        # delete
        driver.find_element(By.CSS_SELECTOR, "#stdreport_delete_btn > span").click()
        # waiting loading
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"))) 
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.25)
        # delete check
        if driver.find_element(By.CSS_SELECTOR, "#stdreport-hotkey-list > tbody > tr:nth-child("+str(rnd_num)+") > td.align-center.modify-stdreport > a").text == "rnd_rp_code2":
            testResult = 'failed'
            Result_msg+="#1 "

        ## Report_delete 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2428, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2428, testPlanID, buildName, 'p', "Report_delete Test Passed")

    def Profile_Worklist_inUserProfile():
        # Setting 접속
        element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-setting > i")
        driver.execute_script("arguments[0].click();", element)

        # waiting loading
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting_user_profile"))) 

        # User profile 접속
        driver.find_element(By.CSS_SELECTOR, "#setting_user_profile").click()
        # waiting loading
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting_confirm_btn")))
            
    def Profile_Worklist():
        testResult=""
        Result_msg = "failed at "

        # 정상적인 계정으로 로그인
        signInOut.normal_login()
        
        # waiting loading
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Setting + User profile + waiting접속
        TOPMENU.Profile_Worklist_inUserProfile()

        # Job Date #1
        driver.find_element(By.CSS_SELECTOR, "#worklist_setting_sort_select").click()
        driver.find_element(By.CSS_SELECTOR, "#worklist_setting_sort_select_option_job_dttm").click()
        # save
        driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.5)
        # 캡처 초기화
        del driver.requests
        # refresh
        driver.find_element(By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title")))
        # get order info
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        url = (request.url).split('&')
        order_col = url[2].split('=')[1]
        #order_type = url[3].split('=')[1]
        try:
            assert(order_col=='JobDateDTTMString')
        except:
            testResult = 'failed'
            Result_msg+="#1 "

        # Setting + User profile + waiting접속
        TOPMENU.Profile_Worklist_inUserProfile()

        # Study Date #2
        driver.find_element(By.CSS_SELECTOR, "#worklist_setting_sort_select").click()
        driver.find_element(By.CSS_SELECTOR, "#worklist_setting_sort_select_option_study_dttm").click()
        # save
        driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.5)
        # 캡처 초기화
        del driver.requests
        # refresh
        driver.find_element(By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title")))
        # get order info
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        url = (request.url).split('&')
        order_col = url[2].split('=')[1]
        #order_type = url[3].split('=')[1]
        try:
            assert(order_col=='StudyDateDTTMString')
        except:
            testResult = 'failed'
            Result_msg+="#2 "

         # Setting + User profile + waiting접속
        TOPMENU.Profile_Worklist_inUserProfile()

        # Uploaded Date #3
        driver.find_element(By.CSS_SELECTOR, "#worklist_setting_sort_select").click()
        driver.find_element(By.CSS_SELECTOR, "#worklist_setting_sort_select_option_upload_dttm").click()
        # save
        driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.5)
        # 캡처 초기화
        del driver.requests
        # refresh
        driver.find_element(By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title")))
        # get order info
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        url = (request.url).split('&')
        order_col = url[2].split('=')[1]
        #order_type = url[3].split('=')[1]
        try:
            assert(order_col=='UploadedDTTMString')
        except:
            testResult = 'failed'
            Result_msg+="#3 "

        # Setting + User profile + waiting접속
        TOPMENU.Profile_Worklist_inUserProfile()

        # ASC #4
        driver.find_element(By.CSS_SELECTOR, "#worklist_setting_sort_select").click()
        driver.find_element(By.CSS_SELECTOR, "#worklist_setting_sort_select_option_job_dttm").click()
        driver.find_element(By.CSS_SELECTOR, "#worklist_profile_row > div > div > div > div > div:nth-child(3) > div > span > label:nth-child(2)").click()
        # save
        driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.5)
        # 캡처 초기화
        del driver.requests
        # refresh
        driver.find_element(By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title")))
        # get order info
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        url = (request.url).split('&')
        #order_col = url[2].split('=')[1]
        order_type = url[3].split('=')[1]
        try:
            assert(order_type=='asc')
        except:
            testResult = 'failed'
            Result_msg+="#4 "

        # Setting + User profile + waiting접속
        TOPMENU.Profile_Worklist_inUserProfile()

        # DESC #5
        driver.find_element(By.CSS_SELECTOR, "#worklist_setting_sort_select").click()
        driver.find_element(By.CSS_SELECTOR, "#worklist_setting_sort_select_option_job_dttm").click()
        driver.find_element(By.CSS_SELECTOR, "#worklist_profile_row > div > div > div > div > div:nth-child(3) > div > span > label:nth-child(4)").click()
        # save
        driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.5)
        # 캡처 초기화
        del driver.requests
        # refresh
        driver.find_element(By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title")))
        # get order info
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        url = (request.url).split('&')
        #order_col = url[2].split('=')[1]
        order_type = url[3].split('=')[1]
        try:
            assert(order_type=='desc')
        except:
            testResult = 'failed'
            Result_msg+="#5 "

        # Setting + User profile + waiting접속
        TOPMENU.Profile_Worklist_inUserProfile()

        # AI off #6
        #value_of_css_property("background-color")
        # off - rgba(129, 129, 129, 1)
        # on - rgba(255, 87, 34, 0.5)
        # if on > change off
        if driver.find_element(By.CSS_SELECTOR, "#ai_setting_section > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span").value_of_css_property("background-color") == "rgba(255, 87, 34, 0.5)":
            element = driver.find_element(By.CSS_SELECTOR, "#ai_setting_section > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span")
            driver.execute_script("arguments[0].click();", element)
            # save
            driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.5)
        # 캡처 초기화
        del driver.requests
        # refresh
        driver.find_element(By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title")))
        time.sleep(3)##
        # get AI on/off info
        request = driver.wait_for_request('.*/GetAIInformationShowUserProfile')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        try:
            assert(data=='F')
        except:
            testResult = 'failed'
            Result_msg+="#6 "

        # Setting + User profile + waiting접속
        TOPMENU.Profile_Worklist_inUserProfile()

        # AI on #7
        # if off > change on
        if driver.find_element(By.CSS_SELECTOR, "#ai_setting_section > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span").value_of_css_property("background-color") == "rgba(129, 129, 129, 1)":
            element = driver.find_element(By.CSS_SELECTOR, "#ai_setting_section > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span")
            driver.execute_script("arguments[0].click();", element)
            # save
            driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        # 캡처 초기화
        del driver.requests
        # refresh
        driver.find_element(By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title")))
        # get AI on/off info
        request = driver.wait_for_request('.*/GetAIInformationShowUserProfile')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        try:
            assert(data=='T')
        except:
            testResult = 'failed'
            Result_msg+="#7 "

        # Setting + User profile + waiting접속
        TOPMENU.Profile_Worklist_inUserProfile()

        # font #8
        # intialize
        driver.find_element(By.CSS_SELECTOR, "#worklist-font-type-select").click()
        driver.find_element(By.CSS_SELECTOR, "#worklist-font-type-select > option:nth-child(1)").click()
        # save
        driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.5)

        # 캡처 초기화
        del driver.requests

        # Comic Sans MS
        driver.find_element(By.CSS_SELECTOR, "#worklist-font-type-select").click()
        driver.find_element(By.CSS_SELECTOR, "#worklist-font-type-select > option:nth-child(8)").click()
        # save
        driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.5)

        request = driver.wait_for_request('.*/GetWorklistFontType')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        try:
            assert(data == " Comic Sans MS")
        except:
            testResult = 'failed'
            Result_msg+="#8 "

        # intialize
        driver.find_element(By.CSS_SELECTOR, "#worklist-font-type-select").click()
        driver.find_element(By.CSS_SELECTOR, "#worklist-font-type-select > option:nth-child(1)").click()
        # save
        driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.5)

        ## Profile_Worklist 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2431, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2431, testPlanID, buildName, 'p', "Profile_Worklist Test Passed")

    def Profile_Standard_Report():
        testResult=""
        Result_msg = "failed at "

        # 정상적인 계정으로 로그인
        signInOut.normal_login()
        
        # waiting loading
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Setting + User profile + waiting접속
        TOPMENU.Profile_Worklist_inUserProfile()

        # standard report
        driver.find_element(By.CSS_SELECTOR, "#standard_report_setting_tab_link > a").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard_report_profile_row > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span")))

        #value_of_css_property("background-color")
        # off - rgba(129, 129, 129, 1) / on - rgba(255, 87, 34, 0.5)
        # Auto Expand off #1
        # if on > off
        if driver.find_element(By.CSS_SELECTOR, "#standard_report_profile_row > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span").value_of_css_property("background-color") == "rgba(255, 87, 34, 0.5)":
            element = driver.find_element(By.CSS_SELECTOR, "#standard_report_profile_row > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span")
            driver.execute_script("arguments[0].click();", element)
            # save
            driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.5)
        # Home
        driver.find_element(By.CSS_SELECTOR, "#right-sidebar-home").click()
        time.sleep(0.25)
        # CT Search
        driver.find_element(By.CSS_SELECTOR, "#search-job-modality").send_keys("CT")
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        # 캡처 초기화
        del driver.requests
        time.sleep(0.25)
        # in report
        driver.find_element(By.CSS_SELECTOR, "#job-report").click()  
        # 탭 전환
        time.sleep(2.5)
        driver.switch_to.window(driver.window_handles[1])
        # AutoExpand check through packet
        request = driver.wait_for_request('.*/GetStdReportExFolderAutoExpand.*'+'CT')
        body = request.response.body.decode('utf-8')
        data = (json.loads(body))
        if 'NOT_USE_AUTO_EXPAND' != data:
            testResult = 'failed'
            Result_msg+="#1 "
        #탭 전환
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Setting + User profile + waiting접속
        TOPMENU.Profile_Worklist_inUserProfile()

        # standard report
        driver.find_element(By.CSS_SELECTOR, "#standard_report_setting_tab_link > a").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard_report_profile_row > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span")))

        #value_of_css_property("background-color")
        # off - rgba(129, 129, 129, 1) / on - rgba(255, 87, 34, 0.5)
        # Auto Expand off #1
        # if off > on
        if driver.find_element(By.CSS_SELECTOR, "#standard_report_profile_row > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span").value_of_css_property("background-color") == "rgba(129, 129, 129, 1)":
            element = driver.find_element(By.CSS_SELECTOR, "#standard_report_profile_row > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span")
            driver.execute_script("arguments[0].click();", element)
            # save
            driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.5)
        # Home
        driver.find_element(By.CSS_SELECTOR, "#right-sidebar-home").click()
        time.sleep(0.25)
        # CT Search
        #driver.find_element(By.CSS_SELECTOR, "#search-job-modality").send_keys("CT")
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        # 캡처 초기화
        del driver.requests
        time.sleep(0.25)
        # in report
        driver.find_element(By.CSS_SELECTOR, "#job-report").click()  
        try:
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        except:
            pass
        # 탭 전환
        time.sleep(2.5)
        driver.switch_to.window(driver.window_handles[1])
        # AutoExpand check through packet
        request = driver.wait_for_request('.*/GetStdReportExFolderAutoExpand.*'+'CT')
        body = request.response.body.decode('utf-8')
        data = (json.loads(body))
        if 'NOT_USE_AUTO_EXPAND' == data:
            testResult = 'failed'
            Result_msg+="#2 "
        #탭 전환
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        ## Profile_Standard_Report 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2444, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2444, testPlanID, buildName, 'p', "Profile_Standard_Report Test Passed")

    #def Statistics_Hospital_SearchFilter():
    #    testResult=""
    #    Result_msg = "failed at "

    #    # 정상적인 계정으로 로그인
    #    signInOut.normal_login()
        
    #    # waiting loading
    #    try:
    #        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
    #    except:
    #        pass

    #    # Statistics 접속
    #    driver.find_element(By.CSS_SELECTOR, "#right-sidebar-statistics").click()
    #    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#statistics-search > span")))

    #    print(Result_msg)

class WORKLIST:
    def HospitalList():
        testResult=""
        Result_msg = "failed at "

        # 정상적인 계정으로 로그인
        signInOut.normal_login()
        
        # waiting loading
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Dropbox & View All Hospital List #1 & 4
        # Admin에서 정보 획득 시작
        # 새로운 탭 + 전환
        driver.execute_script("window.open()")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(AdminUrl);

        # admin 사이트 로그인
        driver.find_element(By.ID, 'user-id').clear()
        driver.find_element(By.ID, 'user-id').send_keys(admin_id)
        driver.find_element(By.ID, 'user-password').clear()
        driver.find_element(By.ID, 'user-password').send_keys(admin_pw)
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)

        # Configuration
        element = driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[2]/div[1]/ul/li[5]/a')
        driver.execute_script("arguments[0].click();", element)
        driver.implicitly_wait(5)

        # Download Control
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn > span").click()
        WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#tab-downloadControl-byUser-list > a")))
        # 캡처 초기화
        del driver.requests
        # id search & get info
        driver.find_element(By.CSS_SELECTOR, "#download-search-user-id").send_keys(worklist_id)
        driver.find_element(By.CSS_SELECTOR, "#download-search").click()
        request = driver.wait_for_request('.*/DownloadControl/GetDownloadControlByInstList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        adm_hospital_list = []
        for n in data:
            if worklist_id in n["UserName"]:
                adm_hospital_list.append(n["InstitutionName"])

        #탭 전환
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        # admin 정보 획득 종료

        # worklist 정보 획득
        # View All Hospital List
        element = driver.find_element(By.CSS_SELECTOR, "#all-institution-list")
        if element.is_selected() == False:
            driver.execute_script("arguments[0].click();", element)
            del driver.requests
        request = driver.wait_for_request('.*/GetHospitalList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)['HospitalList']
        wk_hospital_list= []
        for n in data:
            wk_hospital_list.append(n["InstitutionName"])

        adm_hospital_list.sort()
        wk_hospital_list.sort()
        try:
            assert(adm_hospital_list == wk_hospital_list)
        except:
            testResult = 'failed'
            Result_msg+="#1 #4 "

        # Drppbox / list & 응급/Refer/Auto Refer #2 & 5 & 3
        # View All hospital list off
        if element.is_selected() == True:
            del driver.requests
            driver.execute_script("arguments[0].click();", element)
            request = driver.wait_for_request('.*/GetHospitalList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)['HospitalList']

        # 2 & 5 - click 할 hospital 결정
        least_num = int(data[0]['AutoReferCount'])
        for n in range(0, len(data)):
            if least_num >= data[n]['AutoReferCount']:
                least_num = data[n]['AutoReferCount']
                click_hospital_num = n
        click_hospital = data[click_hospital_num]['InstitutionName']

        ## 3 - 응급/Refer/Auto Refer from pk
        #pk_emergency = []
        #pk_refer = []
        #pk_auto_refer = []
        #for n in data:
        #    pk_emergency.append(n["PriorityCount"])
        #    pk_refer.append(n["ReferCount"])
        #    pk_auto_refer.append(n["AutoReferCount"])

        # 3 - 응급/Refer/Auto Refer from page
        emergency_lbadge = []
        refer_lbadge = []
        auto_refer_lbadge = []
        for n in range(1,len(data)+1):
            emergency_lbadge.append(int(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[1]/div[1]/div[1]/div[3]/div[2]/button["+str(n)+"]/span[3]").text))
            refer_lbadge.append(int(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[1]/div[1]/div[1]/div[3]/div[2]/button["+str(n)+"]/span[2]").text))
            auto_refer_lbadge.append(int(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[1]/div[1]/div[1]/div[3]/div[2]/button["+str(n)+"]/span[1]").text))

        emergency_wk = []
        refer_wk = []
        auto_refer_wk = []
        for n in range(1,len(data)+1):
            del driver.requests
            driver.find_element(By.CSS_SELECTOR, "#hospital_list > button:nth-child("+str(n)+")").click()
            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            page_len = int(data['Length'])
            # total page
            total = math.ceil(int(data['recordsFiltered']) / page_len)
            # remain
            last_page_num = int(data['recordsFiltered']) % page_len
            emergency = 0
            refer = 0
            auto_refer = 0
            if last_page_num == 0:
                for a in range(1, total+1):
                    for b in range(1, page_len+1):
                        ##
                        if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(b)+") > td.current-job.align-center.current-job-column-1").get_property("childElementCount") != 0:
                            emergency += 1
                        if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child(2) > td.refer-tooltip.current-job.align-center.current-list-tooltip.current-job-column-2 > span > label").text == 'R':
                            refer = 1
                        auto_refer+=1
                    element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(0.3)
            else:
                for a in range(1, total+1):
                    if a == total:
                        for b in range(1, last_page_num+1):
                            ##
                            if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(b)+") > td.current-job.align-center.current-job-column-1").get_property("childElementCount") != 0:
                                emergency += 1
                            if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child(2) > td.refer-tooltip.current-job.align-center.current-list-tooltip.current-job-column-2 > span > label").text == 'R':
                                refer = 1
                            auto_refer+=1
                        break
                    for b in range(1, page_len+1):
                        ##
                        if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(b)+") > td.current-job.align-center.current-job-column-1").get_property("childElementCount") != 0:
                            emergency += 1
                        if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child(2) > td.refer-tooltip.current-job.align-center.current-list-tooltip.current-job-column-2 > span > label").text == 'R':
                            refer = 1
                        auto_refer+=1
                    element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(0.3)
            emergency_wk.append(emergency)
            refer_wk.append(refer)
            auto_refer_wk.append(auto_refer)
        try:
            assert(emergency_lbadge == emergency_wk and
                   refer_lbadge == refer_wk and
                   auto_refer_lbadge == auto_refer_wk)
        except:
            testResult = 'failed'
            Result_msg+="#3 "
            
        ## 3 - 비교
        #try:
        #    assert(pk_emergency == emergency and
        #           pk_refer == refer and
        #           pk_auto_refer == auto_refer)
        #except:
        #    testResult = 'failed'
        #    Result_msg+="#3 "
        
        # 2 & 5 - check hospital option
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting-columns-apply")))
        if(driver.find_element(By.CSS_SELECTOR, "#chk-column-13").is_selected()==False):
            element = driver.find_element(By.CSS_SELECTOR, "#chk-column-13")
            driver.execute_script("arguments[0].click();", element)
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()
        time.sleep(0.3)

        # 2 - page 넘기며 확인
        del driver.requests
        # least dropbox click
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > div > div > input[type=text]").send_keys(click_hospital)
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        time.sleep(0.3)
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        page_len = int(data['Length'])
        # total page
        total = math.ceil(int(data['recordsFiltered']) / page_len)
        # remain
        last_page_num = int(data['recordsFiltered']) % page_len
        if last_page_num == 0:
            for a in range(1, total+1):
                for b in range(1, page_len+1):
                    if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(b)+") > td.current-job.align-center.current-job-column-13").text != click_hospital:
                        testResult = 'failed'
                        Result_msg+="#2 "
                        break
                if(testResult != '' or a == total):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        else:
            for a in range(1, total+1):
                if a == total:
                    for b in range(1, last_page_num+1):
                        if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(b)+") > td.current-job.align-center.current-job-column-13").text != click_hospital:
                            testResult = 'failed'
                            Result_msg+="#2 "
                            break
                if a == total:
                    break
                for b in range(1, page_len+1):
                    if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(b)+") > td.current-job.align-center.current-job-column-13").text != click_hospital:
                        testResult = 'failed'
                        Result_msg+="#2 "
                        break
                if(testResult != ''):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)

        # 5 - page 넘기며 확인
        del driver.requests
        # least list click
        element = driver.find_element(By.CSS_SELECTOR, "#hospital_list > button:nth-child("+str(click_hospital_num+1)+")")
        driver.execute_script("arguments[0].click();", element)
        time.sleep(0.3)
        total_list_index = int(((driver.find_element(By.CSS_SELECTOR, "#current-job-list_info").text).split(' '))[5])
        total_list = 0
        if last_page_num == 0:
            for a in range(1, total+1):
                for b in range(1, page_len+1):
                    total_list+=1
                    if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(b)+") > td.current-job.align-center.current-job-column-13").text != click_hospital:
                        testResult = 'failed'
                        Result_msg+="#5 "
                        break
                if(testResult != '' or a == total):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        else:
            for a in range(1, total+1):
                if a == total:
                    for b in range(1, last_page_num+1):
                        total_list+=1
                        if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(b)+") > td.current-job.align-center.current-job-column-13").text != click_hospital:
                            testResult = 'failed'
                            Result_msg+="#5 "
                            break
                if a == total:
                    break
                for b in range(1, page_len+1):
                    total_list+=1
                    if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(b)+") > td.current-job.align-center.current-job-column-13").text != click_hospital:
                        testResult = 'failed'
                        Result_msg+="#5 "
                        break
                if(testResult != ''):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        try:
            assert(total_list_index == total_list)
        except:
            testResult = 'failed'
            Result_msg+="#5 "

        # < / > #6 & 7
        driver.find_element(By.CSS_SELECTOR, "#hospital_list_hide_btn > span").click()
        # find >
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#hospital_list_show_btn > span")))
            driver.find_element(By.CSS_SELECTOR, "#hospital_list_show_btn > span").click()
            # find < 
            try:
                WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#hospital_list_hide_btn > span")))
            except:
                testResult = 'failed'
                Result_msg+="#7 "
        except:
            testResult = 'failed'
            Result_msg+="#6 "

        ## HospitalList 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2506, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2506, testPlanID, buildName, 'p', "HospitalList Test Passed")

    def SearchFilter_JobStatus_Search(job_status_position, target, num):
        testResult = ''
        Result_msg = ''
        time.sleep(0.3)
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        page_len = int(data['Length'])
        # total page
        total = math.ceil(int(data['recordsFiltered']) / page_len)
        # remain
        last_page_num = int(data['recordsFiltered']) % page_len
        if last_page_num == 0:
            for a in range(1, total+1):
                for b in range(1, page_len+1):
                    if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(job_status_position)+"]/span/label").text != target:
                        testResult = 'failed'
                        Result_msg+="#"+num+" "
                        break
                if(testResult != '' or a == total):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        else:
            for a in range(1, total+1):
                if a == total:
                    for b in range(1, last_page_num+1):
                        if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(job_status_position)+"]/span/label").text != target:
                            testResult = 'failed'
                            Result_msg+="#"+num+" "
                            break
                if a == total:
                    break
                for b in range(1, page_len+1):
                    if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(job_status_position)+"]/span/label").text != target:
                        testResult = 'failed'
                        Result_msg+="#"+num+" "
                        break
                if(testResult != ''):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        return Result_msg

    def SearchFilter_JobStatus():
        testResult=""
        Result_msg = "failed at "

        # 정상적인 계정으로 로그인
        signInOut.normal_login()
        
        # waiting loading
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # filter hide check
        if driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").value_of_css_property("transform") != "matrix(6.12323e-17, 1, -1, 6.12323e-17, 0, 0)":
            driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").click()

        # option job status
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(4) > label")))
        # check job status
        if driver.find_element(By.CSS_SELECTOR, "#chk-column-4").is_selected() == False:
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(4) > label").click()
        # showing wk column num
        show_list_num = 1
        for n in range (1,33):
            if driver.find_element(By.CSS_SELECTOR, "#chk-column-"+str(n)).is_selected() == True:
                show_list_num += 1
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()
        time.sleep(0.5)
        # find job status position
        for n in range (2,show_list_num+1):
            if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[1]/div/table/thead/tr/th["+str(n)+"]").text == "Job Status":
                job_status_position = n
                break

        
        # 캡처 초기화
        del driver.requests

        # Requested #2
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li.active-result.result-selected.highlighted").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"Requested", "2")

        # 캡처 초기화
        del driver.requests

        # Reported #3
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(2)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"Reported", "3")

        # 캡처 초기화
        del driver.requests

        # Pending #4
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(3)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"Pending", "4")

        # 캡처 초기화
        del driver.requests

        # Completed #5 
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(4)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"Completed", "5")

        # 캡처 초기화
        del driver.requests

        # Recalled #6
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(5)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"Recalled", "6")

        # 캡처 초기화
        del driver.requests

        # Canceled #7
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(6)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"Canceled", "7")

        # 캡처 초기화
        del driver.requests

        # Canceled2 #8
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(7)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"Canceled2", "8")

        # 캡처 초기화
        del driver.requests

        # AI Processing #9
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(8)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        time.sleep(0.3)
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        page_len = int(data['Length'])
        # total page
        total = math.ceil(int(data['recordsFiltered']) / page_len)
        # remain
        last_page_num = int(data['recordsFiltered']) % page_len
        if last_page_num == 0:
            for a in range(1, total+1):
                for b in range(1, page_len+1):
                    if  "AI" not in driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(job_status_position)+"]/span/label").text:
                        testResult = 'failed'
                        Result_msg+="#9 "
                        break
                if(testResult != '' or a == total):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        else:
            for a in range(1, total+1):
                if a == total:
                    for b in range(1, last_page_num+1):
                        if "AI" not in driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(job_status_position)+"]/span/label").text:
                            testResult = 'failed'
                            Result_msg+="#9 "
                            break
                if a == total:
                    break
                for b in range(1, page_len+1):
                    if "AI" not in driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(job_status_position)+"]/span/label").text:
                        testResult = 'failed'
                        Result_msg+="#9 "
                        break
                if(testResult != ''):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)

        # DiscardRequested #10
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(9").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"DiscardRequested", "10")

        # 캡처 초기화
        del driver.requests

        # DiscardCompleted #11
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(10)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"DiscardCompleted", "11")
        
        ## SearchFilter_JobStatus 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2582, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2582, testPlanID, buildName, 'p', "SearchFilter_JobStatus Test Passed")

    def SearchFilter_JobDate():
        testResult=""
        Result_msg = "failed at "

        # 정상적인 계정으로 로그인
        signInOut.normal_login()
        
        # waiting loading
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # filter hide check
        if driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").value_of_css_property("transform") != "matrix(6.12323e-17, 1, -1, 6.12323e-17, 0, 0)":
            driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").click()

        today = (datetime.today()).strftime('%Y-%m-%d')

        # Job Start/End Date Click #1
        driver.find_element(By.CSS_SELECTOR, "#search-job-start-date").click()
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
        except:
            testResult = "failed"
            Reesult_msg += "#1 "

        driver.find_element(By.CSS_SELECTOR, "#search-job-end-date").click()
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
        except:
            testResult = "failed"
            Reesult_msg += "#1 "

        today_position = []
        if testResult == "":
            # 임의의 날짜 선택(today) #2
            # start
            driver.find_element(By.CSS_SELECTOR, "#search-job-start-date").click()
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
            for a in range(1, 7):
                for b in range(1, 8):
                    element = driver.find_element(By.XPATH, "/html/body/div[11]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]")
                    if("today" in (element.get_property("classList"))):
                        today_position.append(a)
                        today_position.append(b)
                        element.click()
                        break
                if(a in today_position):
                    break
            time.sleep(0.25)
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#search-job-start-date").get_property('value') == str(today))
            except:
                testResult = 'failed'
                Result_msg+="#2 "
            # end
            driver.find_element(By.CSS_SELECTOR, "#search-job-end-date").click()
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
            driver.find_element(By.XPATH, "/html/body/div[11]/div[1]/table/tbody/tr["+str(today_position[0])+"]/td["+str(today_position[1])+"]").click()
            time.sleep(0.25)
            try:             
                assert(driver.find_element(By.CSS_SELECTOR, "#search-job-end-date").get_property('value') == str(today))
            except:
                testResult = 'failed'
                Result_msg+="#2 "

            # clear #3
            driver.find_element(By.CSS_SELECTOR, "#search-job-end-date").click()
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
            driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(4) > th").click()
            time.sleep(0.25)
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#search-job-start-date").get_property('value') == "" and
                       driver.find_element(By.CSS_SELECTOR, "#search-job-end-date").get_property('value') == "")
            except:
                testResult = 'failed'
                Result_msg+="#3 "

            # Yesterday, Today, Week, Month #4
            # Yesterday
            yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
            driver.find_element(By.CSS_SELECTOR, "#search-job-start-date").click()
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
            driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(1) > th:nth-child(1)").click()
            time.sleep(0.25)
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#search-job-start-date").get_property('value') == str(yesterday) and 
                       driver.find_element(By.CSS_SELECTOR, "#search-job-end-date").get_property('value') == str(today))
            except:
                testResult = 'failed'
                Result_msg+="#4_1 "
            # Today
            driver.find_element(By.CSS_SELECTOR, "#search-job-start-date").click()
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
            driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(1) > th:nth-child(2)").click()
            time.sleep(0.25)
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#search-job-start-date").get_property('value') == str(today) and 
                       driver.find_element(By.CSS_SELECTOR, "#search-job-end-date").get_property('value') == str(today))
            except:
                testResult = 'failed'
                Result_msg+="#4_2 "
            # Week            
            for n in range(2, 7):
                driver.find_element(By.CSS_SELECTOR, "#search-job-start-date").click()
                WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
                driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(2) > th:nth-child("+str(n)+")").click()
                time.sleep(0.25)
                try:
                    assert(driver.find_element(By.CSS_SELECTOR, "#search-job-start-date").get_property('value') == str((datetime.today() - timedelta(weeks=(n-1))).strftime('%Y-%m-%d')) and 
                       driver.find_element(By.CSS_SELECTOR, "#search-job-end-date").get_property('value') == str(today))
                except:
                    testResult = 'failed'
                    Result_msg+="#4_3 "
                if testResult != '':
                    break
            # Month
            for n in range(2, 7):
                driver.find_element(By.CSS_SELECTOR, "#search-job-start-date").click()
                WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
                driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(3) > th:nth-child("+str(n)+")").click()
                time.sleep(0.25)
                try:
                    if(n==2):
                        assert(driver.find_element(By.CSS_SELECTOR, "#search-job-start-date").get_property('value') == str((datetime.today() - relativedelta(months=1)).strftime('%Y-%m-%d')) and 
                        driver.find_element(By.CSS_SELECTOR, "#search-job-end-date").get_property('value') == str(today))
                    else:
                        assert(driver.find_element(By.CSS_SELECTOR, "#search-job-start-date").get_property('value') == str((datetime.today() - relativedelta(months=3*(n-2))).strftime('%Y-%m-%d')) and 
                        driver.find_element(By.CSS_SELECTOR, "#search-job-end-date").get_property('value') == str(today))
                except:
                    testResult = 'failed'
                    Result_msg+="#4_4 "
                if testResult != '':
                    break

        ## SearchFilter_JobDate 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2595, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2595, testPlanID, buildName, 'p', "SearchFilter_JobDate Test Passed")
    
    # get target position in worklist and option check
    def SearchFilter_Etc_setting(target_num, target):
        # option
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(4) > label")))
        # check target
        if driver.find_element(By.CSS_SELECTOR, "#chk-column-"+target_num).is_selected() == False:
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(4) > label").click()
        # showing wk column num
        show_list_num = 1
        for n in range (1,33):
            if driver.find_element(By.CSS_SELECTOR, "#chk-column-"+str(n)).is_selected() == True:
                show_list_num += 1
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()
        time.sleep(0.5)
        # find job status position
        for n in range (2,show_list_num+1):
            if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[1]/div/table/thead/tr/th["+str(n)+"]").text == target:
                target_position = n
                break

        return target_position

    def SearchFilter_Etc_Search(target_position, target, particular):
        testResult=""

        del driver.requests

        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        time.sleep(0.3)
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        page_len = int(data['Length'])
        # total page
        total = math.ceil(int(data['recordsFiltered']) / page_len)
        # remain
        last_page_num = int(data['recordsFiltered']) % page_len

        # if gender
        if particular == "Gender":
            if last_page_num == 0:
                for a in range(1, total+1):
                    for b in range(1, page_len+1):
                        if target not in driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(target_position)+"]").text:
                            testResult = 'failed'
                            break
                    if(testResult != '' or a == total):
                        break
                    element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(0.3)
            else:
                for a in range(1, total+1):
                    if a == total:
                        for b in range(1, last_page_num+1):
                            if target not in driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(target_position)+"]").text:
                                testResult = 'failed'
                                break
                    if a == total:
                        break
                    for b in range(1, page_len+1):
                        if target not in driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(target_position)+"]").text:
                            testResult = 'failed'
                            break
                    if(testResult != ''):
                        break
                    element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(0.3)
            # Clear
            driver.find_element(By.CSS_SELECTOR, "#clear_searchfilter > span").click()
            return testResult

        # if PatientName
        if "PatientName" in particular:
            # 비식별화 Name 획득
            temp = particular.split("&")[1:]
            mask = ""
            for n in temp:
                mask += n

            if last_page_num == 0:
                for a in range(1, total+1):
                    for b in range(1, page_len+1):
                        if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(target_position)+"]").text != mask:
                            testResult = 'failed'
                            break
                    if(testResult != '' or a == total):
                        break
                    element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(0.3)
            else:
                for a in range(1, total+1):
                    if a == total:
                        for b in range(1, last_page_num+1):
                            if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(target_position)+"]").text != mask:
                                testResult = 'failed'
                                break
                    if a == total:
                        break
                    for b in range(1, page_len+1):
                        if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(target_position)+"]").text != mask:
                            testResult = 'failed'
                            break
                    if(testResult != ''):
                        break
                    element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(0.3)
            # Clear
            driver.find_element(By.CSS_SELECTOR, "#clear_searchfilter > span").click()
            return testResult

        # not particular
        if last_page_num == 0:
            for a in range(1, total+1):
                for b in range(1, page_len+1):
                    if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(target_position)+"]").text != target:
                        testResult = 'failed'
                        break
                if(testResult != '' or a == total):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        else:
            for a in range(1, total+1):
                if a == total:
                    for b in range(1, last_page_num+1):
                        if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(target_position)+"]").text != target:
                            testResult = 'failed'
                            break
                if a == total:
                    break
                for b in range(1, page_len+1):
                    if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(target_position)+"]").text != target:
                        testResult = 'failed'
                        break
                if(testResult != ''):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        
        # Clear
        driver.find_element(By.CSS_SELECTOR, "#clear_searchfilter > span").click()
        return testResult


    # Department ~ Split Bar simple filter
    def SearchFilter_Etc():
        # 정상적인 계정으로 로그인
        signInOut.normal_login()
        
        # waiting loading
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # filter hide check
        if driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").value_of_css_property("transform") != "matrix(6.12323e-17, 1, -1, 6.12323e-17, 0, 0)":
            driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").click()

        # data setting
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)['data']

        ## Department
        #testResult=""
        #Result_msg = "failed at "
        #particular = ""
        #wk_index_num = WORKLIST.SearchFilter_Etc_setting("19","Department")
        #choice = ""
        #for n in data:
        #    if n["Department"] != None:
        #        choice = n["Department"]
        #        break
        #driver.find_element(By.CSS_SELECTOR, "#search-job-dept").send_keys(choice)
        #if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
        #    testResult="failed"
        #    Result_msg += "#1 "
        ### SearchFilter_Department 결과 전송
        ##if testResult == 'failed':
        ##    testlink.reportTCResult(2605, testPlanID, buildName, 'f', Result_msg)            
        ##else:
        ##    testlink.reportTCResult(2605, testPlanID, buildName, 'p', "SearchFilter_Department Test Passed")

        ## Modality ##
        #testResult=""
        #Result_msg = "failed at "
        #particular = ""
        #wk_index_num = WORKLIST.SearchFilter_Etc_setting("9","Mod") ##
        #choice = ""
        #for n in data:
        #    if n["Modality"] != None: ##
        #        choice = n["Modality"] ##
        #        break
        #driver.find_element(By.CSS_SELECTOR, "#search-job-modality").send_keys(choice)
        #if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
        #    testResult="failed"
        #    Result_msg += "#1 "
        ### SearchFilter_Modality 결과 전송 ##
        ##if testResult == 'failed':
        ##    testlink.reportTCResult(2608, testPlanID, buildName, 'f', Result_msg)            
        ##else:
        ##    testlink.reportTCResult(2608, testPlanID, buildName, 'p', "SearchFilter_Modality Test Passed")

        ## Bodypart ##
        #testResult=""
        #Result_msg = "failed at "
        #particular = ""
        #wk_index_num = WORKLIST.SearchFilter_Etc_setting("16","Bodypart") ##
        #choice = ""
        #for n in data:
        #    if n["Bodypart"] != None: ##
        #        choice = n["Bodypart"] ##
        #        break
        #driver.find_element(By.CSS_SELECTOR, "#search-job-bodypart").send_keys(choice) ##
        #if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
        #    testResult="failed"
        #    Result_msg += "#1 "
        ### SearchFilter_Bodypart 결과 전송 ##
        ##if testResult == 'failed':
        ##    testlink.reportTCResult(2611, testPlanID, buildName, 'f', Result_msg)            
        ##else:
        ##    testlink.reportTCResult(2611, testPlanID, buildName, 'p', "SearchFilter_Bodypart Test Passed")

        ## Gender ##
        #testResult=""
        #Result_msg = "failed at "
        #particular = "Gender"
        #wk_index_num = WORKLIST.SearchFilter_Etc_setting("17","Gender/Age") ##
        #choice = "F"
        #driver.find_element(By.CSS_SELECTOR, "#search_job_pat_gender_chosen > a > span").click()
        #driver.find_element(By.CSS_SELECTOR, "#search_job_pat_gender_chosen > div > ul > li:nth-child(2)").click()
        #if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
        #    testResult="failed"
        #    Result_msg += "#1 "
        ### SearchFilter_Gender 결과 전송 ##
        ##if testResult == 'failed':
        ##    testlink.reportTCResult(2614, testPlanID, buildName, 'f', Result_msg)            
        ##else:
        ##    testlink.reportTCResult(2614, testPlanID, buildName, 'p', "SearchFilter_Gender Test Passed")

        ## PatientID ##
        #testResult=""
        #Result_msg = "failed at "
        #particular = ""
        #wk_index_num = WORKLIST.SearchFilter_Etc_setting("8","P.ID") ##
        #choice = ""
        #for n in data:
        #    if n["PatientID"] != None: ##
        #        choice = n["PatientID"] ##
        #        break
        #driver.find_element(By.CSS_SELECTOR, "#search-job-pat-id").send_keys(choice) ##
        #if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
        #    testResult="failed"
        #    Result_msg += "#1 "
        ### SearchFilter_PatientID 결과 전송 ##
        ##if testResult == 'failed':
        ##    testlink.reportTCResult(2624, testPlanID, buildName, 'f', Result_msg)            
        ##else:
        ##    testlink.reportTCResult(2624, testPlanID, buildName, 'p', "SearchFilter_PatientID Test Passed")

        ## PatientName ##
        #testResult=""
        #Result_msg = "failed at "
        #particular = "PatientName&"
        #wk_index_num = WORKLIST.SearchFilter_Etc_setting("7","P.Name") ##
        #choice = ""
        #for n in data:
        #    if n["PatientName"] != None: ##
        #        choice = n["PatientName"] ##
        #        particular += n["PatientNameMask"]
        #        break
        #driver.find_element(By.CSS_SELECTOR, "#search-job-pat-name").send_keys(choice) ##
        #if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
        #    testResult="failed"
        #    Result_msg += "#1 "
        ### SearchFilter_PatientName 결과 전송 ##
        ##if testResult == 'failed':
        ##    testlink.reportTCResult(2627, testPlanID, buildName, 'f', Result_msg)            
        ##else:
        ##    testlink.reportTCResult(2627, testPlanID, buildName, 'p', "SearchFilter_PatientName Test Passed")

        ## PatientAge ##
        #testResult=""
        #Result_msg = "failed at "
        #particular = ""
        #wk_index_num = WORKLIST.SearchFilter_Etc_setting("17","Gender/Age") ##
        #choice = ""
        #for n in data:
        #    if n["PatientSexAndAge"] != None: ##
        #        temp =  (n["PatientSexAndAge"]).split("/")[1]
        #        if temp != "":
        #            choice = n["PatientSexAndAge"]
        #            break
        #driver.find_element(By.CSS_SELECTOR, "#search-job-pat-age").send_keys(choice.split("/")[1]) ##
        #if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
        #    testResult="failed"
        #    Result_msg += "#1 "
        ### SearchFilter_PatientAge 결과 전송 ##
        ##if testResult == 'failed':
        ##    testlink.reportTCResult(2630, testPlanID, buildName, 'f', Result_msg)            
        ##else:
        ##    testlink.reportTCResult(2630, testPlanID, buildName, 'p', "SearchFilter_PatientAge Test Passed")

        ## ImageCount ##
        #testResult=""
        #Result_msg = "failed at "
        #particular = ""
        #wk_index_num = WORKLIST.SearchFilter_Etc_setting("12","I.CNT") ##
        #choice = ""
        #for n in data:
        #    if n["ImageCount"] != None: ##
        #        choice = str(n["ImageCount"]) ##
        #        break
        #driver.find_element(By.CSS_SELECTOR, "#search-job-image-cnt").send_keys(choice) ##
        #if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
        #    testResult="failed"
        #    Result_msg += "#1 "
        ### SearchFilter_ImageCount 결과 전송 ##
        ##if testResult == 'failed':
        ##    testlink.reportTCResult(2633, testPlanID, buildName, 'f', Result_msg)            
        ##else:
        ##    testlink.reportTCResult(2633, testPlanID, buildName, 'p', "SearchFilter_ImageCount Test Passed")

        ## StudyDesc ##
        #testResult=""
        #Result_msg = "failed at "
        #particular = ""
        #wk_index_num = WORKLIST.SearchFilter_Etc_setting("20","Study Desc") ##
        #choice = ""
        #for n in data:
        #    if n["StudyDesc"] != None: ##
        #        choice = n["StudyDesc"] ##
        #        break
        #driver.find_element(By.CSS_SELECTOR, "#search-job-study-desc").send_keys(choice) ##
        #if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
        #    testResult="failed"
        #    Result_msg += "#1 "
        ### SearchFilter_StudyDesc 결과 전송 ##
        ##if testResult == 'failed':
        ##    testlink.reportTCResult(2624, testPlanID, buildName, 'f', Result_msg)            
        ##else:
        ##    testlink.reportTCResult(2624, testPlanID, buildName, 'p', "SearchFilter_StudyDesc Test Passed")

        # NotRefered R인 경우 확인 필요##
        testResult=""
        Result_msg = "failed at "
        wk_index_num = WORKLIST.SearchFilter_Etc_setting("2","R") ##
        element = driver.find_element(By.CSS_SELECTOR, "#hospital_list > button:nth-child(1)")
        driver.execute_script("arguments[0].click();", element)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr[1]/td[4]/span/label")))

        del driver.requests
        # not refer click
        driver.find_element(By.CSS_SELECTOR, "#search_box_body > div:nth-child(1) > div.col-lg-1.col-md-1.col-sm-12.m-t-10.refer-search-condition.woklist-searchfilter > label").click()
        time.sleep(3)

        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        page_len = int(data['Length'])
        # total page
        total = math.ceil(int(data['recordsFiltered']) / page_len)
        # remain
        last_page_num = int(data['recordsFiltered']) % page_len
        if last_page_num == 0:
            for a in range(1, total+1):
                for b in range(1, page_len+1):
                    if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(wk_index_num)+"]/span/label").text != "":
                        testResult = 'failed'
                        break
                if(testResult != '' or a == total):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        else:
            for a in range(1, total+1):
                if a == total:
                    for b in range(1, last_page_num+1):
                        if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(wk_index_num)+"]/span/label").text != "":
                            testResult = 'failed'
                            break
                if a == total:
                    break
                for b in range(1, page_len+1):
                    if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(wk_index_num)+"]/span/label").text != "":
                        testResult = 'failed'
                        break
                if(testResult != ''):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        
        # Clear
        driver.find_element(By.CSS_SELECTOR, "#clear_searchfilter > span").click()
        # refresh
        driver.find_element(By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title").click()

        ## SearchFilter_NotRefered 결과 전송 ##
        #if testResult == 'failed':
        #    testlink.reportTCResult(2639, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2639, testPlanID, buildName, 'p', "SearchFilter_NotRefered Test Passed")
        


        print(Result_msg)

       


WORKLIST.SearchFilter_Etc()

def test():
    print("test")
    # 정상적인 계정으로 로그인
    signInOut.normal_login()
        
    # waiting loading
    try:
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
    except:
        pass

    tr = "O/"
    temp = tr.split("/")[1]
    print(type(temp))
    print(temp)
    

        
#test()
