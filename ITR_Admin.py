from asyncio.windows_events import NULL
from operator import rshift
import re
from types import NoneType
from weakref import ref
from h11 import Data
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
# import ITR_Admin_Common

# User: kyle
URL = 'http://testserver-win:81/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
DevKey = 'adcb86843d0c77e6e0c9950f80a143c0'
# testlink 초기화
tl_helper = TestLinkHelper()
testlink = tl_helper.connect(TestlinkAPIClient) 
testlink.__init__(URL, DevKey)
testlink.checkDevKey()

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

class signInOut:
    def admin_sign_in():
        driver.find_element(By.ID, 'user-id').clear()
        driver.find_element(By.ID, 'user-id').send_keys('testAdmin')
        driver.find_element(By.ID, 'user-password').send_keys('Server123!@#')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)
    def admin_sign_out():
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
        
        print("ITR-1: Sign In/Out")
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
        
        print("ITR-2: Remember Me")
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

        print("ITR-3: Search Schedule List")
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
        
        signInOut.admin_sign_in()

        # # Hospital list 저장
        # hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        # request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        # body = request.response.body.decode('utf-8')
        # data = json.loads(body)
        # hospital_cnt = len(data)

        # # 각 hospital의 refer, requested, emergency job의 건수 비교
        # if hospital_cnt > 0:
        #     n = 0

        #     for i in data:
        #         priority_cnt = i['PriorityCount']
        #         job_cnt = i['JobCount']
        #         refer_cnt = i['ReferCount']
        #         refer_priority_cnt = 0
        #         time.sleep(2)
        #         del driver.requests
        #         hospital_list[n].click()

        #         # 선택한 병원의 Job list 결과 저장 
        #         request = driver.wait_for_request('.*/GetAllAssignedList.*')
        #         body = request.response.body.decode('utf-8')
        #         data = json.loads(body)["data"]
                
        #         # Showing entry 결과 저장
        #         temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
        #         temp_cnt = temp_cnt.split()
        #         list_cnt = temp_cnt[5]
        #         refer_reporter_list = []
        #         emer_reporter_list = []
                
        #         # Show 100 entries 설정
        #         select = Select(driver.find_element(By.CSS_SELECTOR,"#refer-assigned-list_length > label > select"))
        #         select.select_by_value("100")
        #         pages = math.ceil(int(list_cnt) / 100)
                
        #         # All Assigned List 탭에서 Refer count를 조회 결과에서 계산 
        #         while pages > 0: 
        #             for i in data:
        #                 # All Assigned List 탭에서 Refer 건수 계산
        #                 refer_text = (i["REFERRED_USER_KEYS"])
        #                 temp_refer_text_list = (refer_text.split(','))                        
        #                 for j in temp_refer_text_list:                            
        #                     refer_reporter_list.append(j)
                    
        #                 # All Assigned List 탭에서 Emergency Job 건수 계산
        #                 if i["JobPriority"] == 'E':
        #                     emer_reporter_key = (i["REFERRED_USER_KEYS"])
        #                     temp_emer_reporter_list = (emer_reporter_key.split(','))
        #                     for j in temp_emer_reporter_list:
        #                         emer_reporter_list.append(j)
        #                     emer_reporter_list_cnt = len(emer_reporter_list)
                            
        #             pages = pages - 1
        #             del driver.requests
                    
        #             # 새로운 페이지 조회 결과 저장
        #             if pages > 0:
        #                 driver.find_element(By.CSS_SELECTOR,"#refer-assigned-list_next > a").click()
        #                 request = driver.wait_for_request('.*/GetAllAssignedList.*')
        #                 body = request.response.body.decode('utf-8')
        #                 data = json.loads(body)["data"]
        #             refer_text_list_cnt = len(refer_reporter_list)
                    
        #         try:
        #             assert refer_cnt == refer_text_list_cnt
        #         except:
        #             testResult = 'failed'
        #             reason.append("Step1 - Refer count isn't valid")

        #         # 요청 결과 삭제
        #         del driver.requests
                
        #         # All Assigned List의 Showing entries 값 저장
        #         temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
        #         temp_cnt = temp_cnt.split()
        #         list_cnt = temp_cnt[5]
        #         assigned_list_result = int(list_cnt)

        #         # Not Assigned List 탭 클릭
        #         element = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]/a")
        #         driver.execute_script("arguments[0].click()",element)
                
        #         # 선택한 병원의 Not Assigned List 결과 저장
        #         request = driver.wait_for_request('.*/GetNotAssignedList.*')
        #         body = request.response.body.decode('utf-8')
        #         data = json.loads(body)["data"]

        #         # Not Assigned List의 Showing entries 값 저장
        #         temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
        #         temp_cnt = temp_cnt.split()
        #         list_cnt = temp_cnt[5]
        #         not_refer_text_list = int(list_cnt)
        #         pages = math.ceil(int(list_cnt) / 100)

        #         # Emergency Job 건수 계산
        #         while pages > 0: 
        #             for i in data:
        #                 if i["JobPriority"] == 'E':
        #                     emer_reporter_list_cnt = emer_reporter_list_cnt + 1
                            
        #             pages = pages - 1   
        #             del driver.requests
        #             if pages > 0:
        #                 # 새로운 페이지의 결과 저장
        #                 driver.find_element(By.CSS_SELECTOR,"#refer-assigned-list_next > a").click()
        #                 request = driver.wait_for_request('.*/GetNotAssignedList.*')
        #                 body = request.response.body.decode('utf-8')
        #                 data = json.loads(body)["data"]
        #                 time.sleep(1)

        #         try:
        #             assert (int(priority_cnt), int(job_cnt)) == (int(emer_reporter_list_cnt), int(assigned_list_result) + int(not_refer_text_list))
        #         except:
        #                 testResult = 'failed'
        #                 reason.append("Step 1 - Emergency & Auto Refer count isn't valid")

        #         # All Assigned List 탭 클릭
        #         driver.find_element(By.XPATH,"/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]/a").click()
        #         n = n + 1

        # # Refer 화면 새로고침
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # # Hospital list 저장
        # hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        # request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        # body = request.response.body.decode('utf-8')
        # data = json.loads(body)
        # hospital_cnt = len(data)
        
        # if hospital_cnt > 0:
        #     n = 0

        #     for i in data:
        #         # Institution name 저장
        #         inst_name = i['InstitutionName']
        #         time.sleep(0.5)
        #         del driver.requests
                
        #         # Hospital list 다시 저장
        #         hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        #         hospital_list[n].click()
                
        #         # Hospital list의 Reporter list 저장
        #         request = driver.wait_for_request('.*/GetReporterListByInstitution.*')
        #         body = request.response.body.decode('utf-8')
        #         data = json.loads(body)
        #         reporter_list = []
                
        #         # Reporter Key 저장                
        #         for i in data:
        #             reporter_list.append(i['ReporterKey'])

        #         # Configuration > Download control로 이동
        #         driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[5]/a").click()
        #         driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/button[3]").click()

        #         # 선택한 병원의 institution code 입력 후, 검색
        #         driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[2]/div").click()
        #         driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > div > input[type=text]").send_keys(inst_name)
        #         driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[2]/div/div/div/input").send_keys(Keys.RETURN)
        #         driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[5]/button").click()
        #         time.sleep(0.5)
        #         del driver.requests
                
        #         # Showing entries 100으로 변경
        #         select = Select(driver.find_element(By.CSS_SELECTOR,"#download-list_length > label > select"))                
        #         select.select_by_value("100")

        #         # Download control의 Reporter list 저장
        #         request = driver.wait_for_request('.*/GetDownloadControlList.*')
        #         body = request.response.body.decode('utf-8')
        #         data = json.loads(body)["data"]
        #         dc_reporter_list = []

        #         # 선택한 Institution의 Reporter key 저장
        #         for i in data:
        #             dc_reporter_list.append(i['UserKey'])

        #         # Hospital list에서의 reporter가 download control에서 해당 institution의 reporter인지 확인
        #         for i in reporter_list:
        #                 if int(i) not in dc_reporter_list:
        #                     result = "false"
        #                 else:
        #                     result = "true"

        #         try:
        #             assert result == "true"
        #         except:
        #             testResult = 'failed'
        #             reason.append("Step 2 - Reporter list isn't valid")
                
        #         # Refer 탭 클릭
        #         driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
        #         n = n + 1
        
        # Hospital list 저장
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        hospital_cnt = len(data)

        if hospital_cnt > 0:
            n = 0

            hospital_list[n].click()
            # reporter_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-sub-item")
            # reporter_list_cnt = len(reporter_list)
            # while reporter_list_cnt > 0:
                # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div[2]/div[1]/div/div[1]").click()
            temp = driver.find_elements(By.CLASS_NAME, "list-report-id")            
            temp_cnt = len(temp)
            m = 0
            while m < temp_cnt:
                sub_modal_list = []
                temp = driver.find_elements(By.CLASS_NAME, "list-report-id")
                # temp_reporter = temp[m].get_property("textContent").split('/')[0]
                
                # 병원 탭 > 선택한 Reporter key 저장
                time.sleep(2)
                temp_reporter_key = driver.find_elements(By.CLASS_NAME, "list-group-item.list-sub-item")
                reporter_key = (temp_reporter_key[m].get_property("dataset"))["reporterKey"]
                
                # 병원 탭 > Reporter 클릭
                time.sleep(2)
                temp[m].click()
                
                # 병원 탭 > 선택한 Reporter의 modality 저장
                modality_list = driver.find_elements(By.CLASS_NAME, "list-modality-info")
                for i in modality_list:
                    sub_modal_list.append(i.get_property("outerText").split('\n')[0])
                
                # # 병원 탭 > Modality list 중복 제거
                # for i in temp_sub_modal_list:
                #     if i not in sub_modal_list:
                #         sub_modal_list.append(i)
                
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
                    reason.append("Step 3 - Modality list isn't valid")




                # 판독의 리스트 저장
                # request = driver.wait_for_request('.*/GetReferCountsByReporter.*')
                # body = request.response.body.decode('utf-8')
                # data = json.loads(body)
                # # temp_reporter_key_list = []

                # for i in data:
                #     temp_reporter_key_list.append(i["ReporterKey"])
                

                # reporter_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[4]/div[2]/div/div")
                # for i in reporter_list:
                #     if i.get_property("textContent").split('/')[0] == temp_reporter:
                #         print(i.get_property("textContext").split('/')[0])
                #         i.click()




                # 병원탭 클릭
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/li[1]/a").click()
                m = m + 1
                # hospital_list[n].click()
                  
            n = n + 1
            # reporter_list_cnt = reporter_list_cnt - 1
                





       







        print("ITR-7: Hospital List")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # # Hospital_List 결과 전송
        # result = ' '.join(s for s in reason)
        # if testResult == 'failed':
        #     testlink.reportTCResult(1567, testPlanID, buildName, 'f', result)            
        # else:
        #     testlink.reportTCResult(1567, testPlanID, buildName, 'p', "Hospital_List Test Passed")  

    def Reporter_List():
        testResult = ''
        reason = list()        

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
                        reason.append("refer_cnt isn't valid")
                
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
                        reason.append("proirity_cnt isn't valid")

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
                        reason.append("schedule_cnt isn't valid")
                        
                n = n + 1
                driver.find_element(By.CSS_SELECTOR, "#refer_search_priority_chosen span").click()
                driver.find_element(By.CSS_SELECTOR, ".active-result:nth-child(1)").click()                
        
        print("ITR-8: Reporter List")
        print("Test Result: Pass" if testResult != "failed" else testResult)

        # # Reporter_List 결과 전송
        # result = ' '.join(s for s in reason)
        # if testResult == 'failed':
        #     testlink.reportTCResult(1577, testPlanID, buildName, 'f', result)
        # else:
        #     testlink.reportTCResult(1577, testPlanID, buildName, 'p', "Reporter List Passed")












# Sign.Sign_InOut()
# Sign.Rememeber_Me()
# Topbar.Search_Schedule_List()
Refer.Hospital_List()
# Refer.Reporter_List()