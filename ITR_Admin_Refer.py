import ITR_Admin_Login
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
import math
from datetime import datetime, timedelta
import random
from ITR_Admin_Common import driver
from ITR_Admin_Common import testlink
from ITR_Admin_Common import testPlanID
from ITR_Admin_Common import buildName
from ITR_Admin_Common import Common
from ITR_Admin_Common import Var

class Refer:
    def Hospital_List():
        print("ITR-7: Refer > Hospital List")
        testResult = ''
        reason = list() 

        # SubAdmin 로그인
        ITR_Admin_Login.signInOut.admin_sign_out()
        time.sleep(2)
        ITR_Admin_Login.signInOut.subadmin_sign_in()
        time.sleep(2)

        del driver.requests
        time.sleep(1)

        # Refer 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : 모든 병원의 badge count와 job list의 결과가 일치하는지 확인
        # Hospital list 저장
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        hospital_cnt = len(data)

        # Show 100 entries 설정
        select = Select(driver.find_element(By.CSS_SELECTOR,"#refer-assigned-list_length > label > select"))
        select.select_by_value("100")

        # 각 hospital의 refer, requested, emergency job의 건수 비교
        if hospital_cnt > 0:
            n = 0

            for i in data:
                priority_cnt = i['PriorityCount']
                job_cnt = i['JobCount']
                refer_cnt = i['ReferCount']
                del driver.requests
                time.sleep(0.5)
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]").click()

                # All Assigned List > Showing entry 결과 저장
                time.sleep(1)
                job_refer_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
                job_refer_cnt = job_refer_cnt.split()[5]
                auto_refer_cnt = int(job_refer_cnt)
                emer_list = []
                pages = math.ceil(int(job_refer_cnt) / 100)
                
                # 선택한 병원의 Job list 결과 저장 
                request = driver.wait_for_request('.*/GetAllAssignedList.*')
                time.sleep(0.5)
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]
                
                while pages > 0: 
                    for i in data:
                        # All Assigned List 탭에서 Emergency Job 건수 계산
                        if i["JobPriority"] == 'E':
                            emer_list.append(i)
                            
                    pages = pages - 1
                    del driver.requests
                    time.sleep(1)
                    
                    # 새로운 페이지 조회 결과 저장
                    if pages > 0:
                        driver.find_element(By.CSS_SELECTOR,"#refer-assigned-list_next > a").click()
                        request = driver.wait_for_request('.*/GetAllAssignedList.*')
                        time.sleep(0.3)
                        body = request.response.body.decode('utf-8')
                        data = json.loads(body)["data"]
                    
                # 병원 리스트의 Refer badge count와 Job list의 refer job list 개수 확인
                try:
                    assert refer_cnt == int(job_refer_cnt)
                except:
                    testResult = 'failed'
                    reason.append("Step1 - Refer count isn't valid")
                    
                # 요청 결과 삭제
                del driver.requests
                time.sleep(0.5)
     
                # Not Assigned List 탭 클릭
                element = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]/a")
                driver.execute_script("arguments[0].click()",element)
                
                # 선택한 병원의 Not Assigned List 결과 저장
                request = driver.wait_for_request('.*/GetNotAssignedList.*')
                time.sleep(0.3)
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                # Not Assigned List의 Showing entries 값 저장
                temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
                auto_refer_cnt += int(temp_cnt.split()[5])
                pages = math.ceil(int(auto_refer_cnt) / 100)

                # Emergency Job 건수 계산
                while pages > 0: 
                    for i in data:
                        if i["JobPriority"] == 'E':
                            emer_list.append(i)
                            # emer_reporter_list_cnt = emer_reporter_list_cnt + 1
                            
                    pages = pages - 1   
                    del driver.requests
                    time.sleep(0.5)

                    if pages > 0:
                        # 새로운 페이지의 결과 저장
                        driver.find_element(By.CSS_SELECTOR,"#refer-assigned-list_next > a").click()
                        request = driver.wait_for_request('.*/GetNotAssignedList.*')
                        time.sleep(0.3)
                        body = request.response.body.decode('utf-8')
                        data = json.loads(body)["data"]
                        time.sleep(1)

                try:
                    assert (priority_cnt, job_cnt) == ((len(emer_list), auto_refer_cnt))
                except:
                        testResult = 'failed'
                        reason.append("1 steps failed")

                # Refer 화면 새로고침
                driver.refresh()
                n = n + 1

        # 2 steps start! : 병원을 선택하면 표시되는 Reporter가 해당 병원의 소속된 Reporter 인지 확인
        # Refer 화면 새로고침
        driver.refresh()

        # Hospital list 저장
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        time.sleep(0.3)
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
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]").click()
                
                # Hospital list의 Reporter list 저장
                request = driver.wait_for_request('.*/GetReporterListByInstitution.*')
                time.sleep(0.3)
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
                time.sleep(0.3)
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
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]").click()

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
                    time.sleep(0.3)
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]
                    temp_job_modality_list = []
                    job_modality_list = []

                    for i in data:
                        job_modality_list.append(i["Modality"])

                    # 판독의 탭 클릭
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/li[2]/a")))
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/li[2]/a").click()

                    # 판독의 탭 > 선택한 Reporter 클릭
                    time.sleep(1)
                    del driver.requests
                    driver.find_element(By.CSS_SELECTOR, "#list-reporter-row-"+reporter_key).click()

                    # 판독의 탭 > 선택한 Reporter의 Job list에서 modality 저장                
                    request = driver.wait_for_request('.*/GetAllReferedListByReporter.*')
                    time.sleep(0.3)
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
                # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
                driver.refresh()
                
        # 4 steps start! : View All Institution List 체크 시, 표시되는 병원이 올바른 것인지 확인
        # View All Instituion List 체크
        time.sleep(1)
        del driver.requests
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[2]/label/span").click()

        # All Hospital list 저장
        time.sleep(1)
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        time.sleep(0.3)
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
        time.sleep(0.3)
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
        
        # View All Institution list에서 Job이 있는 Institution list만 저장
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        time.sleep(0.3)
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
        time.sleep(0.3)
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
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        time.sleep(0.3)
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
                time.sleep(1)
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]").click()

                # All Assigned List 탭 > 선택한 병원의 job list 저장
                request = driver.wait_for_request('.*/GetAllAssignedList.*')
                time.sleep(0.3)
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
                time.sleep(0.3)
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
                del driver.requests
                time.sleep(1)
                driver.find_element(By.XPATH,"/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]/a").click()

        # 7 steps start! : 선택한 병원의 badge count와 job list의 count가 일치하는지 확인
        # Hospital list 저장
        driver.refresh()
        time.sleep(2)

        click_hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        hospital_cnt = len(data)
        
        if hospital_cnt > 0:
            n = 0
            reporter_list = []
            
            while n < hospital_cnt:
                # 순서대로 병원 클릭
                time.sleep(0.5)
                del driver.requests
                time.sleep(0.5)
                # click_hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
                # click_hospital_list[n].click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]")))
                click_hospital = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]").get_property("innerText")
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]").click()
                m = 0

                # 선택한 병원의 Reporter list 저장
                time.sleep(2)
                reporter_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-sub-item")
                time.sleep(0.5)
                reporter_list_cnt = len(reporter_list)
                
                # Reporter의 badge count 저장
                request = driver.wait_for_request('.*/GetReporterListByInstitution.*')
                time.sleep(0.3)
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

                    # All Assigned List 탭 > job list에서 선택한 Reporter의 emergency, refer, scheduled count 저장
                    request = driver.wait_for_request('.*/GetReferedListByReporter.*')
                    time.sleep(0.3)
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
                        if i["ScheduleDate"] != None:
                            scheduled_cnt = scheduled_cnt + 1
                        
                    # 판독의 탭 클릭
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/li[2]/a").click()

                    # 판독의 탭 > 선택한 Reporter 클릭
                    time.sleep(2)
                    del driver.requests
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "#list-reporter-row-"+reporter_key).click()

                    # Other refer count 저장
                    request = driver.wait_for_request('.*/GetInstitutionListByReporter.*')
                    time.sleep(0.5)
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)

                    for i in data:
                        if i["InstitutionName"] != click_hospital:
                            other_refer_cnt += int(i["ReferCount"])
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
                    # click_hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
                    # click_hospital_list[n].click()
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a")))
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a").click()
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]")))
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]").click()

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
        request = driver.wait_for_request('.*/GetReferCountsByInstitution.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        hospital_cnt = len(data)
        
        if hospital_cnt > 0:
            n = 0
            
            while n < hospital_cnt:
                # 순서대로 병원 클릭
                time.sleep(1)
                del driver.requests
                time.sleep(1)
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]").click()
                m = 0
                
                driver.wait_for_request('.*/GetReporterListByInstitution.*')
                time.sleep(0.3)

                # 선택한 병원의 Reporter list 저장
                time.sleep(2)
                reporter_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-sub-item")
                reporter_list_cnt = len(reporter_list)

                # 순서대로 Reporter 클릭
                while m < reporter_list_cnt:
                    time.sleep(1)
                    del driver.requests
                    time.sleep(1)               
                    reporter_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-sub-item")
                    reporter_key = (reporter_list[m].get_property("dataset"))["reporterKey"]
                    driver.execute_script("arguments[0].click()",reporter_list[m])

                    # 선택한 Reporter의 Job list 저장
                    request = driver.wait_for_request('.*/GetReferedListByReporter.*')
                    time.sleep(0.3)
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
                while(1):
                    try:
                        webdriver.ActionChains(driver).move_to_element(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[4]")).perform()
                        webdriver.ActionChains(driver).move_to_element(driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]")).perform()
                        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
                        break
                    except:
                        pass
                n = n + 1

        # Hospital_List 결과 전송
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else result)
        if testResult == 'failed':
            testlink.reportTCResult(1567, testPlanID, buildName, 'f', result)            
        else:
            testlink.reportTCResult(1567, testPlanID, buildName, 'p', "Hospital_List Test Passed")  

        # Admin 로그인
        ITR_Admin_Login.signInOut.subadmin_sign_out()
        time.sleep(2)
        ITR_Admin_Login.signInOut.admin_sign_in()
        time.sleep(2)

    def Reporter_List():
        print("ITR-8: Refer > Reporter List")
        testResult = ''
        reason = list()        

        # 1 & 2 steps start! : 판독의 탭 > 판독의 리스트에 표시되는 badge count가 job list와 일치하는지 확인
        # Reporter list를 저장한다.
        driver.find_element(By.XPATH, "//*[@id='tab-reporter']").click()
        request = driver.wait_for_request('.*/GetReferCountsByReporter.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        reporter_cnt = len(data)

        reporter_list = []
        for i in data:
            reporter_list.append(i["ReporterKey"])
        
        del driver.requests
        time.sleep(1)

        # 판독의 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/li[2]").click()
        driver.wait_for_request('.*/GetReferCountsByReporter')
        time.sleep(0.3)
        
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
                    time.sleep(0.3)
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]
                    temp_cnt = 0                    
                    for i in data:              
                        if i['ScheduleDate'] != None:
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
        del driver.requests
        time.sleep(1)

        # 판독의 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/li[2]/a").click()

        # Repoter list 저장
        request = driver.wait_for_request('.*/GetReferCountsByReporter.*')
        time.sleep(0.3)
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
            time.sleep(0.3)
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
                time.sleep(0.3)
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
        # 새로고침
        driver.refresh()

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
                time.sleep(1)
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]").click()
        
                # 병원 선택 > All Assigned List > Priority 드랍박스에서 응급을 선택 후, Search 버튼 클릭
                time.sleep(1)
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div").click()                
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/ul/li[2]").click()
                del driver.requests
                time.sleep(1)
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

                # 병원 선택 > All Assigned List > Job list 저장
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/GetAllAssignedList.*')
                    time.sleep(0.3)
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
                time.sleep(0.5)
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[2]").click()
                
                # 병원 선택 > Not Assigned List > Job list 저장
                time.sleep(1)
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/GetNotAssignedList.*')
                    time.sleep(0.3)
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
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]")))
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
                time.sleep(1)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/a").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div/ul/li["+str(n+2)+"]").click()

                # 병원 선택 > All Assigned List > Priority 드랍박스에서 일반 선택 후, Search 버튼 클릭
                time.sleep(1)
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div").click()                
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/ul/li[3]").click()
                del driver.requests
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

                # 병원 선택 > All Assigned List > Job list 저장
                request = driver.wait_for_request('.*/GetAllAssignedList.*')
                time.sleep(0.3)
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
                    time.sleep(0.3)
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
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[1]")))
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
        # 새로고침
        driver.refresh()
        # All List 탭 클릭
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)

        driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)

        # All List > Job Status를 Requested로 변경하고, Search All 버튼 클릭
        time.sleep(1)
        del driver.requests
        time.sleep(1)

        # All List 탭 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()
        driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)

        del driver.requests
        time.sleep(1)

        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[2]").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[6]/button").click()

        # All List > Job list의 Job Status 저장
        pages = Common.cnt_pages()
        job_status = []
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.3)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

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
        job_status = []
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.3)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

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
        job_status = []
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.3)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

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
        job_status = []
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]
            
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
        time.sleep(0.3)
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
        job_status = []
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.3)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

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
        job_status = []
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

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
        job_status = []
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

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
        job_status = []
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

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
        job_status = []
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

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
        job_status = []
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

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
        job_status = []
        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

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

        # 새로고침
        driver.refresh()

        # 1 steps start! : Date를 Job Date로 선택하고, 임의의 기간을 입력한 후, Search 버튼을 클릭한다.
        # 2 steps start! : Date를 Study Date로 선택하고, 임의의 기간을 입력한 후, Search 버튼을 클릭한다.
        # 3 steps start! : Date를 Schedule Date로 선택하고, 임의의 기간을 입력한 후, Search 버튼을 클릭한다.
        # Test 병원을 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
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
            job_date = []
            while pages > 0:
                time.sleep(1)
                request = driver.wait_for_request('.*/GetAllAssignedList.*')
                time.sleep(0.5)
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

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
                    assert int((Var.today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or job_date == ''
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
            job_date = []
            while pages > 0:
                time.sleep(1)
                request = driver.wait_for_request('.*/GetAllAssignedList.*')
                time.sleep(0.5)
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

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
                assert job_date == str(Var.today.strftime('%Y-%m-%d')) or job_date == ''
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
                job_date = []
                while pages > 0:
                    time.sleep(1)
                    request = driver.wait_for_request('.*/GetAllAssignedList.*')
                    time.sleep(0.5)
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]

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
                        assert int((Var.today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or int(str(((Var.today - timedelta(weeks=(n-1))) - datetime.strptime(i, '%Y-%m-%d'))).split()[0]) <= 0
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
                job_date = []

                while pages > 0:
                    request = driver.wait_for_request('.*/GetAllAssignedList.*')
                    time.sleep(0.5)
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]

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
                            assert int((Var.today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or int(str((Var.today - relativedelta(months=1)) - datetime.strptime(i, '%Y-%m-%d')).split()[0]) <= 0
                        else:
                            assert int((Var.today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or int(str(((Var.today - relativedelta(months=(3*m))) - datetime.strptime(i, '%Y-%m-%d'))).split()[0]) <= 0
                            
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
            job_date = []

            while pages > 0:
                time.sleep(1)
                request = driver.wait_for_request('.*/GetNotAssignedList.*')
                time.sleep(0.5)
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

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
                    assert int((Var.today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or job_date == ''
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
            job_date = []

            while pages > 0:
                time.sleep(1)
                request = driver.wait_for_request('.*/GetNotAssignedList.*')
                time.sleep(0.5)
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

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
                assert job_date == str(Var.today.strftime('%Y-%m-%d')) or job_date == ''
            except:
                testResult = "failed"
                reason.append(j +" steps failed\n")

            # Not Assigned List > Job Date를 last 1~4 week으로 선택
            for n in range(2,7):
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[4]/div/div[1]/input")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[4]/div/div[1]/input").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(2) > th:nth-child("+str(n)+")")))
                driver.find_element(By.CSS_SELECTOR, "body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-bottom > div.datepicker-days > table > tfoot > tr:nth-child(2) > th:nth-child("+str(n)+")").click()

                # Search 버튼 클릭
                time.sleep(1)
                del driver.requests
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

                # Showing entries 100으로 변경
                Common.refer_show_entries(100)
                
                # Not Assigned List > Job list의 결과 저장
                time.sleep(1)
                pages = Common.cnt_pages()
                job_date = []

                while pages > 0:
                    time.sleep(1)
                    request = driver.wait_for_request('.*/GetNotAssignedList.*')
                    time.sleep(0.5)
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]

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
                        assert int((Var.today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or int(str(((Var.today - timedelta(weeks=(n-1))) - datetime.strptime(i, '%Y-%m-%d'))).split()[0]) <= 0
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
                job_date = []

                while pages > 0:
                    request = driver.wait_for_request('.*/GetNotAssignedList.*')
                    time.sleep(0.5)
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)["data"]

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
                            assert int((Var.today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or int(str((Var.today - relativedelta(months=1)) - datetime.strptime(i, '%Y-%m-%d')).split()[0]) <= 0
                        else:
                            assert int((Var.today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or int(str(((Var.today - relativedelta(months=(3*m))) - datetime.strptime(i, '%Y-%m-%d'))).split()[0]) <= 0
                            
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
        job_date = []

        while pages > 0:
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

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
                assert int((Var.today - datetime.strptime(i, '%Y-%m-%d')).days) >= 0 or int(str((Var.today - relativedelta(years=1)) - datetime.strptime(i, '%Y-%m-%d')).split()[0]) <= 0
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

        # 새로고침
        driver.refresh()

        # 1 steps start! : Patient Location 조건을 InPatient로 선택한 후, Search 버튼을 클릭한다.
        # 2 steps start! : Patient Location 조건을 OutPatient로 선택한 후, Search 버튼을 클릭한다.
        # 3 steps start! : Patient Location 조건을 Emergency로 선택한 후, Search 버튼을 클릭한다.
        location_type = [['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[5]/div/div/ul/li[2]','I'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[5]/div/div/ul/li[3]','O'],
        ['/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[5]/div/div/ul/li[4]','E']]

        # All List 탭 클릭
        time.sleep(2)
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
                time.sleep(0.5)
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

        # 새로고침
        driver.refresh()

        # Refer 탭 클릭(화면 초기화)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
        
        # 1 steps start! : 임의의 Patient ID를 입력하고 Search 버튼을 클릭한다.
        # Test 병원을 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
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
                time.sleep(1)
                driver.find_element(By.XPATH, tab_list[i][0]).click()
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                    time.sleep(0.5)
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
                if pat_id != None:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div/input").send_keys(pat_id)
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                # Patient ID가 모두 Null 인 경우
                else:
                    break
            else:
                break

        # 검색한 Patient ID와 Job list의 결과와 비교
        try:
            if pat_id != None:
                result_pat_id = ' '.join(s for s in result_pat_id)
            assert pat_id == result_pat_id or pat_id == None
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
            time.sleep(0.5)
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
            if pat_id != None:
                result_pat_id = ' '.join(s for s in result_pat_id)
            assert pat_id == result_pat_id or pat_id == None
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

        # 새로고침
        driver.refresh()

        # Refer 탭 클릭(화면 초기화)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
        
        # 1 steps start! : 임의의 Patient Name을 입력하고 Search 버튼을 클릭한다.
        # Test 병원을 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
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
                time.sleep(1)
                driver.find_element(By.XPATH, tab_list[i][0]).click()
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                    time.sleep(0.5)
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
                if pat_name != None:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/input").send_keys(pat_name)
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                # Patient_Name이 모두 Null 인 경우
                else:
                    break
            else:
                break

        # 검색한 Patient Name과 Job list의 결과와 비교
        try:
            if pat_name != None:
                result_pat_name = ' '.join(s for s in result_pat_name)
            assert pat_name == result_pat_name or pat_name == None
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
            time.sleep(0.5)
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
            if (pat_name) != None:
                result_pat_name = ' '.join(s for s in result_pat_name)
            assert pat_name == result_pat_name or (pat_name) == None
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

        # 새로고침
        driver.refresh()

        # Refer 탭 클릭(화면 초기화)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : Age 조건을 Year로 선택하고, 임의의 나이를 입력한 후, Search 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
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
                time.sleep(0.5)
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
                time.sleep(0.5)
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
                time.sleep(0.5)
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

        # 새로고침
        driver.refresh()

        # Refer 탭 클릭(화면 초기화)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : 임의의 Study Description을 입력한 후, Search 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
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
                time.sleep(1)
                driver.find_element(By.XPATH, tab_list[i][0]).click()
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                    time.sleep(0.5)
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
                if (study_desc) != None:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div/div/input").send_keys(study_desc)
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                # Study Description이 모두 Null 인 경우
                else:
                    break
            else:
                break

        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            if (study_desc) != None:
                result_study_desc = ' '.join(s for s in result_study_desc)
            assert study_desc == result_study_desc or (study_desc) == None
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

        # 새로고침
        driver.refresh()

        # Refer 탭 클릭(화면 초기화)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : 임의의 Modality를 입력한 후, Search 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
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
                time.sleep(1)
                driver.find_element(By.XPATH, tab_list[i][0]).click()
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                    time.sleep(0.5)
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
                if (modality) != None:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div/div/input").send_keys(modality)
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                # Modality가 모두 Null 인 경우
                else:
                    break
            else:
                break

        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            if (modality) != None:
                result_modality = ' '.join(s for s in result_modality)
            assert modality == result_modality or (modality) == None
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
        
        del driver.requests
        time.sleep(1)

        # 새로고침
        driver.refresh()

        driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)

        del driver.requests
        time.sleep(1)
        # Refer 탭 클릭(화면 초기화)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : 임의의 Bodypart를 입력한 후, Search 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()

        driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)

        del driver.requests
        time.sleep(1)

        # Showing entries 100으로 변경
        Common.refer_show_entries(100)
        try:
            driver.wait_for_request('.*/GetAllAssignedList.*')
            time.sleep(0.3)
        except:
            Common.refer_show_entries(10)

            driver.wait_for_request('.*/GetAllAssignedList.*')
            time.sleep(0.3)

            del driver.requests
            time.sleep(1)

            Common.refer_show_entries(100)
            driver.wait_for_request('.*/GetAllAssignedList.*')
            time.sleep(0.3)
        
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
                time.sleep(1)
                driver.find_element(By.XPATH, tab_list[i][0]).click()
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                    time.sleep(0.5)
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
                if (bodypart) != None:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[3]/div/div/input").send_keys(bodypart)
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                # Bodypart가 모두 Null 인 경우
                else:
                    break
            else:
                break

        # 검색 조건과 Job list 결과가 일치하는지 확인
        time.sleep(1.5)
        try:
            if (bodypart) != None:
                result_bodypart = ' '.join(s for s in result_bodypart)
            assert bodypart == result_bodypart or (bodypart) == None
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

        # 새로고침
        driver.refresh()

        # Refer 탭 클릭(화면 초기화)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : 임의의 Department를 입력한 후, Search 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
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
                time.sleep(1)
                driver.find_element(By.XPATH, tab_list[i][0]).click()
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                    time.sleep(0.5)
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
                if (department) != None:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[4]/div/div/input").send_keys(department)
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                # Department가 모두 Null 인 경우
                else:
                    break
            else:
                break
                
        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            if (department) != None:
                result_department = ' '.join(s for s in result_department)
            assert department == result_department or (department) == None
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
        
        # 새로고침
        driver.refresh()

        # Refer 탭 클릭(화면 초기화)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : 임의의 Request Name을 입력한 후, Search 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
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
                time.sleep(1)
                driver.find_element(By.XPATH, tab_list[i][0]).click()
                pages = Common.cnt_pages()
                while pages > 0:
                    request = driver.wait_for_request('.*/'+tab_list[i][1]+'.*')
                    time.sleep(0.5)
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
                if (request_name) != None:
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[5]/div/div/input").send_keys(request_name)
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()
                # Department가 모두 Null 인 경우
                else:
                    break
            else:
                break
            
        # 검색 조건과 Job list 결과가 일치하는지 확인
        try:
            if (request_name) != None:
                result_request_name = ' '.join(s for s in result_request_name)
            assert request_name == result_request_name or (request_name) == None
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
        
        # 새로고침
        driver.refresh()

        # Refer 탭 클릭(화면 초기화)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()
        time.sleep(1)

        # 1 steps start! : 임의의 검색조건을 입력한 후, Search All 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
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
                time.sleep(0.5)
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
        if (search_item_1) != None:
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
                time.sleep(0.5)
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
        if (search_item_2) != None:
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
                time.sleep(0.5)
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
        
        # 새로고침
        driver.refresh()

        # Refer 탭 클릭(화면 초기화)
        # driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[3]").click()

        # 1 steps start! : Real Time 토글 버튼을 On으로 변경한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()

        # All List 탭으로 이동
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # Show entries를 50개로 변경
        time.sleep(1)
        del driver.requests
        time.sleep(1)
        Common.refer_show_entries(50)

        # Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        # Ream Time 토글을 On으로 변경
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[2]/div/div[2]/label/span").click()
        status = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[2]/div/div[2]/label/input").get_property("checked")

        # 35초 대기(자동 새로고침 시간: 30초) 및 기존 데이터 삭제
        time.sleep(35)
        del driver.requests

        # Show entries를 10개로 변경
        time.sleep(1)
        Common.refer_show_entries(10)

        # Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)
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
        time.sleep(0.5)
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
            time.sleep(0.5)
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

        del driver.requests
        time.sleep(1)

        # 새로고침
        driver.refresh()
        
        driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)

        del driver.requests
        time.sleep(1)

        # 1 steps start! : 임의의 검색조건을 입력한 후, Short cut 버튼을 클릭한다.
        # Test 병원 선택
        hospital_list = driver.find_elements(By.CLASS_NAME, "list-group-item.list-institution")
        time.sleep(1)
        for i in hospital_list:
            if (i.get_property("dataset"))["institutionName"] == Var.test_hospital:
                i.click()

        driver.wait_for_request('.*/GetAllAssignedList.*')
        time.sleep(0.3)

        # 검색할 항목을 리스트로 생성
        search_list = [['StudyDesc','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div/div/input'],
        ['Modality','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div/div/input'],
        ['Bodypart','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[3]/div/div/input'],
        ['Department','/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[4]/div/div/input']]
        search_item = random.choice(search_list)
        
        del driver.requests
        time.sleep(1)

        # All List 탭 클릭
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]")))
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # Job list에서 임의의 검색할 항목을 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        search_sample = []

        for i in data:
            if i[search_item[0]] not in search_sample and (i[search_item[0]]) != None:
                search_sample.append(i[search_item[0]])
        search_sample = random.choice(search_sample)

        del driver.requests
        time.sleep(1)

        # Job list에서 임의의 값으로 검색
        driver.find_element(By.XPATH, search_item[1]).send_keys(search_sample)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button")))
        time.sleep(0.3)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[6]/button").click()

        request = driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)

        # Short cut 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()
        time.sleep(1)
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
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()

        # Title 작성 후, Save 버튼 클릭
        test_shortcut_title = 'TEST' + str(random.randrange(0,1000))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(str(test_shortcut_title))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        time.sleep(0.3)
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
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/ul/li/a/i").click()

        # 임의의 Title을 입력
        test_shortcut_title = 'TEST' + str(random.randrange(0,1000))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(str(test_shortcut_title))

        # Save Insititution 체크 후, Save 버튼 클릭
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[3]/label").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        time.sleep(0.3)
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
        time.sleep(1)
        test_shortcut_title = 'TEST' + str(random.randrange(0,1000))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(test_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        time.sleep(0.3)
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
        time.sleep(1)

        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(random_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut 추가 후, Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        time.sleep(1)
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
        time.sleep(1)
        test_shortcut_title = 'TEST' + str(random.randrange(0,1000))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(test_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        time.sleep(0.3)
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
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[13]/div/div/div[3]/button[1]").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        time.sleep(0.3)
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
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]/span/button")))
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
        time.sleep(1)
        test_shortcut_title = 'TEST' + str(random.randrange(0,1000))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(test_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        time.sleep(0.3)
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
        time.sleep(1)
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
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[1]/ul/li[3]").click()

        # Job list 저장
        request = driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.3)
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
        time.sleep(0.3)
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
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li/div/span")))

        # Short cut list를 저장하기 위해 Short cut 생성
        time.sleep(1)
        del driver.requests
        time.sleep(1)
        test_shortcut_title = 'TEST' + str(random.randrange(0,1000))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[1]/div/input").send_keys(test_shortcut_title)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/div[2]/button").click()

        # Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        time.sleep(0.3)
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
            time.sleep(0.5)
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
        time.sleep(0.5)
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
        time.sleep(0.5)
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
        time.sleep(0.5)
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
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        before_shortcut_list = []

        for i in data:
            before_shortcut_list.append(i["Title"])
        
        # 추가한 short cut 삭제
        time.sleep(1)
        del driver.requests
        time.sleep(1)
        index = before_shortcut_list.index(test_shortcut_title)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]/span/button")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/section/aside/div/div/div[1]/ul/li["+str(int(index)+2)+"]/span/button").click()

        # 삭제 후, Short cut list 저장
        request = driver.wait_for_request('.*/GetReferSearchCondition.*')
        time.sleep(0.3)
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
        result = ' '.join(s for s in reason)
        print("Test Result: Pass" if testResult != "failed" else testResult)
        if testResult == 'failed':
            testlink.reportTCResult(1651, testPlanID, buildName, 'f', result)
        else:
            testlink.reportTCResult(1651, testPlanID, buildName, 'p', "Short cut Passed")
