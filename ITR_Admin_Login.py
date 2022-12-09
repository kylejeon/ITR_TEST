from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
import random
import string
from ITR_Admin_Common import driver
from ITR_Admin_Common import testlink
from ITR_Admin_Common import testPlanID
from ITR_Admin_Common import buildName
from ITR_Admin_Common import Var
import Common_Var

class signInOut:
    def admin_sign_in():
        driver.find_element(By.ID, 'user-id').clear()
        driver.find_element(By.ID, 'user-id').send_keys(Var.adminID)
        driver.find_element(By.ID, 'user-password').send_keys(Var.adminPW)
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)
        time.sleep(0.3)
    def admin_sign_out():
        driver.find_element(By.CSS_SELECTOR, '.pull-right > span').click()
        driver.implicitly_wait(5)
        time.sleep(0.3)
    def stg_admin_sign_in():
        driver.find_element(By.ID, 'user-id').clear()
        driver.find_element(By.ID, 'user-id').send_keys(Var.stg_adminID)
        driver.find_element(By.ID, 'user-password').send_keys(Var.stg_adminPW)
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)
        time.sleep(0.3)
    def stg_admin_sign_out():
        driver.find_element(By.CSS_SELECTOR, '.pull-right > span').click()
        driver.implicitly_wait(5)
        time.sleep(0.3)
    def subadmin_sign_in():
        driver.find_element(By.ID, 'user-id').clear()
        driver.find_element(By.ID, 'user-id').send_keys(Var.subadminID)
        driver.find_element(By.ID, 'user-password').send_keys(Var.subadminPW)
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)
        time.sleep(0.3)
    def subadmin_sign_out():
        driver.find_element(By.CSS_SELECTOR, '.pull-right > span').click()
        driver.implicitly_wait(5)
        time.sleep(0.3)
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
            pass
            #print("no cert")

        # waiting loading
        try:
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div/div/div/section[1]/div[3]/div/div[1]/button[3]")))
        except:
            pass

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
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[3]/div/input").send_keys(Var.adminID)
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
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[3]/div/input").send_keys(Var.reporterID)
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/input").clear()
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/input").send_keys(Var.reporterPW)
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
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[3]/div/input").send_keys(Var.adminID)
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/input").clear()
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/input").send_keys(Var.adminPW)
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
            Common_Var.form.update_failed()
            testlink.reportTCResult(1531, testPlanID, buildName, 'f', result)            
        else:
            Common_Var.form.update_passed()
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
        driver.find_element(By.ID, 'user-id').send_keys(Var.adminID)
        driver.find_element(By.ID, 'user-password').send_keys(Var.adminPW)
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, '.col-xs-8.p-t-5 > label').click()
        driver.find_element(By.CSS_SELECTOR, '.btn').click()         
        driver.implicitly_wait(3)      
        time.sleep(0.5)                 
        
        # 로그아웃 후, 마지막에 접속한 User ID와 Remind Me 체크 상태를 확인한다.
        signInOut.admin_sign_out()        
        try:
            assert (driver.find_element(By.ID, 'user-id').get_property("value"), driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/form/div[5]/div[1]/input').get_property('checked')) == (Var.adminID, True)
        except:
            testResult = 'failed' 
            reason.append("1 Steps failed")
        
        # Remember_Me 결과 전송       
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            Common_Var.form.update_failed()
            testlink.reportTCResult(1538, testPlanID, buildName, 'f', result)            
        else:
            Common_Var.form.update_passed()
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
            Common_Var.form.update_failed()
            testlink.reportTCResult(1542, testPlanID, buildName, 'f', result)            
        else:
            Common_Var.form.update_passed()
            testlink.reportTCResult(1542, testPlanID, buildName, 'p', "Search_Schedule_List Test Passed")  
