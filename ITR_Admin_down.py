# -*- coding: utf-8 -*-

from unittest import result
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
import math
subadmin_id = "testSubadmin"
subadmin_pw = "Server123!@#"
search_id = "testInfReporter" #DirectMessageBox_Search_#2
search_username = "TestINFReporter" #DirectMessageBox_Search_#3
search_text = "test" #DirectMessageBox_Search_#4
search_institution = "INFINITT" #NewDirectMessage_#1
search_center = "인피니트"
search_reporter = "TestINFReporter"

def subadmin_login():
    driver.find_element(By.ID, 'user-id').clear()
    driver.find_element(By.ID, 'user-id').send_keys(subadmin_id)
    driver.find_element(By.ID, 'user-password').send_keys(subadmin_pw)
    driver.find_element(By.CSS_SELECTOR, '.btn').click()
    driver.implicitly_wait(5)

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



    #def NewDirectMessage_Institution_Search():
    #    testResult = True
    #    Result_msg = "failed at "
        
    #    ReFresh()

    #    # DirectMessageBox
    #    driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
    #    driver.implicitly_wait(5)

    #    # NewDirectMessage
    #    driver.find_element(By.CSS_SELECTOR, "#direct-message-add-btn").click()
    #    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add_direct_message")))

    #    print("NewDirectMessage_Institution_Search")
    #    print(testResult)
    #    print(Result_msg)

    #    ## NewDirectMessage_Institution_Search결과 전송 ##
    #    #if testResult == False:
    #    #    testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
    #    #else:
    #    #    testlink.reportTCResult(2245, testPlanID, buildName, 'p', "NewDirectMessage_Institution_Search Test Passed")

subadmin_login()
DirectMessage.NewDirectMessage_Reporter_Search()
#DirectMessage.NewDirectMessage_Reporter_Message()

def test():
    print("test")
    x = {'a': 10, 'b': 20, 'c': 30, 'd': 40}
    print(x)

#test()