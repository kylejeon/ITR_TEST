from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import time
import json
from ITR_Admin_Common import driver
from ITR_Admin_Common import testlink
from ITR_Admin_Common import testPlanID
from ITR_Admin_Common import buildName
from ITR_Admin_Common import Common
import Common_Var
import ITR_Admin_Login

class Auditlog:
    def Auditlog_Search():
        print("ITR-98: Audit Log > Search")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        try:
            if driver.find_element(By.CSS_SELECTOR, "#user-id").get_attribute("name") == "userId":
                time.sleep(0.5)
                ITR_Admin_Login.signInOut.stg_admin_sign_in()
            else:
                Common.ReFresh()
        except:
            Common.ReFresh()

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

        # Auditlog_Search결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2169, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2169, testPlanID, buildName, 'p', "Auditlog_Search Test Passed")

    def Auditlog_Export():
        print("ITR-99: Audit Log > Export")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        try:
            if driver.find_element(By.CSS_SELECTOR, "#user-id").get_attribute("name") == "userId":
                time.sleep(0.5)
                ITR_Admin_Login.signInOut.stg_admin_sign_in()
            else:
                Common.ReFresh()
        except:
            Common.ReFresh()

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

        # Auditlog_Export결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2172, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2172, testPlanID, buildName, 'p', "Auditlog_Export Test Passed")

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
        print("ITR-100: Audit Log > Show Entries")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        try:
            if driver.find_element(By.CSS_SELECTOR, "#user-id").get_attribute("name") == "userId":
                time.sleep(0.5)
                ITR_Admin_Login.signInOut.stg_admin_sign_in()
            else:
                Common.ReFresh()
        except:
            Common.ReFresh()

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

        # Auditlog_Showentries결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2175, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2175, testPlanID, buildName, 'p', "Auditlog_Showentries Test Passed")

    def Auditlog_Sorting():
        print("ITR-101: Audit Log > Sorting")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        try:
            if driver.find_element(By.CSS_SELECTOR, "#user-id").get_attribute("name") == "userId":
                time.sleep(0.5)
                ITR_Admin_Login.signInOut.stg_admin_sign_in()
            else:
                Common.ReFresh()
        except:
            Common.ReFresh()

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

        # Auditlog_Sorting결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2180, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2180, testPlanID, buildName, 'p', "Auditlog_Sorting Test Passed")

    def Auditlog_Data():
        print("ITR-102: Audit Log > Data")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        try:
            if driver.find_element(By.CSS_SELECTOR, "#user-id").get_attribute("name") == "userId":
                time.sleep(0.5)
                ITR_Admin_Login.signInOut.stg_admin_sign_in()
            else:
                Common.ReFresh()
        except:
            Common.ReFresh()

        # Auditlog
        driver.find_element(By.CSS_SELECTOR, "#tab-auditlog > a").click()
        driver.implicitly_wait(5)

        del driver.requests
        time.sleep(0.25)

        # Search
        driver.find_element(By.CSS_SELECTOR, "#auditlog_search_job_key_field").send_keys("74832064")
        driver.find_element(By.CSS_SELECTOR, "#auditlog_search").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#auditlog_search")))

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

        # Auditlog_Data결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2183, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2183, testPlanID, buildName, 'p', "Auditlog_Data Test Passed")
