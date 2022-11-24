# -*- coding: utf-8 -*-

from testlink import TestlinkAPIClient, TestLinkHelper
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
#from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import json, math, time

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# User: kyle
URL = 'http://testserver-win:81/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
DevKey = 'adcb86843d0c77e6e0c9950f80a143c0'
# testlink 초기화
tl_helper = TestLinkHelper()
testlink = tl_helper.connect(TestlinkAPIClient) 
testlink.__init__(URL, DevKey)
testlink.checkDevKey()

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

#Report 용 / Test Hospital 변경 시, 코드 변경 필요 
testHospital = "Cloud Team"

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
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div[2]/button[1]")))
            driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div[2]/button[1]").click()
        except:
            pass

        # waiting loading
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

def ReFresh():
    driver.find_element(By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title").click()
    driver.implicitly_wait(5)

class windowSize:
    driver.set_window_size(1920, 1080)

class Login:
    def Log_InOut():
        print("ITR-121: Log In/Out > Log In/Out")
        testResult = True
        Result_msg = "failed at "

        # 잘못된 user ID를 입력하고 sign in을 클릭한다
        signInOut.admin_sign_in('administrator','Server123!@#')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        time.sleep(0.1)
        # User not found
        try:
            assert driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/form/label").get_property("textContent")=="Please confirm the password by retyping it in the confirm field."
        except:
            testResult = False
            Result_msg+="#3 "

        # 정상적인 계정으로 로그인 한다.
        signInOut.normal_login()
        try:
            assert driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[7]/a/span").text == "Logout"
        except:
            testResult = False
            Result_msg+="#2 "

        # 로그아웃 후, 로그인 페이지를 확인한다.
        driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[7]/a/span").click()
        driver.implicitly_wait(5)
        try:
            assert driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/form/div[1]").text == "Sign in to start your session"
        except:
            testResult = False
            Result_msg+="#4 "

        # sign_InOut 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2309, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2309, testPlanID, buildName, 'p', "Log_InOut Test Passed")
    
    def Remember_me():
        testResult = True
        Result_msg = "failed at "
        print("ITR-122: Remember Me > Remember Me")
        
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
            testResult = False
            Result_msg+="#1 "

        # Remember_me 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2316, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2316, testPlanID, buildName, 'p', "Remember me Test Passed")

class TOPMENU:
    def Badge_Emergency():
        testResult = True
        Result_msg = "failed at "
        print("ITR-127: Badege > Emergency")
        # 캡처 초기화
        del driver.requests
        time.sleep(1)
        # badge 클릭
        driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/div[1]/div/div[2]/div[1]').click()
        # waiting loading
        try:
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Badge의 표시 갯수 획득
        request = driver.wait_for_request('.*AllInstitutionList.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        cmr1 = data['TotalPriorityCount']
        cmr2 = int(driver.find_element(By.CSS_SELECTOR, "#emergency_count").text)

        # worklist record Total 획득
        request = driver.wait_for_request('.*E&JobStatus=200&JobStartDate.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        recordTotal = data['recordsTotal']

        # 비교
        try:
            assert (cmr1 == recordTotal and 
                    cmr1 == cmr2)
        except:
            testResult = False
            Result_msg+="#1 "

        # Badge_Emergency 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2351, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2351, testPlanID, buildName, 'p', "Badge Emergency Test Passed")

    def Badge_Refer():
        testResult = True
        Result_msg = "failed at "
        print("ITR-128: Badge > Refer")
        # 캡처 초기화
        del driver.requests
        time.sleep(1)
        # badge 클릭
        driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/div[2]/div/div[2]/div[1]').click()
        # waiting loading
        try:
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Badge의 표시 갯수 획득
        request = driver.wait_for_request('.*AllInstitutionList.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        cmr1 = data['TotalReferCount']
        cmr2 = int(driver.find_element(By.CSS_SELECTOR, "#refer_count").text)

        # worklist record Total 획득
        request = driver.wait_for_request('./GetReferCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        recordTotal = data['recordsTotal']

        # 비교
        try:
            assert (cmr1 == recordTotal and 
                    cmr1 == cmr2)
        except:
            testResult = False
            Result_msg+="#1 "

        # Badge_Refer 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2354, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2354, testPlanID, buildName, 'p', "Badge Refer Test Passed")

    def Badge_AutoRefer():
        testResult = True
        Result_msg = "failed at "
        print("ITR-129: Badge > Auto Refer")

        # 캡처 초기화
        del driver.requests
        time.sleep(1)
        # badge 클릭
        driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/div[3]/div/div[2]/div[1]').click()
        # waiting loading
        try:
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Badge의 표시 갯수 획득
        request = driver.wait_for_request('.*AllInstitutionList.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        cmr1 = data['TotalAutoReferCount']
        cmr2 = int(driver.find_element(By.CSS_SELECTOR, "#autorefer_count").text)

        # worklist record Total 획득
        request = driver.wait_for_request('.*NotRefered=true.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        recordTotal = data['recordsTotal']
        refer = int(driver.find_element(By.CSS_SELECTOR, "#refer_count").text)

        # 비교
        try:
            assert (cmr1 == (recordTotal-refer) and
                    cmr1 == cmr2)
        except:
            testResult = False
            Result_msg+="#1 "

        # Badge_AutoRefer 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2357, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2357, testPlanID, buildName, 'p', "Badge AutoRefer Test Passed")

    def Badge_Schedule():
        testResult = True
        Result_msg = "failed at "
        print("ITR-130: Badge > Schedule")

        # 캡처 초기화
        del driver.requests
        time.sleep(1)
        # badge 클릭
        driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/div[4]/div/div[2]/div[1]').click()
        time.sleep(0.3)
        # waiting loading
        try:
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Badge의 표시 갯수 획득
        request = driver.wait_for_request('.*AllInstitutionList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        cmr1 = data['TotalScheduleReferCount']
        cmr2 = int(driver.find_element(By.CSS_SELECTOR, "#schedule_count").text)

        # worklist record Total 획득
        request = driver.wait_for_request('./GetScheduleReferCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        recordTotal = data['recordsTotal']

        # 비교
        try:
            assert (cmr1 == recordTotal and 
                    cmr1 == cmr2)
        except:
            testResult = False
            Result_msg+="#1 "

        # Badge_Schedule 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2360, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2360, testPlanID, buildName, 'p', "Badge Schedule Test Passed")

    def Badge_Today():
        testResult = True
        Result_msg = "failed at "
        print("ITR-131: Badge > Today")

        # 캡처 초기화
        del driver.requests
        time.sleep(1)
        # badge 클릭
        driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/div[5]/div/div[2]/div[1]').click()
        # waiting loading
        try:
            WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

        # Badge의 표시 갯수 획득
        request = driver.wait_for_request('.*AllInstitutionList.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        cmr1 = data['TotalReportedCompletedCount']
        cmr2 = int(driver.find_element(By.CSS_SELECTOR, "#today_completed_reported_count").text)

        # worklist record Total 획득
        request = driver.wait_for_request('./GetCompletedReportedJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        recordTotal = data['recordsTotal']

        # 비교
        try:
            assert (cmr1 == recordTotal and 
                    cmr1 == cmr2)
        except:
            testResult = False
            Result_msg+="#1 "

        # Badge_Today 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2363, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2363, testPlanID, buildName, 'p', "Badge Today Test Passed")

    def Badge():
        TOPMENU.Badge_Emergency()
        TOPMENU.Badge_Refer()
        TOPMENU.Badge_AutoRefer()
        TOPMENU.Badge_Schedule()
        TOPMENU.Badge_Today()

    def Home():
        testResult = True
        Result_msg = "failed at "
        print("ITR-132: Top Menu > Home")

        ReFresh()
        
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
            testResult = False
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
            testResult = False
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
            testResult = False
            Result_msg+="#1 "

        # Home 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2367, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2367, testPlanID, buildName, 'p', "Home Test Passed")

    def new_message():
        testResult = True
        Result_msg = "failed at "
        print("ITR-133: Top Menu > Direct Message > New Message")
        ReFresh()

        # READ_FLAG T or F 확인 (파란색 회색 확인) 및 읽지 않은 메시지 수 확인 #2
        element = driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/a/span")
        driver.execute_script("arguments[0].click();", element)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]/span")))

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
                testResult = False
                Result_msg+="#2 "

        # 메인화면 읽지 않은 메시지 수 존재 확인 #1
        try:
            assert (int(driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/a/sup/span").text) == read_count)
        except:
            testResult = False
            Result_msg+="#1 "
        

        # 캡처 초기화
        del driver.requests

        # new message 접속 및 패킷에서 정보 획득 #3
        element = driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/ul/li[2]/div/ul/li/a")
        driver.execute_script("arguments[0].click();", element)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[1]")))

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
        
        driver.find_element(By.CSS_SELECTOR, "body > nav > div > ul:nth-child(3) > li > a > span").click()
        driver.implicitly_wait(5)
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
            testResult = False
            Result_msg+="#3 "

        # 체크 및 체크 해제 #4
        # Institution
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
        except:
            testResult = False
            Result_msg+="#4 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = False
            Result_msg+="#4 "
        except:
            pass

        # Center
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[2]/a").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr/td[1]/label").click()
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
        except:
            testResult = False
            Result_msg+="#4 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr/td[1]/label").click()
        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = False
            Result_msg+="#4 "
        except:
            pass

        # Reporter
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[3]/a").click()
        WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
        except:
            testResult = False
            Result_msg+="#4 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = False
            Result_msg+="#4 "
        except:
            pass

        # 체크 및 삭제아이콘 선택 #5
        # Institution
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[1]/a").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
        except:
            testResult = False
            Result_msg+="#5 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i").click()
        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = False
            Result_msg+="#5 "
        except:
            pass

        # Center
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[2]/a").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr/td[1]/label").click()
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
        except:
            testResult = False
            Result_msg+="#5 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i").click()
        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = False
            Result_msg+="#5 "
        except:
            pass

        # Reporter
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[3]/a").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
        except:
            testResult = False
            Result_msg+="#5 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i").click()
        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
            testResult = False
            Result_msg+="#5 "
        except:
            pass

        # Recipient를 선택하지 않고, 다음 버튼을 클릭 #7
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[4]").click()
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[13]/div[7]/div/button")))
            driver.find_element(By.XPATH, "/html/body/div[13]/div[7]/div/button").click()
        except:
            testResult = False 
            Result_msg+="#7 "
      
        # Recipient 선택 후, 다음 버튼 클릭 #6
        # Institution
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[1]/a").click()
        WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[4]").click()
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]")))
            driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]").click()
        except:
            testResult = False 
            Result_msg+="#6 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i").click()
        
        # Center
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[2]/a").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr/td[1]/label").click()
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[4]").click()
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]")))
            driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]").click()
        except:
            testResult = False
            Result_msg+="#6 "
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i").click()

        # Reporter
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[3]/a").click()
        WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label")))
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label").click()
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[4]").click()
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]")))
            driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]").click()
        except:
            testResult = False
            Result_msg+="#6 "

        # Message 입력창에 메시지를 입력하지 않고, 전송 버튼을 클릭 #10
        driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[4]").click()
        try:
            WebDriverWait(driver,5 ).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]")))
            driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[3]").click()
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[13]/div[7]/div/button")))
                driver.find_element(By.XPATH, "/html/body/div[13]/div[7]/div/button").click()
            except:
                testResult = False
                Result_msg+="#10 "
        except:
            testResult = False 
            Result_msg+="#10 "

        # 임의의 메시지를 입력하고, 이전 버튼을 클릭, 그리고 다시 다음 버튼 클릭 #8
        if(testResult == True):
            rnd_msg = "rnd_msg"
            driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[2]/div/div/div[2]/textarea").send_keys(rnd_msg)
            driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[2]").click()
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[4]")))
                driver.find_element(By.XPATH,"/html/body/div[8]/div/div/div[3]/div/div/button[4]").click()
                try:
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[3]")))
                    assert(driver.find_element(By.XPATH,"/html/body/div[8]/div/div/div[2]/section[2]/div/div/div[2]/textarea").get_property("value")==rnd_msg)
                except:
                    testResult = False
                    Result_msg+="#8 "
            except:
                testResult = False
                Result_msg+="#8 "
        
        # Message 입력창에 메시지를 입력하고, 전송 버튼을 클릭 #9
        if(testResult == True):
            driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[3]").click()
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[12]/div[7]/div/button")))
                driver.find_element(By.XPATH,"/html/body/div[12]/div[7]/div/button").click()
            except:
                testResult = False
                Result_msg+="#9 "
        
        # Message 입력창에 메시지를 입력하고, 취소 버튼을 클릭 #11
        if(testResult == True):
            driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/a/span").click()
            try:
                del driver.requests
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/ul/li[2]/div/ul/li/a")))
                driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/ul/li[2]/div/ul/li/a").click()
                # new message
                
                request = driver.wait_for_request('.*/GetAccessReporterList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]
                order = 0
                for n in data:
                    if n["USER_NAME"].lower() == worklist_id.lower():
                        order = data.index(n) + 1
                        break

                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#next_step_add_direct_message")))
                driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[1]/ul/li[3]/a").click()                
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/label")))
                driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr["+str(order)+"]/td[1]/label").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/ul/li/button[2]/i")))
                driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[4]").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[1]")))
                driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[2]/div/div/div[2]/textarea").send_keys("rnd_msg")
                element = driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[3]/div/div/button[1]")
                driver.execute_script("arguments[0].click();", element)
            except:
                testResult = False
                Result_msg+="#11 "

        # new_message 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2371, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2371, testPlanID, buildName, 'p', "new_message Test Passed")

    def Message():
        testResult = True
        Result_msg = "failed at "
        print("ITR-134: Top Menu > Direct Message > Message")

        ReFresh()

        # add msg
        del driver.requests
        need_msg_num = 0
        try:
            if int(driver.find_element(By.CSS_SELECTOR, "#direct_message_badge_body").text) < 11:
                need_msg_num = 11 - int(driver.find_element(By.CSS_SELECTOR, "#direct_message_badge_body").text)
        except:
            need_msg_num = 11
        if need_msg_num != 0:
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-direct-message > span").click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#direct_message_add_btn")))
            driver.find_element(By.CSS_SELECTOR, "#direct_message_add_btn").click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#select_recipient_section > div.col-lg-7 > div > div.header > ul > li:nth-child(3) > a")))
            
            
            request = driver.wait_for_request('.*/GetAccessReporterList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            order = 0
            for n in data:
                if n["USER_NAME"].lower() == worklist_id.lower():
                    order = data.index(n) + 1
                    break
            driver.find_element(By.CSS_SELECTOR, "#cancel_add_direct_message").click()
            time.sleep(0.25)
            
            for n in range (0, need_msg_num):
                driver.find_element(By.CSS_SELECTOR, "#right-sidebar-direct-message > span").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#direct_message_add_btn")))
                driver.find_element(By.CSS_SELECTOR, "#direct_message_add_btn").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#select_recipient_section > div.col-lg-7 > div > div.header > ul > li:nth-child(3) > a")))
                driver.find_element(By.CSS_SELECTOR, "#select_recipient_section > div.col-lg-7 > div > div.header > ul > li:nth-child(3) > a").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#dm_access_reporter_list > thead > tr > th.th-check.align-center.dm-th-check.sorting_disabled > label")))
                element = driver.find_element(By.XPATH, "/html/body/div[8]/div/div/div[2]/section[1]/div[2]/div/div[2]/div[3]/div/div/div/div/table/tbody/tr["+str(order)+"]/td[1]/input")
                driver.execute_script("arguments[0].click();", element)
                driver.find_element(By.CSS_SELECTOR, "#next_step_add_direct_message").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#confirm_add_direct_message")))
                driver.find_element(By.CSS_SELECTOR, "#add_direct_message_textarea").send_keys(n)
                driver.find_element(By.CSS_SELECTOR, "#confirm_add_direct_message").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#right-sidebar-direct-message > span")))
                
        # 1,2는 new_message와 동일
        del driver.requests

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
                testResult = False
                Result_msg+="#0 "

        # View more messages확인 
        try:
            assert(driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[3]/ul/li[4]/a/div/p").get_property("outerText")=="View more messages")
        except:
            testResult = False
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
            testResult = False
            Result_msg+="#4 "
        driver.find_element(By.XPATH, "/html/body/div[9]/div/div/div[3]/button").click()

        # message 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2384, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2384, testPlanID, buildName, 'p', "Message Test Passed")

    def View_More_Messages():
        testResult = True
        Result_msg = "failed at "
        print("ITR-135: Top Menu > Direct Message > View More Messages")

        ReFresh()

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
            WebDriverWait(driver, 0.25).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[4]/div/div[1]/div/div[1]/div")))
        except:
            pass

        # 리스트 및 아이콘 확인 / 읽지 않은 메시지 클릭 #1 #2
        # 1 - 리스트 확인
        try:
            assert(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[4]/div/div[1]/div/div[2]/button").get_property("id") == "direct_message_all_list_tab")
        except:
            testResult = False
            Result_msg+="#1 "

        # 2 - read unread_count at icon
        unread_count = driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]/a/sup/span").text
        time.sleep(0.1)
        #print(unread_count)

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
                testResult = False
                Result_msg+="#2 "
            non_read_name = data["data"][first_non_read_loc]["WRITER_NAME"]
            non_read_dtm = (data["data"][first_non_read_loc]["WRITE_DTTM"]).replace('T', ' ')
            non_read_msg = data["data"][first_non_read_loc]["MESSAGE_TEXT_LOB"]
            read_flag[non_read_index] = 'T'

        # waiting loading
        try:
            WebDriverWait(driver, 0.3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[4]/div/div[2]/div/div/div/div/div[3]")))
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
                    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[4]/div/div[3]/div/div[3]/textarea")))
                except:
                    testResult = False
                    Result_msg+="#2 "
                time.sleep(0.25)
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
                    testResult = False
                    Result_msg+="#1 "
            else:
                if(icon[i] != "rgba(255, 165, 0, 1)"):
                    testResult = False
                    Result_msg+="#1 "

        #print(int(driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[3]/a/sup/span").get_property("textContent")))
        #print((int(unread_count)-1))
        #print(int(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[4]/div/div[1]/div/div[2]/button/span[2]").text))
        # 2 & 3 - 
        try:
            assert(int(driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[3]/a/sup/span").get_property("textContent")) == (int(unread_count)-1) and
                   non_read_name == non_read_name_pack and 
                   non_read_dtm == non_read_dtm_pack and
                   non_read_msg == non_read_msg_pack and
                   int(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[4]/div/div[1]/div/div[2]/button/span[2]").text) == (int(unread_count)-1))
        except:
            testResult = False
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
            testResult = False
            Result_msg+="#3 "

        # View_More_Message 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2390, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2390, testPlanID, buildName, 'p', "View_More_Message Test Passed")
        
    def Setting():
        testResult = True
        Result_msg = "failed at "
        print("ITR-137: Top Menu > Setting > Setting")

        ReFresh()

        element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-setting > i")
        driver.execute_script("arguments[0].click();", element)

        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting_user_profile"))) 
        except:
            testResult = False
            Result_msg+="#1 "

        # Setting 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2404, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2404, testPlanID, buildName, 'p', "Setting Test Passed")

    def Report_Search_Filter():
        testResult = True
        Result_msg = "failed at "
        print("ITR-138: Top Menu > Setting > Standard Report - Search Filter")

        ReFresh()

        # 캡처 초기화
        del driver.requests
        time.sleep(1) 

        # Setting 접속
        element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-setting > i")
        driver.execute_script("arguments[0].click();", element)

        # waiting loading
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting_user_profile"))) 
        driver.find_element(By.CSS_SELECTOR, "#right-sidebar-home").click()
        element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-setting > i")
        driver.execute_script("arguments[0].click();", element)
        time.sleep(3)

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
            testResult = False
            Result_msg+="#1 "
        
        # 3 - 준비
        request = driver.wait_for_request('.*/GetReportCode.*')
        body = request.response.body.decode('utf-8')
        report_list_pk = (json.loads(body))
        
        # Group Code Search #2
        if(len(data) < 2):
            testResult = False
            Result_msg+="#2-pre_condition "

        if(testResult == True):
            # 캡처 초기화
            del driver.requests
            time.sleep(1) 

            driver.find_element(By.CSS_SELECTOR, "#stdreport-group-code").click()
            driver.find_element(By.CSS_SELECTOR, "#stdreport-group-code > option:nth-child(2)").click()
            driver.find_element(By.CSS_SELECTOR, "#stdreport_search_btn > span").click()
            time.sleep(0.3)

            request = driver.wait_for_request('.*/GetStandardReportForTable.*')
            body = request.response.body.decode('utf-8')
            data = (json.loads(body))["data"]

            for n in data:
                if(n["StdReportGroup"] != search_group):
                    testResult = False
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
                testResult = False
                Result_msg+="#3 "

            # Report Search #4
            # 캡처 초기화
            del driver.requests
            time.sleep(1) 

            driver.find_element(By.CSS_SELECTOR, "#stdreport-report-code > option:nth-child(2)").click()
            driver.find_element(By.CSS_SELECTOR, "#stdreport_search_btn > span").click()
            time.sleep(0.3)

            request = driver.wait_for_request('.*/GetStandardReportForTable.*')
            body = request.response.body.decode('utf-8')
            data = (json.loads(body))["data"]

            try:
                assert(data[0]["StdReportCode"]==select_report)
            except:
                testResult = False
                Result_msg+="#4 "

            # 캡처 초기화
            del driver.requests
            time.sleep(1) 

            # Clear #7
            driver.find_element(By.CSS_SELECTOR, "#stdreport_search_clear_btn > span").click()
            try:
                request = driver.wait_for_request('.*/GetStandardReportForTable.*')
                time.sleep(0.3)
                body = request.response.body.decode('utf-8')
                data = (json.loads(body))["data"]
            except:
                testResult = False
                Result_msg+="#7 "


        if testResult == True:
            # ALL Hot Key #5
            driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[2]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div/div/div[3]/div/select").click()
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
            hotkey_number = 0
            for n in range(2,36):
                hotkey = driver.find_element(By.CSS_SELECTOR, "#stdreport_search_hotkey > option:nth-child("+str(n)+")").text
                hot_key_list.append(hotkey)
                if hotkey == hotkey_select:
                    hotkey_number = n

            try:
                assert(origin_hot_key_list == hot_key_list)
            except:
                testResult = False
                Result_msg+="#5 "

            # Hot Key Search #6
            if hotkey_select == None:
                testResult = False
                Result_msg+="#6-pre_condition "

            # 캡처 초기화
            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#stdreport_search_hotkey > option:nth-child("+str(hotkey_number)+")").click()
            driver.find_element(By.CSS_SELECTOR, "#stdreport_search_btn > span").click()
            time.sleep(0.3)

            request = driver.wait_for_request('.*/GetStandardReportForTable.*')
            body = request.response.body.decode('utf-8')
            data = (json.loads(body))["data"]

            for n in data:
                if(n["HotKey"]!=hotkey_select):
                    testResult = False
                    Result_msg+="#6 "

        # Report_Search_Filter 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2407, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2407, testPlanID, buildName, 'p', "Report_Search_Filter Test Passed")

    def Report_Add():
        testResult = True
        Result_msg = "failed at "
        print("ITR-219: Top Menu > Setting > Standard Report - Add")

        ReFresh()
        driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[7]/a/span").click()
        driver.implicitly_wait(5)
        signInOut.normal_login()

        # Setting 접속
        element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-setting > i")
        driver.execute_script("arguments[0].click();", element)

        # waiting loading
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting_user_profile"))) 
        driver.find_element(By.CSS_SELECTOR, "#right-sidebar-home").click()
        element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-setting > i")
        driver.execute_script("arguments[0].click();", element)
        time.sleep(3)

        # Add Click #1
        driver.find_element(By.CSS_SELECTOR, "#stdreport_add_btn > span").click()
        
        # 탭 전환
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[1])
        try:
            assert(driver.find_element(By.CSS_SELECTOR, "#add-stdreport-creator").get_property("value")==worklist_id)
        except:
            testResult = False
            Result_msg+="#1 "

        if testResult == True:
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
                testResult = False
                Result_msg+="#2 #3 #5 #6 #7 #9 #10 "
            
            #cancel click & check
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#add-stdreport-creator").get_property("value")==worklist_id)
            except:
                testResult = False
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

        if testResult == True:
            # 3 - 
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-home").click()
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "#search-job-modality").send_keys("CT")
            driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
            # 캡처 초기화
            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#job-report").click()
            
            # 탭 전환
            time.sleep(2.5)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(0.5)
            # AutoExpand check through packet
            for n in driver.requests:
                if n.url == "http://vm-onpacs/api/WorklistApi/GetStdReportExFolderAutoExpand?modalitiesString=CT":
                    request = n
                    break
            body = request.response.body.decode('utf-8')
            data = (json.loads(body))

            if 'rnd_gr_code' not in data:
                testResult = False
                Result_msg+="#3 "
                

            #탭 전환
            driver.implicitly_wait(5)
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
                testResult = False
                Result_msg+="#4&#8#11_pre-condition "

            # Add Click 
            driver.find_element(By.CSS_SELECTOR, "#stdreport_add_btn > span").click()
        
            # 탭 전환
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[1])
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#add-stdreport-creator").get_property("value")==worklist_id)
            except:
                testResult = False
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
                testResult = False
                Result_msg+="#4 "

            # 8 - input (z)
            driver.find_element(By.CSS_SELECTOR, "#add_stdreport_hotKey_chosen > a > span").click()
            time.sleep(0.3)
            driver.find_element(By.CSS_SELECTOR, "#add_stdreport_hotKey_chosen > div > div > input[type=text]").send_keys("Z")
            driver.find_element(By.CSS_SELECTOR, "#add_stdreport_hotKey_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            if driver.find_element(By.CSS_SELECTOR,"#add_stdreport_hotKey_chosen > a > span").text=='z':
                testResult = False
                Result_msg+="#8 "

            # 11 - Close
            # close and text check
            element = driver.find_element(By.CSS_SELECTOR, "#add-stdreport-close-btn")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.1)
            if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "Are you sure to close?":
                testResult = False
                Result_msg+="#11 "
            
            # cancel
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#add-stdreport-creator").get_property("value")==worklist_id)
            except:
                testResult = False
                Result_msg+="#11 "
            
            # ok
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add-stdreport-close-btn")))
            driver.close()

            # 탭 전환
            driver.switch_to.window(driver.window_handles[0])

        # Report_Add 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2870, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2870, testPlanID, buildName, 'p', "Report_Add Test Passed")

    def Report_Modify():
        testResult = True
        Result_msg = "failed at "
        print("ITR-139: Top Menu > Setting > Standard Report - Modify")

        ReFresh()

        # Setting 접속
        element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-setting > i")
        driver.execute_script("arguments[0].click();", element)

        # waiting loading
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting_user_profile"))) 
        except:
            testResult = False
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
            testResult = False
            Result_msg+="#1 "

        
        if testResult == True:
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
                testResult = False
                Result_msg+="#4 "
            # no
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-view-label").text == "Modify Standard Report")
            except:
                testResult = False
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
                testResult = False
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
                testResult = False
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
                testResult = False
                Result_msg+="#10 "
            # no
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            # waiting loading
            time.sleep(0.25)
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#modify-stdreport-view-label").text == "Modify Standard Report")
            except:
                testResult = False
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
                testResult = False
                Result_msg+="#10 "

        # Report_Modify 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2416, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2416, testPlanID, buildName, 'p', "Report_Modify Test Passed")

    def Report_delete():
        testResult = True
        Result_msg = "failed at "
        print("ITR-140: Top Menu > Setting > Standard Report - Delete")

        # 정상적인 계정으로 로그인
        ReFresh()

        # Setting 접속
        element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-setting > i")
        driver.execute_script("arguments[0].click();", element)

        # waiting loading
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting_user_profile"))) 
        driver.find_element(By.CSS_SELECTOR, "#right-sidebar-home").click()
        element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-setting > i")
        driver.execute_script("arguments[0].click();", element)
        time.sleep(3)

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
            testResult = False
            Result_msg+="#1 "
        # cancel
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        time.sleep(0.25)
        try:
            assert(driver.find_element(By.CSS_SELECTOR, "#setting_stdreport_searching_card > div.header > h4").text == "Search Filter")
        except:
            testResult = False
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
            testResult = False
            Result_msg+="#1 "

        # Report_delete 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2428, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2428, testPlanID, buildName, 'p', "Report_delete Test Passed")

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
        testResult = True
        Result_msg = "failed at "
        print("ITR-141: Top Menu > Setting > User Profile - Worklist")

        # 정상적인 계정으로 로그인
        ReFresh()

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
            testResult = False
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
            testResult = False
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
            testResult = False
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
            testResult = False
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
            testResult = False
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
            testResult = False
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
            testResult = False
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
            testResult = False
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

        # Profile_Worklist 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2431, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2431, testPlanID, buildName, 'p', "Profile_Worklist Test Passed")

    def Profile_Standard_Report():
        testResult = True
        Result_msg = "failed at "
        print("ITR-143: Top Menu > Setting > User Profile - Standard Report")

        ReFresh()

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
            testResult = False
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
            testResult = False
            Result_msg+="#2 "
        #탭 전환
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Profile_Standard_Report 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2444, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2444, testPlanID, buildName, 'p', "Profile_Standard_Report Test Passed")

class WORKLIST:
    # get target position in worklist and option check
    def SearchFilter_Etc_setting(target_num, target):
        # option
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(4) > label")))
        # check target
        if driver.find_element(By.CSS_SELECTOR, "#chk-column-"+target_num).is_selected() == False:
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child("+target_num+") > label").click()
        # showing wk column num
        show_list_num = 1
        for n in range (1,33):
            if driver.find_element(By.CSS_SELECTOR, "#chk-column-"+str(n)).is_selected() == True:
                show_list_num += 1
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()
        time.sleep(0.5)
        # find position
        for n in range (2,show_list_num+1):
            if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[1]/div/table/thead/tr/th["+str(n)+"]").text == target:
                target_position = n
                break

        return target_position

    def HospitalList():
        testResult = True
        Result_msg = "failed at "
        print("ITR-151: Home > Hospital List")
        ReFresh()

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
        time.sleep(1)
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
            testResult = False
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

        # 3 - 응급/Refer/Auto Refer from page
        emergency_lbadge = []
        refer_lbadge = []
        auto_refer_lbadge = []
        for n in range(1,len(data)+1):
            emergency_lbadge.append(int(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[1]/div[1]/div[1]/div[3]/div[2]/button["+str(n)+"]/span[3]").text))
            refer_lbadge.append(int(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[1]/div[1]/div[1]/div[3]/div[2]/button["+str(n)+"]/span[2]").text))
            auto_refer_lbadge.append(int(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[1]/div[1]/div[1]/div[3]/div[2]/button["+str(n)+"]/span[1]").text))

        emergency_position = WORKLIST.SearchFilter_Etc_setting("1","E")
        refer_position = WORKLIST.SearchFilter_Etc_setting("2","R")
        emergency_wk = []
        refer_wk = []
        auto_refer_wk = []
        for n in range(1,len(data)+1):
            del driver.requests
            driver.find_element(By.CSS_SELECTOR, "#hospital_list > button:nth-child("+str(n)+")").click()
            time.sleep(3)
            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            time.sleep(0.3)
            body = request.response.body.decode('utf-8')
            data_re = json.loads(body)
            page_len = int(data_re['Length'])
            # total page
            total = math.ceil(int(data_re['recordsFiltered']) / page_len)
            # remain
            last_page_num = int(data_re['recordsFiltered']) % page_len
            emergency = 0
            refer = 0
            auto_refer = 0

            for a in range(0, total):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                time.sleep(0.3)
                body = request.response.body.decode('utf-8')
                data_re = json.loads(body)["data"]

                for b in range(0, len(data_re)):
                    if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(b+1)+") > td.current-job.align-center.current-job-column-1").get_property("childElementCount") != 0:
                        emergency += 1
                    if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(b+1)+") > td.refer-tooltip.current-job.align-center.current-list-tooltip.current-job-column-2 > span > label").text == 'R':
                        refer += 1
                    if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(b+1)+") > td.refer-tooltip.current-job.align-center.current-list-tooltip.current-job-column-2 > span > label").text != 'R':
                        auto_refer+=1

                del driver.requests
                time.sleep(1)

                if a+1 == total:
                    break

                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)

            emergency_wk.append(emergency)
            refer_wk.append(refer)
            auto_refer_wk.append(auto_refer)
        try:
            assert(emergency_lbadge == emergency_wk and
                   refer_lbadge == refer_wk and
                   auto_refer_lbadge == auto_refer_wk)
        except:
            testResult = False
            Result_msg+="#3 "
        
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
                        testResult = False
                        Result_msg+="#2 "
                        break
                if(testResult != True or a == total):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        else:
            for a in range(1, total+1):
                if a == total:
                    for b in range(1, last_page_num+1):
                        if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(b)+") > td.current-job.align-center.current-job-column-13").text != click_hospital:
                            testResult = False
                            Result_msg+="#2 "
                            break
                if a == total:
                    break
                for b in range(1, page_len+1):
                    if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(b)+") > td.current-job.align-center.current-job-column-13").text != click_hospital:
                        testResult = False
                        Result_msg+="#2 "
                        break
                if(testResult != True):
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
                        testResult = False
                        Result_msg+="#5 "
                        break
                if(testResult != True or a == total):
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
                            testResult = False
                            Result_msg+="#5 "
                            break
                if a == total:
                    break
                for b in range(1, page_len+1):
                    total_list+=1
                    if driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(b)+") > td.current-job.align-center.current-job-column-13").text != click_hospital:
                        testResult = False
                        Result_msg+="#5 "
                        break
                if(testResult != True):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        try:
            assert(total_list_index == total_list)
        except:
            testResult = False
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
                testResult = False
                Result_msg+="#7 "
        except:
            testResult = False
            Result_msg+="#6 "

        # HospitalList 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2506, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2506, testPlanID, buildName, 'p', "HospitalList Test Passed")

    def SearchFilter_JobStatus_Search(job_status_position, target, num):
        testResult = True
        Result_msg = ''

        time.sleep(0.3)
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        page_len = int(data['Length'])
        # total page
        total = math.ceil(int(data['recordsFiltered']) / page_len)

        for a in range(0, total):
            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            time.sleep(0.3)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in range(0, len(data)):
                if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(n+1)+"]/td["+str(job_status_position)+"]/span/label").text != target:
                    testResult = False
                    Result_msg+="#"+num+" "
                    break
            
            if (testResult == False or a+1 == total+1):
                break

            del driver.requests
            time.sleep(1)

            element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
            driver.execute_script("arguments[0].click();", element)

        return Result_msg

    def SearchFilter_JobStatus():
        testResult = True
        Result_msg = "failed at "
        print("ITR-159: Home > Search Filter > Job Status")

        ReFresh()

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
        time.sleep(1)

        # Requested #2
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li.active-result.result-selected.highlighted").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"Requested", "2")

        # 캡처 초기화
        del driver.requests
        time.sleep(1)

        # Reported #3
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(2)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"Reported", "3")

        # 캡처 초기화
        del driver.requests
        time.sleep(1)

        # Pending #4
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(3)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"Pending", "4")

        # 캡처 초기화
        del driver.requests
        time.sleep(1)

        # Completed #5 
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(4)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"Completed", "5")

        # 캡처 초기화
        del driver.requests
        time.sleep(1)

        # Recalled #6
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(5)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"Recalled", "6")

        # 캡처 초기화
        del driver.requests
        time.sleep(1)
 
        # Canceled #7
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(6)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"Canceled", "7")

        # 캡처 초기화
        del driver.requests
        time.sleep(1)
 
        # Canceled2 #8
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(7)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"Canceled2", "8")

        # 캡처 초기화
        del driver.requests
        time.sleep(1)
 
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
                        testResult = False
                        Result_msg+="#9 "
                        break
                if(testResult != True or a == total):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        else:
            for a in range(1, total+1):
                if a == total:
                    for b in range(1, last_page_num+1):
                        if "AI" not in driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(job_status_position)+"]/span/label").text:
                            testResult = False
                            Result_msg+="#9 "
                            break
                if a == total:
                    break
                for b in range(1, page_len+1):
                    if "AI" not in driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(job_status_position)+"]/span/label").text:
                        testResult = False
                        Result_msg+="#9 "
                        break
                if(testResult != True):
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
        time.sleep(1)
 
        # DiscardCompleted #11
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > div > b").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(10)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        Result_msg+=WORKLIST.SearchFilter_JobStatus_Search(job_status_position,"DiscardCompleted", "11")

        # SearchFilter_JobStatus 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2582, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2582, testPlanID, buildName, 'p', "SearchFilter_JobStatus Test Passed")

    def SearchFilter_Date(s_css, e_css):
        testResult = True
        Result_msg = ""

        today = (datetime.today()).strftime('%Y-%m-%d')

        # Job Start/End Date Click #1
        driver.find_element(By.CSS_SELECTOR, s_css).click()
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
        except:
            testResult = False
            Reesult_msg += "#1 "

        driver.find_element(By.CSS_SELECTOR, e_css).click()
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
        except:
            testResult = False
            Result_msg += "#1 "

        today_position = []
        if testResult == True:
            # 임의의 날짜 선택(today) #2
            # start
            driver.find_element(By.CSS_SELECTOR, s_css).click()
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
                assert(driver.find_element(By.CSS_SELECTOR, s_css).get_property('value') == str(today))
            except:
                testResult = False
                Result_msg+="#2 "
            # end
            driver.find_element(By.CSS_SELECTOR, e_css).click()
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
            driver.find_element(By.XPATH, "/html/body/div[11]/div[1]/table/tbody/tr["+str(today_position[0])+"]/td["+str(today_position[1])+"]").click()
            time.sleep(0.25)
            try:             
                assert(driver.find_element(By.CSS_SELECTOR, e_css).get_property('value') == str(today))
            except:
                testResult = False
                Result_msg+="#2 "

            # clear #3
            driver.find_element(By.CSS_SELECTOR, e_css).click()
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
            driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(4) > th").click()
            time.sleep(0.25)
            try:
                assert(driver.find_element(By.CSS_SELECTOR, s_css).get_property('value') == "" and
                       driver.find_element(By.CSS_SELECTOR, e_css).get_property('value') == "")
            except:
                testResult = False
                Result_msg+="#3 "

            # Yesterday, Today, Week, Month #4
            # Yesterday
            yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
            driver.find_element(By.CSS_SELECTOR, s_css).click()
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
            driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(1) > th:nth-child(1)").click()
            time.sleep(0.25)
            try:
                assert(driver.find_element(By.CSS_SELECTOR, s_css).get_property('value') == str(yesterday) and 
                       driver.find_element(By.CSS_SELECTOR, e_css).get_property('value') == str(today))
            except:
                testResult = False
                Result_msg+="#4_1 "
            # Today
            driver.find_element(By.CSS_SELECTOR, s_css).click()
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
            driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(1) > th:nth-child(2)").click()
            time.sleep(0.25)
            try:
                assert(driver.find_element(By.CSS_SELECTOR, s_css).get_property('value') == str(today) and 
                       driver.find_element(By.CSS_SELECTOR, e_css).get_property('value') == str(today))
            except:
                testResult = False
                Result_msg+="#4_2 "
            # Week            
            for n in range(2, 7):
                driver.find_element(By.CSS_SELECTOR, s_css).click()
                WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
                driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(2) > th:nth-child("+str(n)+")").click()
                time.sleep(0.25)
                try:
                    assert(driver.find_element(By.CSS_SELECTOR, s_css).get_property('value') == str((datetime.today() - timedelta(weeks=(n-1))).strftime('%Y-%m-%d')) and 
                       driver.find_element(By.CSS_SELECTOR, e_css).get_property('value') == str(today))
                except:
                    testResult = False
                    Result_msg+="#4_3 "
                if testResult != True:
                    break
            # Month
            for n in range(2, 7):
                driver.find_element(By.CSS_SELECTOR, s_css).click()
                WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > thead > tr:nth-child(2) > th.datepicker-switch")))
                driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(3) > th:nth-child("+str(n)+")").click()
                time.sleep(0.25)
                try:
                    if(n==2):
                        assert(driver.find_element(By.CSS_SELECTOR, s_css).get_property('value') == str((datetime.today() - relativedelta(months=1)).strftime('%Y-%m-%d')) and 
                        driver.find_element(By.CSS_SELECTOR, e_css).get_property('value') == str(today))
                    else:
                        assert(driver.find_element(By.CSS_SELECTOR, s_css).get_property('value') == str((datetime.today() - relativedelta(months=3*(n-2))).strftime('%Y-%m-%d')) and 
                        driver.find_element(By.CSS_SELECTOR, e_css).get_property('value') == str(today))
                except:
                    testResult = False
                    Result_msg+="#4_4 "
                if testResult != True:
                    break

        return Result_msg


    def SearchFilter_JobDate():
        testResult = True
        Result_msg = "failed at "
        print("ITR-160: Home > Search Filter > Job Date")
        ReFresh()

        # filter hide check
        if driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").value_of_css_property("transform") != "matrix(6.12323e-17, 1, -1, 6.12323e-17, 0, 0)":
            driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").click()

        Result_msg += WORKLIST.SearchFilter_Date("#search-job-start-date", "#search-job-end-date")
        if Result_msg != "failed at ":
            testResult = False

        # SearchFilter_JobDate 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2595, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2595, testPlanID, buildName, 'p', "SearchFilter_JobDate Test Passed")

    def SearchFilter_Etc_Search(target_position, target, particular):
        testResult = True

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
                            testResult = False
                            break
                    if(testResult != True or a == total):
                        break
                    element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(0.3)
            else:
                for a in range(1, total+1):
                    if a == total:
                        for b in range(1, last_page_num+1):
                            if target not in driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(target_position)+"]").text:
                                testResult = False
                                break
                    if a == total:
                        break
                    for b in range(1, page_len+1):
                        if target not in driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(target_position)+"]").text:
                            testResult = False
                            break
                    if(testResult != True):
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
                            testResult = False
                            break
                    if(testResult != True or a == total):
                        break
                    element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(0.3)
            else:
                for a in range(1, total+1):
                    if a == total:
                        for b in range(1, last_page_num+1):
                            if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(target_position)+"]").text != mask:
                                testResult = False
                                break
                    if a == total:
                        break
                    for b in range(1, page_len+1):
                        if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(target_position)+"]").text != mask:
                            testResult = False
                            break
                    if(testResult != True):
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
                        testResult = False
                        break
                if(testResult != True or a == total):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        else:
            for a in range(1, total+1):
                if a == total:
                    for b in range(1, last_page_num+1):
                        if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(target_position)+"]").text != target:
                            testResult = False
                            break
                if a == total:
                    break
                for b in range(1, page_len+1):
                    if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(target_position)+"]").text != target:
                        testResult = False
                        break
                if(testResult != True):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        
        # Clear
        driver.find_element(By.CSS_SELECTOR, "#clear_searchfilter > span").click()
        return testResult


    # Department ~ Split Bar simple filter
    def SearchFilter_Etc():
        # filter hide check
        if driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").value_of_css_property("transform") != "matrix(6.12323e-17, 1, -1, 6.12323e-17, 0, 0)":
            driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").click()

        del driver.requests

        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        time.sleep(1)

        # data setting
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)['data']

        # Department
        testResult = True
        Result_msg = "failed at "
        print("ITR-162: Home > Search Filter > Department")

        particular = ""
        wk_index_num = WORKLIST.SearchFilter_Etc_setting("19","Department")
        choice = ""
        for n in data:
            if n["Department"] != None:
                choice = n["Department"]
                break
        driver.find_element(By.CSS_SELECTOR, "#search-job-dept").send_keys(choice)
        if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
            testResult = False
            Result_msg += "#1 "

        # SearchFilter_Department 결과 전송
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2605, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2605, testPlanID, buildName, 'p', "SearchFilter_Department Test Passed")

        # Modality ##
        testResult = True
        Result_msg = "failed at "
        print("ITR-163: Home > Search Filter > Modality")

        particular = ""
        wk_index_num = WORKLIST.SearchFilter_Etc_setting("9","Mod") ##
        choice = ""
        for n in data:
            if n["Modality"] != None: ##
                choice = n["Modality"] ##
                break
        driver.find_element(By.CSS_SELECTOR, "#search-job-modality").send_keys(choice)
        if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
            testResult = False
            Result_msg += "#1 "

        # SearchFilter_Modality 결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2608, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2608, testPlanID, buildName, 'p', "SearchFilter_Modality Test Passed")

        # Bodypart ##
        testResult = True
        Result_msg = "failed at "
        print("ITR-164: Home > Search Filter > Bodypart")

        particular = ""
        wk_index_num = WORKLIST.SearchFilter_Etc_setting("16","Bodypart") ##
        choice = ""
        for n in data:
            if n["Bodypart"] != None: ##
                choice = n["Bodypart"] ##
                break
        driver.find_element(By.CSS_SELECTOR, "#search-job-bodypart").send_keys(choice) ##
        if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
            testResult = False
            Result_msg += "#1 "

        # SearchFilter_Bodypart 결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2611, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2611, testPlanID, buildName, 'p', "SearchFilter_Bodypart Test Passed")

        # Gender ##
        testResult = True
        Result_msg = "failed at "
        print("ITR-165: Home > Search Filter > Gender")

        particular = "Gender"
        wk_index_num = WORKLIST.SearchFilter_Etc_setting("17","Gender/Age") ##
        choice = "F"
        driver.find_element(By.CSS_SELECTOR, "#search_job_pat_gender_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_pat_gender_chosen > div > ul > li:nth-child(2)").click()
        if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
            testResult = False
            Result_msg += "#1 "

        # SearchFilter_Gender 결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2614, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2614, testPlanID, buildName, 'p', "SearchFilter_Gender Test Passed")

        # PatientID ##
        testResult = True
        Result_msg = "failed at "
        print("ITR-167: Home > Search Filter > Patient ID")

        particular = ""
        wk_index_num = WORKLIST.SearchFilter_Etc_setting("8","P.ID") ##
        choice = ""
        for n in data:
            if n["PatientID"] != None: ##
                choice = n["PatientID"] ##
                break
        driver.find_element(By.CSS_SELECTOR, "#search-job-pat-id").send_keys(choice) ##
        if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
            testResult = False
            Result_msg += "#1 "

        # SearchFilter_PatientID 결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2624, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2624, testPlanID, buildName, 'p', "SearchFilter_PatientID Test Passed")

        # PatientName ##
        testResult = True
        Result_msg = "failed at "
        print("ITR-168: Home > Search Filter > Patient Name")

        particular = "PatientName&"
        wk_index_num = WORKLIST.SearchFilter_Etc_setting("7","P.Name") ##
        choice = ""
        for n in data:
            if n["PatientName"] != None: ##
                choice = n["PatientName"] ##
                particular += n["PatientNameMask"]
                break
        driver.find_element(By.CSS_SELECTOR, "#search-job-pat-name").send_keys(choice) ##
        if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
            testResult = False
            Result_msg += "#1 "

        # SearchFilter_PatientName 결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2627, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2627, testPlanID, buildName, 'p', "SearchFilter_PatientName Test Passed")

        # PatientAge ##
        testResult = True
        Result_msg = "failed at "
        print("ITR-169: Home > Search Filter > Patient Age")

        particular = ""
        wk_index_num = WORKLIST.SearchFilter_Etc_setting("17","Gender/Age") ##
        choice = ""
        
        for n in data:
            if n["PatientSexAndAge"] != None: ##
                temp =  (n["PatientSexAndAge"]).split("/")[1]
                if temp != "":
                    choice = n["PatientSexAndAge"]
                    break
        driver.find_element(By.CSS_SELECTOR, "#search-job-pat-age").send_keys(choice.split("/")[1]) ##
        if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
            testResult = False
            Result_msg += "#1 "

        # SearchFilter_PatientAge 결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2630, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2630, testPlanID, buildName, 'p', "SearchFilter_PatientAge Test Passed")

        # ImageCount ##
        testResult = True
        Result_msg = "failed at "
        print("ITR-170: Home > Search Filter > Image Count")

        particular = ""
        wk_index_num = WORKLIST.SearchFilter_Etc_setting("12","I.CNT") ##
        choice = ""
        for n in data:
            if n["ImageCount"] != None: ##
                choice = str(n["ImageCount"]) ##
                break
        driver.find_element(By.CSS_SELECTOR, "#search-job-image-cnt").send_keys(choice) ##
        if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
            testResult = False
            Result_msg += "#1 "

        # SearchFilter_ImageCount 결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2633, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2633, testPlanID, buildName, 'p', "SearchFilter_ImageCount Test Passed")

        # StudyDesc ##
        testResult = True
        Result_msg = "failed at "
        print("ITR-171: Home > Search Filter > Study Desc")
        particular = ""
        wk_index_num = WORKLIST.SearchFilter_Etc_setting("20","Study Desc") ##
        choice = ""
        for n in data:
            if n["StudyDesc"] != None: ##
                choice = n["StudyDesc"] ##
                break
        driver.find_element(By.CSS_SELECTOR, "#search-job-study-desc").send_keys(choice) ##
        if WORKLIST.SearchFilter_Etc_Search(wk_index_num, choice, particular) == 'failed':
            testResult = False
            Result_msg += "#1 "

        # SearchFilter_StudyDesc 결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2636, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2636, testPlanID, buildName, 'p', "SearchFilter_StudyDesc Test Passed")

        # NotRefered R인 경우 확인 필요##
        testResult = True
        Result_msg = "failed at "
        print("ITR-172: Home > Search Filter > Not Refered")
        wk_index_num = WORKLIST.SearchFilter_Etc_setting("2","R") ##
        element = driver.find_element(By.CSS_SELECTOR, "#hospital_list > button:nth-child(1)")
        driver.execute_script("arguments[0].click();", element)
        time.sleep(2.5)

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
                        testResult = False
                        break
                if(testResult != True or a == total):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)
        else:
            for a in range(1, total+1):
                if a == total:
                    for b in range(1, last_page_num+1):
                        if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(wk_index_num)+"]/span/label").text != "":
                            testResult = False
                            break
                if a == total:
                    break
                for b in range(1, page_len+1):
                    if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(wk_index_num)+"]/span/label").text != "":
                        testResult = False
                        break
                if(testResult != True):
                    break
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)

        # SearchFilter_NotRefered 결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2639, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2639, testPlanID, buildName, 'p', "SearchFilter_NotRefered Test Passed")

        # SearchFilter_Clear
        testResult = True
        Result_msg = "failed at "
        print("ITR-173: Home > Search Filter > Clear")

        # Clear
        driver.find_element(By.CSS_SELECTOR, "#clear_searchfilter > span").click()
        
        try:
            assert(driver.find_element(By.CSS_SELECTOR, "#chk-not-refered").is_selected() == False)
        except:
            testResult = False
            Result_msg += "#1 "

        # SearchFilter_Clear 결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2642, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2642, testPlanID, buildName, 'p', "SearchFilter_Clear Test Passed")

        # SearchFilter_SplitBar
        testResult = True
        Result_msg = "failed at "
        print("ITR-174: Home > Search Filter > Split Bar")

        driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").click()
        time.sleep(0.25)
        if driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").value_of_css_property("transform") != "matrix(-1.83697e-16, -1, 1, -1.83697e-16, 0, 0)":
            testResult = False
            Result_msg += "#1 "

        driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").click()
        WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search-job-start-date")))
        if driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").value_of_css_property("transform") != "matrix(6.12323e-17, 1, -1, 6.12323e-17, 0, 0)":
            testResult = False
            Result_msg += "#1 "

        # SearchFilter_SplitBar 결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2645, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2645, testPlanID, buildName, 'p', "SearchFilter_SplitBar Test Passed")

    def SearchFilter_ScheduleDate():
        testResult = True
        Result_msg = "failed at "
        print("ITR-166: Home > Search Filter > Schedule Date")

        ReFresh()

        # filter hide check
        if driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").value_of_css_property("transform") != "matrix(6.12323e-17, 1, -1, 6.12323e-17, 0, 0)":
            driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").click()

        Result_msg += WORKLIST.SearchFilter_Date("#search-schedule-job-start", "#search-schedule-job-end")
        if Result_msg != "failed at ":
            testResult = False

        # SearchFilter_ScheduleDate결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2617, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2617, testPlanID, buildName, 'p', "SearchFilter_ScheduleDate Test Passed")

    def SearchFilter_Shortcut():
        testResult = True
        Result_msg = "failed at "
        print("ITR-175: Home > Search Filter > Short cut")

        ReFresh()

        # filter hide check
        if driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").value_of_css_property("transform") != "matrix(6.12323e-17, 1, -1, 6.12323e-17, 0, 0)":
            driver.find_element(By.CSS_SELECTOR, "#search_box_collapse_icon").click()

        # choice modality for search
        wk_index_num = WORKLIST.SearchFilter_Etc_setting("9","Mod") ##
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)['data']
        choice = ""
        for n in data:
            if n["Modality"] != None: ##
                choice = n["Modality"] ##
                break

        # Short cut click #1
        element = driver.find_element(By.CSS_SELECTOR, "#searchfilter_card > div.header > ul > li > a > i")
        driver.execute_script("arguments[0].click();", element)
        try:
            time.sleep(0.25)
            driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/section/aside/div/div/div[1]/div[1]/div/input").send_keys("asdfxcdf1")
        except:
            testResult = False
            Result_msg += "#1 "

        if testResult == True:
            # Save, Click #2 & 10
            del driver.requests

            driver.find_element(By.CSS_SELECTOR, "#search-job-modality").send_keys(choice)
            driver.find_element(By.CSS_SELECTOR, "#search_wizard_save > span").click()
            time.sleep(0.25)

            request = driver.wait_for_request('.*/GetSearchWizard')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            save_num = 0
            save_check = False
            for n in data:
                save_num += 1
                if "asdfxcdf1" == n["Title"]:
                    save_check = True
                    break

            del driver.requests

            driver.find_element(By.CSS_SELECTOR, "#settings > div > div:nth-child(1) > ul > li:nth-child("+str(save_num+1)+") > div > span").click()
            time.sleep(0.25)

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
                        if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(wk_index_num)+"]").text != choice:
                            testResult = False
                            break
                    if(testResult != True or a == total):
                        break
                    element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(0.3)
            else:
                for a in range(1, total+1):
                    if a == total:
                        for b in range(1, last_page_num+1):
                            if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(wk_index_num)+"]").text != choice:
                                testResult = False
                                break
                    if a == total:
                        break
                    for b in range(1, page_len+1):
                        if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(wk_index_num)+"]").text != choice:
                            testResult = False
                            break
                    if(testResult != True):
                        break
                    element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(0.3)
            try:
                assert(save_check == True and 
                       testResult == True and
                       driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > span").text == "Requested" and
                       driver.find_element(By.CSS_SELECTOR, "#chk-not-refered").is_selected() == False)
            except:
                testResult = False
                Result_msg += "#2 #10 "

            # Clear #9
            element = driver.find_element(By.CSS_SELECTOR, "#searchfilter_card > div.header > ul > li > a > i")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.25)
            element = driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/section/aside/div/div/div[1]/ul/li[1]/div/span").click()
            time.sleep(0.25)
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#search-job-modality").get_property("value") == "")
            except:
                testResult = False
                Result_msg += "#9 "

            # institution Save #3
            # first institution click
            insti_name = (driver.find_element(By.CSS_SELECTOR, "#hospital_list > button:nth-child(1)").text).split('\n')[0]
            driver.find_element(By.CSS_SELECTOR, "#hospital_list > button:nth-child(1)").click()
            time.sleep(0.5)
            element = driver.find_element(By.CSS_SELECTOR, "#searchfilter_card > div.header > ul > li > a > i")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "#settings > div > div:nth-child(1) > div.col-lg-12 > label").click()
            driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/section/aside/div/div/div[1]/div[1]/div/input").send_keys("asdfxcdf2")

            del driver.requests

            driver.find_element(By.CSS_SELECTOR, "#search_wizard_save > span").click()
            time.sleep(0.25)
            request = driver.wait_for_request('.*/GetSearchWizard')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            save_check = False
            save_num = 0
            for n in data:
                save_num += 1
                if "asdfxcdf2" == n["Title"]:
                    save_check = True
                    break
            
            driver.find_element(By.CSS_SELECTOR, "#settings > div > div:nth-child(1) > ul > li:nth-child("+str(save_num+1)+") > div > span").click()
            time.sleep(0.25)
            try:
                assert(insti_name == driver.find_element(By.CSS_SELECTOR, "#current-hospital-name").text and 
                       save_check == True and
                       driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > span").text == "Requested" and
                       driver.find_element(By.CSS_SELECTOR, "#chk-not-refered").is_selected() == False)
            except:
                testResult = False
                Result_msg += "#3 "
            
            # Clear
            element = driver.find_element(By.CSS_SELECTOR, "#searchfilter_card > div.header > ul > li > a > i")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.25)
            element = driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/section/aside/div/div/div[1]/ul/li[1]/div/span").click()
            time.sleep(0.25)

            # duplicate title #4
            element = driver.find_element(By.CSS_SELECTOR, "#searchfilter_card > div.header > ul > li > a > i")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "#settings > div > div:nth-child(1) > div.col-lg-12 > label").click()
            driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/section/aside/div/div/div[1]/div[1]/div/input").send_keys("asdfxcdf2")
            
            del driver.requests

            driver.find_element(By.CSS_SELECTOR, "#search_wizard_save > span").click()
            time.sleep(0.25)
            request = driver.wait_for_request('.*/GetSearchWizard')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            save_num = 0
            for n in data:
                if "asdfxcdf2" == n["Title"]:
                    save_num += 1
                    if save_num == 2:
                        break
            if save_num != 2:
                testResult = False
                Result_msg += "#4 "

            # aleary existed click #5
            save_num = 0
            for n in data:
                save_num += 1
                if "asdfxcdf1" == n["Title"]:
                    break
            driver.find_element(By.CSS_SELECTOR, "#settings > div > div:nth-child(1) > ul > li:nth-child("+str(save_num+1)+") > div > span").click()
            time.sleep(0.25)
            element = driver.find_element(By.CSS_SELECTOR, "#searchfilter_card > div.header > ul > li > a > i")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.25)
            driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/section/aside/div/div/div[1]/div[1]/div/input").send_keys("_add")


            driver.find_element(By.CSS_SELECTOR, "#search_wizard_save > span").click()
            time.sleep(0.25)
            try:
                assert(driver.find_element(By.CSS_SELECTOR, "#modal_search_wizard > div > div > div.modal-header.modal-col-blue-grey > h4").text == "Search Wizard")
            except:
                testResult = False
                Result_msg += "#5 "

            # Search Wizard add & edit #6 & 7
            driver.find_element(By.CSS_SELECTOR, "#search_wizard_add").click()
            time.sleep(0.25)
            element = driver.find_element(By.CSS_SELECTOR, "#searchfilter_card > div.header > ul > li > a > i")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.25)

            driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/section/aside/div/div/div[1]/div[1]/div/input").send_keys("asdfxcdf1_edit")
            driver.find_element(By.CSS_SELECTOR, "#search_wizard_save > span").click()
            time.sleep(0.25)

            del driver.requests

            driver.find_element(By.CSS_SELECTOR, "#search_wizard_edit").click()
            time.sleep(0.25)

            request = driver.wait_for_request('.*/GetSearchWizard')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)

            element = driver.find_element(By.CSS_SELECTOR, "#searchfilter_card > div.header > ul > li > a > i")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.25)
            add_found = False
            edit_found = False
            for n in range(2, len(data)+2):
                if driver.find_element(By.CSS_SELECTOR, "#settings > div > div:nth-child(1) > ul > li:nth-child("+str(n)+") > div > span").text == "asdfxcdf1_add":
                    add_found = True
                elif driver.find_element(By.CSS_SELECTOR, "#settings > div > div:nth-child(1) > ul > li:nth-child("+str(n)+") > div > span").text == "asdfxcdf1_edit":
                    # 12 & 13
                    found_num = n
                    edit_found = True
                elif add_found == True and edit_found == True:
                    break

            if add_found == False:
                testResult = False
                Result_msg += "#6 "
            if edit_found == False:
                testResult = False
                Result_msg += "#7 "

            # Search Wizard close #8
            driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/section/aside/div/div/div[1]/div[1]/div/input").clear()
            driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/section/aside/div/div/div[1]/div[1]/div/input").send_keys("asdfxcdf1_close")
            driver.find_element(By.CSS_SELECTOR, "#search_wizard_save > span").click()
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "#search_wizard_close").click()
            time.sleep(0.25)
            element = driver.find_element(By.CSS_SELECTOR, "#searchfilter_card > div.header > ul > li > a > i")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.25)
            close_found = False
            for n in range(2, len(data)+2):
                if driver.find_element(By.CSS_SELECTOR, "#settings > div > div:nth-child(1) > ul > li:nth-child("+str(n)+") > div > span").text == "asdfxcdf1_close":
                    close_found = True
                    break
            if close_found == True:
                testResult = False
                Result_msg += "#8 "

            # mouse over #12 & 13
            element = driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/section/aside/div/div/div[1]/ul/li["+str(found_num)+"]")
            webdriver.ActionChains(driver).move_to_element(element).perform()
            time.sleep(0.25)
            context = element.get_property("outerHTML")
            if "aria-describedby" not in context:
                testResult = False
                Result_msg += "#12 "

            element_tmp = driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/section/aside/div/div/div[1]/ul/li["+str(found_num-1)+"]")
            webdriver.ActionChains(driver).move_to_element(element_tmp).perform()
            time.sleep(0.1)
            context = element.get_property("outerHTML")
            if "aria-describedby" in context:
                testResult = False
                Result_msg += "#13 "

            # - #11 
            repeat = 4
            while(1):
                request = driver.wait_for_request('.*/GetSearchWizard')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)

                for n in range(2, (len(data)+2)):
                    target = driver.find_element(By.CSS_SELECTOR, "#settings > div > div:nth-child(1) > ul > li:nth-child("+str(n)+") > div > span").text
                    if  target == "asdfxcdf1_add" or target == "asdfxcdf1_edit" or target ==  "asdfxcdf2":
                        del driver.requests
                        repeat -= 1
                        driver.find_element(By.CSS_SELECTOR, "#settings > div > div:nth-child(1) > ul > li:nth-child("+str(n)+") > span > button > i").click()
                        time.sleep(0.1)
                        break

                if repeat == 0:
                    break

            request = driver.wait_for_request('.*/GetSearchWizard')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            for n in range(2, len(data)+2):
                    if driver.find_element(By.CSS_SELECTOR, "#settings > div > div:nth-child(1) > ul > li:nth-child("+str(n)+") > div > span").text == ("asdfxcdf1_add" or "asdfxcdf1_edit" or "asdfxcdf2"):
                        testResult = False
                        Result_msg += "#14 "
                        break

        # SearchFilter_Shortcut결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2649, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2649, testPlanID, buildName, 'p', "SearchFilter_Shortcut Test Passed")

    def Columns():
        testResult = True
        Result_msg = "failed at "
        print("ITR-154: Home > Columns")

        ReFresh()

        # option #1 
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(4) > label")))
        try:
            assert(driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-header.modal-col-green > h4").text == "Column Show/Hide")
        except:
            testResult = False
            Result_msg += "#1 "

        # check/uncheck apply, cancel #2 & 3
        # 2 - on 
        orgin = False
        found = False
        if driver.find_element(By.CSS_SELECTOR, "#chk-column-32").is_selected() == False:
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(26) > label").click()
        else:
            orgin = True
        # showing wk column num
        show_list_num = 1
        for n in range (1,33):
            if driver.find_element(By.CSS_SELECTOR, "#chk-column-"+str(n)).is_selected() == True:
                show_list_num += 1
        # apply
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()
        time.sleep(0.5)
        # find
        for n in range (2,show_list_num+1):
            if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[1]/div/table/thead/tr/th["+str(n)+"]").text == "Emer Modifier":
                found = True
                break
        if found == False:
            testResult = False
            Result_msg += "#2 "
        # 3 - off cancel
        found = False
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(4) > label")))
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(26) > label").click()
        # cancel
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-close").click()
        time.sleep(0.5)
        # find
        for n in range (2,show_list_num+1):
            if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[1]/div/table/thead/tr/th["+str(n)+"]").text == "Emer Modifier":
                found = True
                break
        if found == False:
            testResult = False
            Result_msg += "#3 "
        # 2 - off
        found = False
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(4) > label")))
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(26) > label").click()
        # showing wk column num
        show_list_num = 1
        for n in range (1,33):
            if driver.find_element(By.CSS_SELECTOR, "#chk-column-"+str(n)).is_selected() == True:
                show_list_num += 1
        # apply
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()
        time.sleep(0.5)
        # find
        for n in range (2,show_list_num+1):
            if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[1]/div/table/thead/tr/th["+str(n)+"]").text == "Emer Modifier":
                found = True
                break
        if found == True:
            testResult = False
            Result_msg += "#2 "

        if orgin == True:
            driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(4) > label")))
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(26) > label").click()
            driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()

        # Reset #4
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(4) > label")))
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-reset").click()
        time.sleep(0.1)
        #E, R, Job Report, Job Status, Patient Name, Upload Date, Modality, Patient ID, Patient Loc
        origin = ["E", "R", "Job Report", "Job Status", "Patient Name", "Upload Date", "Modality", "Patient ID", "Patient Loc"]
        confirm_origin = []
        for n in range (1,33):
            if driver.find_element(By.CSS_SELECTOR, "#chk-column-"+str(n)).is_selected() == True:
                # n = 3 > check box ?
                if(n!=3):
                    confirm_origin.append(driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child("+str(n)+") > label").get_property("textContent"))
        origin.sort()
        confirm_origin.sort()

        driver.find_element(By.CSS_SELECTOR, "#setting-columns-close").click()
        try:
            assert(origin == confirm_origin)
        except:
            testResult = False
            Result_msg += "#4 "

        # AI information on, off #5 & 6
        # Setting + User profile + waiting접속
        TOPMENU.Profile_Worklist_inUserProfile()
        #value_of_css_property("background-color")
        # off - rgba(129, 129, 129, 1)
        # on - rgba(255, 87, 34, 0.5)
        # 5 - on
        ai_origin = True
        # if off > on
        if driver.find_element(By.CSS_SELECTOR, "#ai_setting_section > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span").value_of_css_property("background-color") == "rgba(129, 129, 129, 1)":
            ai_origin = False
            element = driver.find_element(By.CSS_SELECTOR, "#ai_setting_section > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span")
            driver.execute_script("arguments[0].click();", element)
            # save
            driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.1)
        # home
        driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[1]/a").click()
        driver.implicitly_wait(5)
        # option
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(4) > label")))
        try:
            assert(driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div.row.aiainfo_field_box > div:nth-child(1)").text == "AI Information")
        except:
            testResult = False
            Result_msg += "#5 "
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-close").click()
        time.sleep(0.1)

        # 6 - off
        # Setting + User profile + waiting접속
        TOPMENU.Profile_Worklist_inUserProfile()
        # off 
        element = driver.find_element(By.CSS_SELECTOR, "#ai_setting_section > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span")
        driver.execute_script("arguments[0].click();", element)
        # save
        driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.1)
        # home
        driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[1]/a").click()
        driver.implicitly_wait(5)
        # option
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(4) > label")))
        try:
            assert(driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div.row.aiainfo_field_box > div:nth-child(1)").text == "")
        except:
            testResult = False
            Result_msg += "#6 "
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-close").click()
        time.sleep(0.1)

        if ai_origin == True:
            # Setting + User profile + waiting접속
            TOPMENU.Profile_Worklist_inUserProfile()
            element = driver.find_element(By.CSS_SELECTOR, "#ai_setting_section > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span")
            driver.execute_script("arguments[0].click();", element)
            # save
            driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.1)
            # home
            driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[1]/a").click()
            driver.implicitly_wait(5)

        # Columns결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2528, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2528, testPlanID, buildName, 'p', "Columns Test Passed")

    def option_alloff_before():
        # Setting + User profile + waiting접속
        TOPMENU.Profile_Worklist_inUserProfile()

        # off - rgba(129, 129, 129, 1)
        # on - rgba(255, 87, 34, 0.5)
        ai_origin = True
        # if off > on
        if driver.find_element(By.CSS_SELECTOR, "#ai_setting_section > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span").value_of_css_property("background-color") == "rgba(129, 129, 129, 1)":
            ai_origin = False
            element = driver.find_element(By.CSS_SELECTOR, "#ai_setting_section > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span")
            driver.execute_script("arguments[0].click();", element)
            # save
            driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.5)
        # home
        driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[1]/a").click()
        driver.implicitly_wait(5)
        # option
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(4) > label")))

        # origin filter check and set off
        origin_filter = []
        for n in range (1,26):
            if driver.find_element(By.CSS_SELECTOR, "#chk-column-"+str(n)).is_selected() == True:
                if n!=3:
                    origin_filter.append(n)
                    driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child("+str(n)+") > label").click()
        for n in range (26,32):
            if driver.find_element(By.CSS_SELECTOR, "#chk-column-"+str(n)).is_selected() == True:
                origin_filter.append(n)
                driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div.row.aiainfo_field_box > div.setting-column > ul > li:nth-child("+str(n-25)+") > label").click()
        if driver.find_element(By.CSS_SELECTOR, "#chk-column-32").is_selected() == True:
            origin_filter.append(32)
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(26) > label").click()

        context = [ai_origin, origin_filter]
        return context

    def option_alloff_after(ai_origin, origin_filter):
        if ai_origin == False:
            # Setting + User profile + waiting접속
            TOPMENU.Profile_Worklist_inUserProfile()
            element = driver.find_element(By.CSS_SELECTOR, "#ai_setting_section > div > div > div > div > div.col-lg-7.col-md-7.col-sm-7 > div > div > label > span")
            driver.execute_script("arguments[0].click();", element)
            # save
            driver.find_element(By.CSS_SELECTOR, "#setting_confirm_btn").click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.5)

        # home
        driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[1]/a").click()
        driver.implicitly_wait(5)
        # option
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(4) > label")))
        for n in range (1,26):
            if driver.find_element(By.CSS_SELECTOR, "#chk-column-"+str(n)).is_selected() == True:
                if n!=3:
                    element = driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child("+str(n)+") > label")
                    driver.execute_script("arguments[0].click();", element)
        if ai_origin==True:
            for n in range (26,32):
                if driver.find_element(By.CSS_SELECTOR, "#chk-column-"+str(n)).is_selected() == True:
                    driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div.row.aiainfo_field_box > div.setting-column > ul > li:nth-child("+str(n-25)+") > label").click()
        if driver.find_element(By.CSS_SELECTOR, "#chk-column-32").is_selected() == True:
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(26) > label").click()
        
        for n in range(1, 26):
            if origin_filter:
                if n == origin_filter[0]:
                    origin_filter.pop(0)
                    driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child("+str(n)+") > label").click()
            else:
                break
        if ai_origin==True:
            for n in range (26,32):
                if origin_filter:
                    if n == origin_filter[0]:
                        origin_filter.pop(0)
                        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div.row.aiainfo_field_box > div.setting-column > ul > li:nth-child("+str(n-25)+") > label").click()
                else:
                    break
        if origin_filter:
            if origin_filter[0] == 32:
                driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(26) > label").click()
        # apply
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply#setting-columns-apply").click()
        time.sleep(0.5)

    def Sortby():
        testResult = True
        Result_msg = "failed at "
        print("ITR-156: Home > Sort by")

        ReFresh()

        context = WORKLIST.option_alloff_before()
        ai_origin = context[0]
        origin_filter = context[1]
        
        # set filter
        # E(Job Priority) 1
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(1) > label").click()
        # Upload Date 6
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(6) > label").click()
        # Patient Name 7 
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(7) > label").click()
        # Patient ID 8
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(8) > label").click()
        # Modality 9
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(9) > label").click()
        # Study Date 14
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(14) > label").click()
        # Job Date 15
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(15) > label").click()
        # Bodypart 16
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(16) > label").click()
        # Department 19
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(19) > label").click()
        # Study Desc 20
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(20) > label").click()
        # Schedule Date 21
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(21) > label").click()
        # AI Vendor 1 
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div.row.aiainfo_field_box > div.setting-column > ul > li:nth-child(1) > label").click()
        # AI Complex Score 2
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div.row.aiainfo_field_box > div.setting-column > ul > li:nth-child(2) > label").click()
        # AI Disease Name 3
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div.row.aiainfo_field_box > div.setting-column > ul > li:nth-child(3) > label").click()
        # AI Finding Cnt 4
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div.row.aiainfo_field_box > div.setting-column > ul > li:nth-child(4) > label").click()
        # AI Probability 5
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div.row.aiainfo_field_box > div.setting-column > ul > li:nth-child(5) > label").click()
        # AI Service 6
        driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div.row.aiainfo_field_box > div.setting-column > ul > li:nth-child(6) > label").click()
        # apply
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply#setting-columns-apply").click()
        time.sleep(0.5)

        for n in range (2, 19):
            element = driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[1]/div/table/thead/tr/th["+str(n)+"]")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.75)
            try:
                assert(element.get_property("ariaSort")!=None)
            except:
                testResult = False
                Result_msg += "#1 "
                break

        if driver.execute_script("return window.getComputedStyle(document.querySelector('.table.dataTable thead .sorting_asc'),':after').getPropertyValue('color')") != "rgb(173, 255, 47)":
            testResult = False
            Result_msg += "#1 "

        WORKLIST.option_alloff_after(ai_origin, origin_filter)

        # Sortby결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2542, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2542, testPlanID, buildName, 'p', "Sortby Test Passed")

    def option_findposition(target):
        for n in range (2,33):
            if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[1]/div/table/thead/tr/th["+str(n)+"]").text == target:
                return n
        return 0

    def Work_list():
        testResult = True
        Result_msg = "failed at "
        print("ITR-157: Home > Worklist")

        ReFresh()

        # column drop #1
        WORKLIST.option_alloff_before()
        for n in range (1,6):
            if n != 3:
                driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child("+str(n)+") > label").click()
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()
        time.sleep(3)
        source = driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[1]/div/table/thead/tr/th[3]")
        source_context = source.get_property("textContent")
        target = driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[1]/div/table/thead/tr/th[1]")
        #webdriver.ActionChains(driver).drag_and_drop(source ,target).perform()
        webdriver.ActionChains(driver).move_to_element(source).perform()
        webdriver.ActionChains(driver).move_by_offset(-5, 0).perform()
        webdriver.ActionChains(driver).click_and_hold(None).perform()
        webdriver.ActionChains(driver).move_to_element(target).perform()
        webdriver.ActionChains(driver).move_by_offset(-25, 0).perform()
        webdriver.ActionChains(driver).release(None).perform()
        time.sleep(3)
        after_context = driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[1]/div/table/thead/tr/th[2]").get_property("textContent")
        try:
            assert(source_context == after_context)
        except:
            testResult = False
            Result_msg += "#1 "

        ## right click #2 보류
        #source = driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[1]/div/table/thead/tr/th[2]")
        #move_p = (float(source.value_of_css_property("width").split("px")[0])/2)
        #webdriver.ActionChains(driver).move_to_element(source).perform()
        #webdriver.ActionChains(driver).move_by_offset(move_p, 0).perform()
        #webdriver.ActionChains(driver).context_click(None).perform()
        #time.sleep(3)
        #after = source.value_of_css_property("width")

        # check #3 ~ 끝까지
        context = WORKLIST.option_alloff_before()
        ai_origin=context[0]
        origin_filter=context[1]

        del driver.requests

        # all on
        for n in range (1,26):
            if n!=3 and n!=5:
                element = driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child("+str(n)+") > label")
                driver.execute_script("arguments[0].click();", element)
        for n in range (26,32):
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div.row.aiainfo_field_box > div.setting-column > ul > li:nth-child("+str(n-25)+") > label").click()
        #driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(26) > label").click()
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()
        time.sleep(0.75)

        # find position
        position = []
        position.append(WORKLIST.option_findposition("E"))
        position.append(WORKLIST.option_findposition("R"))
        position.append(WORKLIST.option_findposition("Job Status"))
        position.append(WORKLIST.option_findposition("P.Name"))
        position.append(WORKLIST.option_findposition("P.ID"))
        position.append(WORKLIST.option_findposition("Mod"))
        position.append(WORKLIST.option_findposition("Upload Date"))
        position.append(WORKLIST.option_findposition("Loc"))
        position.append(WORKLIST.option_findposition("Reference Files"))
        position.append(WORKLIST.option_findposition("Gender/Age"))
        position.append(WORKLIST.option_findposition("Department"))
        position.append(WORKLIST.option_findposition("Schedule"))
        position.append(WORKLIST.option_findposition("OCS"))
        position.append(WORKLIST.option_findposition("Request Name"))
        position.append(WORKLIST.option_findposition("I.CNT"))
        position.append(WORKLIST.option_findposition("Hospital"))
        position.append(WORKLIST.option_findposition("Study Date"))
        position.append(WORKLIST.option_findposition("D-Time"))
        position.append(WORKLIST.option_findposition("Bodypart"))
        position.append(WORKLIST.option_findposition("Job Date"))
        position.append(WORKLIST.option_findposition("Request Code"))
        position.append(WORKLIST.option_findposition("Study Desc"))
        position.append(WORKLIST.option_findposition("AI Vendor"))
        position.append(WORKLIST.option_findposition("AI Complex Score"))
        position.append(WORKLIST.option_findposition("AI DiseaseNM"))
        position.append(WORKLIST.option_findposition("AI FindingCnt"))
        position.append(WORKLIST.option_findposition("AI Probability"))
        position.append(WORKLIST.option_findposition("AI Service"))

        # ReferenceFileCount / OCSReport OCSReportFilePath
        wk_list = ["EmergencyDateString", "ReferDisplay", "JobStatus", "PatientNameMask", "PatientID", "Modality", "UploadedDTTMString", "PatientLocation", 
                   "ReferenceFileCount", "PatientSexAndAge", "Department", "ScheduledDate", "OCSReport", "RequestName", "ImageCount", "Hospital", 
                   "StudyDateDTTMString", "DTime", "Bodypart", "JobDateDTTMString", "RequestCode", "StudyDesc", "AIInfoVendor", 
                   "AIInfoComplexScore", "AIInfoDiseaseNm", "AIInfoFindingCnt", "AIInfoProbability", "AIInfoService"]

        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        #page_len = int(json.loads(body)['Length'])
        # total page
        #total = math.ceil(int(json.loads(body)['recordsFiltered']) / page_len)
        
        #for a in range(0, total):
        for b in range(0, len(data)):
                for c in range(0, 28):
                    #0, 1, 2, 11
                    # Emergencey      JobPriority > E or N  / EmergencyDateString Data or ""  
                    if c == 0:
                        if data[b]["JobPriority"] == "E":
                            try:
                                assert(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]/i").text == "priority_high")
                            except:
                                testResult = False
                                Result_msg += "#3 "
                        if data[b][wk_list[c]] != "":
                            try:
                                assert(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]/div").text == data[b][wk_list[c]])
                            except:
                                testResult = False
                                Result_msg += "#3 "
                    # Refer     ReferDisplay
                    elif c == 1:
                        try:
                            assert(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]/span/label").text == data[b][wk_list[c]])
                        except:
                            testResult = False
                            Result_msg += "#4 #5 "
                    # JobStatus     JobStatus
                    elif c == 2:
                        try:
                            assert(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]/span/label").text == data[b][wk_list[c]])
                        except:
                            testResult = False
                            Result_msg += "#6 "
                    # ReferenceFile     ReferenceFileCount
                    elif c == 8:
                        pass
                    #elif c == 8:
                    #    if data[b][wk_list[c]] != 0:
                    #        try:
                    #            assert(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]/span").text == "description")
                    #        except:
                    #            testResult = False
                    #            Result_msg += "#12 "
                    # Schedule      ScheduledDate
                    elif c == 11:
                        try:
                            assert(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]/span").text == data[b][wk_list[c]])
                        except:
                            testResult = False
                            Result_msg += "#15 "
                    # OCS       OCSReport
                    elif c == 12:
                        if data[b][wk_list[c]] == "T":
                            try:
                                driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]/div/i").click()
                                time.sleep(1)
                                driver.switch_to.window(driver.window_handles[1])
                                if (driver.find_element(By.CSS_SELECTOR, "#ocs-report-view-institution-name").text != data[b]["Hospital"] and
                                    data[b]["PatientName"] not in driver.find_element(By.CSS_SELECTOR, "#ocs-report-view-patient-name-gender-age").text and 
                                    data[b]["PatientSexAndAge"] not in driver.find_element(By.CSS_SELECTOR, "#ocs-report-view-patient-name-gender-age").text):
                                    testResult = False
                                    Result_msg += "#16 "
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])
                                assert(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]/div/i").text == "receipt")
                            except:
                                testResult = False
                                Result_msg += "#16 "
                    # AIInfoProbability
                    elif c == 26:
                        try:
                            assert(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]").text == str(data[b][wk_list[c]])+"%" or
                                   (driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]").text == "" and data[b][wk_list[c]] == 0.0))
                        except:
                            testResult = False
                            Result_msg += "#30 "
                    else:
                        if c==6:
                            try:
                                assert(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]").text == str((data[b][wk_list[c]])[:-1]) or
                                    (driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]").text == "" and data[b][wk_list[c]] == None) or
                                    (driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]").text == "" and data[b][wk_list[c]] == 0))
                            except:
                                testResult = False
                                Result_msg += ("#"+str(c+4)+" ")
                        else:
                            try:
                                assert(driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]").text == str(data[b][wk_list[c]]) or
                                    (driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]").text == "" and data[b][wk_list[c]] == None) or
                                    (driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[c])+"]").text == "" and data[b][wk_list[c]] == 0))
                            except:
                                testResult = False
                                Result_msg += ("#"+str(c+4)+" ")
            ##next page
            #if a+1 != total:
            #    del driver.requests

            #    element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
            #    driver.execute_script("arguments[0].click();", element)
            #    time.sleep(0.3)

            #    request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            #    body = request.response.body.decode('utf-8')
            #    data = json.loads(body)["data"]

        # Reference Files #12 c=8
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title").click()
        driver.implicitly_wait(5)
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        page_len = int(json.loads(body)['Length'])
        # total page
        total = math.ceil(int(json.loads(body)['recordsFiltered']) / page_len)
        ref_max = 0
        for a in range(0, total):
            for b in range(0, len(data)):
                if data[b][wk_list[8]] != 0:
                    ref_max += 1
                    del driver.requests
                    driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position[8])+"]/span").click()

                    if data[b][wk_list[8]] == 1:
                        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#reference-files-close")))
                        request = driver.wait_for_request('.*/GetReferenceFileList.*')
                        body = request.response.body.decode('utf-8')
                        data = json.loads(body)["data"]
                        try:
                            assert(driver.find_element(By.CSS_SELECTOR, "#reference-file-path-list > tbody > tr > td.reference-files-iframe.reference-file.align-center").text == data[0]["ReferenceFileName"])
                        except:
                            testResult = False
                            Result_msg += "#12 "
                    else:
                        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#reference-file-View-close")))
                        driver.find_element(By.CSS_SELECTOR, "#reference-file-View-close").click()
                        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#reference-files-close")))
                        request = driver.wait_for_request('.*/GetReferenceFileList.*')
                        body = request.response.body.decode('utf-8')
                        data = json.loads(body)["data"]
                        try:
                            count = 0
                            for n in data:
                                count += 1
                                assert(driver.find_element(By.CSS_SELECTOR, "#reference-file-path-list > tbody > tr:nth-child("+str(count)+") > td.reference-files-iframe.reference-file.align-center").text == n["ReferenceFileName"])
                        except:
                            testResult = False
                            Result_msg += "#12 "
            #next page
            if ref_max == 2:
                break
            if a+1 != total:
                del driver.requests

                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.3)

                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

        WORKLIST.option_alloff_after(ai_origin, origin_filter)

        # Work_list결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2545, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2545, testPlanID, buildName, 'p', "Work_list Test Passed")

    def JobReport():
        testResult = True
        Result_msg = "failed at "
        print("ITR-176: Home > Job Report > Job Report")

        ReFresh()

        driver.find_element(By.CSS_SELECTOR, "#setting_columns > i").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting-columns-apply")))
        # on jr
        jr_origin = True
        if driver.find_element(By.CSS_SELECTOR, "#chk-column-5").is_selected() == False:
            jr_origin = False
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(5) > label").click()

        # on js
        js_origin = True
        if driver.find_element(By.CSS_SELECTOR, "#chk-column-4").is_selected() == False:
            js_origin = False
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(4) > label").click()
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()
        time.sleep(0.3)

        js_position = WORKLIST.option_findposition("Job Status")
        jr_position = WORKLIST.option_findposition("Job Report")

        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        page_len = int(json.loads(body)['Length'])
        # total page
        total = math.ceil(int(json.loads(body)['recordsFiltered']) / page_len)
        # 한 페이지만 확인
        for a in range(1, 11):
            del driver.requests
            driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child("+str(a)+")").click()
            driver.find_element(By.CSS_SELECTOR, "#search_current_job > i").click()
            time.sleep(1)
            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for b in range(0, len(data)):
                js = driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(js_position)+"]/span/label")
                jr = driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(jr_position)+"]/span/label")

                jr.click()
                if js.text == "Canceled" or js.text == "Canceled2":
                    try:
                        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
                        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
                        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                        assert(msg == "해당 의뢰건은 취소되었습니다.")
                    except:
                        testResult = False
                        Result_msg += "#2 "
                elif js.text == "DiscardRequest" or js.text == "DiscardCompleted":
                    try:
                        driver.switch_to.window(driver.window_handles[1])
                        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
                        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                        driver.switch_to.window(driver.window_handles[0])
                    except:
                        testResult = False
                        Result_msg += "#3 "
                else:
                    try:
                        driver.switch_to.window(driver.window_handles[1])
                        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#job-report-view-send-btn")))
                        if (data[b]["PatientName"] in driver.find_element(By.CSS_SELECTOR, "#job-report-view-patient-name-sex-age").text and
                            str(data[b]["StudyDateDTTMString"].split(" ")[0]) == driver.find_elemnet(By.CSS_SELECTOR, "#job-report-view-study-dttm").text):
                            testResult = False
                            Result_msg += "#1 "
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    except:
                        testResult = False
                        Result_msg += "#1 "

        # JobReport결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2665, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2665, testPlanID, buildName, 'p', "JobReport Test Passed")

    def  JobReport_ReadingHistory():
        testResult = True
        Result_msg = "failed at "
        print("ITR-177: Home > Job Report > Reading History")

        ReFresh()
        time.sleep(0.3)

        del driver.requests
        time.sleep(1)

        # Cloud team
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > div > div > input[type=text]").send_keys(testHospital)
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        time.sleep(0.3)

        del driver.requests
        time.sleep(1)

        # set option
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting-columns-apply")))
        jr_origin = True
        if driver.find_element(By.CSS_SELECTOR, "#chk-column-5").is_selected() == False:
            jr_origin = False
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(5) > label").click()
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()
        time.sleep(0.5)
        position = WORKLIST.SearchFilter_Etc_setting("5", "Job Report")

        # find
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        remember_pid = None
        for a in range (0, total):
            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            time.sleep(0.3)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in data:
                driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(data.index(n) + 1)+") > td.th-check.align-center > label").click()
                request = driver.wait_for_request('.*/GetRelatedJobWorklist.*')
                time.sleep(0.3)
                body = request.response.body.decode('utf-8')
                related_data = json.loads(body)["data"]

                if len(related_data) >= 2:
                    for i in related_data:
                        if i["ReportText"] != "":
                            remember_pid = n["PatientID"]
                            break

                if remember_pid != None:
                    break

                del driver.requests
                time.sleep(1)

            if (remember_pid != None or
                a+1 == total):
                break

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

        del driver.requests
        time.sleep(1)

        ReFresh()
        time.sleep(0.5)

        del driver.requests
        time.sleep(1)

        # Cloud team
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > div > div > input[type=text]").send_keys(testHospital)
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        time.sleep(0.3)

        # paste #1
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search-job-pat-id")))
        driver.find_element(By.CSS_SELECTOR, "#search-job-pat-id").clear()
        driver.find_element(By.CSS_SELECTOR, "#search-job-pat-id").send_keys(remember_pid)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search_current_job")))
        driver.find_element(By.CSS_SELECTOR, "#search_current_job").click()
        driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        time.sleep(0.3)
        del driver.requests
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr/td["+str(position)+"]/span/label").click()
        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[1]/div[3]/div/div[2]/div[5]/div/div[1]/div[2]/div[2]/button[1]")))
        request = driver.wait_for_request('.*/GetJobReport.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["RelatedReportIncludePriorityStudyReport"]

        for n in data:
            if n["Conclusion"] != None and n["ReportTextLob"] != "":
                textlob = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div["+str(data.index(n)+1)+"]/div[2]/span[1]")
                con = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div["+str(data.index(n)+1)+"]/div[2]/span[2]")
            textlob.click()
            time.sleep(0.3)
            try:
                assert(textlob.text in driver.find_element(By.CSS_SELECTOR, "#job-report-view-report-text").get_property("value") and
                       con.text in driver.find_element(By.CSS_SELECTOR, "#job-report-view-conclusion").get_property("value"))
            except:
                testResult = False
                Result_msg += "#1 "
                break

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.find_element(By.CSS_SELECTOR, "#clear_searchfilter").click()

        # x-paste #2
        # userprofile 접속
        TOPMENU.Profile_Worklist_inUserProfile()
        driver.find_element(By.CSS_SELECTOR, "#report_profile_tab_link > a").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#report_modify_time")))
        re_rpt_day = math.trunc(int(driver.find_element(By.CSS_SELECTOR, "#report_modify_time").get_property("value")) / 24)
        # home
        element = driver.find_element(By.CSS_SELECTOR, "#right-sidebar-home")
        driver.execute_script("arguments[0].click();", element)
        # reported 
        del driver.requests
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(2)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        time.sleep(0.25)

        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        page_len = int(json.loads(body)['Length'])
        # total page
        total = math.ceil(int(json.loads(body)['recordsFiltered']) / page_len)
        check = False
        for a in range(1, total+1):
            for b in range(1, len(data)+1):
                del driver.requests
                if len(data) == 1:
                    driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr/td["+str(position)+"]/span/label").click()
                else:
                    driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b)+"]/td["+str(position)+"]/span/label").click()
                time.sleep(0.5)
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(0.5)
                for n in driver.requests:
                    if "/GetJobReport?jobKey" in n.url:
                        request_sub = n
                        break
                body_sub = request_sub.response.body.decode('utf-8')

                max_date_temp = (datetime.strptime(json.loads(body_sub)["ReportDTTMString"],'%Y-%m-%d %H:%M:%S') + 
                            timedelta(days=re_rpt_day)).strftime('%Y%m%d %H:%M:%S')
                max_date = datetime.strptime(max_date_temp, "%Y%m%d %H:%M:%S")
                current = datetime.today()
                sub = str(max_date - current)
                if '-' in sub:
                    data_sub = json.loads(body_sub)["RelatedReportIncludePriorityStudyReport"]

                    for n in range (1, len(data_sub)+1):
                        origin_rpt = driver.find_element(By.CSS_SELECTOR, "#job-report-view-report-text").get_property("value")
                        origin_con = driver.find_element(By.CSS_SELECTOR, "#job-report-view-conclusion").get_property("value")
                        if len(data_sub) == 1:
                            textlob = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div/div[2]/span[1]")
                        else:
                            textlob = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div["+str(n)+"]/div[2]/span[1]")
                        textlob.click()
                        time.sleep(0.1)
                        try:
                            check=True
                            assert(driver.find_element(By.CSS_SELECTOR, "#job-report-view-report-text").get_property("value") == origin_rpt and
                                driver.find_element(By.CSS_SELECTOR, "#job-report-view-conclusion").get_property("value") == origin_con)
                            break
                        except:
                            testResult = False
                            Result_msg += "#2 "
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                if check == True:
                    break
            if check == True:
                break
            if a != total:
                element= driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
                driver.execute_script("arguments[0].click();", element)

        # Send #3
        # refresh
        driver.find_element(By.CSS_SELECTOR, "#navbar_title > a.m-l-10.navbar-brand.m-l-10.itr-worklist-title").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#current-job-list_next > a")))

        del driver.requests
        time.sleep(1)

        # Cloud team
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > div > div > input[type=text]").send_keys(testHospital)
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        time.sleep(0.3)

        del driver.requests
        time.sleep(1)

        # find
        driver.find_element(By.CSS_SELECTOR, "#search-job-pat-id").clear()
        driver.find_element(By.CSS_SELECTOR, "#search-job-pat-id").send_keys(remember_pid)
        driver.find_element(By.CSS_SELECTOR, "#search_current_job > span").click()
        driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        time.sleep(0.3)
        del driver.requests
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr/td["+str(position)+"]/span/label").click()
        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[1]/div[3]/div/div[2]/div[5]/div/div[1]/div[2]/div[2]/button[1]")))
        request = driver.wait_for_request('.*/GetJobReport.*')
        time.sleep(0.3)

        # Report Send
        # report option off
        driver.find_element(By.CSS_SELECTOR, "#report_setting_btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal_report_settings_save")))
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div/div/div[2]/div[5]/div[2]/div/div[2]/div/label/input").is_selected() == True:
            driver.find_element(By.CSS_SELECTOR, "#modal_report_settings > div > div > div.modal-body > div:nth-child(5) > div.body > div > div.switch.panel-switch-btn > div > label > span").click()
        driver.find_element(By.CSS_SELECTOR, "#modal_report_settings_save").click()
        time.sleep(0.5)

        del driver.requests
        time.sleep(1)

        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[3]/div/div[2]/div[4]/div[2]/div/div/textarea").send_keys("rnd_Report")
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[3]/div/div[2]/div[4]/div[5]/div/div/textarea").send_keys("rnd_Conclusion")
        driver.find_element(By.CSS_SELECTOR, "#job-report-view-send-btn").click()
        
        driver.wait_for_request('.*/GetJobReport.*')
        time.sleep(0.3)
        for n in driver.requests:
            if "/GetJobReport?jobKey" in n.url:
                request = n
                break
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["RelatedReportIncludePriorityStudyReport"]
        check = False
        for n in data:
            if (n["Conclusion"] == "rnd_Conclusion" and n["ReportTextLob"] == "rnd_Report"):
                if (driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div["+str(data.index(n)+1)+"]/div[2]/span[1]").text == "rnd_Report" and
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div["+str(data.index(n)+1)+"]/div[2]/span[2]").text == "rnd_Conclusion"):
                    check=True
        if check == False:
            testResult = False
            Result_msg += "#3 "
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        if jr_origin == False:
            driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting-columns-apply")))
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(5) > label").click()
            driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()

        # JobReport_ReadingHistory결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2670, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2670, testPlanID, buildName, 'p', "JobReport_ReadingHistory Test Passed")

    #ND = 1 (Normal), 2 (Delay) / SC = 3 (Send), 4 (Send&Close)
    def JobReport_ReportSettings_Send(position, ND, SC):
        Result_msg = ""

        del driver.requests
        time.sleep(1)

        # open report for 3, 4
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(1)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job").click()
        time.sleep(1)
        request = driver.wait_for_request(".*/GetCurrentJobWorklist.*")
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        page_len = int(json.loads(body)['Length'])
        # total page
        total = math.ceil(int(json.loads(body)['recordsFiltered']) / page_len)
        check = False
        for a in range(1, total+1):
            driver.wait_for_request(".*/GetCurrentJobWorklist.*")
            time.sleep(0.3)

            for b in range(0, len(data)):
                if (driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position)+"]/span/label").get_property("textContent") == "Unreported"):
                    driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position)+"]/span/label").click()
                    time.sleep(0.5)
                    driver.switch_to.window(driver.window_handles[1])
                    try:
                        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[3]/div/div[2]/div[4]/div[2]/div/div/textarea").clear()
                        check = True
                        break
                    except:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
            if check == True:
                break

            del driver.requests
            time.sleep(1)

            element = driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a")
            driver.execute_script("arguments[0].click();", element)

        # Shortcut
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[3]/div/div[2]/div[4]/div[2]/div/div/textarea").clear()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[3]/div/div[2]/div[4]/div[5]/div/div/textarea").clear()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[3]/div/div[2]/div[4]/div[2]/div/div/textarea").send_keys("Shorcut_Test")
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[3]/div/div[2]/div[4]/div[5]/div/div/textarea").send_keys("Shorcut_Test")
        driver.find_element(By.CSS_SELECTOR, "#report_setting_btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal_report_settings_save")))
        # ND
        driver.find_element(By.CSS_SELECTOR, "#report-send-type-select").click()
        driver.find_element(By.CSS_SELECTOR, "#report-send-type-select > option:nth-child("+str(ND)+")").click()

        # send
        driver.find_element(By.CSS_SELECTOR, "#modal_report_settings > div > div > div.modal-body > div:nth-child(2) > div.body > div > div:nth-child("+str(SC)+") > label").click()
        driver.find_element(By.CSS_SELECTOR, "#modal_report_settings_save").click()
        time.sleep(1)

        del driver.requests
        time.sleep(1)

        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[3]/div/div[2]/div[4]/div[2]/div/div/textarea").send_keys(Keys.CONTROL + "S")

        if SC == 4:
            driver.switch_to.window(driver.window_handles[0])
            driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr["+str(b+1)+"]/td["+str(position)+"]/span/label").click()
            try:
                WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            except:
                pass
            time.sleep(0.5)
            driver.switch_to.window(driver.window_handles[1])
        
        driver.wait_for_request('.*/GetJobReport.*')
        time.sleep(0.3)
        for n in driver.requests:
            if "/GetJobReport?jobKey" in n.url:
                request = n
                break
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["RelatedReportIncludePriorityStudyReport"]

        check = False

        for n in data:
            if (n["Conclusion"] == "Shorcut_Test" and n["ReportTextLob"] == "Shorcut_Test"):
                if (driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div["+str(data.index(n)+1)+"]/div[2]/span[1]").text == "Shorcut_Test" and
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div["+str(data.index(n)+1)+"]/div[2]/span[2]").text == "Shorcut_Test"):
                    check=True
        if check == False:
            Result_msg += "#"+str(ND+2)+" "
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        #if SC == 3:
        #    for n in data:
        #        if (n["Conclusion"] == "Shorcut_Test" and n["ReportTextLob"] == "Shorcut_Test"):
        #            if (driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div["+str(data.index(n)+1)+"]/div[2]/span[1]").text == "Shorcut_Test" and
        #                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div["+str(data.index(n)+1)+"]/div[2]/span[2]").text == "Shorcut_Test"):
        #                check=True
        #    if check == False:
        #        Result_msg += "#"+str(ND+2)+" "
        #    driver.close()
        #    driver.switch_to.window(driver.window_handles[0])
        #elif SC == 4:
        #    for n in data:
        #        if (n["Conclusion"] == "Shorcut_Test" and n["ReportTextLob"] == "Shorcut_Test"):
        #            if (driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div["+str(data.index(n)+1)+"]/div[2]/span[1]").text == "Shorcut_Test" and
        #                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div["+str(data.index(n)+1)+"]/div[2]/span[2]").text == "Shorcut_Test"):
        #                check=True
        #    if check == True:
        #        Result_msg += "#"+str(ND+2)+" "
        #    driver.switch_to.window(driver.window_handles[0])

        return Result_msg


    def JobReport_ReportSettings():
        testResult = True
        Result_msg = "failed at "
        print("ITR-178: Home > Job Report > Report Settings")

        ReFresh()

        # set option (column)
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting-columns-apply")))
        jr_origin = True
        if driver.find_element(By.CSS_SELECTOR, "#chk-column-5").is_selected() == False:
            jr_origin = False
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(5) > label").click()
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()
        time.sleep(0.5)
        position = WORKLIST.SearchFilter_Etc_setting("5", "Job Report")

        del driver.requests
        time.sleep(1)

        # test hospital
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > div > div > input[type=text]").send_keys(testHospital)
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        time.sleep(0.3)

        del driver.requests
        time.sleep(1)

        # search
        driver.find_element(By.CSS_SELECTOR, "#search_box_body > div:nth-child(1) > div:nth-child(1)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_job_status_chosen > div > ul > li:nth-child(2)").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job").click()
        request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        remember_pid = None
        for a in range (0, total):
            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            time.sleep(0.3)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in data:
                driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(data.index(n) + 1)+") > td.th-check.align-center > label").click()
                request = driver.wait_for_request('.*/GetRelatedJobWorklist.*')
                time.sleep(0.3)
                body = request.response.body.decode('utf-8')
                related_data = json.loads(body)["data"]

                if len(related_data) >= 2:
                    for i in related_data:
                        if i["ReportText"] != "":
                            remember_pid = n["PatientID"]
                            break

                if remember_pid != None:
                    break

                del driver.requests
                time.sleep(1)

            if (remember_pid != None or
                a+1 == total):
                break

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

        driver.find_element(By.CSS_SELECTOR, "#search-job-pat-id").send_keys(remember_pid)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search_current_job")))
        driver.find_element(By.CSS_SELECTOR, "#search_current_job").click()
        driver.wait_for_request('.*/GetCurrentJobWorklist.*')
        time.sleep(0.3)
        driver.find_element(By.CSS_SELECTOR, "#search-job-pat-id").clear()

        # open report (exclude 3, 4, 7, 8)
        driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr[1]/td["+str(position)+"]/span/label").click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0.25)

        # report option #1
        driver.find_element(By.CSS_SELECTOR, "#report_setting_btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal_report_settings_save")))
        try:
            assert(driver.find_element(By.CSS_SELECTOR, "#modal_report_settings > div > div > div.modal-header.modal-col-blue-grey > h4").text == "Report Settings")
        except:
            testResult = False
            Result_msg += "#1 "

        # font size #2
        driver.find_element(By.CSS_SELECTOR, "#report-font-size-select-box").click()
        driver.find_element(By.CSS_SELECTOR, "#report-font-size-select-box > option:nth-child(8)").click()
        driver.find_element(By.CSS_SELECTOR, "#modal_report_settings_save").click()
        time.sleep(0.1)
        big = driver.find_element(By.CSS_SELECTOR, "#job-report-view-refer-comments").value_of_css_property("font-size")
        driver.find_element(By.CSS_SELECTOR, "#report_setting_btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal_report_settings_save")))
        driver.find_element(By.CSS_SELECTOR, "#report-font-size-select-box").click()
        driver.find_element(By.CSS_SELECTOR, "#report-font-size-select-box > option:nth-child(1)").click()
        driver.find_element(By.CSS_SELECTOR, "#modal_report_settings_save").click()
        time.sleep(0.1)
        small = driver.find_element(By.CSS_SELECTOR, "#job-report-view-refer-comments").value_of_css_property("font-size")
        try:
            assert(big == "16.5px" and small == "13px")
        except:
            testResult = False
            Result_msg += "#2 #11 "

        # +info (modality, study desc, bodypart, report id)#5
        driver.find_element(By.CSS_SELECTOR, "#report_setting_btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal_report_settings_save")))
        if driver.find_element(By.CSS_SELECTOR, "#reading-history-modality").is_selected() == False:
            driver.find_element(By.CSS_SELECTOR, "#modal_report_settings > div > div > div.modal-body > div:nth-child(3) > div.body > div > div:nth-child(1) > label").click()
        if driver.find_element(By.CSS_SELECTOR, "#reading-history-study-desc").is_selected() == False:
            driver.find_element(By.CSS_SELECTOR, "#modal_report_settings > div > div > div.modal-body > div:nth-child(3) > div.body > div > div:nth-child(2) > label").click()
        if driver.find_element(By.CSS_SELECTOR, "#reading-history-body-part").is_selected() == False:
            driver.find_element(By.CSS_SELECTOR, "#modal_report_settings > div > div > div.modal-body > div:nth-child(3) > div.body > div > div:nth-child(3) > label").click()
        if driver.find_element(By.CSS_SELECTOR, "#reading-history-reporter").is_selected() == False:
            driver.find_element(By.CSS_SELECTOR, "#modal_report_settings > div > div > div.modal-body > div:nth-child(3) > div.body > div > div:nth-child(4) > label").click()
        driver.find_element(By.CSS_SELECTOR, "#modal_report_settings_save").click()
        time.sleep(0.5)        
        try:            
            assert("Modality" in driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div/div[1]/div[2]").get_property("textContent") and
                   "Study Desc" in driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div/div[1]/div[3]").get_property("textContent") and
                   "Bodypart" in driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div/div[1]/div[4]").get_property("textContent") and
                   "Reporter" in driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]/div/div[2]/div/div/div[1]/div[5]").get_property("textContent") )
        except:
            testResult = False
            Result_msg += "#5 "

        # Button Position Top & Bottom #7
        driver.find_element(By.CSS_SELECTOR, "#report_setting_btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal_report_settings_save")))
        driver.find_element(By.CSS_SELECTOR ,"#normal-send-btn-position-select-box").click()
        driver.find_element(By.CSS_SELECTOR, "#normal-send-btn-position-select-box > option:nth-child(2)").click()
        driver.find_element(By.CSS_SELECTOR, "#modal_report_settings_save").click()
        time.sleep(1)
        try:
            assert(driver.find_element(By.CSS_SELECTOR, "#job-report-view-send-btn-alt-top").text == "Send")
        except:
            testResult = False
            Result_msg += "#7 "

        # Button Position Bottom, Cancel #6, 10
        driver.find_element(By.CSS_SELECTOR, "#report_setting_btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal_report_settings_save")))
        driver.find_element(By.CSS_SELECTOR ,"#normal-send-btn-position-select-box").click()
        driver.find_element(By.CSS_SELECTOR, "#normal-send-btn-position-select-box > option:nth-child(1)").click()
        driver.find_element(By.CSS_SELECTOR, "#modal_report_settings_close").click()
        try:
            assert(driver.find_element(By.CSS_SELECTOR, "#job-report-view-send-btn-alt-top").text == "Send")
        except:
            testResult = False
            Result_msg += "#11 "
        
        driver.find_element(By.CSS_SELECTOR, "#report_setting_btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal_report_settings_save")))
        driver.find_element(By.CSS_SELECTOR ,"#normal-send-btn-position-select-box").click()
        driver.find_element(By.CSS_SELECTOR, "#normal-send-btn-position-select-box > option:nth-child(1)").click()
        driver.find_element(By.CSS_SELECTOR, "#modal_report_settings_save").click()
        time.sleep(2)
        try:
            assert(driver.find_element(By.CSS_SELECTOR, "#job-report-view-send-btn-alt-top").text == "Send")
            testResult = False
            Result_msg += "#6 "
        except:
            pass
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Shortcut_Normal&Delay_Send&Close #3 4
        Result_msg += WORKLIST.JobReport_ReportSettings_Send(position,1,3)
        Result_msg += WORKLIST.JobReport_ReportSettings_Send(position,1,4)
        Result_msg += WORKLIST.JobReport_ReportSettings_Send(position,2,3)
        Result_msg += WORKLIST.JobReport_ReportSettings_Send(position,2,4)
        if Result_msg != "failed at ":
            testResult == False

        if jr_origin == False:
            driver.find_element(By.CSS_SELECTOR, "#setting_columns > span").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#setting-columns-apply")))
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(5) > label").click()
            driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()

        # JobReport_ReportSettings결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2675, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2675, testPlanID, buildName, 'p', "JobReport_ReportSettings Test Passed")

    def Related_Exam():
        testResult = True
        Result_msg = "failed at "
        print("ITR-158: Home > Related Exam List")

        ReFresh()

        # clear
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#clear_searchfilter").click()
        driver.find_element(By.CSS_SELECTOR, "#search_current_job").click()
        time.sleep(0.5)

        # Related_Exam Render check #1
        request = driver.wait_for_request('./GetCurrentJobWorklist.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        exam_column = ["Reporter", "JobStatus", "StudyDate", "Modality", "Bodypart", "ReportText", "Conclusion"]

        for n in range(1, len(data)+1):
            del driver.requests
            driver.find_element(By.CSS_SELECTOR, "#current-job-list > tbody > tr:nth-child("+str(n)+") > td.th-check.align-center > label").click()
            time.sleep(0.15)
            if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[3]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[1]").get_property("textContent") == "No matching records found":
                pass
            else:
                 request = driver.wait_for_request('./GetRelatedJobWorklist.*')
                 body = request.response.body.decode('utf-8')
                 data = json.loads(body)["data"]
                 for a in range (1, len(data)):
                     try:
                         for b in  range (2, 9):
                             assert ( str(data[a-1][exam_column[b-2]]) == driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[3]/div[1]/div[3]/div[2]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").text or 
                                     (data[a-1][exam_column[b-2]] == None and driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[3]/div[1]/div[3]/div[2]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").text == ""))
                     except:
                         testResult = False
                         Result_msg += "#1 "

        # Related_Exam결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2578, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2578, testPlanID, buildName, 'p', "Related_Exam Test Passed")

Login_List = [
    Login.Log_InOut,
    Login.Remember_me
    ]

normal_List = [
    #TopMenu_Main_List
    #TOPMENU.Badge,
    TOPMENU.Badge_Emergency,
    TOPMENU.Badge_Refer,
    TOPMENU.Badge_AutoRefer,
    TOPMENU.Badge_Schedule,
    TOPMENU.Badge_Today,

    TOPMENU.Home,
    TOPMENU.new_message,
    TOPMENU.Message,
    TOPMENU.View_More_Messages,
    TOPMENU.Setting,

    #TopMenu_Report_List
    TOPMENU.Report_Search_Filter,
    TOPMENU.Report_Add,
    TOPMENU.Report_Modify,
    TOPMENU.Report_delete,
        
    #TopMenu_Profile_List
    TOPMENU.Profile_Worklist,
    TOPMENU.Profile_Standard_Report,
        
    #WorkList_List
    WORKLIST.HospitalList,
    WORKLIST.SearchFilter_JobStatus,
    WORKLIST.SearchFilter_JobDate,
    WORKLIST.SearchFilter_Etc,
    WORKLIST.SearchFilter_ScheduleDate,
    WORKLIST.SearchFilter_Shortcut,
    WORKLIST.Columns,
    WORKLIST.Sortby,

    WORKLIST.Work_list,

    WORKLIST.JobReport,
    WORKLIST.JobReport_ReadingHistory,
    WORKLIST.JobReport_ReportSettings,

    WORKLIST.Related_Exam
    ]

def All_Scenario():
    start = time.time()
    failed_list = []

    for a in Login_List:
        try:
            print("(",str(Login_List.index(a)+1) + " / " + str(len(Login_List)),")", round(((Login_List.index(a)+1)*100/int(len(Login_List))),1),"%")
            run_time = time.time()
            a()
        except:
            print("Exception on " + str(a))
            driver.get(WorklistUrl)
            if a not in failed_list:
                failed_list.append(a)
            for i in range(0,3):
                try:
                    a()
                    failed_list.remove(a)
                    break
                except:
                    print("Retry Exception on " + str(a))
                    driver.get(WorklistUrl)
                    pass
        finally:
            print("Run Time:", round((int(time.time() - run_time)/60),2),"min\n")

    # 정상적인 계정으로 로그인
    signInOut.normal_login()

    for a in normal_List:
        try:
            print("(",str(normal_List.index(a)+1) + " / " + str(len(normal_List)),")", round(((normal_List.index(a)+1)*100/int(len(normal_List))),1),"%")
            run_time = time.time()
            a()
        except:
            print("Exception on " + str(a))
            driver.get(WorklistUrl)
            if a not in failed_list:
                failed_list.append(a)
            for i in range(0,3): 
                try:
                    a()
                    failed_list.remove(a)
                    break
                except:
                    print("Retry Exception on " + str(a))
                    driver.get(WorklistUrl)
                    pass
        finally:
            print("Run Time:", round((int(time.time() - run_time)/60),2),"min\n")

    print("Total Run Time:", round((int(time.time() - start)/60),2),"min")
    print("Failed List: ", failed_list)

All_Scenario()
