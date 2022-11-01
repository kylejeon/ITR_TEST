from types import NoneType
from testlink import TestlinkAPIClient, TestLinkHelper
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
# import requests
from seleniumwire import webdriver
# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import json
from selenium.webdriver.support.ui import Select
import math
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
import random
# import ITR_Admin_Common

# User: kyle
URL = 'http://testserver-win:81/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
DevKey = 'adcb86843d0c77e6e0c9950f80a143c0'
# testlink 초기화
tl_helper = TestLinkHelper()
# testlink = tl_helper.connect(TestlinkAPIClient) 
# testlink.__init__(URL, DevKey)
# testlink.checkDevKey()

# 브라우저 설정
# baseUrl = 'http://stagingadmin.onpacs.com'
baseUrl = 'http://vm-onpacs:8082'
# html = requests.get(baseUrl)
# soup = BeautifulSoup(html.text, 'html.parser')
# url = baseUrl + quote_plus(plusUrl)
driver = webdriver.Chrome()
driver.get(baseUrl)
# ITR_Admin_Common.close_popup()
# Notice 창 닫기
popup = driver.window_handles
while len(popup) != 1:
    driver.switch_to.window(popup[1])
    #driver.close()
    driver.find_element(By.ID, "notice_modal_cancel_week").click()
    popup = driver.window_handles
driver.switch_to.window(popup[0])
html = driver.page_source
soup = BeautifulSoup(html)
result_list = []

# TestPlanID = AutoTest 버전 테스트
testPlanID = 2996
buildName = 1

# 테스트 계정
adminID = 'testAdmin'
adminPW = 'Server123!@#'
subadmin = 'testSubadmin'
subadminPW = 'Server123!@#'

# 공통 변수
test_hospital = "Cloud Team"
today = datetime.now()
test_patient_id = "PI20200205003"
test_patient_name = "PN20200205003"
test_study_description = 'CHEST AP'
test_modality = 'CR'

class signInOut:
    def admin_sign_in():
        driver.find_element(By.ID, 'user-id').clear()
        driver.find_element(By.ID, 'user-id').send_keys('testAdmin')
        driver.find_element(By.ID, 'user-password').send_keys('Server123!@#')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)
    def admin_sign_out():
        driver.find_element(By.CSS_SELECTOR, '.pull-right > span').click()
    def subadmin_sign_in():
        driver.find_element(By.ID, 'user-id').clear()
        driver.find_element(By.ID, 'user-id').send_keys('testSubadmin')
        driver.find_element(By.ID, 'user-password').send_keys('Server123!@#')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)
    def subadmin_sign_out():
        driver.find_element(By.CSS_SELECTOR, '.pull-right > span').click()

class windowSize:
    driver.set_window_size(1920, 1080)

class Sign:
    def Sign_InOut():
        testResult = ''
        reason = list()       
        
        # user ID와 password를 입력하지 않고 sign in을 클릭한다
        signInOut.admin_sign_in('','')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        # This field is required.
        try:
            assert driver.find_element(By.ID, "user-id-error").text == "This field is required."
        except:
            testResult = 'failed'
            reason.append("Sign_InOut step 2 isn't valid")    
        
        # 잘못된 user ID를 입력하고 sign in을 클릭한다
        signInOut.admin_sign_in('administrator','Server123!@#')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        # User not found
        try:
            assert driver.find_element(By.CSS_SELECTOR, ".validation-summary-errors > ul > li").text == "User not found"
        except:
            testResult = 'failed'
            reason.append("Sign_InOut step 3 isn't valid")
        
        # password 미입력 하고 sign in을 클릭한다        
        signInOut.admin_sign_in('administrator',' ')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        # This field is required.
        try:
           assert driver.find_element(By.ID, "user-password-error").text == "This field is required."
        except:
            testResult = 'failed'
            reason.append("Sign_InOut step 3 isn't valid")
        
        # admin 유저가 아닌 계정으로 로그인 한다.        
        signInOut.admin_sign_in('yhjeon','1')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        # not admin user
        try:
            assert driver.find_element(By.CSS_SELECTOR, ".validation-summary-errors >  ul > li").text == "Not admin user"
        except:
            testResult = 'failed'
            reason.append("Sign_InOut step 4 isn't valid")
        
        # 정상적인 계정으로 로그인 한다.
        signInOut.admin_sign_in('INF_JH','Server123!@#')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)        
        try:
            assert driver.find_element(By.CSS_SELECTOR, ".pull-right > span").text == "Sign Out"
        except:
            testResult = 'failed'
            reason.append("Sign_InOut step 5 isn't valid")
        
        print("ITR-1: Sign > Sign In/Out")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # sign_InOut 결과 전송
        result = ' '.join(s for s in reason)
        if testResult == 'failed':
            testlink.reportTCResult(1531, testPlanID, buildName, 'f', result)            
        else:
            testlink.reportTCResult(1531, testPlanID, buildName, 'p', "Sign In/Out Test Passed")
        driver.find_element(By.CSS_SELECTOR, ".pull-right > span").click()
        driver.implicitly_wait(3)
    
    def Rememeber_Me():
        testResult = ''
        remember_id = 'INF_JH'
        
        # 정상적인 계정을 입력 및 remind me를 체크하고 로그인 한다.
        driver.find_element(By.ID, 'user-id').clear()
        driver.find_element(By.ID, 'user-id').send_keys('INF_JH')
        driver.find_element(By.ID, 'user-password').send_keys('Server123!@#')
        driver.find_element(By.CSS_SELECTOR, '.col-xs-8.p-t-5 > label').click()
        driver.find_element(By.CSS_SELECTOR, '.btn').click()         
        driver.implicitly_wait(3)                       
        
        # 로그아웃 후, 마지막에 접속한 User ID와 Remind Me 체크 상태를 확인한다.
        signInOut.admin_sign_out()        
        try:
            assert (driver.find_element(By.ID, 'user-id').text, driver.find_element(By.CSS_SELECTOR, '.col-xs-8.p-t-5 > input').get_attribute('checked')) == (remember_id, 'true')
        except:
            testResult = 'failed' 
        
        print("ITR-2: Sign > Remember Me")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # Remember_Me 결과 전송       
        if testResult == 'failed':
            testlink.reportTCResult(1538, testPlanID, buildName, 'f', "Remember Me Test Failed")            
        else:
            testlink.reportTCResult(1538, testPlanID, buildName, 'p', "Remember Me Test Passed")    

class Topbar:
    def Search_Schedule_List():
        testResult = '' 
        reason = list() 
        
        # 로그인 후, 상단의 Schedule badge를 클릭하고, Schedule 개수를 확인한다.
        signInOut.admin_sign_in('INF_JH','Server123!@#')
        driver.find_element(By.ID, 'schedule_info_box').click()
        sch_info_num = driver.find_element(By.ID, 'schedule_info_number').text
        driver.find_element(By.ID, 'schedule_info_number').click
        sch_info_num = sch_info_num.split('/')
        refer_sch_num, sch_num = sch_info_num[0], sch_info_num[1].strip()
        time.sleep(3)
        
        # Schedule badge의 schedule 개수와 조회 결과 리스트의 schedule 개수를 비교한다.
        temp_sch_num = driver.find_element(By.ID, 'refer-assigned-list_info').text
        temp_sch_num = temp_sch_num.split()
        total_sch_num = temp_sch_num[5]               
        try:
            assert int(total_sch_num) == int(sch_num)
        except:
            testResult = 'failed'
            reason.append("Sign_InOut step 1 isn't valid")
        
        # Schedule badge의 refer된 schedule 개수와 조회 결과 리스트의 refer된 schedule 개수를 비교한다.        
        cnt_refer = driver.find_elements(By.XPATH, '/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div[2]/table/tbody/tr[1]/td[21]/span/i')
        try:
            assert int(cnt_refer) == int(refer_sch_num)
        except:
            testResult = 'failed'
            reason.append("Sign_InOut step 2 isn't valid")

        print("ITR-3: Topbar > Search Schedule List")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # Searh_Schedule_List 결과 전송
        result = ' '.join(s for s in reason)
        if testResult == 'failed':
            testlink.reportTCResult(1542, testPlanID, buildName, 'f', result)            
        else:
            testlink.reportTCResult(1542, testPlanID, buildName, 'p', "Search_Schedule_List Test Passed")  

class Refer:
    def Hospital_List():
        testResult = ''
        reason = list() 
        
        # 1 steps start! : 모든 병원의 badge count와 job list의 결과가 일치하는지 확인
        # Hospital list 저장
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        hospital_cnt = len(data)

        # 각 hospital의 refer, requested, emergency job의 건수 비교
        if hospital_cnt > 0:
            n = 0

            for i in data:
                priority_cnt = i['PriorityCount']
                job_cnt = i['JobCount']
                refer_cnt = i['ReferCount']
                refer_priority_cnt = 0
                time.sleep(2)
                del driver.requests
                hospital_list[n].click()

                # 선택한 병원의 Job list 결과 저장 
                request = driver.wait_for_request('.*/GetAllAssignedList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]
                
                # Showing entry 결과 저장
                temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
                temp_cnt = temp_cnt.split()
                list_cnt = temp_cnt[5]
                refer_reporter_list = []
                emer_reporter_list = []
                
                # Show 100 entries 설정
                select = Select(driver.find_element(By.CSS_SELECTOR,"#refer-assigned-list_length > label > select"))
                select.select_by_value("100")
                pages = math.ceil(int(list_cnt) / 100)
                
                # All Assigned List 탭에서 Refer count를 조회 결과에서 계산 
                while pages > 0: 
                    for i in data:
                        # All Assigned List 탭에서 Refer 건수 계산
                        refer_text = (i["REFERRED_USER_KEYS"])
                        temp_refer_text_list = (refer_text.split(','))                        
                        for j in temp_refer_text_list:                            
                            refer_reporter_list.append(j)
                    
                        # All Assigned List 탭에서 Emergency Job 건수 계산
                        if i["JobPriority"] == 'E':
                            emer_reporter_key = (i["REFERRED_USER_KEYS"])
                            temp_emer_reporter_list = (emer_reporter_key.split(','))
                            for j in temp_emer_reporter_list:
                                emer_reporter_list.append(j)
                            emer_reporter_list_cnt = len(emer_reporter_list)
                            
                    pages = pages - 1
                    del driver.requests
                    
                    # 새로운 페이지 조회 결과 저장
                    if pages > 0:
                        driver.find_element(By.CSS_SELECTOR,"#refer-assigned-list_next > a").click()
                        request = driver.wait_for_request('.*/GetAllAssignedList.*')
                        body = request.response.body.decode('utf-8')
                        data = json.loads(body)["data"]
                    refer_text_list_cnt = len(refer_reporter_list)
                    
                try:
                    assert refer_cnt == refer_text_list_cnt
                except:
                    testResult = 'failed'
                    reason.append("Step1 - Refer count isn't valid")

                # 요청 결과 삭제
                del driver.requests
                
                # All Assigned List의 Showing entries 값 저장
                temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
                temp_cnt = temp_cnt.split()
                list_cnt = temp_cnt[5]
                assigned_list_result = int(list_cnt)

                # Not Assigned List 탭 클릭
                element = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]/a")
                driver.execute_script("arguments[0].click()",element)
                
                # 선택한 병원의 Not Assigned List 결과 저장
                request = driver.wait_for_request('.*/GetNotAssignedList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                # Not Assigned List의 Showing entries 값 저장
                temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
                temp_cnt = temp_cnt.split()
                list_cnt = temp_cnt[5]
                not_refer_text_list = int(list_cnt)
                pages = math.ceil(int(list_cnt) / 100)

                # Emergency Job 건수 계산
                while pages > 0: 
                    for i in data:
                        if i["JobPriority"] == 'E':
                            emer_reporter_list_cnt = emer_reporter_list_cnt + 1
                            
                    pages = pages - 1   
                    del driver.requests
                    if pages > 0:
                        # 새로운 페이지의 결과 저장
                        driver.find_element(By.CSS_SELECTOR,"#refer-assigned-list_next > a").click()
                        request = driver.wait_for_request('.*/GetNotAssignedList.*')
                        body = request.response.body.decode('utf-8')
                        data = json.loads(body)["data"]
                        time.sleep(1)

                try:
                    assert (int(priority_cnt), int(job_cnt)) == (int(emer_reporter_list_cnt), int(assigned_list_result) + int(not_refer_text_list))
                except:
                        testResult = 'failed'
                        reason.append("1 steps failed")

                # All Assigned List 탭 클릭
                driver.find_element(By.XPATH,"/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]/a").click()
                n = n + 1

        # 2 steps start! : 병원을 선택하면 표시되는 Reporter가 해당 병원의 소속된 Reporter 인지 확인
        # Refer 화면 새로고침
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Hospital list 저장
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        hospital_cnt = len(data)
        
        if hospital_cnt > 0:
            n = 0

            for i in data:
                # Institution name 저장
                inst_name = i['InstitutionName']
                time.sleep(0.5)
                del driver.requests
                
                # Hospital list 다시 저장
                hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
                hospital_list[n].click()
                
                # Hospital list의 Reporter list 저장
                request = driver.wait_for_request('.*/GetReporterListByInstitution.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)
                reporter_list = []
                
                # Reporter Key 저장                
                for i in data:
                    reporter_list.append(i['ReporterKey'])

                # Configuration > Download control로 이동
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[5]/a").click()
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/button[3]").click()

                # 선택한 병원의 institution code 입력 후, 검색
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[2]/div").click()
                driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > div > input[type=text]").send_keys(inst_name)
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[2]/div/div/div/input").send_keys(Keys.RETURN)
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[5]/button").click()
                time.sleep(0.5)
                del driver.requests
                
                # Showing entries 100으로 변경
                select = Select(driver.find_element(By.CSS_SELECTOR,"#download-list_length > label > select"))                
                select.select_by_value("100")

                # Download control의 Reporter list 저장
                request = driver.wait_for_request('.*/GetDownloadControlList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]
                dc_reporter_list = []

                # 선택한 Institution의 Reporter key 저장
                for i in data:
                    dc_reporter_list.append(i['UserKey'])

                # Hospital list에서의 reporter가 download control에서 해당 institution의 reporter인지 확인
                for i in reporter_list:
                        if int(i) not in dc_reporter_list:
                            result = "false"
                        else:
                            result = "true"

                try:
                    assert result == "true"
                except:
                    testResult = 'failed'
                    reason.append("2 steps failed")
                
                # Refer 탭 클릭
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
                n = n + 1
        
        # 3 steps start! : 병원 리스트 > Reporter 클릭 시, 표시되는 modality job count가 job list와 일치하는지 확인
        # Hospital list 저장
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        hospital_cnt = len(data)

        if hospital_cnt > 0:
            n = 0

            while n < hospital_cnt:
                # Hospital list 저장 및 병원 순서대로 클릭
                hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
                hospital_list[n].click()

                # 선택한 병원의 Reporter list 저장 및 인원 수 확인
                temp = driver.find_elements(By.CLASS_NAME, "list-report-id")            
                temp_cnt = len(temp)
                m = 0
                
                # 병원 탭에 표시되는 Reporter의 modality list와 클릭시 표시되는 job list의 modality list 비교
                while m < temp_cnt:
                    sub_modal_list = []
                    
                    # 병원 탭 > 선택한 Reporter key 저장
                    time.sleep(2)
                    temp_reporter_key = driver.find_elements(By.CLASS_NAME, "list-group-item.list-sub-item")
                    reporter_key = (temp_reporter_key[m].get_property("dataset"))["reporterKey"]
                    
                    # 병원 탭 > Reporter 클릭
                    temp = driver.find_elements(By.CLASS_NAME, "list-report-id")
                    driver.execute_script("arguments[0].click()",temp[m])
                    
                    # 병원 탭 > 선택한 Reporter의 modality 저장
                    modality_list = driver.find_elements(By.CLASS_NAME, "list-modality-info")
                    for i in modality_list:
                        sub_modal_list.append(i.get_property("outerText").split('\n')[0])
                    
                    # 병원 탭 > 선택한 Reporter의 Job list 저장
                    request = driver.wait_for_request('.*/GetReferedListByReporter.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]
                    temp_job_modality_list = []
                    job_modality_list = []

                    for i in data:
                        job_modality_list.append(i["Modality"])

                    # 판독의 탭 클릭
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/li[2]/a").click()

                    # 판독의 탭 > 선택한 Reporter 클릭
                    time.sleep(1)
                    del driver.requests
                    driver.find_element(By.CSS_SELECTOR, "#list-reporter-row-"+reporter_key).click()

                    # 판독의 탭 > 선택한 Reporter의 Job list에서 modality 저장                
                    request = driver.wait_for_request('.*/GetAllReferedListByReporter.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]
                    
                    for i in data:
                        temp_job_modality_list.append(i["Modality"])

                    # 판독의 탭 > Modality list에서 중복 제거                    
                    for i in temp_job_modality_list:
                        if i not in job_modality_list:
                            job_modality_list.append(i)

                    # 병원 탭 > Reporter의 Modality와 판독의 탭 > Reporter Job list의 Modality 비교
                    try:
                        assert sub_modal_list.sort() == job_modality_list.sort()
                    except:
                        testResult = 'failed'
                        reason.append("3 steps failed")

                    # 병원탭 클릭
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/li[1]/a").click()
                    m = m + 1
                n = n + 1
                
                # Refer 탭 클릭
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
                
        # 4 steps start! : View All Institution List 체크 시, 표시되는 병원이 올바른 것인지 확인
        # Subadmin 계정으로 로그인
        signInOut.admin_sign_out()
        signInOut.subadmin_sign_in()
        
        # View All Instituion List 체크
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[2]/label/span").click()

        # All Hospital list 저장
        time.sleep(1)
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        All_institution_list = []

        for i in data:
            All_institution_list.append(i["InstitutionCode"])

        # Configuration 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[5]").click()

        # Institutions 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/button[4]").click()

        # Institution list 저장
        request = driver.wait_for_request('.*/GetInstitutionsList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        institutions_list = []
        
        for i in data:
            institutions_list.append(i["InstitutionCode"])

        # Hospital list와 Institution list 비교
        try:
            assert All_institution_list.sort() == institutions_list.sort()
        except:
            testResult = 'failed'
            reason.append("4 steps failed")
        
        # 5 steps start! : View All Institution List 언체크 시, 표시되는 병원이 올바른 것인지 확인
        # Refer 탭 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
        
        # # View All Instituion List 체크
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[2]/label/span").click()

        # View All Institution list에서 Job이 있는 Institution list만 저장
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        all_institution_list = []

        for i in data:
            if i["JobCount"] > 0 or i["PriorityCount"] > 0 or i["ReferCount"] > 0:
                all_institution_list.append(i["InstitutionCode"])

        # View All Instituion List 언체크
        del driver.requests        
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[2]/label/span").click()
        
        # View All Institution list 언체크 시의 Hospital list 저장
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        Job_institution_list = []

        for i in data:
            Job_institution_list.append(i["InstitutionCode"])

        # Job이 있는 hospital 만 list에 표시되는지 확인
        try:
            assert all_institution_list == Job_institution_list
        except:
            testResult = 'failed'
            reason.append("5 steps failed")

        # 6 steps start! : 선택한 병원의 job만 job list에 표시되는지 확인        
        # Hospital list 저장
        click_hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        hospital_cnt = len(data)
        hospital_list = []

        for i in data:
            if i["InstitutionName"] not in hospital_list:
                hospital_list.append(i["InstitutionName"])
        
        if hospital_cnt > 0:
            n = 0
            
            while n < hospital_cnt:
                # 순서대로 병원 클릭
                time.sleep(1)
                del driver.requests
                click_hospital_list[n].click()

                # All Assigned List 탭 > 선택한 병원의 job list 저장
                request = driver.wait_for_request('.*/GetAllAssignedList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]
                job_list = []

                for i in data:
                    if i["InstitutionName"] not in job_list:
                        job_list.append(i["InstitutionName"])

                # Not Assigned List 탭 클릭
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()
                
                # Not Assigned List 탭 > 선택한 병원의 job list 저장
                time.sleep(1)
                request = driver.wait_for_request('.*/GetNotAssignedList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for i in data:
                    if i["InstitutionName"] not in job_list:
                        job_list.append(i["InstitutionName"])

                # job list에 선택한 병원의 job만 표시되는지 확인
                try:
                    check_job_list = ' '.join(s for s in job_list)
                    assert hospital_list[n] == check_job_list                    
                except:
                    testResult = 'failed'
                    reason.append("6 steps failed")
                n = n + 1
            
                # All Assigned List 탭 클릭
                driver.find_element(By.XPATH,"/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]/a").click()

        # Admin 계정으로 로그인
        signInOut.subadmin_sign_out()
        signInOut.admin_sign_in()        

        # 7 steps start! : 선택한 병원의 badge count와 job list의 count가 일치하는지 확인
        # Hospital list 저장
        click_hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        hospital_cnt = len(data)
        
        if hospital_cnt > 0:
            n = 0
            reporter_list = []
            
            while n < hospital_cnt:
                # 순서대로 병원 클릭
                time.sleep(1)
                del driver.requests
                click_hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
                click_hospital_list[n].click()
                m = 0

                # 선택한 병원의 Reporter list 저장
                time.sleep(2)
                reporter_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-sub-item")
                reporter_list_cnt = len(reporter_list)
                
                # Reporter의 badge count 저장
                request = driver.wait_for_request('.*/GetReporterListByInstitution.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)
                badge_cnt_list = []
                job_cnt = []

                for i in data:
                    badge_counts = []
                    badge_counts.append(i["PriorityCount"])
                    badge_counts.append(i["ReferCount"])
                    badge_counts.append(i["OtherInstitutionReferCount"])
                    # badge_counts.append(i["ReportedCount"])
                    badge_counts.append(i["ScheduleCount"])
                    badge_cnt_list.append(badge_counts)

                # 순서대로 Reporter 클릭 후, job list에서 emergency, refer, scheduled count 저장
                while m < reporter_list_cnt:
                    reporter_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-sub-item")
                    reporter_key = (reporter_list[m].get_property("dataset"))["reporterKey"]
                    driver.execute_script("arguments[0].click()",reporter_list[m])

                    # All Assigned 탭 > job list에서 선택한 Reporter의 emergency, refer, scheduled count 저장
                    request = driver.wait_for_request('.*/GetReferedListByReporter.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]
                    emergency_cnt = 0
                    refer_cnt = 0
                    scheduled_cnt = 0
                    other_refer_cnt = 0
                    # reported_cnt = 0

                    for i in data:
                        # Emergency count 계산
                        if i["JobPriority"] == "E":
                            emergency_cnt = emergency_cnt + 1
                        refer_cnt = refer_cnt + 1
                        if type(i["ScheduleDate"]) != NoneType:
                            scheduled_cnt = scheduled_cnt + 1
                        
                    # 판독의 탭 클릭
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/li[2]/a").click()

                    # 판독의 탭 > 선택한 Reporter 클릭
                    time.sleep(2)
                    del driver.requests
                    driver.find_element(By.CSS_SELECTOR, "#list-reporter-row-"+reporter_key).click()

                    # Other refer count 저장
                    request = driver.wait_for_request('.*/GetInstitutionListByReporter.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)

                    for i in data:
                        if i["InstitutionName"] != click_hospital_list[n].get_property("dataset")["institutionName"]:
                            other_refer_cnt = other_refer_cnt + int(i["ReferCount"])
                    job_sub_cnt = []
                    job_sub_cnt.append(emergency_cnt)
                    job_sub_cnt.append(refer_cnt)
                    job_sub_cnt.append(other_refer_cnt)
                    job_sub_cnt.append(scheduled_cnt)
                    job_cnt.append(job_sub_cnt)
                    m = m + 1

                    # Refer 탭 클릭
                    time.sleep(1)
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

                    # 병원 선택
                    time.sleep(2)
                    click_hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
                    click_hospital_list[n].click()

                # Reporter badge count와 job list count 확인
                try:
                    assert badge_cnt_list == job_cnt                    
                except:
                    testResult = 'failed'
                    reason.append("7 steps failed")
                n = n + 1

                # Refer 탭 클릭
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 8 steps start! : 선택한 Reporter의 Job list가 표시되는지 확인
        # Hospital list 저장
        click_hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        hospital_cnt = len(data)
        
        if hospital_cnt > 0:
            n = 0
            
            while n < hospital_cnt:
                # 순서대로 병원 클릭
                time.sleep(1)
                del driver.requests
                click_hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
                click_hospital_list[n].click()
                m = 0

                # 선택한 병원의 Reporter list 저장
                time.sleep(2)
                reporter_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-sub-item")
                reporter_list_cnt = len(reporter_list)

                # 순서대로 Reporter 클릭
                while m < reporter_list_cnt:
                    time.sleep(1)
                    del driver.requests                    
                    reporter_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-sub-item")
                    reporter_key = (reporter_list[m].get_property("dataset"))["reporterKey"]
                    driver.execute_script("arguments[0].click()",reporter_list[m])

                    # 선택한 Reporter의 Job list 저장
                    request = driver.wait_for_request('.*/GetReferedListByReporter.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]
                    job_reporter_key = []

                    for i in data:
                        if i["REFERRED_USER_KEYS"] not in job_reporter_key:
                            job_reporter_key.append(i["REFERRED_USER_KEYS"])
                    job_reporter_key = ' '.join(s for s in job_reporter_key)

                    # 선택한 Reporter의 Job list가 표시되는지 확인
                    try:
                        assert reporter_key == job_reporter_key 
                    except:
                        testResult = 'failed'
                        reason.append("8 steps failed")
                    m = m + 1

                # Refer 탭 클릭
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
                n = n + 1

        print("ITR-7: Refer > Hospital List")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # Hospital_List 결과 전송
        result = ' '.join(s for s in reason)
        if testResult == 'failed':
            testlink.reportTCResult(1567, testPlanID, buildName, 'f', result)            
        else:
            testlink.reportTCResult(1567, testPlanID, buildName, 'p', "Hospital_List Test Passed")  

    def Reporter_List():
        testResult = ''
        reason = list()        

        # 1 & 2 steps start! : 판독의 탭 > 판독의 리스트에 표시되는 badge count가 job list와 일치하는지 확인
        # Reporter list를 저장한다.
        driver.find_element(By.XPATH, "//*[@id='tab-reporter']").click()
        reporter_list = driver.find_elements(By.CSS_SELECTOR, "#refer-reporter-list > div > .list-group-item.list-institution")
        request = driver.wait_for_request('.*/GetReferCountsByReporter.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        reporter_cnt = len(data)

        # 각 reporter의 refer, emergency, schedule job의 건수를 비교한다.
        if reporter_cnt > 0:
            n = 0
            for i in data:                
                proirity_cnt = i['PriorityCount']
                refer_cnt = i['ReferCount']
                schedule_cnt = i['ScheduleCount']
                
                # Tap panel의 refer count와 조회 결과 리스트에서의 refer count를 비교한다.
                del driver.requests
                reporter_list[n].click()
                time.sleep(1.5)                
                if refer_cnt > 0:
                    temp_cnt = driver.find_element(By.XPATH,'/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]').text
                    temp_cnt = temp_cnt.split()
                    list_cnt = temp_cnt[5]
                    try:
                        assert int(refer_cnt) == int(list_cnt)
                    except:
                        testResult = 'failed'
                        reason.append("1 steps failed: refer_cnt isn't valid")
                
                # Tap panel의 emergency job count와 조회 결과 리스트에서의 emergency job count를 비교한다.   
                if proirity_cnt > 0:
                    driver.find_element(By.CSS_SELECTOR, "#refer_search_priority_chosen span").click()
                    driver.find_element(By.CSS_SELECTOR, ".active-result:nth-child(2)").click()
                    driver.find_element(By.XPATH,'/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]').click()
                    time.sleep(1.5) 
                    temp_cnt = driver.find_element(By.XPATH,'/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]').text                                   
                    temp_cnt = temp_cnt.split()
                    list_cnt = temp_cnt[5]
                    try:
                        assert int(proirity_cnt) == int(list_cnt)                        
                    except:
                        testResult = 'failed'
                        reason.append("1 steps failed: proirity_cnt isn't valid")

                # Tap panel의 schedule job count와 조회 결과 리스트에서의 schedule job count를 비교한다.   
                if schedule_cnt > 0:
                    request = driver.wait_for_request('.*/GetAllReferedListByReporter.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]
                    temp_cnt = 0                    
                    for i in data:              
                        if type(i['ScheduleDate']) != NoneType:
                            temp_cnt = temp_cnt + 1
                    try:
                        assert int(schedule_cnt) == int(temp_cnt)                        
                    except:
                        testResult = "failed"
                        reason.append("1 & 2 steps failed: schedule_cnt isn't valid")
                        
                n = n + 1
                
                # 판독의 탭 > Search filter > Priority를 Priority로 선택
                driver.find_element(By.CSS_SELECTOR, "#refer_search_priority_chosen span").click()
                driver.find_element(By.CSS_SELECTOR, ".active-result:nth-child(1)").click()         
        
                # Refer 탭 클릭
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
        
        # 3 steps start! : 판독의 탭 > Reporter를 클릭했을 때, 표시되는 병원 리스트와 병원 선택 시, 해당 병원의 job list가 표시되는지 확인
        # 판독의 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/li[2]/a").click()

        # Repoter list 저장
        request = driver.wait_for_request('.*/GetReferCountsByReporter.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        reporter_key_list = []

        for i in data:
            reporter_key_list.append(i["ReporterKey"])
        
        # 순서대로 Reporter를 선택
        for reporter_key in reporter_key_list:
            time.sleep(1)
            del driver.requests
            driver.find_element(By.CSS_SELECTOR, "#list-reporter-row-" + reporter_key).click()
            
            # 선택한 Reporter의 Institution list 저장
            request = driver.wait_for_request('.*/GetInstitutionListByReporter.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            intitution_code_list = []
            
            for i in data:
                intitution_code_list.append(i["InstitutionCode"])

            # 선택한 Reporter의 institution 개수 확인
            intitution_code_cnt = len(intitution_code_list)
            m = 0 
            
            # 선택한 Reporter의 institution을 순서대로 클릭
            job_list = []
            while m < intitution_code_cnt:
                time.sleep(1)
                del driver.requests
                click = driver.find_element(By.CSS_SELECTOR, ".list-group-item.list-sub-item[data-institution-code='" + intitution_code_list[m] + "']")
                driver.execute_script("arguments[0].click()",click)

                # 선택한 institution의 job list 저장
                request = driver.wait_for_request('.*/GetReferedListByReporter.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]
            
                for i in data:
                    if i["InstitutionCode"] not in job_list:
                        job_list.append(i["InstitutionCode"])
                m = m + 1

            # 선택한 Reporter의 institution과 job list 데이터의 institution이 동일한지 확인
            try:
                assert intitution_code_list == job_list
            except:
                testResult = "failed"
                reason.append("3 steps failed")

            # 판독의 탭 클릭
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/li[2]/a").click()
                
        print("ITR-8: Refer > Reporter List")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # Reporter_List 결과 전송
        result = ' '.join(s for s in reason)
        if testResult == 'failed':
            testlink.reportTCResult(1577, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1577, testPlanID, buildName, 'p', "Reporter List Passed")
    
class Search_filter:
    def Priority():
        testResult = ''
        reason = list()

        # 1 steps start! : Priority 조건을 응급으로 선택한 후, Search 버튼 클릭
        # Refer 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Hospital list 저장
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        hospital_cnt = len(hospital_list)

        # 순서대로 Hospital 선택
        if hospital_cnt > 0:
            n = 0

            while n < hospital_cnt:
                # Hospital list 저장 및 병원 순서대로 클릭
                hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
                hospital_list[n].click()
        
                # 병원 선택 > All Assigned List > Priority 드랍박스에서 Priority 선택 후, Search 버튼 클릭
                time.sleep(1)
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div").click()                
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/ul/li[2]").click()
                del driver.requests
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

                # 병원 선택 > All Assigned List > Job list 저장
                request = driver.wait_for_request('.*/GetAllAssignedList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]
                job_priority = []

                for i in data:
                    if i["JobPriority"] not in job_priority:
                        job_priority.append(i["JobPriority"])

                # Not Assigned List 탭 클릭
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()
                
                # 병원 선택 > Not Assigned List > Job list 저장
                request = driver.wait_for_request('.*/GetNotAssignedList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for i in data:
                    if i["JobPriority"] not in job_priority:
                        job_priority.append(i["JobPriority"])

                # 병원 선택 > Job list에서 응급만 표시되는지 확인
                try:
                    job_priority = ' '.join(s for s in job_priority)
                    assert job_priority == "E"
                except:
                    testResult = "failed"
                    reason.append("1 steps failed")
                n = n + 1
                # All Assigned List 탭 클릭
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        # 2 steps start! : Priority 조건을 일반으로 선택한 후, Search 버튼 클릭
        # Refer 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Hospital list 저장
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        hospital_cnt = len(hospital_list)

        # 순서대로 Hospital 선택
        if hospital_cnt > 0:
            n = 0

            while n < hospital_cnt:
                # Hospital list 저장 및 병원 순서대로 클릭
                click = hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
                # hospital_list[n].click()
                driver.execute_script("arguments[0].click()",click[n])

                # 병원 선택 > All Assigned List > Priority 드랍박스에서 일반 선택 후, Search 버튼 클릭
                time.sleep(1)
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div").click()                
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/ul/li[3]").click()
                del driver.requests
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

                # 병원 선택 > All Assigned List > Job list 저장
                request = driver.wait_for_request('.*/GetAllAssignedList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]
                job_priority = []

                for i in data:
                    if i["JobPriority"] not in job_priority:
                        job_priority.append(i["JobPriority"])
                
                # Not Assigned List 탭 클릭
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

                # 병원 선택 > Not Assigned List > Job list 저장
                request = driver.wait_for_request('.*/GetNotAssignedList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for i in data:
                    if i["JobPriority"] not in job_priority:
                        job_priority.append(i["JobPriority"])
                
                # 병원 선택 > Job list에서 응급만 표시되는지 확인
                try:
                    job_priority = ' '.join(s for s in job_priority)
                    assert job_priority == "N"
                except:
                    testResult = "failed"
                    reason.append("2 steps failed")
                n = n + 1
                # All Assigned List 탭 클릭
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        print("ITR-9: Search Filter > Priority")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # Priority 결과 전송
        result = ' '.join(s for s in reason)
        if testResult == 'failed':
            testlink.reportTCResult(1583, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1583, testPlanID, buildName, 'p', "Priority Passed")

    def Job_Status():
        testResult = ''
        reason = list()

        # 1 steps start! : Job Status를 Requested로 선택한 후, Search All버튼을 클릭한다.
        # All List 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # All List > Job Status를 Requested로 변경하고, Search All 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[2]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # All List > Job list의 Job Status 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_status = []

        for i in data:
            if i["StatDescription"] not in job_status:
                job_status.append(i["StatDescription"])

        # Job Status가 Requested 만 조회되었는지 확인
        try:
            job_status = ' '.join(s for s in job_status)
            assert job_status == "Requested" or job_status == ''
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! : Job Status를 Reported로 선택한 후, Search All버튼을 클릭한다.
        # All List > Job Status를 Reported로 변경하고, Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[3]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # All List > Job list의 Job Status 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_status = []

        for i in data:
            if i["StatDescription"] not in job_status:
                job_status.append(i["StatDescription"])

        # Job Status가 Reported 만 조회되었는지 확인
        try:
            job_status = ' '.join(s for s in job_status)
            assert job_status == "Reported" or job_status == ''
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # 3 steps start! : Job Status를 Pending으로 선택한 후, Search All버튼을 클릭한다.
        # All List > Job Status를 Pending로 변경하고, Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[4]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # All List > Job list의 Job Status 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_status = []

        for i in data:
            if i["StatDescription"] not in job_status:
                job_status.append(i["StatDescription"])

        # Job Status가 Pending 만 조회되었는지 확인
        try:
            job_status = ' '.join(s for s in job_status)
            assert job_status == "Pending" or job_status == ''
        except:
            testResult = "failed"
            reason.append("3 steps failed\n")

        # 4 steps start! : Job Status를 Completed로 선택한 후, Search All버튼을 클릭한다.
        # All List > Job Status를 Completed로 변경하고, Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[5]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # All List > Job list의 Job Status 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_status = []

        for i in data:
            if i["StatDescription"] not in job_status:
                job_status.append(i["StatDescription"])

        # Job Status가 Completed 만 조회되었는지 확인
        try:
            job_status = ' '.join(s for s in job_status)
            assert job_status == "Completed" or job_status == ''
        except:
            testResult = "failed"
            reason.append("4 steps failed\n")

        # 5 steps start! : Job Status를 Recalled로 선택한 후, Search All버튼을 클릭한다.
        # All List > Job Status를 Recalled로 변경하고, Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[6]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # All List > Job list의 Job Status 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_status = []

        for i in data:
            if i["StatDescription"] not in job_status:
                job_status.append(i["StatDescription"])

        # Job Status가 Recalled 만 조회되었는지 확인
        try:
            job_status = ' '.join(s for s in job_status)
            assert job_status == "Recalled" or job_status == ''
        except:
            testResult = "failed"
            reason.append("5 steps failed\n")

        # 6 steps start! : Job Status를 Canceled로 선택한 후, Search All버튼을 클릭한다.
        # All List > Job Status를 Canceled로 변경하고, Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[7]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # All List > Job list의 Job Status 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_status = []

        for i in data:
            if i["StatDescription"] not in job_status:
                job_status.append(i["StatDescription"])

        # Job Status가 Canceled 만 조회되었는지 확인
        try:
            job_status = ' '.join(s for s in job_status)
            assert job_status == "Canceled" or job_status == ''
        except:
            testResult = "failed"
            reason.append("6 steps failed\n")

        # 7 steps start! : Job Status를 Canceled2로 선택한 후, Search All버튼을 클릭한다.
        # All List > Job Status를  Canceled2로 변경하고, Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[8]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # All List > Job list의 Job Status 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_status = []

        for i in data:
            if i["StatDescription"] not in job_status:
                job_status.append(i["StatDescription"])

        # Job Status가 Canceled2 만 조회되었는지 확인
        try:
            job_status = ' '.join(s for s in job_status)
            assert job_status == "Canceled2" or job_status == ''
        except:
            testResult = "failed"
            reason.append("7 steps failed\n")

        # 8 steps start! : Job Status를 Returned로 선택한 후, Search All버튼을 클릭한다.
        # All List > Job Status를 Returned로 변경하고, Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[9]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # All List > Job list의 Job Status 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_status = []

        for i in data:
            if i["StatDescription"] not in job_status:
                job_status.append(i["StatDescription"])

        # Job Status가 Returned 만 조회되었는지 확인
        try:
            job_status = ' '.join(s for s in job_status)
            assert job_status == "Returned" or job_status == ''
        except:
            testResult = "failed"
            reason.append("8 steps failed\n")

        # 9 steps start! : Job Status를 Failed Download Report로 선택한 후, Search All버튼을 클릭한다.
        # All List > Job Status를 Failed Download Report로 변경하고, Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[10]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # All List > Job list의 Job Status 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_status = []

        for i in data:
            if i["StatDescription"] not in job_status:
                job_status.append(i["StatDescription"])

        # Job Status가 Failed Download Report 만 조회되었는지 확인
        try:
            job_status = ' '.join(s for s in job_status)
            assert job_status == "Failed Download Report" or job_status == ''
        except:
            testResult = "failed"
            reason.append("9 steps failed\n")

        # 10 steps start! : Job Status를 AI Processing으로 선택한 후, Search All버튼을 클릭한다.
        # All List > Job Status를 AI Processing로 변경하고, Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[11]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # All List > Job list의 Job Status 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_status = []

        for i in data:
            if i["StatDescription"] not in job_status:
                job_status.append(i["StatDescription"])

        # Job Status가 AI Processing 만 조회되었는지 확인
        try:
            job_status = ' '.join(s for s in job_status)
            assert job_status == "AI Processing" or job_status == ''
        except:
            testResult = "failed"
            reason.append("10 steps failed\n")

        # 11 steps start! : Job Status를 DiscardRequest로 선택한 후, Search All버튼을 클릭한다.
        # All List > Job Status를 DiscardRequest로 변경하고, Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[12]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # All List > Job list의 Job Status 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_status = []

        for i in data:
            if i["StatDescription"] not in job_status:
                job_status.append(i["StatDescription"])

        # Job Status가 DiscardRequest 만 조회되었는지 확인
        try:
            job_status = ' '.join(s for s in job_status)
            assert job_status == "DiscardRequest" or job_status == ''
        except:
            testResult = "failed"
            reason.append("11 steps failed\n")

        # 12 steps start! : Job Status를 DiscardCompleted로 선택한 후, Search All버튼을 클릭한다.
        # All List > Job Status를 DiscardCompleted로 변경하고, Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[13]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # All List > Job list의 Job Status 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_status = []

        for i in data:
            if i["StatDescription"] not in job_status:
                job_status.append(i["StatDescription"])

        # Job Status가 DiscardCompleted 만 조회되었는지 확인
        try:
            job_status = ' '.join(s for s in job_status)
            assert job_status == "DiscardCompleted" or job_status == ''
        except:
            testResult = "failed"
            reason.append("12 steps failed\n")

        print("ITR-10: Search Filter > Job Status")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # Priority 결과 전송
        result = ' '.join(s for s in reason)
        if testResult == 'failed':
            testlink.reportTCResult(1588, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1588, testPlanID, buildName, 'p', "Job Status Passed")
    
    def Date():
        testResult = ''
        reason = list()

        # 1 steps start! : Date를 Job Date로 선택하고, 임의의 기간을 입력한 후, Search 버튼을 클릭한다.
        # 2 steps start! : Date를 Study Date로 선택하고, 임의의 기간을 입력한 후, Search 버튼을 클릭한다.
        # 3 steps start! : Date를 Schedule Date로 선택하고, 임의의 기간을 입력한 후, Search 버튼을 클릭한다.
        # Test 병원을 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # date_type에 job date, study date, schedule date 주소를 리스트로 선언
        date_type = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[3]/div/div/ul/li[1]','JobDTTMString'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[3]/div/div/ul/li[2]','StudyDTTMString'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[3]/div/div/ul/li[3]','ScheduleDateDTTMString']]

        # Date를 Job Date, Study Date, Schedule Date 순서대로 조회 시, All/Not Assigned List 탭의 데이터가 올바르게 조회되는지 확인
        for j in range(0,3):
            # All Assigned List 탭 클릭
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

            # Date를 Job Date로 선택
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[3]/div").click()
            driver.find_element(By.XPATH, date_type[j][0]).click()

            # Start Date를 Yesterday로 선택
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[4]/div/div[1]/input").click()
            driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(1) > th:nth-child(1)").click()

            # Search 버튼 클릭
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

            # All Assigned List > Job list의 결과 저장
            time.sleep(1)
            request = driver.wait_for_request('.*/GetAllAssignedList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_date = []

            if data != '':
                for i in data:
                    temp_job_date = i[date_type[j][1]]
                    if temp_job_date.split()[0] not in job_date:
                        job_date.append(temp_job_date.split()[0])
            
            # All Assigned List > Job list의 결과가 Yesterday 인지 확인
            try:
                for i in job_date:
                    assert int((today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or job_date == ''
            except:
                testResult = "failed"
                reason.append(j +" steps failed\n")

            # All Assigned List > Job Date를 Today로 선택
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[4]/div/div[1]/input").click()
            driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(1) > th:nth-child(2)").click()

            # Search 버튼 클릭
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

            # All Assigned List > Job list의 결과 저장
            time.sleep(1)
            request = driver.wait_for_request('.*/GetAllAssignedList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_date = []

            if data != '':
                for i in data:
                    temp_job_date = i[date_type[j][1]]
                    if temp_job_date.split()[0] not in job_date:
                        job_date.append(temp_job_date.split()[0])

            # All Assigned List > Job list의 결과가 Today 인지 확인
            try:
                job_date = ' '.join(s for s in job_date)
                assert job_date == str(today.strftime('%Y-%m-%d')) or job_date == ''
            except:
                testResult = "failed"
                reason.append(j +" steps failed\n")

            # All Assigned List > Job Date를 last 1~4 week으로 선택
            for n in range(2,7):
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[4]/div/div[1]/input").click()
                driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(2) > th:nth-child("+str(n)+")").click()

                # Search 버튼 클릭
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                
                # All Assigned List > Job list의 결과 저장
                time.sleep(1)
                request = driver.wait_for_request('.*/GetAllAssignedList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]
                job_date = []

                if data != '':
                    for i in data:
                        temp_job_date = i[date_type[j][1]]
                        if temp_job_date.split()[0] not in job_date:
                            job_date.append(temp_job_date.split()[0])

                # All Assigned List > Job list의 결과가 last 1~5week 인지 확인
                try:
                    for i in job_date:
                        assert int((today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or int(str(((today - timedelta(weeks=(n-1))) - datetime.strptime(i, '%Y-%m-%d'))).split()[0]) <= 0
                except:
                    testResult = "failed"
                    reason.append(j +" steps failed\n")

            # All Assigned List > Job Date를 last 1~12 month으로 선택
            m = 0
            for n in range(2,7):
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[4]/div/div[1]/input").click()
                driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(3) > th:nth-child("+str(n)+")").click()

                # Search 버튼 클릭
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
            
                # All Assigned List > Job list의 결과 저장
                request = driver.wait_for_request('.*/GetAllAssignedList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]
                job_date = []

                if data != '':
                    for i in data:
                        temp_job_date = i[date_type[j][1]]
                        if temp_job_date.split()[0] not in job_date:
                            job_date.append(temp_job_date.split()[0])

                # All Assigned List > Job list의 결과가 last 1~12 month 인지 확인
                try:
                    for i in job_date:
                        if n == 2:
                            assert int((today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or int(str((today - relativedelta(months=1)) - datetime.strptime(i, '%Y-%m-%d')).split()[0]) <= 0
                        else:
                            assert int((today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or int(str(((today - relativedelta(months=(3*m))) - datetime.strptime(i, '%Y-%m-%d'))).split()[0]) <= 0
                            
                except:
                    testResult = "failed"
                    reason.append(j +" steps failed\n")
                m = m + 1

            # Not Assigned List 탭 클릭
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

            # Date를 Job Date로 선택
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[3]/div").click()
            driver.find_element(By.XPATH, date_type[j][0]).click()

            # Start Date를 Yesterday로 선택
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[4]/div/div[1]/input").click()
            driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(1) > th:nth-child(1)").click()

            # Search 버튼 클릭
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

            # Not Assigned List > Job list의 결과 저장
            time.sleep(1)
            request = driver.wait_for_request('.*/GetNotAssignedList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_date = []

            if data != '':
                for i in data:
                    temp_job_date = i[date_type[j][1]]
                    if temp_job_date.split()[0] not in job_date:
                        job_date.append(temp_job_date.split()[0])
            
            # Not Assigned List > Job list의 결과가 Yesterday 인지 확인
            try:
                for i in job_date:
                    assert int((today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or job_date == ''
            except:
                testResult = "failed"
                reason.append(j +" steps failed\n")

            # Not Assigned List > Job Date를 Today로 선택
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[4]/div/div[1]/input").click()
            driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(1) > th:nth-child(2)").click()

            # Search 버튼 클릭
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

            # Not Assigned List > Job list의 결과 저장
            time.sleep(1)
            request = driver.wait_for_request('.*/GetNotAssignedList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_date = []

            if data != '':
                for i in data:
                    temp_job_date = i[date_type[j][1]]
                    if temp_job_date.split()[0] not in job_date:
                        job_date.append(temp_job_date.split()[0])

            # Not Assigned List > Job list의 결과가 Today 인지 확인
            try:
                job_date = ' '.join(s for s in job_date)
                assert job_date == str(today.strftime('%Y-%m-%d')) or job_date == ''
            except:
                testResult = "failed"
                reason.append(j +" steps failed\n")

            # Not Assigned List > Job Date를 last 1~4 week으로 선택
            for n in range(2,7):
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[4]/div/div[1]/input").click()
                driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(2) > th:nth-child("+str(n)+")").click()

                # Search 버튼 클릭
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                
                # Not Assigned List > Job list의 결과 저장
                time.sleep(1)
                request = driver.wait_for_request('.*/GetNotAssignedList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]
                job_date = []

                if data != '':
                    for i in data:
                        temp_job_date = i[date_type[j][1]]
                        if temp_job_date.split()[0] not in job_date:
                            job_date.append(temp_job_date.split()[0])

                # All Assigned List > Job list의 결과가 last 1~5week 인지 확인
                try:
                    for i in job_date:
                        assert int((today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or int(str(((today - timedelta(weeks=(n-1))) - datetime.strptime(i, '%Y-%m-%d'))).split()[0]) <= 0
                except:
                    testResult = "failed"
                    reason.append(j +" steps failed\n")

            # Not Assigned List > Job Date를 last 1~12 month으로 선택
            m = 0
            for n in range(2,7):
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[4]/div/div[1]/input").click()
                driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(3) > th:nth-child("+str(n)+")").click()

                # Search 버튼 클릭
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
            
                # Not Assigned List > Job list의 결과 저장
                request = driver.wait_for_request('.*/GetNotAssignedList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]
                job_date = []

                if data != '':
                    for i in data:
                        temp_job_date = i[date_type[j][1]]
                        if temp_job_date.split()[0] not in job_date:
                            job_date.append(temp_job_date.split()[0])

                # Not Assigned List > Job list의 결과가 last 1~12 month 인지 확인
                try:
                    for i in job_date:
                        if n == 2:
                            assert int((today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or int(str((today - relativedelta(months=1)) - datetime.strptime(i, '%Y-%m-%d')).split()[0]) <= 0
                        else:
                            assert int((today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or int(str(((today - relativedelta(months=(3*m))) - datetime.strptime(i, '%Y-%m-%d'))).split()[0]) <= 0
                            
                except:
                    testResult = "failed"
                    reason.append(j +" steps failed\n")
                m = m + 1

        # 4 steps start! : All List 탭을 클릭한 후, Job list의 job date가 최근 1년의 데이터인지 확인한다.
        # All List 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # All List > Date Type의 Job Date 인지 확인
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[3]/div/a").get_property("textContent") != "Job Date":
            testResult = "4 steps failed\n"

        # All List > Date 기간이 오늘날짜부터 과거 1년으로 설정되어 있는지 확인
        start_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[4]/div/div[1]/input").get_property("value")
        end_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[4]/div/div[2]/input").get_property("value")
        if (datetime.strptime(start_date, '%Y-%m-%d') - datetime.strptime(end_date, '%Y-%m-%d')).days <= 365:
            testResult = '4 steps failed'
        
        # All List > Job list의 job date를 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_date = []

        if data != '':
            for i in data:
                temp_job_date = i['JobDTTMString']
                if temp_job_date.split()[0] not in job_date:
                    job_date.append(temp_job_date.split()[0])
            
        # All List > Job list의 Job date가 최근 1년 이내의 job 인지 확인
        try:
            for i in job_date:
                assert int((today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or int(str((today - relativedelta(years=1)) - datetime.strptime(i, '%Y-%m-%d')).split()[0]) <= 0
        except:
            testResult = "failed"
            reason.append("4 steps failed\n")

        print("ITR-11: Search Filter > Job Date")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # Job Date 결과 전송
        result = ' '.join(s for s in reason)
        if testResult == 'failed':
            testlink.reportTCResult(1603, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1603, testPlanID, buildName, 'p', "Job Date Passed")

    def Patient_Location():
        testResult = ''
        reason = list()

        # 1 steps start! : Patient Location 조건을 InPatient로 선택한 후, Search 버튼을 클릭한다.
        # 2 steps start! : Patient Location 조건을 OutPatient로 선택한 후, Search 버튼을 클릭한다.
        # 3 steps start! : Patient Location 조건을 Emergency로 선택한 후, Search 버튼을 클릭한다.
        location_type = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[5]/div/div/ul/li[2]','I'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[5]/div/div/ul/li[3]','O'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[5]/div/div/ul/li[4]','E']]

        # All List 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        for j in range(0,3):
            # Patient Location 버튼 클릭
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[5]/div/a").click()
            
            # Patient Location을 InPatient, OutPatient, Emergency 순서대로 선택
            driver.find_element(By.XPATH,location_type[j][0]).click()
            
            # Showing entries 100으로 변경
            select = Select(driver.find_element(By.CSS_SELECTOR,"#refer-assigned-list_length > label > select"))                
            select.select_by_value("100")

            # Search All 버튼 클릭
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

            # Showing entries 결과 저장 후, page 계산
            temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
            temp_cnt = temp_cnt.split()
            list_cnt = temp_cnt[5]
            pages = math.ceil(int(list_cnt) / 100)

            while pages > 0:
                # All list > Job list에서 Patient Location 저장
                time.sleep(1)
                request = driver.wait_for_request('.*/GetAllList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]
                pat_location = []
            
                for i in data:
                    if i["PatientLocation"] not in pat_location:
                        pat_location.append(i["PatientLocation"])
                pages = pages - 1
            
            # 선택한 Patient Location과 Job list의 Patient Location이 일치하는지 확인
            try:
                for i in pat_location:
                    assert i == location_type[j][1]
            except:
                testResult = "failed"
                reason.append(j+ " steps failed\n")

        print("ITR-12: Search Filter > Patient Location")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # Patient Location 결과 전송
        result = ' '.join(s for s in reason)
        if testResult == 'failed':
            testlink.reportTCResult(1608, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1608, testPlanID, buildName, 'p', "Patient Location Passed")

    def Patient_ID():
        testResult = ''
        reason = list()

        # Refer 탭 클릭(화면 초기화)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
        
        # 1 steps start! : 임의의 Patient ID를 입력하고 Search 버튼을 클릭한다.
        # Test 병원을 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Patient ID를 입력한 후, Search 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div/input").send_keys(test_patient_id)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

        # All Assigned/Not Assigned/All List 탭을 순서대로 클릭하면서 Job list의 해당 Patient ID를 가진 job이 있으면 저장
        tab_list = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]','GetAllAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]','GetNotAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]','GetAllList']]

        pat_id = []
        for i in range(0,3):
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, tab_list[i][0]).click()

            request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for j in data:
                if j["PatientID"] not in pat_id:
                    pat_id.append(j["PatientID"])

        # 검색한 Patient ID와 Job list의 결과와 비교
        try:
            for i in pat_id:
                assert i == test_patient_id
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! : 임의의 Patient ID를 입력하고 Search All 버튼을 클릭한다.
        # Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # Job list의 Patient ID 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        pat_id = []

        for j in data:
            if j["PatientID"] not in pat_id:
                pat_id.append(j["PatientID"])

        # 검색한 Patient ID와 Job list의 결과와 비교
        try:
            for i in pat_id:
                assert i == test_patient_id
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        print("ITR-13: Search Filter > Patient ID")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # Patient ID 결과 전송
        result = ' '.join(s for s in reason)
        if testResult == 'failed':
            testlink.reportTCResult(1615, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1615, testPlanID, buildName, 'p', "Patient ID Passed")

    def Patient_Name():
        testResult = ''
        reason = list()

        # Refer 탭 클릭(화면 초기화)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
        
        # 1 steps start! : 임의의 Patient Name을 입력하고 Search 버튼을 클릭한다.
        # Test 병원을 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Patient Name을 입력한 후, Search 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/input").send_keys(test_patient_name)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

        # All Assigned/Not Assigned/All List 탭을 순서대로 클릭하면서 Job list의 해당 Patient Name을 가진 job이 있으면 저장
        tab_list = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]','GetAllAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]','GetNotAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]','GetAllList']]

        pat_name = []
        for i in range(0,3):
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, tab_list[i][0]).click()

            request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for j in data:
                if j["PatientName"] not in pat_name:
                    pat_name.append(j["PatientName"])

        # 검색한 Patient Name과 Job list의 결과와 비교
        try:
            for i in pat_name:
                assert i == test_patient_name
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # 2 steps start! : 임의의 Patient Name을 입력하고 Search All 버튼을 클릭한다.
        # Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # Job list의 Patient ID 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        pat_name = []

        for j in data:
            if j["PatientName"] not in pat_name:
                pat_name.append(j["PatientName"])

        # 검색한 Patient ID와 Job list의 결과와 비교
        try:
            for i in pat_name:
                assert i == test_patient_name
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        print("ITR-14: Search Filter > Patient Name")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # Patient Name 결과 전송
        result = ' '.join(s for s in reason)
        if testResult == 'failed':
            testlink.reportTCResult(1615, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1615, testPlanID, buildName, 'p', "Patient Name Passed")

    def Age():
        testResult = ''
        reason = list()

        # Refer 탭 클릭(화면 초기화)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : Age 조건을 Year로 선택하고, 임의의 나이를 입력한 후, Search 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()
        
        # Search Filter > All Age를 Year로 변경
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[3]/div/a").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[3]/div/div/ul/li[2]").click()
        
        # Search Filter > end, start age를 랜덤으로 입력 후, Search 버튼 클릭
        start_age = random.randrange(0, 90)
        end_age = random.randrange(start_age, 96)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[4]/input").clear()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[4]/input").send_keys(start_age)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[5]/input").clear()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[5]/input").send_keys(end_age)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

        # All Assigned/Not Assigned/All List 탭을 순서대로 클릭하면서 Job list의 해당 age를 가진 job이 있으면 저장
        tab_list = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]','GetAllAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]','GetNotAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]','GetAllList']]

        age = []
        for i in range(0,3):
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, tab_list[i][0]).click()
            request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]            

            for j in data:
                if j["PatientAge"] not in age:
                    age.append(j["PatientAge"])
        
        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            for i in age:
                assert int(i) >= start_age or int(i) <= end_age
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! : Age 조건을 Month로 선택하고, 임의의 나이를 입력한 후, Search 버튼을 클릭한다.
        # Search Filter > All Age를 Month로 변경
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[3]/div/a").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[3]/div/div/ul/li[3]").click()

        # Search Filter > end, start age를 랜덤으로 입력 후, Search 버튼 클릭
        start_age = random.randrange(0, 90)
        end_age = random.randrange(start_age, 96)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[4]/input").clear()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[4]/input").send_keys(start_age*12)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[5]/input").clear()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[5]/input").send_keys(end_age*12)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

        # All Assigned/Not Assigned/All List 탭을 순서대로 클릭하면서 Job list의 해당 age를 가진 job이 있으면 저장
        tab_list = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]','GetAllAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]','GetNotAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]','GetAllList']]
        
        age = []
        for i in range(0,3):
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, tab_list[i][0]).click()
            request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for j in data:
                if j["PatientAge"] not in age:
                    age.append(j["PatientAge"])
        
        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            for i in age:
                assert int(i) >= start_age or int(i) <= end_age
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # 3 steps start! : Age 조건을 Day로 선택하고, 임의의 나이를 입력한 후, Search 버튼을 클릭한다.
        # Search Filter > All Age를 Day로 변경
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[3]/div/a").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[3]/div/div/ul/li[4]").click()

        # end, start age를 랜덤으로 입력 후, Search 버튼 클릭
        start_age = random.randrange(0, 90)
        end_age = random.randrange(start_age, 96)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[4]/input").clear()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[4]/input").send_keys(start_age*365)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[5]/input").clear()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[5]/input").send_keys(end_age*365)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

        # All Assigned/Not Assigned/All List 탭을 순서대로 클릭하면서 Job list의 해당 age를 가진 job이 있으면 저장
        tab_list = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]','GetAllAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]','GetNotAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]','GetAllList']]
        
        age = []
        for i in range(0,3):
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, tab_list[i][0]).click()
            request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for j in data:
                if j["PatientAge"] not in age:
                    age.append(j["PatientAge"])
        
        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            for i in age:
                assert int(i) >= start_age or int(i) <= end_age
        except:
            testResult = "failed"
            reason.append("3 steps failed\n")

        print("ITR-15: Search Filter > Age")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # Age 결과 전송
        result = ' '.join(s for s in reason)
        if testResult == 'failed':
            testlink.reportTCResult(1615, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1615, testPlanID, buildName, 'p', "Age Passed")

    def Study_Description():
        testResult = ''
        reason = list()

        # Refer 탭 클릭(화면 초기화)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : 임의의 Study Description을 입력한 후, Search 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Search Filter > Study Description 입력 후, Search 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div/div/input").send_keys(test_study_description)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

        # All Assigned/Not Assigned/All List 탭을 순서대로 클릭하면서 Job list의 해당 StudyDescription을 가진 job이 있으면 저장
        tab_list = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]','GetAllAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]','GetNotAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]','GetAllList']]
        
        study_desc = []
        for i in range(0,3):
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, tab_list[i][0]).click()
            request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for j in data:
                if j["StudyDesc"] not in study_desc:
                    study_desc.append(j["StudyDesc"])

        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            for i in study_desc:
                assert test_study_description in i.upper()
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        print("ITR-16: Search Filter > Study Description")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # Study Description 결과 전송
        result = ' '.join(s for s in reason)
        if testResult == 'failed':
            testlink.reportTCResult(1629, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1629, testPlanID, buildName, 'p', "Study Description Passed")

    def Modality():
        testResult = ''
        reason = list()

        signInOut.admin_sign_in()

        # Refer 탭 클릭(화면 초기화)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : 임의의 Modality를 입력한 후, Search 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Search filter > Modality를 입력한 후, Search 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div/div/input").send_keys(test_modality)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

        # All Assigned/Not Assigned/All List 탭을 순서대로 클릭하면서 Job list의 해당 StudyDescription을 가진 job이 있으면 저장
        tab_list = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]','GetAllAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]','GetNotAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]','GetAllList']]
        
        modality = []
        for i in range(0,3):
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, tab_list[i][0]).click()
            request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for j in data:
                if j["Modality"] not in modality:
                    modality.append(j["Modality"])

        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            for i in modality:
                assert i == test_modality
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        print("ITR-17: Search Filter > Modality")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # Modality 결과 전송
        result = ' '.join(s for s in reason)
        if testResult == 'failed':
            testlink.reportTCResult(1629, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1629, testPlanID, buildName, 'p', "Modality Passed")

    def Bodypart():
        







# Sign.Sign_InOut()
# Sign.Rememeber_Me()
# Topbar.Search_Schedule_List()
# Refer.Hospital_List()
# Refer.Reporter_List()
# Search_filter.Priority()
# Search_filter.Job_Status()
# Search_filter.Date()
# Search_filter.Patient_Location()
# Search_filter.Patient_ID()
# Search_filter.Patient_Name()
# Search_filter.Age()
# Search_filter.Study_Description()
# Search_filter.Modality()
Search_filter.Bodypart()
