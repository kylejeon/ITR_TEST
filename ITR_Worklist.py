# -*- coding: utf-8 -*-

#from testlink import TestlinkAPIClient, TestLinkHelper
from ast import Try
from doctest import TestResults
from mailbox import Babyl
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
import json, math
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

        # 잘못된 user ID를 입력하고 sign in을 클릭한다
        signInOut.admin_sign_in('administrator','Server123!@#')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        # User not found
        try:
            assert driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/form/label").text=="Please confirm the password by retyping it in the confirm field."
        except:
            testResult = 'failed'

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
    def Badge_Emergency():
        testResult=""

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

        ## Badge_Emergency 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2351, testPlanID, buildName, 'f', "Badge Emergency Test Failed")            
        #else:
        #    testlink.reportTCResult(2351, testPlanID, buildName, 'p', "Badge Emergency Test Passed")

    def Badge_Refer():
        testResult=""

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

        ## Badge_Refer 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2354, testPlanID, buildName, 'f', "Badge Refer Test Failed")            
        #else:
        #    testlink.reportTCResult(2354, testPlanID, buildName, 'p', "Badge Refer Test Passed")

    def Badge_AutoRefer():
        testResult=""

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

        ## Badge_AutoRefer 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2357, testPlanID, buildName, 'f', "Badge AutoRefer Test Failed")            
        #else:
        #    testlink.reportTCResult(2357, testPlanID, buildName, 'p', "Badge AutoRefer Test Passed")

    def Badge_Schedule():
        testResult=""

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

        ## Badge_Schedule 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2360, testPlanID, buildName, 'f', "Badge Schedule Test Failed")            
        #else:
        #    testlink.reportTCResult(2360, testPlanID, buildName, 'p', "Badge Schedule Test Passed")

    def Badge_Today():
        testResult=""

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

        ## Badge_Today 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2363, testPlanID, buildName, 'f', "Badge Today Test Failed")            
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

        ## Home 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2367, testPlanID, buildName, 'f', "Home Test Failed")            
        #else:
        #    testlink.reportTCResult(2367, testPlanID, buildName, 'p', "Home Test Passed")

    def new_message():
        testResult=""

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

        # 메인화면 읽지 않은 메시지 수 존재 확인 #1
        try:
            assert (int(driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/a/sup/span").text) == read_count)
        except:
            testResult = 'failed'
        

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

        # 체크 및 체크 해제 #4
        # Institution
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
        except:
            testResult = 'failed'
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = 'failed'
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
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr/td[1]/label").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = 'failed'
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
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = 'failed'
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
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = 'failed'
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
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = 'failed'
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
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = 'failed'
        except:
            pass

        # Recipient를 선택하지 않고, 다음 버튼을 클릭 #7
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[4]").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[13]/div[7]/div/button")))
            driver.find_element(By.XPATH, "/html/body/div[13]/div[7]/div/button").click()
        except:
            testResult = 'failed' 
      
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
        except:
            testResult = 'failed' 

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
            except:
                testResult = 'failed'
        
        # Message 입력창에 메시지를 입력하고, 전송 버튼을 클릭 #9
        if(testResult == ''):
            driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[3]").click()
            try:
                WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[12]/div[7]/div/button")))
                driver.find_element(By.XPATH,"/html/body/div[12]/div[7]/div/button").click()
            except:
                testResult = 'failed'
        
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

        ## new_message 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2371, testPlanID, buildName, 'f', "new_message Test Failed")            
        #else:
        #    testlink.reportTCResult(2371, testPlanID, buildName, 'p', "new_message Test Passed")

    def Message():
        testResult=""

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

        # View more messages확인 
        try:
            assert(driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[3]/ul/li[4]/a/div/p").get_property("outerText")=="View more messages")
        except:
            testResult = 'failed'

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
        driver.find_element(By.XPATH, "/html/body/div[9]/div/div/div[3]/button").click()

        ## message 결과 전송
        #if testResult == 'failed':
        #    testlink.reportTCResult(2384, testPlanID, buildName, 'f', "Message Test Failed")            
        #else:
        #    testlink.reportTCResult(2384, testPlanID, buildName, 'p', "Message Test Passed")

    def View_More_Messages():
        testResult=""

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

        # 리스트 및 아이콘 확인 #1 ##리스트확인도 수정해야함
        print(driver.find_element(By.XPATH,"/html/body/section[1]/div/div/div/section[4]/div/div[1]/div/div[2]/button").text)
        try:
            assert(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[4]/div/div[1]/div/div[2]/button/span[1]".text == "Direct Message List"))
        except:
            testResult = 'failed'

        request = driver.wait_for_request('.*/GetDirectMessageList')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        read_flag = []
        for n in data:
            read_flag.append(data["READ_FLAG"])####여기부터 수정
        print(testResult)

        

    ## 전체 긁는 방식
    #def test():
    #    # 새로운 탭 + 전환
    #    driver.execute_script("window.open()")
    #    driver.switch_to.window(driver.window_handles[1])
    #    driver.get(AdminUrl);

    #    # admin 사이트 로그인
    #    driver.find_element(By.ID, 'user-id').clear()
    #    driver.find_element(By.ID, 'user-id').send_keys(admin_id)
    #    driver.find_element(By.ID, 'user-password').clear()
    #    driver.find_element(By.ID, 'user-password').send_keys(admin_pw)
    #    driver.find_element(By.CSS_SELECTOR, '.btn').click()
    #    driver.implicitly_wait(5)

    #    # Configuration
    #    element = driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[2]/div[1]/ul/li[5]/a')
    #    driver.execute_script("arguments[0].click();", element)
    #    driver.implicitly_wait(5)

    #    # 캡처 초기화
    #    del driver.requests

    #    # 아이디 검색 및 패킷에서 center 정보 습득
    #    driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[3]/div/div/input').send_keys(worklist_id)
    #    driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[6]/div/button').click()
    #    driver.implicitly_wait(5)
    #    request = driver.wait_for_request('.*/GetUserList.*')
    #    body = request.response.body.decode('utf-8')
    #    data = (json.loads(body))['data']
    #    center = ""
    #    for n in data:
    #        if n['UserID'] == worklist_id:
    #            center = n['CenterCode']
    #            break

    #    # 캡처 초기화
    #    del driver.requests

    #    # Reporter 검색 및 패킷에서 Center가 같은 Reporter 정보 습득
    #    driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[3]/div/div/input').clear()

    #    driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[1]/div').click()
    #    driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[1]/div/div/ul/li[4]').click()
    #    driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[6]/div/button').click()
    #    driver.implicitly_wait(5)
        
    #    request = driver.wait_for_request('.*/GetUserList.*')
    #    body = request.response.body.decode('utf-8')
    #    data = json.loads(body)

    #    total = math.trunc(data['recordsTotal'] / data['Length'])
    #    same_center = []

    #    for repeat in range(0,total):
    #        request = driver.wait_for_request('.*/GetUserList.*')
    #        body = request.response.body.decode('utf-8')
    #        data = (json.loads(body))['data']

    #        for n in data:
    #            if n['CenterCode'] == center:
    #                same_center.append(n['UserName'])

    #        # 캡처 초기화
    #        del driver.requests

    #        element = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[4]/ul/li[9]/a")
    #        driver.execute_script("arguments[0].click();", element)

    #    for n in same_center:
    #        print(n)

    #    #driver.close()


TOPMENU.View_More_Messages()
