from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
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
import Common_Var

class Statistics:
    def SearchFilter_Date():
        print("ITR-44: Statistics > Search Filter > Date")
        run_time = time.time()
        testResult = ''
        reason = list()

        # 새로고침
        driver.refresh()

        # DB 접속
        os.putenv('NLS_LANG', '.UTF8')
        cx_Oracle.init_oracle_client(lib_dir=r"D:\app\user\instantclient_21_7")
        connection = cx_Oracle.connect("pantheon","pantheon",Var.staging_tns, encoding="UTF-8")
        cursor = connection.cursor()

        # Staging Admin으로 탭 전환
        driver.execute_script("window.open()")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(Var.StagingAdmin)

        ITR_Admin_Login.signInOut.stg_admin_sign_in()

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
        end_date = str(Var.today.strftime('%Y%m%d'))
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
        end_date = str(Var.today.strftime('%Y%m%d'))
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
        end_date = str(Var.today.strftime('%Y%m%d'))
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
            time.sleep(1)
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
        end_date = str(Var.today.strftime('%Y%m%d'))
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
        close_month = int(Var.today.strftime('%m')) - 2
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
        end_date = str(Var.today.strftime('%Y%m%d'))
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
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1772, testPlanID, buildName, 'f', result)
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1772, testPlanID, buildName, 'p', "Search Filter > Date Passed")  

    def SearchFilter_Hospital():
        print("ITR-45: Statistics > Search Filter > Hospital")
        run_time = time.time()
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
        end_date = str(Var.today.strftime('%Y%m%d'))
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
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1779, testPlanID, buildName, 'f', result)
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1779, testPlanID, buildName, 'p', "Search Filter > Hospital Passed")  

    def SearchFilter_Reporter():
        print("ITR-46: Statistics > Search Filter > Reporter")
        run_time = time.time()
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
        end_date = str(Var.today.strftime('%Y%m%d'))
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
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1782, testPlanID, buildName, 'f', result)
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1782, testPlanID, buildName, 'p', "Search Filter > Reporter Passed")  

    def SearchFilter_Modality():
        print("ITR-47: Statistics > Search Filter > Modality")
        run_time = time.time()
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
        end_date = str(Var.today.strftime('%Y%m%d'))
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
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1785, testPlanID, buildName, 'f', result)
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1785, testPlanID, buildName, 'p', "Search Filter > Modality Passed")  

    def Columns():
        # Statistics 탭 클릭
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[1]/ul/li[4]").click()

        print("ITR-42: Statistics > Columns")
        run_time = time.time()
        testResult = ''
        reason = list()

        # 1 steps start! : Columns 버튼을 클릭한다.
        # 페이지 초기화
        driver.refresh()

        # Columns 클릭
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/button").click()
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#modal_statistics_columns_setting > div > div > div.modal-header.modal-col-teal > h4")))

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
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1759, testPlanID, buildName, 'f', result)
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1759, testPlanID, buildName, 'p', "Columns Passed")  

    def Show_Entries():
        print("ITR-43: Statistics > Show entries")
        run_time = time.time()
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
        # hospital_list = driver.find_elements(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/ul/li")
        # hospital_cnt = len(hospital_list) - 1
        hospital_cnt = driver.find_element(By.CSS_SELECTOR, "#statistics-hospital-list-drop-box > ul").get_property("childElementCount")

        # for i in range(2, hospital_cnt):
        for i in range(1, hospital_cnt+1):
            temp_hospital_cnt_list.append(i)
        
        # 조회 결과가 100개를 초과할 때까지 임의의 병원을 찾아서 조회
        while int(list_cnt) < 100:
            # 임의의 병원 선택
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/ul")))
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/ul").click()
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
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1765, testPlanID, buildName, 'f', result)
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1765, testPlanID, buildName, 'p', "Show entries Passed")  
        
        # 탭 종료 및 vmonpacs로 전환
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
