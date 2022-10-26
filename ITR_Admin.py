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
        time.sleep(3)

        # Hospital list를 저장한다.
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        hospital_cnt = len(data)

        # 각 hospital의 refer, requested, emergency job의 건수를 비교한다.
        if hospital_cnt > 0:
            n = 0
            refer_priority_cnt = 0

            for i in data:
                priority_cnt = i['PriorityCount']
                job_cnt = i['JobCount']
                refer_cnt = i['ReferCount']
                del driver.requests
                hospital_list[n].click()

                # Tap panel의 refer count와 조회 결과 리스트에서의 refer count를 비교한다.  
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[3]/div/div/ul/li[2]/a")))
                sub_request = driver.wait_for_request('.*/GetAllAssignedList.*')
                sub_body = sub_request.response.body.decode('utf-8')
                assigned_data = json.loads(sub_body)["data"]
                refer_text_list = []
                
                # 각 Reporter의 Refer count를 계산하여 비교한다.
                for i in assigned_data:
                   refer_text = (i["REFERRED_USER_KEYS"])
                   temp_refer_text_list = (refer_text.split(','))
                   for j in temp_refer_text_list:
                        if j not in refer_text_list:
                            refer_text_list.append(j)
                   print(refer_text_list)
                    
                    # All Assigned List 탭에서 Emergency Job의 건수를 계산한다.
                   if i["JobPriority"] == 'E':
                    refer_priority_cnt = refer_priority_cnt + 1
                    print(refer_priority_cnt)               
                refer_text_list_cnt = len(refer_text_list)
                print(refer_text_list_cnt)

                try:
                    assert refer_cnt == refer_text_list_cnt
                    print('pass')
                except:
                    testResult = 'failed'
                    reason.append("Step1 - Refer count isn't valid")

                # Not Assigned List 탭에서 Emergency Job의 건수를 계산한다.
                del driver.requests
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]/a").click()
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[3]/div/div/ul/li[2]/a")))
                
                request = driver.wait_for_request('.*/GetNotAssignedList.*')
                body = request.response.body.decode('utf-8')
                notAssigned_data = json.loads(body)["data"]

                for i in notAssigned_data:
                    if i["JobPriority"] == 'E':
                        refer_priority_cnt = refer_priority_cnt + 1
                print(len(notAssigned_data))
                autorefer_text_list_cnt = len(notAssigned_data)
                print(autorefer_text_list_cnt)

            try:
                assert (int(priority_cnt), int(job_cnt)) == (int(refer_priority_cnt), int(refer_text_list_cnt) + int(autorefer_text_list_cnt))
            except:
                    testResult = 'failed'
                    reason.append("Step 1 - Emergency & Auto Refer count isn't valid")








                # Tap panel의 refer count와 조회 결과 리스트에서의 refer count를 비교한다.            
                # WebDriverWait(driver, 3).until(EC.element_to_be_clickable(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[3]/div/div/ul/li[2]/a"))
                # element = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]/a")
                
                # driver.execute_script("arguments[0].click()",element)
                # time.sleep(3)
                # temp_cnt = driver.find_element(By.XPATH,'/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]').text
                # temp_cnt = temp_cnt.split()
                # list_cnt = temp_cnt[5]
                # try:
                #     assert int(refer_cnt) == int(list_cnt)
                # except:
                #     testResult = 'failed'
                #     reason.append("Hospital_List step 1 isn't valid")
                
                # Tap panel의 requested job count와 조회 결과 리스트에서의 requested job count를 비교한다.  


                # driver.find_element(By.LINK_TEXT, 'library_booksAll List').click()
                # time.sleep(3)
                # temp_cnt = driver.find_element(By.XPATH,'/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]').text
                # temp_cnt = temp_cnt.split()
                # list_cnt = temp_cnt[5]
                # try:
                #     assert int(job_cnt) == int(list_cnt)
                # except:
                #     testResult = 'failed'
                #     reason.append("Hospital_List step 1 isn't valid")
                
                # # Tap panel의 emergency job count와 조회 결과 리스트에서의 emergency job count를 비교한다.  
                # driver.find_element(By.CSS_SELECTOR, "#refer_search_priority_chosen span").click()
                # driver.find_element(By.CSS_SELECTOR, ".active-result:nth-child(2)").click()
                # driver.find_element(By.XPATH,'/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]').click()
                # driver.find_element(By.XPATH, '/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]').click()
                # time.sleep(3)
                # temp_cnt = driver.find_element(By.XPATH,'/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]').text
                # temp_cnt = temp_cnt.split()
                # list_cnt = temp_cnt[5]
                # try:
                #     assert int(proirity_cnt) == int(list_cnt)
                #     print("pass")
                # except:
                #     testResult = 'failed'
                #     print("fail")
                #     reason.append("Hospital_List step 1 isn't valid")
                # n = n + 1
                # driver.find_element(By.CSS_SELECTOR, "#refer_search_priority_chosen span").click()
                # driver.find_element(By.CSS_SELECTOR, ".active-result:nth-child(1)").click()

        # 각 hospital의 refer 받은 reporter list를 확인한다.
        # if hospital_cnt > 0:
        #     n = 0
        #     while hospital_cnt >= n:
        #         del driver.requests
        #         hospital_list[n].click()

        #         # Reporter list를 저장한다.
        #         request = driver.wait_for_request('.*/GetReporterListByInstitution.*')
        #         body = request.response.body.decode('utf-8')
        #         data = json.loads(body)
        #         reporter_list = list()

        #         # Reporter list의 Reporter key를 가져온다.
        #         for i in data:
        #             reporter_list.append(i["ReporterKey"])
        #         print("ReporterList:", reporter_list)
        #         # Reporter를 클릭했을 때, 조회 결과의 Reporter list를 저장한다.
        #         del driver.requests
        #         hospital_list[n].click()
        #         request_2 = driver.wait_for_request('.*/GetAllAssignedList.*')
        #         body_2 = request_2.response.body.decode('utf-8')
        #         data_2 = json.loads(body_2)["data"]
        #         refer_text = list()
        #         reporter_key_list = list()

        #         for i in data_2:
        #             refer_text.append(i["REFERRED_USER_KEYS"])
        #         print("refer_text:", refer_text)
        #         # # user_key = driver.find_element(By.CLASS_NAME, "check-refer-job.filled-in.chk-col-purple.refer-list-column-context.refer-list-column-center").get_attribute("data-referred-user-keys")
        #         user_keys = driver.find_elements(By.CLASS_NAME, "check-refer-job.filled-in.chk-col-purple.refer-list-column-context.refer-list-column-center")
        #         # job_cnt = len(user_keys)
        #         # for i in user_keys:                
        #         #     refer_text.append(i.get_attribute("data-referred-user-keys"))
        #         temp_reporter_key = set(refer_text)
        #         print(temp_reporter_key)
        #         temp_reporter_key = ' '.join(s for s in temp_reporter_key)
        #         print(temp_reporter_key)
        #         if len(list(temp_reporter_key)) > 1:
        #             for i in temp_reporter_key:
        #                 if i in ",":
        #                     reporter_key_list.append(i.split(','))
        #                 else:
        #                     reporter_key_list.append(i)
        #         print(reporter_key_list)
        #         try:
        #             assert reporter_list == list(reporter_key_list)
        #         except:
        #             testResult = 'failed'
        #             reason.append("Hospital_List step 1 isn't valid")
        #         n = n + 1





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
        
        #Reporter_List 결과 전송
        result = ' '.join(s for s in reason)
        if testResult == 'failed':
            testlink.reportTCResult(1577, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1577, testPlanID, buildName, 'p', "Reporter List Passed")            


# Sign.Sign_InOut()
# Sign.Rememeber_Me()
# Topbar.Search_Schedule_List()
Refer.Hospital_List()
# Refer.Reporter_List()