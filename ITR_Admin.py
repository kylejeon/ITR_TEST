from types import NoneType
from testlink import TestlinkAPIClient, TestLinkHelper
# from bs4 import BeautifulSoup
# from urllib.parse import quote_plus
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import json
from selenium.webdriver.support.ui import Select
import math
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random
import cx_Oracle
import os
import pandas as pd
import string

# import ITR_Admin_Common

# TestLink User: kyle
URL = 'http://testserver-win:81/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
DevKey = 'adcb86843d0c77e6e0c9950f80a143c0'

# TestLink 초기화
tl_helper = TestLinkHelper()
testlink = tl_helper.connect(TestlinkAPIClient) 
testlink.__init__(URL, DevKey)
testlink.checkDevKey()

# 브라우저 설정
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
# baseUrl = 'http://stagingadmin.onpacs.com'
baseUrl = 'http://vm-onpacs:8082'
# html = requests.get(baseUrl)
# soup = BeautifulSoup(html.text, 'html.parser')
# url = baseUrl + quote_plus(plusUrl)
driver.get(baseUrl)


# Notice 창 닫기
popup = driver.window_handles
while len(popup) != 1:
    driver.switch_to.window(popup[1])
    #driver.close()
    driver.find_element(By.ID, "notice_modal_cancel_week").click()
    popup = driver.window_handles
driver.switch_to.window(popup[0])
# html = driver.page_source
# soup = BeautifulSoup(html)
# result_list = []

# TestPlanID = AutoTest 버전 테스트
testPlanID = 2996
buildName = 1

# 테스트 계정
adminID = 'testAdmin'
adminPW = 'Server123!@#'
subadminID = 'testSubadmin'
subadminPW = 'Server123!@#'
reporterID = 'testReporter'
reporterPW = 'Server123!@#'

# 공통 변수
today = datetime.now()
test_hospital = "Cloud Team"
test_hospital_code = '997'

class Common:
    def refer_show_entries(num):
        select = Select(driver.find_element(By.CSS_SELECTOR,"#refer-assigned-list_length > label > select"))                
        select.select_by_value(str(num))
    def config_show_entries(num):
        select = Select(driver.find_element(By.CSS_SELECTOR,"#download-list_length > label > select"))
        select.select_by_value(str(num))
    def cnt_pages():
        # 현재 Job list 페이지의 job count 리턴
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[5]
        pages = math.ceil(int(list_cnt) / 100)
        return pages

class signInOut:
    def admin_sign_in():
        driver.find_element(By.ID, 'user-id').clear()
        driver.find_element(By.ID, 'user-id').send_keys(adminID)
        driver.find_element(By.ID, 'user-password').send_keys(adminPW)
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)
    def admin_sign_out():
        driver.find_element(By.CSS_SELECTOR, '.pull-right > span').click()
    def subadmin_sign_in():
        driver.find_element(By.ID, 'user-id').clear()
        driver.find_element(By.ID, 'user-id').send_keys(subadminID)
        driver.find_element(By.ID, 'user-password').send_keys(subadminPW)
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)
    def subadmin_sign_out():
        driver.find_element(By.CSS_SELECTOR, '.pull-right > span').click()

class windowSize:
    driver.set_window_size(1920, 1080)

class Sign:
    def Sign_InOut():
        print("ITR-1: Sign > Sign In/Out")
        testResult = ''
        reason = list()       
        
        # 2 steps start! : user ID와 password를 입력하지 않고 sign in을 클릭한다
        # user ID와 password를 입력하지 않고 sign in을 클릭한다
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[3]/div/input").send_keys("")
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/input").send_keys("")
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, '.btn').click()

        # 오류 메시지 확인: This field is required.
        try:
            assert driver.find_element(By.ID, "user-id-error").text == "This field is required."
        except:
            testResult = 'failed'
            reason.append("Sign_InOut step 2 isn't valid")    
        
        # 3 steps start! : 잘못된 user ID를 입력하고 sign in을 클릭한다
        # 잘못된 user ID와 Password를 입력하고 sign in을 클릭한다
        strings = string.ascii_letters
        userid = ""
        for i in range(8):
            userid += random.choice(strings)
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[3]/div/input").send_keys(userid)
        time.sleep(0.5)
        
        digits = string.digits
        pw = ""
        for i in range(8):
            pw += random.choice(digits)
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/input").send_keys(pw)
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        
        # 오류 메시지 확인: User not found
        try:
            assert driver.find_element(By.CSS_SELECTOR, ".validation-summary-errors > ul > li").text == "User not found"
        except:
            testResult = 'failed'
            reason.append("Sign_InOut step 3 isn't valid")
        
        # 4 steps start! : password 미입력 하고 sign in을 클릭한다 
        # password 미입력 하고 sign in을 클릭한다        
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[3]/div/input").clear()
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[3]/div/input").send_keys(adminID)
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/input").clear()
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/input").send_keys("")
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, '.btn').click()

        # 오류 메시지 확인: This field is required.
        try:
           assert driver.find_element(By.ID, "user-password-error").text == "This field is required."
        except:
            testResult = 'failed'
            reason.append("Sign_InOut step 3 isn't valid")
        
        # 4 steps start! : admin 유저가 아닌 계정으로 로그인 한다.
        # admin 유저가 아닌 계정으로 로그인 한다.    
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[3]/div/input").clear()    
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[3]/div/input").send_keys(reporterID)
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/input").clear()
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/input").send_keys(reporterPW)
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, '.btn').click()

        # 오류 메시지 확인: not admin user
        try:
            assert driver.find_element(By.CSS_SELECTOR, ".validation-summary-errors >  ul > li").text == "Not admin user"
        except:
            testResult = 'failed'
            reason.append("Sign_InOut step 4 isn't valid")
        
        # 5 steps start! : 정상적인 계정으로 로그인 한다.
        # 정상적인 계정으로 로그인 한다.
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[3]/div/input").clear()   
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[3]/div/input").send_keys(adminID)
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/input").clear()
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/input").send_keys(adminPW)
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)        

        # 정상적으로 로그인 되었는지 확인
        try:
            assert driver.find_element(By.CSS_SELECTOR, ".pull-right > span").text == "Sign Out"
        except:
            testResult = 'failed'
            reason.append("Sign_InOut step 5 isn't valid")
        
        # sign_InOut 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1531, testPlanID, buildName, 'f', result)            
        else:
            testlink.reportTCResult(1531, testPlanID, buildName, 'p', "Sign In/Out Test Passed")
        driver.find_element(By.CSS_SELECTOR, ".pull-right > span").click()
        driver.implicitly_wait(3)
    
    def Rememeber_Me():
        print("ITR-2: Sign > Remember Me")
        testResult = ''
        reason = list() 
        
        # 1 steps start! : User ID와 User Password를 입력하고, Remember Me를 체크한 후, Sign In을 클릭한다.
        # 정상적인 계정을 입력 및 remind me를 체크하고 로그인 한다.
        driver.find_element(By.ID, 'user-id').clear()
        driver.find_element(By.ID, 'user-id').send_keys(adminID)
        driver.find_element(By.ID, 'user-password').send_keys(adminPW)
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, '.col-xs-8.p-t-5 > label').click()
        driver.find_element(By.CSS_SELECTOR, '.btn').click()         
        driver.implicitly_wait(3)                       
        
        # 로그아웃 후, 마지막에 접속한 User ID와 Remind Me 체크 상태를 확인한다.
        signInOut.admin_sign_out()        
        try:
            assert (driver.find_element(By.ID, 'user-id').get_property("value"), driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/form/div[5]/div[1]/input').get_property('checked')) == (adminID, True)
        except:
            testResult = 'failed' 
            reason.append("1 Steps failed")
        
        # Remember_Me 결과 전송       
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1538, testPlanID, buildName, 'f', result)            
        else:
            testlink.reportTCResult(1538, testPlanID, buildName, 'p', "Remember Me Test Passed")    

class Topbar:
    def Search_Schedule_List():
        print("ITR-3: Topbar > Search Schedule List")
        testResult = '' 
        reason = list() 
        
        signInOut.admin_sign_in()

        # 1 steps start! : 상단의 Schedule badge를 클릭하고, Schedule 개수를 확인한다.
        # 상단의 Schedule badge를 클릭하고, Schedule 개수를 확인한다.
        time.sleep(3)
        driver.find_element(By.ID, 'schedule_info_box').click()
        sch_info_num = driver.find_element(By.ID, 'schedule_info_number').text
        sch_info_num = sch_info_num.split('/')
        refer_sch_num, sch_num = sch_info_num[0], sch_info_num[1].strip()
        time.sleep(3)

        # Hospital list에서 schedule count 저장
        hospitals = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        hospital_list = []
        for i in hospitals:
            hospital_list.append((i.get_property("dataset"))["institutionCode"])
        
        hospital_schedule_cnt = int()
        not_refer_joblist_cnt = int()
        all_joblist_cnt = int()
        for i in hospital_list:
            try:
                # 병원 리스트에서 Schedule badge의 count 저장
                temp_schedule_cnt = driver.find_element(By.CSS_SELECTOR, "#list-institution-row-"+str(i)+" > span:nth-child(1) > span").get_property("textContent")
                hospital_schedule_cnt += int((temp_schedule_cnt.split())[2])
                
                # Schedule이 있는 병원 선택
                driver.find_element(By.CSS_SELECTOR, "#list-institution-row-"+str(i)).click()
                
                # All Assigned List 탭 클릭
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()
                time.sleep(1)         
                
                # All Assigned List > Showing entry 결과 저장
                temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
                all_joblist_cnt += int((temp_cnt.split())[5])

                # Not Assigned List 탭 클릭
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

                # Not Assigned List > Showing entry 결과 저장
                time.sleep(1)
                temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
                all_joblist_cnt += int((temp_cnt.split())[5])
                not_refer_joblist_cnt += int((temp_cnt.split())[5])

                # All Assigned List 탭 클릭
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()
                time.sleep(1)
            except:
                continue

        # Schedule badge의 schedule 개수와 조회 결과 리스트의 schedule 개수를 비교한다.              
        try:
            assert int(sch_num) == all_joblist_cnt == hospital_schedule_cnt
        except:
            testResult = 'failed'
            reason.append("1 steps failed")
        
        # Schedule badge의 refer된 schedule 개수와 조회 결과 리스트의 refer된 schedule 개수를 비교한다.        
        try:
            assert int(refer_sch_num) == not_refer_joblist_cnt
        except:
            testResult = 'failed'
            reason.append("2 steps failed")

        # Searh_Schedule_List 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1542, testPlanID, buildName, 'f', result)            
        else:
            testlink.reportTCResult(1542, testPlanID, buildName, 'p', "Search_Schedule_List Test Passed")  

class Refer:
    def Hospital_List():
        print("ITR-7: Refer > Hospital List")
        testResult = ''
        reason = list() 

        # Refer 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
        time.sleep(1)

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
                emer_reporter_list_cnt = int()
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
                            temp_emer_reporter = (emer_reporter_key.split(','))
                            for j in temp_emer_reporter:
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
                    
                # 병원 리스트의 Refer badge count와 Job list의 refer job list 개수 확인
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

        # Hospital_List 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1567, testPlanID, buildName, 'f', result)            
        else:
            testlink.reportTCResult(1567, testPlanID, buildName, 'p', "Hospital_List Test Passed")  

    def Reporter_List():
        print("ITR-8: Refer > Reporter List")
        testResult = ''
        reason = list()        

        # 1 & 2 steps start! : 판독의 탭 > 판독의 리스트에 표시되는 badge count가 job list와 일치하는지 확인
        # Reporter list를 저장한다.
        driver.find_element(By.XPATH, "//*[@id='tab-reporter']").click()
        request = driver.wait_for_request('.*/GetReferCountsByReporter.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        reporter_cnt = len(data)

        reporter_list = []
        for i in data:
            reporter_list.append(i["ReporterKey"])

        # 판독의 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/li[2]").click()
        time.sleep(1)
        
        # 각 reporter의 refer, emergency, schedule job의 건수를 비교한다.
        if reporter_cnt > 0:
            n = 0
            for i in data:                
                proirity_cnt = i['PriorityCount']
                refer_cnt = i['ReferCount']
                schedule_cnt = i['ScheduleCount']
                
                # Tap panel의 refer count와 조회 결과 리스트에서의 refer count를 비교한다.
                del driver.requests
                driver.find_element(By.CSS_SELECTOR, "#list-reporter-row-"+str(reporter_list[n])).click()
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
                priority = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div/a/span").get_property("textContent")
                if priority == "응급":
                    driver.find_element(By.CSS_SELECTOR, "#refer_search_priority_chosen span").click()
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/ul/li[1]").click()

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

        # Reporter_List 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1577, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1577, testPlanID, buildName, 'p', "Reporter List Passed")
    
class Search_filter:
    def Priority():
        print("ITR-9: Search Filter > Priority")
        testResult = ''
        reason = list()

        # 1 steps start! : Priority 조건을 응급으로 선택한 후, Search 버튼 클릭
        # Refer 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Hospital list 저장
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        hospital_cnt = len(hospital_list)

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)
        
        # 순서대로 Hospital 선택
        if hospital_cnt > 0:
            n = 0

            while n < hospital_cnt:
                # Hospital list 저장 및 병원 순서대로 클릭
                hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
                time.sleep(1)
                hospital_list[n].click()
        
                # 병원 선택 > All Assigned List > Priority 드랍박스에서 응급을 선택 후, Search 버튼 클릭
                time.sleep(1)
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div").click()                
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/ul/li[2]").click()
                del driver.requests
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

                # 병원 선택 > All Assigned List > Job list 저장
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/GetAllAssignedList.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]
                    job_priority = []

                    for i in data:
                        if i["JobPriority"] not in job_priority:
                            job_priority.append(i["JobPriority"])
                    # Next 클릭
                    next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                    if "disabled" not in next_btn.get_attribute("class"):
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                    pages = pages - 1  

                # Not Assigned List 탭 클릭
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()
                
                # 병원 선택 > Not Assigned List > Job list 저장
                time.sleep(1)
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/GetNotAssignedList.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]

                    for i in data:
                        if i["JobPriority"] not in job_priority:
                            job_priority.append(i["JobPriority"])
                    # Next 클릭
                    next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                    if "disabled" not in next_btn.get_attribute("class"):
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                    pages = pages - 1  

                # 병원 선택 > Job list에서 응급만 표시되는지 확인
                try:
                    job_priority = ' '.join(s for s in job_priority)
                    assert job_priority == "E"
                except:
                    testResult = "failed"
                    reason.append("1 steps failed")
                n = n + 1
                # All Assigned List 탭 클릭
                time.sleep(1)
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
                time.sleep(1)
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/GetNotAssignedList.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]

                    for i in data:
                        if i["JobPriority"] not in job_priority:
                            job_priority.append(i["JobPriority"])
                    # Next 클릭
                    next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                    if "disabled" not in next_btn.get_attribute("class"):
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                    pages = pages - 1  
                
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

        # Priority 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1583, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1583, testPlanID, buildName, 'p', "Priority Passed")

    def Job_Status():
        print("ITR-10: Search Filter > Job Status")
        testResult = ''
        reason = list()

        # 1 steps start! : Job Status를 Requested로 선택한 후, Search All버튼을 클릭한다.
        # All List 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)

        # All List > Job Status를 Requested로 변경하고, Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[2]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # All List > Job list의 Job Status 저장
        pages = Common.cnt_pages()
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_status = []

            for i in data:
                if i["StatDescription"] not in job_status:
                    job_status.append(i["StatDescription"])
            
            # Next 클릭
            next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
            if "disabled" not in next_btn.get_attribute("class"):
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
            pages = pages - 1  

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
        driver.refresh()
        # All List 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/a").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[3]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # All List > Job list의 Job Status 저장
        pages = Common.cnt_pages()
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_status = []

            for i in data:
                if i["StatDescription"] not in job_status:
                    job_status.append(i["StatDescription"])
            # Next 클릭
            next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
            if "disabled" not in next_btn.get_attribute("class"):
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
            pages = pages - 1

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
        pages = Common.cnt_pages()
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_status = []

            for i in data:
                if i["StatDescription"] not in job_status:
                    job_status.append(i["StatDescription"])
            # Next 클릭
            next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
            if "disabled" not in next_btn.get_attribute("class"):
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
            pages = pages - 1

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
        pages = Common.cnt_pages()
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_status = []

            for i in data:
                if i["StatDescription"] not in job_status:
                    job_status.append(i["StatDescription"])
            # Next 클릭
            next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
            if "disabled" not in next_btn.get_attribute("class"):
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
            pages = pages - 1

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
        # pages = Common.cnt_pages()
        # while pages > 0:
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_status = []

        for i in data:
            if i["StatDescription"] not in job_status:
                job_status.append(i["StatDescription"])
        
        # Next 클릭
        if len(data) == 100:
            next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
            if "disabled" not in next_btn.get_attribute("class"):
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
            # pages = pages - 1

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
        time.sleep(1)
        pages = Common.cnt_pages()
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_status = []

            for i in data:
                if i["StatDescription"] not in job_status:
                    job_status.append(i["StatDescription"])
            # Next 클릭
            next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
            if "disabled" not in next_btn.get_attribute("class"):
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
            pages = pages - 1

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
        pages = Common.cnt_pages()
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_status = []

            for i in data:
                if i["StatDescription"] not in job_status:
                    job_status.append(i["StatDescription"])
            # Next 클릭
            next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
            if "disabled" not in next_btn.get_attribute("class"):
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
            pages = pages - 1

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
        time.sleep(1)
        pages = Common.cnt_pages()
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_status = []

            for i in data:
                if i["StatDescription"] not in job_status:
                    job_status.append(i["StatDescription"])
            # Next 클릭
            next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
            if "disabled" not in next_btn.get_attribute("class"):
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
            pages = pages - 1

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
        pages = Common.cnt_pages()
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_status = []

            for i in data:
                if i["StatDescription"] not in job_status:
                    job_status.append(i["StatDescription"])
            # Next 클릭
            next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
            if "disabled" not in next_btn.get_attribute("class"):
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
            pages = pages - 1

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
        pages = Common.cnt_pages()
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_status = []

            for i in data:
                if i["StatDescription"] not in job_status:
                    job_status.append(i["StatDescription"])
            # Next 클릭
            next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
            if "disabled" not in next_btn.get_attribute("class"):
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
            pages = pages - 1

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
        pages = Common.cnt_pages()
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_status = []

            for i in data:
                if i["StatDescription"] not in job_status:
                    job_status.append(i["StatDescription"])
            # Next 클릭
            next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
            if "disabled" not in next_btn.get_attribute("class"):
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
            pages = pages - 1

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
        pages = Common.cnt_pages()
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_status = []

            for i in data:
                if i["StatDescription"] not in job_status:
                    job_status.append(i["StatDescription"])
            # Next 클릭
            next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
            if "disabled" not in next_btn.get_attribute("class"):
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
            pages = pages - 1

        # Job Status가 DiscardCompleted 만 조회되었는지 확인
        try:
            job_status = ' '.join(s for s in job_status)
            assert job_status == "DiscardCompleted" or job_status == ''
        except:
            testResult = "failed"
            reason.append("12 steps failed\n")

        # Priority 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1588, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1588, testPlanID, buildName, 'p', "Job Status Passed")
    
    def Date():
        print("ITR-11: Search Filter > Job Date")
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

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)

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
            pages = Common.cnt_pages()
            while pages > 0:
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
                # Next 클릭
                next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                if "disabled" not in next_btn.get_attribute("class"):
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                pages = pages - 1
            
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

            # Showing entries 100으로 변경
            Common.refer_show_entries(100)

            # All Assigned List > Job list의 결과 저장
            pages = Common.cnt_pages()
            while pages > 0:
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
                # Next 클릭
                next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                if "disabled" not in next_btn.get_attribute("class"):
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                pages = pages - 1

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
                
                # Showing entries 100으로 변경
                Common.refer_show_entries(100)
                
                # All Assigned List > Job list의 결과 저장
                pages = Common.cnt_pages()
                while pages > 0:
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
                    # Next 클릭
                    next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                    if "disabled" not in next_btn.get_attribute("class"):
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                    pages = pages - 1

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

                # Showing entries 100으로 변경
                Common.refer_show_entries(100)
            
                # All Assigned List > Job list의 결과 저장
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/GetAllAssignedList.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]
                    job_date = []

                    if data != '':
                        for i in data:
                            temp_job_date = i[date_type[j][1]]
                            if temp_job_date.split()[0] not in job_date:
                                job_date.append(temp_job_date.split()[0])
                    # Next 클릭
                    next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                    if "disabled" not in next_btn.get_attribute("class"):
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                    pages = pages - 1

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
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[3]/div").click()
            driver.find_element(By.XPATH, date_type[j][0]).click()

            # Start Date를 Yesterday로 선택
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[4]/div/div[1]/input").click()
            driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(1) > th:nth-child(1)").click()

            # Search 버튼 클릭
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

            # Showing entries 100으로 변경
            Common.refer_show_entries(100)

            # Not Assigned List > Job list의 결과 저장
            pages = Common.cnt_pages()
            while pages > 0:
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
                # Next 클릭
                next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                if "disabled" not in next_btn.get_attribute("class"):
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                pages = pages - 1
            
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

            # Showing entries 100으로 변경
            Common.refer_show_entries(100)

            # Not Assigned List > Job list의 결과 저장
            pages = Common.cnt_pages()
            while pages > 0:
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
                # Next 클릭
                next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                if "disabled" not in next_btn.get_attribute("class"):
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                pages = pages - 1

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

                # Showing entries 100으로 변경
                Common.refer_show_entries(100)
                
                # Not Assigned List > Job list의 결과 저장
                pages = Common.cnt_pages()
                while pages > 0:
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
                    # Next 클릭
                    next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                    if "disabled" not in next_btn.get_attribute("class"):
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                    pages = pages - 1

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

                # Showing entries 100으로 변경
                Common.refer_show_entries(100)
            
                # Not Assigned List > Job list의 결과 저장
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/GetNotAssignedList.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]
                    job_date = []

                    if data != '':
                        for i in data:
                            temp_job_date = i[date_type[j][1]]
                            if temp_job_date.split()[0] not in job_date:
                                job_date.append(temp_job_date.split()[0])
                    # Next 클릭
                    next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                    if "disabled" not in next_btn.get_attribute("class"):
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                    pages = pages - 1

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

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)

        # All List > Date Type의 Job Date 인지 확인
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[3]/div/a").get_property("textContent") != "Job Date":
            testResult = "4 steps failed\n"

        # All List > Date 기간이 오늘날짜부터 과거 1년으로 설정되어 있는지 확인
        start_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[4]/div/div[1]/input").get_property("value")
        end_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[4]/div/div[2]/input").get_property("value")
        if (datetime.strptime(start_date, '%Y-%m-%d') - datetime.strptime(end_date, '%Y-%m-%d')).days <= 365:
            testResult = '4 steps failed'
        
        # All List > Job list의 job date를 저장
        pages = Common.cnt_pages()
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            job_date = []

            if data != '':
                for i in data:
                    temp_job_date = i['JobDTTMString']
                    if temp_job_date.split()[0] not in job_date:
                        job_date.append(temp_job_date.split()[0])
            # Next 클릭
            next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
            if "disabled" not in next_btn.get_attribute("class"):
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
            pages = pages - 1
            
        # All List > Job list의 Job date가 최근 1년 이내의 job 인지 확인
        try:
            for i in job_date:
                assert int((today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or int(str((today - relativedelta(years=1)) - datetime.strptime(i, '%Y-%m-%d')).split()[0]) <= 0
        except:
            testResult = "failed"
            reason.append("4 steps failed\n")

        # Job Date 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1603, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1603, testPlanID, buildName, 'p', "Job Date Passed")

    def Patient_Location():
        print("ITR-12: Search Filter > Patient Location")
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
            Common.refer_show_entries(100)

            # Search All 버튼 클릭
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

            pages = Common.cnt_pages()
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
                # Next 클릭
                next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                if "disabled" not in next_btn.get_attribute("class"):
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                pages = pages - 1
            
            # 선택한 Patient Location과 Job list의 Patient Location이 일치하는지 확인
            try:
                for i in pat_location:
                    assert i == location_type[j][1]
            except:
                testResult = "failed"
                reason.append(j+ " steps failed\n")
        
        # Patient Location 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1608, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1608, testPlanID, buildName, 'p', "Patient Location Passed")

    def Patient_ID():
        print("ITR-13: Search Filter > Patient ID")
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

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)

        # All Assigned/Not Assigned/All List 탭을 순서대로 클릭하면서 Job list의 해당 Patient ID를 가진 job이 있으면 저장
        tab_list = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]','GetAllAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]','GetNotAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]','GetAllList']]

        pat_id = ''
        while True:
            result_pat_id = []
            for i in range(0,3):
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, tab_list[i][0]).click()
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]

                    for j in data:
                        if j["PatientID"] not in result_pat_id:
                            result_pat_id.append(j["PatientID"])
                    # Next 클릭
                    next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                    if "disabled" not in next_btn.get_attribute("class"):
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                    pages = pages - 1

            if pat_id == '':
                # Job list에서 임의의 Patient ID를 선택
                pat_id = random.choice(result_pat_id)

                # Search filter > Patient ID를 입력한 후, Search 버튼 클릭
                if type(pat_id) != NoneType:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div/input").send_keys(pat_id)
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                # Patient ID가 모두 Null 인 경우
                else:
                    break
            else:
                break

        # 검색한 Patient ID와 Job list의 결과와 비교
        try:
            if type(pat_id) != NoneType:
                result_pat_id = ' '.join(s for s in result_pat_id)
            assert pat_id == result_pat_id or type(pat_id) == NoneType
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! : 임의의 Patient ID를 입력하고 Search All 버튼을 클릭한다.
        # Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)

        # Job list의 Patient ID 저장
        pages = Common.cnt_pages()
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            result_pat_id = []

            for j in data:
                if j["PatientID"] not in result_pat_id:
                    result_pat_id.append(j["PatientID"])
            # Next 클릭
            next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
            if "disabled" not in next_btn.get_attribute("class"):
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
            pages = pages - 1

        # 검색한 Patient ID와 Job list의 결과와 비교
        try:
            if type(pat_id) != NoneType:
                result_pat_id = ' '.join(s for s in result_pat_id)
            assert pat_id == result_pat_id or type(pat_id) == NoneType
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # Patient ID 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1615, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1615, testPlanID, buildName, 'p', "Patient ID Passed")

    def Patient_Name():
        print("ITR-14: Search Filter > Patient Name")
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

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)

        # All Assigned/Not Assigned/All List 탭을 순서대로 클릭하면서 Job list의 해당 Patient Name을 가진 job이 있으면 저장
        tab_list = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]','GetAllAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]','GetNotAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]','GetAllList']]

        pat_name = ''
        while True:
            result_pat_name = []
            for i in range(0,3):
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, tab_list[i][0]).click()
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]

                    for j in data:
                        if j["PatientName"] not in result_pat_name:
                            result_pat_name.append(j["PatientName"])
                    # Next 클릭
                    next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                    if "disabled" not in next_btn.get_attribute("class"):
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                    pages = pages - 1

            if pat_name == '':
                # Job list에서 임의의 Patient_Name을 선택
                pat_name = random.choice(result_pat_name)

                # Search filter > Patient_Name을 입력한 후, Search 버튼 클릭
                if type(pat_name) != NoneType:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/input").send_keys(pat_name)
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                # Patient_Name이 모두 Null 인 경우
                else:
                    break
            else:
                break

        # 검색한 Patient Name과 Job list의 결과와 비교
        try:
            if type(pat_name) != NoneType:
                result_pat_name = ' '.join(s for s in result_pat_name)
            assert pat_name == result_pat_name or type(pat_name) == NoneType
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # 2 steps start! : 임의의 Patient Name을 입력하고 Search All 버튼을 클릭한다.
        # Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()
        
        # Showing entries 100으로 변경
        Common.refer_show_entries(100)

        # Job list의 Patient Name 저장
        pages = Common.cnt_pages()
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            result_pat_name = []

            for j in data:
                if j["PatientName"] not in result_pat_name:
                    result_pat_name.append(j["PatientName"])
            # Next 클릭
            next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
            if "disabled" not in next_btn.get_attribute("class"):
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
            pages = pages - 1

        # 검색한 Patient ID와 Job list의 결과와 비교
        try:
            if type(pat_name) != NoneType:
                result_pat_name = ' '.join(s for s in result_pat_name)
            assert pat_name == result_pat_name or type(pat_name) == NoneType
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # Patient Name 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1619, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1619, testPlanID, buildName, 'p', "Patient Name Passed")

    def Age():
        print("ITR-15: Search Filter > Age")
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

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)
        
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
            pages = Common.cnt_pages()
            while pages > 0:
                request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]            

                for j in data:
                    if j["PatientAge"] not in age:
                        age.append(j["PatientAge"])
                # Next 클릭
                next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                if "disabled" not in next_btn.get_attribute("class"):
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                pages = pages - 1

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

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)

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
            pages = Common.cnt_pages()
            while pages > 0:
                request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for j in data:
                    if j["PatientAge"] not in age:
                        age.append(j["PatientAge"])
                # Next 클릭
                next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                if "disabled" not in next_btn.get_attribute("class"):
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                pages = pages - 1
        
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

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)

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
            pages = Common.cnt_pages()
            while pages > 0:
                request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for j in data:
                    if j["PatientAge"] not in age:
                        age.append(j["PatientAge"])
                # Next 클릭
                next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                if "disabled" not in next_btn.get_attribute("class"):
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                pages = pages - 1

        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            for i in age:
                assert int(i) >= start_age or int(i) <= end_age
        except:
            testResult = "failed"
            reason.append("3 steps failed\n")

        # Age 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1623, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1623, testPlanID, buildName, 'p', "Age Passed")

    def Study_Description():
        print("ITR-16: Search Filter > Study Description")
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

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)
        
        # All Assigned/Not Assigned/All List 탭을 순서대로 클릭하면서 Job list의 해당 StudyDescription을 가진 job이 있으면 저장
        tab_list = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]','GetAllAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]','GetNotAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]','GetAllList']]
        
        # Test 병원의 Job list에서 Study Description을 추출 후, 임의의 Study Description을 선택해서 검색
        study_desc = ''
        while True:
            result_study_desc = []
            for i in range(0,3):
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, tab_list[i][0]).click()
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]

                    for j in data:
                        if j["StudyDesc"] not in result_study_desc:
                            result_study_desc.append(j["StudyDesc"])
                    # Next 클릭
                    next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                    if "disabled" not in next_btn.get_attribute("class"):
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                    pages = pages - 1

            if study_desc == '':
                # Job list에서 임의의 Study Description을 선택
                study_desc = random.choice(result_study_desc)

                # Search filter > Study Description을 입력한 후, Search 버튼 클릭
                if type(study_desc) != NoneType:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div/div/input").send_keys(study_desc)
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                # Study Description이 모두 Null 인 경우
                else:
                    break
            else:
                break

        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            if type(study_desc) != NoneType:
                result_study_desc = ' '.join(s for s in result_study_desc)
            assert study_desc == result_study_desc or type(study_desc) == NoneType
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")
        
        # Study Description 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1629, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1629, testPlanID, buildName, 'p', "Study Description Passed")

    def Modality():
        print("ITR-17: Search Filter > Modality")
        testResult = ''
        reason = list()

        # Refer 탭 클릭(화면 초기화)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : 임의의 Modality를 입력한 후, Search 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)
        
        # All Assigned/Not Assigned/All List 탭을 순서대로 클릭하면서 Job list의 해당 Modality를 가진 job이 있으면 저장
        tab_list = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]','GetAllAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]','GetNotAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]','GetAllList']]
        
        modality = ''
        while True:
            result_modality = []
            for i in range(0,3):
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, tab_list[i][0]).click()
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]
                    
                    for j in data:
                        if j["Modality"] not in result_modality:
                            result_modality.append(j["Modality"])
                    # Next 클릭
                    next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                    if "disabled" not in next_btn.get_attribute("class"):
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                    pages = pages - 1
            
            if modality == '':
                # Job list에서 임의의 Modality를 선택
                modality = random.choice(result_modality)

                # Search filter > Modality를 입력한 후, Search 버튼 클릭
                if type(modality) != NoneType:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div/div/input").send_keys(modality)
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                # Modality가 모두 Null 인 경우
                else:
                    break
            else:
                break

        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            if type(modality) != NoneType:
                result_modality = ' '.join(s for s in result_modality)
            assert modality == result_modality or type(modality) == NoneType
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # Modality 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1632, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1632, testPlanID, buildName, 'p', "Modality Passed")

    def Bodypart():
        print("ITR-18: Search Filter > Bodypart")
        testResult = ''
        reason = list()

        # Refer 탭 클릭(화면 초기화)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : 임의의 Bodypart를 입력한 후, Search 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)
        
        # All Assigned/Not Assigned/All List 탭을 순서대로 클릭하면서 Job list의 해당 Bodypart를 가진 job이 있으면 저장
        tab_list = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]','GetAllAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]','GetNotAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]','GetAllList']]

        bodypart = ''
        while True:
            result_bodypart = []
            for i in range(0,3):
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, tab_list[i][0]).click()
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]

                    for j in data:
                        if j["Bodypart"] not in result_bodypart:
                            result_bodypart.append(j["Bodypart"])
                    # Next 클릭
                    next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                    if "disabled" not in next_btn.get_attribute("class"):
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                    pages = pages - 1

            if bodypart == '':
                # Job list에서 임의의 Bodypart를 선택
                bodypart = random.choice(result_bodypart)

                # Search filter > Bodypart를 입력한 후, Search 버튼 클릭
                if type(bodypart) != NoneType:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[3]/div/div/input").send_keys(bodypart)
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                # Bodypart가 모두 Null 인 경우
                else:
                    break
            else:
                break

        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            if type(bodypart) != NoneType:
                result_bodypart = ' '.join(s for s in result_bodypart)
            assert bodypart == result_bodypart or type(bodypart) == NoneType
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # Bodypart 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1635, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1635, testPlanID, buildName, 'p', "Bodypart Passed")

    def Department():
        print("ITR-19: Search Filter > Department")
        testResult = ''
        reason = list()

        # Refer 탭 클릭(화면 초기화)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : 임의의 Department를 입력한 후, Search 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)
        
        # All Assigned/Not Assigned/All List 탭을 순서대로 클릭하면서 Job list의 해당 Department를 가진 job이 있으면 저장
        tab_list = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]','GetAllAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]','GetNotAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]','GetAllList']]

        department = ''
        while True:
            result_department = []
            for i in range(0,3):
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, tab_list[i][0]).click()
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]

                    for j in data:
                        if j["Department"] not in result_department:
                            result_department.append(j["Department"])
                    # Next 클릭
                    next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                    if "disabled" not in next_btn.get_attribute("class"):
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                    pages = pages - 1      

            if department == '':
                # Job list에서 임의의 Department를 선택
                department = random.choice(result_department)

                # Search filter > Department를 입력한 후, Search 버튼 클릭
                if type(department) != NoneType:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[4]/div/div/input").send_keys(department)
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                # Department가 모두 Null 인 경우
                else:
                    break
            else:
                break
                
        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            if type(department) != NoneType:
                result_department = ' '.join(s for s in result_department)
            assert department == result_department or type(department) == NoneType
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")
        
        # Department 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1638, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1638, testPlanID, buildName, 'p', "Department Passed")

    def Request_Name():
        print("ITR-20: Search Filter > Request_Name")
        testResult = ''
        reason = list()

        # Refer 탭 클릭(화면 초기화)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : 임의의 Request Name을 입력한 후, Search 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)
        
        # All Assigned/Not Assigned/All List 탭을 순서대로 클릭하면서 Job list의 해당 Request Name을 가진 job이 있으면 저장
        tab_list = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]','GetAllAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]','GetNotAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]','GetAllList']]
        
        request_name = ''
        while True:
            result_request_name = []
            for i in range(0,3):
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, tab_list[i][0]).click()
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]

                    for j in data:
                        if j["StudyRequestName"] not in result_request_name:
                            result_request_name.append(j["StudyRequestName"])
                    # Next 클릭
                    next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                    if "disabled" not in next_btn.get_attribute("class"):
                        time.sleep(1)
                        driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                    pages = pages - 1    

            if request_name == '':
                # Job list에서 임의의 Request Name을 선택
                request_name = random.choice(result_request_name)

                # Search filter > Request Name을 입력한 후, Search 버튼 클릭
                if type(request_name) != NoneType:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[5]/div/div/input").send_keys(request_name)
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                # Department가 모두 Null 인 경우
                else:
                    break
            else:
                break
            
        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            if type(request_name) != NoneType:
                result_request_name = ' '.join(s for s in result_request_name)
            assert request_name == result_request_name or type(request_name) == NoneType
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # Request Name 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1641, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1641, testPlanID, buildName, 'p', "Request Name Passed")

    def Search_All():
        print("ITR-21: Search Filter > Search All")
        testResult = ''
        reason = list()

        # Refer 탭 클릭(화면 초기화)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
        time.sleep(1)

        # 1 steps start! : 임의의 검색조건을 입력한 후, Search All 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)
        
        # All Assigned/Not Assigned/All List 탭을 순서대로 클릭하면서 Job list의 해당 조건을 가진 job이 있으면 저장
        tab_list = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]','GetAllAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]','GetNotAssignedList'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]','GetAllList']]

        # 검색할 항목을 리스트로 생성
        search_list = [['StudyDesc','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div/div/input'],
        ['Modality','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div/div/input'],
        ['Bodypart','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[3]/div/div/input'],
        ['Department','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[4]/div/div/input'],
        ['StudyRequestName','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[5]/div/div/input']]

        # Search list에서 임의의 Search 조건을 2개 선택
        search_item_1 = ''; search_item_2 = ''
        search_sample_1 = []; search_sample_2 = []; result_sample = []
        search_sample_list = random.sample(search_list, 2)
        
        # 아무런 조건없이 All Assigned/Not Assigned/All List 탭을 이동하면서 조건에 맞는 job list 저장
        for i in range(0,3):
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, tab_list[i][0]).click()
            pages = Common.cnt_pages()
            while pages > 0:
                request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for j in data:
                    if j[search_sample_list[0][0]] not in search_sample_1 and j[search_sample_list[0][0]] != None:
                        search_sample_1.append(j[search_sample_list[0][0]])
          
                # Next 클릭
                next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                if "disabled" not in next_btn.get_attribute("class"):
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                pages = pages - 1
                
        # 저장된 job list에서 첫 번째 Search 조건에 해당하는 임의의 값을 선택
        search_item_1 = random.choice(search_sample_1)

        # Search filter > 임의의 Search condition에 첫 번째 Search 값을 입력한 후, Search All 버튼 클릭
        if type(search_item_1) != NoneType:
            driver.find_element(By.XPATH, search_sample_list[0][1]).send_keys(search_item_1)
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # 첫 번째 Search 조건에 해당하는 job list 저장
        for i in range(0,3):
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, tab_list[i][0]).click()
            pages = Common.cnt_pages()
            while pages > 0:
                request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for j in data:
                    if j[search_sample_list[1][0]] not in search_sample_2 and j[search_sample_list[1][0]] != None:
                        search_sample_2.append(j[search_sample_list[1][0]])

                # Next 클릭
                time.sleep(1)
                next_btn = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next")
                if "disabled" not in next_btn.get_attribute("class"):
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()
                pages = pages - 1
        
        # 조회 결과에서 두 번째 Search 조건에 해당하는 임의의 값을 선택
        search_item_2 = random.choice(search_sample_2)

        # Search filter > 임의의 Search condition에 두 번째 Search 값을 입력한 후, Search All 버튼 클릭
        if type(search_item_2) != NoneType:
            driver.find_element(By.XPATH, search_sample_list[1][1]).send_keys(search_item_2)
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # 첫 번째, 두 번째 Search 조건에 해당하는 job list 저장
        temp_search_1 = []
        temp_search_2 = []
        result_list = []
        for i in range(0,3):
            time.sleep(1)
            del driver.requests
            driver.find_element(By.XPATH, tab_list[i][0]).click()
            pages = Common.cnt_pages()
            while pages > 0:
                request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for j in data:
                    if j[search_sample_list[0][0]] not in temp_search_1 and j[search_sample_list[0][0]] != None:
                        temp_search_1.append(j[search_sample_list[0][0]])
                        result_list.append(temp_search_1)
                    if j[search_sample_list[1][0]] not in temp_search_2 and j[search_sample_list[1][0]] != None:
                        temp_search_2.append(j[search_sample_list[1][0]])
                        result_list.append(temp_search_2)
                pages = pages - 1
                          
        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            result_list_1 = ' '.join(s for s in result_list[0])
            result_list_2 = ' '.join(s for s in result_list[1])
            assert (search_item_1, search_item_2) == (result_list_1, result_list_2)
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # Search All 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1644, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1644, testPlanID, buildName, 'p', "Search All Passed")

    def RealTime():
        print("ITR-22: Search Filter > Real Time")
        testResult = ''
        reason = list()

        # Refer 탭 클릭(화면 초기화)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : Real Time 토글 버튼을 On으로 변경한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # All List 탭으로 이동
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # Show entries를 50개로 변경
        time.sleep(1)
        del driver.requests
        Common.refer_show_entries(50)

        # Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        # Ream Time 토글을 On으로 변경
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[2]/div/div[2]/label/span").click()
        status = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[2]/div/div[2]/label/input").get_property("checked")

        # 35초 대기(자동 새로고침 시간: 30초) 및 기존 데이터 삭제
        time.sleep(35)
        del driver.requests

        # Show entries를 10개로 변경
        Common.refer_show_entries(10)

        # Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        after_data_cnt = len(data)

        # Job list가 새로 고침되었는지 확인
        try:
            assert status == True and after_data_cnt == 10
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! : Real Time 토글 버튼을 Off로 변경한다.
        # Search 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]").click()
        
        # Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        
        # Ream Time 토글을 Off로 변경
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[2]/div/div[2]/label/span").click()

        # Show entries를 25개로 변경
        Common.refer_show_entries(25)
        
        # 35초 대기(자동 새로고침 시간: 30초) 및 기존 데이터 삭제
        time.sleep(35)
        del driver.requests

        # Job list가 새로 고침되었는지 확인. 새로고침을 안했다면, 새로운 job list가 없을테니 exception이 발생해야 함.
        try:
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            testResult = "failed"
            reason.append("2 steps failed\n")
        except:
            time.sleep(0.5)
        
        # Real Time 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1647, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1647, testPlanID, buildName, 'p', "Real Time Passed")

    def ShortCut():
        print("ITR-23: Search Filter > Short cut")
        testResult = ''
        reason = list()

        # Refer 탭 클릭(화면 초기화)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : 임의의 검색조건을 입력한 후, Short cut 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        time.sleep(1)
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # 검색할 항목을 리스트로 생성
        search_list = [['StudyDesc','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div/div/input'],
        ['Modality','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div/div/input'],
        ['Bodypart','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[3]/div/div/input'],
        ['Department','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[4]/div/div/input']]
        search_item = random.choice(search_list)
        
        # All List 탭 클릭
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # Job list에서 임의의 검색할 항목을 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        search_sample = []

        for i in data:
            if i[search_item[0]] not in search_sample and type(i[search_item[0]]) != NoneType:
                search_sample.append(i[search_item[0]])
        search_sample = random.choice(search_sample)

        # Job list에서 임의의 값으로 검색
        driver.find_element(By.XPATH, search_item[1]).send_keys(search_sample)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
        
        # Short cut 버튼 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()
        status = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside").get_attribute("class")

        # Short cut 창 팝업 확인
        try:
            assert status == 'right-sidebar open'
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")
        
        # Short cut 창 닫기
        driver.find_element(By.XPATH, "/html/body/nav/div").click()

        # 2 steps start! : 임의의 Title을 작성한 후, Save 버튼을 클릭한다.
        # Short cut 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()

        # Title 작성 후, Save 버튼 클릭
        test_shortcut_title = 'TEST' + str(random.randrange(0,1000))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(str(test_shortcut_title))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        shortcut_title = []

        for i in data:
            if i["Title"] not in shortcut_title:
                shortcut_title.append(i["Title"])
        
        # Short cut이 생성되었는지 확인
        try:
            assert test_shortcut_title in shortcut_title
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # 3 steps start! : Title을 작성하지 않은 상태에서 Save 버튼을 클릭한다.
        # Title 삭제
        driver.find_element(By.XPATH,"/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").clear()

        # Title이 없는 상태에서 Save 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # 팝업창 메시지 저장
        text = driver.find_element(By.XPATH, "/html/body/div[6]/h2").get_property("textContent")
        
        # 팝업창 메시지가 정상적으로 표시되는지 확인
        try:
            assert text == "Title 을 입력해주세요."
        except:
            testResult = "failed"
            reason.append("3 steps failed\n")
        
        # 팝업창의 OK 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/div[6]/div[7]/div/button").click()

        # 4 steps start! : 임의의 Title을 작성하고 "Save Institution"을 체크한 후, Save 버튼을 클릭한다.
        # Short cut 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()

        # 임의의 Title을 입력
        test_shortcut_title = 'TEST' + str(random.randrange(0,1000))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(str(test_shortcut_title))

        # Save Insititution 체크 후, Save 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[3]/label").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        shortcut_title = []

        for i in data:
            temp_list = []
            temp_list.append(i["Title"])
            temp_list.append(i["InstitutionCode"])
            shortcut_title.append(temp_list)
        
        # Short cut이 생성되었는지 확인
        try:
            for i in shortcut_title:
                if i[0] == test_shortcut_title:
                    assert i[1] == '997'
        except:
            testResult = "failed"
            reason.append("4 steps failed\n")

        # 5 steps start! : 기존의 short cut에 등록된 동일한 title을 입력한 후, Save 버튼을 클릭한다.
        # Short cut list를 저장하기 위해 Short cut 생성
        time.sleep(1)
        del driver.requests
        test_shortcut_title = 'TEST' + str(random.randrange(0,1000))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(test_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        shortcut_title = []

        for i in data:
            if i["Title"] not in shortcut_title:
                shortcut_title.append(i["Title"])
        
        # 임의의 Short cut title 선택
        random_shortcut_title = random.choice(shortcut_title)
                
        # 기존에 저장된 short cut title 입력 후, Save 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(random_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut 추가 후, Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        new_shortcut_title = []

        for i in data:
            new_shortcut_title.append(i["Title"])

        # 동일한 short cut title이 생성되는지 확인
        try:
            cnt = 0
            for i in new_shortcut_title:
                if i == random_shortcut_title:
                    cnt = cnt + 1
            assert cnt >= 2
        except:
            testResult = "failed"
            reason.append("5 steps failed\n")

        # 동일한 short cut 삭제 (다음 테스트를 위해)
        index = new_shortcut_title.index(random_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]/span/button").click()
        
        # 6 steps start! : 이미 등록된 short cut을 클릭한 후, 다시 short cut 버튼을 클릭해서 Save 버튼을 클릭한다.
        # Short cut list를 저장하기 위해 Short cut 생성
        time.sleep(1)
        del driver.requests
        test_shortcut_title = 'TEST' + str(random.randrange(0,1000))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(test_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        shortcut_title = []

        for i in data:
            shortcut_title.append(i["Title"])

        # 임의의 Short cut 클릭
        random_shortcut_title = random.choice(shortcut_title)
        index = shortcut_title.index(random_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]").click()

        # Short cut 버튼 클릭
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()
        
        # Title에 이전에 선택했던 Short cut title이 있는지 확인 후, Save 버튼 클릭
        title = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").get_property("value")
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()
        
        # Search Condition 팝업창이 나타나는지 확인
        try:
            assert title == random_shortcut_title and driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[13]/div/div/div[1]/h4").get_property("textContent") == "Search Condition"
        except:
            testResult = "failed"
            reason.append("6 steps failed\n")

        # 7 steps start! : Search Condition 팝업창에서 Add를 클릭한다.
        # Search Condition > Add 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[13]/div/div/div[3]/button[1]").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        shortcut_title = []

        for i in data:
            shortcut_title.append(i["Title"])

        # Short cut 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()
        
        # 동일한 Short cut title이 추가되었는지 확인인
        try:
            cnt = 0
            for i in shortcut_title:
                if i == random_shortcut_title:
                    cnt = cnt + 1
            assert cnt >= 2
        except:
            testResult = "failed"
            reason.append("7 steps failed\n")
        
        # 동일한 short cut 삭제 (다음 테스트를 위해)
        index = shortcut_title.index(random_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]/span/button").click()
        
        # 8 steps start! : Search Condition 팝업창에서 Edit를 클릭한다.
        # Short cut > Clear 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li[1]").click()

        # Short cut 버튼 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()

        # Short cut list를 저장하기 위해 Short cut 생성
        time.sleep(1)
        del driver.requests
        test_shortcut_title = 'TEST' + str(random.randrange(0,1000))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(test_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        before_shortcut = []
        shortcut_title = []

        for i in data:
            temp = []
            temp_title = []
            temp_title.append(i["Title"])
            temp.append(i["Title"])
            temp.append(i["StudyDesc"])
            temp.append(i["Modality"])
            temp.append(i["Bodypart"])
            temp.append(i["Department"])
            shortcut_title.append(temp_title)
            before_shortcut.append(temp)

        # 임의의 Short cut 클릭
        time.sleep(1)
        del driver.requests
        random_shortcut_title = random.choice(shortcut_title)
        index = shortcut_title.index(random_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]").click()
        
        # 검색할 항목을 리스트로 생성
        search_list = [['StudyDesc','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div/div/input','1'],
        ['Modality','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div/div/input','2'],
        ['Bodypart','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[3]/div/div/input','3'],
        ['Department','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[4]/div/div/input','4']]
        choice_search_item = random.choice(search_list)
        index_search_item = search_list.index(choice_search_item) + 1

        # Short cut 창 닫기
        driver.find_element(By.XPATH, "/html/body/nav/div").click()

        # All List 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            if i[choice_search_item[0]] != None:
                if i[choice_search_item[0]] not in job_list:
                    job_list.append(i[choice_search_item[0]])
        search_item = random.choice(job_list)

        # 검색 조건에 입력 후, Search 버튼 클릭
        driver.find_element(By.XPATH, choice_search_item[1]).send_keys(search_item)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

        # Short cut 버튼 클릭 후, Save 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Search Condition > Edit 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[13]/div/div/div[3]/button[2]").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        after_shortcut = []
        random_shortcut_title = ' '.join(s for s in random_shortcut_title)
        choice_search_item = str(choice_search_item[0])

        for i in data:
            if i["Title"] == random_shortcut_title:
                temp = []
                temp.append(i["Title"])
                temp.append(i["StudyDesc"])
                temp.append(i["Modality"])
                temp.append(i["Bodypart"])
                temp.append(i["Department"])
                after_shortcut.append(temp)
        
        # Edit 시, 동일한 Short cut title에 저장되는지 확인
        try:
            for i in before_shortcut:
                if i[0] == random_shortcut_title:
                    assert i[index_search_item] != search_item
        except:
            testResult = "failed"
            reason.append("8 steps failed\n")

        # 9 steps start! : Search Condition 팝업창에서 Close를 클릭한다.
        # Short cut 버튼 클릭 후, Clear 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li[1]").click()

        # Short cut 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()

        # Short cut list를 저장하기 위해 Short cut 생성
        time.sleep(1)
        del driver.requests
        test_shortcut_title = 'TEST' + str(random.randrange(0,1000))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(test_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        shortcut_title = []

        for i in data:
            temp_title = []
            temp_title.append(i["Title"])
            shortcut_title.append(temp_title)

        # Short cut > 임의의 Short cut 클릭
        random_shortcut_title = random.choice(shortcut_title)
        index = shortcut_title.index(random_shortcut_title)
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]").click()

        # Short cut 버튼 클릭 후, Save 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()
        
        # Search Condition > Close 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[13]/div/div/div[3]/button[3]").click()

        # Short cut 생성 취소 확인
        try:
            request = driver.wait_for_request('.*/GetReferSearchCondition.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            testResult = "failed"
            reason.append("9 steps failed\n")
        except:
            time.sleep(0.5)

        # 10 steps start! : Short cut 리스트에서 "Clear"를 클릭한다.
        # Short cut 버튼 클릭 후, Clear 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li[1]").click()

        # 검색 조건 상태 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        search_filter = []
        search_filter.append(data["StudyDesc"])
        search_filter.append(data["Modality"])
        search_filter.append(data["Bodypart"])
        search_filter.append(data["Department"])

        # Short cut 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()
        
        # Title 입력값이 초기화 되었는지 확인
        try:
            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").get_property("value") == '':
                for i in search_filter:
                    assert i == None
        except:
            testResult = "failed"
            reason.append("10 steps failed\n")

        # 11 steps start! : Short cut 리스트에서 임의의 short cut을 클릭한다.
        # Short cut list를 저장하기 위해 Short cut 생성
        time.sleep(1)
        del driver.requests
        test_shortcut_title = 'TEST' + str(random.randrange(0,1000))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(test_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        shortcut_title = []

        for i in data:
            temp = []
            temp.append(i["Title"])
            temp.append(i["StudyDesc"])
            temp.append(i["Modality"])
            temp.append(i["Bodypart"])
            temp.append(i["Department"])
            shortcut_title.append(temp)

        # Short cut > 임의의 Short cut 클릭
        random_shortcut_title = random.choice(shortcut_title)
        index = shortcut_title.index(random_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]").click()

        # 검색 조건 상태 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        search_filter = []
        search_filter.append(data["StudyDesc"])
        search_filter.append(data["Modality"])
        search_filter.append(data["Bodypart"])
        search_filter.append(data["Department"])

        # Short cut의 검색 조건과 검색 결과의 검색 조건이 동일한지 확인
        try:
            for i in shortcut_title:
                if i[0] == random_shortcut_title:
                    for n in range(1,4):
                        assert i[n] == search_filter[n-1]
        except:
            testResult = "failed"
            reason.append("11 steps failed\n")

        # 12 steps start! : Short cut 리스트에서 "-" 버튼을 클릭한다.
        # Short cut 버튼 클릭 후, Clear 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li[1]").click()

        # Short cut 버튼 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()

         # Short cut list를 저장하기 위해 Short cut 생성
        time.sleep(1)
        del driver.requests
        test_shortcut_title = 'TEST' + str(random.randrange(0,1000))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(test_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        before_shortcut_list = []

        for i in data:
            before_shortcut_list.append(i["Title"])
        
        # 추가한 short cut 삭제
        time.sleep(1)
        del driver.requests
        index = before_shortcut_list.index(test_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]/span/button").click()

        # 삭제 후, Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        after_shortcut_list = []

        for i in data:
            after_shortcut_list.append(i["Title"])

        # 정상적으로 Short cut이 삭제되었는지 확인
        try:
            assert test_shortcut_title not in after_shortcut_list
        except:
            testResult = "failed"
            reason.append("12 steps failed\n")

        # 13 steps start! : Short cut 리스트에서 Short cut에 마우스 오버한다.
        # 임의의 Short cut에 마우스 오버
        random_shortcut_title = random.choice(after_shortcut_list)
        index = after_shortcut_list.index(random_shortcut_title)
        webdriver.ActionChains(driver).move_to_element(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]")).perform()

        # 마우스 오버 시, 툴팁 정보 저장
        tooltip = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]").get_property("outerHTML")

        # 툴팁이 표시되는지 확인
        try:
            assert "aria-describedby" in tooltip
        except:
            testResult = "failed"
            reason.append("13 steps failed\n")

        # 14 steps start! : Short cut 리스트에서 Short cut에 마우스 오버한 후, "-" 버튼을 클릭한다.
        # 현재 리스트 개수 확인
        shortcut_list_cnt = len(after_shortcut_list) + 2

        # 현재 Short cut list의 툴팁에 있는 key 값 저장
        before_shortcut_key_list = []
        for n in range(2, shortcut_list_cnt):
            shortcut_key = (driver.find_element(By.CSS_SELECTOR, "#settings > div > div:nth-child(1) > ul > li:nth-child("+str(n)+")").get_property("dataset"))["key"]
            if shortcut_key not in before_shortcut_key_list:
                before_shortcut_key_list.append(shortcut_key)

        # 임의의 Short cut에 마우스 오버
        random_shortcut_title = random.choice(after_shortcut_list)
        index = after_shortcut_list.index(random_shortcut_title)
        webdriver.ActionChains(driver).move_to_element(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]")).perform()

        # 마우스 오버 시, 툴팁 정보 저장
        tooltip = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]").get_property("outerHTML")
        tooltip_key = (driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]").get_property("dataset"))["key"]

        # 임의의 Short cut 삭제
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]/span/button").click()
        
        # Short cut 삭제 후, Short cut list의 툴팁에 있는 key 값 저장
        time.sleep(1)
        after_shortcut_key_list = []
        for n in range(2, shortcut_list_cnt-1):
            shortcut_key = (driver.find_element(By.CSS_SELECTOR, "#settings > div > div:nth-child(1) > ul > li:nth-child("+str(n)+")").get_property("dataset"))["key"]
            if shortcut_key not in after_shortcut_key_list:
                after_shortcut_key_list.append(shortcut_key)

        # 삭제한 Short cut의 툴팁이 삭제되었는지 확인
        try:
            assert tooltip_key not in after_shortcut_key_list
        except:
            testResult = "failed"
            reason.append("14 steps failed\n")

        # Short cut 창 닫기
        driver.find_element(By.XPATH, "/html/body/nav/div").click()

        # Short cut 결과 전송
        result = ' '.join(s for s in result)
        print("Test Result: Pass" if testResult != "failed" else testResult)
        if testResult == 'failed':
            testlink.reportTCResult(1651, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1651, testPlanID, buildName, 'p', "Short cut Passed")

class Worklist:
    def All_Assigned_List():
        print("ITR-24: Worklist > All Assigned List")
        testResult = ''
        reason = list()

        # Refer 탭 클릭(화면 초기화)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : All Assigned List 탭을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        time.sleep(1)
        del driver.requests
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # All Assigned List 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        # Job list 저장
        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        # All Assigned List의 Job list를 가져오는지 확인
        try:
            assert data is not None
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")
        
        # All Assigned List 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1668, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1668, testPlanID, buildName, 'p', "All Assigned List Passed")

    def Not_Assigned_List():
        print("ITR-25: Worklist > Not Assigned List")
        testResult = ''
        reason = list()

        # 1 steps start! : Not Assigned List 탭을 클릭한다.
        # All Assigned List 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        # Job list 저장
        time.sleep(1)
        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        # All Assigned List의 Job list를 가져오는지 확인
        try:
            assert data is not None
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")
        
        # Not Assigned List 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1671, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1671, testPlanID, buildName, 'p', "Not Assigned List Passed")

    def All_List():
        print("ITR-26: Worklist > All List")
        testResult = ''
        reason = list()

        # 1 steps start! : All List 탭을 클릭한다.
        # All List 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # Job list 저장
        time.sleep(1)
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        # All Assigned List의 Job list를 가져오는지 확인
        try:
            assert data is not None
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # All List 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1674, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1674, testPlanID, buildName, 'p', "All List Passed")

    def Schedule():
        print("ITR-27: Worklist > Schedule")
        testResult = ''
        reason = list()

        # 1 steps start! : Schedule 체크박스를 체크한다.
        # Refer 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 병원 리스트와 Schedule count 저장
        time.sleep(1)
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        schedule_list = []

        for i in data:
            if i["ScheduleTotalCount"] != 0:
                temp = []
                temp.append(i["InstitutionCode"])
                temp.append(i["ScheduleTotalCount"])
                schedule_list.append(temp)

        # Schedule이 있는 병원을 순서대로 클릭
        for i in schedule_list:
            driver.find_element(By.CSS_SELECTOR, "#list-institution-row-"+str(i[0])).click()

            # Schedule 체크
            status = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[4]/a/input").get_property("checked")
            if status != True:
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[4]/a/label").click()

            # All Assigned List 클릭
            time.sleep(0.5)
            del driver.requests
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()
            
            # All Assigned List의 scheduled job list 저장
            request = driver.wait_for_request('.*/GetAllAssignedList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            schedule_job_list = []

            for j in data:
                schedule_job_list.append(j)

            # Not Assigned List의 scheduled job list 저장
            time.sleep(0.5)
            del driver.requests
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()
            request = driver.wait_for_request('.*/GetNotAssignedList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for j in data:
                schedule_job_list.append(j)

            # Schedule Job list 개수 저장
            schedule_job_cnt = len(schedule_job_list)
            
            # 병원 리스트에 표시된 Schedule count와 scheduled list의 count가 일치하는지 확인
            try:
                assert i[1] == schedule_job_cnt
            except:
                testResult = "failed"
                reason.append("1 steps failed\n")

        # 2 steps start! : Schedule 체크박스를 체크 해제한다.
        # 병원 탭 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/li[1]").click()

        # Schedule이 있는 병원의 Job count 저장
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        schedule_list = []

        for i in data:
            if i["ScheduleTotalCount"] != 0:
                temp = []
                temp.append(i["InstitutionCode"])
                temp.append(i["JobCount"])
                schedule_list.append(temp)

        # Schedule이 있는 병원을 순서대로 클릭
        for i in schedule_list:
            driver.find_element(By.CSS_SELECTOR, "#list-institution-row-"+str(i[0])).click()

            # Schedule 체크 해제
            status = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[4]/a/input").get_property("checked")
            if status != False:
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[4]/a/label").click()

            # All Assigned List 탭 클릭
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

            # All Assigned List의 Job count 저장
            time.sleep(1)
            temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
            temp_cnt = temp_cnt.split()
            list_cnt = 0
            list_cnt = int(temp_cnt[5])

            # Not Assigned List 탭 클릭
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()
            
            # Not Assigned List의 Job count 저장
            time.sleep(1)
            temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
            temp_cnt = temp_cnt.split()
            list_cnt = int(list_cnt) + int(temp_cnt[5])

            # 병원 리스트의 Job count와 Job list의 job count가 일치하는지 확인
            try:
                assert int(i[1]) == int(list_cnt)
            except:
                testResult = "failed"
                reason.append("2 steps failed\n")

        # Schedule 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1677, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1677, testPlanID, buildName, 'p', "Schedule Passed")
        
    def Priority():
        print("ITR-28: Worklist > Priority")
        testResult = ''
        reason = list()

        # 1 steps start! : Worklist에서 Priority가 일반인 의뢰 검사를 선택한 후, Priority 버튼을 클릭한다.
        # Refer 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
        
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()
        
        # Show entries를 100개로 변경
        Common.refer_show_entries(100)
        
        # Not Assigned List 탭 클릭
        time.sleep(0.5)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        # Not Assigned List > Job priority가 일반인 Job list 저장
        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            if i["JobPriority"] == 'N':
                job_list.append(i["JobKey"])

        # Not Assigned List > Priority가 일반인 임의의 job 체크
        job_key = random.choice(job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()="+str(job_key)+"]").click()

        # Not Assigned List > Priority 버튼 클릭
        priority_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[1]/button[1]")
        if priority_btn.get_property("disabled") != True:
            driver.execute_script("arguments[0].click()",priority_btn)

        # Not Assigned List 탭 클릭 후, Not Assigned List > Job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()
        
        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            if i["JobPriority"] == 'N':
                job_list.append(i["JobKey"])

        # 선택한 job의 priority가 응급으로 변경되었는지 확인
        try:
            assert job_key not in job_list
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")
        
        # 2 steps start! : Worklist에서 Priority가 응급인 의뢰 검사를 선택한 후, Priority 버튼을 클릭한다.
        # Not Assigned List 탭 클릭 후, Priority가 응급인 job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            if i["JobPriority"] == 'E':
                job_list.append(i["JobKey"])

        # Not Assigned List > Priority가 응급인 job 체크
        job_key = random.choice(job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # Not Assigned List > Priority 버튼 클릭
        priority_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[1]/button[1]")
        if priority_btn.get_property("disabled") != True:
            driver.execute_script("arguments[0].click()",priority_btn)

        # Not Assigned List 탭 클릭 후, Priority가 응급인 Job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            if i["JobPriority"] == 'E':
                job_list.append(i["JobKey"])

        # 선택한 job의 priority가 일반으로 변경되었는지 확인
        try:
            assert job_key not in job_list
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")
        
        # Priority 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1681, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1681, testPlanID, buildName, 'p', "Priority Passed")

    def Canceled():
        print("ITR-29: Worklist > Canceled")
        testResult = ''
        reason = list()

        # 1 steps start! : Worklist에서 Job Status가 Canceled 이외의 의뢰 검사를 선택한 후, Cancel 버튼을 클릭한다.
        # Refer 탭 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
        
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Not Assigned List 탭 클릭 후, Job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()
        
        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        before_job_list = []

        for i in data:
            before_job_list.append(i["JobKey"])

        # Not Assigned List > 임의의 Job 선택
        job_key = random.choice(before_job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # Cancel 버튼 클릭
        cancel_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[1]/button[2]")
        if cancel_btn.get_property("disabled") != True:
            driver.execute_script("arguments[0].click()",cancel_btn)
        
        # Request Cancel 팝업창이 나타나는지 확인
        try:
            assert driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[9]/div/div/div[1]/h4").get_property("textContent") == "Request Cancel"
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")
        
        # 2 steps start! : Request Cancel 팝업창에서 "OK"를 클릭한다.
        # Request Cancel > OK 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[9]/div/div/div[3]/button[1]").click()

        # Not Assigned List > Job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()
        
        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        after_job_list = []

        for i in data:
            after_job_list.append(i["JobKey"])

        # Not Assigned List > Job list에서 Cancel 한 job이 없는지 확인
        try:
            assert job_key not in after_job_list
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # 3 steps start! : Request Cancel 팝업창에서 "Close"를 클릭한다.
        # Not Assigned List > 임의의 Job 선택
        job_key = random.choice(before_job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # Cancel 버튼 클릭
        cancel_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[1]/button[2]")
        if cancel_btn.get_property("disabled") != True:
            driver.execute_script("arguments[0].click()",cancel_btn)

        # Request Cancel > Close 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[9]/div/div/div[3]/button[2]").click()

        # Net Assigned List 탭 클릭(job list 획득하기 위함)
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        close_job_list = []

        for i in data:
            close_job_list.append(i["JobKey"])

        # Not Assgined List > Job list에서 Cancel 한 job이 있는지 확인
        try:
            assert job_key in close_job_list
        except:
            testResult = "failed"
            reason.append("3 steps failed\n")    

        # Canceled 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1685, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1685, testPlanID, buildName, 'p', "Canceled Passed")

    def Refer():
        print("ITR-30: Worklist > Refer")
        testResult = ''
        reason = list()

        # 1 steps start! : Worklist에서 임의의 의뢰 검사를 선택한 후, Refer 버튼을 클릭한다.
        # Configuration > Institutions로 이동 후, 테스트 병원 검색
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[5]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/button[4]").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[2]/div/div[1]/div/div/input").send_keys(test_hospital_code)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[2]/div/div[3]/button").click()

        # Configuration > Institutions > Institutions Modify 팝업창 > Use Default Referring Comment 체크 해제
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#i_l_997").click()
        time.sleep(1)
        referring_comment = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[1]/div[6]/div/div/input").get_property("checked")
        if referring_comment == True:
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[1]/div[6]/div/div/label").click()
         
        # Save 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[3]/div/button[2]").click()

        # 팝업창에서 Yes 클릭
        try:
            EC.element_attribute_to_include(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible")
            if (driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible").get_property("classList"))[2] == "visible":
                driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # Refer 탭 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Show entries를 100개로 변경
        Common.refer_show_entries(100)

        # Not Assigned List 탭 클릭 후, job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            job_list.append(i["JobKey"])

        # Not Assigned List > 임의의 job 선택
        job_key = random.choice(job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # Refer 버튼 클릭
        refer_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[1]")
        if refer_btn.get_property("disabled") != True:
            driver.execute_script("arguments[0].click()",refer_btn)

        # Refer 창이 팝업됐는지 확인
        try:
            assert driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[1]/h4").get_property("textContent") == "Refer"
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! : Search 입력란에 ID 또는 이름을 입력한다.
        # Refer 팝업창의 Reporter list 저장
        temp_list = ''
        time.sleep(1)
        temp_list = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul").get_property("outerText")
        reporter_list = temp_list.split('\n')
        reporter_id_list = []
        reporter_name_list = []

        for i in reporter_list:
            reporter_id_list.append(i.split()[0])
            reporter_name_list.append(i.split()[2])

        # Refer 팝업창 > Search 필드에 임의의 Reporter ID를 입력
        random_reporter_id = random.choice(reporter_id_list)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/input").clear()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/input").send_keys(random_reporter_id)

        # Refer 팝업창 > 검색 결과 저장
        temp_list = ''
        temp_list = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul").get_property("outerText")
        reporter_list = temp_list.split('\n')
        check_reporter_id_list = []

        for i in reporter_list:
            check_reporter_id_list.append(i.split()[0])

        # Refer 팝업창 > Reporter list에 검색한 Reporter가 표시되는지 확인
        try:
            assert random_reporter_id in check_reporter_id_list
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # Refer 팝업창 > Search 필드에 임의의 Reporter Name을 입력
        random_reporter_name = random.choice(reporter_name_list)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/input").clear()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/input").send_keys(random_reporter_name)

        # Refer 팝업창 > 검색 결과 저장
        temp_list = ''
        temp_list = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul").get_property("outerText")
        reporter_list = temp_list.split('\n')
        check_reporter_name_list = []

        for i in reporter_list:
            check_reporter_name_list.append(i.split()[2])
        
        # Refer 팝업창 > Reporter list에 검색한 Reporter가 표시되는지 확인
        try:
            assert random_reporter_name in check_reporter_name_list
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")
        
        # 3 steps start! : Sort By Name에 체크한다.
        # Refer 팝업창 > Search 필드 초기화
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/input").clear()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/input").send_keys(" ")

        # Refer 팝업창 > Reporter list 저장 및 오름차순 정렬
        temp_list = ''
        temp_list = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul").get_property("outerText")
        reporter_list = temp_list.split('\n')
        before_reporter_name_list = []

        for i in reporter_list:
            before_reporter_name_list.append(i.split()[2])
        before_reporter_name_list.sort()

        # Refer 팝업창 > Sort By Name 체크
        check = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[1]/input")
        if refer_btn.get_property("checked") != True:
            driver.execute_script("arguments[0].click()",check)

        # Refer 팝업창 > Reporter list 저장
        time.sleep(1)
        temp_list = ''
        temp_list = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul").get_property("outerText")
        reporter_list = temp_list.split('\n')
        after_reporter_name_list = []

        for i in reporter_list:
            after_reporter_name_list.append(i.split()[2])

        # Reporter list가 Name으로 정렬되었는지 확인
        try:
            assert before_reporter_name_list == after_reporter_name_list
        except:
            testResult = "failed"
            reason.append("3 steps failed\n")

        # 4 steps start! : 리스트에서 임의의 판독의를 클릭한다.
        # Refer 팝업창 > Reporter list에서 repoter의 수를 확인
        reporter_cnt = len(after_reporter_name_list)
        count_list = []
        if reporter_cnt > 1:
            for i in range(1, reporter_cnt+1):
                count_list.append(i)
        else:
            reporter_cnt = 1

        # Refer 팝업창 > 임의의 Reporter를 임의의 숫자만큼 선택 후, reporter list 저장
        select_reporter_list = []
        selected_reporter_list = []
        if int(reporter_cnt) > 1:
            i = 0
            cnt = random.randrange(1, reporter_cnt+1)
            while i < int(cnt):
                # n = count_list.pop(random.randrange(0, reporter_cnt))
                n = count_list.pop(count_list.index(random.choice(count_list)))
                select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").get_property("textContent"))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").click()
                selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/ul/li["+str(n)+"]").get_property("textContent"))
                i = i + 1
        else:
            select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").click()
            selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))

        # Refer 팝업창 > 선택한 Reporter가 정상적으로 선택됐는지 확인
        try:
            assert select_reporter_list == selected_reporter_list
        except:
            testResult = "failed"
            reason.append("4 steps failed\n")

        # 5 steps start! : Comment를 입력한다.
        # Comment를 입력하고 Save 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/textarea").send_keys("Refer Comment Test")
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[3]/button[1]").click()

        # Refer 탭 클릭
        time.sleep(1)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
        driver.refresh()

        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # All Assigned List > Refer 한 Job에서 마우스 우클릭
        time.sleep(1)
        # WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//td[normalize-space()='"+str(job_key)+"']")))
        webdriver.ActionChains(driver).context_click(driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']")).perform()

        # Report View 창 팝업 확인
        try:
            assert driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[17]/div/div/div[1]/h3").get_property("textContent") == "Report View"
        except:
            testResult = "failed"
            reason.append("5 steps failed\n")

        # Report View 팝업창 > Refer Comment에 입력한 comment가 표시되는지 확인
        try:
            time.sleep(1)
            assert driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[17]/div/div/div[2]/div[5]/div[2]/div/textarea").get_property("value") == "Refer Comment Test"
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[17]/div/div/div[2]/div[12]/button").click()
        except:
            testResult = "failed"
            reason.append("5 steps failed\n")

        # 6 steps start! : Comment를 선택하고, 추가 Comment가 있다면 입력한다.
        # Configuration > Institutions로 이동 후, 테스트 병원 검색
        # time.sleep(2)
        element = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[5]/a")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[5]/a").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/button[4]").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[2]/div/div[1]/div/div/input").send_keys(test_hospital_code)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[2]/div/div[3]/button").click()

        # Configuration > Institutions > Institutions Modify 팝업창 > Use Default Referring Comment 체크
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#i_l_997").click()
        time.sleep(1)
        referring_comment = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[1]/div[6]/div/div/input").get_property("checked")
        if referring_comment != True:
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[1]/div[6]/div/div/label").click()
         
        # Save 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[3]/div/button[2]").click()

        # 팝업창에서 Yes 클릭
        try:
            EC.element_attribute_to_include(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible")
            if (driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible").get_property("classList"))[2] == "visible":
                driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        except:
            testResult = "failed"
            reason.append("6 steps failed\n")

        # Refer 탭 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Not Assigned List 탭 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        # Not Assigned List > 임의의 job 선택
        job_key = random.choice(job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()
        
        # Not Assigned List > Refer 버튼 클릭
        refer_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[1]")
        if refer_btn.get_property("disabled") != True:
            driver.execute_script("arguments[0].click()",refer_btn)
        
        # Refer 팝업창 > Reporter list에서 repoter의 수를 확인
        reporter_cnt = len(after_reporter_name_list)
        count_list = []
        if reporter_cnt > 1:
            for i in range(1, reporter_cnt+1):
                count_list.append(i)
        else:
            reporter_cnt = 1

        # Refer 팝업창 > 임의의 Reporter를 임의의 숫자만큼 선택 후, reporter list 저장
        select_reporter_list = []
        selected_reporter_list = []
        if int(reporter_cnt) > 1:
            i = 0
            cnt = random.randrange(1, reporter_cnt+1)
            while i < int(cnt):
                n = count_list.pop(count_list.index(random.choice(count_list)))
                select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").get_property("textContent"))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").click()
                selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/ul/li["+str(n)+"]").get_property("textContent"))
                i = i + 1
        else:
            select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").click()
            selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))

        # Refer 팝업창 > Comment dropbox list 저장
        comment_list = []
        comment_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/select/option")

        # Refer 팝업창 > 임의의 Comment 선택
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/select").click()
        select_comment = random.choice(comment_list)
        select_comment.click()

        # Refer 팝업창 > Comment 내용 저장
        comment = ''
        comment = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/textarea").get_property("value")

        # Refer 팝업창 > Save 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[3]/button[1]").click()

        # All Assigned List 탭 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        # All Assigned List 저장
        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        before_all_assigned_job_list = []

        for i in data:
            temp = []
            temp.append(i["JobKey"])
            temp.append(i["PatientID"])
            temp.append(i["InstitutionCode"])
            temp.append(i["Modality"])
            before_all_assigned_job_list.append(temp)

        # All Assigned List > Refer 한 Job에서 마우스 우클릭
        time.sleep(1)
        webdriver.ActionChains(driver).context_click(driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']")).perform()

        # Report View 팝업창 > Refer Comment에 입력한 comment가 표시되는지 확인
        try:
            time.sleep(1)
            assert driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[17]/div/div/div[2]/div[5]/div[2]/div/textarea").get_property("value") == comment
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[17]/div/div/div[2]/div[12]/button").click()
        except:
            testResult = "failed"
            reason.append("6 steps failed\n")

        # 7 steps start! : With Releated Job에 체크한 후, Save 버튼을 클릭한다.
        # Refer 탭 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()
        
        # Not Assigned List 탭 클릭 후, job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            job_list.append(i["JobKey"])

        # Not Assigned List > 임의의 job 선택
        job_key = random.choice(job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # Not Assigned List > Refer 버튼 클릭
        refer_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[1]")
        if refer_btn.get_property("disabled") != True:
            driver.execute_script("arguments[0].click()",refer_btn)
        
        # Refer 팝업창 > Reporter list에서 repoter의 수를 확인
        reporter_cnt = len(after_reporter_name_list)
        count_list = []
        if reporter_cnt > 1:
            for i in range(1, reporter_cnt+1):
                count_list.append(i)
        else:
            reporter_cnt = 1

        # Refer 팝업창 > 임의의 Reporter를 임의의 숫자만큼 선택 후, reporter list 저장
        select_reporter_list = []
        selected_reporter_list = []
        if int(reporter_cnt) > 1:
            i = 0
            cnt = random.randrange(1, reporter_cnt+1)
            while i < int(cnt):
                n = count_list.pop(count_list.index(random.choice(count_list)))
                select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").get_property("textContent"))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").click()
                selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/ul/li["+str(n)+"]").get_property("textContent"))
                i = i + 1
        else:
            select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").click()
            selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))

        # Refer 팝업창 > Comment dropbox list 저장
        comment_list = []
        comment_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/select/option")

        # Refer 팝업창 > 임의의 Comment 선택
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/select").click()
        select_comment = random.choice(comment_list)
        select_comment.click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/select").click()

        # Refer 팝업창 > Comment 내용 저장
        comment = ''
        comment = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/textarea").get_property("value")

        # Refer 팝업창 > With Related Job 체크
        check = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/input")
        if check.get_property("checked") == False:
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/label").click()
            # check.click()

        # Refer 팝업창 > Save 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[3]/button[1]").click()

        # All Assigned List 탭 클릭 및 job list 저장
        time.sleep(2)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        after_all_assigned_job_list = []

        for i in data:
            temp = []
            temp.append(i["JobKey"])
            temp.append(i["PatientID"])
            temp.append(i["InstitutionCode"])
            temp.append(i["Modality"])
            after_all_assigned_job_list.append(temp)
        
        # Refer 후, 추가된 job list 추출
        changes_job_list = []
        for i in after_all_assigned_job_list:
            if i not in before_all_assigned_job_list:
                changes_job_list.append(i)
        
        # Refer 한 job 찾기
        sample_list = []
        for i in after_all_assigned_job_list:
            if i[0] == job_key:
                temp = []
                temp.append(i[1])
                temp.append(i[2])
                temp.append(i[3])
                sample_list.append(temp)

        # Changes_job_list에서 job key만 제거
        if len(changes_job_list) != 1:
            for i in changes_job_list:
                del i[0]
        else:
            del changes_job_list[0][0]

        # 추가된 job list의 job이 Refer 한 job의 Patient ID, Institution Code, Modality가 동일한지 확인
        try:
            if len(changes_job_list) != 1:
                for i in changes_job_list:
                    assert i == sample_list
            else:
                assert changes_job_list == sample_list
        except:
            testResult = "failed"
            reason.append("7 steps failed\n")

        # 8 steps start! : With Releated Job에 체크 해제한 후, Save 버튼을 클릭한다.
        # All Assigned List 탭 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        # All Assigned List 저장
        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        before_all_assigned_job_list = []

        for i in data:
            temp = []
            temp.append(i["JobKey"])
            temp.append(i["PatientID"])
            temp.append(i["InstitutionCode"])
            temp.append(i["Modality"])
            before_all_assigned_job_list.append(temp)

        # Not Assigned List 탭 클릭 후, job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            job_list.append(i["JobKey"])

        # Not Assigned List > 임의의 job 선택
        job_key = random.choice(job_list)
        time.sleep(2)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # Not Assigned List > Refer 버튼 클릭
        refer_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[1]")
        if refer_btn.get_property("disabled") != True:
            driver.execute_script("arguments[0].click()",refer_btn)
        
        # Refer 팝업창 > Reporter list에서 repoter의 수를 확인
        reporter_cnt = len(after_reporter_name_list)
        count_list = []
        if reporter_cnt > 1:
            for i in range(1, reporter_cnt+1):
                count_list.append(i)
        else:
            reporter_cnt = 1

        # Refer 팝업창 > 임의의 Reporter를 임의의 숫자만큼 선택 후, reporter list 저장
        select_reporter_list = []
        selected_reporter_list = []
        if int(reporter_cnt) > 1:
            i = 0
            cnt = random.randrange(1, reporter_cnt+1)
            while i < int(cnt):
                n = count_list.pop(count_list.index(random.choice(count_list)))
                select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").get_property("textContent"))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").click()
                selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/ul/li["+str(n)+"]").get_property("textContent"))
                i = i + 1
        else:
            select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").click()
            selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))

        # Refer 팝업창 > Comment dropbox list 저장
        comment_list = []
        comment_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/select/option")

        # Refer 팝업창 > 임의의 Comment 선택
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/select").click()
        select_comment = random.choice(comment_list)
        select_comment.click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/select").click()

        # Refer 팝업창 > Comment 내용 저장
        comment = ''
        comment = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/textarea").get_property("value")

        # Refer 팝업창 > With Related Job 체크
        check = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/input")
        if check.get_property("checked") != False:
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/label").click()

        # Refer 팝업창 > Save 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[3]/button[1]").click()

        # All Assigned List 탭 클릭 및 job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        after_all_assigned_job_list = []

        for i in data:
            temp = []
            temp.append(i["JobKey"])
            temp.append(i["PatientID"])
            temp.append(i["InstitutionCode"])
            temp.append(i["Modality"])
            after_all_assigned_job_list.append(temp)
        
        # Refer 후, 추가된 job list 추출
        changes_job_list = []
        for i in after_all_assigned_job_list:
            if i not in before_all_assigned_job_list:
                changes_job_list.append(i)
        
        # Refer 한 job 찾기
        sample_list = []
        for i in after_all_assigned_job_list:
            if i[0] == job_key:
                temp = []
                temp.append(i[1])
                temp.append(i[2])
                temp.append(i[3])
                sample_list.append(temp)

        # Changes_job_list에서 job key만 제거
        if len(changes_job_list) != 1:
            for i in changes_job_list:
                del i[0]
        else:
            del changes_job_list[0][0]

        # 추가된 job list의 job이 Refer 한 job의 Patient ID, Institution Code, Modality가 동일한지 확인
        try:
            assert len(changes_job_list) == 1 and changes_job_list == sample_list
        except:
            testResult = "failed"
            reason.append("8 steps failed\n")

        # 9 steps start! : Refer를 하지 않고 Close 버튼을 클릭한다.
        # Not Assigned List 탭 클릭 후, job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            job_list.append(i["JobKey"])
        
        # Not Assigned List > 임의의 job 선택
        job_key = random.choice(job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # Not Assigned List > Refer 버튼 클릭
        refer_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[1]")
        if refer_btn.get_property("disabled") != True:
            driver.execute_script("arguments[0].click()",refer_btn)
        
        # Refer 팝업창 > Reporter list에서 repoter의 수를 확인
        reporter_cnt = len(after_reporter_name_list)
        count_list = []
        if reporter_cnt > 1:
            for i in range(1, reporter_cnt+1):
                count_list.append(i)
        else:
            reporter_cnt = 1

        # Refer 팝업창 > 임의의 Reporter를 임의의 숫자만큼 선택 후, reporter list 저장
        select_reporter_list = []
        selected_reporter_list = []
        if int(reporter_cnt) > 1:
            i = 0
            cnt = random.randrange(1, reporter_cnt+1)
            while i < int(cnt):
                n = count_list.pop(count_list.index(random.choice(count_list)))
                select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").get_property("textContent"))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").click()
                selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/ul/li["+str(n)+"]").get_property("textContent"))
                i = i + 1
        else:
            select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").click()
            selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))

        # Refer 팝업창 > Comment dropbox list 저장
        comment_list = []
        comment_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/select/option")

        # Refer 팝업창 > 임의의 Comment 선택
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/select").click()
        select_comment = random.choice(comment_list)
        select_comment.click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/select").click()

        # Refer 팝업창 > Close 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[3]/div/div/div[3]/button[2]").click()

        # All Assigned List 탭 클릭 후, job list 저장
        # time.sleep(1)
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]/a")))
        del driver.requests
        click = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]/a")
        driver.execute_script("arguments[0].click()",click)

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            job_list.append(i["JobKey"])

        # 선택한 job이 Refer 되지 않았는지 확인
        try:
            for i in job_list:
                assert i != job_key
        except:
            testResult = "failed"
            reason.append("9 steps failed\n")
        
        # Refer 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1690, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1690, testPlanID, buildName, 'p', "Refer Passed")

    def Refer_Cancel():
        print("ITR-31: Worklist > Refer Cancel")
        testResult = ''
        reason = list()

        # 1 steps start! : 판독의가 할당된 의뢰 검사를 선택한 후, Refer Cancel 버튼을 클릭한다.
        # Refer 탭 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Show entries를 100개로 변경
        Common.refer_show_entries(100)

        # All Assigned List 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        before_job_list = []

        for i in data:
            before_job_list.append(i["JobKey"])
        
        # All Assigned List > 임의의 job 선택
        job_key = random.choice(before_job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # All Assigned List > Refer Cancel 버튼 클릭
        btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[2]")
        if btn.get_property("disabled") == False:
            btn.click()

        # All Assigned List > Refer Cancel 팝업창 확인
        popup_title = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[10]/div/div/div[1]/h4")
        try:
            assert popup_title.get_property("textContent") == "Refer Cancel"
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! : Refer Cancel 팝업창에서 "Close"를 클릭한다.
        # Refer Cancel 팝업창 > Close 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[10]/div/div/div[3]/button[2]").click()

        # All Assigned List 탭 클릭 후, job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        after_job_list = []

        for i in data:
            after_job_list.append(i["JobKey"])

        # All Assigned List > Refer Cancel 한 job이 남아있는지 확인
        try:
            assert job_key in after_job_list
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # 3 steps start! : Refer Cancel 팝업창에서 "OK"를 클릭한다.
        # All Assigned List > 임의의 job 선택
        job_key = random.choice(after_job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # All Assigned List > Refer Cancel 버튼 클릭
        btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[2]")
        if btn.get_property("disabled") == False:
            btn.click()

        # Refer Cancel 팝업창 > OK 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[10]/div/div/div[3]/button[1]").click()

        # All Assigned List 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            job_list.append(i["JobKey"])

        # All Assigned List > 선택한 job이 사라졌는지 확인
        try:
            assert job_key not in job_list
        except:
            testResult = "failed"
            reason.append("3 steps failed\n")

        # 4 steps start! : 판독의가 할당되지 않은 의뢰 검사를 선택한 후, Refer Cancel 버튼을 클릭한다.
        # Not Assigned List 탭 클릭 후, job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        not_assigned_job_list = []

        for i in data:
            not_assigned_job_list.append(i["JobKey"])

        # Not Assigned List > 임의의 job 선택
        job_key = random.choice(not_assigned_job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # Not Assigned List > Refer Cancel 버튼 상태 확인
        refer_cancel_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[2]")
        try:
            assert refer_cancel_btn.get_property("disabled") == True
        except:
            testResult = "failed"
            reason.append("4 steps failed\n")

        # 5 steps start! : 병원 리스트에서 임의의 판독의를 클릭한다.        
        # 선택한 병원의 Reporter list 저장
        time.sleep(1)
        reporter_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-sub-item")
        reporter_cnt = len(reporter_list)
        select_reporter_list = []

        for i in reporter_list:
            select_reporter_list.append((i.get_property("dataset"))["reporterKey"])

        # 선택한 병원에서 임의의 Reporter 클릭
        time.sleep(1)
        reporter_key = (reporter_list[random.randrange(0,reporter_cnt+1)].get_property("dataset"))["reporterKey"]
        btn = driver.find_element(By.CSS_SELECTOR, "#institution_reporter_list_row_"+str(reporter_key))
        driver.execute_script("arguments[0].click()",btn)

        # Refer Cancel(All) 버튼이 표시되는지 확인
        try:
            btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[3]")
            assert btn.get_property("disabled") == False
        except:
            testResult = "failed"
            reason.append("5 steps failed\n")

        # 6 steps start! : 임의의 판독의를 클릭하고 Refer Cancel(All) 버튼을 클릭한다. 
        # Job list 저장
        request = driver.wait_for_request('.*/GetReferedListByReporter.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        before_job_list = []

        for i in data:
            before_job_list.append(i["JobKey"])

        # Refer Cancel(All) 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[3]").click()

        # Refer Cancel(All) 팝업창 > Close 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[11]/div/div/div[3]/button[2]").click()
        
        # 선택했던 Reporter 다시 클릭해서 job list 저장
        btn = driver.find_element(By.CSS_SELECTOR, "#institution_reporter_list_row_"+str(reporter_key))
        driver.execute_script("arguments[0].click()",btn)
        time.sleep(1)

        request = driver.wait_for_request('.*/GetReferedListByReporter.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        after_job_list = []

        for i in data:
            after_job_list.append(i["JobKey"])

        # Job list에 refer 된 job이 그대로 유지되는지 확인
        try:
            assert before_job_list == after_job_list
        except:
            testResult = "failed"
            reason.append("6 steps failed\n")

        # Refer Cancel(All) 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[3]").click()

        # Refer Cancel(All) 팝업창 > OK 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[11]/div/div/div[3]/button[1]").click()

        # 테스트 병원의 Report list 저장
        time.sleep(1)
        reporter_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-sub-item")
        reporter_cnt = len(reporter_list)
        changes_reporter_list = []        
        
        for i in reporter_list:
            changes_reporter_list.append((i.get_property("dataset"))["reporterKey"])

        # 테스트 병원에서 선택했던 Reporter가 사라졌는지 확인
        try:
            assert reporter_key not in changes_reporter_list
        except:
            testResult = "failed"
            reason.append("6 steps failed\n")
        
        # Refer Cancel 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1701, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1701, testPlanID, buildName, 'p', "Refer Cancel Passed")

    def Refer_Cancel_And_Refer():
        print("ITR-32: Worklist > Refer Cancel and Refer")
        testResult = ''
        reason = list()

        # 1 steps start! : 판독의에게 할당된 임의의 의뢰 검사를 선택하고, Refer Cancel and Refer 버튼을 클릭한다.
        # Refer 탭 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Show entries를 100개로 변경
        Common.refer_show_entries(100)

        # 선택한 병원의 Reporter list 저장
        time.sleep(1)
        reporter_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-sub-item")
        reporter_id_key_list = []

        for i in reporter_list:
            temp = []
            temp.append((i.get_property("dataset"))["reporterId"])
            temp.append((i.get_property("dataset"))["reporterKey"])
            reporter_id_key_list.append(temp)

        # All Assigned List 탭 클릭 후, job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            job_list.append(i["JobKey"])

        # All Assigned List > 임의의 job 선택
        job_key = random.choice(job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # All Assigned List > R.Cancel & Refer 클릭
        btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[4]")
        if btn.get_property("disabled") == False:
            btn.click()

        # R.Cancel & Refer 팝업창 확인
        try:
            popup_title = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[1]/h4")
            assert popup_title.get_property("textContent") == "Refer Cancel & Refer"
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # R.Cancel & Refer 팝업창 > Reporter list 저장
        time.sleep(1)
        temp_list = ''
        temp_list = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul").get_property("outerText")
        
        reporter_list = temp_list.split('\n')
        reporter_id_list = []

        for i in reporter_list:
            reporter_id_list.append(i.split()[0])

        # R.Cancel & Refer 팝업창 > Reporter list에서 repoter의 수를 확인
        reporter_cnt = len(reporter_list)
        count_list = []
        if reporter_cnt > 1:
            for i in range(1, reporter_cnt+1):
                count_list.append(i)
        else:
            reporter_cnt = 1

        # R.Cancel & Refer 팝업창 > 임의의 Reporter를 임의의 숫자만큼 선택 후, reporter list 저장
        select_reporter_list = []
        selected_reporter_list = []
        if int(reporter_cnt) > 1:
            i = 0
            cnt = random.randrange(1, reporter_cnt+1)
            while i < int(cnt):
                n = count_list.pop(count_list.index(random.choice(count_list)))
                select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").get_property("textContent"))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").click()
                selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[2]/ul/li["+str(n)+"]").get_property("textContent"))
                i = i + 1
        else:
            select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").click()
            selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))

        # 선택한 Reporter ID 저장
        selected_reporter_id_list = []
        for i in selected_reporter_list:
            selected_reporter_id_list.append(i.split()[0])

        # R.Cancel & Refer 팝업창 > Save 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[3]/button[1]").click()

        # 테스트 병원에서 선택한 Reporter를 순서대로 클릭하면서 refer 됐는지 확인
        for i in selected_reporter_id_list:
            for j in reporter_id_key_list:
                if j[0] == i:
                    del driver.requests
                    time.sleep(1)
                    btn = driver.find_element(By.CSS_SELECTOR, "#institution_reporter_list_row_"+str(j[1]))
                    driver.execute_script("arguments[0].click()",btn)
                    time.sleep(1)

                    request = driver.wait_for_request('.*/GetReferedListByReporter.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]
                    after_job_list = []

                    for i in data:
                        after_job_list.append(i["JobKey"])
                    
                    try:
                        assert job_key in after_job_list
                    except:
                        testResult = "failed"
                        reason.append("1 steps failed\n")

        # 2 steps start! : Refer 된 Job와 Refer 되지 않은 Job을 함께 선택한다.
        # 테스트 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # All List 탭 클릭 후, job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        refer_job_list = []
        job_list = []

        for i in data:
            if i["ReferDate"] == None:
                job_list.append(i["JobKey"])
            else:
                refer_job_list.append(i["JobKey"])

        # Refer 된 job과 Refer 되지 않는 job을 함께 선택
        refer_job = random.choice(refer_job_list)
        not_refer_job = random.choice(job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(refer_job)+"']").click()
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(not_refer_job)+"']").click()

        # R.Cancel & Refer 버튼이 비활성화 상태인지 확인
        try:
            btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[4]")
            assert btn.get_property("disabled") == True
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")
        
        # 다음 테스트를 위해 선택 해제(새로고침)
        time.sleep(1)
        driver.refresh()

        # Test 병원 선택
        time.sleep(1)
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()
        
        # All List 탭 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # 3 steps start! : All Assigned/All List에서 Refer 된 Job을 선택한다.
        # All List > Refer 된 job 만 선택
        time.sleep(1)
        for i in range(0,3):
            refer_job_key = refer_job_list.pop(refer_job_list.index(random.choice(refer_job_list)))
            time.sleep(1)
            # driver.find_element(By.XPATH, "//td[normalize-space()='"+str(refer_job_key)+"']").click()
            driver.find_element(By.XPATH, "//label[@for='r_j_c_"+str(refer_job_key)+"']").click()
            
        # R.Cancel & Refer 버튼이 활성화 상태인지 확인
        btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[4]")
        try:
            assert btn.get_property("disabled") == False
        except:
            testResult = "failed"
            reason.append("3 steps failed\n")

        # 새로고침
        time.sleep(1)
        driver.refresh()
        del driver.requests

        # Test 병원 선택
        time.sleep(1)
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()
        
        # All Assigned List > job list 저장
        time.sleep(1)
        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            job_list.append(i["JobKey"])

        # 임의의 job 선택 후, R.Cancel & Refer 버튼이 활성화 상태인지 확인
        job_key = random.choice(job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()
        time.sleep(1)

        try:
            assert driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[4]").get_property("disabled") == False
        except:
            testResult = "failed"
            reason.append("3 steps failed\n")

        # 4 steps start! : 임의의 의뢰 검사를 선택한 후, Refer Cancel & Refer 버튼을 클릭한다.
        # R.Cancel & Refer 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[4]").click()

        # R.Cancel & Refer 팝업창이 팝업되는지 확인
        try:
            popup_title = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[1]/h4")
            assert popup_title.get_property("textContent") == "Refer Cancel & Refer"
        except:
            testResult = "failed"
            reason.append("4 steps failed\n")

        # 5 steps start! : 판독의를 선택한 후, Save 버튼을 클릭한다.
        # R.Cancel & Refer 팝업창 > Reporter list 저장
        time.sleep(1)
        temp_list = ''
        temp_list = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul").get_property("outerText")
        
        reporter_list = temp_list.split('\n')
        reporter_id_list = []

        for i in reporter_list:
            reporter_id_list.append(i.split()[0])

        # R.Cancel & Refer 팝업창 > Reporter list에서 repoter의 수를 확인
        reporter_cnt = len(reporter_list)
        count_list = []
        if reporter_cnt > 1:
            for i in range(1, reporter_cnt+1):
                count_list.append(i)
        else:
            reporter_cnt = 1

        # R.Cancel & Refer 팝업창 > 임의의 Reporter를 임의의 숫자만큼 선택 후, reporter list 저장
        select_reporter_list = []
        selected_reporter_list = []
        if int(reporter_cnt) > 1:
            i = 0
            cnt = random.randrange(1, reporter_cnt+1)
            while i < int(cnt):
                n = count_list.pop(count_list.index(random.choice(count_list)))
                select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").get_property("textContent"))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").click()
                selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[2]/ul/li["+str(n)+"]").get_property("textContent"))
                i = i + 1
        else:
            select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").click()
            selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))

        # 선택한 Reporter ID 저장
        selected_reporter_id_list = []
        for i in selected_reporter_list:
            selected_reporter_id_list.append(i.split()[0])

        # R.Cancel & Refer 팝업창 > Save 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[3]/button[1]").click()

        # 테스트 병원에서 Refer 한 Reporter를 선택하고 refer 한 job이 job list에 있는지 확인
        for i in selected_reporter_id_list:
            for j in reporter_id_key_list:
                if j[0] == i:
                    del driver.requests
                    btn = driver.find_element(By.CSS_SELECTOR, "#institution_reporter_list_row_"+str(j[1]))
                    try:
                        driver.execute_script("arguments[0].click()",btn)
                    except:
                        driver.find_element(By.CSS_SELECTOR, "#institution_reporter_list_row_"+str(j[1])).click()
                    time.sleep(1)

                    request = driver.wait_for_request('.*/GetReferedListByReporter.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]
                    after_job_list = []

                    for i in data:
                        after_job_list.append(i["JobKey"])
                    
                    try:
                        assert job_key in after_job_list
                    except:
                        testResult = "failed"
                        reason.append("5 steps failed\n")

        # 6 steps start! : 판독의에게 할당된 임의의 의뢰 검사를 선택하고, Refer Cancel & Refer 버튼을 클릭한다.
        # 선택한 병원의 Reporter list 저장
        time.sleep(1)
        reporter_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-sub-item")
        reporter_cnt = len(reporter_list)
        select_reporter_list = []

        for i in reporter_list:
            select_reporter_list.append((i.get_property("dataset"))["reporterKey"])

        # 선택한 병원에서 임의의 Reporter 클릭
        time.sleep(1)
        del driver.requests
        reporter_key = (reporter_list[random.randrange(0,reporter_cnt)].get_property("dataset"))["reporterKey"]
        btn = driver.find_element(By.CSS_SELECTOR, "#institution_reporter_list_row_"+str(reporter_key))
        driver.execute_script("arguments[0].click()",btn)

        # Reporter의 refer 받은 job list 저장
        request = driver.wait_for_request('.*/GetReferedListByReporter.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        refer_job_list = []

        for i in data:
            refer_job_list.append(i["JobKey"])

        # 임의의 job 선택 후, R.Cancel & Refer 버튼 클릭
        job_key_list = []
        refer_job_cnt = len(refer_job_list)
        for i in range(0, refer_job_list if refer_job_cnt < 2 else 2):
            job_key = refer_job_list.pop(refer_job_list.index(random.choice(refer_job_list)))
            time.sleep(1)
            driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()
            job_key_list.append(job_key)
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[4]").click()

        # R.Cancel & Refer 팝업창 > Reporter list 저장
        time.sleep(1)
        temp_list = ''
        temp_list = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul").get_property("outerText")
        
        reporter_list = temp_list.split('\n')
        reporter_id_list = []

        for i in reporter_list:
            reporter_id_list.append(i.split()[0])

        # R.Cancel & Refer 팝업창 > Reporter list에서 repoter의 수를 확인
        reporter_cnt = len(reporter_list)
        count_list = []
        if reporter_cnt > 1:
            for i in range(1, reporter_cnt+1):
                count_list.append(i)
        else:
            reporter_cnt = 1

        # R.Cancel & Refer 팝업창 > 임의의 Reporter를 임의의 숫자만큼 선택 후, reporter list 저장
        select_reporter_list = []
        selected_reporter_list = []
        if int(reporter_cnt) > 1:
            i = 0
            cnt = random.randrange(1, reporter_cnt+1)
            while i < int(cnt):
                n = count_list.pop(count_list.index(random.choice(count_list)))
                select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").get_property("textContent"))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li["+str(n)+"]").click()
                selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[2]/ul/li["+str(n)+"]").get_property("textContent"))
                i = i + 1
        else:
            select_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").click()
            selected_reporter_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]").get_property("textContent"))

        # 선택한 Reporter ID 저장
        selected_reporter_id_list = []
        for i in selected_reporter_list:
            selected_reporter_id_list.append(i.split()[0])

        # R.Cancel & Refer 팝업창 > Save 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[3]/button[1]").click()

        # 테스트 병원에서 Refer 한 Reporter를 선택하고 refer 한 job이 job list에 있는지 확인
        for i in selected_reporter_id_list:
            for j in reporter_id_key_list:
                if j[0] == i:
                    del driver.requests
                    btn = driver.find_element(By.CSS_SELECTOR, "#institution_reporter_list_row_"+str(j[1]))
                    driver.execute_script("arguments[0].click()",btn)
                    time.sleep(1)

                    request = driver.wait_for_request('.*/GetReferedListByReporter.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]
                    after_job_list = []

                    for i in data:
                        after_job_list.append(i["JobKey"])
                    
                    try:
                        for i in job_key_list:
                            assert i in after_job_list
                    except:
                        testResult = "failed"
                        reason.append("6 steps failed\n")

        # 7 steps start! : Not Assigned List로 이동한 후, 임의의 Job을 선택한다.
        # 다음 테스트를 위해 선택 해제(새로고침)
        time.sleep(1)
        driver.refresh()

        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Not Assigned List 탭 클릭 후, job list 저장
        time.sleep(1.5)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        not_assigned_job_list = []

        for i in data:
            not_assigned_job_list.append(i["JobKey"])

        # Not Assigned List > 임의의 job 선택
        job_key = random.choice(not_assigned_job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()
        
        # Not Assigned List > R.Cancel & Refer 버튼이 표시되지 않는지 확인
        try:
            btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[4]")
            assert btn.get_property("disabled") == True
        except:
            testResult = "failed"
            reason.append("7 steps failed\n")

        # Refer Cancel and Refer 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1711, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1711, testPlanID, buildName, 'p', "Refer Cancel and Refer Passed")

    def Set_Schedule():
        print("ITR-34: Worklist > Set Schedule")
        testResult = ''
        reason = list()

        # 1 steps start! : Job stat이 Requested 인 임의의 의뢰 검사를 선택한 후, Schedule 버튼을 클릭한다.
        # 다음 테스트를 위해 선택 해제(새로고침)
        time.sleep(1)
        driver.refresh()

        # # Refer 탭 클릭
        # time.sleep(0.5)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        time.sleep(1)
        del driver.requests
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Show entries를 100개로 변경
        Common.refer_show_entries(100)

        # All Assigned List에서 schedule이 없는 job list 저장
        time.sleep(1)
        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        before_assigned_job_list = []

        for i in data:
            if i["ScheduleDateDTTMString"] == "":
                before_assigned_job_list.append(i["JobKey"])

        # All Assigned List > 임의의 job 선택
        job_key = random.choice(before_assigned_job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # All Assigned List > Schedule 버튼 클릭
        schedule_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/button[1]")
        if schedule_btn.get_property("disabled") == False:
            for i in range(0,3):
                time.sleep(0.5)
                schedule_btn.click()

        # All Assigned List > Schedule 버튼 옆에 날짜와 시간 선택 기능이 표시되는지 확인
        input_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/div")
        try:
            time.sleep(1)
            assert "display: inline-block" in input_date.get_attribute("style")
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! : 임의의 날짜와 시간을 입력한 후, 확인 버튼을 클릭한다.
        # All Assigned List > Schedule 날짜는 기본값, 시간은 1030으로 입력 후, 체크 클릭
        input_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/div/div/div[2]/div/div[1]/input").get_property("value")
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/div/div/div[2]/div/div[2]/input").send_keys("1030")
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/div/div/button").click()

        # Schedule 등록 완료 팝업창이 팝업되는지 확인
        try:
            popup_msg = driver.find_element(By.XPATH ,"/html/body/div[6]/h2")
            assert popup_msg.get_property("textContent") == "예약 환자가 등록되었습니다"
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # Schedule 팝업창 > 확인 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[6]/div[7]/div/button").click()

        # All Assigned List에서 schedule이 있는 job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        after_assigned_job_list = []

        for i in data:
            if i["ScheduleDateDTTMString"] != "":
                after_assigned_job_list.append(i)

        # 선택한 job의 Schedule 컬럼에 입력한 날짜와 시간이 표시되는지 확인
        try:
            for i in after_assigned_job_list:
                if i["JobKey"] == job_key:
                    check_date = i["ScheduleDateDTTMString"].split()[0]
                    check_time = i["ScheduleDateDTTMString"].split()[1]

            assert (check_date, check_time.replace(":", "")) == (input_date, "103000")
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # 3 steps start! : Job stat이 Requested 인 임의의 의뢰 검사를 선택한 후, Schedule 버튼을 클릭한다.
        # All Assigned List > Schdule이 있는 임의의 job을 선택한 후, Schedule 버튼 클릭
        sample_job = random.choice(after_assigned_job_list)
        job_key = sample_job["JobKey"]
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()
        
        schedule_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/button[1]")
        if schedule_btn.get_property("disabled") == False:
            schedule_btn.click()

        # All Assigned List > Schedule 버튼 옆에 날짜와 시간 선택 기능이 표시되는지 확인
        input_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/div")
        try:
            time.sleep(1)
            assert "display: inline-block" in input_date.get_attribute("style")
        except:
            testResult = "failed"
            reason.append("3 steps failed\n")

        # 4 steps start! : 임의의 날짜와 시간을 입력한 후, 확인 버튼을 클릭한다.
        # All Assigned List > Schedule 날짜와 시간 입력 후, 체크 클릭
        check_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/div/div/div[2]/div/div[1]/input")
        check_time = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/div/div/div[2]/div/div[2]/input")
        input_date = (today + relativedelta(months=1)).strftime('%Y-%m-%d') 
        check_date.clear()
        check_date.send_keys(input_date)
        check_time.send_keys("1100")
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/div/div/button").click()

        # Schedule 팝업창이 팝업되는지 확인
        try:
            time.sleep(1)
            popup_msg = driver.find_element(By.XPATH ,"/html/body/div[6]/h2")
            assert popup_msg.get_property("textContent") == "예약 정보가 변경되었습니다"
        except:
            testResult = "failed"
            reason.append("4 steps failed\n")

        # Schedule 팝업창 > 확인 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[6]/div[7]/div/button").click()

        # All Assigned List의 job list 저장
        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        change_assigned_job_list = []

        for i in data:
            change_assigned_job_list.append(i)

        # 선택한 job의 Schedule 컬럼에 입력한 날짜와 시간이 표시되는지 확인
        try:
            for i in change_assigned_job_list:
                if i["JobKey"] == job_key:
                    check_date = i["ScheduleDateDTTMString"].split()[0]
                    check_time = i["ScheduleDateDTTMString"].split()[1]
            assert (check_date, check_time.replace(":", "")) == ((today + relativedelta(months=1)).strftime('%Y-%m-%d'), "110000")
        except:
            testResult = "failed"
            reason.append("5 steps failed\n")

        # Set Schedule 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1718, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1718, testPlanID, buildName, 'p', "Set Schedule Passed")        

    def Schedule_Cancel():
        print("ITR-35: Worklist > Cancel Schedule")
        testResult = ''
        reason = list()

        # 1 steps start! : Schedule이 없는 임의의 의뢰 job을 선택한 후, Schedule Cancel 버튼을 클릭한다.
        # Refer 탭 클릭
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        time.sleep(1)
        del driver.requests
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Show entries를 100개로 변경
        Common.refer_show_entries(100)

        # All Assigned List에서 schedule이 없는 job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        not_schedule_job_list = []

        for i in data:
            if i["ScheduleDate"] == None:
                not_schedule_job_list.append(i)

        # All Assigned List > Schedule이 없는 임의의 job 선택
        sample_job = random.choice(not_schedule_job_list)
        job_key = sample_job["JobKey"]
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # All Assigned List > S.Cancel 클릭
        btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/button[2]")
        if btn.get_property("disabled") == False:
            btn.click()

        # S.Cancel 팝업창 확인
        time.sleep(1)
        popup = driver.find_element(By.XPATH, "/html/body/div[6]/h2")
        try:
            assert popup.get_property("textContent") == "예약건만 취소 가능합니다"
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # OK 버튼 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[6]/div[7]/div/button").click()

        # 2 steps start! : Schedule이 있는 임의의 의뢰 job을 선택한 후, Schedule Cancel 버튼을 클릭한다.
        # All Assigned List에서 schedule이 있는 job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        schedule_job_list = []

        for i in data:
            if i["ScheduleDate"] != None:
                schedule_job_list.append(i)

        # All Assigned List > Schedule이 있는 임의의 job 선택
        sample_job = random.choice(schedule_job_list)
        job_key = sample_job["JobKey"]
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # All Assigned List > S.Cancel 클릭
        btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/button[2]")
        if btn.get_property("disabled") == False:
            btn.click()

        # S.Cancel 팝업창 확인
        time.sleep(1)
        popup = driver.find_element(By.XPATH, "/html/body/div[6]/h2")
        try:
            assert popup.get_property("textContent") == "예약이 취소되었습니다"
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # OK 버튼 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[6]/div[7]/div/button").click()

        # All Assigned List > Schedule이 없는 job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        not_schedule_job_list = []

        for i in data:
            if i["ScheduleDate"] != None:
                not_schedule_job_list.append(i)

        # schedule 컬럼에서 S.Cancel 했던 job의 정보가 표시되지 않는지 확인
        try:
            for i in not_schedule_job_list:
                if i["JobKey"] == job_key:
                    assert i["ScheduleDateDTTMString"] == ""
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # 3 steps start! : 임의의 의뢰 검사를 선택한 후, Schedule 버튼을 클릭한다.
        # All Assigned List > job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        schedule_job_list = []
        non_schedule_job_list = []

        for i in data:
            if i["ScheduleDate"] != None:
                schedule_job_list.append(i)
            else:
                non_schedule_job_list.append(i)

        # All Assigned List > Schedule 있는 job과 Schedule이 없는 job을 함께 선택
        schedule_job = (random.choice(schedule_job_list))["JobKey"]
        non_schedule_job = (random.choice(non_schedule_job_list))["JobKey"]
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(schedule_job)+"']").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(non_schedule_job)+"']").click()

        # All Assigned List > Schedule 버튼 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/button[1]").click()
        
        # Schedule 팝업창 확인
        popup = driver.find_element(By.XPATH, "/html/body/div[6]/h2")
        try:
            assert popup.get_property("textContent") == "동일한 예약상태가 아닌 경우 수정이 불가합니다"
        except:
            testResult = "failed"
            reason.append("3 steps failed\n")

        # OK 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/div[6]/div[7]/div/button").click()

        # 4 steps start! : 임의의 의뢰 검사를 선택한 후, Schedule Cancel 버튼을 클릭한다.
        # All Assigned List > S.Cancel 클릭
        btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/button[2]")
        if btn.get_property("disabled") == False:
            btn.click()

        # S.Cancel 팝업창 확인
        time.sleep(1)
        popup = driver.find_element(By.XPATH, "/html/body/div[6]/h2")
        try:
            assert popup.get_property("textContent") == "동일한 예약상태가 아닌 경우 취소가 불가합니다"
        except:
            testResult = "failed"
            reason.append("4 steps failed\n")

        # S.Cancel 팝업창 > OK 클릭
        time.sleep(1)
        driver.find_element(by.XPATH, "/html/body/div[6]/div[7]/div/button").click()
        
        # Schedule 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1724, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1724, testPlanID, buildName, 'p', "Schedule Passed")    

    def Revised():
        print("ITR-36: Worklist > Revised")
        testResult = ''
        reason = list()

        # 1 steps start! : Job Status가 Completed 상태인 의뢰 검사를 선택한 후, Revised 버튼을 클릭한다.
        # Configuration > Institutions > 테스트 병원 선택
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[5]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/button[4]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[2]/div/div[1]/div/div/input").send_keys("997")
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[2]/div/div[1]/div/div/input").send_keys(Keys.RETURN)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#i_l_997").click()
        
        # Configuration > Institutions > Institution Modify > Enable Revised 체크
        popup = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[1]/h3")
        revised = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[1]/div[7]/div/div/input")
        time.sleep(1)
        try:
            if popup.get_property("textContent") == "Institutions Modify":
                if revised.get_property("checked") == False:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[1]/div[7]/div/div/label").click()
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[3]/div/button[2]").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()
            time.sleep(1.5)
            driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # Refer 탭 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        time.sleep(1)
        del driver.requests
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Show entries를 100개로 변경
        Common.refer_show_entries(100)

        # All List 탭 클릭 후, job list 저장
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            job_list.append(i)

        # Search Condition > Job status를 Completed로 선택 후, Search 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        time.sleep(0.25)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[5]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

        # All List > Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        search_job_list = []

        for i in data:
            search_job_list.append(i)

        # All List > 검색 결과 중 임의의 job 선택
        try:
            sample_job = random.choice(search_job_list)
            job_key = sample_job["JobKey"]
            time.sleep(1)
            driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()
        except IndexError:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # Revised 클릭
        btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[3]/button[1]")
        if btn.get_property("disabled") == False:
            btn.click()
        
        # Update Request Status 팝업창 확인
        time.sleep(0.5)
        popup = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[1]/h4")
        try:
            assert popup.get_property("textContent") == "Update Request Status"
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # Update Request Status 팝업창 > Close 클릭
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[3]/button[2]").click()

        # 다시 Revised 클릭
        if btn.get_property("disabled") == False:
            btn.click()

        # Update Request Status 팝업창 > OK 클릭
        time.sleep(0.5)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[3]/button[1]").click()

        # All List > job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        change_job_list = []

        for i in data:
            change_job_list.append(i)

        # Completed job list에서 Revised 한 job이 사라졌는지 확인
        try:
            for i in change_job_list:
                assert i["JobKey"] != job_key
        except IndexError:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # Revised 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1730, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1730, testPlanID, buildName, 'p', "Revised Passed")    

    def Discard():
        print("ITR-37: Worklist > Discard")
        testResult = ''
        reason = list()

        # 1 steps start! : 임의의 의뢰 검사를 선택한 후, Discard 버튼을 클릭한다.
        # Configuration > Institutions > 테스트 병원 선택
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[5]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/button[4]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[2]/div/div[1]/div/div/input").send_keys("997")
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[2]/div/div[1]/div/div/input").send_keys(Keys.RETURN)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#i_l_997").click()
        
        # Configuration > Institutions > Institution Modify > Enable Discard 체크
        popup = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[1]/h3")
        discard = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[1]/div[8]/div/div/input")
        time.sleep(1)
        try:
            if popup.get_property("textContent") == "Institutions Modify":
                if discard.get_property("checked") == False:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[1]/div[8]/div/div/label").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[3]/div/button[2]").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()
            time.sleep(1.5)
            driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # Refer 탭 클릭
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        time.sleep(1)
        del driver.requests
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Show entries를 100개로 변경
        Common.refer_show_entries(100)

        # All Assigend List > job list 저장
        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            job_list.append(i)

        # All Assigend List > 임의의 job 선택
        sample_job = random.choice(job_list)
        job_key = sample_job["JobKey"]
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # All Assigend List > Discard 클릭
        time.sleep(1)
        btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[3]/button[2]")
        if btn.get_property("disabled") == False:
            btn.click()

        # Discard 팝업창 확인
        popup = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[1]/h4")
        try:
            assert popup.get_property("textContent") == "Update Request Status"
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")
        
        # Discard 팝업창 > Close 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[3]/button[2]").click()

        # All Assigend List > job list 저장
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()
        time.sleep(1)
        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        close_job_list = []

        for i in data:
            close_job_list.append(i)

        # Discard 이전의 job list와 비교
        try:
            assert len(job_list) == len(close_job_list)
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # All Assigend List > 임의의 job 선택
        sample_job = random.choice(job_list)
        job_key = sample_job["JobKey"]
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()
        
        # All Assigend List > Discard 클릭
        time.sleep(1)
        btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[3]/button[2]")
        if btn.get_property("disabled") == False:
            btn.click()

        # Discard 팝업창 > OK 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[3]/button[1]").click()

        # All Assigend List > job list 저장
        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        discard_job_list = []

        for i in data:
            discard_job_list.append(i)

        # Discard 후, 이전의 job list에서 해당 job이 사라졌는지 확인
        try:
            assert job_key not in discard_job_list
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! :Job Stauts가 DiscardRequest 인 의뢰 검사를 선택한 후, Discard 버튼을 클릭한다.
        # All List 탭 클릭
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # Search filter > Job status를 DiscardRequest로 선택 후, Search 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[12]").click()
        time.sleep(0.5)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
        time.sleep(1)

        # 조회 결과의 job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        discard_job_list = []

        for i in data:
            discard_job_list.append(i)

        # All List > 임의의 job 선택
        sample_job = random.choice(discard_job_list)
        job_key = sample_job["JobKey"]
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # Discard 버튼이 비활성화 상태인지 확인
        try:
            btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[3]/button[2]")
            assert btn.get_property("disabled") == True
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")
        
        # Discard 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1733, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1733, testPlanID, buildName, 'p', "Discard Passed")    

    def Retry_Request():
        print("ITR-38: Worklist > Retry Request")
        testResult = ''
        reason = list()

        # 1 steps start! : Job Status가 Reported, Completed, Recalled 이외의 상태인 의뢰 검사를 선택한 후, Retry Request 버튼을 클릭한다.
        # Configuration > Institutions > 테스트 병원 선택
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[5]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/button[4]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[2]/div/div[1]/div/div/input").send_keys("997")
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[2]/div/div[1]/div/div/input").send_keys(Keys.RETURN)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#i_l_997").click()
        
        # Configuration > Institutions > Institution Modify > Enable Request 체크
        popup = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[1]/h3")
        discard = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[1]/div[9]/div/div/input")
        time.sleep(1)
        try:
            if popup.get_property("textContent") == "Institutions Modify":
                if discard.get_property("checked") == False:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[1]/div[9]/div/div/label").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[3]/div/button[2]").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()
            time.sleep(1.5)
            driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # Refer 탭 클릭
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        time.sleep(1)
        del driver.requests
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Show entries를 100개로 변경
        Common.refer_show_entries(100)

        # All List 탭 클릭
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # Search condition > Job Status를 All로 선택하고, Search 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[1]").click()
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
        time.sleep(1)

        # All List > Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            if i["StatDescription"] in ("Requested","Canceled2","DiscardCompleted"):
                job_list.append(i)

        # Job status가 Reported, Completed, Recalled 외의 임의의 job을 선택
        try:
            sample_job = random.choice(job_list)
            job_key = sample_job["JobKey"]
            time.sleep(1)
            driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")
        
        # Retry Request 클릭
        time.sleep(2)
        btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[3]/button[3]")
        driver.execute_script("arguments[0].click()",btn)

        # Retry Request 팝업창 확인
        popup = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[1]/h4")
        try:
            popup.get_property("textContent") == "Update Request Status"
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # Retry Request 팝업창 > Close 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[3]/button[2]").click()

        # All List > Retry Request 클릭
        time.sleep(1.5)
        btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[3]/button[3]")
        driver.execute_script("arguments[0].click()",btn)

        # Retry Request 팝업창 > OK 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[3]/button[1]").click()

        # All List > Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            job_list.append(i)
    
        # All List > Job list에서 선택했던 job의 job status가 RetryRequest로 변경되었는지 확인
        try:
            for i in job_list:
                if i["JobKey"] == job_key:
                    assert i["StatDescription"] == "RetryRequest"
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! : Job status가 DiscardCompleted 인 임의의 job을 선택한 후, Retry Request 버튼을 클릭한다.
        # Job status가 DiscardCompleted 인 임의의 job을 선택 후, Retry Request 클릭
        job_list = []
        for i in data:
            if i["StatDescription"] =="DiscardCompleted":
                job_list.append(i)

        # Job status가 DiscardCompleted 인 임의의 job을 선택
        try:
            sample_job = random.choice(job_list)
            job_key = sample_job["JobKey"]
            time.sleep(3)
            driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # Retry Request 클릭
        time.sleep(1)
        btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[3]/button[3]")
        driver.execute_script("arguments[0].click()",btn)

        # Retry Request 팝업창 확인
        popup = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[1]/h4")
        try:
            popup.get_property("textContent") == "Update Request Status"
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # Retry Request 팝업창 > Close 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[3]/button[2]").click()

        # All List > Retry Request 클릭
        time.sleep(1)
        btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[3]/button[3]")
        driver.execute_script("arguments[0].click()",btn)

        # Retry Request 팝업창 > OK 클릭
        time.sleep(0.5)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[3]/button[1]").click()

        # All List > Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            job_list.append(i)
    
        # All List > Job list에서 선택했던 job의 job status가 RetryRequest로 변경되었는지 확인
        try:
            for i in job_list:
                if i["JobKey"] == job_key:
                    assert i["StatDescription"] == "RetryRequest"
        except:
            testResult = "failed"
            reason.append("2 steps failed\n") 

        # Retry Request 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1737, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1737, testPlanID, buildName, 'p', "Retry Request Passed")    

    def Columns():
        print("ITR-39: Worklist > Columns")
        testResult = ''
        reason = list()

        # 1 steps start! : Columns 버튼을 클릭한다.
        # 새로고침
        time.sleep(1)
        driver.refresh()

        # Test 병원 선택
        time.sleep(1)
        del driver.requests
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # All Assigned List > Column list 저장
        column_list = []
        columns = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div[1]/div/table/thead/tr").get_property("outerText")
        column_list = columns.split('\t')
        del column_list[0]

        # Columns 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[5]/div[1]/button").click()

        # Columns 팝업창 확인
        popup = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[1]/h4")
        try:
            popup.get_property("textContent") == "Display Column Setting"
        except:
            testResult = "failed"
            reason.append("1 steps failed\n") 

        # 2 steps start! : Not Display Column과 Display Column에 컬럼들을 위치시키고 Save 버튼을 클릭한다.
        # Columns 팝업창 > Display Column의 column list 저장
        time.sleep(1)
        diplay_column_list = []
        display_column_index_list = []
        display_column = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[2]/div/div/div[3]/select/option")
        for i in display_column:
            temp = []
            temp.append(i.text)
            temp.append(i.get_attribute("value"))
            display_column_index_list.append(i.text)
            diplay_column_list.append(temp)

        # Columns 팝업창 > Display Column에서 임의의 Column을 선택해서 Not Display Column으로 변경
        select_column = random.choice(display_column_index_list)
        for i in diplay_column_list:
            if i[0] == select_column:
                driver.find_element(By.CSS_SELECTOR, "#job-column-setting-selected-"+str(i[1])).click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[2]/div/div/div[2]/button[2]").click()

        # Columns 팝업창 > Display Column의 column list 저장
        time.sleep(1)
        diplay_column_list = []
        display_column_index_list = []
        display_column = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[2]/div/div/div[3]/select/option")
        for i in display_column:
            temp = []
            temp.append(i.text)
            temp.append(i.get_attribute("value"))
            display_column_index_list.append(i.text)
            diplay_column_list.append(temp)

        # Save 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[3]/button[1]").click()

        # All Assigned List > Column list 저장
        time.sleep(4)
        column_list = []
        columns = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div[1]/div/table/thead/tr").get_property("outerText")
        column_list = columns.split('\t')
        del column_list[0]

        # Display Column의 column list와 All Assigned List의 Column list 비교
        try: 
            assert column_list == display_column_index_list
        except:
            testResult = "failed"
            reason.append("2 steps failed\n") 

        # 3 steps start! : Display Column에서 임의의 column을 선택하고, Up 버튼을 클릭한 후, Save 버튼을 클릭한다.
        # Columns 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[5]/div[1]/button").click()

        # Display Column에서 임의의 column을 선택하고, Up 버튼 클릭
        time.sleep(1)
        select_column = random.choice(display_column_index_list)
        for i in diplay_column_list:
            if i[0] == select_column:
                driver.find_element(By.CSS_SELECTOR, "#job-column-setting-selected-"+str(i[1])).click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[2]/div/div/div[3]/div/button[1]").click()

        # Columns 팝업창 > Display Column의 column list 저장
        time.sleep(1)
        diplay_column_list = []
        display_column_index_list = []
        display_column = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[2]/div/div/div[3]/select/option")
        for i in display_column:
            temp = []
            temp.append(i.text)
            temp.append(i.get_attribute("value"))
            display_column_index_list.append(i.text)
            diplay_column_list.append(temp)

        # Save 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[3]/button[1]").click()

        # All Assigned List > Column list 저장
        time.sleep(4)
        column_list = []
        columns = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div[1]/div/table/thead/tr").get_property("outerText")
        column_list = columns.split('\t')
        del column_list[0] 

        # Display Column의 column list와 All Assigned List의 Column list 비교
        try:
            assert column_list == display_column_index_list
        except:
            testResult = "failed"
            reason.append("3 steps failed\n") 

        # 4 steps start! : Display Column에서 임의의 column을 선택하고, Down 버튼을 클릭한 후, Save 버튼을 클릭한다.
        # Columns 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[5]/div[1]/button").click()

        # Display Column에서 임의의 column을 선택하고, Down 버튼 클릭
        time.sleep(1)
        select_column = random.choice(display_column_index_list)
        for i in diplay_column_list:
            if i[0] == select_column:
                driver.find_element(By.CSS_SELECTOR, "#job-column-setting-selected-"+str(i[1])).click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[2]/div/div/div[3]/div/button[2]").click()

        # Columns 팝업창 > Display Column의 column list 저장
        time.sleep(1)
        display_column_index_list = []
        display_column = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[2]/div/div/div[3]/select/option")
        for i in display_column:
            temp = []
            temp.append(i.text)
            temp.append(i.get_attribute("value"))
            display_column_index_list.append(i.text)

        # Save 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[3]/button[1]").click()

        # All Assigned List > Column list 저장
        time.sleep(3)
        column_list = []
        columns = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div[1]/div/table/thead/tr").get_property("outerText")
        column_list = columns.split('\t')
        del column_list[0] 

        # Display Column의 column list와 All Assigned List의 Column list 비교
        try:
            assert column_list == display_column_index_list
        except:
            testResult = "failed"
            reason.append("4 steps failed\n") 

        # 5 steps start! : Reset 버튼을 클릭한다.
        # Columns 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[5]/div[1]/button").click()

        # Reset 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[2]/div/div/div[1]/div/button").click()

        # Columns 팝업창 > Display Column의 column list 저장
        time.sleep(1)
        diplay_column_list = []
        display_column_index_list = []
        display_column = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[2]/div/div/div[3]/select/option")
        for i in display_column:
            temp = []
            temp.append(i.text)
            temp.append(i.get_attribute("value"))
            display_column_index_list.append(i.text)
            diplay_column_list.append(temp)

        # Save 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[3]/button[1]").click()

        # All Assigned List > Column list 저장
        time.sleep(3)
        column_list = []
        columns = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div[1]/div/table/thead/tr").get_property("outerText")
        column_list = columns.split('\t')
        del column_list[0] 

        # Display Column의 column list와 All Assigned List의 Column list 비교
        try:
            assert column_list == display_column_index_list
        except:
            testResult = "failed"
            reason.append("5 steps failed\n") 

        # 6 steps start! : Column의 상태를 임의대로 변경한 후, Cancel 버튼을 클릭한다.
        # Columns 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[5]/div[1]/button").click()

        # Display Column에서 임의의 column을 선택하고, Up 버튼 클릭
        time.sleep(1)
        select_column = random.choice(display_column_index_list)
        for i in diplay_column_list:
            if i[0] == select_column:
                driver.find_element(By.CSS_SELECTOR, "#job-column-setting-selected-"+str(i[1])).click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[2]/div/div/div[3]/div/button[1]").click()

        # Display Column에서 임의의 column을 선택하고, Down 버튼 클릭
        time.sleep(1.5)
        select_column = random.choice(display_column_index_list)
        for i in diplay_column_list:
            if i[0] == select_column:
                driver.find_element(By.CSS_SELECTOR, "#job-column-setting-selected-"+str(i[1])).click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[2]/div/div/div[3]/div/button[2]").click()

        # Columns 팝업창 > Display Column의 column list 저장
        time.sleep(1)
        display_column_index_list = []
        display_column = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[2]/div/div/div[3]/select/option")
        for i in display_column:
            temp = []
            temp.append(i.text)
            temp.append(i.get_attribute("value"))
            display_column_index_list.append(i.text)
        
        # Cancel 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[18]/div/div/div[3]/button[2]").click()

        # All Assigned List > Column list 저장
        time.sleep(3)
        column_list = []
        columns = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div[1]/div/table/thead/tr").get_property("outerText")
        column_list = columns.split('\t')
        del column_list[0]

        # Display Column의 column list와 All Assigned List의 Column list 비교
        try:
            assert column_list != display_column_index_list
        except:
            testResult = "failed"
            reason.append("6 steps failed\n") 
        
        # Columns 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1741, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1741, testPlanID, buildName, 'p', "Columns Passed")    

    def Show_Entries():
        print("ITR-40: Worklist > Show entries")
        testResult = ''
        reason = list()

        # 1 steps start! : Show entries의 개수를 10으로 변경한다.
        # Refer 탭 클릭
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        time.sleep(1)
        del driver.requests
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # All List 탭 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # Show entries를 10으로 변경
        Common.refer_show_entries(10)

        # Showing entries 값 저장
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[3]

        # All List > Job list의 개수가 10개로 표시되는지 확인
        try:
            if int(temp_cnt[5]) > 10:
                assert int(list_cnt) == 10
        except:
            testResult = "failed"
            reason.append("1 steps failed\n") 

        # 2 steps start! : Show entries의 개수를 25으로 변경한다.
        # Show entries를 25로 변경
        Common.refer_show_entries(25)

        # Showing entries 값 저장
        time.sleep(1)
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[3]

        # All List > Job list의 개수가 25개로 표시되는지 확인
        try:
            if int(temp_cnt[5]) > 25:
                assert int(list_cnt) == 25
        except:
            testResult = "failed"
            reason.append("2 steps failed\n") 

        # 3 steps start! : Show entries의 개수를 50으로 변경한다.
        # Show entries를 50으로 변경
        Common.refer_show_entries(50)

        # Showing entries 값 저장
        time.sleep(1)
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[3]

        # All List > Job list의 개수가 50개로 표시되는지 확인
        try:
            if int(temp_cnt[5]) > 50:
                assert int(list_cnt) == 50
        except:
            testResult = "failed"
            reason.append("3 steps failed\n") 

        # 4 steps start! : Show entries의 개수를 100으로 변경한다.
        # Show entries를 100로 변경
        Common.refer_show_entries(100)

        # Showing entries 값 저장
        time.sleep(1)
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[3]

        # All List > Job list의 개수가 100개로 표시되는지 확인
        try:
            if int(temp_cnt[5]) > 100:
                assert int(list_cnt) == 100
        except:
            testResult = "failed"
            reason.append("4 steps failed\n") 
        
        # Show entries 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1749, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1749, testPlanID, buildName, 'p', "Show entries Passed")  

    def Use_Related_Worklist():
        print("ITR-224: Worklist > Use Related Worklist")
        testResult = ''
        reason = list()

        # 1 steps start! : Use Related Worklist에 체크한 후, worklist에서 임의의 의뢰 검사를 선택한다.
        # Refer 탭 클릭
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        time.sleep(1)
        del driver.requests
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # Use Related Worklist 체크
        time.sleep(1)
        check = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[5]/div[3]/input")
        if check.get_property("checked") == False:
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[5]/div[3]/label").click()

        # All List 탭 클릭 후, job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()
        
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []
        temp = []
        
        # All List > job list에서 동일한 Patient ID가 2개 이상인 P.ID를 찾기
        for i in data:
            if i["PatientID"] not in temp:
                temp.append(i["PatientID"])
            else:
                job_list.append(i["JobKey"])

        # All List > 해당 P.ID의 job 선택
        job_key = random.choice(job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()="+str(job_key)+"]").click()

        # All List > Job list에서 Related worklist가 표시되는지 확인
        try:
            assert driver.find_element(By.CSS_SELECTOR, "#refer-related-list_wrapper").get_property("id") == "refer-related-list_wrapper"
        except:
            testResult = "failed"
            reason.append("1 steps failed\n") 
        
        # Use Related Worklist 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(3074, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(3074, testPlanID, buildName, 'p', "Use Related Worklist Passed")  

    def Sort_By():
        print("ITR-41: Worklist > Sort By")
        testResult = ''
        reason = list()

        signInOut.admin_sign_in()

        # 1 steps start! : 정렬 가능한 컬럼을 확인한다.
        # 새로고침
        driver.refresh()

        # Test 병원 선택
        time.sleep(1)
        del driver.requests
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == test_hospital:
                i.click()

        # All Assigend List > 정렬이 가능한 컬럼 저장
        time.sleep(1)
        columns = driver.find_elements(By.XPATH,"/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div[1]/div/table/thead/tr/th")
        column_list = []
        for i in columns:
            if "sort" in i.get_attribute("aria-label"):
                column_list.append(i.get_property("textContent"))

        # All Assigend List > 정렬 가능한 컬럼이 맞는지 확인
        sort_column_list = ["E","I.CNT","P.ID","P.Name","Study Date","Job Date","Upload Date","Mod","Bodypart","Study Desc","Request Name","Department","Schedule","Emer Date","AI Vendor","AI Complex Score","AI Finding Cnt","AI Probability","AI Disease NM","AI Service","Emer Modifier ","Refer Date "]
        try:
            # assert column_list.sort() in sort_column_list.sort() or column_list.sort() == sort_column_list.sort()
            for i in column_list:
                assert i in sort_column_list
        except:
            testResult = "failed"
            reason.append("1 steps failed\n") 

        # Not Assigend List > 정렬이 가능한 컬럼 저장
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()
        time.sleep(1)
        columns = driver.find_elements(By.XPATH,"/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div[1]/div/table/thead/tr/th")
        column_list = []
        for i in columns:
            if "sort" in i.get_attribute("aria-label"):
                column_list.append(i.get_property("textContent"))

        # 정렬 가능한 컬럼이 맞는지 확인
        sort_column_list = ["E","I.CNT","P.ID","P.Name","Study Date","Job Date","Upload Date","Mod","Bodypart","Study Desc","Request Name","Department","Schedule","Emer Date","AI Vendor","AI Complex Score","AI Finding Cnt","AI Probability","AI Disease NM","AI Service","Emer Modifier ","Refer Date "]
        try:
            for i in column_list:
                assert i in sort_column_list
        except:
            testResult = "failed"
            reason.append("1 steps failed\n") 
        
        # All List > 정렬이 가능한 컬럼 저장
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()
        time.sleep(1)
        columns = driver.find_elements(By.CSS_SELECTOR,"#refer-assigned-list_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th")
        column_list = []

        for i in columns:
            temp_list = []
            temp = i.get_attribute("class")
            temp_list = temp.split()
            if "sorting" in temp_list:
                column_list.append(i.get_property("textContent"))

        # 정렬 가능한 컬럼이 맞는지 확인
        sort_column_list = ["Job Date"]
        try:
            assert column_list == sort_column_list
        except:
            testResult = "failed"
            reason.append("1 steps failed\n") 

        # Sort By 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1755, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1755, testPlanID, buildName, 'p', "Sort By Passed")  

class Statistics:
    def SearchFilter_Date():
        print("ITR-44: Statistics > Search Filter > Date")
        testResult = ''
        reason = list()

        signInOut.admin_sign_in()

        # DB 접속
        os.putenv('NLS_LANG', '.UTF8')
        cx_Oracle.init_oracle_client(lib_dir=r"D:\app\user\instantclient_21_7")
        connection = cx_Oracle.connect("pantheon","pantheon","211.43.8.73:1521/spectra", encoding="UTF-8")
        cursor = connection.cursor()

        # 1 steps start! : Date를 Study Date로 선택하고, 임의의 기간을 입력한 후, Search 버튼을 클릭한다.
        # Statistics 탭 클릭
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[4]").click()

        # Show entries 100 변경
        select = Select(driver.find_element(By.CSS_SELECTOR,"#institution-interpretation-list_length > label > select"))                
        select.select_by_value(str(100))

        # Showing entry 결과 저장
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[5]

        # Study Date 선택
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/table/tfoot/tr[2]/th[2]").click()
        start_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").get_property("value")
        start_date = start_date.replace("-","")

        # 임의의 병원 선택
        time.sleep(1)
        temp_hospital_cnt_list = []
        hospital_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/ul/li")
        hospital_cnt = len(hospital_list) - 1

        for i in range(2, hospital_cnt):
            temp_hospital_cnt_list.append(i)

        # 조회 결과가 0이 아닐 때까지 임의의 병원을 찾아서 조회
        inst_code = []
        while list_cnt == '0':
            # 임의의 병원 선택
            driver.find_element(By.CSS_SELECTOR, "#statistics-search-hospital").click()
            time.sleep(1)
            select_hospital = temp_hospital_cnt_list.pop(temp_hospital_cnt_list.index(random.choice(temp_hospital_cnt_list)))
            hospital = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/div/ul/li["+str(select_hospital)+"]/label")
            hospital.click()
            index = (hospital.get_attribute("for")).split('-')[2]
            inst_code.append(driver.find_element(By.CSS_SELECTOR, "#hospital-index-"+str(index)+"-view").get_attribute("value"))

            # Searh 클릭
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[4]/button").click()

            # Showing entry 결과 저장
            time.sleep(4)
            temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
            temp_cnt = temp_cnt.split()
            list_cnt = temp_cnt[5]
            list_cnt = list_cnt.replace(",","")
        inst_code = "','".join(s for s in inst_code)

        # 조회 결과 저장
        result_list = []
        pat_list = []
        result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
        pages = math.ceil(int(list_cnt) / 100)
        
        for page in range(1, pages +1):
            result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
            for i in result_list:
                pat_list.append(i.get_property("outerText").split('\t')[2])
            driver.find_element(By.CSS_SELECTOR, "#institution-interpretation-list_next > a").click()
            time.sleep(2)
        
        # DB에서 선택한 병원을 동일한 조건으로 조회
        end_date = str(today.strftime('%Y%m%d'))
        sql = f"""
            select patient_id from MVIEWINSTSTAT 
            where study_dttm >= to_date('{start_date}', 'YYYY-MM-DD') and study_dttm <= to_date('{end_date}', 'YYYY-MM-DD')
            and institution_code in ('{inst_code}')
            """

        # DB 조회 결과 저장
        cursor.execute(sql)
        row = cursor.fetchall()
        db_pat_id = []
        for i in row:
            db_pat_id.append(i)
        
        # DB 조회 결과와 Admin 조회 결과 비교
        try:
            assert db_pat_id.sort() == pat_list.sort()
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! : Date를 Request Date로 선택하고, 임의의 기간을 입력한 후, Search 버튼을 클릭한다.
        # 페이지 초기화
        driver.refresh()

        # Show entries 100 변경
        select = Select(driver.find_element(By.CSS_SELECTOR,"#institution-interpretation-list_length > label > select"))                
        select.select_by_value(str(100))

        # Date를 Requested Date로 선택
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/section[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]")))
        driver.find_element(By.XPATH, "/html[1]/body[1]/section[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[1]/div/div/ul/li[2]").click()

        # Date 선택
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/table/tfoot/tr[2]/th[2]").click()
        start_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").get_property("value")
        start_date = start_date.replace("-","")

        # Showing entry 결과 저장
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[5]

        # 조회 결과가 0이 아닐 때까지 임의의 병원을 찾아서 조회
        inst_code = []
        while list_cnt == '0':
            # 임의의 병원 선택
            driver.find_element(By.CSS_SELECTOR, "#statistics-search-hospital").click()
            time.sleep(1)
            select_hospital = temp_hospital_cnt_list.pop(temp_hospital_cnt_list.index(random.choice(temp_hospital_cnt_list)))
            hospital = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/div/ul/li["+str(select_hospital)+"]/label")
            hospital.click()
            index = (hospital.get_attribute("for")).split('-')[2]
            inst_code.append(driver.find_element(By.CSS_SELECTOR, "#hospital-index-"+str(index)+"-view").get_attribute("value"))

            # Searh 클릭
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[4]/button").click()

            # Showing entry 결과 저장
            time.sleep(4)
            temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
            temp_cnt = temp_cnt.split()
            list_cnt = temp_cnt[5]
            list_cnt = list_cnt.replace(",","")
        inst_code = "','".join(s for s in inst_code)

        # 조회 결과 저장
        time.sleep(1)
        result_list = []
        pat_list = []
        result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
        pages = math.ceil(int(list_cnt) / 100)
        
        for page in range(1, pages +1):
            result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
            for i in result_list:
                pat_list.append(i.get_property("outerText").split('\t')[2])
            driver.find_element(By.CSS_SELECTOR, "#institution-interpretation-list_next > a").click()
            time.sleep(2)

        # DB에서 선택한 병원을 동일한 조건으로 조회
        end_date = str(today.strftime('%Y%m%d'))
        sql = f"""
            select patient_id from MVIEWINSTSTAT 
            where job_dttm >= to_date('{start_date}', 'YYYY-MM-DD') and job_dttm <= to_date('{end_date}', 'YYYY-MM-DD')
            and institution_code in ('{inst_code}')            
            """

        # DB 조회 결과 저장
        cursor.execute(sql)
        row = cursor.fetchall()
        db_pat_id = []
        for i in row:
            db_pat_id.append(i)

        # DB 조회 결과와 Admin 조회 결과 비교
        try:
            assert db_pat_id.sort() == pat_list.sort()
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # 3 steps start! : Date를 Report Date로 선택하고, 임의의 기간을 입력한 후, Search 버튼을 클릭한다.
        # 페이지 초기화
        driver.refresh()
        
        # Show entries 100 변경
        select = Select(driver.find_element(By.CSS_SELECTOR,"#institution-interpretation-list_length > label > select"))                
        select.select_by_value(str(100))

        # Date를 Report Date로 선택
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/section[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]")))
        driver.find_element(By.XPATH, "/html[1]/body[1]/section[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[1]/div/div/ul/li[3]").click()

        # Date 선택
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/table/tfoot/tr[2]/th[2]").click()
        start_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").get_property("value")
        start_date = start_date.replace("-","")

        # Showing entry 결과 저장
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[5]

        # 조회 결과가 0이 아닐 때까지 임의의 병원을 찾아서 조회
        inst_code = []
        while list_cnt == '0':
            # 임의의 병원 선택
            driver.find_element(By.CSS_SELECTOR, "#statistics-search-hospital").click()
            time.sleep(1)
            select_hospital = temp_hospital_cnt_list.pop(temp_hospital_cnt_list.index(random.choice(temp_hospital_cnt_list)))
            hospital = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/div/ul/li["+str(select_hospital)+"]/label")
            hospital.click()
            index = (hospital.get_attribute("for")).split('-')[2]
            inst_code.append(driver.find_element(By.CSS_SELECTOR, "#hospital-index-"+str(index)+"-view").get_attribute("value"))

            # Searh 클릭
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[4]/button").click()

            # Showing entry 결과 저장
            time.sleep(4)
            temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
            temp_cnt = temp_cnt.split()
            list_cnt = temp_cnt[5]
            list_cnt = list_cnt.replace(",","")
        inst_code = "','".join(s for s in inst_code)

        # 조회 결과 저장
        time.sleep(1)
        result_list = []
        pat_list = []
        result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
        pages = math.ceil(int(list_cnt) / 100)
        
        for page in range(1, pages +1):
            result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
            for i in result_list:
                pat_list.append(i.get_property("outerText").split('\t')[2])
            
            driver.find_element(By.CSS_SELECTOR, "#institution-interpretation-list_next > a").click()
            time.sleep(2)

        # DB에서 선택한 병원을 동일한 조건으로 조회
        end_date = str(today.strftime('%Y%m%d'))
        sql = f"""
            select patient_id from MVIEWINSTSTAT 
            where report_dttm >= to_date('{start_date}', 'YYYY-MM-DD') and report_dttm <= to_date('{end_date}', 'YYYY-MM-DD')
            and institution_code in ('{inst_code}')            
            """

        # DB 조회 결과 저장
        cursor.execute(sql)
        row = cursor.fetchall()
        db_pat_id = []
        for i in row:
            db_pat_id.append(i)

        # DB 조회 결과와 Admin 조회 결과 비교
        try:
            assert db_pat_id.sort() == pat_list.sort()
        except:
            testResult = "failed"
            reason.append("3 steps failed\n")

        # 4 steps start! : Date를 Completed Date로 선택하고, 임의의 기간을 입력한 후, Search 버튼을 클릭한다.
        # 페이지 초기화
        driver.refresh()
        
        # Show entries 100 변경
        select = Select(driver.find_element(By.CSS_SELECTOR,"#institution-interpretation-list_length > label > select"))                
        select.select_by_value(str(100))

        # Date를 Completed Date로 선택
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/section[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]")))
        driver.find_element(By.XPATH, "/html[1]/body[1]/section[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[1]/div/div/ul/li[4]").click()

        # Date 선택
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/table/tfoot/tr[2]/th[2]").click()
        start_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").get_property("value")
        start_date = start_date.replace("-","")

        # Showing entry 결과 저장
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[5]

        # 조회 결과가 0이 아닐 때까지 임의의 병원을 찾아서 조회
        inst_code = []
        while list_cnt == '0':
            # 임의의 병원 선택
            driver.find_element(By.CSS_SELECTOR, "#statistics-search-hospital").click()
            time.sleep(1)
            select_hospital = temp_hospital_cnt_list.pop(temp_hospital_cnt_list.index(random.choice(temp_hospital_cnt_list)))
            hospital = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/div/ul/li["+str(select_hospital)+"]/label")
            hospital.click()
            index = (hospital.get_attribute("for")).split('-')[2]
            inst_code.append(driver.find_element(By.CSS_SELECTOR, "#hospital-index-"+str(index)+"-view").get_attribute("value"))

            # Searh 클릭
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[4]/button").click()

            # Showing entry 결과 저장
            time.sleep(4)
            temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
            temp_cnt = temp_cnt.split()
            list_cnt = temp_cnt[5]
            list_cnt = list_cnt.replace(",","")
        inst_code = "','".join(s for s in inst_code)

        # 조회 결과 저장
        time.sleep(1)
        result_list = []
        pat_list = []
        result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
        pages = math.ceil(int(list_cnt) / 100)
        
        for page in range(1, pages +1):
            result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
            for i in result_list:
                pat_list.append(i.get_property("outerText").split('\t')[2])
            driver.find_element(By.CSS_SELECTOR, "#institution-interpretation-list_next > a").click()
            time.sleep(2)

        # DB에서 선택한 병원을 동일한 조건으로 조회
        end_date = str(today.strftime('%Y%m%d'))
        sql = f"""
            select patient_id from MVIEWINSTSTAT 
            where completed_dttm >= to_date('{start_date}', 'YYYY-MM-DD') and completed_dttm <= to_date('{end_date}', 'YYYY-MM-DD')
            and institution_code in ('{inst_code}')   
            """

        # DB 조회 결과 저장
        cursor.execute(sql)
        row = cursor.fetchall()
        db_pat_id = []
        for i in row:
            db_pat_id.append(i)

        # DB 조회 결과와 Admin 조회 결과 비교
        try:
            assert db_pat_id.sort() == pat_list.sort()
        except:
            testResult = "failed"
            reason.append("4 steps failed\n")

        # 5 steps start! : Date를 Bill Month로 선택하고, 임의의 기간을 입력한 후, Search 버튼을 클릭한다.
        # 페이지 초기화
        driver.refresh()
        
        # Show entries 100 변경
        select = Select(driver.find_element(By.CSS_SELECTOR,"#institution-interpretation-list_length > label > select"))                
        select.select_by_value(str(100))

        # Date를 Bill Month로 선택
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/section[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]")))
        driver.find_element(By.XPATH, "/html[1]/body[1]/section[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[1]/div/div/ul/li[5]").click()

        # Date 선택
        time.sleep(2)
        close_year = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[3]/div[1]/div/a").get_property("textContent")
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[3]/div[2]/div/a").click()
        close_month = int(today.strftime('%m')) - 2
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[3]/div[2]/div/div/ul/li["+str(close_month)+"]").click()
        time.sleep(1)

        # Showing entry 결과 저장
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[5]

        # 조회 결과가 0이 아닐 때까지 임의의 병원을 찾아서 조회
        inst_code = []
        while list_cnt == '0':
            # 임의의 병원 선택
            driver.find_element(By.CSS_SELECTOR, "#statistics-search-hospital").click()
            time.sleep(1)
            select_hospital = temp_hospital_cnt_list.pop(temp_hospital_cnt_list.index(random.choice(temp_hospital_cnt_list)))
            hospital = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/div/ul/li["+str(select_hospital)+"]/label")
            hospital.click()
            index = (hospital.get_attribute("for")).split('-')[2]
            inst_code.append(driver.find_element(By.CSS_SELECTOR, "#hospital-index-"+str(index)+"-view").get_attribute("value"))

            # Searh 클릭
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[4]/button").click()

            # Showing entry 결과 저장
            time.sleep(4)
            temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
            temp_cnt = temp_cnt.split()
            list_cnt = temp_cnt[5]
            list_cnt = list_cnt.replace(",","")
        inst_code = "','".join(s for s in inst_code)

        # 조회 결과 저장
        time.sleep(1)
        result_list = []
        pat_list = []
        result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
        pages = math.ceil(int(list_cnt) / 100)
        
        for page in range(1, pages +1):
            result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
            for i in result_list:
                pat_list.append(i.get_property("outerText").split('\t')[2])
            driver.find_element(By.CSS_SELECTOR, "#institution-interpretation-list_next > a").click()
            time.sleep(2)

        # DB에서 선택한 병원을 동일한 조건으로 조회
        end_date = str(today.strftime('%Y%m%d'))
        if len(str(close_month)) < 2:
            close_month = '0' + str(close_month)
        sql = f"""
            select patient_id from closedbill 
            where closed_year = '{close_year}'
            and closed_month = '{close_month}'
            and closed_stat = 'Y'
            and institution_code in ('{inst_code}')
            """

        # DB 조회 결과 저장
        cursor.execute(sql)
        row = cursor.fetchall()
        db_pat_id = []
        for i in row:
            db_pat_id.append(i)

        # DB 조회 결과와 Admin 조회 결과 비교
        try:
            assert db_pat_id.sort() == pat_list.sort()
        except:
            testResult = "failed"
            reason.append("5 steps failed\n")

        # DB 연결 해제
        cursor.close()
        connection.close()
        
        # Search Filter > Date 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1772, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1772, testPlanID, buildName, 'p', "Search Filter > Date Passed")  

    def SearchFilter_Hospital():
        print("ITR-45: Statistics > Search Filter > Hospital")
        testResult = ''
        reason = list()

        # DB 접속
        os.putenv('NLS_LANG', '.UTF8')
        cx_Oracle.init_oracle_client(lib_dir=r"D:\app\user\instantclient_21_7")
        connection = cx_Oracle.connect("pantheon","pantheon","211.43.8.73:1521/spectra", encoding="UTF-8")
        cursor = connection.cursor()

        # 1 steps start! : Date를 Study Date로 선택하고, 임의의 기간을 입력한 후, Search 버튼을 클릭한다.
        # 페이지 초기화
        driver.refresh()

        # Show entries 100 변경
        select = Select(driver.find_element(By.CSS_SELECTOR,"#institution-interpretation-list_length > label > select"))                
        select.select_by_value(str(100))

        # Showing entry 결과 저장
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[5]

        # Study Date 선택
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/table/tfoot/tr[2]/th[2]").click()
        start_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").get_property("value")
        start_date = start_date.replace("-","")

        # 임의의 병원 선택
        time.sleep(1)
        temp_hospital_cnt_list = []
        hospital_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/ul/li")
        hospital_cnt = len(hospital_list) - 1

        for i in range(2, hospital_cnt):
            temp_hospital_cnt_list.append(i)

        # 조회 결과가 0이 아닐 때까지 임의의 병원을 찾아서 조회
        inst_code = []
        while list_cnt == '0':
            # 임의의 병원 선택
            driver.find_element(By.CSS_SELECTOR, "#statistics-search-hospital").click()
            time.sleep(1)
            select_hospital = temp_hospital_cnt_list.pop(temp_hospital_cnt_list.index(random.choice(temp_hospital_cnt_list)))
            hospital = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/div/ul/li["+str(select_hospital)+"]/label")
            hospital.click()
            index = (hospital.get_attribute("for")).split('-')[2]
            inst_code.append(driver.find_element(By.CSS_SELECTOR, "#hospital-index-"+str(index)+"-view").get_attribute("value"))

            # Searh 클릭
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[4]/button").click()

            # Showing entry 결과 저장
            time.sleep(4)
            temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
            temp_cnt = temp_cnt.split()
            list_cnt = temp_cnt[5]
            list_cnt = list_cnt.replace(",","")
        inst_code = "','".join(s for s in inst_code)

        # 조회 결과 저장
        result_list = []
        pat_list = []
        result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
        pages = math.ceil(int(list_cnt) / 100)
        
        for page in range(1, pages +1):
            result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
            for i in result_list:
                pat_list.append(i.get_property("outerText").split('\t')[2])
            driver.find_element(By.CSS_SELECTOR, "#institution-interpretation-list_next > a").click()
            time.sleep(2)
        
        # DB에서 선택한 병원을 동일한 조건으로 조회
        end_date = str(today.strftime('%Y%m%d'))
        sql = f"""
            select patient_id from MVIEWINSTSTAT 
            where study_dttm >= to_date('{start_date}', 'YYYY-MM-DD') and study_dttm <= to_date('{end_date}', 'YYYY-MM-DD')
            and institution_code in ('{inst_code}')
            """

        # DB 조회 결과 저장
        cursor.execute(sql)
        row = cursor.fetchall()
        db_pat_id = []
        for i in row:
            db_pat_id.append(i)
        
        # DB 조회 결과와 Admin 조회 결과 비교
        try:
            assert db_pat_id.sort() == pat_list.sort()
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # DB 연결 해제
        cursor.close()
        connection.close()
        
        # Search Filter > Hospital 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1779, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1779, testPlanID, buildName, 'p', "Search Filter > Hospital Passed")  

    def SearchFilter_Reporter():
        print("ITR-46: Statistics > Search Filter > Reporter")
        testResult = ''
        reason = list()

        # DB 접속
        os.putenv('NLS_LANG', '.UTF8')
        cx_Oracle.init_oracle_client(lib_dir=r"D:\app\user\instantclient_21_7")
        connection = cx_Oracle.connect("pantheon","pantheon","211.43.8.73:1521/spectra", encoding="UTF-8")
        cursor = connection.cursor()

        # 1 steps start! : Date를 Study Date로 선택하고, 임의의 기간을 입력한 후, Search 버튼을 클릭한다.
        # 페이지 초기화
        driver.refresh()

        # Show entries 100 변경
        select = Select(driver.find_element(By.CSS_SELECTOR,"#institution-interpretation-list_length > label > select"))                
        select.select_by_value(str(100))

        # Showing entry 결과 저장
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[5]

        # Study Date 선택
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/table/tfoot/tr[2]/th[2]").click()
        start_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").get_property("value")
        start_date = start_date.replace("-","")

        # 임의의 병원 선택
        time.sleep(1)
        temp_hospital_cnt_list = []
        hospital_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/ul/li")
        hospital_cnt = len(hospital_list) - 1

        for i in range(2, hospital_cnt):
            temp_hospital_cnt_list.append(i)
        
        # 조회 결과가 0이 아닐 때까지 임의의 병원을 찾아서 조회
        inst_code = []
        while list_cnt == '0':
            # 임의의 병원 선택
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#statistics-search-hospital")))
            driver.find_element(By.CSS_SELECTOR, "#statistics-search-hospital").click()
            time.sleep(1)
            select_hospital = temp_hospital_cnt_list.pop(temp_hospital_cnt_list.index(random.choice(temp_hospital_cnt_list)))
            hospital = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/div/ul/li["+str(select_hospital)+"]/label")
            hospital.click()
            index = (hospital.get_attribute("for")).split('-')[2]
            inst_code.append(driver.find_element(By.CSS_SELECTOR, "#hospital-index-"+str(index)+"-view").get_attribute("value"))

            # Searh 클릭
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[4]/button").click()

            # Showing entry 결과 저장
            time.sleep(4)
            temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
            temp_cnt = temp_cnt.split()
            list_cnt = temp_cnt[5]
            list_cnt = list_cnt.replace(",","")
        inst_code = "','".join(s for s in inst_code)

        # 조회 결과 저장
        result_list = []
        pat_list = []
        reporter_list = []
        result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
        pages = math.ceil(int(list_cnt) / 100)
        
        for page in range(1, pages +1):
            result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
            for i in result_list:
                pat_list.append(i.get_property("outerText").split('\t')[2])
                if i.get_property("outerText").split('\t')[1] not in reporter_list:
                    reporter_list.append(i.get_property("outerText").split('\t')[1])
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institution-interpretation-list_next > a")))
            driver.find_element(By.CSS_SELECTOR, "#institution-interpretation-list_next > a").click()
            time.sleep(2)
        
        # 조회 결과 내에서 임의의 Reporter 선택
        select_reporter = random.choice(reporter_list)

        # 새로고침
        driver.refresh()

        # Show entries 100 변경
        select = Select(driver.find_element(By.CSS_SELECTOR,"#institution-interpretation-list_length > label > select"))                
        select.select_by_value(str(100))

        # Study Date 선택
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/table/tfoot/tr[2]/th[2]").click()
        start_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").get_property("value")
        start_date = start_date.replace("-","")

        # 이전에 찾았던 병원 선택
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "#statistics-search-hospital").click()
        time.sleep(1)
        hospital = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/div/ul/li["+str(select_hospital)+"]/label")
        hospital.click()

        # Search filter에 임의의 Reporter ID 입력 후, Search 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html[1]/body[1]/section[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div/ul/li/input").send_keys(select_reporter)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div/ul/li/input").send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[4]/button").click()

        # Showing entry 결과 저장
        time.sleep(4)
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[5]
        list_cnt = list_cnt.replace(",","")

        # 조회 결과 저장
        time.sleep(4)
        result_list = []
        pat_list = []
        reporter_list = []
        result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
        pages = math.ceil(int(list_cnt) / 100)
        
        for page in range(1, pages +1):
            # result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
            for i in result_list:
                pat_list.append(i.get_property("outerText").split('\t')[2])
                reporter_list.append(i.get_property("outerText").split('\t')[1])
            driver.find_element(By.CSS_SELECTOR, "#institution-interpretation-list_next > a").click()
            time.sleep(2)

        # DB에서 선택한 병원을 동일한 조건으로 조회
        end_date = str(today.strftime('%Y%m%d'))
        sql = f"""
            select patient_id from MVIEWINSTSTAT 
            where study_dttm >= to_date('{start_date}', 'YYYY-MM-DD') and study_dttm <= to_date('{end_date}', 'YYYY-MM-DD')
            and institution_code in ('{inst_code}')
            and reporter_id = '{select_reporter}'
            """

        # DB 조회 결과 저장
        cursor.execute(sql)
        row = cursor.fetchall()
        db_pat_id = []
        for i in row:
            db_pat_id.append(i)
        
        # DB 조회 결과와 Admin 조회 결과 비교
        try:
            assert db_pat_id.sort() == pat_list.sort()
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # DB 연결 해제
        cursor.close()
        connection.close()

        # Search Filter > Reporter 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else testResult)
        if testResult == 'failed':
            testlink.reportTCResult(1782, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1782, testPlanID, buildName, 'p', "Search Filter > Reporter Passed")  

    def SearchFilter_Modality():
        print("ITR-47: Statistics > Search Filter > Modality")
        testResult = ''
        reason = list()

        # DB 접속
        os.putenv('NLS_LANG', '.UTF8')
        cx_Oracle.init_oracle_client(lib_dir=r"D:\app\user\instantclient_21_7")
        connection = cx_Oracle.connect("pantheon","pantheon","211.43.8.73:1521/spectra", encoding="UTF-8")
        cursor = connection.cursor()

        # 1 steps start! : Date를 Study Date로 선택하고, 임의의 기간을 입력한 후, Search 버튼을 클릭한다.
        # 페이지 초기화
        driver.refresh()

        # Show entries 100 변경
        select = Select(driver.find_element(By.CSS_SELECTOR,"#institution-interpretation-list_length > label > select"))                
        select.select_by_value(str(100))

        # Showing entry 결과 저장
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[5]

        # Study Date 선택
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/table/tfoot/tr[2]/th[2]").click()
        start_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").get_property("value")
        start_date = start_date.replace("-","")

        # 임의의 병원 선택
        time.sleep(1)
        temp_hospital_cnt_list = []
        hospital_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/ul/li")
        hospital_cnt = len(hospital_list) - 1

        for i in range(2, hospital_cnt):
            temp_hospital_cnt_list.append(i)
        
        # 조회 결과가 0이 아닐 때까지 임의의 병원을 찾아서 조회
        inst_code = []
        while list_cnt == '0':
            # 임의의 병원 선택
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#statistics-search-hospital")))
            driver.find_element(By.CSS_SELECTOR, "#statistics-search-hospital").click()
            time.sleep(1)
            select_hospital = temp_hospital_cnt_list.pop(temp_hospital_cnt_list.index(random.choice(temp_hospital_cnt_list)))
            hospital = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/div/ul/li["+str(select_hospital)+"]/label")
            hospital.click()
            index = (hospital.get_attribute("for")).split('-')[2]
            inst_code.append(driver.find_element(By.CSS_SELECTOR, "#hospital-index-"+str(index)+"-view").get_attribute("value"))

            # Searh 클릭
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[4]/button").click()

            # Showing entry 결과 저장
            time.sleep(4)
            temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
            temp_cnt = temp_cnt.split()
            list_cnt = temp_cnt[5]
            list_cnt = list_cnt.replace(",","")
        inst_code = "','".join(s for s in inst_code)

        # 조회 결과 저장
        result_list = []
        pat_list = []
        modality_list = []
        result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
        pages = math.ceil(int(list_cnt) / 100)
        
        for page in range(1, pages +1):
            result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
            for i in result_list:
                pat_list.append(i.get_property("outerText").split('\t')[2])
                if i.get_property("outerText").split('\t')[1] not in modality_list:
                    modality_list.append(i.get_property("outerText").split('\t')[8])
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institution-interpretation-list_next > a")))
            driver.find_element(By.CSS_SELECTOR, "#institution-interpretation-list_next > a").click()
            time.sleep(2)
        
        # 조회 결과 내에서 임의의 Modality 선택
        select_modality = random.choice(modality_list)

        # 새로고침
        driver.refresh()

        # Show entries 100 변경
        select = Select(driver.find_element(By.CSS_SELECTOR,"#institution-interpretation-list_length > label > select"))                
        select.select_by_value(str(100))

        # Study Date 선택
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/table/tfoot/tr[2]/th[2]").click()
        start_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").get_property("value")
        start_date = start_date.replace("-","")

        # 이전에 찾았던 병원 선택
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "#statistics-search-hospital").click()
        time.sleep(1)
        hospital = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/div/ul/li["+str(select_hospital)+"]/label")
        hospital.click()

        # Search filter에 임의의 Modality 입력 후, Search 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[3]/div").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[3]/div/ul/li/input").send_keys(select_modality)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[3]/div/ul/li/input").send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[4]/button").click()

        # Showing entry 결과 저장
        time.sleep(4)
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[5]
        list_cnt = list_cnt.replace(",","")

        # 조회 결과 저장
        time.sleep(4)
        result_list = []
        pat_list = []
        modality_list = []
        result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
        pages = math.ceil(int(list_cnt) / 100)
        
        for page in range(1, pages +1):
            result_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table/tbody/tr")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/table")))
            for i in result_list:
                pat_list.append(i.get_property("outerText").split('\t')[2])
                modality_list.append(i.get_property("outerText").split('\t')[1])
            driver.find_element(By.CSS_SELECTOR, "#institution-interpretation-list_next > a").click()
            time.sleep(2)

        # DB에서 선택한 병원을 동일한 조건으로 조회
        end_date = str(today.strftime('%Y%m%d'))
        sql = f"""
            select patient_id from MVIEWINSTSTAT 
            where study_dttm >= to_date('{start_date}', 'YYYY-MM-DD') and study_dttm <= to_date('{end_date}', 'YYYY-MM-DD')
            and institution_code in ('{inst_code}')
            and modality = '{select_modality}'
            """

        # DB 조회 결과 저장
        cursor.execute(sql)
        row = cursor.fetchall()
        db_pat_id = []
        for i in row:
            db_pat_id.append(i)
        
        # DB 조회 결과와 Admin 조회 결과 비교
        try:
            assert db_pat_id.sort() == pat_list.sort()
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # DB 연결 해제
        cursor.close()
        connection.close()

        # Search Filter > Modality 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1785, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1785, testPlanID, buildName, 'p', "Search Filter > Modality Passed")  

    def Columns():
        print("ITR-42: Statistics > Columns")
        testResult = ''
        reason = list()

        # 1 steps start! : Columns 버튼을 클릭한다.
        # 페이지 초기화
        driver.refresh()

        # Columns 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/button").click()

        # Columns 팝업창 팝업 확인
        popup = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[1]/h4")
        try:
            assert popup.get_property("textContent") == "Column Show/Hide"
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! : 임의의 컬럼을 체크 또는 언체크하고, Apply 버튼을 클릭한다.
        # Columns 팝업창 > 임의의 컬럼을 체크 또는 언체크
        columns = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div/ul/li")
        columns_cnt = len(columns)
        column_index = []
        
        for i in range(1, columns_cnt+1):
            column_index.append(i)

        for i in range(0,3):
            select_column = column_index.pop(column_index.index(random.choice(column_index)))
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div/ul/li["+str(select_column)+"]/label").click()
            time.sleep(1)

        # 선택한 column list 저장
        checked_column_list = []
        unchecked_column_list = []
        
        for i in range(1, columns_cnt+1):
            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div/ul/li["+str(i)+"]/input").get_property("checked") == True:
                checked_column_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div/ul/li["+str(i)+"]").get_property("textContent"))

        # Columns 팝업창 > Apply 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[3]/button[3]").click()

        # Statistics > column list 저장
        time.sleep(2)
        static_column_list = []
        static_column = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[1]/div/table/thead/tr/th")
        for i in static_column:
            static_column_list.append(i.get_property("textContent"))

        # Columns 팝업창의 column list와 Statistics column list와 비교
        try:
            assert checked_column_list.sort() == static_column_list.sort()
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # 3 steps start! : 임의의 컬럼을 체크 또는 언체크하고, Cancel 버튼을 클릭한다.
        # Columns 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/button").click()

        # Columns 팝업창 > 임의의 컬럼을 체크 또는 언체크
        for i in range(0,3):
            select_column = column_index.pop(column_index.index(random.choice(column_index)))
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div/ul/li["+str(select_column)+"]/label").click()
            time.sleep(1)

        # 선택한 column list 저장
        checked_column_list = []
        unchecked_column_list = []
        
        for i in range(1, columns_cnt+1):
            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div/ul/li["+str(i)+"]/input").get_property("checked") == True:
                checked_column_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div/ul/li["+str(i)+"]").get_property("textContent"))

        # Columns 팝업창 > Cancel 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[3]/button[2]").click()

        # Statistics > column list 저장
        time.sleep(2)
        static_column_list = []
        static_column = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[1]/div/table/thead/tr/th")
        for i in static_column:
            static_column_list.append(i.get_property("textContent"))

        # Columns 팝업창의 column list와 Statistics column list와 비교
        try:
            assert checked_column_list.sort() == static_column_list.sort()
        except:
            testResult = "failed"
            reason.append("3 steps failed\n")

        # 4 steps start! : 임의의 컬럼을 체크 또는 언체크하고, Reset 버튼을 클릭한다.
        # Columns 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/button").click()

        # Columns 팝업창 > Reset 버튼 클릭 후, Apply 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[3]/button[1]").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[3]/button[3]").click()

        # 선택한 column list 저장
        checked_column_list = []
        unchecked_column_list = []
        
        for i in range(1, columns_cnt+1):
            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div/ul/li["+str(i)+"]/input").get_property("checked") == True:
                checked_column_list.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[4]/div/div/div[2]/div/ul/li["+str(i)+"]").get_property("textContent"))

        # Statistics > column list 저장
        time.sleep(2)
        static_column_list = []
        static_column = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[3]/div[1]/div/table/thead/tr/th")
        for i in static_column:
            static_column_list.append(i.get_property("textContent"))

        # Columns 팝업창의 column list와 Statistics column list와 비교
        try:
            assert checked_column_list.sort() == static_column_list.sort()
        except:
            testResult = "failed"
            reason.append("4 steps failed\n")
        
        # Columns 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else testResult)
        if testResult == 'failed':
            testlink.reportTCResult(1759, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1759, testPlanID, buildName, 'p', "Columns Passed")  

    def Show_Entries():
        print("ITR-43: Statistics > Show entries")
        testResult = ''
        reason = list()

        # 1 steps start! : Show entries의 개수를 10으로 변경한다.
        # 페이지 초기화
        driver.refresh()

        # Showing entry 결과 저장
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[5]

        # Study Date 선택
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/table/tfoot/tr[2]/th[2]").click()
        start_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/input").get_property("value")
        start_date = start_date.replace("-","")

        # 임의의 병원 선택
        time.sleep(1)
        temp_hospital_cnt_list = []
        hospital_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/ul/li")
        hospital_cnt = len(hospital_list) - 1

        for i in range(2, hospital_cnt):
            temp_hospital_cnt_list.append(i)
        
        # 조회 결과가 100개를 초과할 때까지 임의의 병원을 찾아서 조회
        while int(list_cnt) < 100:
            # 임의의 병원 선택
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#statistics-search-hospital")))
            driver.find_element(By.CSS_SELECTOR, "#statistics-search-hospital").click()
            time.sleep(1)
            select_hospital = temp_hospital_cnt_list.pop(temp_hospital_cnt_list.index(random.choice(temp_hospital_cnt_list)))
            hospital = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/div/ul/li["+str(select_hospital)+"]/label")
            hospital.click()

            # Searh 클릭
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div[4]/button").click()

            # Showing entry 결과 저장
            time.sleep(4)
            temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
            temp_cnt = temp_cnt.split()
            list_cnt = temp_cnt[5]

        # Show entries 10으로 변경
        select = Select(driver.find_element(By.CSS_SELECTOR,"#institution-interpretation-list_length > label > select"))                
        select.select_by_value(str(10))

        # Showing entry 결과 저장
        time.sleep(4)
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[3] 

        # 조회결과 리스트가 10개 단위로 표시되는지 확인
        try:
            assert list_cnt == '10'
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! : Show entries의 개수를 25로 변경한다.
        # Show entries 25로 변경
        select = Select(driver.find_element(By.CSS_SELECTOR,"#institution-interpretation-list_length > label > select"))                
        select.select_by_value(str(25))

        # Showing entry 결과 저장
        time.sleep(4)
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[3] 

        # 조회결과 리스트가 25개 단위로 표시되는지 확인
        try:
            assert list_cnt == '25'
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")

        # 3 steps start! : Show entries의 개수를 50으로 변경한다.
        # Show entries 50으로 변경
        select = Select(driver.find_element(By.CSS_SELECTOR,"#institution-interpretation-list_length > label > select"))                
        select.select_by_value(str(50))

        # Showing entry 결과 저장
        time.sleep(4)
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[3] 

        # 조회결과 리스트가 50개 단위로 표시되는지 확인
        try:
            assert list_cnt == '50'
        except:
            testResult = "failed"
            reason.append("3 steps failed\n")

        # 4 steps start! : Show entries의 개수를 100으로 변경한다.
        # Show entries 100으로 변경
        select = Select(driver.find_element(By.CSS_SELECTOR,"#institution-interpretation-list_length > label > select"))                
        select.select_by_value(str(100))

        # Showing entry 결과 저장
        time.sleep(4)
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div[4]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[3] 

        # 조회결과 리스트가 100개 단위로 표시되는지 확인
        try:
            assert list_cnt == '100'
        except:
            testResult = "failed"
            reason.append("4 steps failed\n")

        # Show entries 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else testResult)
        if testResult == 'failed':
            testlink.reportTCResult(1765, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1765, testPlanID, buildName, 'p', "Show entries Passed")  
