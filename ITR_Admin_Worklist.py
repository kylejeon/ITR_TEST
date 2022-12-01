from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import json
import math
from dateutil.relativedelta import relativedelta
import random
import cx_Oracle
import os
import ITR_Admin_Login
from ITR_Admin_Common import driver
from ITR_Admin_Common import testlink
from ITR_Admin_Common import testPlanID
from ITR_Admin_Common import buildName
from ITR_Admin_Common import Var
from ITR_Admin_Common import Common

class Worklist:
    def All_Assigned_List():
        print("ITR-24: Worklist > All Assigned List")
        testResult = ''
        reason = list()
        
        # 새로고침
        driver.refresh()
        #driver.wait_for_request('.*/GetAllAssignedList.*')
        #time.sleep(0.3)
        driver.implicitly_wait(5)
        time.sleep(1)

        # 1 steps start! : All Assigned List 탭을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        time.sleep(1)
        del driver.requests
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()

        driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)

        del driver.requests
        time.sleep(1)

        # All Assigned List 탭 클릭
        while(1):
            try:
                webdriver.ActionChains(driver).move_to_element(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]")).perform()
                webdriver.ActionChains(driver).move_to_element(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]")).perform()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()
                break
            except:
                pass

        # Job list 저장
        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)
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

        # 새로고침
        driver.refresh()
        driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)

        # 1 steps start! : Not Assigned List 탭을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        time.sleep(1)
        del driver.requests
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()
        
        driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)

        del driver.requests
        time.sleep(1)

        # Not Assigned List 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        # Job list 저장
        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        # Not Assigned List의 Job list를 가져오는지 확인
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

        # 새로고침
        driver.refresh()
        driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)

        # 1 steps start! : All List 탭을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        time.sleep(1)
        del driver.requests
        time.sleep(1)
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()

        driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)

        del driver.requests
        time.sleep(1)

        # All List 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        # All List의 Job list를 가져오는지 확인
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

        del driver.requests
        time.sleep(1)

        # 새로고침
        driver.refresh()

        # 1 steps start! : Schedule 체크박스를 체크한다.
        # Refer 탭 클릭
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 병원 리스트와 Schedule count 저장
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        time.sleep(0.3)
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
            del driver.requests
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "#list-institution-row-"+str(i[0])).click()
            driver.wait_for_request('.*/GetAllAssignedList.*')
            time.sleep(0.3)

            # Schedule 체크
            status = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[4]/a/input").get_property("checked")
            if status != True:
                del driver.requests
                time.sleep(1)
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[4]/a/label").click()
                driver.wait_for_request('.*/GetAllAssignedList.*')
                time.sleep(0.3)

            # All Assigned List 클릭
            del driver.requests
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()
            
            # All Assigned List의 scheduled job list 저장
            request = driver.wait_for_request('.*/GetAllAssignedList.*')
            time.sleep(0.3)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            schedule_job_list = []

            for j in data:
                schedule_job_list.append(j)

            # Not Assigned List의 scheduled job list 저장
            time.sleep(0.5)
            del driver.requests
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()
            request = driver.wait_for_request('.*/GetNotAssignedList.*')
            time.sleep(0.3)
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
            
             # All Assigned List 클릭
            del driver.requests
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()
            driver.wait_for_request('.*/GetAllAssignedList.*')
            time.sleep(0.3)

        # 2 steps start! : Schedule 체크박스를 체크 해제한다.
        # 병원 탭 클릭
        time.sleep(1)
        del driver.requests
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/li[1]").click()

        # Schedule이 있는 병원의 Job count 저장
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        time.sleep(0.3)
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
            time.sleep(1)
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

        # 새로고침
        driver.refresh()

        # 1 steps start! : Worklist에서 Priority가 일반인 의뢰 검사를 선택한 후, Priority 버튼을 클릭한다.
        # Refer 탭 클릭
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
        
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()
        
        # Show entries를 100개로 변경
        Common.refer_show_entries(100)
        
        # Not Assigned List 탭 클릭
        time.sleep(0.5)
        del driver.requests
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        # Not Assigned List > Job priority가 일반인 Job list 저장
        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        time.sleep(0.3)
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
        time.sleep(0.3)
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
        time.sleep(0.3)
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
        time.sleep(0.3)
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

        # 새로고침
        driver.refresh()

        # 1 steps start! : Worklist에서 Job Status가 Canceled 이외의 의뢰 검사를 선택한 후, Cancel 버튼을 클릭한다.
        # Refer 탭 클릭
        time.sleep(1)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
        
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()

        # Not Assigned List 탭 클릭 후, Job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()
        
        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        time.sleep(0.3)
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
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[9]/div/div/div[3]/button[1]").click()

        # Not Assigned List > Job list 저장
        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        time.sleep(0.3)
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
        time.sleep(1.5)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # Cancel 버튼 클릭
        cancel_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[1]/button[2]")
        if cancel_btn.get_property("disabled") != True:
            driver.execute_script("arguments[0].click()",cancel_btn)

        # Request Cancel > Close 버튼 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[9]/div/div/div[3]/button[2]").click()

        # Not Assigned List 탭 클릭(job list 획득하기 위함)
        time.sleep(1)
        del driver.requests
        time.sleep(1)

        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]")))
        element = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]")
        driver.execute_script("arguments[0].click()",element)

        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        time.sleep(0.3)
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

        # 새로고침
        driver.refresh()
        
        # 1 steps start! : Worklist에서 임의의 의뢰 검사를 선택한 후, Refer 버튼을 클릭한다.
        # Configuration > Institutions로 이동 후, 테스트 병원 검색
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[5]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/button[4]").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[2]/div/div[1]/div/div/input").send_keys(Var.test_hospital_code)
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
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()

        # Show entries를 100개로 변경
        Common.refer_show_entries(100)

        # Not Assigned List 탭 클릭 후, job list 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            job_list.append(i["JobKey"])

        # Not Assigned List > 임의의 job 선택
        job_key = random.choice(job_list)
        time.sleep(1)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//td[normalize-space()='"+str(job_key)+"']")))
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
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
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
        # 새로 고침
        time.sleep(1)
        driver.refresh()

        # Configuration > Institutions로 이동 후, 테스트 병원 검색
        element = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[5]")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[5]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/button[4]").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[2]/div/div[1]/div/div/input").send_keys(Var.test_hospital_code)
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

        # 새로 고침
        time.sleep(1)
        driver.refresh()

        # Refer 탭 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
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

        # Comment empty
        if len(comment_list) == 0:
            testResult = "failed"
            reason.append("6 steps failed(comment_list empty)\n")
            driver.find_element(By.CSS_SELECTOR, "#refer-close").click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button")))
        else:
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
            time.sleep(0.3)
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
        # 새로고침
        time.sleep(1)
        driver.refresh()

        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()
        
        # Not Assigned List 탭 클릭 후, job list 저장
        time.sleep(1)
        del driver.requests
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        time.sleep(0.3)
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
        time.sleep(0.3)
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
        time.sleep(0.3)
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
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        time.sleep(0.3)
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
        time.sleep(0.3)
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
        time.sleep(0.3)
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
        time.sleep(0.3)
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

        # 새로고침
        driver.refresh()

        # 1 steps start! : 판독의가 할당된 의뢰 검사를 선택한 후, Refer Cancel 버튼을 클릭한다.
        # Refer 탭 클릭
        time.sleep(1)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()

        # Show entries를 100개로 변경
        Common.refer_show_entries(100)

        # All Assigned List 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)
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
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[2]")))
        driver.execute_script("arguments[0].click()",btn)

        # All Assigned List > Refer Cancel 팝업창 확인
        popup_title = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[10]/div/div/div[1]/h4")
        try:
            assert popup_title.get_property("textContent") == "Refer Cancel"
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! : Refer Cancel 팝업창에서 "Close"를 클릭한다.
        # Refer Cancel 팝업창 > Close 클릭
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#refer-cancel-close")))
        driver.find_element(By.CSS_SELECTOR, "#refer-cancel-close").click()
        
        # All Assigned List 탭 클릭 후, job list 저장
        while(1):
            try:
                del driver.requests
                time.sleep(1)

                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()
                break
            except:
                # 새로고침
                driver.refresh()

                # 1 steps start! : 판독의가 할당된 의뢰 검사를 선택한 후, Refer Cancel 버튼을 클릭한다.
                # Refer 탭 클릭
                time.sleep(1)
                # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

                # Test 병원 선택
                hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
                for i in hospital_list:
                    if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                        i.click()
                        break

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)
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
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[2]")))
        driver.execute_script("arguments[0].click()",btn)

        # Refer Cancel 팝업창 > OK 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[10]/div/div/div[3]/button[1]").click()

        # All Assigned List 저장
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)
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
        time.sleep(0.5)
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
        reporter_key = (reporter_list[random.randrange(0,reporter_cnt)].get_property("dataset"))["reporterKey"]
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
        time.sleep(0.3)
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
        time.sleep(0.3)
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

        # 새로고침
        driver.refresh()

        # 1 steps start! : 판독의에게 할당된 임의의 의뢰 검사를 선택하고, Refer Cancel and Refer 버튼을 클릭한다.
        # Refer 탭 클릭
        time.sleep(1)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
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
        del driver.requests
        time.sleep(1)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)
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
            driver.execute_script("arguments[0].click()",btn)
            
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
                    time.sleep(0.3)
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
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                driver.execute_script("arguments[0].click()",i)
                break

        driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)

        # All List 탭 클릭 후, job list 저장
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        request = driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)
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
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//td[normalize-space()='"+str(not_refer_job)+"']")))
        time.sleep(0.3)
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
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()
        
        del driver.requests
        time.sleep(1)
        
        # All List 탭 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)

        # 3 steps start! : All Assigned/All List에서 Refer 된 Job을 선택한다.
        # All List > Refer 된 job 만 선택
        for i in range(0,3):
            refer_job_key = refer_job_list.pop(refer_job_list.index(random.choice(refer_job_list)))
            time.sleep(1)
            element = driver.find_element(By.XPATH, "//label[@for='r_j_c_"+str(refer_job_key)+"']")
            driver.execute_script("arguments[0].click()",element)
            
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
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()
        
        # All Assigned List > job list 저장
        time.sleep(1)
        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)
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
                    time.sleep(1)
                    btn = driver.find_element(By.CSS_SELECTOR, "#institution_reporter_list_row_"+str(j[1]))
                    try:
                        driver.execute_script("arguments[0].click()",btn)
                    except:
                        driver.find_element(By.CSS_SELECTOR, "#institution_reporter_list_row_"+str(j[1])).click()
                    time.sleep(1)

                    request = driver.wait_for_request('.*/GetReferedListByReporter.*')
                    time.sleep(0.3)
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
        time.sleep(1)
        reporter_key = (reporter_list[random.randrange(0,reporter_cnt)].get_property("dataset"))["reporterKey"]
        btn = driver.find_element(By.CSS_SELECTOR, "#institution_reporter_list_row_"+str(reporter_key))
        driver.execute_script("arguments[0].click()",btn)

        # Reporter의 refer 받은 job list 저장
        request = driver.wait_for_request('.*/GetReferedListByReporter.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        refer_job_list = []

        for i in data:
            refer_job_list.append(i["JobKey"])

        # 임의의 job 선택 후, R.Cancel & Refer 버튼 클릭
        job_key_list = []
        refer_job_cnt = len(refer_job_list)
        for i in range(0, len(refer_job_list) if refer_job_cnt < 2 else 2):
            job_key = refer_job_list.pop(refer_job_list.index(random.choice(refer_job_list)))
            time.sleep(1)
            driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()
            job_key_list.append(job_key)
        time.sleep(1)

        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/button[4]")))
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
                    time.sleep(1)
                    btn = driver.find_element(By.CSS_SELECTOR, "#institution_reporter_list_row_"+str(j[1]))
                    driver.execute_script("arguments[0].click()",btn)
                    time.sleep(1)

                    request = driver.wait_for_request('.*/GetReferedListByReporter.*')
                    time.sleep(0.3)
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
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()

        # Not Assigned List 탭 클릭 후, job list 저장
        time.sleep(1.5)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()

        request = driver.wait_for_request('.*/GetNotAssignedList.*')
        time.sleep(0.3)
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

        # Test 병원 선택
        del driver.requests
        time.sleep(1)
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()
                break

        driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)

        del driver.requests
        time.sleep(1)

        # Show entries를 100개로 변경
        Common.refer_show_entries(100)
        try:
            request = driver.wait_for_request('.*/GetAllAssignedList.*')
        except:
            Common.refer_show_entries(10)
            driver.wait_for_request('.*/GetAllAssignedList.*')
            time.sleep(0.3)
            del driver.requests
            time.sleep(1)

            Common.refer_show_entries(100)
            request = driver.wait_for_request('.*/GetAllAssignedList.*')
            time.sleep(0.3)

        # All Assigned List에서 schedule이 없는 job list 저장
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        remain = data["recordsFiltered"] % data["Length"]

        check = False
        for a in range(0, total):
            before_assigned_job_list = []
            request = driver.wait_for_request('.*/GetAllAssignedList.*')
            time.sleep(0.3)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for i in data:
                if i["ScheduleDateDTTMString"] == "":
                    before_assigned_job_list.append(i["JobKey"])
                    check = True

            if check == True or a+1 == total:
                break

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()

        # All Assigned List > 임의의 job 선택
        job_key = random.choice(before_assigned_job_list)
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # 추가
        if len(before_assigned_job_list) >= remain:
            while(1):
                job_key = random.choice(before_assigned_job_list)
                time.sleep(1)
                if driver.find_element(By.XPATH, "//*[@id=\"r_j_c_"+str(job_key)+"\"]").get_property("checked")==False:
                    driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()
                    break

        # All Assigned List > Schedule 버튼 클릭
        while(1):
            try:
                webdriver.ActionChains(driver).move_to_element(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]/a")).perform()
                schedule_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/button[1]")
                webdriver.ActionChains(driver).move_to_element(schedule_btn).perform()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/button[1]")))
                schedule_btn.click()
                break
            except:
                pass

        # All Assigned List > Schedule 버튼 옆에 날짜와 시간 선택 기능이 표시되는지 확인
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/div")))
        except:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! : 임의의 날짜와 시간을 입력한 후, 확인 버튼을 클릭한다.
        # All Assigned List > Schedule 날짜는 기본값, 시간은 1030으로 입력 후, 체크 클릭
        input_date = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/div/div/div[2]/div/div[1]/input").get_property("value")
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/div/div/div[2]/div/div[2]/input").send_keys("1030")
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/div/div/button")))
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/div/div/button").click()

        # Schedule 등록 완료 팝업창이 팝업되는지 확인
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[6]/h2")))
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
        time.sleep(0.3)
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
        
        while(1):
            try:
                schedule_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/button[1]")
                webdriver.ActionChains(driver).move_to_element(schedule_btn).perform()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/button[1]")))
                schedule_btn.click()
                break
            except:
                pass

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
        input_date = (Var.today + relativedelta(months=1)).strftime('%Y-%m-%d') 
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
        time.sleep(0.3)
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
            assert (check_date, check_time.replace(":", "")) == ((Var.today + relativedelta(months=1)).strftime('%Y-%m-%d'), "110000")
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

        # 새로고침
        driver.refresh()

        # 1 steps start! : Schedule이 없는 임의의 의뢰 job을 선택한 후, Schedule Cancel 버튼을 클릭한다.
        # Refer 탭 클릭
        time.sleep(0.5)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        del driver.requests
        time.sleep(1)
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()
                break

        driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)

        del driver.requests
        time.sleep(1)

        # Show entries를 100개로 변경
        Common.refer_show_entries(10)
        try:
            driver.wait_for_request('.*/GetAllAssignedList.*')
            time.sleep(0.3)
            del driver.requests
            time.sleep(1)
        except:
            pass
        Common.refer_show_entries(100)

        # All Assigned List에서 schedule이 없는 job list 저장
        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        cehck = False
        for a in range(0, total):
            not_schedule_job_list = []
            request = driver.wait_for_request('.*/GetAllAssignedList.*')
            time.sleep(0.3)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for i in data:
                if i["ScheduleDate"] == None:
                    not_schedule_job_list.append(i)
                    check = True

            if check == True or a+1 == total:
                break

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()

        # All Assigned List > Schedule이 없는 임의의 job 선택
        sample_job = random.choice(not_schedule_job_list)
        job_key = sample_job["JobKey"]
        time.sleep(1)
        driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()

        # All Assigned List > S.Cancel 클릭
        btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/button[2]")
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/button[2]")))
        driver.execute_script("arguments[0].click()",btn)

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
        while(1):
            try:
                del driver.requests
                time.sleep(1)
<<<<<<< HEAD
                
                webdriver.ActionChains(driver).move_to_element(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]/a")).perform()
                webdriver.ActionChains(driver).move_to_element(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]")).perform()
=======

                webdriver.ActionChains(driver).move_to_element(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]/a")).perform()
                webdriver.ActionChains(driver).move_to_element(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]")).perform()

>>>>>>> cff2bd10732de6906ffa8c8d8cf1bf8ba489a3ac
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()
                break
            except:
                # 새로고침
                driver.refresh()

                # 1 steps start! : 판독의가 할당된 의뢰 검사를 선택한 후, Refer Cancel 버튼을 클릭한다.
                # Refer 탭 클릭
                time.sleep(1)
                # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

                # Test 병원 선택
                hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
                for i in hospital_list:
                    if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                        i.click()
                        break

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)
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
            driver.execute_script("arguments[0].click()",btn)

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
        time.sleep(0.3)
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
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()

        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)
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
        time.sleep(1)

        while(1):
            try:
                webdriver.ActionChains(driver).move_to_element(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]/a")).perform()
                schedule_btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/button[1]")
                webdriver.ActionChains(driver).move_to_element(schedule_btn).perform()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/button[1]")))
                schedule_btn.click()
                break
            except:
                pass
        
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
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[4]/button[2]")))
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
        driver.find_element(By.XPATH, "/html/body/div[6]/div[7]/div/button").click()
        
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

        # 새로고침
        driver.refresh()

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
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()

        # Show entries를 100개로 변경
        Common.refer_show_entries(100)

        # All List 탭 클릭 후, job list 저장
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()
        request = driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)
        time.sleep(1)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        job_list = []

        for i in data:
            job_list.append(i)
        job_key = (job_list[0])["JobKey"]

        # Search Condition > Job status를 Completed로 선택 후, Search 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        time.sleep(0.25)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[5]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

        # All List > Completed job 개수 확인
        time.sleep(1)
        all_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div[2]/table/tbody/tr")

        # All List > Completed job 개수가 0인 경우
        if len(all_list) == 1:
            # DB 접속
            os.putenv('NLS_LANG', '.UTF8')
            cx_Oracle.init_oracle_client(lib_dir=r"D:\app\user\instantclient_21_7")
            connection = cx_Oracle.connect("pantheon","pantheon",Var.vmonpacs_tns, encoding="UTF-8")
            cursor = connection.cursor()

            # DB에서 선택한 병원의 All list의 첫번째 job의 job stat을 Completed로 변경
            sql = f"""
                update job set job_stat = '310' where job_key = '{job_key}'
                """
            cursor.execute(sql)
            cursor.close()
            connection.commit()
            connection.close()
        
        # All List > Search 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
        time.sleep(1)
        
        # All List > Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.5)
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
            driver.execute_script("arguments[0].click()",btn)
        
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
            driver.execute_script("arguments[0].click()",btn)

        # Update Request Status 팝업창 > OK 클릭
        time.sleep(0.5)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[3]/button[1]").click()

        # All List > job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)
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

        # 새로고침
        driver.refresh()

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
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()

        # Show entries를 100개로 변경
        Common.refer_show_entries(100)

        # All Assigend List > job list 저장
        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)
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
            driver.execute_script("arguments[0].click()",btn)

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
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]").click()
        time.sleep(1)
        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)
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
            driver.execute_script("arguments[0].click()",btn)

        # Discard 팝업창 > OK 클릭
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[3]/button[1]").click()

        # All Assigend List > job list 저장
        request = driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)
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
        time.sleep(0.3)
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

        # 새로고침
        Common.ReFresh()

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
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
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
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
        time.sleep(1)

        # All List > Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        check = False
        for a in range(0, total):
            job_list = []
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.3)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]


            for i in data:
                if i["StatDescription"] in ("Requested","Canceled2","DiscardCompleted"):
                    job_list.append(i)
                    check = True

            if check == True or a+1 == total:
                break

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()

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
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[3]/button[1]").click()

        # All List > Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        check = False
        for a in range(0, total):
            job_list = []
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.3)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for i in data:
                job_list.append(i)

            # All List > Job list에서 선택했던 job의 job status가 RetryRequest로 변경되었는지 확인
            for i in job_list:
                if i["JobKey"] == job_key:
                    assert i["StatDescription"] == "RetryRequest"
                    check = True
                    break

            if a+1 == total or check == True:
                break

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()

        if check == False:
            testResult = "failed"
            reason.append("1 steps failed\n")

        # 2 steps start! : Job status가 DiscardCompleted 인 임의의 job을 선택한 후, Retry Request 버튼을 클릭한다.
        # Job status가 DiscardCompleted 인 임의의 job을 선택 후, Retry Request 클릭
        del driver.requests
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
        time.sleep(1)

        request = driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        check = False
        for a in range(0, total):
            job_list = []
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.3)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for i in data:
                if i["StatDescription"] =="DiscardCompleted":
                    job_list.append(i)
                    check = True

            if check == True or a+1 == total:
                break

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()

        # Job status가 DiscardCompleted 인 job이 없는 경우, 추가
        if len(job_list) == 0:
            # DB 접속
            os.putenv('NLS_LANG', '.UTF8')
            cx_Oracle.init_oracle_client(lib_dir=r"D:\app\user\instantclient_21_7")
            connection = cx_Oracle.connect("pantheon","pantheon",Var.vmonpacs_tns, encoding="UTF-8")
            cursor = connection.cursor()

            # DB에서 선택한 병원의 All list의 첫번째 job의 job stat을 Completed로 변경
            random_data = random.choice(data)
            job_key = random_data["JobKey"]
            job_list.append(random_data)

            sql = f"""
                update job set job_stat = '610' where job_key = '{job_key}'
                """
            cursor.execute(sql)
            cursor.close()
            connection.commit()
            # DB 연결 해제
            connection.close()

        # Job status가 DiscardCompleted 인 임의의 job을 선택
        try:
            sample_job = random.choice(job_list)
            job_key = sample_job["JobKey"]
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
            time.sleep(3)
            driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()
        except:
            testResult = "failed"
            reason.append("2 steps failed\n")
        
        if "2 steps failed\n" not in reason:
            # Retry Request 클릭
            time.sleep(2)
            btn = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[3]/button[3]")
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[3]/button[3]")))
            try:
                btn.click()
            except:
                Common.ReFresh()
                time.sleep(3)
                hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
                for i in hospital_list:
                    if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                        i.click()
                time.sleep(1)
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()
                time.sleep(1)

                # Search condition > Job Status를 Discard Completed로 선택하고, Search 클릭
                time.sleep(1)
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
                time.sleep(0.5)
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[13]").click()
                time.sleep(1)
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                time.sleep(1)
                
                # All List > Job stat이 Discard Completed 인 job 선택
                driver.find_element(By.XPATH, "//td[normalize-space()='"+str(job_key)+"']").click()
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "#refer-retry-btn").click()

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
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[14]/div/div/div[3]/button[1]").click()
        else:
            del driver.requests
            time.sleep(1)
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#tab_all_list > a")))
            driver.find_element(By.CSS_SELECTOR, "#tab_all_list > a").click()
        
        # Search condition > Job Status를 Discard Completed로 선택하고, Search 클릭
        del driver.requests
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[1]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
        time.sleep(1)

        # All List > Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        check = False

        for a in range(0, total):
            job_list = []
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.3)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for i in data:
                job_list.append(i)

            # All List > Job list에서 선택했던 job의 job status가 RetryRequest로 변경되었는지 확인
            for i in job_list:
                if i["JobKey"] == job_key:
                    assert i["StatDescription"] == "RetryRequest"
                    check = True
                    break

            if a+1 == total or check == True:
                break

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()

        if check == False:
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
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()

        # All Assigned List > Column list 저장
        column_list = []
        columns = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div[1]/div/table/thead/tr").get_property("outerText")
        column_list = columns.split('\t')
        del column_list[0]

        # Columns 클릭
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/div[5]/div[1]/button")))
        time.sleep(0.5)
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
        
        # 새로고침
        driver.refresh()

        # 1 steps start! : Show entries의 개수를 10으로 변경한다.
        # Refer 탭 클릭
        time.sleep(0.5)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        time.sleep(1)
        del driver.requests
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()

        # All List 탭 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        del driver.requests
        time.sleep(1)

        # Show entries를 10으로 변경
        Common.refer_show_entries(10)

        driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)
        
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

        # 새로고침
        driver.refresh()

        # 1 steps start! : Use Related Worklist에 체크한 후, worklist에서 임의의 의뢰 검사를 선택한다.
        # Refer 탭 클릭
        time.sleep(0.5)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # Test 병원 선택
        time.sleep(1)
        del driver.requests
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
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
        time.sleep(0.3)
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

        # 1 steps start! : 정렬 가능한 컬럼을 확인한다.
        # 새로고침
        driver.refresh()

        # Test 병원 선택
        time.sleep(1)
        del driver.requests
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
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

