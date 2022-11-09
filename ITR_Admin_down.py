# -*- coding: utf-8 -*-

import re
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
#URL = 'http://testserver-win:81/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
#DevKey = 'adcb86843d0c77e6e0c9950f80a143c0'
## testlink 초기화
#tl_helper = TestLinkHelper()
#testlink = tl_helper.connect(TestlinkAPIClient) 
#testlink.__init__(URL, DevKey)
#testlink.checkDevKey()

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
                autorefer_text_list = []

                for i in notAssigned_data:
                    # autorefer_text = i["REFERRED_USER_KEYS"]
                    # temp_autorefer_text_list = autorefer_text.split(',')
                    # for j in temp_autorefer_text_list:
                    #     if j not in autorefer_text_list:
                    #         autorefer_text_list.append(j)
                    if i["JobPriority"] == 'E':
                        refer_priority_cnt = refer_priority_cnt + 1
                print(len(notAssigned_data))
                autorefer_text_list_cnt = len(notAssigned_data)
                print(autorefer_text_list_cnt)

            try:
                assert (int(priority_cnt), int(job_cnt)) == (int(refer_priority_cnt), int(refer_text_list_cnt) + int(autorefer_text_list_cnt))
            except:
                    testResult = 'failed'
                    reason.append("Hospital_List step 1 isn't valid")








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
# Refer.Hospital_List()
# Refer.Reporter_List()























###########################################################
# save as witt signature UTF-8
from datetime import datetime
import math, random
WorklistUrl = 'http://vm-onpacs'

admin_id = "testAdmin"
admin_pw = "Server123!@#"
subadmin_id = "testSubadmin"
subadmin_pw = "Server123!@#"
wk_id = "testInfReporter"
wk_pw = "Server123!@#"
wk_id_2 = "ITRTestUser" #DownloadControl_User_Add / DownloadControl_User_Modify
wk_pw_2 = "1234qwer!@"#DownloadControl_User_Add
search_id = "testInfReporter" #DirectMessageBox_Search / DirectMessageSetting_Search
search_username = "TestINFReporter" #DirectMessageBox_Search / DirectMessageSetting_Search
search_text = "test" #DirectMessageBox_Search
search_institution = "INFINITT" #NewDirectMessage_Institution
search_institution_2 = "Cloud" #MultiReadingCenterRule / Institution_SearchFilter
search_institution_3 = "Cloud Team" #Institution_Modify / DownloadControl_User_Add
search_institution_code = "997" #Institution_SearchFilter / Institution_Add
search_center = "인피니트" #NewDirectMessage_Center_Search / MultiReadingCenterRule / Institution_Add
search_center_2 = "인피니트테스트" #MultiReadingCenterRule
search_reporter = "TestINFReporter" #NewDirectMessage_Center_Reporter
unauth_search_id = "TEST_MAP" #DirectMessageSetting_Search
unauth_search_username = "김태호" #DirectMessageSetting_Search
add_test_id = "TestA" #+난수 # DirectMessageSetting_Authorize
add_test_pw = "1234qwer!" #DirectMessageSetting_Authorize
upload_pic = "C:\\Users\\INFINITT\\Desktop\\uploadtest.png" # NoticeList_NoticeEditBoard
upload_pic_url = "https://i.ytimg.com/vi/gREpAVOERis/maxresdefault.jpg" # NoticeList_NoticeEditBoards
specialty = "ITRTest" #DownloadControl_Add

def admin_login():
    driver.find_element(By.ID, 'user-id').clear()
    driver.find_element(By.ID, 'user-id').send_keys(admin_id)
    driver.find_element(By.ID, 'user-password').send_keys(admin_pw)
    driver.find_element(By.CSS_SELECTOR, '.btn').click()
    driver.implicitly_wait(5)

def subadmin_login():
    driver.find_element(By.ID, 'user-id').clear()
    driver.find_element(By.ID, 'user-id').send_keys(subadmin_id)
    driver.find_element(By.ID, 'user-password').send_keys(subadmin_pw)
    driver.find_element(By.CSS_SELECTOR, '.btn').click()
    driver.implicitly_wait(5)

def wk_login(work_id, work_pw):
    driver.find_element(By.ID, 'user-id').clear()
    driver.find_element(By.ID, 'user-id').send_keys(work_id)
    driver.find_element(By.ID, 'user-password').clear()
    driver.find_element(By.ID, 'user-password').send_keys(work_pw)
    driver.find_element(By.CSS_SELECTOR, '.btn').click()
    driver.implicitly_wait(5)    

    driver.find_element(By.CSS_SELECTOR, '.btn').click()
    driver.implicitly_wait(5)
    # 인증서 비밀번호 입력 닫기
    try:
        WebDriverWait(driver, 1.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div[2]/button[1]")))
        driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div[2]/button[1]").click()
    except:
        print("no cert")

    # waiting loading
    try:
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
    except:
        pass

def ReFresh():
    driver.find_element(By.CSS_SELECTOR, "body > nav > div > div:nth-child(1) > a.navbar-brand").click()
    driver.implicitly_wait(5)

class DirectMessage:
    def DirectMessageBox_ViewSort(asc):
        #del driver.requests - need
        testResult = True
        if asc == True:
            ori_order = "mail"
            nxt_order = "drafts"
        else:
            ori_order = "drafts"
            nxt_order = "mail"

        request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        cmr_content = []
        cmr_content.append(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div[4]/div[2]/table/tbody/tr[1]/td[1]/span/i").text)
        time_temp = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div[4]/div[2]/table/tbody/tr[1]/td[4]").text
        cmr_content.append(datetime.strptime(time_temp, '%Y-%m-%d %H:%M'))
        num = 2
        while num < (len(data)+1):
            time_temp = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div[4]/div[2]/table/tbody/tr["+str(num)+"]/td[4]").text
            selected_time = datetime.strptime(time_temp, '%Y-%m-%d %H:%M')

            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div[4]/div[2]/table/tbody/tr["+str(num)+"]/td[1]/span/i").text == nxt_order:
                cmr_content[0] = nxt_order
                cmr_content[1] = selected_time
                num += 1
                break
            
            num += 1
            sub = str(cmr_content[1] - selected_time)
            if '-' in sub:
                testResult = False
                break
            else:
                cmr_content[1] = selected_time

        while num < (len(data)+1):
            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div[4]/div[2]/table/tbody/tr["+str(num)+"]/td[1]/span/i").text == ori_order:
                testResult = False
                break
            
            time_temp = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div[4]/div[2]/table/tbody/tr["+str(num)+"]/td[4]").text
            selected_time = datetime.strptime(time_temp, '%Y-%m-%d %H:%M')
            num += 1
            sub = str(cmr_content[1] - selected_time)
            if '-' in sub:
                testResult = False
                break
            else:
                cmr_content[1] = selected_time

        return testResult


    def DirectMessageBox_Search():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Direct Message Tab #1
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        temp = DirectMessage.DirectMessageBox_ViewSort(asc=True)
        if temp == False:
            testResult = False
            Result_msg += "#1 "

        # User ID Search #2
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_value").send_keys(search_id)
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search > i").click()
        
        request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        for current_page in range(0, total):
            for n in range (1, (len(data["data"]) + 1) ):
                if search_id not in driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div[4]/div[2]/table/tbody/tr["+str(n)+"]/td[3]").text:
                        testResult = False
                        Result_msg += "#2 "

            if current_page + 1 == total:
                break
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_value").clear()

        # User Name Search #3
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_type").click()
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_type > option:nth-child(2)").click()
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_value").send_keys(search_username)
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search > i").click()
        
        request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        for current_page in range(0, total):
            for n in range (1, (len(data["data"]) + 1) ):
                if search_username not in driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div[4]/div[2]/table/tbody/tr["+str(n)+"]/td[3]").text:
                        testResult = False
                        Result_msg += "#3 "

            if current_page + 1 == total:
                break
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_value").clear()

        # Msg Text Search #4
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_type").click()
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_type > option:nth-child(3)").click()
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_value").send_keys(search_text)
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search > i").click()
        
        request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        for current_page in range(0, total):
            for n in range (1, (len(data["data"]) + 1) ):
                if search_text not in driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div[4]/div[2]/table/tbody/tr["+str(n)+"]/td[2]").text:
                        testResult = False
                        Result_msg += "#4 "

            if current_page + 1 == total:
                break

        print("DirectMessageBox_Search")
        print(testResult)
        print(Result_msg)

        # DirectMessageBox_Search결과 전송 ##
        if testResult == False:
            testlink.reportTCResult(2232, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2232, testPlanID, buildName, 'p', "DirectMessageBox_Search Test Passed")

    def DirectMessageBox_ShowEntries_fun(entries, num):
        Result_msg = ""

        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#message_list_group_length > label > select").click()
        driver.find_element(By.CSS_SELECTOR, "#message_list_group_length > label > select > option:nth-child("+str(num)+")").click()
        request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        if data["Length"] != entries:
            Result_msg += "#"+str(num)+" "
        if data["recordsFiltered"] > entries:
            try:
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#message_list_group_next > a")))
            except:
                Result_msg += "#"+str(num)+" "

        return Result_msg

    def DirectMessageBox_ShowEntries():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # 5 #1
        temp = DirectMessage.DirectMessageBox_ShowEntries_fun(5, 1)
        if temp != "":
            testResult = False
            Result_msg += temp

        # 10 #2
        temp = DirectMessage.DirectMessageBox_ShowEntries_fun(10, 2)
        if temp != "":
            testResult = False
            Result_msg += temp

        # 20 #3
        temp = DirectMessage.DirectMessageBox_ShowEntries_fun(20, 3)
        if temp != "":
            testResult = False
            Result_msg += temp

        # 50 #4
        temp = DirectMessage.DirectMessageBox_ShowEntries_fun(50, 4)
        if temp != "":
            testResult = False
            Result_msg += temp

        # 100 #5
        temp = DirectMessage.DirectMessageBox_ShowEntries_fun(100, 5)
        if temp != "":
            testResult = False
            Result_msg += temp

        print("DirectMessageBox_ShowEntries")
        print(testResult)
        print(Result_msg)

        # DirectMessageBox_ShowEntries결과 전송 ##
        if testResult == False:
            testlink.reportTCResult(2238, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2238, testPlanID, buildName, 'p', "DirectMessageBox_ShowEntries Test Passed")

    def DirectMessageBox_WNSort(length, asc):
        testResult = True
        sender = []

        for n in range (1, length+1):
            sender.append(driver.find_element(By.CSS_SELECTOR, "#message_list_group > tbody > tr:nth-child("+str(n)+") > td:nth-child(3)").text)
        sorted_sender = sender
        if asc == True:
            sorted_sender.sort()
        else:
            sorted_sender.sort(reverse=True)

        if sender != sorted_sender:
            testResult = False

        return testResult

    def DirectMessageBox_STSort(length, asc):
        testResult = True

        time_temp = driver.find_element(By.CSS_SELECTOR, "#message_list_group > tbody > tr:nth-child(1) > td:nth-child(4)").text
        cmr_time = datetime.strptime(time_temp, '%Y-%m-%d %H:%M')
        for n in range(2, length + 1):
            time_temp = driver.find_element(By.CSS_SELECTOR, "#message_list_group > tbody > tr:nth-child("+str(n)+") > td:nth-child(4)").text
            selected_time = datetime.strptime(time_temp, '%Y-%m-%d %H:%M')

            sub = str(cmr_time - selected_time)
            #true일떄 - 찍히거나 0:00:00
            #false일떄 - 안찍히고 0:00:00
            if asc == False:
                if '-' in sub:
                    testResult = False
                    break
            else:
                if sub != "0:00:00":
                    if '-' not in sub:
                        testResult = False
                        break
            cmr_time = selected_time

    def DirectMessageBox_Sorting():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # R #1
        for n in range(0,2):
            del driver.requests
            driver.find_element(By.CSS_SELECTOR, "#message_list_group_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(1)").click()
            request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)

            if data["OrderColumn"] == "view":
                if data["OrderType"] == "asc":
                    temp = DirectMessage.DirectMessageBox_ViewSort(asc=True)
                    if temp == False:
                        testResult = False
                        Result_msg += "#1 "
                elif data["OrderType"] == "desc":
                    temp = DirectMessage.DirectMessageBox_ViewSort(asc=False)
                    if temp == False:
                        testResult = False
                        Result_msg += "#1 "
            else:
                testResult = False
                Result_msg += "#1 "

        # Sender #2
        for n in range(0,2):
            del driver.requests
            driver.find_element(By.CSS_SELECTOR, "#message_list_group_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(3)").click()
            request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)

            if data["OrderColumn"] == "WRITER_NAME":
                if data["OrderType"] == "asc":
                    temp = DirectMessage.DirectMessageBox_WNSort(len(data["data"]),asc=True)
                    if temp == False:
                        testResult = False
                        Result_msg += "#2 "
                elif data["OrderType"] == "desc":
                    temp = DirectMessage.DirectMessageBox_WNSort(len(data["data"]),asc=False)
                    if temp == False:
                        testResult = False
                        Result_msg += "#2 "
            else:
                testResult = False
                Result_msg += "#2 "

        # SendTime #3
        for n in range(0,2):
            del driver.requests
            driver.find_element(By.CSS_SELECTOR, "#message_list_group_wrapper > div.dataTables_scroll > div.dataTables_scrollHead > div > table > thead > tr > th:nth-child(4)").click()
            request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)

            if data["OrderColumn"] == "WRITE_DTTM":
                if data["OrderType"] == "asc":
                    temp = DirectMessage.DirectMessageBox_STSort(len(data["data"]),asc=True)
                    if temp == False:
                        testResult = False
                        Result_msg += "#3 "
                elif data["OrderType"] == "desc":
                    temp = DirectMessage.DirectMessageBox_STSort(len(data["data"]),asc=False)
                    if temp == False:
                        testResult = False
                        Result_msg += "#3 "
            else:
                testResult = False
                Result_msg += "#3 "

        print("DirectMessageBox_Sorting")
        print(testResult)
        print(Result_msg)

        # DirectMessageBox_Sorting결과 전송 ##
        if testResult == False:
            testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2245, testPlanID, buildName, 'p', "DirectMessageBox_Sorting Test Passed")
   
    def DirectMessageBox_Badge():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # DirectMessageBox
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # Message Box Count #1
        request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        unread_count = 0
        for a in range(1, total+1):
            for b in range(1, len(data["data"])+1):
                if driver.find_element(By.CSS_SELECTOR, "#message_list_group > tbody > tr:nth-child("+str(b)+") > td:nth-child(1)").get_property("textContent") == "mail":
                    unread_count += 1
                else:
                    break
            if driver.find_element(By.CSS_SELECTOR, "#message_list_group > tbody > tr:nth-child("+str(len(data["data"]))+") > td:nth-child(1)").get_property("textContent") == "drafts" or a == total:
                break
            driver.find_element(By.CSS_SELECTOR, "#message_list_group_next > a").click()

        try:
            assert(unread_count != driver.find_element(By.CSS_SELECTOR, "#direct_message_total_count").text and
                   unread_count != driver.find_element(By.CSS_SELECTOR, "#unread_dm_cnt").text)
        except:
            testResult = False
            Result_msg += "#1 "
            
        print("DirectMessageBox_Badge")
        print(testResult)
        print(Result_msg)

        # DirectMessageBox_Badge결과 전송 ##
        if testResult == False:
            testlink.reportTCResult(2250, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2250, testPlanID, buildName, 'p', "DirectMessageBox_Badge Test Passed")

    def DirectMessageBox_Message():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # Read
        request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        target = []
        target.append(data[len(data)-1]["WRITER_NAME"])
        target.append(str(datetime.strptime(data[len(data)-1]["WRITE_DTTM"], '%Y-%m-%dT%H:%M:%S')))
        target.append(data[len(data)-1]["MESSAGE_TEXT_LOB"])
        
        driver.find_element(By.CSS_SELECTOR, "#message_list_group > tbody > tr:nth-child("+str(len(data))+") > td:nth-child(2)").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#load_message_text")))
        try:
            assert(target[0] == driver.find_element(By.CSS_SELECTOR, "#load_message_writer").get_property("value") and 
                   target[1] == driver.find_element(By.CSS_SELECTOR, "#load_message_write_dttm").get_property("value") and
                   target[2] == driver.find_element(By.CSS_SELECTOR, "#load_message_text").get_property("value"))
        except:
            testResult = False
            Result_msg += "#1 "
        
        print("DirectMessageBox_Message")
        print(testResult)
        print(Result_msg)

        # DirectMessageBox_Message결과 전송 ##
        if testResult == False:
            testlink.reportTCResult(2253, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2253, testPlanID, buildName, 'p', "DirectMessageBox_Message Test Passed")

    # search = Institution, Center, Reporter
    def NewDirectMessage_Search_fun(search, search_target):
        testResult = True
        Result_msg = ""
        driver.wait_for_request('.*/GetAccess'+search+'List*')
        
        # Search & Select & Selected select #1 2 3
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#direct_message_send_search_value").send_keys(search_target) 
        driver.find_element(By.CSS_SELECTOR, "#direct_message_send_search > i").click()
        request = driver.wait_for_request('.*/GetAccess'+search+'List*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        for a in range (1, total+1):
            request = driver.wait_for_request('.*/GetAccess'+search+'List*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            for b in range (1, len(data)+1):
                if search == "Reporter":
                    if search_target not in driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/div[6]/div/table/tbody/tr["+str(b)+"]/td[3]").text:
                        testResult = False
                        Result_msg += "#1 "
                        break
                else:
                    if search_target not in driver.find_element(By.CSS_SELECTOR, "#add_dm_access_"+search.lower()+"_list > tbody > tr:nth-child("+str(b)+") > td:nth-child(2)").text:
                        testResult = False
                        Result_msg += "#1 "
                        break
            if testResult == False or a == total:
                # 2, 3은 마지막을 기준으로 판단
                try:
                    if search == "Reporter":
                        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/div[6]/div/table/tbody/tr["+str(len(data))+"]/td[1]/label").click()
                    else:
                        driver.find_element(By.CSS_SELECTOR, "#add_dm_access_"+search.lower()+"_list > tbody > tr:nth-child("+str(len(data))+") > td.th-check.align-center.dm-th-check > label").click()
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#selected_recipient_list_wrapper > button")))
                    if search == "Reporter":
                        assert(driver.find_element(By.CSS_SELECTOR, "#selected_recipient_list_wrapper > button").text == driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/div[6]/div/table/tbody/tr["+str(len(data))+"]/td[3]").text.split(' / ')[1])
                    else:
                        assert(driver.find_element(By.CSS_SELECTOR, "#selected_recipient_list_wrapper > button").text == driver.find_element(By.CSS_SELECTOR, "#add_dm_access_"+search.lower()+"_list > tbody > tr:nth-child("+str(len(data))+") > td:nth-child(2)").text)
                except:
                    testResult = False
                    Result_msg += "#2 "
                driver.find_element(By.CSS_SELECTOR, "#selected_recipient_list_wrapper > button").click()
                time.sleep(0.25)
                if driver.find_element(By.CSS_SELECTOR, "#add_dm_access_"+search.lower()+"_list > tbody > tr:nth-child("+str(len(data))+") > td.th-check.align-center.dm-th-check > label").is_selected == True:
                    testResult = False
                    Result_msg += "#3 "
                break
            del driver.requests
            driver.find_element(By.CSS_SELECTOR, "#add_dm_access_"+search.lower()+"_list_next > a").click()

        return Result_msg

    # msg - NewDirectMessage_Institution_Message Test, NewDirectMessage_Center_Message Test, NewDirectMessage_Reporter_Message Test
    def NewDirectMessage_Message_fun(search, search_target, num):
        Result_msg = ""

        # Search
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#message-add-tab > div:nth-child(2) > div > div.col-lg-5 > div:nth-child(1) > ul > li:nth-child("+str(num)+") > a").click()
        driver.wait_for_request('.*/GetAccess'+search+'List*')
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#direct_message_send_search_value").send_keys(search_target) 
        driver.find_element(By.CSS_SELECTOR, "#direct_message_send_search > i").click()
        driver.wait_for_request('.*/GetAccess'+search+'List*')

        # Send #1
        driver.find_element(By.CSS_SELECTOR, "#add_dm_access_"+search.lower()+"_list > tbody > tr:nth-child(1) > td.th-check.align-center.dm-th-check > label").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#selected_recipient_list_wrapper > button")))
        driver.find_element(By.CSS_SELECTOR, "#add_direct_message_textarea").send_keys("NewDirectMessage_"+search+"_Message Test")
        driver.find_element(By.CSS_SELECTOR, "#add_direct_message").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        if "Direct Message를 전송하였습니다" != driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text:
            Result_msg += "#1 "
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.5)

        # Search
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#message-add-tab > div:nth-child(2) > div > div.col-lg-5 > div:nth-child(1) > ul > li:nth-child("+str(num)+") > a").click()
        driver.wait_for_request('.*/GetAccess'+search+'List*')
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#direct_message_send_search_value").send_keys(search_target) 
        driver.find_element(By.CSS_SELECTOR, "#direct_message_send_search > i").click()
        driver.wait_for_request('.*/GetAccess'+search+'List*')
        
        # no input send #2
        driver.find_element(By.CSS_SELECTOR, "#add_dm_access_"+search.lower()+"_list > tbody > tr:nth-child(1) > td.th-check.align-center.dm-th-check > label").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#selected_recipient_list_wrapper > button")))
        driver.find_element(By.CSS_SELECTOR, "#add_direct_message").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        if "Message 내용을 입력해주세요" != driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text:
            Result_msg += "#2 "
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.5)

        # Cancel #3
        driver.find_element(By.CSS_SELECTOR, "#add_direct_message_textarea").send_keys("NewDirectMessage_"+search+"_Message Test")
        driver.find_element(By.CSS_SELECTOR, "#cancel_add_direct_message").click()
        # text안의 값이 바뀐 경우 처리
        if driver.find_element(By.CSS_SELECTOR, "#add_direct_message_textarea").get_property("value") != "NewDirectMessage_"+search+"_Message Test":
            Result_msg += "#3 "
        time.sleep(0.25)

        return Result_msg

    def NewDirectMessage_Institution_Search():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # NewDirectMessage
        driver.find_element(By.CSS_SELECTOR, "#direct-message-add-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add_direct_message")))

        # Search & Select & Selected select #1 2 3
        driver.find_element(By.CSS_SELECTOR, "#message-add-tab > div:nth-child(2) > div > div.col-lg-5 > div:nth-child(1) > ul > li:nth-child(1) > a").click()
        temp = DirectMessage.NewDirectMessage_Search_fun("Institution", search_institution)
        if temp != "":
            testResult = False
            Result_msg += temp

        print("NewDirectMessage_Institution_Search")
        print(testResult)
        print(Result_msg)

        # NewDirectMessage_Institution_Search결과 전송 ##
        if testResult == False:
            testlink.reportTCResult(2256, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2256, testPlanID, buildName, 'p', "NewDirectMessage_Institution_Search Test Passed")

    def NewDirectMessage_Institution_Message():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # NewDirectMessage
        driver.find_element(By.CSS_SELECTOR, "#direct-message-add-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add_direct_message")))

        # Send, no input send, Cancel #1, 2, 3
        # search, search_target, num, msg
        temp = DirectMessage.NewDirectMessage_Message_fun("Institution", search_institution, 1)
        if temp != "":
            testResult = False
            Result_msg += temp

        print("NewDirectMessage_Institution_Message")
        print(testResult)
        print(Result_msg)

        # NewDirectMessage_Institution_Message결과 전송 ##
        if testResult == False:
            testlink.reportTCResult(2261, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2261, testPlanID, buildName, 'p', "NewDirectMessage_Institution_Message Test Passed")

    def NewDirectMessage_Center_Search():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # NewDirectMessage
        driver.find_element(By.CSS_SELECTOR, "#direct-message-add-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add_direct_message")))

        # Search & Select & Selected select #1 2 3
        driver.find_element(By.CSS_SELECTOR, "#message-add-tab > div:nth-child(2) > div > div.col-lg-5 > div:nth-child(1) > ul > li:nth-child(2) > a").click()
        temp = DirectMessage.NewDirectMessage_Search_fun("Center", search_center)
        if temp != "":
            testResult = False
            Result_msg += temp

        print("NewDirectMessage_Center_Search")
        print(testResult)
        print(Result_msg)

        # NewDirectMessage_Center_Search결과 전송 ##
        if testResult == False:
            testlink.reportTCResult(2266, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2266, testPlanID, buildName, 'p', "NewDirectMessage_Center_Search Test Passed")

    def NewDirectMessage_Center_Message():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # NewDirectMessage
        driver.find_element(By.CSS_SELECTOR, "#direct-message-add-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add_direct_message")))

        # Send, no input send, Cancel #1, 2, 3
        # search, search_target, num, msg
        temp = DirectMessage.NewDirectMessage_Message_fun("Center", search_center, 2)
        if temp != "":
            testResult = False
            Result_msg += temp

        print("NewDirectMessage_Center_Message")
        print(testResult)
        print(Result_msg)

        # NewDirectMessage_Center_Message결과 전송 ##
        if testResult == False:
            testlink.reportTCResult(2271, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2271, testPlanID, buildName, 'p', "NewDirectMessage_Center_Message Test Passed")


    def NewDirectMessage_Reporter_Search():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # NewDirectMessage
        driver.find_element(By.CSS_SELECTOR, "#direct-message-add-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add_direct_message")))

        # Search & Select & Selected select #1 2 3
        driver.find_element(By.CSS_SELECTOR, "#message-add-tab > div:nth-child(2) > div > div.col-lg-5 > div:nth-child(1) > ul > li:nth-child(3) > a").click()
        temp = DirectMessage.NewDirectMessage_Search_fun("Reporter", search_reporter)
        if temp != "":
            testResult = False
            Result_msg += temp

        print("NewDirectMessage_Reporter_Search")
        print(testResult)
        print(Result_msg)

        # NewDirectMessage_Reporter_Search결과 전송 ##
        if testResult == False:
            testlink.reportTCResult(2276, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2276, testPlanID, buildName, 'p', "NewDirectMessage_Reporter_Search Test Passed")

    def NewDirectMessage_Reporter_Message():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # NewDirectMessage
        driver.find_element(By.CSS_SELECTOR, "#direct-message-add-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add_direct_message")))

        # Send, no input send, Cancel #1, 2, 3
        # search, search_target, num, msg
        temp = DirectMessage.NewDirectMessage_Message_fun("Reporter", search_reporter, 3)
        if temp != "":
            testResult = False
            Result_msg += temp

        print("NewDirectMessage_Reporter_Message")
        print(testResult)
        print(Result_msg)

        # NewDirectMessage_Reporter_Message결과 전송 ##
        if testResult == False:
            testlink.reportTCResult(2281, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2281, testPlanID, buildName, 'p', "NewDirectMessage_Reporter_Message Test Passed")

    def DirectMessageSetting_Search_fun(auth, search_target):
        Result_msg = ""

        if auth == "unAuth":
            list_position = 2
        elif auth == "auth":
            list_position = 4

        # ID & Name
        for a in range (1, 3):
            del driver.requests

            driver.find_element(By.CSS_SELECTOR, "#"+auth+"_reporter_search_type").click()
            driver.find_element(By.CSS_SELECTOR, "#"+auth+"_reporter_search_type > option:nth-child("+str(a)+")").click()
            driver.find_element(By.CSS_SELECTOR, "#"+auth+"_reporter_search_value").send_keys(search_target)
            driver.find_element(By.CSS_SELECTOR, "#search_"+auth+"_reporter").click()
            driver.find_element(By.CSS_SELECTOR, "#"+auth+"_reporter_search_value").clear()

            request = driver.wait_for_request('.*/GetDirectMessage.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for b in range(1, len(data)+1):
                if search_target not in driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div["+str(list_position)+"]/div[3]/div/div/table/tbody/tr["+str(b)+"]/td["+str(a+1)+"]").text:
                    if auth == "unAuth":
                        Result_msg += "#"+str(a)+" "
                    else:
                        Result_msg += "#"+str(a+2)+" "
                    break
        
        return Result_msg

    def DirectMessageSetting_Search():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # DirectMessage
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # Direct Message Setting
        driver.find_element(By.CSS_SELECTOR, "#direct-message-setting-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search_unAuth_reporter > i")))

        # unAuth / auth Search #1 2 3 4
        temp = DirectMessage.DirectMessageSetting_Search_fun("unAuth", unauth_search_id)
        temp += DirectMessage.DirectMessageSetting_Search_fun("unAuth", unauth_search_username)
        temp += DirectMessage.DirectMessageSetting_Search_fun("auth", search_id)
        temp += DirectMessage.DirectMessageSetting_Search_fun("auth", search_username)

        if temp != "":
            testResult = False
            Result_msg += temp

        print("DirectMessageSetting_Search")
        print(testResult)
        print(Result_msg)

        ## DirectMessageSetting_Search결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2287, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2287, testPlanID, buildName, 'p', "DirectMessageSetting_Search Test Passed")

    def DirectMessageSetting_Authorize():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # DirectMessage
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # Direct Message Setting
        driver.find_element(By.CSS_SELECTOR, "#direct-message-setting-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search_unAuth_reporter > i")))

        # Auth Search
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#auth_reporter_search_value").send_keys(search_id)
        driver.find_element(By.CSS_SELECTOR, "#search_auth_reporter").click()
        driver.wait_for_request('.*/GetDirectMessage.*')

        # Select #2
        driver.find_element(By.CSS_SELECTOR, "#center_authorized_reporter_list > tbody > tr.odd > td.th-check.align-center.dm-th-check > label").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#selected_reporter_box > button")))
        #rgb(242, 222, 222)
        color = driver.find_element(By.CSS_SELECTOR, "#selected_reporter_box > button").value_of_css_property("background-color")
        driver.find_element(By.CSS_SELECTOR, "#remove_direct_message_authentication_btn > i").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        if color != "rgba(242, 222, 222, 1)" or driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "Direct Messsage 권한을 삭제하였습니다":
            testResult = False
            Result_msg += "#2 "
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.25)

        # UnAuth Search
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#unAuth_reporter_search_value").send_keys(search_id)
        driver.find_element(By.CSS_SELECTOR, "#search_unAuth_reporter").click()
        driver.wait_for_request('.*/GetDirectMessage.*')

        # Select #1
        driver.find_element(By.CSS_SELECTOR, "#center_unauthorized_reporter_list > thead > tr > th.align-center.th-check.dm-th-check.sorting_disabled > label").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#selected_reporter_box > button")))
        #rgb(255, 152, 0)
        color = driver.find_element(By.CSS_SELECTOR, "#selected_reporter_box > button").value_of_css_property("background-color")
        driver.find_element(By.CSS_SELECTOR, "#grant_direct_message_authentication_btn > i").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        if color != "rgba(255, 152, 0, 1)" or driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "Direct Messsage 권한을 추가하였습니다":
            testResult = False
            Result_msg += "#1 "
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.25)

        # Non Select Arrow #3
        if (driver.find_element(By.CSS_SELECTOR, "#remove_direct_message_authentication_btn").value_of_css_property("cursor") != "not-allowed" and
            driver.find_element(By.CSS_SELECTOR, "#grant_direct_message_authentication_btn").value_of_css_property("cursor") != "not-allowed"):
            testResult = False
            Result_msg += "#3 "

        # New User #4
        # User Management Add
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
        driver.find_element(By.CSS_SELECTOR, "#user-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        # Input
        while(1):
            test_id = add_test_id+str(random.randrange(0,100000))
            driver.find_element(By.CSS_SELECTOR, "#user-add-id").send_keys(test_id)
            driver.find_element(By.CSS_SELECTOR, "#user-add-validation-btn > span").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            check = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            if check != "User ID is Exist!":
                break
        driver.find_element(By.CSS_SELECTOR, "#user-add-pw").send_keys(add_test_pw)
        driver.find_element(By.CSS_SELECTOR, "#user-add-name").send_keys(test_id)

        # Reporter Click
        driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > a").click()
        child_num = driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > div").get_property("childElementCount")
        for n in range (1, child_num+1):
            if driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > div > ul > li:nth-child("+str(n)+")").text == "Reporter":
                driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > div > ul > li:nth-child("+str(n)+")").click()

        # Center Click
        driver.find_element(By.CSS_SELECTOR, "#user_add_center_chosen").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user_add_center_chosen > div > div > input[type=text]")))
        driver.find_element(By.CSS_SELECTOR, "#user_add_center_chosen > div > div > input[type=text]").send_keys("인피니트")
        driver.find_element(By.CSS_SELECTOR, "#user_add_center_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        
        # Save
        driver.find_element(By.CSS_SELECTOR, "#user-add-save-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # DirectMessage
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.wait_for_request(".*/GetUnread.*")

        # Direct Message Setting
        driver.find_element(By.CSS_SELECTOR, "#direct-message-setting-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search_unAuth_reporter > i")))

        # Search
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#unAuth_reporter_search_value").send_keys(test_id)
        driver.find_element(By.CSS_SELECTOR, "#search_unAuth_reporter").click()
        driver.wait_for_request('.*/GetDirectMessage.*')

        # Check
        if driver.find_element(By.CSS_SELECTOR, "#center_unauthorized_reporter_list > tbody > tr:nth-child(1) > td:nth-child(2)").text != test_id:
            testResult = False
            Result_msg += "#4 "

        print("DirectMessageSetting_Authorize")
        print(testResult)
        print(Result_msg)

        ## DirectMessageSetting_Authorize결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "DirectMessageSetting_Authorize Test Passed")

    def DirectMessageSetting_Selection():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # DirectMessage
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # Direct Message Setting
        driver.find_element(By.CSS_SELECTOR, "#direct-message-setting-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search_unAuth_reporter > i")))

        # Click > Click & Arrow #1, 2, 3, 4
        driver.find_element(By.CSS_SELECTOR, "#center_unauthorized_reporter_list > tbody > tr:nth-child(1) > td.th-check.align-center.dm-th-check > label").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#selected_reporter_box > button")))
        driver.find_element(By.CSS_SELECTOR, "#center_authorized_reporter_list > tbody > tr.odd > td.th-check.align-center.dm-th-check > label").click()
        time.sleep(0.25)
        if (driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[2]/div[3]/div/div/table/tbody/tr[1]/td[1]/input").is_selected() == True or
            driver.find_element(By.CSS_SELECTOR, "#selected_reporter_box > button").value_of_css_property("background-color") == "rgba(255, 152, 0, 1)"):
            testResult = False
            Result_msg += "#1 "

        if driver.find_element(By.CSS_SELECTOR, "#grant_direct_message_authentication_btn").value_of_css_property("cursor") != "not-allowed":
            tesTresult = False
            Result_msg += "#4 "

        driver.find_element(By.CSS_SELECTOR, "#center_unauthorized_reporter_list > tbody > tr:nth-child(1) > td.th-check.align-center.dm-th-check > label").click()
        time.sleep(0.25)
        if (driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div[3]/div/div/table/tbody/tr[1]/td[1]/input").is_selected() == True or
            driver.find_element(By.CSS_SELECTOR, "#selected_reporter_box > button").value_of_css_property("background-color") == "rgba(242, 222, 222, 1)"):
            testResult = False
            Result_msg += "#2 "

        if driver.find_element(By.CSS_SELECTOR, "#remove_direct_message_authentication_btn").value_of_css_property("cursor") != "not-allowed":
            tesTresult = False
            Result_msg += "#3 "

        print("DirectMessageSetting_Selection")
        print(testResult)
        print(Result_msg)

        ## DirectMessageSetting_Selection결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "DirectMessageSetting_Selection Test Passed")

class Notice:
    def NoticeList_NoticeEditBoard():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Notice
        driver.find_element(By.CSS_SELECTOR, "#tab-notice > a").click()
        driver.implicitly_wait(5)

        # Notice Title #1
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_title").send_keys("rnd_title3#")
        if driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_title").get_property("value") != "rnd_title3#":
            testResult = False
            Rersult_msg += "#1 "
        
        # Notice Board #2
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys("rnd_board3#")
        if driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable > p").get_property("textContent") != "rnd_board3#":
            testResult = False
            Rersult_msg += "#2 "
        
        # Board Bold #3 4
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys(Keys.CONTROL + "a")
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-style > button.note-btn.btn.btn-default.btn-sm.note-btn-bold > i").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/section[1]/div[2]/div[2]/div/div[4]/div[3]/div[2]/p/b")))
        except:
            testResult = False
            Result_msg += "#3 "
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-style > button.note-btn.btn.btn-default.btn-sm.note-btn-bold > i").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/section[1]/div[2]/div[2]/div/div[4]/div[3]/div[2]/p/b")))
            testResult = False
            Result_msg += "#4 "
        except:
            pass
        
        # Board Italic #5 6
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-style > button.note-btn.btn.btn-default.btn-sm.note-btn-italic").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/section[1]/div[2]/div[2]/div/div[4]/div[3]/div[2]/p/i")))
        except:
            testResult = False
            Result_msg += "#5 "
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-style > button.note-btn.btn.btn-default.btn-sm.note-btn-italic").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/section[1]/div[2]/div[2]/div/div[4]/div[3]/div[2]/p/i")))
            testResult = False
            Result_msg += "#6 "
        except:
            pass
        
        # Board Underline #7 8
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-style > button.note-btn.btn.btn-default.btn-sm.note-btn-underline").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/section[1]/div[2]/div[2]/div/div[4]/div[3]/div[2]/p/u")))
        except:
            testResult = False
            Result_msg += "#7 "
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-style > button.note-btn.btn.btn-default.btn-sm.note-btn-underline").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/section[1]/div[2]/div[2]/div/div[4]/div[3]/div[2]/p/u")))
            testResult = False
            Result_msg += "#8 "
        except:
            pass
        
        # Board Strikethrough #9 10
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-style > button.note-btn.btn.btn-default.btn-sm.note-btn-strikethrough").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/section[1]/div[2]/div[2]/div/div[4]/div[3]/div[2]/p/strike")))
        except:
            testResult = False
            Result_msg += "#9 "
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-style > button.note-btn.btn.btn-default.btn-sm.note-btn-strikethrough").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/section[1]/div[2]/div[2]/div/div[4]/div[3]/div[2]/p/strike")))
            testResult = False
            Result_msg += "#10 "
        except:
            pass
        
        # Board Remove #11
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-style > button.note-btn.btn.btn-default.btn-sm.note-btn-strikethrough").click()
        WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/section[1]/div[2]/div[2]/div/div[4]/div[3]/div[2]/p/strike")))
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-style > button:nth-child(5) > i").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/section[1]/div[2]/div[2]/div/div[4]/div[3]/div[2]/p/strike")))
            testResult = False
            Result_msg += "#11 "
        except:
            pass

        # Board Color #12
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-color > div.note-btn-group.btn-group.note-color.note-color-fore > button.note-btn.btn.btn-default.btn-sm.dropdown-toggle > span").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-color > div.note-btn-group.btn-group.note-color.note-color-fore.open > ul > div > div.note-holder > div > div:nth-child(2) > button:nth-child(1)")))
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-color > div.note-btn-group.btn-group.note-color.note-color-fore.open > ul > div > div.note-holder > div > div:nth-child(2) > button:nth-child(1)").click()
            WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable > p > font")))
            assert(driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable > p > font").value_of_css_property("color") == "rgba(255, 0, 0, 1)")
        except:
            testResult = False
            Result_msg += "#12 "
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-style > button:nth-child(5) > i").click()

        # Board Backgorund color #13
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-color > div.note-btn-group.btn-group.note-color.note-color-all > button.note-btn.btn.btn-default.btn-sm.dropdown-toggle > span").click()
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-color > div.note-btn-group.btn-group.note-color.note-color-all.open > ul > div:nth-child(1) > div.note-holder > div > div:nth-child(2) > button:nth-child(1)")))
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-color > div.note-btn-group.btn-group.note-color.note-color-all.open > ul > div:nth-child(1) > div.note-holder > div > div:nth-child(2) > button:nth-child(1)").click()
            WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable > p > span")))
            assert(driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable > p > span").value_of_css_property("background-color") == "rgba(255, 0, 0, 1)")
        except:
            testResult = False
            Result_msg += "#13 "
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-style > button:nth-child(5) > i").click()

        # Picture select #14
        driver.find_element(By.CSS_SELECTOR,"#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-insert > button > i").click()
        WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.modal.note-modal.in > div > div > div.modal-header > h4")))
        if "Insert Image" != driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.modal.note-modal.in > div > div > div.modal-header > h4").text:
            testResult = False
            Result_msg += "#14 "

        if "#14" not in Result_msg:
            # Picture upload #15 16
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/section[1]/div[2]/div[2]/div/div[4]/div[7]/div/div/div[2]/div[1]/input").send_keys(upload_pic)
            try:
                WebDriverWait(driver, 0.3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable > p > img")))
            except:
                testResult = False
                Result_msg += "#15 #16 "

            # A + backspace
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys(Keys.CONTROL + "A")
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys(Keys.BACKSPACE)

            # Picture Open
            driver.find_element(By.CSS_SELECTOR,"#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-insert > button > i").click()
            WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.modal.note-modal.in > div > div > div.modal-header > h4")))

            # Picutre url upload #17
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/section[1]/div[2]/div[2]/div/div[4]/div[7]/div/div/div[2]/div[2]/input").send_keys(upload_pic_url)
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.modal.note-modal.in > div > div > div.modal-footer > input").click()
            try:
                WebDriverWait(driver, 0.3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable > p > img")))
            except:
                testResult = False
                Result_msg += "#17 "

            # A + backspace
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys(Keys.CONTROL + "A")
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys(Keys.BACKSPACE)

            # Picture Open
            driver.find_element(By.CSS_SELECTOR,"#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.panel-heading.note-toolbar > div.note-btn-group.btn-group.note-insert > button > i").click()
            WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.modal.note-modal.in > div > div > div.modal-header > h4")))
            
            # Picutre url bad upload #18
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/section[1]/div[2]/div[2]/div/div[4]/div[7]/div/div/div[2]/div[2]/input").send_keys("bad")
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.modal.note-modal.in > div > div > div.modal-footer > input").click()
            try:
                WebDriverWait(driver, 0.3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable > p > img")))
                testResult = False
                Result_msg += "#18 "
            except:
                pass
        
        # Board input
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys("rnd_board3#")

        # Both On #21
        # Display Now On (Public On - Default)
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(1) > div:nth-child(1) > label").click()
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_confirm").click()
        WebDriverWait(driver, 0.3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        text = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.25)
        if (text != "Notice 등록에 성공하였습니다." or 
            driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(2) > div > label > input").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr.odd > td:nth-child(3) > div > label > input").get_property("checked") == False):
            testResult = False
            Result_msg = "#21 "

        if "#21" not in Result_msg:
            # Title & Board input
            driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_title").send_keys("rnd_title3#")
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys("rnd_board3#")
            
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(1) > div:nth-child(1) > label").click()
            driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_confirm").click()
            WebDriverWait(driver, 0.3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.25)

            if driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr.even > td:nth-child(3) > div > label > input").get_property("checked") == True:
                testResult = False
                Result_msg += "#21"
        
        # Deletion
        if "#21" not in Result_msg:
            for n in range (0, 2):
                element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(7) > button")
                driver.execute_script("arguments[0].click()",element)
                WebDriverWait(driver, 0.3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                time.sleep(0.25)

        # Title & Board input
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_title").send_keys("rnd_title3#")
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys("rnd_board3#")

        # Public off, now on #22
        # public off, now on
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(1) > div:nth-child(1) > label").click()
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(1) > div:nth-child(2) > label").click()
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_confirm").click()
        WebDriverWait(driver, 0.3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        text = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.25)
        if (text != "Notice 등록에 성공하였습니다." or 
            driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(2) > div > label > input").get_property("checked") == True or
            driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr.odd > td:nth-child(3) > div > label > input").get_property("checked") == False):
            testResult = False
            Result_msg = "#22 "

        if "#22" not in Result_msg:
            # Title & Board input
            driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_title").send_keys("rnd_title3#")
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys("rnd_board3#")
            
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(1) > div:nth-child(1) > label").click()
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(1) > div:nth-child(2) > label").click()
            driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_confirm").click()
            WebDriverWait(driver, 0.3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.25)

            if driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr.even > td:nth-child(3) > div > label > input").get_property("checked") == True:
                testResult = False
                Result_msg += "#22"
        
        # Deletion
        if "#22" not in Result_msg:
            for n in range (0, 2):
                element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(7) > button")
                driver.execute_script("arguments[0].click()",element)
                WebDriverWait(driver, 0.3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                time.sleep(0.25)

        # Title & Board input
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_title").send_keys("rnd_title3#")
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys("rnd_board3#")

        # Clear #23
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_clear").click()
        if (driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_title").get_property("value") != "" or
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").get_property("textContent") != ""):
            testResult = False
            Result_msg += "#23 "

        # Public Display Function #20
        # Title & Board input & Save
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_title").send_keys("rnd_title3#")
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys("rnd_board3#_public")
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(1) > div:nth-child(1) > label").click()
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_confirm").click()
        WebDriverWait(driver, 0.3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.25)

        # Title & Board input & Save
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_title").send_keys("rnd_title3#")
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys("rnd_board3#_nopublic")
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(1) > div:nth-child(1) > label").click()
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(1) > div:nth-child(2) > label").click()
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_confirm").click()
        WebDriverWait(driver, 0.3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # 새로운 탭 + 전환
        driver.execute_script("window.open()")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(WorklistUrl);
        driver.implicitly_wait(5)
        time.sleep(1.5)

        driver.switch_to.window(driver.window_handles[2])
        driver.implicitly_wait(5)
        if driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/div[2]/div").text != "rnd_board3#_public":
            testResult = False
            Result_msg += "#20 "
        driver.close()
        driver.switch_to.window(driver.window_handles[1])

        wk_login(wk_id, wk_pw)
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[2])
        driver.implicitly_wait(5)
        if driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/div[2]/div").text != "rnd_board3#_nopublic":
            testResult = False
            Result_msg += "#20 "
        driver.close()
        driver.switch_to.window(driver.window_handles[1])

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        driver.find_element(By.CSS_SELECTOR, "body > nav > div > ul:nth-child(3) > li > a > span").click()
        driver.implicitly_wait(5)
        time.sleep(1.5)

        driver.switch_to.window(driver.window_handles[1])
        if driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/div[2]/div").text != "rnd_board3#_public":
            testResult = False
            Result_msg = "#20 "
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Deletion
        admin_login()
        # Notice
        driver.find_element(By.CSS_SELECTOR, "#tab-notice > a").click()
        driver.implicitly_wait(5)
        for n in range (0, 2):
            element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(7) > button")
            driver.execute_script("arguments[0].click()",element)
            WebDriverWait(driver, 0.3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.25)

        print("NoticeList_NoticeEditBoard")
        print(testResult)
        print(Result_msg)

        ## NoticeList_NoticeEditBoard결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "NoticeList_NoticeEditBoard Test Passed")

    def NoticeList_Edit():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Notice
        driver.find_element(By.CSS_SELECTOR, "#tab-notice > a").click()
        driver.implicitly_wait(5)

        # Add #9
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_title").send_keys("rnd_title_edit")
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys("rnd_board_edit")
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(1) > div:nth-child(1) > label").click()
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_confirm").click()
        WebDriverWait(driver, 0.3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        if driver.find_element(By.CSS_SELECTOR , "#curernt_display_list > tbody > tr.odd > td:nth-child(5)").text != "rnd_title_edit":
            testResult = False
            Result_msg  += "#9 "
        
        if "#9" not in Result_msg:       
            # Edit #1
            element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr.odd > td:nth-child(1) > div")
            driver.execute_script("arguments[0].click()",element)
            time.sleep(0.15)
            if driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_title").get_property("value") != "rnd_title_edit":
                testResult == False
                Result_msg += "#1 "

        if "#1" not in Result_msg:
            # Update #2
            driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_title").send_keys("_update")
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys("_update")
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(1) > div:nth-child(1) > label").click()
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(1) > div:nth-child(2) > label").click()

            driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_update").click()
            WebDriverWait(driver, 0.3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            driver.find_element(By.CSS_SELECTOR , "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.25)
            if (driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(3) > div > label > input").get_property("checked") == True or 
                driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr.odd > td:nth-child(2) > div > label > input").get_property("checked") == True or
                driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(5)").text != "rnd_title_edit_update" or 
                msg != "Notice 정보를 수정하였습니다."):
                testResult = False
                Result_msg += "#2 "

            # Edit
            element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr.odd > td:nth-child(1) > div")
            driver.execute_script("arguments[0].click()",element)
            time.sleep(0.15)

            # Create #3
            driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_title").send_keys("_create")
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys("_create")
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(1) > div:nth-child(1) > label").click()
            driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(1) > div:nth-child(2) > label").click()

            driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_confirm").click()
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            driver.find_element(By.CSS_SELECTOR , "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.25)
            if (driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(3) > div > label > input").get_property("checked") == False or 
                driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr.odd > td:nth-child(2) > div > label > input").get_property("checked") == False or
                driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(5)").text != "rnd_title_edit_update_create" or 
                driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(2) > td:nth-child(5)").text != "rnd_title_edit_update" or
                msg != "Notice 등록에 성공하였습니다."):
                testResult = False
                Result_msg += "#3 "

            # Toggle #4 5 6 7
            # 2-1 off > on
            element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(2) > td:nth-child(2) > div > label > span")
            driver.execute_script("arguments[0].click()",element)
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            if (msg != "Notice 정보를 수정하였습니다." or 
                driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(2) > td:nth-child(2) > div > label > input").get_property("checked")==False):
                testResult = False
                Result_msg += "#4 "
            # 2-2 off > on
            element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(2) > td:nth-child(3) > div > label > span")
            driver.execute_script("arguments[0].click()",element)
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            if (msg != "Notice 정보를 수정하였습니다." or 
                driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(5)").text != "rnd_title_edit_update" or
                driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(3) > div > label > input").get_property("checked")==False):
                testResult = False
                Result_msg += "#5 "

            if (driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(2) > td:nth-child(5)").text != "rnd_title_edit_update_create" or 
                driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(2) > td:nth-child(3) > div > label > input").get_property("checked") != False):
                testResult = False
                Result_msg += "#6 "

            # 1-1 on > off
            element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(2) > div > label > span")
            driver.execute_script("arguments[0].click()",element)
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.15)
            # 2-1 on > off
            element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(2) > td:nth-child(2) > div > label > span")
            driver.execute_script("arguments[0].click()",element)
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.15)
            # 2-2 off > on
            element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(2) > td:nth-child(2) > div > label > span")
            driver.execute_script("arguments[0].click()",element)
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.15)
            if (driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(2) > td:nth-child(5)").text != "rnd_title_edit_update" or 
                driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(2) > td:nth-child(3) > div > label > input").get_property("checked") != False):
                testResult = False
                Result_msg += "#7 "

            for n in range (0, 2):
                element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(7) > button")
                driver.execute_script("arguments[0].click()",element)
                WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                time.sleep(0.25)

        print("NoticeList_Edit")
        print(testResult)
        print(Result_msg)

        ## NoticeList_Edit결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "NoticeList_Edit Test Passed")

    def NoticeList_Delete():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Notice
        driver.find_element(By.CSS_SELECTOR, "#tab-notice > a").click()
        driver.implicitly_wait(5)

        # Add
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_title").send_keys("rnd_title_delete")
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys("rnd_board_edit")
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_confirm").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.3)

        # Delete #1
        element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(7) > button")
        driver.execute_script("arguments[0].click()",element)
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.25)

        try:
            if (msg != "Notice가 삭제되었습니다." or 
                driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr.odd > td:nth-child(5)").text == "rnd_title_delete"):
                testResult = False
                Result_msg += "#1 "
        except:
            pass

        print("NoticeList_Delete")
        print(testResult)
        print(Result_msg)

        ## NoticeList_Delete결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "NoticeList_Delete Test Passed")

    def NoticeList_NoticeDisplay():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Notice
        driver.find_element(By.CSS_SELECTOR, "#tab-notice > a").click()
        driver.implicitly_wait(5)

        # Add
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_title").send_keys("rnd_title_display")
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div.note-editor.note-frame.panel.panel-default > div.note-editing-area > div.note-editable").send_keys("rnd_board_display")
        driver.find_element(By.CSS_SELECTOR, "#register_itr_notice_confirm").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.3)

        # Display #1
        element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr.odd > td:nth-child(8) > button")
        driver.execute_script("arguments[0].click()",element)
        driver.switch_to.window(driver.window_handles[1])
        driver.implicitly_wait(5)
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#notice_modal_cancel")))
        if (driver.find_element(By.CSS_SELECTOR, "#notice_body_title").text !=  "rnd_title_display" or
            driver.find_element(By.CSS_SELECTOR, "#notice_modal_body_right_side > div").text != "rnd_board_display"):
            testResult = False
            Result_msg += "#1 "
        driver.find_element(By.CSS_SELECTOR, "#notice_modal_cancel").click()
        driver.switch_to.window(driver.window_handles[0])
        driver.implicitly_wait(5)

        # Delete
        element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(7) > button")
        driver.execute_script("arguments[0].click()",element)
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.25)


        print("NoticeList_NoticeDisplay")
        print(testResult)
        print(Result_msg)

        ## NoticeList_NoticeDisplay결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "NoticeList_NoticeDisplay Test Passed")

class Auditlog:
    def Auditlog_Search():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Get Job Key & Insti Name
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div[1]").click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#refer-assigned-list > tbody > tr.odd > td:nth-child(2)")))
        job_key = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list > tbody > tr.odd > td:nth-child(2)").get_property("textContent")
        insti_name = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div[1]").get_attribute("data-institution-name")

        # Auditlog
        driver.find_element(By.CSS_SELECTOR, "#tab-auditlog > a").click()
        driver.implicitly_wait(5)

        # Search #1
        del driver.requests
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "#auditlog_search_job_key_field").send_keys(job_key)
        driver.find_element(By.CSS_SELECTOR, "#auditlog_search").click()
        request = driver.wait_for_request('.*/SearchAuditLog.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        board_date = datetime.strptime(driver.find_element(By.CSS_SELECTOR, "#auditlog_search_table > tbody > tr:nth-child(1) > td.align-center\,.auditlog-table-data.sorting_1").text, '%Y-%m-%d %H:%M:%S')
        for n in range(1, len(data)+1):
            date_temp = datetime.strptime(driver.find_element(By.CSS_SELECTOR, "#auditlog_search_table > tbody > tr:nth-child("+str(n)+") > td.align-center\,.auditlog-table-data.sorting_1").text, '%Y-%m-%d %H:%M:%S')
            sub = str(board_date - date_temp)
            board_date = date_temp
            if (driver.find_element(By.CSS_SELECTOR, "#auditlog_search_table > tbody > tr:nth-child("+str(n)+") > td:nth-child(2)").text != insti_name or 
                '-' in sub):
                testResult = False
                Result_msg += "#1 "
                break

        print("Auditlog_Search")
        print(testResult)
        print(Result_msg)

        ## Auditlog_Search결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "Auditlog_Search Test Passed")

    def Auditlog_Export():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Get Job Key & Insti Name
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div[1]").click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#refer-assigned-list > tbody > tr.odd > td:nth-child(2)")))
        job_key = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list > tbody > tr.odd > td:nth-child(2)").get_property("textContent")

        # Auditlog
        driver.find_element(By.CSS_SELECTOR, "#tab-auditlog > a").click()
        driver.implicitly_wait(5)

        # Search
        driver.find_element(By.CSS_SELECTOR, "#auditlog_search_job_key_field").send_keys(job_key)
        driver.find_element(By.CSS_SELECTOR, "#auditlog_search").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#auditlog_export")))

        # Export #1
        driver.find_element(By.CSS_SELECTOR, "#auditlog_export").click()
        try:
            driver.wait_for_request(".*/GetExportData")
        except:
            testResult = False
            Result_msg += "#1 "

        print("Auditlog_Export")
        print(testResult)
        print(Result_msg)

        ## Auditlog_Export결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "Auditlog_Export Test Passed")

    def Auditlog_Showentries_fun(entries, num):
        Result_msg = ""

        del driver.requests
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "#auditlog_search_table_length > label > select").click()
        driver.find_element(By.CSS_SELECTOR, "#auditlog_search_table_length > label > select > option:nth-child("+str(num)+")").click()
        request = driver.wait_for_request('.*/SearchAuditLog.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        if data["Length"] != entries:
            Result_msg += "#"+str(num)+" "
        if data["recordsFiltered"] > entries:
            try:
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#auditlog_search_table_next > a")))
            except:
                Result_msg += "#"+str(num)+" "

        return Result_msg

    def Auditlog_Showentries():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Get Job Key & Insti Name
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div[1]").click()
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#refer-assigned-list > tbody > tr.odd > td:nth-child(2)")))
        job_key = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list > tbody > tr.odd > td:nth-child(2)").get_property("textContent")

        # Auditlog
        driver.find_element(By.CSS_SELECTOR, "#tab-auditlog > a").click()
        driver.implicitly_wait(5)

         # Search
        driver.find_element(By.CSS_SELECTOR, "#auditlog_search_job_key_field").send_keys(job_key)
        driver.find_element(By.CSS_SELECTOR, "#auditlog_search").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#auditlog_export")))



        Result_msg += Auditlog.Auditlog_Showentries_fun(20, 1)
        Result_msg += Auditlog.Auditlog_Showentries_fun(50, 2)
        Result_msg += Auditlog.Auditlog_Showentries_fun(100, 3)

        print("Auditlog_Showentries")
        print(testResult)
        print(Result_msg)

        ## Auditlog_Showentries결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "Auditlog_Showentries Test Passed")

    def Auditlog_Sorting():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Get Job Key
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div[1]").click()
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#refer-assigned-list > tbody > tr.odd > td:nth-child(2)")))
        job_key = driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list > tbody > tr.odd > td:nth-child(2)").get_property("textContent")

        # Auditlog
        driver.find_element(By.CSS_SELECTOR, "#tab-auditlog > a").click()
        driver.implicitly_wait(5)

        # Search & Date #1
        driver.find_element(By.CSS_SELECTOR, "#auditlog_search_job_key_field").send_keys(job_key)
        driver.find_element(By.CSS_SELECTOR, "#auditlog_search").click()

        del driver.requests
        time.sleep(0.25)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div/div[4]/div[1]/div/table/thead/tr/th[11]").click()
        time.sleep(0.25)
        request = driver.wait_for_request('.*/SearchAuditLog.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        board_date = datetime.strptime(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div/div[4]/div[2]/table/tbody/tr[1]/td[11]").text, '%Y-%m-%d %H:%M:%S')
        for n in range(1, len(data)+1):
            date_temp = datetime.strptime(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div/div[4]/div[2]/table/tbody/tr["+str(n)+"]/td[11]").text, '%Y-%m-%d %H:%M:%S')
            sub = str(board_date - date_temp)
            board_date = date_temp
            if '-' not in sub:
               if sub != "0:00:00":
                    testResult = False
                    Result_msg += "#1 "
                    break

        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div/div[4]/div[1]/div/table/thead/tr/th[11]").click()
        time.sleep(0.25)
        board_date = datetime.strptime(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div/div[4]/div[2]/table/tbody/tr[1]/td[11]").text, '%Y-%m-%d %H:%M:%S')
        for n in range(1, len(data)+1):
            date_temp = datetime.strptime(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div/div[4]/div[2]/table/tbody/tr["+str(n)+"]/td[11]").text, '%Y-%m-%d %H:%M:%S')
            sub = str(board_date - date_temp)
            board_date = date_temp
            if '-' in sub:
                testResult = False
                Result_msg += "#1 "
                break

        print("Auditlog_Sorting")
        print(testResult)
        print(Result_msg)

        ## Auditlog_Sorting결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "Auditlog_Sorting Test Passed")

    def Auditlog_Data():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Auditlog
        driver.find_element(By.CSS_SELECTOR, "#tab-auditlog > a").click()
        driver.implicitly_wait(5)

        # Search
        driver.find_element(By.CSS_SELECTOR, "#auditlog_search_job_key_field").send_keys("74832064")
        driver.find_element(By.CSS_SELECTOR, "#auditlog_search").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#auditlog_export")))

        del driver.requests
        time.sleep(0.25)
        request = driver.wait_for_request('.*/SearchAuditLog.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        for n in range(1, len(data)+1):
            # app
            if ("PANDORA" in driver.find_element(By.CSS_SELECTOR, "#auditlog_search_table > tbody > tr:nth-child("+str(n)+") > td:nth-child(5)").text or 
                "PANGEA" in driver.find_element(By.CSS_SELECTOR, "#auditlog_search_table > tbody > tr:nth-child("+str(n)+") > td:nth-child(5)").text or 
                "ITRWeb" in driver.find_element(By.CSS_SELECTOR, "#auditlog_search_table > tbody > tr:nth-child("+str(n)+") > td:nth-child(5)").text or 
                "ITRWorklist" in driver.find_element(By.CSS_SELECTOR, "#auditlog_search_table > tbody > tr:nth-child("+str(n)+") > td:nth-child(5)").text):
                testResult = False
                Result_msg += "#1 "
                break
            # id
            if ("PANDORA" in driver.find_elemnet(By.CSS_SELECTOR, "#auditlog_search_table > tbody > tr:nth-child("+str(n)+") > td:nth-child(7)").text or 
                "PANGEA" in driver.find_elemnet(By.CSS_SELECTOR, "#auditlog_search_table > tbody > tr:nth-child("+str(n)+") > td:nth-child(7)").text or 
                "ITRWeb" in driver.find_elemnet(By.CSS_SELECTOR, "#auditlog_search_table > tbody > tr:nth-child("+str(n)+") > td:nth-child(7)").text or 
                "ITRWorklist" in driver.find_elemnet(By.CSS_SELECTOR, "#auditlog_search_table > tbody > tr:nth-child("+str(n)+") > td:nth-child(7)").text):
                testResult = False
                Result_msg += "#1 "
                break
            # name
            if ("PANDORA" in driver.find_element(By.CSS_SELECTORq, "#auditlog_search_table > tbody > tr:nth-child("+str(n)+") > td:nth-child(8)").text or 
                "PANGEA" in driver.find_element(By.CSS_SELECTORq, "#auditlog_search_table > tbody > tr:nth-child("+str(n)+") > td:nth-child(8)").text or 
                "ITRWeb" in driver.find_element(By.CSS_SELECTORq, "#auditlog_search_table > tbody > tr:nth-child("+str(n)+") > td:nth-child(8)").text or 
                "ITRWorklist" in driver.find_element(By.CSS_SELECTORq, "#auditlog_search_table > tbody > tr:nth-child("+str(n)+") > td:nth-child(8)").text):
                testResult = False
                Result_msg += "#1 "
                break

        print("Auditlog_Data")
        print(testResult)
        print(Result_msg)

        ## Auditlog_Data결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "Auditlog_Data Test Passed")

class MultiReadingCenterRule:
    def SearchFilter():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # Institution
        driver.find_element(By.CSS_SELECTOR, "#institutions-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr[1]/td[2]/a")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr[1]/td[2]/a").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-modify-close-btn")))
        insti_name = driver.find_element(By.CSS_SELECTOR, "#institutions-modify-institution-name").get_property("value")
        center_name = []
        num = 0
        while(1):
            try:
                num += 1
                center_name.append(driver.find_element(By.CSS_SELECTOR, "#institutions_modify_center_code_list_chosen > ul > li:nth-child("+str(num)+") > span").text)
            except:
                if num == 1:
                    center_name.append("")
                break
        element = driver.find_element(By.CSS_SELECTOR, "#institutions-modify-close-btn")
        driver.execute_script("arguments[0].click()",element)
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        
        # MultiReadingCenterRule
        driver.find_element(By.CSS_SELECTOR, "#multiReadingCenterRule-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi_center_rule_search_modality_chosen > a > span")))

        # Institution > Center #1
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[1]/div[2]/div/div[1]/div/a/span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_institutioncode_chosen > div > div > input[type=text]").send_keys(insti_name)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_institutioncode_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        time.sleep(0.25)
        try:
            center_name.index(driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_centercode_chosen > a > span").get_property("textContent"))
        except:
            testResult = False
            Result_msg += "#1 "
        
        # Institution & Center Search #2
        del driver.requests
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-search").click()
        request = driver.wait_for_request('.*/GetMultiReadingCenterRuleList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        for n in range (1, len(data)+1):
            if (driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[2]/div/table/tbody/tr["+str(n)+"]/td[2]/a").text != insti_name or
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[2]/div/table/tbody/tr["+str(n)+"]/td[3]").text not in center_name):
                testResult = False
                Result_msg += "#2 "

        # Request Code #4
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_requestcode_chosen > ul > li > input[type=text]").click()
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi_center_rule_search_requestcode_chosen > div > ul > li:nth-child(1)")))
        except:
            testResult = False
            Result_msg += "#4 "

        # Request Code Delete #5
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_requestcode_chosen > div > ul > li:nth-child(1)").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi_center_rule_search_requestcode_chosen > ul > li.search-choice > a")))
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_requestcode_chosen > ul > li.search-choice > a").click()
        try:
            driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_requestcode_chosen > ul > li.search-choice > span")
            testResult = False
            Result_msg += "#5 "
        except:
            pass

        # MultiReadingCenterRule
        driver.find_element(By.CSS_SELECTOR, "#multiReadingCenterRule-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi_center_rule_search_modality_chosen > a > span")))

        # Modality Search #3
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_modality_chosen > a > span").click()
        modal = driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_modality_chosen > div > ul > li:nth-child(3)").text.split(' ')[0]
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_modality_chosen > div > ul > li:nth-child(3)").click()
        del driver.requests
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-search").click()
        request = driver.wait_for_request('.*/GetMultiReadingCenterRuleList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        for n in range (1, len(data)+1):
            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[2]/div/table/tbody/tr["+str(n)+"]/td[4]").text != modal:
                testResult = False
                Result_msg += "#3 "

        print("MultiReadingCenterRule_SearchFilter")
        print(testResult)
        print(Result_msg)

        ## MultiReadingCenterRule_SearchFilter결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "MultiReadingCenterRule_SearchFilter Test Passed")

    def Add():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

         # Institution
        driver.find_element(By.CSS_SELECTOR, "#institutions-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr[1]/td[2]/a")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr[1]/td[2]/a").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-modify-close-btn")))
        insti_name = driver.find_element(By.CSS_SELECTOR, "#institutions-modify-institution-name").get_property("value")
        center_name = []
        num = 0
        while(1):
            try:
                num += 1
                center_name.append(driver.find_element(By.CSS_SELECTOR, "#institutions_modify_center_code_list_chosen > ul > li:nth-child("+str(num)+") > span").text)
            except:
                if num == 1:
                    center_name.append("")
                break
        element = driver.find_element(By.CSS_SELECTOR, "#institutions-modify-close-btn")
        driver.execute_script("arguments[0].click()",element)
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        
        # MultiReadingCenterRule
        driver.find_element(By.CSS_SELECTOR, "#multiReadingCenterRule-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi_center_rule_search_modality_chosen > a > span")))

        # Institution Select #1
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-add-close-btn")))
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > div > div > input[type=text]").send_keys(insti_name)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        time.sleep(0.25)
        if (driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > a > span").text not in center_name or 
            driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-add-save-btn").value_of_css_property("cursor") != "not-allowed"):
            testResult = False
            Result_msg += "#1 "

        # Center Right #2
        select_center = driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > a > span").text
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-center-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-center-remove-btn")))
        if (driver.find_element(By.CSS_SELECTOR, "#selected_multi_center_rule_add_center_chosen > a > span").text != select_center or 
            driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-add-save-btn").value_of_css_property("cursor") != "not-allowed"):
            testResult = False
            Result_msg += "#2 "

        # Center Left #3
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-center-remove-btn").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > div > div > input[type=text]").send_keys(select_center)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        if driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > a > span").text != select_center:
            testResult = False
            Result_msg += "#3 "

        # Center Right
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-center-remove-btn").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > div > div > input[type=text]").send_keys(select_center)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-center-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-center-remove-btn")))

        # Modality Right #4
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > ul > li:nth-child(2)").click()
        select_modal = driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > a > span").text
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modality-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-modality-remove-btn")))
        if (driver.find_element(By.CSS_SELECTOR, "#selected_multi_center_rule_add_modality_chosen > a > span").text != select_modal or
            driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-add-save-btn").value_of_css_property("cursor") == "not-allowed"):
            testResult = False
            Result_msg += "#4 "

        # Modality Left #5
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modality-remove-btn").click()
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys(select_modal.split(' - ')[0])
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        if (driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > a > span").text != select_modal or
            driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-add-save-btn").value_of_css_property("cursor") != "not-allowed"):
            testResult = False
            Result_msg += "#5 "

        # Modality Right
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modality-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-modality-remove-btn")))

        # Request Code #6
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_request_code_chosen > ul > li > input").click()
        request_name = driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_request_code_chosen > div > ul > li:nth-child(1)").text
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_request_code_chosen > div > ul > li:nth-child(1)").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi_center_rule_add_request_code_chosen > ul > li.search-choice > a")))
        if driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_request_code_chosen > ul > li.search-choice > span").text != request_name:
            testResult = False
            Result_msg += "#6 "

        # Request Code Delete #7
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_request_code_chosen > ul > li.search-choice > a").click()
        try:
            driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_request_code_chosen > ul > li.search-choice > span")
            testResult = False
            Result_msg += "#7 "
        except:
            pass

        # Institution Change #8
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > a > span").click()
        num = 0
        while(1):
            num+=1
            if driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > div > ul > li:nth-child("+str(num)+")").text != insti_name:
                driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > div > ul > li:nth-child("+str(num)+")").click()
                break
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-center-add-btn")))
        if (driver.find_element(By.CSS_SELECTOR, "#selected_multi_center_rule_add_center_chosen > a > span").text == select_center or 
            driver.find_element(By.CSS_SELECTOR, "#selected_multi_center_rule_add_modality_chosen > a > span").text == select_modal):
            testResult = False
            Result_msg += "#8 "

        # Center Delete #9
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-center-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-center-remove-btn")))
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys(select_modal.split(' - ')[0])
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modality-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-modality-remove-btn")))
        # center left
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-center-remove-btn").click()
        time.sleep(0.25)
        if (driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-add-save-btn").value_of_css_property("cursor") != "not-allowed" or 
            driver.find_element(By.CSS_SELECTOR, "#selected_multi_center_rule_add_modality_chosen > a > span").text == select_modal):
            testResult = False
            Result_msg += "#9 "

        # Modality Delete #10
        # Set
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > div > div > input[type=text]").send_keys(insti_name)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > div > div > input[type=text]").send_keys(select_center)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-center-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-center-remove-btn")))
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys(select_modal.split(' - ')[0])
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modality-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-modality-remove-btn")))
        # modality left
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modality-remove-btn").click()
        time.sleep(0.25)
        if driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-add-save-btn").value_of_css_property("cursor") != "not-allowed":
            testResult = False
            Result_msg += "#10 "
            
        # Close #12
        # close
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-add-close-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button")))
        # no
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-add-close-btn")))
        except:
            testResult = False
            Result_msg += "#12 "
        # close
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-add-close-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button")))
        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
        except:
            testResult = False
            Result_msg += "#12 "

        # Save #11
        # Add
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > a > span")))
        # institution
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > div > div > input[type=text]").send_keys("INFINITT_TEST")
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        # Center
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > div > div > input[type=text]").send_keys("TEST_CENTER")
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        # Center right
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-center-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
        # Modality
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys("AU")
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        # Modality right
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modality-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-modality-remove-btn")))
        # save
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-add-save-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button")))
        # no
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
        except:
            testResult = False
            Result_msg += "#11 "

        # Add
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > a > span")))
        # institution
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > div > div > input[type=text]").send_keys(search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        # Center
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > div > div > input[type=text]").send_keys(search_center)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        # Center right
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-center-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
        # Modality
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys("AS")
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        # Modality right
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modality-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-modality-remove-btn")))
        # Modality
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys("AU")
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        # Modality right
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modality-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-modality-remove-btn")))
        # Center
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > div > div > input[type=text]").send_keys(search_center_2)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        # Center right
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-center-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
        # Modality
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys("AS")
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        # Modality right
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modality-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-modality-remove-btn")))
        # Modality
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys("AU")
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_modality_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        # Modality right
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modality-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-modality-remove-btn")))
        # save
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-add-save-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button")))
        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        try:
            time.sleep(0.25)
            driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()
        except:
            testResult = False
            Result_msg += "#11 "
        time.sleep(0.25)
 
        print("MultiReadingCenterRule_Add")
        print(testResult)
        print(Result_msg)

        ## MultiReadingCenterRule_Add결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "MultiReadingCenterRule_Add Test Passed")

    def Delete():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)
        time.sleep(0.15)

        # MultiReadingCenterRule
        driver.find_element(By.CSS_SELECTOR, "#multiReadingCenterRule-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi_center_rule_search_modality_chosen > a > span")))

        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_institutioncode_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_institutioncode_chosen > div > div > input[type=text]").send_keys(search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_institutioncode_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_centercode_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_centercode_chosen > div > div > input[type=text]").send_keys("인피니트테스트")
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_centercode_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)

        time.sleep(0.1)
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-search").click()
        time.sleep(0.1)

        # No
        try:
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[2]/div/table/tbody/tr/td[1]/label").click()
            driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.delete-btn").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button")))
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        except:
            testResult = False
            Result_msg += "#1 "
        # yes
        try:
            driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.delete-btn").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button")))
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.1)
            assert(driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text == "삭제하였습니다.")
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        except:
            testResul = False
            Result_msg += "#1 "


        print("MultiReadingCenterRule_Delete")
        print(testResult)
        print(Result_msg)

        ## MultiReadingCenterRule_Delete결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "MultiReadingCenterRule_Delete Test Passed")

    def Modify():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)
        time.sleep(0.3)

        # MultiReadingCenterRule
        driver.find_element(By.CSS_SELECTOR, "#multiReadingCenterRule-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi_center_rule_search_modality_chosen > a > span")))

        del driver.requests
        time.sleep(0.1)

        # Search
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_institutioncode_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_institutioncode_chosen > div > div > input[type=text]").send_keys(search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_institutioncode_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        time.sleep(0.1)
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-search").click()
        time.sleep(0.1)

        request = driver.wait_for_request('.*/GetMultiReadingCenterRuleList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        selected_center = []
        for n in data:
            if n["CenterName"] not in selected_center:
                selected_center.append(n["CenterName"])
        selected_modal = []
        temp = []
        num = 0
        for n in range (0, len(data)):
            if data[n]["CenterName"] != selected_center[num]:
                selected_modal.append(temp)
                num += 1
                temp = []
            if data[n]["Modality"] not in temp:
                temp.append(data[n]["Modality"])
            if n+1 == len(data):
                selected_modal.append(temp)


        # instituion name click #1
        insti_name = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[2]/div/table/tbody/tr[1]/td[2]/a").text
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[2]/div/table/tbody/tr[1]/td[2]/a").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-modify-close-btn")))
        if (driver.find_element(By.CSS_SELECTOR, "#modifyCenterRuleLabel").text != "Multi Reading Center Rule Modify" or 
            driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_institution_chosen > a > span").text != insti_name):
            testResult = False
            Result_msg += "#1 "

        # Selected Center, Selected Center Change(Modality) #2 3
        a_num = 0
        while(1):
            a_num += 1
            driver.find_element(By.CSS_SELECTOR, "#selected_multi_center_rule_modify_center_chosen > a").click()
            try:
                element = driver.find_element(By.CSS_SELECTOR, "#selected_multi_center_rule_modify_center_chosen > div > ul > li:nth-child("+str(a_num)+")")
                cur_center = element.text
            except:
                if len(selected_center) != 0:
                    testResult = False
                    Result_msg += "#2 "
                break

            if cur_center in selected_center:
                target = selected_center.index(cur_center)
                element.click()
                
                b_num = 0
                temp = []
                driver.find_element(By.CSS_SELECTOR, "#selected_multi_center_rule_modify_modality_chosen > a > span").click()
                while(1):
                    try:
                        b_num += 1
                        temp.append(driver.find_element(By.CSS_SELECTOR, "#selected_multi_center_rule_modify_modality_chosen > div > ul > li:nth-child("+str(b_num)+")").text.split('-')[0])
                    except:
                        break
                if temp != selected_modal[target]:
                    testResult = False
                    Result_msg += "#3 "

                selected_center.remove(cur_center)
                del selected_modal[target]
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modify-close-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.25)

        # Institution name click
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[2]/div/table/tbody/tr[1]/td[2]/a").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-modify-close-btn")))

        # Modality Left Save #6 7
        # left
        driver.find_element(By.CSS_SELECTOR, "#modify-multi-center-rule-modality-remove-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-modify-save-btn")))
        # != not-allowed
        one_remain = driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modify-save-btn").value_of_css_property("cursor")
        # save
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modify-save-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#modifyCenterRuleLabel")))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#modifyCenterRuleLabel").get_property("textContent")
        # left
        driver.find_element(By.CSS_SELECTOR, "#modify-multi-center-rule-modality-remove-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-modify-save-btn")))
        # save
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modify-save-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.15)
        yes_msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        # institution name click
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[2]/div/table/tbody/tr[1]/td[2]/a")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[2]/div/table/tbody/tr[1]/td[2]/a").click()
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#modifyCenterRuleLabel")))
        # modality check
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_modality_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_modality_chosen > div > div > input[type=text]").send_keys("AS")
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_modality_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)

        if (msg != "수정하시겠습니까?" or
            no_msg != "Multi Reading Center Rule Modify" or
            yes_msg != "수정하였습니다." or 
            driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_modality_chosen > a > span").text != "AS - Angioscopy"):
            testResult = False
            Result_msg += "#6 "

        # left
        driver.find_element(By.CSS_SELECTOR, "#modify-multi-center-rule-modality-remove-btn").click()
        if (one_remain == "not-allowed" or
            driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modify-save-btn").value_of_css_property("cursor") != "not-allowed"):
            testResult = False
            REesult_msg += "#7 "

        # Center Left Save #4 5
        # left
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[4]/div/div/div[2]/div[2]/div/div/div[2]/button[2]").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[4]/div/div/div[3]/button[2]")))
        # != not-allowed
        one_remain = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[4]/div/div/div[3]/button[2]").value_of_css_property("cursor")
        # save
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[4]/div/div/div[3]/button[2]").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[14]/div[7]/button"),"No"))
        msg = driver.find_element(By.XPATH, "/html/body/div[14]/h2").text
        # no
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#selected_multi_center_rule_modify_center_chosen > a > span"),"인피니트"))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#modifyCenterRuleLabel").get_property("textContent")
         # left
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[4]/div/div/div[2]/div[2]/div/div/div[2]/button[2]").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[4]/div/div/div[3]/button[2]")))
        # save
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[4]/div/div/div[3]/button[2]").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[14]/div[7]/button"),"No"))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[14]/div[7]/div/button"),"OK"))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-search")))
        # search
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_centercode_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_centercode_chosen > div > div > input[type=text]").send_keys("인피니트테스트")
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_centercode_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-search").click()
        # institution name click
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[2]/div/table/tbody/tr[1]/td[2]/a")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[2]/div/table/tbody/tr[1]/td[2]/a").click()
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#modifyCenterRuleLabel")))
        # modality check
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_center_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_center_chosen > div > div > input[type=text]").send_keys("인피니트")
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_center_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)

        if (msg != "수정하시겠습니까?" or
            no_msg != "Multi Reading Center Rule Modify" or
            yes_msg != "수정하였습니다." or 
            driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_center_chosen > a > span").text != "인피니트"):
            testResult = False
            Result_msg += "#4 "

        # left
        driver.find_element(By.CSS_SELECTOR, "#modify-multi-center-rule-center-remove-btn").click()
        if (one_remain == "not-allowed" or
            driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modify-save-btn").value_of_css_property("cursor") != "not-allowed"):
            testResult = False
            REesult_msg += "#5 "

        ## Change Save #8 #보류

        # Close #9
        # close
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modify-close-btn").click()
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#modifyCenterRuleLabel")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#selected_multi_center_rule_modify_center_chosen > a > span"), "인피니트테스트"))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#modifyCenterRuleLabel").get_property("textContent")
        # close
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modify-close-btn").click()
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#modifyCenterRuleLabel")))
        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-search")))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "#multi-reading-center-rule-tab-name").get_property("textContent")
        if (msg != "수정을 취소하시겠습니까?" or 
            no_msg != "Multi Reading Center Rule Modify" or 
            yes_msg != "Multi Reading Center Rule"):
            testResult = False
            Result_msg += "#9 "
        
        print("MultiReadingCenterRule_Modify")
        print(testResult)
        print(Result_msg)

        ## MultiReadingCenterRule_Modify결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "MultiReadingCenterRule_Modify Test Passed")

    def All():
        MultiReadingCenterRule.Add()
        MultiReadingCenterRule.Modify()
        MultiReadingCenterRule.Delete()


#GroupCode_Test
#ReportCode_Test
# Add > GroupAdd > GroupModify > Modify > Delete
class StandardReport:
    def GroupAdd():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # StandardReport
        driver.find_element(By.CSS_SELECTOR, "#standard-report-btn").click()
        driver.wait_for_request('.*/StandardReport.*')
        
        # None Select Group Add #1
        if driver.find_element(By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn.group-add-btn.disabled").value_of_css_property("cursor") != "not-allowed":
            testResult = False
            Result_msg += "#1 "

        # Find & Select
        check = False
        while(1):
            request = driver.wait_for_request('.*/GetStandardReportList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in data:
                if n["ReportCode"] == "ReportCode_Test":
                    check = True
                    num = data.index(n) + 1
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num)+"]/td[1]/label").click()
                    break

            if check == True:
                break

            del driver.requests
            time.sleep(0.1)
            try:
                driver.find_element(By.CSS_SELECTOR, "#standard-report-list_next > a").click()
            except:
                break

        # Group Add
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn.group-add-btn")))
        driver.find_element(By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn.group-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-group-add-close-btn")))
        
        # Input Group Code Save #2
        # input group code save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-add-group-code").send_keys("GroupCode_Test_re")
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-add-save-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        # no
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn.group-add-btn")))
        except:
            testResult = False
            Result_msg += "#2 "
        driver.find_element(By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn.group-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-group-add-close-btn")))
        # input group code save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-add-group-code").send_keys("GroupCode_Test_re")
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-add-save-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))

        del driver.requests
        time.sleep(0.1)

        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.15)
        if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "등록하였습니다.":
            testResult = False
            Result_msg += "#2 "
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        
        driver.wait_for_request('.*/StandardReport.*')

        # recovery
        # Find & Select
        check = False
        while(1):
            request = driver.wait_for_request('.*/GetStandardReportList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in data:
                if n["ReportCode"] == "ReportCode_Test":
                    check = True
                    num = data.index(n) + 1
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num)+"]/td[1]/label").click()
                    break

            if check == True:
                break

            del driver.requests
            time.sleep(0.1)
            try:
                driver.find_element(By.CSS_SELECTOR, "#standard-report-list_next > a").click()
            except:
                break
        # Group Add
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn.group-add-btn")))
        driver.find_element(By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn.group-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-group-add-close-btn")))
        # input group code save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-add-group-code").send_keys("GroupCode_Test")
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-add-save-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        del driver.requests
        time.sleep(0.1)
        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.15)
        if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "등록하였습니다.":
            testResult = False
            Result_msg += "#2 "
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        driver.wait_for_request('.*/StandardReport.*')

        # Click & Group Add
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr[1]/td[1]/label").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn.group-add-btn")))
        driver.find_element(By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn.group-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-group-add-close-btn")))

        # Close #3
        # close
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-add-close-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-group-add-close-btn")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[5]/div/div/div[1]/h3").get_property("textContent")
        #print(no_msg)
        # close
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-add-close-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn.group-add-btn")))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "#standard-report-tab-name").get_property("textContent")
        if (msg != "등록을 취소하시겠습니까?" or
            no_msg != "Standard Report Group Registration" or
            yes_msg != "Standard Report List"):
            testResult = False
            Result_msg += "#3 "

        print("StandardReport_GroupAdd")
        print(testResult)
        print(Result_msg)

        ## StandardReport_GroupAdd결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "StandardReport_GroupAdd Test Passed")

    def Add():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # StandardReport
        driver.find_element(By.CSS_SELECTOR, "#standard-report-btn").click()
        driver.wait_for_request('.*/StandardReport.*')
        
        del driver.requests

        # Add #1
        driver.find_element(By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a:nth-child(2) > span").click()
        driver.wait_for_request('.*/GetStandardReportCreatorID')
        if driver.find_element(By.CSS_SELECTOR, "#standard-report-add-creator").get_property("value") != admin_id:
            testResult = False
            Result_msg += "#1 "

        # Group Code, Modality, Report Code, Description, Hot Key, Report, Conclusion #2 3 5 6 7 8 9
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-group-code").send_keys("GroupCode_Test")
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-auto-expand").send_keys("CT")
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-add-auto-expand"), "CT"))
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-report-code").send_keys("ReportCode_Test")
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-add-report-code"), "ReportCode_Test"))
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-desc").send_keys("Description_Test")
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-add-desc"), "Description_Test"))
        driver.find_element(By.CSS_SELECTOR, "#standard_report_add_hotkey_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#standard_report_add_hotkey_chosen > div > ul > li:nth-child(37)").click()
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-report").send_keys("Report_Test123!@#")
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-conclusion").send_keys("Conclusion123!@#")
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-add-conclusion"), "Conclusion123!@#"))
        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[14]/div[7]/div/button"),"Yes"))
        msg = driver.find_element(By.XPATH, "/html/body/div[14]/h2").text
        # no
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-add-report-code"), "ReportCode_Test"))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#addStandartReportLabel").get_property("textContent")
        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[14]/div[7]/div/button"),"Yes"))
        del driver.requests

        ## yes
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[14]/div[7]/div/button"), "OK"))
        ok_msg = driver.find_element(By.XPATH, "/html/body/div[14]/h2").get_property("textContent")
        driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()

        check = False
        while(1):
            request = driver.wait_for_request('.*/GetStandardReportList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in data:
                if n["ReportCode"] == "ReportCode_Test":
                    check = True
                    num = data.index(n) + 1
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num)+"]/td[4]/a").click()
                    try:
                        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-desc"), "Description_Test"))
                        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#standard_report_modify_hotkey_chosen > a > span"), "Z"))
                        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-report"), "Report_Test123!@#"))
                        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-conclusion"), "Conclusion123!@#"))
                    except:
                        testResult = False
                        Result_msg += "#6 #7 #8 #9 "
                    driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-close-btn").click()
                    driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-close-btn").send_keys(Keys.ENTER)
                    WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.visible.showSweetAlert > div.sa-button-container > div > button"), "Yes"))
                    driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.visible.showSweetAlert > div.sa-button-container > div > button").click()
                    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num)+"]/td[4]/a")))
                    break

            if check == True:
                break

            del driver.requests
            time.sleep(0.1)
            try:
                driver.find_element(By.CSS_SELECTOR, "#standard-report-list_next > a").click()
            except:
                break

        if (no_msg != "Standard Report Registration" or 
            msg != "등록하시겠습니까?" or 
            ok_msg != "등록하였습니다." or 
            check == False):
            testResult = False
            Result_msg += "#2 #5 "
        

        del driver.requests
        time.sleep(0.25)
        # Add
        driver.find_element(By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a:nth-child(2) > span").click()
        driver.wait_for_request('.*/GetStandardReportCreatorID')

        # Alreay Report Code #4
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-report-code").send_keys("ReportCode_Test")
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-add-report-code"), "ReportCode_Test"))
        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[14]/div[7]/div/button"),"Yes"))
        msg = driver.find_element(By.XPATH, "/html/body/div[14]/h2").text
        # no
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-add-report-code"), "ReportCode_Test"))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#addStandartReportLabel").get_property("textContent")
        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[14]/div[7]/div/button"),"Yes"))
        # yes
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[14]/div[7]/div/button"), "OK"))
        yes_msg = driver.find_element(By.XPATH, "/html/body/div[14]/h2").get_property("textContent")
        # ok
        driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()
        result_msg = driver.find_element(By.CSS_SELECTOR, "#addStandartReportLabel").get_property("textContent")

        if (msg != "등록하시겠습니까?" or 
            no_msg != "Standard Report Registration" or 
            yes_msg != "등록을 실패하였습니다." or 
            result_msg != "Standard Report Registration"):
            testResult = False
            Result_msg += "#4 "

        # Close #10
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-close-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.visible.showSweetAlert > div.sa-button-container > div > button"), "Yes"))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-add-creator"), admin_id))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#addStandartReportLabel").get_property("textContent")
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-close-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.visible.showSweetAlert > div.sa-button-container > div > button"), "Yes"))
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr[1]/td[4]/a")))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "#standard-report-tab-name").get_property("textContent")
        if (msg != "등록을 취소하시겠습니까?" or 
            no_msg != "Standard Report Registration" or 
            yes_msg != "Standard Report List"):
            testResult = False
            Result_msg += "#10 "

        print("StandardReport_Add")
        print(testResult)
        print(Result_msg)

        ## StandardReport_Add결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "StandardReport_Add Test Passed")

    def Delete():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # StandardReport
        driver.find_element(By.CSS_SELECTOR, "#standard-report-btn").click()
        driver.wait_for_request('.*/StandardReport.*')
        
        # Non-Select Delete #1
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/div[1]/a[3]").value_of_css_property("cursor") != "not-allowed":
            testResult = False
            Result_msg += "#1 "

        # Select Delete #2
        # Find & Select
        check = False
        while(1):
            request = driver.wait_for_request('.*/GetStandardReportList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in data:
                if n["ReportCode"] == "ReportCode_Test":
                    check = True
                    num = data.index(n) + 1
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num)+"]/td[1]/label").click()
                    break

            if check == True:
                break

            del driver.requests
            time.sleep(0.1)
            try:
                driver.find_element(By.CSS_SELECTOR, "#standard-report-list_next > a").click()
            except:
                break
        # Delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/div[1]/a[3]").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.delete-btn")))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#standard-report-tab-name").get_property("textContent")
        # Delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/div[1]/a[3]").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        del driver.requests
        time.sleep(0.1)
        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a:nth-child(2)")))

        # additional delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num+1)+"]/td[1]/label").click()
        driver.find_element(By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.delete-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-btn")))

        # 패킷으로 지움확인
        check = False
        request = driver.wait_for_request('.*/GetStandardReportList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        for a in range(1, total+1):
            request = driver.wait_for_request('.*/GetStandardReportList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in data:
                if n["ReportCode"] == "ReportCode_Test":
                    check = True
                    break

            if check == True:
                break
            
            del driver.requests
            time.sleep(0.1)

            if a == total:
                break
            driver.find_element(By.CSS_SELECTOR, "#standard-report-list_next > a").click()

        if (msg != "삭제하시겠습니까?" or 
            no_msg != "Standard Report List" or 
            yes_msg != "삭제하였습니다." or 
            check == True):
            testResult= False
            Result_msg += "#2 "

        # StandardReport
        driver.find_element(By.CSS_SELECTOR, "#standard-report-btn").click()
        request = driver.wait_for_request('.*/GetStandardReportList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        
        # Select & Other Tab #3
        if total < 2:
            testResult = False
            Result_msg += "#3 "
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr[1]/td[1]/label").click()
        del driver.requests
        time.sleep(0.1)
        driver.find_element(By.CSS_SELECTOR, "#standard-report-list_next > a").click()
        driver.wait_for_request('.*/StandardReport.*')
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/div[1]/a[3]").value_of_css_property("cursor") != "not-allowed":
            testResult = False
            Result_msg += "#3 "

        # Select at >= 2 & Other Tab #4
        if total < 3:
            testResult = False
            Result_msg += "#4 "
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr[1]/td[1]/label").click()
        del driver.requests
        time.sleep(0.1)
        driver.find_element(By.CSS_SELECTOR, "#standard-report-list_next > a").click()
        driver.wait_for_request('.*/StandardReport.*')
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/div[1]/a[3]").value_of_css_property("cursor") != "not-allowed":
            testResult = False
            Result_msg += "#4 "

        print("StandardReport_Delete")
        print(testResult)
        print(Result_msg)

        ## StandardReport_Delete결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "StandardReport_Delete Test Passed")

    # ReportCode_Test Search
    def ReportSearch(total):
        num = 0
        for a in range(1, total+1):
            request = driver.wait_for_request('.*/GetStandardReportList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in data:
                if n["ReportCode"] == "ReportCode_Test":
                    num = data.index(n) + 1
                    break

            if num != 0:
                break
            
            del driver.requests
            time.sleep(0.1)

            if a == total:
                break
            driver.find_element(By.CSS_SELECTOR, "#standard-report-list_next > a").click()

        return num


    def GroupModify():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        del driver.requests

        # StandardReport
        driver.find_element(By.CSS_SELECTOR, "#standard-report-btn").click()
        request = driver.wait_for_request('.*/GetStandardReportList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        # ReportCode_Test Search
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        num = StandardReport.ReportSearch(total)

        # Group Code Click #1
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num)+"]/td[3]/a").click()
        try:
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[6]/div/div/div[1]/h3"), "Standard Report Group Modify"))
        except:
            testResult = False
            Result_msg += "#1 "

        # Group Code Change #2
        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-modify-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # no
        time.sleep(0.1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-btn")))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#standard-report-tab-name").get_property("textContent")
        # Group Code Click
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num)+"]/td[3]/a").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[6]/div/div/div[1]/h3"), "Standard Report Group Modify"))
        # input
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-modify-group-code").send_keys("_re")
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-group-modify-group-code"), "GroupCode_Test_re"))
        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-modify-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))

        del driver.requests
        time.sleep(0.1)

        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-btn")))

        # ReportCode_Test Search
        num = StandardReport.ReportSearch(total)

        if (msg != "기존 Standard Report Group Code로 수정하시겠습니까?" or 
            no_msg != "Standard Report List" or 
            yes_msg != "수정하였습니다." or 
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num)+"]/td[3]/a").get_property('textContent') != "GroupCode_Test_re"):
            testResult = False
            Result_msg += "#2 "

        # additional report for total check
        driver.find_element(By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a:nth-child(2) > span").click()
        driver.wait_for_request('.*/GetStandardReportCreatorID')
        # input
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-group-code").send_keys("GroupCode_Test_re")
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-report-code").send_keys("ReportCode_Test2")
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-add-report-code"), "ReportCode_Test"))
        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[14]/div[7]/div/button"),"Yes"))
        del driver.requests
        time.sleep(0.1)
        ## yes
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[14]/div[7]/div/button"), "OK"))
        driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()

        request = driver.wait_for_request('.*/GetStandardReportList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        # ReportCode_Test Search
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        num = StandardReport.ReportSearch(total)

        # Total Check #3
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num)+"]/td[3]/a").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[6]/div/div/div[1]/h3"), "Standard Report Group Modify"))
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-modify-popup-modal > div > div > div.modal-body > div:nth-child(2) > div > div > label").click()
        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-modify-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # no
        time.sleep(0.1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-btn")))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#standard-report-tab-name").get_property("textContent")
        # Group Code Click
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num)+"]/td[3]/a").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[6]/div/div/div[1]/h3"), "Standard Report Group Modify"))
        # input
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-modify-group-code").send_keys("_total")
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-modify-popup-modal > div > div > div.modal-body > div:nth-child(2) > div > div > label").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-group-modify-group-code"), "GroupCode_Test_re"))
        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-modify-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))

        del driver.requests
        time.sleep(0.1)

        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-btn")))

        # ReportCode_Test Search
        num = StandardReport.ReportSearch(total)
        if (msg != "기존 Standard Report Group Code로 모두 수정하시겠습니까?" or 
            no_msg != "Standard Report List" or 
            yes_msg != "수정하였습니다." or 
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num)+"]/td[3]/a").get_property('textContent') != "GroupCode_Test_re_total" or
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num+1)+"]/td[3]/a").get_property('textContent') != "GroupCode_Test_re_total"):
            testResult = False
            Result_msg += "#3 "

        # Close #4
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num)+"]/td[3]/a").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#standard-report-group-modify-close-btn"), "Close"))
        # close
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-modify-close-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # no
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-group-modify-group-code"), "GroupCode_Test"))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[6]/div/div/div[1]/h3").get_property("textContent")
        # close
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-modify-close-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        # yes
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-btn")))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "#standard-report-tab-name").get_property("textContent")
        if (msg != "수정을 취소하시겠습니까?" or 
            no_msg != "Standard Report Group Modify" or 
            yes_msg != "Standard Report List"):
            testResult = False
            Result_msg += "#4 "

        print("StandardReport_GroupModify")
        print(testResult)
        print(Result_msg)

        ## StandardReport_GroupModify결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "StandardReport_GroupModify Test Passed")

    def Modify():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # StandardReport
        driver.find_element(By.CSS_SELECTOR, "#standard-report-btn").click()
        request = driver.wait_for_request('.*/GetStandardReportList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        
        num = StandardReport.ReportSearch(total)

        # Report Code Click #1
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num+1)+"]/td[4]/a").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-creator"), admin_id))
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[4]/div/div/div[1]/h3").get_property("textContent") != "Standard Report Modify":
            testResult = False
            Result_msg += "#1 "

        # Group Code, Description, Hot Key, Report, Conclusion #2 6 7 8 9
        driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-group-code").send_keys("_re")
        driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-desc").send_keys("Description_Test")
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-desc"), "Description_Test"))
        driver.find_element(By.CSS_SELECTOR, "#standard_report_modify_hotkey_chosen").click()
        driver.find_element(By.CSS_SELECTOR, "#standard_report_modify_hotkey_chosen > div > ul > li:nth-child(37)").click()
        driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-report").send_keys("Report_Test123!@#")
        driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-conclusion").send_keys("Conclusion123!@#")
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-conclusion"), "Conclusion123!@#"))
        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # no
        time.sleep(0.1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-creator"), admin_id))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[4]/div/div/div[1]/h3").get_property("textContent")
        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        ok_msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a:nth-child(2)")))

        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num+1)+"]/td[4]/a").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-creator"), admin_id))
        if (msg != "수정하시겠습니까?" or 
            no_msg != "Standard Report Modify" or 
            ok_msg != "수정하였습니다." or 
            driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-group-code").get_property("value") != "GroupCode_Test_re_total_re"):
            testResult = False
            Result_msg += "#2 "
        if driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-desc").get_property("value") != "Description_Test":
            testResult = False
            Result_msg += "#6 "
        if driver.find_element(By.CSS_SELECTOR, "#standard_report_modify_hotkey_chosen > a > span").get_property("textContent") != "Z":
            testResult = False
            Result_msg += "#7 "
        if driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-report").get_property("value") != "Report_Test123!@#":
            testResult = False
            Result_msg += "#8 "
        if driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-conclusion").get_property("value") != "Conclusion123!@#":
            testResult = False
            Result_msg += "#9 "

        # alreay Report Code #4
        driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-report-code").clear()
        driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-report-code").send_keys("ReportCode_Test")
        # save
        element = driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-save-btn")
        driver.execute_script("arguments[0].click()",element)
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # no
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-creator"), admin_id))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[4]/div/div/div[1]/h3").get_property("textContent")
        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        # yes
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # ok
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-modify-save-btn")))
        if (msg != "수정하시겠습니까?" or 
            no_msg != "Standard Report Modify" or 
            yes_msg != "수정을 실패하였습니다." or 
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[4]/div/div/div[1]/h3").get_property("textContent") != "Standard Report Modify"):
            testResult = False
            Result_msg += "#4 "

        time.sleep(0.25)
        # new #5
        driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-report-code").send_keys("3")
        # save
        element = driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-save-btn")
        driver.execute_script("arguments[0].click()",element)
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # no
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-creator"), admin_id))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[4]/div/div/div[1]/h3").get_property("textContent")
        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        # yes
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a:nth-child(2)")))
        if (msg != "수정하시겠습니까?" or 
            no_msg != "Standard Report Modify" or 
            yes_msg != "수정하였습니다." or 
            driver.find_element(By.CSS_SELECTOR, "#standard-report-tab-name").get_property("textContent") != "Standard Report List"):
            testResult = False
            Result_msg += "#5 "

        # Close #10
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num+1)+"]/td[4]/a").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-creator"), admin_id))
        # close
        element = driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-close-btn")
        driver.execute_script("arguments[0].click()",element)
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # no
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-modify-close-btn")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[4]/div/div/div[1]/h3").get_property("textContent")
        # close
        time.sleep(0.25)
        element = driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-close-btn")
        driver.execute_script("arguments[0].click()",element)
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a:nth-child(2)")))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "#standard-report-tab-name").get_property("textContent")
        if (msg != "수정을 취소하시겠습니까?" or 
            no_msg != "Standard Report Modify" or 
            yes_msg != "Standard Report List"):
            testResult = False
            Result_msg += "#10 "

        print("StandardReport_Modify")
        print(testResult)
        print(Result_msg)

        ## StandardReport_Modify결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "StandardReport_Modify Test Passed")
    
    def All():
        StandardReport.Add()
        StandardReport.GroupAdd()
        StandardReport.GroupModify()
        StandardReport.Modify()
        StandardReport.Delete()

class Institution:
    def insti_idx_find(target):
        # Find
        request = driver.wait_for_request('.*/GetInstitutionsList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        idx = 0
        check = False
        for a in range(0, total):
            request = driver.wait_for_request('.*/GetInstitutionsList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in data:
                if n["InstitutionName"] == target:
                    idx = data.index(n) + 1
                    check = True
                    break
            if check == True:
                break
            del driver.requests
            time.sleep(0.1)
            driver.find_element(By.CSS_SELECTOR, "#institutions-list_next > a").click()

        return idx

    def SearchFilter():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # Institution
        driver.find_element(By.CSS_SELECTOR, "#institutions-btn").click()
        driver.wait_for_request('.*/GetInstitutionsList.*')

        del driver.requests
        time.sleep(0.1)
        
        driver.find_element(By.CSS_SELECTOR, "#institutions-search-institution-code").send_keys(search_institution_code)
        driver.find_element(By.CSS_SELECTOR, "#institutions-search").click()

        request = driver.wait_for_request('.*/GetInstitutionsList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        check = True
        num = 0
        for n in data:
            if search_institution_code not in n["InstitutionCode"]:
                check = False

            num += 1
            if (driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(2)").text != n["InstitutionCode"] or
                driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(3)").text != n["InstitutionName"] or 
                driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(4)").text != n["CenterCodeList"] or 
                driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(5)").text != n["ReportModificationMode"] or 
                driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(6)").text != str(n["ReportingRuleCount"]) or
                driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(7)").text != n["ReportingDownloadDelayTime"]):
                check = False

            if check == False:
                testResult = False
                Result_msg += "#1 "
                break

        print("SearchFilter_InstitutionCode")
        print(testResult)
        print(Result_msg)

        ## SearchFilter_InstitutionCode결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "SearchFilter_InstitutionCode Test Passed")

        testResult = True
        Result_msg = "failed at "

        del driver.requests
        time.sleep(0.1)
        

        driver.find_element(By.CSS_SELECTOR, "#institutions-search-institution-code").clear()
        driver.find_element(By.CSS_SELECTOR, "#institutions-search-institution-name").send_keys(search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#institutions-search").click()

        request = driver.wait_for_request('.*/GetInstitutionsList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        check = True
        num = 0
        for n in data:
            if search_institution_code not in n["InstitutionCode"]:
                check = False

            num += 1
            if (driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(2)").text != n["InstitutionCode"] or
                driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(3)").text != n["InstitutionName"] or 
                driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(4)").text != n["CenterCodeList"] or 
                driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(5)").text != n["ReportModificationMode"] or 
                driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(6)").text != str(n["ReportingRuleCount"]) or
                driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(7)").text != n["ReportingDownloadDelayTime"]):
                check = False

            if check == False:
                testResult = False
                Result_msg += "#1 "
                breakrequest = driver.wait_for_request('.*/GetInstitutionsList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        check = True
        num = 0
        for n in data:
            if search_institution_code not in n["InstitutionCode"]:
                check = False

            num += 1
            if (driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(2)").text != n["InstitutionCode"] or
                driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(3)").text != n["InstitutionName"] or 
                driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(4)").text != n["CenterCodeList"] or 
                driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(5)").text != n["ReportModificationMode"] or 
                driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(6)").text != str(n["ReportingRuleCount"]) or
                driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(num)+") > td:nth-child(7)").text != n["ReportingDownloadDelayTime"]):
                check = False

            if check == False:
                testResult = False
                Result_msg += "#2 "
                break

        print("SearchFilter_InstitutionName")
        print(testResult)
        print(Result_msg)

        ## SearchFilter_InstitutionName결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "SearchFilter_InstitutionName Test Passed")

    def Add():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # Institution
        driver.find_element(By.CSS_SELECTOR, "#institutions-btn").click()
        driver.wait_for_request('.*/GetInstitutionsList.*')
        
        # Add #1
        driver.find_element(By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[3]/div/div/div[1]/h3")))
            assert(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[3]/div/div/div[1]/h3").text == "Institutions Registration")
        except:
            testResult = False
            Result_msg += "#1 "

        if testResult == True:
            # None input Save Yes #2
            # save
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-save-btn").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            try:
                WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2"),"Institution Code를 입력해주세요."))
            except:
                testResult = False
                Result_msg += "#2 "
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-add-save-btn")))
                

            # Institution Code input #3 4
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-institution-code").send_keys("123456")
 
            # save
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-save-btn").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            try:
                WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2"),"Institution Name를 입력해주세요."))
            except:
                testResult = False
                if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2") == "Exist검사 중 문제가 발생하였습니다.":
                    Result_msg += "#3 "
                else:
                    Result_msg += "#4 "
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-add-save-btn"))) 
            
            # Already Institution Code #5
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-institution-code").clear()
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-institution-code").send_keys(search_institution_code)

            # save
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-save-btn").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            try:
                WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2"),"이미 동일한 내용이 존재합니다."))
            except:
                testResult = False
                Result_msg += "#5 "
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-add-save-btn"))) 

            # Center #6
            driver.find_element(By.CSS_SELECTOR, "#institutions_add_center_code_list_chosen > ul > li > input[type=text]").click()
            driver.find_element(By.CSS_SELECTOR, "#institutions_add_center_code_list_chosen > ul > li > input[type=text]").send_keys(search_center)
            driver.find_element(By.CSS_SELECTOR, "#institutions_add_center_code_list_chosen > ul > li > input[type=text]").send_keys(Keys.ENTER)
            try:
                WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#institutions_add_center_code_list_chosen > ul > li.search-choice > span"),search_center))
            except:
                testResult = False
                Result_msg += "#6 "

            # Center X #7
            if "#6" not in Result_msg:
                driver.find_element(By.CSS_SELECTOR, "#institutions_add_center_code_list_chosen > ul > li.search-choice > a").click()
                try:
                    WebDriverWait(driver, 0.5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#institutions_add_center_code_list_chosen > ul > li.search-choice > span"),search_center))
                    testResult = False
                    Result_msg += "#7 "
                except:
                    pass
            
            # input Institution Name
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-institution-code").clear()
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-institution-code").send_keys("123456")
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-institution-name").send_keys("Cloud_ITRTest")

            del driver.requests
            time.sleep(0.1)

            # Save #15
            # save
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-save-btn").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            # no
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[3]/div/div/div[1]/h3")))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[3]/div/div/div[1]/h3").text
            # save
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-save-btn").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            try:
                assert((msg == "등록하시겠습니까?") and (no_msg == "Institutions Registration"))
                WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2"),"등록하였습니다."))
            except:
                testResult = False
                Result_msg += "#15 "
            # ok
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn"))) 

            if "#15" not in Result_msg:
                request = driver.wait_for_request('.*/GetInstitutionsList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)
                total = math.ceil(data["recordsFiltered"] / data["Length"])

                check = False
                for a in range(0, total):
                    request = driver.wait_for_request('.*/GetInstitutionsList.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]

                    for n in data:
                        if n["InstitutionName"] == "Cloud_ITRTest":
                            if driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(data.index(n)+1)+") > td:nth-child(3)").text == "Cloud_ITRTest":
                                check = True
                            break
                    if check == True:
                        break
                    del driver.requests
                    time.sleep(0.1)
                    driver.find_element(By.CSS_SELECTOR, "#institutions-list_next > a").click()

                if check== False:
                    testResult = False
                    Result_msg += "#15 "

            # Close #14
            # add
            driver.find_element(By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[3]/div/div/div[1]/h3")))
            # close
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-close-btn").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            # no
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-add-close-btn")))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[3]/div/div/div[1]/h3").text
            # close
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-close-btn").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            #WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
            try:
                assert((msg == "등록을 취소하시겠습니까?")and(no_msg == "Institutions Registration"))
                WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#institutions-tab-name"),"Institution List"))
            except:
                testResult = False
                Result_msg += "#14 "

        print("Institution_Add")
        print(testResult)
        print(Result_msg)

        ## Institution_Add결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "Institution_Add Test Passed")

    # Cloud_ITRTest
    def Delete():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # Institution
        driver.find_element(By.CSS_SELECTOR, "#institutions-btn").click()
        driver.wait_for_request('.*/GetInstitutionsList.*')
        
        # None Selecet Delete #1
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
            testResult = False
            Result_msg += "#1 "

        # Select Delete #2
        request = driver.wait_for_request('.*/GetInstitutionsList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        check = False
        for a in range(0, total):
            request = driver.wait_for_request('.*/GetInstitutionsList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in data:
                if n["InstitutionName"] == "Cloud_ITRTest":
                    if driver.find_element(By.CSS_SELECTOR, "#institutions-list > tbody > tr:nth-child("+str(data.index(n)+1)+") > td:nth-child(3)").text == "Cloud_ITRTest":
                        check = True
                        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(data.index(n)+1)+"]/td[1]/label").click()
                    break
            if check == True:
                break
            del driver.requests
            time.sleep(0.1)
            driver.find_element(By.CSS_SELECTOR, "#institutions-list_next > a").click()
        # delete
        driver.find_element(By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.delete-btn").click()
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.delete-btn")))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#institutions-tab-name").text
        # delete
        driver.find_element(By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.delete-btn").click()
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

        del driver.requests
        time.sleep(0.1)

        # yes
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        try:
            assert((msg == "삭제하시겠습니까?") and (no_msg == "Institution List"))
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2"), "삭제하였습니다."))
        except:
            testResult = False
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
        if "#2 " not in Result_msg:
            request = driver.wait_for_request('.*/GetInstitutionsList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"] / data["Length"])

            check = False
            for a in range(0, total):
                request = driver.wait_for_request('.*/GetInstitutionsList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["InstitutionName"] == "Cloud_ITRTest":
                        testResult = False
                        Result_msg += "#2 "
                        check = True    
                        break
                if check == True:
                    break
                del driver.requests
                time.sleep(0.1)
                driver.find_element(By.CSS_SELECTOR, "#institutions-list_next > a").click()

        # Institution
        driver.find_element(By.CSS_SELECTOR, "#institutions-btn").click()
        request = driver.wait_for_request('.*/GetInstitutionsList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        if total < 2:
            testResult = False
            Result_msg += "#3 #4 "

        if ("#3" not in Result_msg) and ("#4" not in Result_msg):
            # Select & Other Tab #3
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr[1]/td[1]/label").click()

            del driver.requests
            time.sleep(0.1)

            driver.find_element(By.CSS_SELECTOR, "#institutions-list_next > a").click()
            driver.wait_for_request('.*/GetInstitutionsList.*')

            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
                testResult = False
                Result_msg += "#3 "

            # Select at 2> & Other Tab #4
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr[1]/td[1]/label").click()

            del driver.requests
            time.sleep(0.1)

            driver.find_element(By.CSS_SELECTOR, "#institutions-list_previous > a").click()
            driver.wait_for_request('.*/GetInstitutionsList.*')

            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
                testResult = False
                Result_msg += "#4 "

        print("Institution_Delete")
        print(testResult)
        print(Result_msg)

        ## Institution_Delete결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "Institution_Delete Test Passed")

    def Modify_ToWL(RM_num, RM, RDT_num, RDT):
        Result_msg = ""
        time.sleep(1)

        # report mode - None
        driver.find_element(By.CSS_SELECTOR, "#institutions_modify_report_mode_chosen").click()
        #driver.execute_script("arguments[0].click()",element)
        driver.find_element(By.CSS_SELECTOR, "#institutions_modify_report_mode_chosen > div > ul > li:nth-child("+str(RM_num)+")").click()

        # report delay time - None
        driver.find_element(By.CSS_SELECTOR, "#institutions_modify_report_time_chosen").click()
        driver.find_element(By.CSS_SELECTOR, "#institutions_modify_report_time_chosen > div > ul > li:nth-child("+str(RDT_num)+")").click()

        del driver.requests

        # save
        driver.find_element(By.CSS_SELECTOR, "#institutions-modify-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), search_institution_3))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[1]/h3").get_property("textContent")
        # save
        driver.find_element(By.CSS_SELECTOR, "#institutions-modify-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
        
        # 새로운 탭 + 전환
        driver.execute_script("window.open()")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(WorklistUrl);
        driver.implicitly_wait(5)
        wk_login(wk_id, wk_pw)

        # search hospital
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > a").click()
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > div > div > input[type=text]").send_keys(search_institution_3)
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#current-hospital-name"), search_institution_3))
        
        # set job report
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > i").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#setting-columns-apply")))
        if driver.find_element(By.CSS_SELECTOR, "#chk-column-5").get_property("checked") == False:
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(5) > label").click()
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()
        time.sleep(0.25)
        num = 0
        while(1):
            try:
                num += 1
                if driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[1]/div/table/thead/tr/th["+str(num)+"]").get_property("textContent") == "Job Report":
                   break
            except:
                Result_msg += "worklist setting "
                return Result_msg
         
        driver.find_element(By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[2]/div/div[4]/div[2]/table/tbody/tr[1]/td["+str(num)+"]/span/label").click()
        # 탭 전환
        driver.switch_to.window(driver.window_handles[2])
        driver.implicitly_wait(5)
        driver.wait_for_request(".*/GetJobReport.*")
        
        if RM_num != 1:
            if RM not in driver.find_element(By.CSS_SELECTOR, "#job-report-view-report-mode").get_property("textContent"):
                Result_msg += "#6 "
        else:
            if "" != driver.find_element(By.CSS_SELECTOR, "#job-report-view-report-mode").get_property("textContent"):
                Result_msg += "#6 "
        if RDT not in driver.find_element(By.CSS_SELECTOR, "#job-report-view-delaytime").get_property("textContent"):
            Result_msg += "#7 "

        if (Result_msg != "" or 
            msg != "수정하시겠습니까?" or 
            no_msg != "Institutions Modify"):
            Result_msg += "#13 "

        driver.close()
        driver.switch_to.window(driver.window_handles[1])

        driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout").click()
        driver.implicitly_wait(5)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        return Result_msg
        

    def Modify():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # Institution
        driver.find_element(By.CSS_SELECTOR, "#institutions-btn").click()
        driver.wait_for_request('.*/GetInstitutionsList.*')
        
        # Find
        idx = Institution.insti_idx_find(search_institution_3)
        
        # Select Institution Code #1
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), search_institution_3))
        try:
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), search_institution_3))
            assert(driver.find_element(By.CSS_SELECTOR, "#institutions-modify-institution-code").get_property("value") == search_institution_code)
        except:
            testResult = False
            Result_msg += "#1 "

        if "#1" not in Result_msg:
            # Change Institution Code #2
            if driver.find_element(By.CSS_SELECTOR, "#institutions-modify-institution-code").value_of_css_property("cursor") != "not-allowed":
                testResult = False
                Result_msg += "#2 "

            # Change Institution Name #3
            driver.find_element(By.CSS_SELECTOR, "#institutions-modify-institution-name").send_keys("_re")
            time.sleep(0.25)
            # save
            driver.find_element(By.CSS_SELECTOR, "#institutions-modify-save-btn").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            # no
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), search_institution_3+"_re"))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[1]/h3").get_property("textContent")
            # save
            driver.find_element(By.CSS_SELECTOR, "#institutions-modify-save-btn").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(0.1)

            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
            # find
            idx = Institution.insti_idx_find(search_institution_3+"_re")
            if (idx == 0 or 
                msg != "수정하시겠습니까?" or 
                no_msg != "Institutions Modify") :
                testResult = False
                Result_msg += "#3 "

            # Select Institution Code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), search_institution_3))
            driver.find_element(By.CSS_SELECTOR, "#institutions-modify-institution-name").clear()
            driver.find_element(By.CSS_SELECTOR, "#institutions-modify-institution-name").send_keys(search_institution_3)

            time.sleep(1)#
            # Center X #5
            temp = driver.find_element(By.CSS_SELECTOR, "#institutions_modify_center_code_list_chosen > ul > li:nth-child(1) > span").get_property("textContent")
            driver.find_element(By.CSS_SELECTOR, "#institutions_modify_center_code_list_chosen > ul > li:nth-child(1) > a").click()
            if temp == driver.find_element(By.CSS_SELECTOR, "#institutions_modify_center_code_list_chosen > ul > li:nth-child(1) > span").get_property("textContent"):
                testResult = False
                Result_msg += "#5 "

            # Center Select #4
            driver.find_element(By.CSS_SELECTOR, "#institutions_modify_center_code_list_chosen > ul > li.search-field > input[type=text]").send_keys(temp)
            driver.find_element(By.CSS_SELECTOR, "#institutions_modify_center_code_list_chosen > ul > li.search-field > input[type=text]").send_keys(Keys.ENTER)
            num = 0
            while(1):
                try:
                    num+=1
                    select_check = driver.find_element(By.CSS_SELECTOR, "#institutions_modify_center_code_list_chosen > ul > li:nth-child("+str(num)+") > span").get_property("textContent")
                except:
                    break
            if temp != select_check:
                testResult = False
                Result_msg += "#4 "

            # Report Mode, Delay Time, Save #6 7 13
            ori_RM = driver.find_element(By.CSS_SELECTOR, "#institutions_modify_report_mode_chosen > a > span").text
            ori_RDT = driver.find_element(By.CSS_SELECTOR, "#institutions_modify_report_time_chosen > a > span").text
            ori_comment = driver.find_element(By.CSS_SELECTOR, "#institutions-modify-use-referring-comment2").get_property("checked")
            ori_revised = driver.find_element(By.CSS_SELECTOR, "#institutions-modify-enable-revised").get_property("checked")
            ori_discard = driver.find_element(By.CSS_SELECTOR, "#institutions-modify-enable-discard").get_property("checked")
            ori_request = driver.find_element(By.CSS_SELECTOR, "#institutions-modify-enable-request").get_property("checked") 

            driver.find_element(By.CSS_SELECTOR, "#institutions-modify-institution-name").send_keys("")

            temp = Institution.Modify_ToWL(1, "", 1, "0분")
            if temp != "":
                testResult= False
                Result_msg += temp

            # Find
            idx = Institution.insti_idx_find(search_institution_3)
        
            # select institution code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), search_institution_3))

            temp = Institution.Modify_ToWL(2, "Overwrite", 2, "30분")
            if temp != "":
                testResult= False
                Result_msg += temp

            # Find
            idx = Institution.insti_idx_find(search_institution_3)
        
            # select institution code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), search_institution_3))

            temp = Institution.Modify_ToWL(3, "Addendum", 3, "60분")
            if temp != "":
                testResult= False
                Result_msg += temp

            # Find
            idx = Institution.insti_idx_find(search_institution_3)
        
            # select institution code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), search_institution_3))

            temp = Institution.Modify_ToWL(4, "Prohibition", 4, "120분")
            if temp != "":
                testResult= False
            Result_msg += temp 

            # Find
            idx = Institution.insti_idx_find(search_institution_3)
        
            # select institution code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), search_institution_3))

            temp = Institution.Modify_ToWL(4, "Prohibition", 5, "180분")
            if temp != "":
                testResult= False
                Result_msg += temp 

            # Find
            idx = Institution.insti_idx_find(search_institution_3)
        
            # select institution code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), search_institution_3))

            # Comment, Revised, Discard, Request  #8 9 10 11
            # comment - check
            if ori_comment == driver.find_element(By.CSS_SELECTOR, "#institutions-modify-use-referring-comment2").get_property("checked") == False:
                driver.find_element(By.CSS_SELECTOR, "#not-use-default-refer-comment > div:nth-child(6) > div > div > label").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#institution-modify-refer-comment-select-box > li > span"), "+ Create New Comment"))

            del driver.requests
            time.sleep(0.25)

            driver.find_element(By.CSS_SELECTOR, "#institution-modify-refer-comment-select-box > li").click()
            request = driver.wait_for_request(".*/LoadReferringComments")
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[2]/div/div[2]/ul/li["+str(len(data)+1)+"]").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institution-modify-refer-comment-title"), "New Refer Comment"))
            driver.find_element(By.CSS_SELECTOR, "#institution-modify-refer-comment-title").clear()
            driver.find_element(By.CSS_SELECTOR, "#institution-modify-refer-comment-title").send_keys("test_comment")
            driver.find_element(By.CSS_SELECTOR, "#institution-modify-refer-comment-text").send_keys("test_comment")
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institution-modify-refer-comment-text"), "test_comment"))
            driver.find_element(By.CSS_SELECTOR, "#modify-institution-refer-comment-confirm-btn").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[2]/div/div[2]/ul/li["+str(len(data)+1)+"]").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institution-modify-refer-comment-title"), "test_comment"))
            driver.find_element(By.CSS_SELECTOR, "#modify-institution-refer-comment-set-default-btn").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # revised - check
            if ori_revised == driver.find_element(By.CSS_SELECTOR, "#institutions-modify-enable-revised").get_property("checked") == False:
                driver.find_element(By.CSS_SELECTOR, "#not-use-default-refer-comment > div:nth-child(7) > div > div > label").click()

            # discard - check
            if ori_discard == driver.find_element(By.CSS_SELECTOR, "#institutions-modify-enable-discard").get_property("checked") == False:
                driver.find_element(By.CSS_SELECTOR, "#not-use-default-refer-comment > div:nth-child(8) > div > div > label").click()

            # request - check
            if ori_request == driver.find_element(By.CSS_SELECTOR, "#institutions-modify-enable-request").get_property("checked") == False:
                driver.find_element(By.CSS_SELECTOR, "#not-use-default-refer-comment > div:nth-child(9) > div > div > label").click()

            # save
            driver.find_element(By.CSS_SELECTOR, "#institutions-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))

            del driver.requests
            time.sleep(0.5)
            
            # refer
            driver.find_element(By.CSS_SELECTOR, "#tab-refer > a").click()
            driver.wait_for_request(".*/GetReferCountsByInstitution.*")

            del driver.requests
            time.sleep(0.5)

            driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > div > div > input[type=text]").send_keys(search_institution_2)
            driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            driver.wait_for_request(".*/GetAllAssignedList.*")

            del driver.requests
            time.sleep(0.5)
            
            driver.find_element(By.CSS_SELECTOR, "#tab_all_list > a").click()
            driver.wait_for_request(".*/GetAllList.*")

            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div[2]/table/tbody/tr[1]/td[1]/label").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#refer_tab > div > div:nth-child(4) > div > div.p-t-15 > div.row > div:nth-child(2) > button.btn.bg-purple.btn-xs.waves-effect.refer-btn")))
            driver.find_element(By.CSS_SELECTOR, "#refer_tab > div > div:nth-child(4) > div > div.p-t-15 > div.row > div:nth-child(2) > button.btn.bg-purple.btn-xs.waves-effect.refer-btn").click()
            try:
                WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#refer-comments"), "test_comment"))
            except:
                testResult = False
                Result_msg += "#8 "
            driver.find_element(By.CSS_SELECTOR, "#refer-close").click()
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#refer-revised-btn > span")))
            except:
                testResult = False
                Result_msg += "#9 "
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#refer-discard-btn > span")))
            except:
                testResult = False
                Result_msg += "#10 "
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#refer-retry-btn > span")))
            except:
                testResult = False
                Result_msg += "#11 "

            del driver.requests
            time.sleep(0.25)

            # Configuration
            driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
            driver.implicitly_wait(5)

            # Institution
            driver.find_element(By.CSS_SELECTOR, "#institutions-btn").click()
            driver.wait_for_request('.*/GetInstitutionsList.*')

            # Find
            idx = Institution.insti_idx_find(search_institution_3)

            del driver.requests
            time.sleep(0.25)
        
            # select institution code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), search_institution_3))

            # delete comment
            driver.wait_for_request(".*/LoadReferringComments")
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[2]/div/div[2]/ul/li[2]/button").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # comment -ucheck
            driver.find_element(By.CSS_SELECTOR, "#not-use-default-refer-comment > div:nth-child(6) > div > div > label").click()
            # revised - uncheck
            driver.find_element(By.CSS_SELECTOR, "#not-use-default-refer-comment > div:nth-child(7) > div > div > label").click()
            # discard - uncheck
            driver.find_element(By.CSS_SELECTOR, "#not-use-default-refer-comment > div:nth-child(8) > div > div > label").click()
            # request - uncheck
            driver.find_element(By.CSS_SELECTOR, "#not-use-default-refer-comment > div:nth-child(9) > div > div > label").click()

            # save
            driver.find_element(By.CSS_SELECTOR, "#institutions-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))

            del driver.requests
            time.sleep(0.5)
            
            # refer
            driver.find_element(By.CSS_SELECTOR, "#tab-refer > a").click()
            driver.wait_for_request(".*/GetReferCountsByInstitution.*")

            del driver.requests
            time.sleep(0.5)

            driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > div > div > input[type=text]").send_keys(search_institution_2)
            driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            driver.wait_for_request(".*/GetAllAssignedList.*")

            del driver.requests
            time.sleep(0.5)
            
            driver.find_element(By.CSS_SELECTOR, "#tab_all_list > a").click()
            driver.wait_for_request(".*/GetAllList.*")

            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div[2]/table/tbody/tr[1]/td[1]/label").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#refer_tab > div > div:nth-child(4) > div > div.p-t-15 > div.row > div:nth-child(2) > button.btn.bg-purple.btn-xs.waves-effect.refer-btn")))
            driver.find_element(By.CSS_SELECTOR, "#refer_tab > div > div:nth-child(4) > div > div.p-t-15 > div.row > div:nth-child(2) > button.btn.bg-purple.btn-xs.waves-effect.refer-btn").click()
            try:
                WebDriverWait(driver, 0.5).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#refer-comments"), "test_comment"))
                testResult = False
                Result_msg += "#8 "
            except:
                pass
            driver.find_element(By.CSS_SELECTOR, "#refer-close").click()
            try:
                WebDriverWait(driver, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#refer-revised-btn > span")))
                testResult = False
                Result_msg += "#9 "
            except:
                pass
            try:
                WebDriverWait(driver, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#refer-discard-btn > span")))
                testResult = False
                Result_msg += "#10 "
            except:
                pass
            try:
                WebDriverWait(driver, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#refer-retry-btn > span")))
                testResult = False
                Result_msg += "#11 "
            except:
                pass

            del driver.requests
            time.sleep(0.25)

            # Configuration
            driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
            driver.implicitly_wait(5)

            # Institution
            driver.find_element(By.CSS_SELECTOR, "#institutions-btn").click()
            driver.wait_for_request('.*/GetInstitutionsList.*')

            # Find
            idx = Institution.insti_idx_find(search_institution_3)

            del driver.requests
            time.sleep(0.25)
        
            # select institution code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), search_institution_3))
            
            # set
            driver.find_element(By.CSS_SELECTOR, "#institutions_modify_report_mode_chosen > a > span").click()
            for n in range(1,5):
                if driver.find_element(By.CSS_SELECTOR, "#institutions_modify_report_mode_chosen > div > ul > li:nth-child("+str(n)+")").text == ori_RM:
                    driver.find_element(By.CSS_SELECTOR, "#institutions_modify_report_mode_chosen > div > ul > li:nth-child("+str(n)+")").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#institutions_modify_report_mode_chosen > a > span"), ori_RM))
            driver.find_element(By.CSS_SELECTOR, "#institutions_modify_report_time_chosen > a > span").click()
            for n in range(1, 6):
                if driver.find_element(By.CSS_SELECTOR, "#institutions_modify_report_time_chosen > div > ul > li:nth-child("+str(n)+")").text == ori_RDT:
                    driver.find_element(By.CSS_SELECTOR, "#institutions_modify_report_time_chosen > div > ul > li:nth-child("+str(n)+")").click()
            if ori_comment == True:
                driver.find_element(By.CSS_SELECTOR, "#not-use-default-refer-comment > div:nth-child(6) > div > div > label").click()
            if ori_revised == True:
                driver.find_element(By.CSS_SELECTOR, "#not-use-default-refer-comment > div:nth-child(7) > div > div > label").click()
            if ori_discard == True:
                driver.find_element(By.CSS_SELECTOR, "#not-use-default-refer-comment > div:nth-child(8) > div > div > label").click()
            if ori_request == True:
                driver.find_element(By.CSS_SELECTOR, "#not-use-default-refer-comment > div:nth-child(9) > div > div > label").click()

             # save
            driver.find_element(By.CSS_SELECTOR, "#institutions-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
            
            # Cancel #12
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr[1]/td[2]/a").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-modify-close-btn")))
            # cancel
            driver.find_element(By.CSS_SELECTOR, "#institutions-modify-close-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            # no
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#institutions-modify-close-btn")))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[1]/h3").text
            # cancel
            driver.find_element(By.CSS_SELECTOR, "#institutions-modify-close-btn").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-modify-close-btn")))
            # yes
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            if (msg != "수정을 취소하시겠습니까?" or 
                no_msg != "Institutions Modify" or
                driver.find_element(By.CSS_SELECTOR, "#institutions-tab-name").text != "Institution List"):
                testResult = False
                Reulst_msg += "#12 "

        print("Institution_Modify")
        print(testResult)
        print(Result_msg)

        ## Institution_Modify결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "Institution_Modify Test Passed")

class DownloadControl:
    def User_SearchFilter_Class_Search(num):
        del driver.requests
        time.sleep(0.25)

        driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > div > ul > li:nth-child("+(str(num))+")").click()
        driver.find_element(By.CSS_SELECTOR, "#download-search").click()

        request = driver.wait_for_request('.*/GetDownloadControlList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        check = True
        for n in range(1, len(data)+1):
            if (driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child("+str(n)+") > td:nth-child(2)").get_property("textContent") != data[n-1]["UserID"] or 
                driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child("+str(n)+") > td:nth-child(3)").get_property("textContent") != data[n-1]["UserName"] or 
                driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child("+str(n)+") > td:nth-child(4)").get_property("textContent") != data[n-1]["Institution"].replace('<br />', '')):
                check = False
                break
            
        return check

    def User_SearchFilter_Class():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')

        for a in range (2,6):
            temp = DownloadControl.User_SearchFilter_Class_Search(a)
            if temp == False:
                testResult = False
                Result_msg += "#1 "
                break

        print("DownloadControl_User_SearchFilter_Class")
        print(testResult)
        print(Result_msg)

        ## User_SearchFilter_Class결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "User_SearchFilter_Class Test Passed")

    def User_SearchFilter_Institution_Search(num):
        del driver.requests
        time.sleep(0.25)

        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > ul > li:nth-child("+str(num)+")").click()
        check_insti = driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > ul > li:nth-child("+str(num)+")").get_property("outerText")
        driver.find_element(By.CSS_SELECTOR, "#download-search").click()

        request = driver.wait_for_request('.*/GetDownloadControlList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        check = True
        for n in range(1, len(data)+1):
            insti = data[n-1]["Institution"].replace('<br />', '')
            if (driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child("+str(n)+") > td:nth-child(2)").get_property("textContent") != data[n-1]["UserID"] or 
                driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child("+str(n)+") > td:nth-child(3)").get_property("textContent") != data[n-1]["UserName"] or 
                driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child("+str(n)+") > td:nth-child(4)").get_property("textContent") != insti or 
                insti != check_insti):
                check = False
                break
            
        return check

    def User_SearchFilter_Institution():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')

        for a in range(2,7):
            temp = DownloadControl.User_SearchFilter_Institution_Search(a)
            if temp == False:
                testResult = False
                Result_msg += "#1 "
                break

        print("User_SearchFilter_Institution")
        print(testResult)
        print(Result_msg)

        ## User_SearchFilter_Institution결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "User_SearchFilter_Institution Test Passed")

    # target 1 = id / 2 = name
    def User_SearchFilter_Filter(target):
        rnd_id = driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child(1) > td:nth-child("+str(target+1)+")").get_property("textContent")
        rnd_insti = driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child(1) > td.align-center.download-control-institution").get_property("innerHTML")
        print(rnd_id)
        # User Management
        driver.find_element(By.CSS_SELECTOR, "#user-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[1]"), "User Management List"))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div["+str(target+2)+"]/div/div/input").send_keys(rnd_id)

        del driver.requests
        time.sleep(0.25)

        # search
        driver.find_element(By.CSS_SELECTOR, "#user-search").click()
        driver.wait_for_request('.*/GetUserList')
        rnd_class = driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr > td:nth-child(4)").get_property("textContent")

        del driver.requests
        time.sleep(0.25)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')

        request = driver.wait_for_request('.*/GetInstitutionList')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        
        for n in data:
            if n["InstitutionName"] == rnd_insti.split('<br>')[0]:
                insti_num = data.index(n) + 2
                break

        del driver.requests
        time.sleep(0.25)

        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div["+str(target+2)+"]/div/div/input").send_keys(rnd_id)
        driver.find_element(By.CSS_SELECTOR, "#download-search").click()

        request = driver.wait_for_request('.*/GetDownloadControlList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        check = True
        for n in range(1, len(data)+1):
            if (rnd_id not in data[n-1]["UserID"] or
                driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child("+str(n)+") > td:nth-child(2)").get_property("textContent") != data[n-1]["UserID"] or 
                driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child("+str(n)+") > td:nth-child(3)").get_property("textContent") != data[n-1]["UserName"] or 
                driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child("+str(n)+") > td:nth-child(4)").get_property("textContent") != data[n-1]["Institution"].replace('<br />', '')):
                check = False
                break

        if check == True:
            del driver.requests
            time.sleep(0.25)

            driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > a > span").click()
            for n in range(2,7):
                if rnd_class == driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > div > ul > li:nth-child("+str(n)+")").text:
                    driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > div > ul > li:nth-child("+str(n)+")").click()
                    break
            driver.find_element(By.CSS_SELECTOR, "#download-search").click()

            driver.wait_for_request('.*/GetDownloadControlList.*')

            if rnd_id != driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr > td:nth-child(2)").get_property("textContent"):
                check = False
            
        if check == True:
            del driver.requests
            time.sleep(0.25)

            driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > div > ul > li:nth-child(1)").click()

            driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > ul > li:nth-child("+str(insti_num)+")").click()

            driver.find_element(By.CSS_SELECTOR, "#download-search").click()

            driver.wait_for_request('.*/GetDownloadControlList.*')

            if rnd_id != driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr > td:nth-child(2)").get_property("textContent"):
                check = False

        if check == True:
            del driver.requests
            time.sleep(0.25)

            driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > a > span").click()
            for n in range(2,7):
                if rnd_class == driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > div > ul > li:nth-child("+str(n)+")").text:
                    driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > div > ul > li:nth-child("+str(n)+")").click()
                    break
            driver.find_element(By.CSS_SELECTOR, "#download-search").click()

            driver.wait_for_request('.*/GetDownloadControlList.*')

            if rnd_id != driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr > td:nth-child(2)").get_property("textContent"):
                check = False

        return check

    def User_SearchFilter_UserID():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')
        
        temp = DownloadControl.User_SearchFilter_Filter(target=1)

        if temp == False:
            testResult = False
            Result_msg += "#1 "

        print("User_SearchFilter_UserID")
        print(testResult)
        print(Result_msg)

        ## User_SearchFilter_UserID결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "User_SearchFilter_UserID Test Passed")

    def User_SearchFilter_UserName():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')
        
        temp = DownloadControl.User_SearchFilter_Filter(target=2)

        if temp == False:
            testResult = False
            Result_msg += "#1 "

        print("User_SearchFilter_UserName")
        print(testResult)
        print(Result_msg)

        ## User_SearchFilter_UserName결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "User_SearchFilter_UserName Test Passed")

    def User_Add_DeletionSetup(insti_position):
            # Deletion
            driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr > td:nth-child(1) > label").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.delete-btn")))
            # delete
            driver.find_element(By.CSS_SELECTOR, "#download-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.delete-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # Add
            driver.find_element(By.CSS_SELECTOR, "#download-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#download-contol-add-save-btn"), "Save"))

            # User right
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_user_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(wk_id_2)
            driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(Keys.ENTER)
            driver.find_element(By.CSS_SELECTOR, "#download-config-add-user-add-btn").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-user-remove-btn")))

            # Institution right 
            driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution > option:nth-child("+str(insti_position)+")").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-institution-add-btn")))
            driver.find_element(By.CSS_SELECTOR, "#download-config-add-institution-add-btn").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-institution-remove-btn")))

    def User_Add():
        testResult = True
        Result_msg = "failed at "
        #####request code, request name
        request_name = "Chest PA"
        #####
        
        ReFresh()

        del driver.requests
        time.sleep(0.5)

        # Get info from list
        driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > div > div > input[type=text]").send_keys(search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.wait_for_request(".*/GetAllAssignedList.*")

        del driver.requests
        time.sleep(0.5)

        driver.find_element(By.CSS_SELECTOR, "#tab_all_list > a").click()
        request = driver.wait_for_request('.*/GetAllList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        target_modal = ""
        target_date = ""
        for a in range(0, total):
            request = driver.wait_for_request('.*/GetAllList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in data:
                if n["Modality"] != None:
                    target_modal = n["Modality"]
                if n["JobDTTMString"] != "":
                    target_date = n["JobDTTMString"]
                if target_modal != "" and target_date != "":
                    break

            del driver.requests
            time.sleep(0.25)

            if (a+1 == total or
                (target_modal != "" and target_date != "")):
                break

            driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')
        
        # Add
        driver.find_element(By.CSS_SELECTOR, "#download-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#download-contol-add-save-btn"), "Save"))

        # User right #1
        driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_user_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(wk_id_2)
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#download-config-add-user-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-user-remove-btn")))
        if wk_id_2 not in driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_selected_user_chosen > a > span").text:
            testResult = False
            Result_msg += "#1 "

        # User left #2
        driver.find_element(By.CSS_SELECTOR, "#download-config-add-user-remove-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#sel_available_download_control_add_selected_user_chosen > a > span"),"Select an Option"))
        driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_user_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(wk_id_2)
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(Keys.ENTER)
        if wk_id_2 not in driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_user_chosen > a > span").text:
            testResult = False
            Result_msg += "#2 "

        # User right
        driver.find_element(By.CSS_SELECTOR, "#download-config-add-user-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-user-remove-btn")))

        if "#1" not in Result_msg:
            # Institution right #3
            left_insti_count = driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution").get_property("childElementCount")
            for n in range (1, left_insti_count+1):
                if driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution > option:nth-child("+str(n)+")").text == search_institution_3:
                    insti_position = n
                    driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution > option:nth-child("+str(insti_position)+")").click()
                    break
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-institution-add-btn")))
            driver.find_element(By.CSS_SELECTOR, "#download-config-add-institution-add-btn").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-institution-remove-btn")))
            right_insti_count = driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-selected-institution").get_property("childElementCount")
            if driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-selected-institution > option:nth-child("+str(right_insti_count)+")").text != search_institution_3:
                testResult = False
                Result_msg += "#3 "

            # Institution left #4
            driver.find_element(By.CSS_SELECTOR, "#download-config-add-institution-remove-btn").click()
            try:
                WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#sel-available-download-control-add-institution > option:nth-child("+str(insti_position)+")"), search_institution_3))
            except:
                testResult = False
                Result_msg += "#4 "

            # Institution right 
            driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution > option:nth-child("+str(insti_position)+")").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-institution-add-btn")))
            driver.find_element(By.CSS_SELECTOR, "#download-config-add-institution-add-btn").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-institution-remove-btn")))

            # Emergency only, Save #5 #12
            # not emergency only off
            driver.find_element(By.CSS_SELECTOR, "#download-control-add-popup-modal > div > div > div.modal-body > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(2) > label").click()
            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            # no
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[5]/div/div/div[1]/h3")))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[5]/div/div/div[1]/h3").text
            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            
            del driver.requests
            time.sleep(0.25)   

            # search
            driver.find_element(By.CSS_SELECTOR, "#download-search-user-id").send_keys(wk_id_2)
            driver.find_element(By.CSS_SELECTOR, "#download-search").click()
            driver.wait_for_request('.*/GetDownloadControlList.*')

            if (msg != "등록하시겠습니까?" or 
                no_msg != "Download Control Registration" or 
                driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr > td:nth-child(2)").get_property("textContent") != wk_id_2):
                testResult = False
                Result_msg += "#12 "
            
            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(WorklistUrl);
            wk_login(wk_id_2, wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["JobPriority"] != "E" and wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#5 "
                        break

                if ("#5" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(0.25)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            DownloadControl.User_Add_DeletionSetup(insti_position)

            # Not Emergency Only #6
            # emergency only off
            driver.find_element(By.CSS_SELECTOR, "#download-control-add-popup-modal > div > div > div.modal-body > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > label").click()
            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(0.25)

            driver.get(WorklistUrl);
            wk_login(wk_id_2, wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["JobPriority"] == "E" and wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#6 "
                        break

                if ("#6" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(0.25)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            DownloadControl.User_Add_DeletionSetup(insti_position)

            # Both on #7
            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(0.25)

            driver.get(WorklistUrl);
            wk_login(wk_id_2, wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])
            
            emergency_check = False
            normal_check = False
            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["JobPriority"] == "E" and emergency_check == False:
                        emergency_check = True
                    if n["JobPriority"] != "E" and normal_check == False:
                        normal_check = True

                if ((emergency_check == True and normal_check == True) or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(0.25)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()
            if emergency_check == False or normal_check == False:
                testResult = False
                Result_msg += "#7 "

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            DownloadControl.User_Add_DeletionSetup(insti_position)

            # Both off #8
            driver.find_element(By.CSS_SELECTOR, "#download-control-add-popup-modal > div > div > div.modal-body > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(2) > label").click()
            driver.find_element(By.CSS_SELECTOR, "#download-control-add-popup-modal > div > div > div.modal-body > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > label").click()
            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(0.25)

            driver.get(WorklistUrl);
            wk_login(wk_id_2, wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#8 "
                        break

                if ("#8" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(0.25)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            DownloadControl.User_Add_DeletionSetup(insti_position)

            # Modality #9
            request = driver.wait_for_request('.*/GetModalityList')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            for n in data:
                if n["ModalityCode"] == target_modal:
                    temp_modal = n["ModalityDesc"]
                    break
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_modality_chosen > ul > li > input").send_keys(temp_modal)
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_modality_chosen > ul > li > input").send_keys(Keys.ENTER)

            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(0.25)

            driver.get(WorklistUrl);
            wk_login(wk_id_2, wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if target_modal != n["Modality"] and wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#9 "
                        break

                if ("#9" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(0.25)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            DownloadControl.User_Add_DeletionSetup(insti_position)

            # Date(Job date) #10
            driver.find_element(By.CSS_SELECTOR, "#download-control-add-starting-date").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[2]/button[4]")))
            target_date = target_date.split(' ')[0]
            year = target_date.split('-')[0]
            month_list = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
            month = target_date.split('-')[1]
            for n in range (1, 13):
                if int(month) == n:
                    month = month_list[n-1]
                    break
            day = target_date.split('-')[2]
            while(1):
                if (driver.find_element(By.XPATH, "/html/body/div[4]/div/div[1]/div[1]/div[3]/div[2]").text == year and 
                    driver.find_element(By.XPATH, "/html/body/div[4]/div/div[1]/div[1]/div[1]/div[2]").text == month):
                    break
                driver.find_element(By.XPATH, "/html/body/div[4]/div/div[1]/div[1]/div[1]/div[1]/a/i").click()
                time.sleep(0.3)
            time.sleep(1)
            check = False
            for a in range(2, 7):
                for b in range(1, 8):
                    if driver.find_element(By.XPATH, "/html/body/div[4]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").get_property("textContent") == day:
                        driver.find_element(By.XPATH, "/html/body/div[4]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").click()
                        check = True
                        break
                if check == True:
                    break
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#download-control-add-starting-date"), target_date))

            driver.find_element(By.CSS_SELECTOR, "#download-control-add-ending-date").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[2]/button[4]")))
            while(1):
                if (driver.find_element(By.XPATH, "/html/body/div[5]/div/div[1]/div[1]/div[3]/div[2]").text == year and 
                    driver.find_element(By.XPATH, "/html/body/div[5]/div/div[1]/div[1]/div[1]/div[2]").text == month):
                    break
                driver.find_element(By.XPATH, "/html/body/div[5]/div/div[1]/div[1]/div[1]/div[1]/a/i").click()
                time.sleep(0.3)
            time.sleep(1)
            check = False
            for a in range(2, 7):
                for b in range(1, 8):
                    if driver.find_element(By.XPATH, "/html/body/div[5]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").get_property("textContent") == day:
                        driver.find_element(By.XPATH, "/html/body/div[5]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").click()
                        check = True
                        break
                if check == True:
                    break
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#download-control-add-ending-date"), target_date))

            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(0.25)

            driver.get(WorklistUrl);
            wk_login(wk_id_2, wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if target_date != (n["JobDateDTTMString"].split(' '))[0] and wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#10 "
                        break

                if ("#10" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(0.25)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            DownloadControl.User_Add_DeletionSetup(insti_position)

            # Specialty #11
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_specialty_chosen > ul > li > input").send_keys(specialty)
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_specialty_chosen > ul > li > input").send_keys(Keys.ENTER)

            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(0.25)

            driver.get(WorklistUrl);
            wk_login(wk_id_2, wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if request_name != n["RequestName"] and wk_id_2 not in n["Refer"]:
                        print(request_name)
                        print(n["RequestName"])
                        testResult = False
                        Result_msg += "#11 "
                        break

                if ("#11" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(0.25)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            DownloadControl.User_Add_DeletionSetup(insti_position)

            # Close #13
            # close
            driver.find_element(By.CSS_SELECTOR, "#download-contol-add-close-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            # no
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[5]/div/div/div[1]/h3")))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[5]/div/div/div[1]/h3").text
            # close
            driver.find_element(By.CSS_SELECTOR, "#download-contol-add-close-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            if (msg != "등록을 취소하시겠습니까?" or 
                no_msg != "Download Control Registration" or 
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[1]/h4").text != "Download Control List"):
                testResult = False
                Result_msg += "#13 "

        print("User_Add")
        print(testResult)
        print(Result_msg)

        ## DownloadControl_User_SearchFilter_Class결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "User_Add Test Passed")

    def User_Delete():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')
        
        # Add
        driver.find_element(By.CSS_SELECTOR, "#download-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#download-contol-add-save-btn"), "Save"))

        # User right #1
        driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_user_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(wk_id_2)
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#download-config-add-user-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-user-remove-btn")))
        
        # Institution right
        left_insti_count = driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution").get_property("childElementCount")
        for n in range (1, left_insti_count+1):
            if driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution > option:nth-child("+str(n)+")").text == search_institution_3:
                insti_position = n
                driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution > option:nth-child("+str(insti_position)+")").click()
                break
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-institution-add-btn")))
        driver.find_element(By.CSS_SELECTOR, "#download-config-add-institution-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-institution-remove-btn")))

        # Save
        driver.find_element(By.CSS_SELECTOR, "#download-contol-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # Yes
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # Ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # Nonclick Delete #1
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
            testResult = False
            Result_msg += "#1 "

        # Search
        driver.find_element(By.CSS_SELECTOR, "#download-search-user-id").send_keys(wk_id_2)
        driver.find_element(By.CSS_SELECTOR, "#download-search").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#download-list > tbody > tr > td:nth-child(2)"), wk_id_2))
        
        # Click Delete #2
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr/td[1]/label").click()
        # delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/div[1]/a[2]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[1]/h4").text
        # delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/div[1]/a[2]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        
        if (msg != "삭제하시겠습니까?" or
            no_msg != "Download Control List" or 
            yes_msg != "삭제하였습니다."):
            testResult = False
            Result_msg += "#2 "

        del driver.requests
        time.sleep(1)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')
        for n in driver.requests:
            if "GetDownloadControlList?UserID=&UserName" in n.url:
                request = n
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        if total > 1:
            del driver.requests
            time.sleep(1)

            # Select Other Tab #3
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[1]/td[1]/label").click()
            driver.find_element(By.CSS_SELECTOR, "#download-list_next > a").click()

            driver.wait_for_request('.*/GetDownloadControlList.*')
            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
                testResult = False
                Result_msg += "#3 "

            del driver.requests
            time.sleep(1)

            # Select Other Tab > 2 #4
            element = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[1]/td[1]/label")
            driver.execute_script("arguments[0].click()",element)
            driver.find_element(By.CSS_SELECTOR, "#download-list_previous > a").click()

            driver.wait_for_request('.*/GetDownloadControlList.*')
            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
                testResult = False
                Result_msg += "#4 "
        else:
            testResult = False
            Result_msg += "#3 #4 "

        print("User_Delete")
        print(testResult)
        print(Result_msg)

        ## User_Delete결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "User_Delete Test Passed")

    def User_Modify():
        testResult = True
        Result_msg = "failed at "
        
        ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')
        
        ## Add
        #driver.find_element(By.CSS_SELECTOR, "#download-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        #WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#download-contol-add-save-btn"), "Save"))

        ## User right #1
        #driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_user_chosen > a > span").click()
        #driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(wk_id_2)
        #driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(Keys.ENTER)
        #driver.find_element(By.CSS_SELECTOR, "#download-config-add-user-add-btn").click()
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-user-remove-btn")))
        
        ## Institution right
        #left_insti_count = driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution").get_property("childElementCount")
        #for n in range (1, left_insti_count+1):
        #    if driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution > option:nth-child("+str(n)+")").text == search_institution_3:
        #        insti_position = n
        #        driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution > option:nth-child("+str(insti_position)+")").click()
        #        break
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-institution-add-btn")))
        #driver.find_element(By.CSS_SELECTOR, "#download-config-add-institution-add-btn").click()
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-institution-remove-btn")))

        ## Save
        #driver.find_element(By.CSS_SELECTOR, "#download-contol-add-save-btn").click()
        #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        ## Yes
        #time.sleep(0.25)
        #driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        #WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        ## Ok
        #driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # Search
        driver.find_element(By.CSS_SELECTOR, "#download-search-user-id").send_keys(wk_id_2)
        driver.find_element(By.CSS_SELECTOR, "#download-search").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#download-list > tbody > tr > td:nth-child(2)"), wk_id_2))

        # User ID Click #1
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[1]/td[2]/a").click()
        request = driver.wait_for_request('.*/GetModifyInstitutionList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        if (wk_id_2 not in driver.find_element(By.CSS_SELECTOR, "#download-control-modify-user-name").get_property("textContent") or
            data[0]["InstitutionName"] != search_institution_3 or
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[6]/div/div/div[2]/div[2]/div/div/div[3]/select/option[1]").get_property("text") != search_institution_3 or 
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-check-emergency-only").get_property("disabled") != True or 
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-check-not-emergency-only").get_property("disabled") != True or 
            driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-modality").get_property("disabled") != True or 
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-starting-date").get_property("disabled") != True or 
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-ending-date").get_property("disabled") != True or 
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_modify_specialty_chosen > ul > li > input").get_property("disabled") != True ):
            testResult = False
            Result_msg += "#1 "

        if "#1" not in Result_msg:
            # Institution right #2
            left_insti_count = driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-all-institution").get_property("childElementCount")
            for n in range (1, left_insti_count+1):
                if driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-all-institution > option:nth-child("+str(n)+")").text == search_institution_3:
                    insti_position = n
                    driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-all-institution > option:nth-child("+str(insti_position)+")").click()
                    break

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-modify-institution-add-btn")))
            driver.find_element(By.CSS_SELECTOR, "#download-config-modify-institution-add-btn").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-modify-institution-remove-btn")))
            right_insti_count = driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-institution").get_property("childElementCount")
            if driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-institution > option:nth-child("+str(right_insti_count)+")").text != search_institution_3:
                testResult = False
                Result_msg += "#2 "

            # Institution left #3
            driver.find_element(By.CSS_SELECTOR, "#download-config-modify-institution-remove-btn").click()
            try:
                WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#sel-available-download-control-modify-all-institution > option:nth-child("+str(insti_position)+")"), search_institution_3))
            except:
                testResult = False
                Result_msg += "#3 "

            # Institution right 
            driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-all-institution > option:nth-child("+str(insti_position)+")").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-modify-institution-add-btn")))
            driver.find_element(By.CSS_SELECTOR, "#download-config-modify-institution-add-btn").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-modify-institution-remove-btn")))

            # Selected Institution Click #4
            if (driver.find_element(By.CSS_SELECTOR, "#download-control-modify-check-emergency-only").get_property("disabled") == True or 
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-check-not-emergency-only").get_property("disabled") == True or 
            driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-modality").get_property("disabled") == True or 
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-starting-date").get_property("disabled") == True or 
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-ending-date").get_property("disabled") == True or 
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_modify_specialty_chosen > ul > li > input").get_property("disabled") == True ):
                testResult = False
                Result_msg += "#4 "

            # Emergency only, Save #5 #13
            # not emergency only off
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(2) > label").click()
            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            # no
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[6]/div/div/div[1]/h3")))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[6]/div/div/div[1]/h3").text
            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(0.25)

            # yes
            time.sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            driver.wait_for_request('.*/GetDownloadControlList.*')

            del driver.requests
            time.sleep(0.25)

            # user select
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/GetModifyInstitutionList.*')
            # institution click
            driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-institution > option:nth-child("+str(right_insti_count)+")").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-modify-institution-remove-btn")))
            
            if (msg != "수정하시겠습니까?" or 
                no_msg != "Download Control Modify" or
                driver.find_element(By.CSS_SELECTOR, "#download-control-modify-check-not-emergency-only").get_property("checked") != False ):
                testResult = False
                Result_msg += "#13 "

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(WorklistUrl);
            wk_login(wk_id_2, wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["JobPriority"] != "E" and wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#5 "
                        break

                if ("#5" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(0.25)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])


            




        
        ## Click Delete
        #driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr/td[1]/label").click()
        ## delete
        #driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/div[1]/a[2]").click()
        #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        ## delete
        #driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/div[1]/a[2]").click()
        #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        ## yes
        #driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        #WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        ## ok
        #driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()



        print("User_Modify")
        print(testResult)
        print(Result_msg)

        ## User_Modify결과 전송 ##
        #if testResult == False:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        #else:
        #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "User_Modify Test Passed")

    #def User_SearchFilter_Class():
    #    testResult = True
    #    Result_msg = "failed at "
        
    #    ReFresh()

    #    # Configuration
    #    driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
    #    driver.implicitly_wait(5)

    #    # DownloadControl
    #    driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
    #    driver.wait_for_request('.*/GetDownloadControlList.*')
        
            

    #    print("DownloadControl_User_SearchFilter_Class")
    #    print(testResult)
    #    print(Result_msg)

    #    ## DownloadControl_User_SearchFilter_Class결과 전송 ##
    #    #if testResult == False:
    #    #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
    #    #else:
    #    #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "DownloadControl_User_SearchFilter_Class Test Passed")


#subadmin_login()
admin_login()
DownloadControl.User_Modify()



def test():

    # Configuration
    driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
    driver.implicitly_wait(5)
    time.sleep(0.15)

    # MultiReadingCenterRule
    driver.find_element(By.CSS_SELECTOR, "#multiReadingCenterRule-btn").click()
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi_center_rule_search_modality_chosen > a > span")))

    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[1]/div[2]/div/div[1]/div/a/span").click()
    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[1]/div[2]/div/div[1]/div/div/div/input").send_keys(search_institution_2)
    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[1]/div[2]/div/div[1]/div/div/div/input").send_keys(Keys.ENTER)
    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[1]/div[2]/div/div[5]/div/button").click()
    time.sleep(0.35)
    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[2]/div/table/tbody/tr[1]/td[2]/a").click()
    time.sleep(0.35)

    # left
    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[4]/div/div/div[2]/div[2]/div/div/div[2]/button[2]").click()
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[4]/div/div/div[3]/button[2]")))
    # != not-allowed
    one_remain = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[4]/div/div/div[3]/button[2]").value_of_css_property("cursor")
    # save
    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[4]/div/div/div[3]/button[2]").click()
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[14]/h2")))
    msg = driver.find_element(By.XPATH, "/html/body/div[14]/h2").text
    print(msg)
    element = driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/button")
    
    print(element.get_property("textContent"))
    driver.execute_script("arguments[0].click()",element)
    #driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/button").click()
    #time.sleep(2)

#test()