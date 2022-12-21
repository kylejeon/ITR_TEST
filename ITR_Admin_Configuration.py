from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import math
from dateutil.relativedelta import relativedelta
import random
import json
from ITR_Admin_Common import driver
from ITR_Admin_Common import testlink
from ITR_Admin_Common import testPlanID
from ITR_Admin_Common import buildName
from ITR_Admin_Common import Var
from ITR_Admin_Common import Common
from ITR_Admin_Login import signInOut
import Common_Var

class UserManagement:
    def SearchFilter_Class():
        print("ITR-49: Configuration > User Management > Search Filter > Class")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)
        
        request = driver.wait_for_request('.*/GetUserList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        select_class = data[0]["ClassCode"]

        del driver.requests
        time.sleep(1)
        
        # Select Class Search #1
        driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > a > span").click()
        for n in range(1,7):
            if driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul > li:nth-child("+str(n)+")").text == select_class:
                driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul > li:nth-child("+str(n)+")").click()
                break
        driver.find_element(By.CSS_SELECTOR, "#user-search").click()

        request = driver.wait_for_request('.*/GetUserList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        for n in range(0, len(data)):
            if (data[n]["ClassCode"] != select_class or
                driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(4)").text != data[n]["ClassCode"]):
                testResult = False
                Result_msg += "#1 "

        # SearchFilter_Class결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1797, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1797, testPlanID, buildName, 'p', "SearchFilter_Class Test Passed")

    def SearchFilter_Institution():
        print("ITR-50: Configuration > User Management > Search Filter > Institution")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)
        
        request = driver.wait_for_request('.*/GetUserList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        select_insti = ""
        for a in range(0, total):
            request = driver.wait_for_request('.*/GetUserList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in range(1, len(data)+1):
                del driver.requests
                time.sleep(1)
                    
                # Select
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(n)+"]/td[2]/a").click()
                driver.wait_for_request('.*/GetUserModifyData.*')
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-close-btn")))
                if driver.find_element(By.CSS_SELECTOR, "#user_add_institution_chosen > a > span").text != "None":
                    select_insti = driver.find_element(By.CSS_SELECTOR, "#user_add_institution_chosen > a > span").text
                    # Close
                    element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
                    driver.execute_script("arguments[0].click()",element)
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                    # Yes
                    driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                    break
                # Close
                element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
                driver.execute_script("arguments[0].click()",element)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                # Yes
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            if (a+1 == total or
                select_insti != ""):
                break

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#user-list_next > a").click()

        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        del driver.requests
        time.sleep(1)

        # Select Institution Search #1
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user_search_institution_chosen > a > span")))
        driver.find_element(By.CSS_SELECTOR, "#user_search_institution_chosen > a > span").click()
        child = driver.find_element(By.CSS_SELECTOR, "#user_search_institution_chosen > div > ul").get_property("childElementCount")
        for n in range(1, child+1):
            if driver.find_element(By.CSS_SELECTOR, "#user_search_institution_chosen > div > ul > li:nth-child("+str(n)+")").text == select_insti:
                driver.find_element(By.CSS_SELECTOR, "#user_search_institution_chosen > div > ul > li:nth-child("+str(n)+")").click()
                WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#user_search_institution_chosen > a > span"), select_insti))
                break
        element = driver.find_element(By.CSS_SELECTOR, "#user-search")
        driver.execute_script("arguments[0].click()",element)

        request = driver.wait_for_request('.*/GetUserList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        for n in range(1, len(data)+1):
            del driver.requests
            time.sleep(1)

            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(n)+"]/td[2]/a").click()
            driver.wait_for_request('.*/GetUserModifyData.*')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-close-btn")))

            if driver.find_element(By.CSS_SELECTOR, "#user_add_institution_chosen > a > span").text != select_insti:
                testResult = False
                Result_msg += "#1 "
                # Close
                element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
                driver.execute_script("arguments[0].click()",element)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                # Yes
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                break

            # Close
            element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
            driver.execute_script("arguments[0].click()",element)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # Yes
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # SearchFilter_Institution결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1800, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1800, testPlanID, buildName, 'p', "SearchFilter_Institution Test Passed")

    def SearchFilter_UserID():
        print("ITR-51: Configuration > User Management > Search Filter > User ID")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)
        
        request = driver.wait_for_request('.*/GetUserList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        select_insti = ""
        for a in range(0, total):
            request = driver.wait_for_request('.*/GetUserList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in range(1, len(data)+1):
                del driver.requests
                time.sleep(1)
                    
                # Select
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(n)+"]/td[2]/a").click()
                driver.wait_for_request('.*/GetUserModifyData.*')
                time.sleep(0.5)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-close-btn")))
                if driver.find_element(By.CSS_SELECTOR, "#user_add_institution_chosen > a > span").text != "None":
                    select_user = driver.find_element(By.CSS_SELECTOR, "#user-add-id").get_property("value")
                    select_class = driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > a > span").text
                    select_insti = driver.find_element(By.CSS_SELECTOR, "#user_add_institution_chosen > a > span").text
                    # Close
                    element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
                    driver.execute_script("arguments[0].click()",element)
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                    # Yes
                    driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                    break
                # Close
                element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
                driver.execute_script("arguments[0].click()",element)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                # Yes
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            if (a+1 == total or
                select_insti != ""):
                break

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#user-list_next > a").click()

        del driver.requests
        time.sleep(1)

        # User ID Search #1
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-id").send_keys(select_user)
        element = driver.find_element(By.CSS_SELECTOR, "#user-search")
        driver.execute_script("arguments[0].click()",element)

        request = driver.wait_for_request('.*/GetUserList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        for n in range (0, len(data)):
            if (select_user not in data[n]["UserID"] or
                data[n]["UserID"] != driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(2)").get_property("textContent")):
                testResult = False
                break

        del driver.requests
        time.sleep(1)

        if testResult == True:
            # class
            driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > a > span").click()
            child = driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul").get_property("childElementCount")
            for n in range(1, child+1):
                if driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul > li:nth-child("+str(n)+")").text == select_class:
                    driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul > li:nth-child("+str(n)+")").click()
                    break
            driver.find_element(By.CSS_SELECTOR, "#user-search").click()

            request = driver.wait_for_request('.*/GetUserList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in range(0, len(data)):
                if (select_user not in data[n]["UserID"] or
                    data[n]["UserID"] != driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(2)").get_property("textContent") or
                    data[n]["ClassCode"] != select_class or 
                    data[n]["ClassCode"] != driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(4)").text):
                    testResult = False
                    break

            driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul > li:nth-child(1)").click()
           
        del driver.requests
        time.sleep(1)

        if testResult == True:
            # institution
            driver.find_element(By.CSS_SELECTOR, "#user_search_institution_chosen > a > span").click()
            child = driver.find_element(By.CSS_SELECTOR, "#user_search_institution_chosen > div > ul").get_property("childElementCount")
            for n in range(1, child+1):
                if driver.find_element(By.CSS_SELECTOR, "#user_search_institution_chosen > div > ul > li:nth-child("+str(n)+")").text == select_insti:
                    driver.find_element(By.CSS_SELECTOR, "#user_search_institution_chosen > div > ul > li:nth-child("+str(n)+")").click()
                    break
            driver.find_element(By.CSS_SELECTOR, "#user-search").click()

            request = driver.wait_for_request('.*/GetUserList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in range(0, len(data)):
                if (select_user not in data[n]["UserID"] or
                    data[n]["UserID"] != driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(2)").get_property("textContent")):                    
                    testResult = False
                    break

            if testResult == True:
                for n in range(1, len(data)+1):
                    del driver.requests
                    time.sleep(1)

                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(n)+"]/td[2]/a").click()
                    driver.wait_for_request('.*/GetUserModifyData.*')
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-close-btn")))

                    if driver.find_element(By.CSS_SELECTOR, "#user_add_institution_chosen > a > span").text != select_insti:
                        testResult = False
                        # Close
                        element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
                        driver.execute_script("arguments[0].click()",element)
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                        # Yes
                        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                        break

                    # Close
                    element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
                    driver.execute_script("arguments[0].click()",element)
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                    # Yes
                    driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        if testResult == True:
            # class & institution
            driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > a > span").click()
            child = driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul").get_property("childElementCount")
            for n in range(1, child+1):
                if driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul > li:nth-child("+str(n)+")").text == select_class:
                    driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul > li:nth-child("+str(n)+")").click()
                    break
            driver.find_element(By.CSS_SELECTOR, "#user-search").click()

            request = driver.wait_for_request('.*/GetUserList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in range(0, len(data)):
                if (select_user not in data[n]["UserID"] or
                    data[n]["UserID"] != driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(2)").get_property("textContent") or
                    data[n]["ClassCode"] != select_class or 
                    data[n]["ClassCode"] != driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(4)").text):
                    testResult = False
                    break

            if testResult == True:
                for n in range(1, len(data)+1):
                    del driver.requests
                    time.sleep(1)

                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(n)+"]/td[2]/a").click()
                    driver.wait_for_request('.*/GetUserModifyData.*')
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-close-btn")))

                    if driver.find_element(By.CSS_SELECTOR, "#user_add_institution_chosen > a > span").text != select_insti:
                        testResult = False
                        # Close
                        element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
                        driver.execute_script("arguments[0].click()",element)
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                        # Yes
                        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                        break

                    # Close
                    element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
                    driver.execute_script("arguments[0].click()",element)
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                    # Yes
                    driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        if testResult == False:
            Result_msg += "#1 "

        # SearchFilter_UserID결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1803, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1803, testPlanID, buildName, 'p', "SearchFilter_UserID Test Passed")

    def SearchFilter_UserName():
        print("ITR-52: Configuration > User Management > Search Filter > User Name")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)
        
        request = driver.wait_for_request('.*/GetUserList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        select_insti = ""
        for a in range(0, total):
            request = driver.wait_for_request('.*/GetUserList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in range(1, len(data)+1):
                del driver.requests
                time.sleep(1)
                    
                # Select
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(n)+"]/td[2]/a").click()
                driver.wait_for_request('.*/GetUserModifyData.*')
                time.sleep(0.5)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-close-btn")))
                if driver.find_element(By.CSS_SELECTOR, "#user_add_institution_chosen > a > span").text != "None":
                    select_user = driver.find_element(By.CSS_SELECTOR, "#user-add-name").get_property("value")
                    select_class = driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > a > span").text
                    select_insti = driver.find_element(By.CSS_SELECTOR, "#user_add_institution_chosen > a > span").text
                    # Close
                    element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
                    driver.execute_script("arguments[0].click()",element)
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                    # Yes
                    time.sleep(0.5)
                    driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                    break
                # Close
                element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
                driver.execute_script("arguments[0].click()",element)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                # Yes
                time.sleep(0.5)
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            if (a+1 == total or
                select_insti != ""):
                break

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#user-list_next > a").click()

        del driver.requests
        time.sleep(1)

        # User ID Search #1
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-name").send_keys(select_user)
        element = driver.find_element(By.CSS_SELECTOR, "#user-search")
        driver.execute_script("arguments[0].click()",element)

        request = driver.wait_for_request('.*/GetUserList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        for n in range (0, len(data)):
            if (select_user not in data[n]["UserName"] or
                data[n]["UserName"] != driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(3)").get_property("textContent")):
                testResult = False
                break

        del driver.requests
        time.sleep(1)

        if testResult == True:
            # class
            driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > a > span").click()
            child = driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul").get_property("childElementCount")
            for n in range(1, child+1):
                if driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul > li:nth-child("+str(n)+")").text == select_class:
                    driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul > li:nth-child("+str(n)+")").click()
                    break
            driver.find_element(By.CSS_SELECTOR, "#user-search").click()

            request = driver.wait_for_request('.*/GetUserList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in range(0, len(data)):
                if (select_user not in data[n]["UserName"] or
                    data[n]["UserName"] != driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(3)").get_property("textContent") or
                    data[n]["ClassCode"] != select_class or 
                    data[n]["ClassCode"] != driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(4)").text):
                    testResult = False
                    break

            driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul > li:nth-child(1)").click()
           
        del driver.requests
        time.sleep(1)

        if testResult == True:
            # institution
            driver.find_element(By.CSS_SELECTOR, "#user_search_institution_chosen > a > span").click()
            child = driver.find_element(By.CSS_SELECTOR, "#user_search_institution_chosen > div > ul").get_property("childElementCount")
            for n in range(1, child+1):
                if driver.find_element(By.CSS_SELECTOR, "#user_search_institution_chosen > div > ul > li:nth-child("+str(n)+")").text == select_insti:
                    driver.find_element(By.CSS_SELECTOR, "#user_search_institution_chosen > div > ul > li:nth-child("+str(n)+")").click()
                    break
            driver.find_element(By.CSS_SELECTOR, "#user-search").click()

            request = driver.wait_for_request('.*/GetUserList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in range(0, len(data)):
                if (select_user not in data[n]["UserName"] or
                    data[n]["UserName"] != driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(3)").get_property("textContent")):                    
                    testResult = False
                    break

            if testResult == True:
                for n in range(1, len(data)+1):
                    del driver.requests
                    time.sleep(1)

                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(n)+"]/td[2]/a").click()
                    driver.wait_for_request('.*/GetUserModifyData.*')
                    time.sleep(0.5)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-close-btn")))

                    if driver.find_element(By.CSS_SELECTOR, "#user_add_institution_chosen > a > span").text != select_insti:
                        testResult = False
                        # Close
                        element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
                        driver.execute_script("arguments[0].click()",element)
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                        # Yes
                        time.sleep(0.5)
                        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                        break

                    # Close
                    element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
                    driver.execute_script("arguments[0].click()",element)
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                    # Yes
                    time.sleep(0.5)
                    driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        if testResult == True:
            # class & institution
            driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > a > span").click()
            child = driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul").get_property("childElementCount")
            for n in range(1, child+1):
                if driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul > li:nth-child("+str(n)+")").text == select_class:
                    driver.find_element(By.CSS_SELECTOR, "#user_search_class_chosen > div > ul > li:nth-child("+str(n)+")").click()
                    break
            driver.find_element(By.CSS_SELECTOR, "#user-search").click()

            request = driver.wait_for_request('.*/GetUserList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in range(0, len(data)):
                if (select_user not in data[n]["UserName"] or
                    data[n]["UserName"] != driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(3)").get_property("textContent") or
                    data[n]["ClassCode"] != select_class or 
                    data[n]["ClassCode"] != driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(4)").text):
                    testResult = False
                    break

            if testResult == True:
                for n in range(1, len(data)+1):
                    del driver.requests
                    time.sleep(1)

                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(n)+"]/td[2]/a").click()
                    driver.wait_for_request('.*/GetUserModifyData.*')
                    time.sleep(0.5)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-close-btn")))

                    if driver.find_element(By.CSS_SELECTOR, "#user_add_institution_chosen > a > span").text != select_insti:
                        testResult = False
                        # Close
                        element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
                        driver.execute_script("arguments[0].click()",element)
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                        # Yes
                        time.sleep(0.5)
                        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                        break

                    # Close
                    element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
                    driver.execute_script("arguments[0].click()",element)
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                    # Yes
                    time.sleep(0.5)
                    driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        if testResult == False:
            Result_msg += "#1 "

        # SearchFilter_UserName결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1806, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1806, testPlanID, buildName, 'p', "SearchFilter_UserName Test Passed")

    def SearchFilter_ShowWithMappingID():
        print("ITR-53: Configuration > User Management > Search Filter > Show With Mapping ID")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)
        driver.wait_for_request('.*/GetUserList.*')
        time.sleep(0.5)

        # Show With Mapping ID #1
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(5) > div > label").click()
        driver.find_element(By.CSS_SELECTOR, "#user-search").click()

        request = driver.wait_for_request('.*/GetUserList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        check = False
        for a in range (0, total):
            request = driver.wait_for_request('.*/GetUserList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in range(0, len(data)):
                if data[n]["IsMappingID"] == "Y":
                    if driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(7)").text == "Y":
                        check = True
                        break

            if (check == True or 
                a+1 == total):
                break

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#user-list_next > a").click()

        if check == False:
            testResult = False
            Result_msg += "#1 "

        # SearchFilter_ShowWithMappingID결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1809, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1809, testPlanID, buildName, 'p', "SearchFilter_ShowWithMappingID Test Passed")

    def UserRegistartion_Add():
        print("ITR-54: Configuration > User Management > User Registration > Add")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        class_check = True
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)
        driver.wait_for_request('.*/GetUserList.*')
        time.sleep(0.5)

        # Add #1
        driver.find_element(By.CSS_SELECTOR, "#user-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        try:
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/h3"), "User Registration"))
        except:
            testResult = False
            Result_msg += "#1 "

        # Validation #2
        check = ""
        for i in range(0, 30):
            test_id = Var.add_test_id+str(random.randrange(0,100000))
            driver.find_element(By.CSS_SELECTOR, "#user-add-id").clear()
            driver.find_element(By.CSS_SELECTOR, "#user-add-id").send_keys(test_id)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-add-validation-btn")))
            driver.find_element(By.CSS_SELECTOR, "#user-add-validation-btn").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            check = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            if check == "User ID is available!":
                break
        if check != "User ID is available!":
            testResult = False
            Result_msg += "#2 "

        # < 5 Validation #3
        driver.find_element(By.CSS_SELECTOR, "#user-add-id").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-add-id").send_keys("55555")
        if driver.find_element(By.CSS_SELECTOR, "#user-add-validation-btn").value_of_css_property("cursor") != "not-allowed":
            testResult = False
            Result_msg += "#3 "

        # Only Number Validation #4
        driver.find_element(By.CSS_SELECTOR, "#user-add-id").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-add-id").send_keys("555555")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-add-validation-btn")))
        driver.find_element(By.CSS_SELECTOR, "#user-add-validation-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "User ID로 숫자만 사용할 수 없습니다.":
            testResult = False
            Result_msg += "#4 "
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        
        # Korean Validation #5
        driver.find_element(By.CSS_SELECTOR, "#user-add-id").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-add-id").send_keys("한글1234")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-add-validation-btn")))
        driver.find_element(By.CSS_SELECTOR, "#user-add-validation-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "User ID로 한글은 사용할 수 없습니다.":
            testResult = False
            Result_msg += "#5 "
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # Already Validation #6
        driver.find_element(By.CSS_SELECTOR, "#user-add-id").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-add-id").send_keys(Var.adminID)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-add-validation-btn")))
        driver.find_element(By.CSS_SELECTOR, "#user-add-validation-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "User ID is Exist!":
            testResult = False
            Result_msg += "#6 "
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # Input
        driver.find_element(By.CSS_SELECTOR, "#user-add-id").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-add-id").send_keys(test_id)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-add-validation-btn")))
        driver.find_element(By.CSS_SELECTOR, "#user-add-validation-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # Short Password #8
        driver.find_element(By.CSS_SELECTOR, "#user-add-pw").send_keys("Ser12!@")
        driver.find_element(By.CSS_SELECTOR, "#user-add-name").send_keys(test_id)
        driver.find_element(By.CSS_SELECTOR, "#user-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "Password는 8자 이상이여야 합니다.":
            testResult = False
            Result_msg += "#8 "
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/h3")))

        # Single Password #9
        check = True
        driver.find_element(By.CSS_SELECTOR, "#user-add-pw").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-add-pw").send_keys("qwerasdf")
        driver.find_element(By.CSS_SELECTOR, "#user-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "Password의 영문 대 소문자, 숫자, 특수문자를 혼용하여 사용하여야 합니다.":
            check = False
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/h3")))

        driver.find_element(By.CSS_SELECTOR, "#user-add-pw").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-add-pw").send_keys("12345678")
        driver.find_element(By.CSS_SELECTOR, "#user-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "Password의 영문 대 소문자, 숫자, 특수문자를 혼용하여 사용하여야 합니다.":
            check = False
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/h3")))

        driver.find_element(By.CSS_SELECTOR, "#user-add-pw").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-add-pw").send_keys("!@#$%^&*")
        driver.find_element(By.CSS_SELECTOR, "#user-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "Password의 영문 대 소문자, 숫자, 특수문자를 혼용하여 사용하여야 합니다.":
            check = False
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/h3")))

        if check == False:
            testResult = False
            Result_msg += "#9 "

        # Password input
        driver.find_element(By.CSS_SELECTOR, "#user-add-pw").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-add-pw").send_keys(Var.wk_pw_2)

        # Non User Name Save #10
        driver.find_element(By.CSS_SELECTOR, "#user-add-name").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "User Name를 입력해주세요.":
            testResult = False
            Result_msg += "#10 "
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/h3")))

        # Right PW Save, Right User Name Save, Class, E-mail, Phone, License, Administrator, Select Authority, Unselect Authority  #7 11 12 15 16 17 18 23 24
        driver.find_element(By.CSS_SELECTOR, "#user-add-name").send_keys(test_id)

        driver.find_element(By.CSS_SELECTOR, "#user-add-email").send_keys("EmailTest")
        driver.find_element(By.CSS_SELECTOR, "#user-add-phone").send_keys("PhoneTest")
        driver.find_element(By.CSS_SELECTOR, "#user-add-license").send_keys("LicenseTest")

        if (driver.find_element(By.CSS_SELECTOR, "#user-add-authority-view-image").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-view-image").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-config-view").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-config-view").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-config-create").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-config-create").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-config-delete").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-config-delete").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-admin-advanced-result").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-admin-advanced-result").get_property("willValidate") == False):
            testResult = False
            Result_msg += "#18 "

        driver.find_element(By.CSS_SELECTOR, "#add-user-popup > div > div > div.modal-body > div:nth-child(10) > div > div.col-lg-9.col-xs-9 > div > div > label:nth-child(2)").click()
        if driver.find_element(By.CSS_SELECTOR, "#user-add-authority-job-display").get_property("checked") == False:
            testResult = False
            Result_msg += "#23 "

        if "#23" not in Result_msg:
            driver.find_element(By.CSS_SELECTOR, "#add-user-popup > div > div > div.modal-body > div:nth-child(10) > div > div.col-lg-9.col-xs-9 > div > div > label:nth-child(2)").click()
            if driver.find_element(By.CSS_SELECTOR, "#user-add-authority-job-display").get_property("checked") == True:
                testResult = False
                Result_msg += "#24"

        # save
        driver.find_element(By.CSS_SELECTOR, "#user-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/h3")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/h3").text
        # save
        driver.find_element(By.CSS_SELECTOR, "#user-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
       
        del driver.requests
        time.sleep(1)

        # search
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-id").send_keys(test_id)
        driver.find_element(By.CSS_SELECTOR, "#user-search").click()

        request = driver.wait_for_request('.*/GetUserList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        del driver.requests
        time.sleep(1)

        idx = -1
        for n in data:
            if n["UserID"] == test_id:
                idx = data.index(n) + 1
                break

        if (idx == -1 or 
            msg != "등록하시겠습니까?" or 
            no_msg != "User Registration"):
            testResult = False
            Result_msg += "#7 "

        if "#7" not in Result_msg:
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()

            driver.wait_for_request('.*/GetUserModifyData.*')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-save-btn")))

            if driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > a > span").text != "Administrator":
                class_check = False
            if driver.find_element(By.CSS_SELECTOR, "#user-add-email").get_property("value") != "EmailTest":
                testResult = False
                Result_msg += "#15 "
            if driver.find_element(By.CSS_SELECTOR, "#user-add-phone").get_property("value") != "PhoneTest":
                testResult = False
                Result_msg += "#16 "
            if driver.find_element(By.CSS_SELECTOR, "#user-add-license").get_property("value") != "LicenseTest":
                testResult = False
                Result_msg += "#17 "

            # close
            driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # Center, Class, SubAdministrator #12 13 19
        # add
        driver.find_element(By.CSS_SELECTOR, "#user-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/h3"), "User Registration"))
        # input
        while(1):
            test_id = Var.add_test_id+str(random.randrange(0,100000))
            driver.find_element(By.CSS_SELECTOR, "#user-add-id").clear()
            driver.find_element(By.CSS_SELECTOR, "#user-add-id").send_keys(test_id)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-add-validation-btn")))
            driver.find_element(By.CSS_SELECTOR, "#user-add-validation-btn").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            check = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            if check == "User ID is available!":
                break
        driver.find_element(By.CSS_SELECTOR, "#user-add-pw").send_keys(Var.wk_pw_2)
        driver.find_element(By.CSS_SELECTOR, "#user-add-name").send_keys(test_id)
        driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > a > span").click()
        child = driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > div > ul").get_property("childElementCount")
        for n in range(1, child+1):
            if driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > div > ul > li:nth-child("+str(n)+")").text == "SubAdministrator":
                driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > div > ul > li:nth-child("+str(n)+")").click()
                break
        # center
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user_add_center_chosen > a > span")))
        driver.find_element(By.CSS_SELECTOR, "#user_add_center_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#user_add_center_chosen > div > div > input[type=text]").send_keys(Var.search_center)
        driver.find_element(By.CSS_SELECTOR, "#user_add_center_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)

        # subadministrator
        if (driver.find_element(By.CSS_SELECTOR, "#user-add-authority-view-image").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-view-image").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-report-display").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-report-display").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-report-delete").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-report-delete").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-config-view").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-config-view").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-config-create").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-config-create").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-admin-advanced-result").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-admin-advanced-result").get_property("willValidate") == False):
            testResult = False
            Result_msg += "#19 "

        # save
        driver.find_element(By.CSS_SELECTOR, "#user-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
       
        del driver.requests
        time.sleep(1)

        # search
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-id").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-id").send_keys(test_id)
        driver.find_element(By.CSS_SELECTOR, "#user-search").click()

        request = driver.wait_for_request('.*/GetUserList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        del driver.requests
        time.sleep(1)

        idx = -1
        for n in data:
            if n["UserID"] == test_id:
                idx = data.index(n) + 1
                break

        if idx != -1:
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()

            driver.wait_for_request('.*/GetUserModifyData.*')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-save-btn")))

            if driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > a > span").text != "SubAdministrator":
                class_check = False
            if driver.find_element(By.CSS_SELECTOR, "#user_add_center_chosen > a > span").text != Var.search_center:
                testResult = False
                Result_msg += "#13 "

            # close
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-close-btn")))
            driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        else:
            testResult = False
            Result_msg += "#13 "
            class_check = False

        # Class, Reporter #12 20
        # add
        driver.find_element(By.CSS_SELECTOR, "#user-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/h3"), "User Registration"))
        # input
        while(1):
            test_id = Var.add_test_id+str(random.randrange(0,100000))
            driver.find_element(By.CSS_SELECTOR, "#user-add-id").clear()
            driver.find_element(By.CSS_SELECTOR, "#user-add-id").send_keys(test_id)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-add-validation-btn")))
            driver.find_element(By.CSS_SELECTOR, "#user-add-validation-btn").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            check = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            if check == "User ID is available!":
                break
        driver.find_element(By.CSS_SELECTOR, "#user-add-pw").send_keys(Var.wk_pw_2)
        driver.find_element(By.CSS_SELECTOR, "#user-add-name").send_keys(test_id)
        driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > a > span").click()
        child = driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > div > ul").get_property("childElementCount")
        for n in range(1, child+1):
            if driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > div > ul > li:nth-child("+str(n)+")").text == "Reporter":
                driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > div > ul > li:nth-child("+str(n)+")").click()
                break

        # reporter
        if (driver.find_element(By.CSS_SELECTOR, "#user-add-authority-file-upload-job").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-file-upload-job").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-file-download-job").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-file-download-job").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-file-download-module").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-file-download-module").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-view-image").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-view-image").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-report-display").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-report-display").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-report-create").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-report-create").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-report-delete").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-report-delete").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-admin-advanced-result").get_property("checked") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-admin-advanced-result").get_property("willValidate") == True ):
            testResult = False
            Result_msg += "#20 "

        # save
        driver.find_element(By.CSS_SELECTOR, "#user-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
       
        del driver.requests
        time.sleep(1)

        # search
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-id").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-id").send_keys(test_id)
        driver.find_element(By.CSS_SELECTOR, "#user-search").click()

        request = driver.wait_for_request('.*/GetUserList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        del driver.requests
        time.sleep(1)

        idx = -1
        for n in data:
            if n["UserID"] == test_id:
                idx = data.index(n) + 1
                break

        if idx != -1:
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()

            driver.wait_for_request('.*/GetUserModifyData.*')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-save-btn")))

            if driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > a > span").text != "Reporter":
                class_check = False

            # close
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-close-btn")))
            element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
            driver.execute_script("arguments[0].click()",element)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        else:
            class_check = False

        # Institution, Class, Requester #12 14 21
        # add
        driver.find_element(By.CSS_SELECTOR, "#user-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/h3"), "User Registration"))
        # input
        while(1):
            test_id = Var.add_test_id+str(random.randrange(0,100000))
            driver.find_element(By.CSS_SELECTOR, "#user-add-id").clear()
            driver.find_element(By.CSS_SELECTOR, "#user-add-id").send_keys(test_id)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-add-validation-btn")))
            driver.find_element(By.CSS_SELECTOR, "#user-add-validation-btn").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            check = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            if check == "User ID is available!":
                break
        driver.find_element(By.CSS_SELECTOR, "#user-add-pw").send_keys(Var.wk_pw_2)
        driver.find_element(By.CSS_SELECTOR, "#user-add-name").send_keys(test_id)
        driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > a > span").click()
        child = driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > div > ul").get_property("childElementCount")
        for n in range(1, child+1):
            if driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > div > ul > li:nth-child("+str(n)+")").text == "Requester":
                driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > div > ul > li:nth-child("+str(n)+")").click()
                break

        # institution
        driver.find_element(By.CSS_SELECTOR, "#user_add_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#user_add_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#user_add_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)


        # requester
        if (driver.find_element(By.CSS_SELECTOR, "#user-add-authority-job-display").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-job-display").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-job-edit").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-job-edit").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-job-delete").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-job-delete").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-file-upload-job").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-file-upload-job").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-view-image").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-view-image").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-report-display").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-report-display").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-admin-advanced-result").get_property("checked") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-admin-advanced-result").get_property("willValidate") == True ):
            testResult = False
            Result_msg += "#21 "

        # save
        driver.find_element(By.CSS_SELECTOR, "#user-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
       
        del driver.requests
        time.sleep(1)

        # search
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-id").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-id").send_keys(test_id)
        driver.find_element(By.CSS_SELECTOR, "#user-search").click()

        request = driver.wait_for_request('.*/GetUserList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        del driver.requests
        time.sleep(1)

        idx = -1
        for n in data:
            if n["UserID"] == test_id:
                idx = data.index(n) + 1
                break

        if idx != -1:
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()

            driver.wait_for_request('.*/GetUserModifyData.*')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-save-btn")))

            if driver.find_element(By.CSS_SELECTOR, "#user_add_institution_chosen > a > span").text != Var.search_institution_3:
                testResult = False
                Result_msg += "#14 "
            if driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > a > span").text != "Requester":
                class_check = False

            # close
            driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        else:
            class_check = False

        # Class, Product #12 22
        # add
        driver.find_element(By.CSS_SELECTOR, "#user-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/h3"), "User Registration"))
        # input
        while(1):
            test_id = Var.add_test_id+str(random.randrange(0,100000))
            driver.find_element(By.CSS_SELECTOR, "#user-add-id").clear()
            driver.find_element(By.CSS_SELECTOR, "#user-add-id").send_keys(test_id)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-add-validation-btn")))
            driver.find_element(By.CSS_SELECTOR, "#user-add-validation-btn").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            check = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            if check == "User ID is available!":
                break
        driver.find_element(By.CSS_SELECTOR, "#user-add-pw").send_keys(Var.wk_pw_2)
        driver.find_element(By.CSS_SELECTOR, "#user-add-name").send_keys(test_id)
        driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > a > span").click()
        child = driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > div > ul").get_property("childElementCount")
        for n in range(1, child+1):
            if driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > div > ul > li:nth-child("+str(n)+")").text == "Product":
                driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > div > ul > li:nth-child("+str(n)+")").click()
                break

        # product
        if (driver.find_element(By.CSS_SELECTOR, "#user-add-authority-job-delete").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-job-delete").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-report-display").get_property("checked") == False or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-report-display").get_property("willValidate") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-admin-advanced-result").get_property("checked") == True or
            driver.find_element(By.CSS_SELECTOR, "#user-add-authority-admin-advanced-result").get_property("willValidate") == True ):
            testResult = False
            Result_msg += "#22 "

        # save
        driver.find_element(By.CSS_SELECTOR, "#user-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
       
        del driver.requests
        time.sleep(1)

        # search
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-id").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-id").send_keys(test_id)
        driver.find_element(By.CSS_SELECTOR, "#user-search").click()

        request = driver.wait_for_request('.*/GetUserList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        del driver.requests
        time.sleep(1)

        idx = -1
        for n in data:
            if n["UserID"] == test_id:
                idx = data.index(n) + 1
                break

        if idx != -1:
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()

            driver.wait_for_request('.*/GetUserModifyData.*')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-save-btn")))

            if driver.find_element(By.CSS_SELECTOR, "#user_add_level_chosen > a > span").text != "Product":
                class_check = False

            # close
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-close-btn")))
            element = driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn")
            driver.execute_script("arguments[0].click()",element)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        else:
            class_check = False

        if class_check ==  False:
            testResult = False
            Result_msg += "#12 "

        # UserRegistartion_Add결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1813, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1813, testPlanID, buildName, 'p', "UserRegistartion_Add Test Passed")

    def UserRegistration_Modify_Entry(target):
        testResult = True

        driver.find_element(By.CSS_SELECTOR, "#mapping-userid-list_length > label > select").click()
        child = driver.find_element(By.CSS_SELECTOR, "#mapping-userid-list_length > label > select").get_property("childElementCount")
        for n in range(1, child + 1):
            if driver.find_element(By.CSS_SELECTOR, "#mapping-userid-list_length > label > select > option:nth-child("+str(n)+")").text == str(target):
                driver.find_element(By.CSS_SELECTOR, "#mapping-userid-list_length > label > select > option:nth-child("+str(n)+")").click()
                break

        request = driver.wait_for_request('.*/GetUserMappingList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        if data["Length"] != target:
            testResult = False

        del driver.requests
        time.sleep(1)

        return testResult

    def UserRegistartion_Modify():
        print("ITR-55: Configuration > User Management > User Registration > Modify")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # DownalodControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')
        time.sleep(0.5)

        # Add
        driver.find_element(By.CSS_SELECTOR, "#download-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[5]/div/div/div[1]/h3")))
        # User
        driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_user_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
        driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#download-config-add-user-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-user-remove-btn")))
        # Institution
        driver.find_element(By.CSS_SELECTOR, "#add_sel_institution_search").send_keys(Var.search_institution_3)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[5]/div/div/div[2]/div[1]/div[2]/div/div/div[1]/select/option[1]").click()
        driver.find_element(By.CSS_SELECTOR, "#download-config-add-institution-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-institution-remove-btn")))
        # Save
        driver.find_element(By.CSS_SELECTOR, "#download-contol-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # Yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # Ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        del driver.requests
        time.sleep(1)

        # UserManagement
        driver.find_element(By.CSS_SELECTOR, "#user-btn").click()
        driver.wait_for_request('.*/GetUserList.*')
        time.sleep(0.5)

        del driver.requests
        time.sleep(1)

        # Search
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-id").send_keys(Var.wk_id_2)
        driver.find_element(By.CSS_SELECTOR, "#user-search").click()
        request = driver.wait_for_request('.*/GetUserList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        # Select
        idx = -1
        for n in range(0, len(data)):
            if data[n]["UserID"] == Var.wk_id_2:
                idx = n+1
                select_user = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").text
                break
        # User ID Click #1
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-save-btn")))
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/h3").text != "User Modify":
            testResult = False
            Result_msg += "#1 "

        if testResult == True:
            # Modify ID #2
            if driver.find_element(By.CSS_SELECTOR, "#user-add-id").value_of_css_property("cursor") != "not-allowed":
                testResult = False
                Result_msg += "#2 "

            # Download User ID #3
            driver.find_element(By.CSS_SELECTOR, "#user-modify-download-userid-btn > span").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[1]/h3")))
            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[1]/h3").text != "User Mapping":
                testResult = False
                Result_msg += "#3 "

            if "#3" not in Result_msg:
                # Institution #4
                driver.find_element(By.CSS_SELECTOR, "#download_userid_select_institution_chosen > a > span").click()
                child = driver.find_element(By.CSS_SELECTOR, "#download_userid_select_institution_chosen > div > ul").get_property("childElementCount")
                check = False
                for n in range(1, child+1):
                    if driver.find_element(By.CSS_SELECTOR, "#download_userid_select_institution_chosen > div > ul > li:nth-child("+str(n)+")").text == Var.search_institution_3:
                        driver.find_element(By.CSS_SELECTOR, "#download_userid_select_institution_chosen > div > ul > li:nth-child("+str(n)+")").click()
                        check = True
                        break
                if check == False:
                    testResult = False
                    Result_msg += "#4 "

                # Already Mapping Validation #6
                driver.find_element(By.CSS_SELECTOR, "#user-modify-download-userid-popup > div > div > div.modal-body > div:nth-child(2) > div > div.col-lg-6.col-xs-6.switch.panel-switch-btn > label > span").click()
                driver.find_element(By.CSS_SELECTOR, "#download-userid-add-id").send_keys(Var.wk_id_2)
                driver.find_element(By.CSS_SELECTOR, "#download-userid-add-id-validation-btn > span").click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "User ID is Exist!":
                    testResult = False
                    Result_msg += "#6 "
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

                # Mapping Validation #5
                check = False
                for i in range(0, 30):
                    test_id = Var.add_test_id+str(random.randrange(0,100000))
                    driver.find_element(By.CSS_SELECTOR, "#download-userid-add-id").clear()
                    driver.find_element(By.CSS_SELECTOR, "#download-userid-add-id").send_keys(test_id)
                    driver.find_element(By.CSS_SELECTOR, "#download-userid-add-id-validation-btn > span").click()
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                    if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text == "User ID is available!":
                        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                        check = True
                        break
                if check == False:
                    testResult = False
                    Result_msg += "#5 "

                # Save
                driver.find_element(By.CSS_SELECTOR, "#mapping-userid-save-btn").click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                # Yes
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
                # Ok
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-download-userid-popup > div > div > div.modal-body > div:nth-child(2) > div > div.col-lg-6.col-xs-6.switch.panel-switch-btn > label > span")))

                # Second Save #9
                driver.find_element(By.CSS_SELECTOR, "#user-modify-download-userid-popup > div > div > div.modal-body > div:nth-child(2) > div > div.col-lg-6.col-xs-6.switch.panel-switch-btn > label > span").click()
                while (1):
                    test_id = Var.add_test_id+str(random.randrange(0,100000))
                    driver.find_element(By.CSS_SELECTOR, "#download-userid-add-id").clear()
                    driver.find_element(By.CSS_SELECTOR, "#download-userid-add-id").send_keys(test_id)
                    driver.find_element(By.CSS_SELECTOR, "#download-userid-add-id-validation-btn > span").click()
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                    if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text == "User ID is available!":
                        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                        break
                # save
                driver.find_element(By.CSS_SELECTOR, "#mapping-userid-save-btn").click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                # yes
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))

                if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "선택한 병원에 등록된 Mapping ID가 존재합니다.":
                    testResult = False
                    Result_msg += "#9 "

                # ok
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

                # Close #10
                # close
                driver.find_element(By.CSS_SELECTOR, "#mapping-userid-close-btn").click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
                # no
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mapping-userid-close-btn")))
                no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[1]/h3").text
                # close
                driver.find_element(By.CSS_SELECTOR, "#mapping-userid-close-btn").click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                # yes
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-close-btn")))
                yes_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/h3").text
                if (msg != "설정을 종료하시겠습니까?" or
                    no_msg != "User Mapping" or
                    yes_msg != "User Modify"):
                    testResult = False
                    Result_msg += "#10 "

            # Download User ID
            driver.find_element(By.CSS_SELECTOR, "#user-modify-download-userid-btn > span").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[1]/h3")))
            
            del driver.requests
            time.sleep(1)

            if "#3" not in Result_msg:
                # Institution None Search #11
                driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > a > span").click()
                child = driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > div > ul").get_property("childElementCount")
                for n in range (1, child+1):
                    if driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > div > ul > li:nth-child("+str(n)+")").text == "Institution":
                        driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > div > ul > li:nth-child("+str(n)+")").click()
                        break

                driver.find_element(By.CSS_SELECTOR, "#download_userid_search_select_institution_chosen > a > span").click()
                child = driver.find_element(By.CSS_SELECTOR, "#download_userid_search_select_institution_chosen > div > ul").get_property("childElementCount")
                for n in range (1, child+1):
                    if driver.find_element(By.CSS_SELECTOR, "#download_userid_search_select_institution_chosen > div > ul > li:nth-child("+str(n)+")").text == "None":
                        driver.find_element(By.CSS_SELECTOR, "#download_userid_search_select_institution_chosen > div > ul > li:nth-child("+str(n)+")").click()
                        break
                
                driver.find_element(By.CSS_SELECTOR, "#mapping-userid-search-btn").click()
                request = driver.wait_for_request('.*/GetUserMappingList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]
                remember_id = data[0]["InstitutionUserID"]

                for n in range(0, len(data)):
                    if (data[n]["InstitutionName"] != driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/tbody/tr["+str(n+1)+"]/td[1]").text or
                        data[n]["InstitutionUserID"] != driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/tbody/tr["+str(n+1)+"]/td[2]").text):
                        testResult = False
                        Result_msg += "#11 "
                        break

                del driver.requests
                time.sleep(1)

                # Institution Select Search #12
                driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > a > span").click()
                child = driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > div > ul").get_property("childElementCount")
                for n in range (1, child+1):
                    if driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > div > ul > li:nth-child("+str(n)+")").text == "Institution":
                        driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > div > ul > li:nth-child("+str(n)+")").click()
                        break

                driver.find_element(By.CSS_SELECTOR, "#download_userid_search_select_institution_chosen > a > span").click()
                child = driver.find_element(By.CSS_SELECTOR, "#download_userid_search_select_institution_chosen > div > ul").get_property("childElementCount")
                for n in range (1, child+1):
                    if driver.find_element(By.CSS_SELECTOR, "#download_userid_search_select_institution_chosen > div > ul > li:nth-child("+str(n)+")").text == Var.search_institution_3:
                        driver.find_element(By.CSS_SELECTOR, "#download_userid_search_select_institution_chosen > div > ul > li:nth-child("+str(n)+")").click()
                        break

                driver.find_element(By.CSS_SELECTOR, "#mapping-userid-search-btn").click()
                request = driver.wait_for_request('.*/GetUserMappingList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                time.sleep(1)
                for n in range(0, len(data)):
                    if (data[n]["InstitutionName"] != Var.search_institution_3 or
                        Var.search_institution_3 != driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/tbody/tr["+str(n+1)+"]/td[1]").text or
                        data[n]["InstitutionUserID"] != driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/tbody/tr["+str(n+1)+"]/td[2]").text):
                        testResult = False
                        Result_msg += "#12 "
                        break

                del driver.requests
                time.sleep(1)

                # Blank Mapping ID Search #13
                driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > a > span").click()
                child = driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > div > ul").get_property("childElementCount")
                for n in range (1, child+1):
                    if driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > div > ul > li:nth-child("+str(n)+")").text == "Mapping ID":
                        driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > div > ul > li:nth-child("+str(n)+")").click()
                        break

                driver.find_element(By.CSS_SELECTOR, "#mapping-userid-search-btn").click()
                request = driver.wait_for_request('.*/GetUserMappingList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in range(0, len(data)):
                    if (data[n]["InstitutionName"] != driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/tbody/tr["+str(n+1)+"]/td[1]").text or
                        data[n]["InstitutionUserID"] != driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/tbody/tr["+str(n+1)+"]/td[2]").text):
                        testResult = False
                        Result_msg += "#13 "
                        break

                del driver.requests
                time.sleep(1)

                # Input Mapping ID Search #14
                driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > a > span").click()
                child = driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > div > ul").get_property("childElementCount")
                for n in range (1, child+1):
                    if driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > div > ul > li:nth-child("+str(n)+")").text == "Mapping ID":
                        driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > div > ul > li:nth-child("+str(n)+")").click()
                        break

                driver.find_element(By.CSS_SELECTOR, "#download-userid-search-mapping-id-input").send_keys(remember_id)

                driver.find_element(By.CSS_SELECTOR, "#mapping-userid-search-btn").click()
                request = driver.wait_for_request('.*/GetUserMappingList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in range(0, len(data)):
                    if (data[n]["InstitutionUserID"] != remember_id or
                        remember_id != driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/tbody/tr["+str(n+1)+"]/td[2]").text or
                        data[n]["InstitutionName"] != driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/tbody/tr["+str(n+1)+"]/td[1]").text):
                        testResult = False
                        Result_msg += "#14 "
                        break

                del driver.requests
                time.sleep(1)

                # Other Input Mapping ID Search #15
                driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > a > span").click()
                child = driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > div > ul").get_property("childElementCount")
                for n in range (1, child+1):
                    if driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > div > ul > li:nth-child("+str(n)+")").text == "Mapping ID":
                        driver.find_element(By.CSS_SELECTOR, "#download_userid_select_search_type_chosen > div > ul > li:nth-child("+str(n)+")").click()
                        break

                driver.find_element(By.CSS_SELECTOR, "#download-userid-search-mapping-id-input").clear()
                driver.find_element(By.CSS_SELECTOR, "#download-userid-search-mapping-id-input").send_keys(Var.wk_id_2)

                driver.find_element(By.CSS_SELECTOR, "#mapping-userid-search-btn").click()
                request = driver.wait_for_request('.*/GetUserMappingList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                if len(data) != 0:
                    testResult = False 
                    Result_msg += "#15 "

                del driver.requests
                time.sleep(1)

                # Clear
                driver.find_element(By.CSS_SELECTOR, "#download-userid-search-mapping-id-input").clear()
                driver.find_element(By.CSS_SELECTOR, "#mapping-userid-search-btn").click()
                driver.wait_for_request('.*/GetUserMappingList.*')
                del driver.requests
                time.sleep(1)

                # Entries 25 #17
                temp = UserManagement.UserRegistration_Modify_Entry(25)
                if temp == False:
                    testResult = False
                    Result_msg += "#17 "

                # Entries 10 #16
                temp = UserManagement.UserRegistration_Modify_Entry(10)
                if temp == False:
                    testResult = False
                    Result_msg += "#16 "

                # Entries 50 #18
                temp = UserManagement.UserRegistration_Modify_Entry(50)
                if temp == False:
                    testResult = False
                    Result_msg += "#18 "

                # Entries 100 #19
                temp = UserManagement.UserRegistration_Modify_Entry(100)
                if temp == False:
                    testResult = False
                    Result_msg += "#19 "

                # Institution Sort #20
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/thead/tr/th[1]").click()
                check = True
                request = driver.wait_for_request('.*/GetUserMappingList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)

                before = data["OrderType"]
                if (data["OrderColumn"] != "InstitutionName" or 
                    before != driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/thead/tr/th[1]").get_property("ariaSort").split('ending')[0]):
                    check = False

                if check == False:
                    testResult = False
                    Result_msg += "#20 "
                else:
                    del driver.requests
                    time.sleep(1)

                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/thead/tr/th[1]").click()
                    request = driver.wait_for_request('.*/GetUserMappingList.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)
                    after = data["OrderType"]
                    if (data["OrderColumn"] != "InstitutionName" or 
                    after != driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/thead/tr/th[1]").get_property("ariaSort").split('ending')[0] or
                    before == after ):
                        check = False

                if check == False:
                    testResult = False
                    Result_msg += "#20 "

                del driver.requests
                time.sleep(1)

                # User ID Sort #21
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/thead/tr/th[2]").click()
                check = True
                request = driver.wait_for_request('.*/GetUserMappingList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)

                before = data["OrderType"]
                if (data["OrderColumn"] != "InstitutionUserID" or 
                    before != driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/thead/tr/th[2]").get_property("ariaSort").split('ending')[0]):
                    check = False

                if check == False:
                    testResult = False
                    Result_msg += "#21 "
                else:
                    del driver.requests
                    time.sleep(1)

                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/thead/tr/th[2]").click()
                    request = driver.wait_for_request('.*/GetUserMappingList.*')
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)
                    after = data["OrderType"]
                    if (data["OrderColumn"] != "InstitutionUserID" or 
                    after != driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/thead/tr/th[2]").get_property("ariaSort").split('ending')[0] or
                    before == after ):
                        check = False

                if check == False:
                    testResult = False
                    Result_msg += "#21 "

                del driver.requests
                time.sleep(1)

                # Delete #22
                driver.find_element(By.CSS_SELECTOR, "#mapping-userid-search-btn").click()
                request = driver.wait_for_request('.*/GetUserMappingList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                idx = -1
                for n in data:
                    if n["InstitutionUserID"] == remember_id:
                        idx = data.index(n) + 1
                        break

                del driver.requests
                time.sleep(1)

                # delete
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/tbody/tr["+str(idx)+"]/td[3]/a/i").click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
                # no
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mapping-userid-close-btn")))
                no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[1]/h3").text
                # delete
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/tbody/tr["+str(idx)+"]/td[3]/a/i")))
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div[9]/div/table/tbody/tr["+str(idx)+"]/td[3]/a/i").click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                # yes
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
                # ok
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

                request = driver.wait_for_request('.*/GetUserMappingList.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                if (msg != "삭제하시겠습니까?" or 
                    no_msg != "User Mapping"):
                    testResult = False
                    Result_msg += "#22 "
                else:
                    for n in data:
                        if n["InstitutionUserID"] == remember_id:
                            testResult = False
                            Result_msg += "#22 "

                # Close
                driver.find_element(By.CSS_SELECTOR, "#mapping-userid-close-btn").click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
                # Yes
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-modify-close-btn")))
            # Close
            driver.find_element(By.CSS_SELECTOR, "#user-modify-close-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # Yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-search")))

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')

        del driver.requests
        time.sleep(1)

        # Search
        driver.find_element(By.CSS_SELECTOR, "#download-search-user-id").send_keys(Var.wk_id_2)
        driver.find_element(By.CSS_SELECTOR, "#download-search").click()
        request = driver.wait_for_request('.*/GetDownloadControlList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        
        idx = -1
        for n in data:
            if n["UserID"] == Var.wk_id_2 :
                idx = data.index(n) + 1
                break

        # Click
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr["+str(idx)+"]/td[1]/label").click()
        # Delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/div[1]/a[2]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # Yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # UserRegistartion_Modify결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1839, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1839, testPlanID, buildName, 'p', "UserRegistartion_Modify Test Passed")

    def UserRegistartion_Delete():
        print("ITR-218: Configuration > User Management > User Registration > Delete")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)
        driver.wait_for_request('.*/GetUserList.*')

        # None Select Delete #1
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
            testResult = False
            Result_msg += "#1 "

        del driver.requests
        time.sleep(1)

        # Search
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-id").send_keys(Var.add_test_id)
        driver.find_element(By.CSS_SELECTOR, "#user-search").click()
        request = driver.wait_for_request('.*/GetUserList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        # Select Delete #2
        # select
        for n in range(0, len(data)):
            if data[n]["UserID"].split(Var.add_test_id)[1].isdigit() == True :
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(n+1)+"]/td[1]/label").click()
                select_user = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr["+str(n+1)+"]/td[2]/a").text
                break

        del driver.requests
        time.sleep(1)

        # delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/a[2]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/a[2]")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[1]/h4").text
        # delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/a[2]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        
        # search
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-id").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-id").send_keys(select_user)
        driver.find_element(By.CSS_SELECTOR, "#user-search").click()
        request = driver.wait_for_request('.*/GetUserList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        for n in data:
            if n["UserID"] == select_user:
                testResult = False
                Result_msg += "#2 "

        del driver.requests
        time.sleep(1)

        # Search
        driver.find_element(By.CSS_SELECTOR, "#user-search-user-id").clear()
        driver.find_element(By.CSS_SELECTOR, "#user-search").click()
        request = driver.wait_for_request('.*/GetUserList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        if total < 2:
            testResult = False
            Result_msg += "#3 #4 "
        else:
            # Delete Other Tab #3
            del driver.requests
            time.sleep(1)
            
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr[1]/td[1]/label").click()
            driver.find_element(By.CSS_SELECTOR, "#user-list_next > a").click()

            driver.wait_for_request('.*/GetUserList.*')

            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
                testResult = False
                Result_msg += "#3 "

            # Delete Other Tab > 2
            del driver.requests
            time.sleep(1)
            
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr[1]/td[1]/label").click()
            driver.find_element(By.CSS_SELECTOR, "#user-list_previous > a").click()

            driver.wait_for_request('.*/GetUserList.*')

            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
                testResult = False
                Result_msg += "#4 "

        # UserRegistartion_Delete결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2864, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2864, testPlanID, buildName, 'p', "UserRegistartion_Delete Test Passed")

class Specialty:
    def SpecialtyList_Search():
        print("ITR-56: Configuration > Specialty > Specialty list > Search")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # Specialty
        driver.find_element(By.CSS_SELECTOR, "#specialty-btn").click()
        driver.wait_for_request('.*/GetSpecialtyList.*')  

        del driver.requests
        time.sleep(1)

        # Code Search #1
        driver.find_element(By.CSS_SELECTOR, "#specialty-search-code").send_keys(Var.specialty)
        driver.find_element(By.CSS_SELECTOR, "#specialty-search").click()
        request = driver.wait_for_request('.*/GetSpecialtyList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        for n in range(0, len(data)):
            if (Var.specialty not in data[n]["SpecialtyCode"] or 
                data[n]["SpecialtyCode"] != driver.find_element(By.CSS_SELECTOR, "#specialty-code-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(2)").get_property("textContent")):
                testResult = False
                Result_msg += "#1 "

        del driver.requests
        time.sleep(1)

        # Description Search #2
        driver.find_element(By.CSS_SELECTOR, "#specialty-search-code").clear()
        driver.find_element(By.CSS_SELECTOR, "#specialty-search-desc").send_keys(Var.specialty)
        driver.find_element(By.CSS_SELECTOR, "#specialty-search").click()
        request = driver.wait_for_request('.*/GetSpecialtyList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        for n in range(0, len(data)):
            if (Var.specialty not in data[n]["SpecialtyDescription"] or 
                data[n]["SpecialtyDescription"] != driver.find_element(By.CSS_SELECTOR, "#specialty-code-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(3)").get_property("textContent")):
                testResult = False
                Result_msg += "#2 "

        # SpecialtyList_Search결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1865, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1865, testPlanID, buildName, 'p', "SpecialtyList_Search Test Passed")

    def SpecialtyList_Add():
        print("ITR-57: Configuration > Specialty > Specialty list > Add")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # Specialty
        driver.find_element(By.CSS_SELECTOR, "#specialty-btn").click()
        driver.wait_for_request('.*/GetSpecialtyList.*')  
        time.sleep(0.5)

        # Add #1
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/a[1]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/h3")))
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/h3").text != "Specialty Registration":
            testResult = False
            Result_msg += "#1 "

        # Input Save #2
        driver.find_element(By.CSS_SELECTOR, "#specialty-add-specialty-code").send_keys(Var.specialty_add)
        driver.find_element(By.CSS_SELECTOR, "#specialty-add-specialty-desc").send_keys(Var.specialty_add)
        # save
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty-add-save-btn")))
        driver.find_element(By.CSS_SELECTOR, "#specialty-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/h3")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/h3").text
        # save
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty-add-save-btn")))
        driver.find_element(By.CSS_SELECTOR, "#specialty-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        del driver.requests
        time.sleep(1)

        # search
        driver.find_element(By.CSS_SELECTOR, "#specialty-search-code").send_keys(Var.specialty_add)
        driver.find_element(By.CSS_SELECTOR, "#specialty-search").click()
        request = driver.wait_for_request('.*/GetSpecialtyList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        idx = -1
        for n in data:
            if n["SpecialtyCode"] == Var.specialty_add:
                idx = data.index(n)
                break

        if (msg != "등록하시겠습니까?" or
            no_msg != "Specialty Registration" or
            idx == -1):
            testResult = False
            Result_msg += "#2 "

        del driver.requests
        time.sleep(1)

        # Already Save #3
        # add
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/a[1]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/h3")))
        # input
        driver.find_element(By.CSS_SELECTOR, "#specialty-add-specialty-code").send_keys(Var.specialty_add)
        driver.find_element(By.CSS_SELECTOR, "#specialty-add-specialty-desc").send_keys(Var.specialty_add)
        # save
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty-add-save-btn")))
        driver.find_element(By.CSS_SELECTOR, "#specialty-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/h3")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/h3").text
        # save
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty-add-save-btn")))
        driver.find_element(By.CSS_SELECTOR, "#specialty-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        request = driver.wait_for_request('.*/GetSpecialtyList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        idx = -1
        for n in data:
            if n["SpecialtyCode"] == Var.specialty_add:
                idx = data.index(n)
                break

        if (msg != "등록하시겠습니까?" or
            no_msg != "Specialty Registration" or
            idx == -1):
            testResult = False
            Result_msg += "#3 "

        # SpecialtyList_Add결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1869, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1869, testPlanID, buildName, 'p', "SpecialtyList_Add Test Passed")

    def SpecialtyList_Delete():
        print("ITR-58: Configuration > Specialty > Specialty list > Delete")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # Specialty
        driver.find_element(By.CSS_SELECTOR, "#specialty-btn").click()
        driver.wait_for_request('.*/GetSpecialtyList.*')  
        time.sleep(0.5)

        # Nonclick Delete #1
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/a[2]").value_of_css_property('cursor') != "not-allowed":
            testResult = False
            Result_msg += "#1 "

        del driver.requests
        time.sleep(1)

        # search
        driver.find_element(By.CSS_SELECTOR, "#specialty-search-code").send_keys(Var.specialty_add)
        driver.find_element(By.CSS_SELECTOR, "#specialty-search").click()
        request = driver.wait_for_request('.*/GetSpecialtyList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        idx = -1
        for n in data:
            if n["SpecialtyCode"] == Var.specialty_add:
                idx = data.index(n)
                break

        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/table/tbody/tr["+str(idx+1)+"]/td[1]/label").click()

        del driver.requests
        time.sleep(1)

        # Delete #2
        # delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/a[2]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/a[2]")))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#specialty-tab-name").text
        # delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/a[2]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        request = driver.wait_for_request('.*/GetSpecialtyList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        idx = -1
        for n in data:
            if n["SpecialtyCode"] == Var.specialty_add:
                idx = data.index(n)
                break

        if (msg != "삭제하시겠습니까?" or 
            no_msg != "Specialty List" or
            idx != -1):
            testResult = False
            Result_msg += "#2 "

        del driver.requests
        time.sleep(1)

        # Specialty
        driver.find_element(By.CSS_SELECTOR, "#specialty-btn").click()
        request = driver.wait_for_request('.*/GetSpecialtyList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        # Other Tab Delete #3
        if total < 2:
            testResult = False
            Result_msg += "#3 #4 "
        else:
            del driver.requests
            time.sleep(1)

            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[1]/td[1]/label").click()
            driver.find_element(By.CSS_SELECTOR, "#specialty-code-list_next > a").click()

            driver.wait_for_request('.*/GetSpecialtyList.*')

            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
                testResult = False
                Result_msg += "#3 "

            # Other Tab Delete > 2 #4
            del driver.requests
            time.sleep(1)

            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[1]/td[1]/label").click()
            driver.find_element(By.CSS_SELECTOR, "#specialty-code-list_previous > a").click()

            driver.wait_for_request('.*/GetSpecialtyList.*')

            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
                testResult = False
                Result_msg += "#4 "

        # SpecialtyList_Delete결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1874, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1874, testPlanID, buildName, 'p', "SpecialtyList_Delete Test Passed")

    def SpecialtyList_Modify():
        print("ITR-59: Configuration > Specialty > Specialty list > Modify")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # Specialty
        driver.find_element(By.CSS_SELECTOR, "#specialty-btn").click()
        driver.wait_for_request('.*/GetSpecialtyList.*')  
        time.sleep(0.5)

        # Add
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/a[1]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/h3")))
        # Input
        driver.find_element(By.CSS_SELECTOR, "#specialty-add-specialty-code").send_keys(Var.specialty_add)
        driver.find_element(By.CSS_SELECTOR, "#specialty-add-specialty-desc").send_keys(Var.specialty_add)
        # Save
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty-add-save-btn")))
        driver.find_element(By.CSS_SELECTOR, "#specialty-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # Yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # Ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        del driver.requests
        time.sleep(1)

        # Search
        driver.find_element(By.CSS_SELECTOR, "#specialty-search-code").send_keys(Var.specialty_add)
        driver.find_element(By.CSS_SELECTOR, "#specialty-search").click()
        request = driver.wait_for_request('.*/GetSpecialtyList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        idx = -1
        for n in data:
            if n["SpecialtyCode"] == Var.specialty_add:
                idx = data.index(n)
                break

        # Specialty Code Click #1
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/table/tbody/tr["+str(idx+1)+"]/td[2]/a").click()
        driver.wait_for_request('.*/GetSpecialtyItemList.*')
        try:
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[4]/div/div/div[1]/h3"), "Specialty Rule Setting"))
        except:
            testResult = False
            Result_msg += "#1 "

        # Select Save #2
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#specialty_rulesetting_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty_rulesetting_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#specialty_rulesetting_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#specialty_rulesetting_request_code_chosen > a > span").click()
        code = driver.find_element(By.CSS_SELECTOR, "#specialty_rulesetting_request_code_chosen > div > ul > li:nth-child(1)").text
        driver.find_element(By.CSS_SELECTOR, "#specialty_rulesetting_request_code_chosen > div > ul > li:nth-child(1)").click()

        # save
        driver.find_element(By.CSS_SELECTOR, "#specialty-rulesetting-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[4]/div/div/div[1]/h3")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[4]/div/div/div[1]/h3").text
        # save
        driver.find_element(By.CSS_SELECTOR, "#specialty-rulesetting-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        del driver.requests
        time.sleep(1)

        # specialty code click
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/table/tbody/tr["+str(idx+1)+"]/td[2]/a").click()
        request = driver.wait_for_request('.*/GetSpecialtyItemList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        check = False
        idx = 0
        for n in data:
            if n["RequestCodeVal"] == code:
                idx = data.index(n)
                if driver.find_element(By.CSS_SELECTOR, "#specialty-rulesetting-rule-list > tbody > tr:nth-child("+str(idx+1)+") > td:nth-child(3)").text == code:
                    check = True
                break
        if (msg != "등록하시겠습니까?" or
            no_msg != "Specialty Rule Setting" or
            check == False):
            testResult = False
            Result_msg += "#2 "

        # Select Close #3
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#specialty_rulesetting_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty_rulesetting_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#specialty_rulesetting_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#specialty_rulesetting_request_code_chosen > a > span").click()
        code = driver.find_element(By.CSS_SELECTOR, "#specialty_rulesetting_request_code_chosen > div > ul > li:nth-child(1)").text
        driver.find_element(By.CSS_SELECTOR, "#specialty_rulesetting_request_code_chosen > div > ul > li:nth-child(1)").click()

        # close
        driver.find_element(By.CSS_SELECTOR, "#specialty-rulesetting-close-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[4]/div/div/div[1]/h3")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[4]/div/div/div[1]/h3").text
        # close
        driver.find_element(By.CSS_SELECTOR, "#specialty-rulesetting-close-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty-code-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "#specialty-tab-name").text

        if (msg != "등록을 취소하시겠습니까?" or 
            no_msg != "Specialty Rule Setting" or
            yes_msg != "Specialty List"):
            testResult = False
            Result_msg += "#3 "

        # Specialty Code Search #4
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/table/tbody/tr["+str(idx+1)+"]/td[2]/a").click()
        driver.wait_for_request('.*/GetSpecialtyItemList.*')

        del driver.requests
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#specialty_specialty_rule_search").send_keys(Var.specialty_add)
        driver.find_element(By.CSS_SELECTOR, "#specialty_specialty_rule_search_btn").click()
        request = driver.wait_for_request('.*/GetSpecialtyItemList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        for n in data:
            if Var.specialty_add not in n["SpecialtyCode"]:
                testResult = False
                Result_msg += "#4 "
                break

        # Request Code Search #5
        del driver.requests
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#specialty_specialty_rule_search_index_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty_specialty_rule_search_index_chosen > div > ul > li:nth-child(2)").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty_specialty_rule_search").send_keys(code.split(':')[0])
        driver.find_element(By.CSS_SELECTOR, "#specialty_specialty_rule_search_btn").click()

        request = driver.wait_for_request('.*/GetSpecialtyItemList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        for n in data:
            if code not in n["RequestCodeVal"]:
                testResult = False
                Result_msg += "#5 "
                break

        del driver.requests
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#specialty_specialty_rule_search").clear()
        driver.find_element(By.CSS_SELECTOR, "#specialty_specialty_rule_search_btn").click()
        driver.wait_for_request('.*/GetSpecialtyItemList.*')

        # Entries 25 #7
        del driver.requests
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#specialty-rulesetting-rule-list_length > label > select").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty-rulesetting-rule-list_length > label > select > option:nth-child(2)").click()
        request = driver.wait_for_request('.*/GetSpecialtyItem.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        
        if data["Length"] != 25:
            testResult = False
            Result_msg += "#7 "
        # Entries 10 #6
        del driver.requests
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#specialty-rulesetting-rule-list_length > label > select").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty-rulesetting-rule-list_length > label > select > option:nth-child(1)").click()
        request = driver.wait_for_request('.*/GetSpecialtyItem.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        
        if data["Length"] != 10:
            testResult = False
            Result_msg += "#6 "

        # Entries 50 #8
        del driver.requests
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#specialty-rulesetting-rule-list_length > label > select").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty-rulesetting-rule-list_length > label > select > option:nth-child(3)").click()
        request = driver.wait_for_request('.*/GetSpecialtyItem.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        
        if data["Length"] != 50:
            testResult = False
            Result_msg += "#8 "

        # Entries 100 #9
        del driver.requests
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#specialty-rulesetting-rule-list_length > label > select").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty-rulesetting-rule-list_length > label > select > option:nth-child(4)").click()
        request = driver.wait_for_request('.*/GetSpecialtyItem.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        
        if data["Length"] != 100:
            testResult = False
            Result_msg += "#9 "

        # Delete #10
        del driver.requests
        time.sleep(1)
        #delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr[1]/td[4]/a/i").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty-rulesetting-close-btn")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[4]/div/div/div[1]/h3").text

        del driver.requests
        time.sleep(1)

        #delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr[1]/td[4]/a/i").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        request = driver.wait_for_request('.*/GetSpecialtyItemList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        if (msg != "삭제하시겠습니까?" or
            no_msg != "Specialty Rule Setting"):
            testResult=False
            Result_msg+="#10 "
        
        if "#10" not in Result_msg:
            for n in data:
                if n["RequestCodeVal"] == code:
                    testResult = False
                    Result_msg += "#10 "

        # Close
        driver.find_element(By.CSS_SELECTOR, "#specialty-rulesetting-close-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        del driver.requests
        time.sleep(1)

        # Deletion
        #driver.find_element(By.CSS_SELECTOR, "#specialty-search-code").send_keys(Var.specialty_add)
        driver.find_element(By.CSS_SELECTOR, "#specialty-search").click()
        request = driver.wait_for_request('.*/GetSpecialtyList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        for n in data:
            if n["SpecialtyCode"] == Var.specialty_add:
                idx = data.index(n) + 1
                break

        driver.find_element(By.CSS_SELECTOR, "#specialty-code-list > tbody > tr:nth-child("+str(idx)+") > td:nth-child(1) > label").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/a[2]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # SpecialtyList_Modify결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1880, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1880, testPlanID, buildName, 'p', "SpecialtyList_Modify Test Passed")

    def InstitutionList_Search():
        print("ITR-60: Configuration > Specialty > Institution list > Search")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # Specialty
        driver.find_element(By.CSS_SELECTOR, "#specialty-btn").click()
        driver.wait_for_request('.*/GetSpecialtyList.*')  
        time.sleep(0.5)

        # InstitutionList
        driver.find_element(By.CSS_SELECTOR, "#tab-specialty-institution-list > a").click()
        request = driver.wait_for_request('.*/GetInstitutionListAssignedSpecialty.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        rnd_insti = data[0]["InstitutionName"]

        del driver.requests
        time.sleep(1)

        # Search #1
        driver.find_element(By.CSS_SELECTOR, "#specialtyInstitution-search-name").send_keys(rnd_insti)
        driver.find_element(By.CSS_SELECTOR, "#specialtyInstitution-search").click()

        request = driver.wait_for_request('.*/GetInstitutionListAssignedSpecialty.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        for n in range (0, len(data)):
            if (rnd_insti not in data[n]["InstitutionName"] or 
                data[n]["InstitutionName"] != driver.find_element(By.CSS_SELECTOR, "#specialty-institution-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(2)").get_property("textContent")):
                testResult = False
                Result_msg += "#1 "

        # InstitutionList_Search결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1893, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1893, testPlanID, buildName, 'p', "InstitutionList_Search Test Passed")

    def InstitutionList_Add():
        print("ITR-61: Configuration > Specialty > Institution list > Add")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # Specialty
        driver.find_element(By.CSS_SELECTOR, "#specialty-btn").click()
        driver.wait_for_request('.*/GetSpecialtyList.*')  
        time.sleep(0.5)

        # InstitutionList
        driver.find_element(By.CSS_SELECTOR, "#tab-specialty-institution-list > a").click()
        driver.wait_for_request('.*/GetInstitutionListAssignedSpecialty.*')
        time.sleep(0.5)

        # Add #1
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/a[1]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[5]/div/div/div[1]/h3")))
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[5]/div/div/div[1]/h3").text != "Specialty Registration":
            testResult = False
            Result_msg += "#1 "

        # Input Save #2
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_request_code_chosen > a > span")))
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_request_code_chosen > a > span").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_request_code_chosen > div > div > input[type=text]")))
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_request_code_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-specialty-code").send_keys(Var.specialty_add)
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-specialty-desc").send_keys(Var.specialty_add)
        # save
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-save-btn")))
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[5]/div/div/div[1]/h3")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[5]/div/div/div[1]/h3").text
        # save
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-save-btn")))
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        del driver.requests
        time.sleep(1)

        # search
        driver.find_element(By.CSS_SELECTOR, "#specialtyInstitution-search-name").send_keys(Var.search_institution_3)
        driver.find_element(By.CSS_SELECTOR, "#specialtyInstitution-search").click()
        request = driver.wait_for_request('.*/GetInstitutionListAssignedSpecialty.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        idx = -1
        for n in data:
            if n["InstitutionName"] == Var.search_institution_3:
                idx = data.index(n)
                break

        if (msg != "Specialty Rule을 등록하시겠습니까?" or
            no_msg != "Specialty Registration" or
            idx == -1):
            testResult = False
            Result_msg += "#2 "

        del driver.requests
        time.sleep(1)

        # Already Save #3
        # add
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[5]/div/div/div[1]/h3")))
        # input
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_request_code_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_request_code_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-specialty-code").send_keys(Var.specialty_add)
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-specialty-desc").send_keys(Var.specialty_add)  
        # save
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-save-btn")))
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[5]/div/div/div[1]/h3")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[5]/div/div/div[1]/h3").text
        # save
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-save-btn")))
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        request = driver.wait_for_request('.*/GetInstitutionListAssignedSpecialty.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        idx = -1
        for n in data:
            if n["InstitutionName"] == Var.search_institution_3:
                idx = data.index(n)
                break

        if (msg != "Specialty Rule을 등록하시겠습니까?" or
            no_msg != "Specialty Registration" or
            idx == -1):
            testResult = False
            Result_msg += "#3 "

        # NonInput Save #4
        # add
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[5]/div/div/div[1]/h3")))
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_request_code_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_add_request_code_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)

        if driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-save-btn").value_of_css_property("cursor") != "not-allowed":
            testResult = False
            Result_msg += "#4 "

        # Close #5
        # close
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-close-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[5]/div/div/div[1]/h3")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[5]/div/div/div[1]/h3").text
        # close
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-close-btn")))
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-add-close-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        yes_msg = driver.find_element(By.CSS_SELECTOR, "#specialtyInstitution-tab-name").text

        if (msg != "Specialty Rule 등록을 취소하시겠습니까?" or 
            no_msg != "Specialty Registration" or 
            yes_msg != "Institution List"):
            testResult = False
            Result_Msg += "#5 "

        # InstitutionList_Add결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1896, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1896, testPlanID, buildName, 'p', "InstitutionList_Add Test Passed")

    def InstitutionList_Delete():
        print("ITR-64: Configuration > Specialty > Institution list > Delete")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # Specialty
        driver.find_element(By.CSS_SELECTOR, "#specialty-btn").click()
        driver.wait_for_request('.*/GetSpecialtyList.*')  
        time.sleep(0.5)

        # InstitutionList
        driver.find_element(By.CSS_SELECTOR, "#tab-specialty-institution-list > a").click()
        driver.wait_for_request('.*/GetInstitutionListAssignedSpecialty.*')
        time.sleep(0.5)

        # Nonclick Delete #1
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/a[2]").value_of_css_property('cursor') != "not-allowed":
            testResult = False
            Result_msg += "#1 "

        del driver.requests
        time.sleep(1)

        # Search
        driver.find_element(By.CSS_SELECTOR, "#specialtyInstitution-search-name").send_keys(Var.search_institution_3)
        driver.find_element(By.CSS_SELECTOR, "#specialtyInstitution-search").click()
        request = driver.wait_for_request('.*/GetInstitutionListAssignedSpecialty.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        idx = -1
        for n in data:
            if n["InstitutionName"] == Var.search_institution_3:
                idx = data.index(n)
                break

        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/table/tbody/tr["+str(idx+1)+"]/td[1]/label").click()

        del driver.requests
        time.sleep(1)

        ## Delete #2
        ## delete
        #driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/a[2]").click()
        #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        #msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        ## no
        #time.sleep(1)
        #driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/a[2]")))
        #no_msg = driver.find_element(By.CSS_SELECTOR, "#specialtyInstitution-tab-name").text
        ## delete
        #driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/a[2]").click()
        #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        ## yes
        #driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        #WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        ## ok
        #driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        #request = driver.wait_for_request('.*/GetInstitutionListAssignedSpecialty.*')
        #body = request.response.body.decode('utf-8')
        #data = json.loads(body)["data"]

        #idx = -1
        #for n in data:
        #    if n["InstitutionName"] == search_institution_3:
        #        idx = data.index(n)
        #        break

        #if (msg != "Institution에 할당된 Specialty를 삭제하시겠습니까?" or 
        #    no_msg != "Specialty List" or
        #    idx != -1):
        #    testResult = False
        #    Result_msg += "#2 "

        #del driver.requests
        #time.sleep(1)

        # Specialty
        driver.find_element(By.CSS_SELECTOR, "#specialty-btn").click()
        driver.wait_for_request('.*/GetSpecialtyList.*')
        time.sleep(0.5)

        # InstitutionList
        driver.find_element(By.CSS_SELECTOR, "#tab-specialty-institution-list > a").click()
        request = driver.wait_for_request('.*/GetInstitutionListAssignedSpecialty.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        # Other Tab Delete #3
        if total < 2:
            testResult = False
            Result_msg += "#3 #4 "
        else:
            del driver.requests
            time.sleep(1)

            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/table/tbody/tr[1]/td[1]/label").click()
            driver.find_element(By.CSS_SELECTOR, "#specialty-institution-list_next > a").click()

            driver.wait_for_request('.*/GetInstitutionListAssignedSpecialty.*')

            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
                testResult = False
                Result_msg += "#3 "

            # Other Tab Delete > 2 #4
            del driver.requests
            time.sleep(1)

            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/table/tbody/tr[1]/td[1]/label").click()
            driver.find_element(By.CSS_SELECTOR, "#specialty-institution-list_previous > a").click()

            driver.wait_for_request('.*/GetInstitutionListAssignedSpecialty.*')

            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
                testResult = False
                Result_msg += "#4 "

        # InstitutionList_Delete결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1912, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1912, testPlanID, buildName, 'p', "InstitutionList_Delete Test Passed")

    def InstitutionList_Modify():
        print("ITR-65: Configuration > Specialty > Institution list > Modify")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # Specialty
        driver.find_element(By.CSS_SELECTOR, "#specialty-btn").click()
        driver.wait_for_request('.*/GetSpecialtyList.*')  
        time.sleep(0.5)

        # InstitutionList
        driver.find_element(By.CSS_SELECTOR, "#tab-specialty-institution-list > a").click()
        driver.wait_for_request('.*/GetInstitutionListAssignedSpecialty.*')
        time.sleep(0.5)

        # Search
        driver.find_element(By.CSS_SELECTOR, "#specialtyInstitution-search-name").send_keys(Var.search_institution_3)
        driver.find_element(By.CSS_SELECTOR, "#specialtyInstitution-search").click()
        request = driver.wait_for_request('.*/GetInstitutionListAssignedSpecialty.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        idx = -1
        for n in data:
            if n["InstitutionName"] == Var.search_institution_3:
                idx = data.index(n)
                break

        # Institution Name Click #1
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/table/tbody/tr["+str(idx+1)+"]/td[2]/a").click()
        driver.wait_for_request('.*/GetSpecialtyItemList.*')
        try:
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[6]/div/div/div[1]/h3"), "Specialty Rule Setting"))
        except:
            testResult = False
            Result_msg += "#1 "

        # Select Save #2
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_modify_specialty_code_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_modify_specialty_code_chosen > div > div > input[type=text]").send_keys(Var.specialty_add)
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_modify_specialty_code_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_modify_request_code_chosen > a > span").click()
        code = driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_modify_request_code_chosen > div > ul > li:nth-child(1)").text
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_modify_request_code_chosen > div > ul > li:nth-child(1)").click()

        # save
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[6]/div/div/div[1]/h3")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[6]/div/div/div[1]/h3").text
        # save
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        del driver.requests
        time.sleep(1)

        # institution name click
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/table/tbody/tr["+str(idx+1)+"]/td[2]/a").click()
        request = driver.wait_for_request('.*/GetSpecialtyItemList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        check = False
        idx = 0
        for n in data:
            if n["RequestCodeVal"] == code:
                idx = data.index(n)
                if driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-list > tbody > tr:nth-child("+str(idx+1)+") > td:nth-child(2)").text == code:
                    check = True
                break
        if (msg != "Specialty Rule을 등록하시겠습니까?" or
            no_msg != "Specialty Rule Setting" or
            check == False):
            testResult = False
            Result_msg += "#2 "

        # Select Close #3
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_modify_specialty_code_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_modify_specialty_code_chosen > div > div > input[type=text]").send_keys(Var.specialty_add)
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_modify_specialty_code_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_modify_request_code_chosen > a > span").click()
        code = driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_modify_request_code_chosen > div > ul > li:nth-child(1)").text
        driver.find_element(By.CSS_SELECTOR, "#specialty_institution_rulesetting_modify_request_code_chosen > div > ul > li:nth-child(1)").click()

        # close
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-close-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[6]/div/div/div[1]/h3")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[6]/div/div/div[1]/h3").text
        # close
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-close-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty-institution-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "#specialtyInstitution-tab-name").text

        if (msg != "Specialty Rule 등록을 취소하시겠습니까?" or 
            no_msg != "Specialty Rule Setting" or
            yes_msg != "Institution List"):
            testResult = False
            Result_msg += "#3 "

        # InstitutionList_Modify결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1918, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1918, testPlanID, buildName, 'p', "InstitutionList_Modify Test Passed")

    def InstitutionList_Modify_Search():
        print("ITR-68: Configuration > Specialty > Institution list > Modify - Search")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # Specialty
        driver.find_element(By.CSS_SELECTOR, "#specialty-btn").click()
        driver.wait_for_request('.*/GetSpecialtyList.*')  
        time.sleep(0.5)

        # InstitutionList
        driver.find_element(By.CSS_SELECTOR, "#tab-specialty-institution-list > a").click()
        driver.wait_for_request('.*/GetInstitutionListAssignedSpecialty.*')
        time.sleep(0.5)

        # Search
        driver.find_element(By.CSS_SELECTOR, "#specialtyInstitution-search-name").send_keys(Var.search_institution_3)
        driver.find_element(By.CSS_SELECTOR, "#specialtyInstitution-search").click()
        request = driver.wait_for_request('.*/GetInstitutionListAssignedSpecialty.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        idx = -1
        for n in data:
            if n["InstitutionName"] == Var.search_institution_3:
                idx = data.index(n)
                break

        del driver.requests
        time.sleep(1)

        # Institution Name Click
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/table/tbody/tr["+str(idx+1)+"]/td[2]/a").click()
        request = driver.wait_for_request('.*/GetSpecialtyItemList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[6]/div/div/div[1]/h3"), "Specialty Rule Setting"))

        code = ""
        for a in range (0, total):
            driver.wait_for_request('.*/GetSpecialtyItemList.*')
            time.sleep(0.5)
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for b in data:
                if b["SpecialtyCode"] == Var.specialty_add:
                    code = b["RequestCodeVal"]
                    break

            if (code != "" or 
                a+1 == total):
                break

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-list_next > a").click()

        del driver.requests
        time.sleep(1)

        # Specialty Code Search #1
        driver.find_element(By.CSS_SELECTOR, "#institution_specialty_rule_search").send_keys(Var.specialty_add)
        driver.find_element(By.CSS_SELECTOR, "#institution_specialty_rule_search_btn").click()

        request = driver.wait_for_request('.*/GetSpecialtyItemList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        for n in range (0, len(data)):
            if (Var.specialty_add not in data[n]["SpecialtyCode"] or 
                data[n]["SpecialtyCode"] != driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(1)").text):
                testResult = False
                Result_msg += "#1 "
        
        driver.find_element(By.CSS_SELECTOR, "#institution_specialty_rule_search").clear()

        del driver.requests
        time.sleep(1)

        # Request Code Search #2
        driver.find_element(By.CSS_SELECTOR, "#institution_specialty_rule_search_index_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#institution_specialty_rule_search_index_chosen > div > ul > li:nth-child(2)").click()
        driver.find_element(By.CSS_SELECTOR, "#institution_specialty_rule_search").send_keys(code.split(':')[0])
        driver.find_element(By.CSS_SELECTOR, "#institution_specialty_rule_search_btn").click()
        
        driver.wait_for_request('.*/GetSpecialtyItemList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        for n in range (0, len(data)):
            if (code.split(':')[0] not in data[n]["RequestCode"] or 
                data[n]["RequestCode"] not in driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-list > tbody > tr:nth-child("+str(n+1)+") > td:nth-child(2)").text):
                testResult = False
                Result_msg += "#2 "

        # Entries 25 #4
        del driver.requests
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-list_length > label > select").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-list_length > label > select > option:nth-child(2)").click()
        request = driver.wait_for_request('.*/GetSpecialtyItem.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        
        if data["Length"] != 25:
            testResult = False
            Result_msg += "#4 "
        # Entries 10 #3
        del driver.requests
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-list_length > label > select").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-list_length > label > select > option:nth-child(1)").click()
        request = driver.wait_for_request('.*/GetSpecialtyItem.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        
        if data["Length"] != 10:
            testResult = False
            Result_msg += "#3 "

        # Entries 50 #5
        del driver.requests
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-list_length > label > select").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-list_length > label > select > option:nth-child(3)").click()
        request = driver.wait_for_request('.*/GetSpecialtyItem.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        
        if data["Length"] != 50:
            testResult = False
            Result_msg += "#5 "

        # Entries 100 #6
        del driver.requests
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-list_length > label > select").click()
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-list_length > label > select > option:nth-child(4)").click()
        request = driver.wait_for_request('.*/GetSpecialtyItem.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        
        if data["Length"] != 100:
            testResult = False
            Result_msg += "#6 "

        del driver.requests
        time.sleep(1)

        # Search
        driver.find_element(By.CSS_SELECTOR, "#institution_specialty_rule_search").clear()
        driver.find_element(By.CSS_SELECTOR, "#institution_specialty_rule_search_index_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#institution_specialty_rule_search_index_chosen > div > ul > li:nth-child(1)").click()
        driver.find_element(By.CSS_SELECTOR, "#institution_specialty_rule_search").send_keys(Var.specialty_add)
        driver.find_element(By.CSS_SELECTOR, "#institution_specialty_rule_search_btn").click()

        request = driver.wait_for_request('.*/GetSpecialtyItemList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        idx = -1
        for n in data:
            if n["SpecialtyCode"] == Var.specialty_add:
                idx = data.index(n) + 1
                break
        
        # Delete #7
        #delete
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[3]/a/i").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-close-btn")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[6]/div/div/div[1]/h3").text
        #delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[3]/a/i").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

        del driver.requests
        time.sleep(1)

        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        request = driver.wait_for_request('.*/GetSpecialtyItemList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        if (msg != "Specialty Rule을 삭제하시겠습니까?" or
            no_msg != "Specialty Rule Setting"):
            testResult=False
            Result_msg+="#7 "
        
        if "#7" not in Result_msg:
            for n in data:
                if n["RequestCodeVal"] == code:
                    testResult = False
                    Result_msg += "#7 "

        # Close
        driver.find_element(By.CSS_SELECTOR, "#specialty-institution-rulesetting-modify-close-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # Yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        
        # InstitutionList_Modify_Search결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1931, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1931, testPlanID, buildName, 'p', "InstitutionList_Modify_Search Test Passed")


class DownloadControl:
    def User_SearchFilter_Class_Search(num):
        del driver.requests
        time.sleep(1)

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
                driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child("+str(n)+") > td:nth-child(4)").get_property("textContent") != (data[n-1]["Institution"].replace('<br />', '')).replace('&nbsp;', ' ')):
                check = False
                break
            
        return check
    # Render 확인
    def User_SearchFilter_Class():
        print("ITR-69: Configuration > Download Control > User > Search Filter - Class")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

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

        # User_SearchFilter_Class결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1942, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1942, testPlanID, buildName, 'p', "User_SearchFilter_Class Test Passed")

    def User_SearchFilter_Institution_Search(num):
        del driver.requests
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > a > span").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#download_search_institution_chosen > div > ul > li:nth-child("+str(num)+")")))
        check_insti = driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > ul > li:nth-child("+str(num)+")").get_property("outerText")
        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > ul > li:nth-child("+str(num)+")").click()
        driver.find_element(By.CSS_SELECTOR, "#download-search").click()

        request = driver.wait_for_request('.*/GetDownloadControlList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        time.sleep(1)
        check = True
        for n in range(1, len(data)+1):
            insti = (data[n-1]["Institution"].replace('<br />', '')).replace('&nbsp;', ' ')
            if (driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child("+str(n)+") > td:nth-child(2)").get_property("textContent") != data[n-1]["UserID"] or 
                driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child("+str(n)+") > td:nth-child(3)").get_property("textContent") != data[n-1]["UserName"] or 
                driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child("+str(n)+") > td:nth-child(4)").get_property("textContent") != insti or 
                insti != check_insti):
                check = False
                break
            
        return check

    def User_SearchFilter_Institution():
        print("ITR-70: Configuration > Download Control > User > Search Filter - Institution")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        del driver.requests
        time.sleep(1)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')

        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > a > span").click()
        child = driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > ul").get_property("childElementCount")
        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > ul > li:nth-child(1)").click()

        if child > 50:
            for a in range(2, 50):
                temp = DownloadControl.User_SearchFilter_Institution_Search(a)
                if temp == False:
                    testResult = False
                    Result_msg += "#1 "
                    break
        else:
            for a in range(2, child+1):
                temp = DownloadControl.User_SearchFilter_Institution_Search(a)
                if temp == False:
                    testResult = False
                    Result_msg += "#1 "
                    break

        # User_SearchFilter_Institution결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1945, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1945, testPlanID, buildName, 'p', "User_SearchFilter_Institution Test Passed")

    # target 1 = id / 2 = name
    def User_SearchFilter_Filter(target):
        rnd_id = driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child(1) > td:nth-child("+str(target+1)+")").get_property("textContent")
        rnd_insti = driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child(1) > td.align-center.download-control-institution").get_property("innerHTML")

        # User Management
        driver.find_element(By.CSS_SELECTOR, "#user-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[1]"), "User Management List"))
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(5) > div > label").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div["+str(target+2)+"]/div/div/input").send_keys(rnd_id)

        del driver.requests
        time.sleep(1)

        # search
        driver.find_element(By.CSS_SELECTOR, "#user-search").click()
        driver.wait_for_request('.*/GetUserList')
        rnd_class = driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr > td:nth-child(4)").get_property("textContent")

        del driver.requests
        time.sleep(1)

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
        time.sleep(1)

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
                driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child("+str(n)+") > td:nth-child(4)").get_property("textContent") != (data[n-1]["Institution"].replace('<br />', '')).replace('&nbsp;', ' ')):
                check = False
                break

        if check == True:
            del driver.requests
            time.sleep(1)

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
            time.sleep(1)

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
            time.sleep(1)

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
        print("ITR-71: Configuration > Download Control > User > Search Filter - UserID")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

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

        # User_SearchFilter_UserID결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1948, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1948, testPlanID, buildName, 'p', "User_SearchFilter_UserID Test Passed")

    def User_SearchFilter_UserName():
        print("ITR-72: Configuration > Download Control > User > Search Filter - User Name")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

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

        # User_SearchFilter_UserName결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1951, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1951, testPlanID, buildName, 'p', "User_SearchFilter_UserName Test Passed")

    def User_Add_DeletionSetup(insti_position):
        # Deletion
        driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr > td:nth-child(1) > label").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.delete-btn")))
        # delete
        driver.find_element(By.CSS_SELECTOR, "#download-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.delete-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # Add
        driver.find_element(By.CSS_SELECTOR, "#download-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#download-contol-add-save-btn"), "Save"))

        # User right
        driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_user_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(Var.wk_id_2)
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#download-config-add-user-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-user-remove-btn")))

        # Institution right 
        driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution > option:nth-child("+str(insti_position)+")").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-institution-add-btn")))
        driver.find_element(By.CSS_SELECTOR, "#download-config-add-institution-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-institution-remove-btn")))

    def User_Add():
        print("ITR-73: Configuration > Download Control > User > Add")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        #####request code, request name
        request_name = "Chest PA"
        #####
        
        Common.ReFresh()

        del driver.requests
        time.sleep(0.5)

        # Get info from list
        driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
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
            time.sleep(1)

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
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(Var.wk_id_2)
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#download-config-add-user-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-user-remove-btn")))
        if Var.wk_id_2 not in driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_selected_user_chosen > a > span").text:
            testResult = False
            Result_msg += "#1 "

        # User left #2
        driver.find_element(By.CSS_SELECTOR, "#download-config-add-user-remove-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#sel_available_download_control_add_selected_user_chosen > a > span"),"Select an Option"))
        driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_user_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(Var.wk_id_2)
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(Keys.ENTER)
        if Var.wk_id_2 not in driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_user_chosen > a > span").text:
            testResult = False
            Result_msg += "#2 "

        # User right
        driver.find_element(By.CSS_SELECTOR, "#download-config-add-user-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-user-remove-btn")))

        if "#1" not in Result_msg:
            # Institution right #3
            left_insti_count = driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution").get_property("childElementCount")
            for n in range (1, left_insti_count+1):
                if driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution > option:nth-child("+str(n)+")").text == Var.search_institution_3:
                    insti_position = n
                    driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution > option:nth-child("+str(insti_position)+")").click()
                    break
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-institution-add-btn")))
            driver.find_element(By.CSS_SELECTOR, "#download-config-add-institution-add-btn").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-institution-remove-btn")))
            right_insti_count = driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-selected-institution").get_property("childElementCount")
            if driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-selected-institution > option:nth-child("+str(right_insti_count)+")").text != Var.search_institution_3:
                testResult = False
                Result_msg += "#3 "

            # Institution left #4
            driver.find_element(By.CSS_SELECTOR, "#download-config-add-institution-remove-btn").click()
            try:
                WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#sel-available-download-control-add-institution > option:nth-child("+str(insti_position)+")"), Var.search_institution_3))
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
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[5]/div/div/div[1]/h3")))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[5]/div/div/div[1]/h3").text
            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            
            del driver.requests
            time.sleep(1)   

            # search
            driver.find_element(By.CSS_SELECTOR, "#download-search-user-id").send_keys(Var.wk_id_2)
            driver.find_element(By.CSS_SELECTOR, "#download-search").click()
            driver.wait_for_request('.*/GetDownloadControlList.*')

            if (msg != "등록하시겠습니까?" or 
                no_msg != "Download Control Registration" or 
                driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr > td:nth-child(2)").get_property("textContent") != Var.wk_id_2):
                testResult = False
                Result_msg += "#12 "
            
            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if n["JobPriority"] != "E":
                            testResult = False
                            Result_msg += "#5 "
                            break
                    elif n["JobPriority"] != "E" and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#5 "
                        break

                if ("#5" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

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
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if n["JobPriority"] == "E":
                            testResult = False
                            Result_msg += "#6 "
                            break
                    elif n["JobPriority"] == "E" and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#6 "
                        break

                if ("#6" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

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
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

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
                time.sleep(1)

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
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        testResult = False
                        Result_msg += "#8 "
                        break
                    elif Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#8 "
                        break

                if ("#8" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

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
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_modality_chosen > ul > li > input").click()
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_modality_chosen > ul > li > input").send_keys(temp_modal)
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_modality_chosen > ul > li > input").send_keys(Keys.ENTER)
            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if target_modal != n["Modality"]:
                            testResult = False
                            Result_msg += "#9 "
                            break
                    elif target_modal != n["Modality"] and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#9 "
                        break

                if ("#9" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

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
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if target_date != (n["JobDateDTTMString"].split(' '))[0]:
                            testResult = False
                            Result_msg += "#10 "
                            break
                    elif target_date != (n["JobDateDTTMString"].split(' '))[0] and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#10 "
                        break

                if ("#10" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            DownloadControl.User_Add_DeletionSetup(insti_position)

            # Specialty #11
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_specialty_chosen > ul > li > input").send_keys(Var.specialty)
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_specialty_chosen > ul > li > input").send_keys(Keys.ENTER)

            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if request_name != n["RequestName"]:
                            testResult = False
                            Result_msg += "#11 "
                            break
                    elif request_name != n["RequestName"] and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#11 "
                        break

                if ("#11" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

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
            time.sleep(1)
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

        # DownloadControl_User_Add결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1954, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1954, testPlanID, buildName, 'p', "User_Add Test Passed")

    def User_Delete():
        print("ITR-74: Configuration > Download Control > User > Delete")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')
        
        # Add
        driver.find_element(By.CSS_SELECTOR, "#download-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#download-contol-add-save-btn"), "Save"))

        # User right
        driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_add_user_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(Var.wk_id_2)
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#download-config-add-user-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-user-remove-btn")))
        
        # Institution right
        left_insti_count = driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution").get_property("childElementCount")
        for n in range (1, left_insti_count+1):
            if driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution > option:nth-child("+str(n)+")").text == Var.search_institution_3:
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
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # Ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # Nonclick Delete #1
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
            testResult = False
            Result_msg += "#1 "

        # Search
        driver.find_element(By.CSS_SELECTOR, "#download-search-user-id").send_keys(Var.wk_id_2)
        driver.find_element(By.CSS_SELECTOR, "#download-search").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#download-list > tbody > tr > td:nth-child(2)"), Var.wk_id_2))
        
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

        # User_Delete결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1969, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1969, testPlanID, buildName, 'p', "User_Delete Test Passed")

    def User_Modify():
        print("ITR-75: Configuration > Download Control > User > Modify")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        #####request code, request name
        request_name = "Chest PA"
        #####
        
        Common.ReFresh()

        del driver.requests
        time.sleep(0.5)

        # Get info from list
        driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
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
            time.sleep(1)

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
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(Var.wk_id_2)
        driver.find_element(By.CSS_SELECTOR, '#sel_available_download_control_add_user_chosen > div > div > input[type=text]').send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#download-config-add-user-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-add-user-remove-btn")))
        
        # Institution right
        left_insti_count = driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution").get_property("childElementCount")
        for n in range (1, left_insti_count+1):
            if driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-add-institution > option:nth-child("+str(n)+")").text == Var.search_institution_3:
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
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # Ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # Search
        driver.find_element(By.CSS_SELECTOR, "#download-search-user-id").send_keys(Var.wk_id_2)
        driver.find_element(By.CSS_SELECTOR, "#download-search").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#download-list > tbody > tr > td:nth-child(2)"), Var.wk_id_2))

        # User ID Click #1
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[1]/td[2]/a").click()
        request = driver.wait_for_request('.*/GetModifyInstitutionList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        if (Var.wk_id_2 not in driver.find_element(By.CSS_SELECTOR, "#download-control-modify-user-name").get_property("textContent") or
            data[0]["InstitutionName"] != Var.search_institution_3 or
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[6]/div/div/div[2]/div[2]/div/div/div[3]/select/option[1]").get_property("text") != Var.search_institution_3 or 
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
                if driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-all-institution > option:nth-child("+str(n)+")").text == Var.search_institution_3:
                    insti_position = n
                    driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-all-institution > option:nth-child("+str(insti_position)+")").click()
                    break

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-modify-institution-add-btn")))
            driver.find_element(By.CSS_SELECTOR, "#download-config-modify-institution-add-btn").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-modify-institution-remove-btn")))
            right_insti_count = driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-institution").get_property("childElementCount")
            if driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-institution > option:nth-child("+str(right_insti_count)+")").text != Var.search_institution_3:
                testResult = False
                Result_msg += "#2 "

            # Institution left #3
            driver.find_element(By.CSS_SELECTOR, "#download-config-modify-institution-remove-btn").click()
            try:
                WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#sel-available-download-control-modify-all-institution > option:nth-child("+str(insti_position)+")"), Var.search_institution_3))
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
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[6]/div/div/div[1]/h3")))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[6]/div/div/div[1]/h3").text
            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            driver.wait_for_request('.*/GetDownloadControlList.*')

            del driver.requests
            time.sleep(1)

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
            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if n["JobPriority"] != "E":
                            testResult = False
                            Result_msg += "#5 "
                            break
                    elif n["JobPriority"] != "E" and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#5 "
                        break

                if ("#5" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Not Emergency Only #6
            # emergency only off
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(1) > label").click()
            # not emergency only on 
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(2) > label").click()

            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            driver.wait_for_request('.*/GetDownloadControlList.*')

            del driver.requests
            time.sleep(1)

            # user select
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/GetModifyInstitutionList.*')
            # institution click
            driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-institution > option:nth-child("+str(right_insti_count)+")").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-modify-institution-remove-btn")))

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if n["JobPriority"] == "E":
                            testResult = False
                            Result_msg += "#6 "
                            break
                    elif n["JobPriority"] == "E" and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#6 "
                        break

                if ("#6" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Both on #7
            # emergency only on
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(1) > label").click()

            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            driver.wait_for_request('.*/GetDownloadControlList.*')

            del driver.requests
            time.sleep(1)

            # user select
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/GetModifyInstitutionList.*')
            # institution click
            driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-institution > option:nth-child("+str(right_insti_count)+")").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-modify-institution-remove-btn")))

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

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
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()
            if emergency_check == False or normal_check == False:
                testResult = False
                Result_msg += "#7 "

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Both off #8
            # emergency only off
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(1) > label").click()
            # not emergency only off
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(2) > label").click()
            time.sleep(2)

            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            driver.wait_for_request('.*/GetDownloadControlList.*')

            del driver.requests
            time.sleep(1)

            # user select
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/GetModifyInstitutionList.*')
            # institution click
            driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-institution > option:nth-child("+str(right_insti_count)+")").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-modify-institution-remove-btn")))

            request = driver.wait_for_request('.*/GetModalityList')
            body = request.response.body.decode('utf-8')
            modal_data = json.loads(body)

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        testResult = False
                        Result_msg += "#8 "
                        break
                    elif Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#8 "
                        break

                if ("#8" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Modality #9
            # both on
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(1) > label").click()
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(2) > label").click()
            
            for n in modal_data:
                if n["ModalityCode"] == target_modal:
                    temp_modal = n["ModalityDesc"]
                    break
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_modify_modality_chosen > ul > li > input").click()
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_modify_modality_chosen > ul > li > input").send_keys(temp_modal)##
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_modify_modality_chosen > ul > li > input").send_keys(Keys.ENTER)
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#sel_available_download_control_modify_modality_chosen > ul > li.search-choice > span"), temp_modal))

            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            driver.wait_for_request('.*/GetDownloadControlList.*')

            del driver.requests
            time.sleep(1)

            # user select
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/GetModifyInstitutionList.*')
            # institution click
            driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-institution > option:nth-child("+str(right_insti_count)+")").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-modify-institution-remove-btn")))

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if target_modal != n["Modality"]:
                        if n["Refer"] == None:
                            testResult = False
                            Result_msg += "#9 "
                            break
                        elif Var.wk_id_2 not in n["Refer"]:
                            testResult = False
                            Result_msg += "#9 "
                            break

                if ("#9" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Date(Job date) #10
            # modality off
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_modify_modality_chosen > ul > li.search-choice > a").click()

            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-starting-date").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div[2]/button[4]")))
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
                if (driver.find_element(By.XPATH, "/html/body/div[6]/div/div[1]/div[1]/div[3]/div[2]").text == year and 
                    driver.find_element(By.XPATH, "/html/body/div[6]/div/div[1]/div[1]/div[1]/div[2]").text == month):
                    break
                driver.find_element(By.XPATH, "/html/body/div[6]/div/div[1]/div[1]/div[1]/div[1]/a/i").click()
                time.sleep(0.3)
            time.sleep(1)
            check = False
            for a in range(2, 7):
                for b in range(1, 8):
                    if driver.find_element(By.XPATH, "/html/body/div[6]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").get_property("textContent") == day:
                        driver.find_element(By.XPATH, "/html/body/div[6]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").click()
                        check = True
                        break
                if check == True:
                    break
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#download-control-modify-starting-date"), target_date))

            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-ending-date").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div/div[2]/button[4]")))
            while(1):
                if (driver.find_element(By.XPATH, "/html/body/div[7]/div/div[1]/div[1]/div[3]/div[2]").text == year and 
                    driver.find_element(By.XPATH, "/html/body/div[7]/div/div[1]/div[1]/div[1]/div[2]").text == month):
                    break
                driver.find_element(By.XPATH, "/html/body/div[7]/div/div[1]/div[1]/div[1]/div[1]/a/i").click()
                time.sleep(0.3)
            time.sleep(1)
            check = False
            for a in range(2, 7):
                for b in range(1, 8):
                    if driver.find_element(By.XPATH, "/html/body/div[7]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").get_property("textContent") == day:
                        driver.find_element(By.XPATH, "/html/body/div[7]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").click()
                        check = True
                        break
                if check == True:
                    break
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#download-control-modify-ending-date"), target_date))

            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            driver.wait_for_request('.*/GetDownloadControlList.*')

            del driver.requests
            time.sleep(1)

            # user select
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/GetModifyInstitutionList.*')
            # institution click
            driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-institution > option:nth-child("+str(right_insti_count)+")").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-modify-institution-remove-btn")))

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if target_date != (n["JobDateDTTMString"].split(' '))[0]:
                            testResult = False
                            Result_msg += "#10 "
                            break
                    elif target_date != (n["JobDateDTTMString"].split(' '))[0] and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#10 "
                        break

                if ("#10" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Specialty #11
            # date clear
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-starting-date").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div[2]/button[4]")))
            driver.find_element(By.XPATH, "/html/body/div[6]/div/div[2]/button[2]").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-contol-modify-save-btn")))
            driver.find_element(By.CSS_SELECTOR, "#download-control-modify-ending-date").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div/div[2]/button[4]")))
            driver.find_element(By.XPATH, "/html/body/div[7]/div/div[2]/button[2]").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-contol-modify-save-btn")))
            
            # specialty
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_modify_specialty_chosen > ul > li > input").click()
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_modify_specialty_chosen > ul > li > input").send_keys(Var.specialty)
            driver.find_element(By.CSS_SELECTOR, "#sel_available_download_control_modify_specialty_chosen > ul > li > input").send_keys(Keys.ENTER)

            # save
            driver.find_element(By.CSS_SELECTOR, "#download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            driver.wait_for_request('.*/GetDownloadControlList.*')

            del driver.requests
            time.sleep(1)

            # user select
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/GetModifyInstitutionList.*')
            # institution click
            driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-institution > option:nth-child("+str(right_insti_count)+")").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-modify-institution-remove-btn")))

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if request_name != n["RequestName"]:
                            testResult = False
                            Result_msg += "#11 "
                            break
                    elif request_name != n["RequestName"] and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#11 "
                        break

                if ("#11" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Close #14
            # close
            driver.find_element(By.CSS_SELECTOR, "#download-contol-modify-close-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            # no
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-contol-modify-close-btn")))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[6]/div/div/div[1]/h3").text
            # close
            driver.find_element(By.CSS_SELECTOR, "#download-contol-modify-close-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            if (msg != "수정을 취소하시겠습니까?" or 
                no_msg != "Download Control Modify" or 
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[1]/h4").text != "Download Control List"):
                testResult = False
                Result_msg += "#14 "

            # user select
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/GetModifyInstitutionList.*')
            # institution click
            driver.find_element(By.CSS_SELECTOR, "#sel-available-download-control-modify-institution > option:nth-child("+str(right_insti_count)+")").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-config-modify-institution-remove-btn")))

            # Delete #12
            # delete
            driver.find_element(By.CSS_SELECTOR, "#download-contol-modify-delete-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            # no
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-contol-modify-delete-btn")))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[6]/div/div/div[1]/h3").text
            # delete
            driver.find_element(By.CSS_SELECTOR, "#download-contol-modify-delete-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"),"OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-search")))

            request = driver.wait_for_request('.*/GetDownloadControlList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in data:
                if n["UserID"]==Var.wk_id_2:
                    testResult= False
                    Result_msg += "#12 "

            if "#12" not in Result_msg:
                if (msg != "삭제하시겠습니까?" or
                    no_msg != "Download Control Modify"):
                    testResult= False
                    Reuslt_msg += "#12 "
       
        # User_Modify결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1975, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1975, testPlanID, buildName, 'p', "User_Modify Test Passed")

    def Institution_SearchFilter_Class_Search(num):
        del driver.requests
        time.sleep(1)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download_search_class_chosen > a > span")))
        driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > div > ul > li:nth-child("+(str(num))+")").click()
        driver.find_element(By.CSS_SELECTOR, "#download-search").click()

        request = driver.wait_for_request('.*/GetDownloadControlByInstList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        check = True
        for n in range(1, len(data)+1):
            if (driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child("+str(n)+") > td:nth-child(2)").get_property("textContent") != str(data[n-1]["InstitutionCode"]) or 
                driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child("+str(n)+") > td:nth-child(3)").get_property("textContent") != data[n-1]["InstitutionName"] or 
                driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child("+str(n)+") > td:nth-child(4)").get_property("textContent") != (data[n-1]["UserName"].replace('<br />', '')).replace('&nbsp;', ' ') or
                driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child("+str(n)+") > td:nth-child(5)").get_property("textContent") != (data[n-1]["Specialty"].replace('<br />', '')).replace('&nbsp;', ' ')):
                check = False
                break
            
        return check

    def Institution_SearchFilter_Class():
        print("ITR-76: Configuration > Download Control > Institution > Search Filter - Class")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')

        # Instituion
        driver.find_element(By.CSS_SELECTOR, "#tab-downloadControl-byInst-list").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-search")))

        # Class Search #1
        for a in range (2,6):
            temp = DownloadControl.Institution_SearchFilter_Class_Search(a)
            if temp == False:
                testResult = False
                Result_msg += "#1 "
                break

        # Institution_SearchFilter_Class결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1992, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1992, testPlanID, buildName, 'p', "Institution_SearchFilter_Class Test Passed")

    def Institution_SearchFilter_Institution_Search(num):
        del driver.requests
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > a > span").click()
        insti = driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > ul > li:nth-child("+str(num)+")").text
        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > ul > li:nth-child("+str(num)+")").click()
        check_insti = driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > ul > li:nth-child("+str(num)+")").get_property("outerText")
        driver.find_element(By.CSS_SELECTOR, "#download-search").click()

        request = driver.wait_for_request('.*/GetDownloadControlByInstList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        check = True
        for n in range(1, len(data)+1):
            if (driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child("+str(n)+") > td:nth-child(2)").get_property("textContent") != data[n-1]["InstitutionCode"] or 
                driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child("+str(n)+") > td:nth-child(3)").get_property("textContent") != data[n-1]["InstitutionName"] or 
                driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child("+str(n)+") > td:nth-child(4)").get_property("textContent") != (data[n-1]["UserName"].replace('<br />', '')).replace('&nbsp;', ' ') or
                driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child("+str(n)+") > td:nth-child(5)").get_property("textContent") != (data[n-1]["Specialty"].replace('<br />', '')).replace('&nbsp;', ' ') or
                insti !=  driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child("+str(n)+") > td:nth-child(3)").get_property("textContent")):
                check = False
                break
            
        return check

    def Institution_SearchFilter_Institution():
        print("ITR-77: Configuration > Download Control > Institution > Search Filter - Institution")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')
        
        # Instituion
        driver.find_element(By.CSS_SELECTOR, "#tab-downloadControl-byInst-list").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-search")))
        driver.wait_for_request('.*/GetInstitutionList')
        
        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > a > span").click()
        child = driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > ul").get_property("childElementCount")
        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > ul > li:nth-child(1)").click()

        if child > 50:
            for a in range(2, 50):
                temp = DownloadControl.Institution_SearchFilter_Institution_Search(a)
                if temp == False:
                    testResult = False
                    Result_msg += "#1 "
                    break
        else:
            for a in range(2, child + 1):
                temp = DownloadControl.Institution_SearchFilter_Institution_Search(a)
                if temp == False:
                    testResult = False
                    Result_msg += "#1 "
                    break

        # Institution_SearchFilter_Institution결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1995, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1995, testPlanID, buildName, 'p', "Institution_SearchFilter_Institution Test Passed")

    # target 1 = id / 2 = name
    def Institution_SearchFilter_Filter(target):
        print("ITR-78: Configuration > Download Control > Institution > Search Filter - User ID")
        run_time = time.time()
        rnd_id = driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child(1) > td:nth-child("+str(target+1)+")").get_property("textContent")
        rnd_insti = driver.find_element(By.CSS_SELECTOR, "#download-list > tbody > tr:nth-child(1) > td.align-center.download-control-institution").get_property("innerHTML").split('<br>')[0]
        # User Management
        driver.find_element(By.CSS_SELECTOR, "#user-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[1]"), "User Management List"))
        driver.find_element(By.CSS_SELECTOR, "#user-search-option > div > div:nth-child(5) > div > label").click()
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div["+str(target+2)+"]/div/div/input").send_keys(rnd_id)

        del driver.requests
        time.sleep(1)

        # search
        driver.find_element(By.CSS_SELECTOR, "#user-search").click()
        driver.wait_for_request('.*/GetUserList')
        rnd_class = driver.find_element(By.CSS_SELECTOR, "#user-list > tbody > tr > td:nth-child(4)").get_property("textContent")

        del driver.requests
        time.sleep(1)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')

        # Instituion
        driver.find_element(By.CSS_SELECTOR, "#tab-downloadControl-byInst-list").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-search")))

        request = driver.wait_for_request('.*/GetInstitutionList')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        
        for n in data:
            if n["InstitutionName"] == rnd_insti.split('<br>')[0]:
                insti_num = data.index(n) + 2
                break

        del driver.requests
        time.sleep(1)

        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div["+str(target+2)+"]/div/div/input").send_keys(rnd_id)
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-search")))
        driver.find_element(By.CSS_SELECTOR, "#download-search").click()

        request = driver.wait_for_request('.*/GetDownloadControlByInstList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        check = True
        for n in range(1, len(data)+1):
            if (rnd_id not in data[n-1]["UserName"] or
                driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child("+str(n)+") > td:nth-child(2)").get_property("textContent") != data[n-1]["InstitutionCode"] or 
                driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child("+str(n)+") > td:nth-child(3)").get_property("textContent") != data[n-1]["InstitutionName"] or 
                driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child("+str(n)+") > td:nth-child(4)").get_property("textContent") != ((data[n-1]["UserName"]).replace('<br />', '')).replace('&nbsp;', ' ') or 
                driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child("+str(n)+") > td:nth-child(5)").get_property("textContent") != (data[n-1]["Specialty"].replace('<br />', '')).replace('&nbsp;', ' ')):
                check = False
                break

        if check == True:
            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > a > span").click()
            for n in range(2,7):
                if rnd_class == driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > div > ul > li:nth-child("+str(n)+")").text:
                    driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > div > ul > li:nth-child("+str(n)+")").click()
                    break
            driver.find_element(By.CSS_SELECTOR, "#download-search").click()

            request = driver.wait_for_request('.*/GetDownloadControlByInstList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in range(1, len(data) + 1):
                if rnd_id not in driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child("+str(n)+") > td:nth-child(4)").get_property("textContent"):
                    check = False
                    break
            
        if check == True:
            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > div > ul > li:nth-child(1)").click()

            driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > ul > li:nth-child("+str(insti_num)+")").click()

            driver.find_element(By.CSS_SELECTOR, "#download-search").click()

            driver.wait_for_request('.*/GetDownloadControlByInstList.*')

            if rnd_id not in driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child(1) > td:nth-child(4)").get_property("textContent"):
                check = False

        if check == True:
            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > a > span").click()
            for n in range(2,7):
                if rnd_class == driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > div > ul > li:nth-child("+str(n)+")").text:
                    driver.find_element(By.CSS_SELECTOR, "#download_search_class_chosen > div > ul > li:nth-child("+str(n)+")").click()
                    break
            driver.find_element(By.CSS_SELECTOR, "#download-search").click()

            driver.wait_for_request('.*/GetDownloadControlByInstList.*')

            if rnd_id not in driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child(1) > td:nth-child(4)").get_property("textContent"):
                check = False

        return check

    def Institution_SearchFilter_UserID():
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')

        temp = DownloadControl.Institution_SearchFilter_Filter(target=1)

        if temp == False:
            testResult = False
            Result_msg += "#1 "

        # Institution_SearchFilter_UserID결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1998, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(1998, testPlanID, buildName, 'p', "Institution_SearchFilter_UserID Test Passed")

    def Institution_SearchFilter_UserName():
        print("ITR-79: Configuration > Download Control > Institution > Search Filter - User Name")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')  

        temp = DownloadControl.Institution_SearchFilter_Filter(target=2)

        if temp == False:
            testResult = False
            Result_msg += "#1 "

        # Institution_SearchFilter_UserName결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2001, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2001, testPlanID, buildName, 'p', "Institution_SearchFilter_UserName Test Passed")

    def Institution_Add_DeletionSetup(insti_position):
        # Deletion
        driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child(1) > td:nth-child(1) > label").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/div[1]/a[2]")))
        # delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/div[1]/a[2]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # Add
        driver.find_element(By.CSS_SELECTOR, "#download-list-byInst_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#byInst-download-contol-add-save-btn"), "Save"))

        # Institution right
        driver.find_element(By.CSS_SELECTOR, "#byInst-sel-available-download-control-add-institution > option:nth-child("+str(insti_position)+")").click()
        driver.find_element(By.CSS_SELECTOR, "#byInst-download-config-add-institution-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-add-institution-remove-btn")))

        # User right
        driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_user_chosen > a").click()
        driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
        driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#byInst-download-config-add-user-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-add-user-remove-btn")))

    def Institution_Add():
        print("ITR-80: Configuration > Download Control > Institution > Add")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "

        #####request code, request name
        request_name = "Chest PA"
        #####
        
        Common.ReFresh()

        del driver.requests
        time.sleep(0.5)

        # Get info from list
        driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
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
            time.sleep(1)

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
        
        # Instituion
        driver.find_element(By.CSS_SELECTOR, "#tab-downloadControl-byInst-list").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-search")))  
        
        del driver.requests
        time.sleep(1)

        # Add
        driver.find_element(By.CSS_SELECTOR, "#download-list-byInst_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#byInst-download-contol-add-save-btn"), "Save"))

        # Institution right #1
        request = driver.wait_for_request('.*/GetInstitutionList')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        for n in data:
            if n["InstitutionName"] == Var.search_institution_3:
                insti_position = data.index(n) + 1
                driver.find_element(By.CSS_SELECTOR, "#byInst-sel-available-download-control-add-institution > option:nth-child("+str(insti_position)+")").click()
                break
        driver.find_element(By.CSS_SELECTOR, "#byInst-download-config-add-institution-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-add-institution-remove-btn")))
        
        child = driver.find_element(By.CSS_SELECTOR, "#byInst-sel-available-download-control-add-selected-institution").get_property("childElementCount")
        if driver.find_element(By.CSS_SELECTOR, "#byInst-sel-available-download-control-add-selected-institution > option:nth-child("+str(child)+")").text != Var.search_institution_3:
            testResult = False
            Result_msg += "#1 "

        if testResult == True:
            # Institution left #2
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-config-add-institution-remove-btn").click()
            try:
                WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#byInst-sel-available-download-control-add-institution > option:nth-child("+str(insti_position)+")"), Var.search_institution_3))
            except:
                testResult = False
                Result_msg += "#2 "

            # Institution right
            driver.find_element(By.CSS_SELECTOR, "#byInst-sel-available-download-control-add-institution > option:nth-child("+str(insti_position)+")").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-config-add-institution-add-btn").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-add-institution-remove-btn")))

        if testResult == True:
            # User rigth #3
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_user_chosen > a").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-config-add-user-add-btn").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-add-user-remove-btn")))
            if driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_selected_user_chosen > a > span").text.split(' - ')[0] != Var.wk_id_2:
                testResult = False
                Result_msg += "#3 "

            if testResult == True:
                # User left #4
                driver.find_element(By.CSS_SELECTOR, "#byInst-download-config-add-user-remove-btn").click()
                try:
                    WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_selected_user_chosen > a > span"), "Select an Option"))
                except:
                    testResult = False
                    Result_msg += "#4 "

                # User right
                driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_user_chosen > a").click()
                driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
                driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
                driver.find_element(By.CSS_SELECTOR, "#byInst-download-config-add-user-add-btn").click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-add-user-remove-btn")))

        if testResult == True:
            # Emergency only, Save #5 #12
            # not emergency only off
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-add-popup-modal > div > div > div.modal-body > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(2) > label").click()
            ## save
            #driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-add-save-btn").click()
            #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            #msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            ## no
            #time.sleep(1)
            #driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[5]/div/div/div[1]/h3")))
            #no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[5]/div/div/div[1]/h3").text
            # save
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            
            del driver.requests
            time.sleep(1)   

            # search
            driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
            driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            driver.find_element(By.CSS_SELECTOR, "#download-search-user-id").send_keys(Var.wk_id_2)
            driver.find_element(By.CSS_SELECTOR, "#download-search").click()
            driver.wait_for_request('.*/GetDownloadControlByInstList.*')

            #if (msg != "등록하시겠습니까?" or 
            #    no_msg != "Download Control Registration" or 
            #    driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child(1) > td:nth-child(3)").get_property("textContent") != search_institution_3 or 
            #    driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child(1) > td.align-center.download-control-institution").text.split(' - ')[0] != Var.wk_id_2) :
            #    testResult = False
            #    Result_msg += "#12 "
            
            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if n["JobPriority"] != "E":
                            testResult = False
                            Result_msg += "#5 "
                            break
                    elif n["JobPriority"] != "E" and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#5 "
                        break

                if ("#5" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            DownloadControl.Institution_Add_DeletionSetup(insti_position)

            # Not Emergency Only #6
            # emergency only off
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-add-popup-modal > div > div > div.modal-body > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > label").click()
            # save
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if n["JobPriority"] == "E":
                            testResult = False
                            Result_msg += "#6 "
                            break
                    if n["JobPriority"] == "E" and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#6 "
                        break

                if ("#6" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            DownloadControl.Institution_Add_DeletionSetup(insti_position)

            # Both on #7
            # save
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

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
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()
            if emergency_check == False or normal_check == False:
                testResult = False
                Result_msg += "#7 "

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            DownloadControl.Institution_Add_DeletionSetup(insti_position)
           
            # Both off #8
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-add-popup-modal > div > div > div.modal-body > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > label").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-add-popup-modal > div > div > div.modal-body > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(2) > label").click()
            # save
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        testResult = False
                        Result_msg += "#8 "
                        break
                    elif Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#8 "
                        break

                if ("#8" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            DownloadControl.Institution_Add_DeletionSetup(insti_position)

            # Modality #9
            request = driver.wait_for_request('.*/GetModalityList')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            for n in data:
                if n["ModalityCode"] == target_modal:
                    temp_modal = n["ModalityDesc"]
                    break
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_modality_chosen > ul > li > input").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_modality_chosen > ul > li > input").send_keys(temp_modal)
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_modality_chosen > ul > li > input").send_keys(Keys.ENTER)

            # save
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if target_modal != n["Modality"]:
                            testResult = False
                            Result_msg += "#9 "
                            break
                    elif target_modal != n["Modality"] and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#9 "
                        break

                if ("#9" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            DownloadControl.Institution_Add_DeletionSetup(insti_position)

            # Date(Job date) #10
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-add-starting-date").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div[2]/button[4]")))
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
                if (driver.find_element(By.XPATH, "/html/body/div[8]/div/div[1]/div[1]/div[3]/div[2]").text == year and 
                    driver.find_element(By.XPATH, "/html/body/div[8]/div/div[1]/div[1]/div[1]/div[2]").text == month):
                    break
                driver.find_element(By.XPATH, "/html/body/div[8]/div/div[1]/div[1]/div[1]/div[1]/a/i").click()
                time.sleep(0.3)
            time.sleep(1)
            check = False
            for a in range(2, 7):
                for b in range(1, 8):
                    if driver.find_element(By.XPATH, "/html/body/div[8]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").get_property("textContent") == day:
                        driver.find_element(By.XPATH, "/html/body/div[8]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").click()
                        check = True
                        break
                if check == True:
                    break
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#byInst-download-control-add-starting-date"), target_date))

            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-add-ending-date").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[9]/div/div[2]/button[4]")))
            while(1):
                if (driver.find_element(By.XPATH, "/html/body/div[9]/div/div[1]/div[1]/div[3]/div[2]").text == year and 
                    driver.find_element(By.XPATH, "/html/body/div[9]/div/div[1]/div[1]/div[1]/div[2]").text == month):
                    break
                driver.find_element(By.XPATH, "/html/body/div[9]/div/div[1]/div[1]/div[1]/div[1]/a/i").click()
                time.sleep(0.3)
            time.sleep(1)
            check = False
            for a in range(2, 7):
                for b in range(1, 8):
                    if driver.find_element(By.XPATH, "/html/body/div[9]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").get_property("textContent") == day:
                        driver.find_element(By.XPATH, "/html/body/div[9]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").click()
                        check = True
                        break
                if check == True:
                    break
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#byInst-download-control-add-ending-date"), target_date))

            # save
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if target_date != (n["JobDateDTTMString"].split(' '))[0]:
                            testResult = False
                            Result_msg += "#10 "
                    elif target_date != (n["JobDateDTTMString"].split(' '))[0] and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#10 "
                        break

                if ("#10" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            DownloadControl.Institution_Add_DeletionSetup(insti_position)

            # Specialty #11
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_specialty_chosen > ul > li > input").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_specialty_chosen > ul > li > input").send_keys(Var.specialty)
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_specialty_chosen > ul > li > input").send_keys(Keys.ENTER)

            # save
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-add-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if request_name != n["RequestName"]:
                            testResult = False
                            Result_msg += "#11 "
                            break
                    elif request_name != n["RequestName"] and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#11 "
                        break

                if ("#11" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            DownloadControl.Institution_Add_DeletionSetup(insti_position)

            # Close #13
            # close
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-add-close-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            # no
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[7]/div/div/div[1]/h3")))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[7]/div/div/div[1]/h3").text
            # close
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-add-close-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            if (msg != "등록을 취소하시겠습니까?" or 
                no_msg != "Download Control Registration" or 
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[1]/h4").text != "Download Control List"):
                testResult = False
                Result_msg += "#13 "

        # Institution_Add결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2004, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2004, testPlanID, buildName, 'p', "Institution_Add Test Passed")

    def Institution_Delete():
        print("ITR-81: Configuration > Download Control > Institution > Delete")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')
        
        # Instituion
        driver.find_element(By.CSS_SELECTOR, "#tab-downloadControl-byInst-list").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-search")))   

        # Add
        driver.find_element(By.CSS_SELECTOR, "#download-list-byInst_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#byInst-download-contol-add-save-btn"), "Save"))

        # Institution right
        left_insti_count = driver.find_element(By.CSS_SELECTOR, "#byInst-sel-available-download-control-add-institution").get_property("childElementCount")
        for n in range (1, left_insti_count+1):
            if driver.find_element(By.CSS_SELECTOR, "#byInst-sel-available-download-control-add-institution > option:nth-child("+str(n)+")").text == Var.search_institution_3:
                driver.find_element(By.CSS_SELECTOR, "#byInst-sel-available-download-control-add-institution > option:nth-child("+str(n)+")").click()
                break
        driver.find_element(By.CSS_SELECTOR, "#byInst-download-config-add-institution-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-add-institution-remove-btn")))

        # User right
        driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_user_chosen > a").click()
        driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
        driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#byInst-download-config-add-user-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-add-user-remove-btn")))

        # save
        driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # Nonclick Delete #1
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
            testResult = False
            Result_msg += "#1 "

        # Search
        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#download-search-user-id").send_keys(Var.wk_id_2)
        driver.find_element(By.CSS_SELECTOR, "#download-search").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child(1) > td:nth-child(3)"), Var.search_institution_3))
        
        # Click Delete #2
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/table/tbody/tr[1]/td[1]/label").click()
        # delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/div[1]/a[2]").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[1]/h4").text
        # delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/div[1]/a[2]").click()
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

        del driver.requests
        time.sleep(1)

        # Instituion
        driver.find_element(By.CSS_SELECTOR, "#tab-downloadControl-byInst-list").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-search")))   

        request = driver.wait_for_request('.*/GetDownloadControlByInstList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        if total > 1:
            del driver.requests
            time.sleep(1)

            # Select Other Tab #3
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/table/tbody/tr[1]/td[1]/label").click()
            driver.find_element(By.CSS_SELECTOR, "#download-list-byInst_next > a").click()

            driver.wait_for_request('.*/GetDownloadControlByInstList.*')
            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
                testResult = False
                Result_msg += "#3 "

            del driver.requests
            time.sleep(1)

        # Select Other Tab > 2 #4
            element = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/table/tbody/tr[1]/td[1]/label")
            driver.execute_script("arguments[0].click()",element)
            driver.find_element(By.CSS_SELECTOR, "#download-list-byInst_previous > a").click()

            driver.wait_for_request('.*/GetDownloadControlByInstList.*')
            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/div[1]/a[2]").value_of_css_property("cursor") != "not-allowed":
                testResult = False
                Result_msg += "#4 "
        else:
            testResult = False
            Result_msg += "#3 #4 "

        # institution_delete결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2019, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2019, testPlanID, buildName, 'p', "institution_delete Test Passed")

    def Institution_Modify():
        print("ITR-82: Configuration > Download Control > Institution > Modify")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        #####request code, request name
        request_name = "Chest PA"
        #####

        Common.ReFresh()

        del driver.requests
        time.sleep(0.5)

        # Get info from list
        driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.wait_for_request(".*/GetAllAssignedList.*")
        time.sleep(0.5)

        del driver.requests
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#tab_all_list > a").click()
        request = driver.wait_for_request('.*/GetAllList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        target_modal = ""
        target_date = ""
        for a in range(0, total):
            request = driver.wait_for_request('.*/GetAllList.*')
            time.sleep(0.5)
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
            time.sleep(1)

            if (a+1 == total or
                (target_modal != "" and target_date != "")):
                break

            driver.find_element(By.CSS_SELECTOR, "#refer-assigned-list_next > a").click()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)
        time.sleep(0.5)

        # DownloadControl
        driver.find_element(By.CSS_SELECTOR, "#download-control-btn").click()
        driver.wait_for_request('.*/GetDownloadControlList.*')
        time.sleep(0.5)
        
        # Instituion
        driver.find_element(By.CSS_SELECTOR, "#tab-downloadControl-byInst-list").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-search")))   

        # Add
        driver.find_element(By.CSS_SELECTOR, "#download-list-byInst_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#byInst-download-contol-add-save-btn"), "Save"))

        # Institution right
        left_insti_count = driver.find_element(By.CSS_SELECTOR, "#byInst-sel-available-download-control-add-institution").get_property("childElementCount")
        for n in range (1, left_insti_count+1):
            if driver.find_element(By.CSS_SELECTOR, "#byInst-sel-available-download-control-add-institution > option:nth-child("+str(n)+")").text == Var.search_institution_3:
                driver.find_element(By.CSS_SELECTOR, "#byInst-sel-available-download-control-add-institution > option:nth-child("+str(n)+")").click()
                break
        driver.find_element(By.CSS_SELECTOR, "#byInst-download-config-add-institution-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-add-institution-remove-btn")))

        # User right
        driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_user_chosen > a").click()
        driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
        driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_add_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#byInst-download-config-add-user-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-add-user-remove-btn")))

        # save
        driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-add-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        # yes
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        
        del driver.requests
        time.sleep(1)

        # Search
        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#download_search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#download-search-user-id").send_keys(Var.wk_id_2)
        driver.find_element(By.CSS_SELECTOR, "#download-search").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child(1) > td:nth-child(3)"), Var.search_institution_3))
        time.sleep(1)

        # Institution click #1
        insti_code = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/table/tbody/tr[1]/td[2]/a").text
        insti_name = driver.find_element(By.CSS_SELECTOR, "#download-list-byInst > tbody > tr:nth-child(1) > td:nth-child(3)").text
        temp = "(" + insti_code + ") " + insti_name
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/table/tbody/tr[1]/td[2]/a").click()
        request = driver.wait_for_request('.*/ByInstGetModifyUserList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)

        check = False
        for n in data:
            if n["UserID"] == Var.wk_id_2:
                check = True
                break

        if (driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-modify-institution-name").text != temp or
            check == False or
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-modify-check-emergency-only").get_property("disabled") != True or 
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-modify-check-not-emergency-only").get_property("disabled") != True or 
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_modality_chosen > ul > li > input").get_property("disabled") != True or 
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-modify-starting-date").get_property("disabled") != True or 
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-modify-ending-date").get_property("disabled") != True or 
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_specialty_chosen > ul > li > input").get_property("disabled") != True ):
            testResult = False
            Result_msg += "#1 "

        if "#1" not in Result_msg:
            # User right #2
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_all_user_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_all_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_all_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-config-modify-user-add-btn").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-modify-user-remove-btn")))
            try:
                WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > a > span"), Var.wk_id_2))
            except:
                pass
            if driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > a > span").text.split(' - ')[0] != Var.wk_id_2:
                testResult = False
                Result_msg += "#2 "

            # Option on #4
            if (driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-modify-check-emergency-only").get_property("disabled") != False or 
                driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-modify-check-not-emergency-only").get_property("disabled") != False or 
                driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_modality_chosen > ul > li > input").get_property("disabled") != False or 
                driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-modify-starting-date").get_property("disabled") != False or 
                driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-modify-ending-date").get_property("disabled") != False or 
                driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_specialty_chosen > ul > li > input").get_property("disabled") != False ):
                testResult = False
                Result_msg += "#4 "

            # User left #3
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-config-modify-user-remove-btn").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > a > span"), "Select an Option"))
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_all_user_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_all_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_all_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            if driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_all_user_chosen > a > span").text.split(' - ')[0] != Var.wk_id_2:
                testResult = False
                Result_msg += "#3 "

            # User right
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-config-modify-user-add-btn").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-modify-user-remove-btn")))

        if testResult == True:
            # Emergency only, Save #5 #13
            # not emergency only off
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-byInst-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(2) > label").click()
            # save
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            # no
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[8]/div/div/div[1]/h3")))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[8]/div/div/div[1]/h3").text
            # save
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            driver.wait_for_request('.*/GetDownloadControlByInstList.*')
            time.sleep(0.5)

            del driver.requests
            time.sleep(1)

            # code click
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/ByInstGetModifyUserList.*')
            # user click
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-modify-user-remove-btn")))
            
            if (msg != "수정하시겠습니까?" or 
                no_msg != "Download Control Modify" or
                driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-modify-check-not-emergency-only").get_property("checked") != False ):
                testResult = False
                Result_msg += "#13 "

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if n["JobPriority"] != "E":
                            testResult = False
                            Result_msg += "#5 "
                            break
                    elif n["JobPriority"] != "E" and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#5 "
                        break

                if ("#5" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Not Emergency Only #6
            # emergency only off
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-byInst-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(1) > label").click()
            # not emergency only on 
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-byInst-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(2) > label").click()

            # save
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            driver.wait_for_request('.*/GetDownloadControlByInstList.*')

            del driver.requests
            time.sleep(1)

            # code click
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/ByInstGetModifyUserList.*')
            # user click
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-modify-user-remove-btn")))

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if n["JobPriority"] == "E":
                            testResult = False
                            Result_msg += "#6 "
                            break
                    elif n["JobPriority"] == "E" and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#6 "
                        break

                if ("#6" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Both on #7
            # emergency only on
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-byInst-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(1) > label").click()

            # save
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            driver.wait_for_request('.*/GetDownloadControlByInstList.*')

            del driver.requests
            time.sleep(1)

            # code click
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/ByInstGetModifyUserList.*')
            # user click
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-modify-user-remove-btn")))

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

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
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()
            if emergency_check == False or normal_check == False:
                testResult = False
                Result_msg += "#7 "

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Both off #8
            # emergency only off
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-byInst-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(1) > label").click()
            # not emergency only off
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-byInst-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(2) > label").click()
            time.sleep(2)

            # save
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            driver.wait_for_request('.*/GetDownloadControlByInstList.*')

            del driver.requests
            time.sleep(1)

            # code click
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/ByInstGetModifyUserList.*')
            # user click
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-modify-user-remove-btn")))

            request = driver.wait_for_request('.*/GetModalityList')
            body = request.response.body.decode('utf-8')
            modal_data = json.loads(body)

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        testResult = False
                        Result_msg += "#8 "
                        break
                    elif Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#8 "
                        break

                if ("#8" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Modality #9
            # both on
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-byInst-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(1) > label").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-byInst-modify-popup-modal > div > div > div.modal-body > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(2) > label").click()
            
            for n in modal_data:
                if n["ModalityCode"] == target_modal:
                    temp_modal = n["ModalityDesc"]
                    break
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_modality_chosen > ul > li > input").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_modality_chosen > ul > li > input").send_keys(temp_modal)##
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_modality_chosen > ul > li > input").send_keys(Keys.ENTER)
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_modality_chosen > ul > li.search-choice > span"), temp_modal))

            # save
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            driver.wait_for_request('.*/GetDownloadControlByInstList.*')

            del driver.requests
            time.sleep(1)

            # code click
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/ByInstGetModifyUserList.*')
            # user click
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-modify-user-remove-btn")))

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if target_modal != n["Modality"]:
                        if n["Refer"] == None:
                            testResult = False
                            Result_msg += "#9 "
                            break
                        elif Var.wk_id_2 not in n["Refer"]:
                            testResult = False
                            Result_msg += "#9 "
                            break

                if ("#9" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Date(Job date) #10
            # modality off
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_modality_chosen > ul > li.search-choice > a").click()

            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-modify-starting-date").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[10]/div/div[2]/button[4]")))
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
                if (driver.find_element(By.XPATH, "/html/body/div[10]/div/div[1]/div[1]/div[3]/div[2]").text == year and 
                    driver.find_element(By.XPATH, "/html/body/div[10]/div/div[1]/div[1]/div[1]/div[2]").text == month):
                    break
                driver.find_element(By.XPATH, "/html/body/div[10]/div/div[1]/div[1]/div[1]/div[1]/a/i").click()
                time.sleep(0.3)
            time.sleep(1)
            check = False
            for a in range(2, 7):
                for b in range(1, 8):
                    if driver.find_element(By.XPATH, "/html/body/div[10]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").get_property("textContent") == day:
                        driver.find_element(By.XPATH, "/html/body/div[10]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").click()
                        check = True
                        break
                if check == True:
                    break
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#byInst-download-control-modify-starting-date"), target_date))

            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-modify-ending-date").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[11]/div/div[2]/button[4]")))
            while(1):
                if (driver.find_element(By.XPATH, "/html/body/div[11]/div/div[1]/div[1]/div[3]/div[2]").text == year and 
                    driver.find_element(By.XPATH, "/html/body/div[11]/div/div[1]/div[1]/div[1]/div[2]").text == month):
                    break
                driver.find_element(By.XPATH, "/html/body/div[11]/div/div[1]/div[1]/div[1]/div[1]/a/i").click()
                time.sleep(0.3)
            time.sleep(1)
            check = False
            for a in range(2, 7):
                for b in range(1, 8):
                    if driver.find_element(By.XPATH, "/html/body/div[11]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").get_property("textContent") == day:
                        driver.find_element(By.XPATH, "/html/body/div[11]/div/div[1]/div[3]/div[1]/table/tbody/tr["+str(a)+"]/td["+str(b)+"]").click()
                        check = True
                        break
                if check == True:
                    break
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#byInst-download-control-modify-ending-date"), target_date))

            # save
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            driver.wait_for_request('.*/GetDownloadControlByInstList.*')

            del driver.requests
            time.sleep(1)

            # code click
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/ByInstGetModifyUserList.*')
            # user click
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-modify-user-remove-btn")))

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if target_date != (n["JobDateDTTMString"].split(' '))[0]:
                            testResult = False
                            Result_msg += "#10 "
                            break
                    elif target_date != (n["JobDateDTTMString"].split(' '))[0] and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#10 "
                        break

                if ("#10" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Specialty #11
            # date clear
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-modify-starting-date").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[10]/div/div[2]/button[4]")))
            driver.find_element(By.XPATH, "/html/body/div[10]/div/div[2]/button[2]").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-contol-modify-save-btn")))
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-control-modify-ending-date").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[11]/div/div[2]/button[4]")))
            driver.find_element(By.XPATH, "/html/body/div[11]/div/div[2]/button[2]").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-contol-modify-save-btn")))
            
            # specialty
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_specialty_chosen > ul > li > input").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_specialty_chosen > ul > li > input").send_keys(Var.specialty)
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_specialty_chosen > ul > li > input").send_keys(Keys.ENTER)

            # save
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-modify-save-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

            driver.wait_for_request('.*/GetDownloadControlByInstList.*')

            del driver.requests
            time.sleep(1)

            # code click
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/ByInstGetModifyUserList.*')
            # user click
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-modify-user-remove-btn")))

            # 새로운 탭 + 전환
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])

            del driver.requests
            time.sleep(1)

            driver.get(Var.WorklistUrl);
            signInOut.wk_login(Var.wk_id_2, Var.wk_pw_2)

            request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            total = math.ceil(data["recordsFiltered"]/data["Length"])

            for a in range (0, total+1):
                request = driver.wait_for_request('.*/GetCurrentJobWorklist.*')
                body = request.response.body.decode('utf-8')
                data = json.loads(body)["data"]

                for n in data:
                    if n["Refer"] == None:
                        if request_name != n["RequestName"] :
                            testResult = False
                            Result_msg += "#11 "
                            break
                    elif request_name != n["RequestName"] and Var.wk_id_2 not in n["Refer"]:
                        testResult = False
                        Result_msg += "#11 "
                        break

                if ("#11" in Result_msg or 
                    a+1 == total):
                    break

                del driver.requests
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "#current-job-list_next > a").click()

            # logout 및 전환
            driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout > span").click()
            driver.implicitly_wait(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Close #14
            # close
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-modify-close-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            # no
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-contol-modify-close-btn")))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[8]/div/div/div[1]/h3").text
            # close
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-modify-close-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            if (msg != "수정을 취소하시겠습니까?" or 
                no_msg != "Download Control Modify" or 
                driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div[1]/h4").text != "Download Control List"):
                testResult = False
                Result_msg += "#14 "

            # code click
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[4]/div/table/tbody/tr[1]/td[2]/a").click()
            driver.wait_for_request('.*/ByInstGetModifyUserList.*')
            # user click
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Var.wk_id_2)
            driver.find_element(By.CSS_SELECTOR, "#byInst_sel_available_download_control_modify_user_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-config-modify-user-remove-btn")))

            # Delete #12
            ## delete
            #driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-modify-delete-btn").click()
            #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            #msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            ## no
            #time.sleep(1)
            #driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#byInst-download-contol-modify-delete-btn")))
            #no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div[8]/div/div/div[1]/h3").text
            # delete
            driver.find_element(By.CSS_SELECTOR, "#byInst-download-contol-modify-delete-btn").click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"),"OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#download-search")))

            request = driver.wait_for_request('.*/GetDownloadControlByInstList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in data:
                if n["InstitutionName"]==Var.search_institution_3:
                    testResult= False
                    Result_msg += "#12 "

            #if "#12" not in Result_msg:
            #    if (msg != "삭제하시겠습니까?" or
            #        no_msg != "Download Control Modify"):
            #        testResult= False
            #        Reuslt_msg += "#12 "

        # Institution_Modify결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2025, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2025, testPlanID, buildName, 'p', "Institution_Modify Test Passed")

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

    def SearchFilter_Institution_Code():
        print("ITR-83: Configuration > Institution > Search Filter > Institution Code")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # Institution
        driver.find_element(By.CSS_SELECTOR, "#institutions-btn").click()
        request = driver.wait_for_request('.*/GetInstitutionsList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        search_institution_code = data[0]["InstitutionCode"]
        
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

            lst = ["InstitutionCode", "InstitutionName", "CenterCodeList", "ReportModificationMode", "ReportingRuleCount", "ReportingDownloadDelayTime"]
            for a in lst:
                if n[a] == None:
                    n[a] = ""

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

        # SearchFilter_InstitutionCode결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":    
                testlink.reportTCResult(2043, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2043, testPlanID, buildName, 'p', "SearchFilter_InstitutionCode Test Passed")
    
    def SearchFilter_Institution_Name():
        print("ITR-84: Configuration > Institution > Search Filter > Institution Name")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "

        del driver.requests
        time.sleep(1)
        
        driver.find_element(By.CSS_SELECTOR, "#institutions-search-institution-code").clear()
        driver.find_element(By.CSS_SELECTOR, "#institutions-search-institution-name").send_keys(Var.search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#institutions-search").click()

        request = driver.wait_for_request('.*/GetInstitutionsList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]

        check = True
        num = 0
        for n in data:
            if Var.search_institution_2 not in n["InstitutionName"]:
                check = False

            lst = ["InstitutionCode", "InstitutionName", "CenterCodeList", "ReportModificationMode", "ReportingRuleCount", "ReportingDownloadDelayTime"]
            for a in lst:
                if n[a] == None:
                    n[a] = ""

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

        # SearchFilter_InstitutionName결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2046, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2046, testPlanID, buildName, 'p', "SearchFilter_InstitutionName Test Passed")

    def Add():
        print("ITR-85: Configuration > Institution > Add")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)
        time.sleep(0.5)

        del driver.requests
        time.sleep(1)

        # Institution
        driver.find_element(By.CSS_SELECTOR, "#institutions-btn").click()
        request = driver.wait_for_request('.*/GetInstitutionsList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        search_institution_code = data[0]["InstitutionCode"]
        
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
            time.sleep(0.5)
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
            time.sleep(0.5)
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
            driver.find_element(By.CSS_SELECTOR, "#institutions_add_center_code_list_chosen > ul > li > input[type=text]").send_keys(Var.search_center)
            driver.find_element(By.CSS_SELECTOR, "#institutions_add_center_code_list_chosen > ul > li > input[type=text]").send_keys(Keys.ENTER)
            try:
                WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#institutions_add_center_code_list_chosen > ul > li.search-choice > span"),Var.search_center))
            except:
                testResult = False
                Result_msg += "#6 "

            # Center X #7
            if "#6" not in Result_msg:
                driver.find_element(By.CSS_SELECTOR, "#institutions_add_center_code_list_chosen > ul > li.search-choice > a").click()
                try:
                    WebDriverWait(driver, 0.5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#institutions_add_center_code_list_chosen > ul > li.search-choice > span"),Var.search_center))
                    testResult = False
                    Result_msg += "#7 "
                except:
                    pass
            
            # input Institution Name
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-institution-code").clear()
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-institution-code").send_keys("123456")
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-institution-name").send_keys("Cloud_ITRTest")

            del driver.requests
            time.sleep(1)

            # Save #15
            # save
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-save-btn").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            # no
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[3]/div/div/div[1]/h3")))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[3]/div/div/div[1]/h3").text
            # save
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-save-btn").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            try:
                assert((msg == "등록하시겠습니까?") and (no_msg == "Institutions Registration"))
                WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2"),"등록하였습니다."))
            except:
                testResult = False
                Result_msg += "#15 "
            # ok
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn"))) 

            if "#15" not in Result_msg:
                request = driver.wait_for_request('.*/GetInstitutionsList.*')
                time.sleep(0.5)
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
                    time.sleep(1)
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
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-add-close-btn")))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[3]/div/div/div[1]/h3").text
            # close
            driver.find_element(By.CSS_SELECTOR, "#institutions-add-close-btn").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            # yes
            time.sleep(0.5)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            #WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
            try:
                assert((msg == "등록을 취소하시겠습니까?")and(no_msg == "Institutions Registration"))
                WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#institutions-tab-name"),"Institution List"))
            except:
                testResult = False
                Result_msg += "#14 "

        # Institution_Add결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2049, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2049, testPlanID, buildName, 'p', "Institution_Add Test Passed")

    # Cloud_ITRTest
    def Delete():
        print("ITR-86: Configuration > Institution > Delete")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)
        time.sleep(0.5)

        del driver.requests
        time.sleep(1)

        # Institution
        driver.find_element(By.CSS_SELECTOR, "#institutions-btn").click()
        driver.wait_for_request('.*/GetInstitutionsList.*')
        time.sleep(0.5)
        
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
            time.sleep(0.5)
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
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "#institutions-list_next > a").click()
        # delete
        driver.find_element(By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.delete-btn").click()
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.delete-btn")))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#institutions-tab-name").text
        # delete
        driver.find_element(By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.delete-btn").click()
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

        del driver.requests
        time.sleep(1)

        # yes
        time.sleep(1)
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
            time.sleep(0.5)
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
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])

        if total < 2:
            testResult = False
            Result_msg += "#3 #4 "

        if ("#3" not in Result_msg) and ("#4" not in Result_msg):
            # Select & Other Tab #3
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr[1]/td[1]/label")))
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr[1]/td[1]/label").click()

            del driver.requests
            time.sleep(1)

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

        # Institution_Delete결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2066, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2066, testPlanID, buildName, 'p', "Institution_Delete Test Passed")

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
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), Var.search_institution_3))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[1]/h3").get_property("textContent")
        # save
        driver.find_element(By.CSS_SELECTOR, "#institutions-modify-save-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
        
        # 새로운 탭 + 전환
        driver.execute_script("window.open()")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(Var.WorklistUrl);
        driver.implicitly_wait(5)
        signInOut.wk_login(Var.wk_id, Var.wk_pw)

        # search hospital
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > a").click()
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_3)
        driver.find_element(By.CSS_SELECTOR, "#search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#current-hospital-name"), Var.search_institution_3))
        
        # set job report
        driver.find_element(By.CSS_SELECTOR, "#setting_columns > i").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#setting-columns-apply")))
        if driver.find_element(By.CSS_SELECTOR, "#chk-column-5").get_property("checked") == False:
            driver.find_element(By.CSS_SELECTOR, "#modal-setting-columns > div > div > div.modal-body > div:nth-child(1) > div.setting-column > ul > li:nth-child(5) > label").click()
        driver.find_element(By.CSS_SELECTOR, "#setting-columns-apply").click()
        time.sleep(1)
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
        print("ITR-87: Configuration > Institution > Modify")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)
        time.sleep(0.5)

        del driver.requests
        time.sleep(1)

        # Institution
        driver.find_element(By.CSS_SELECTOR, "#institutions-btn").click()
        driver.wait_for_request('.*/GetInstitutionsList.*')
        time.sleep(0.5)
        
        # Find
        idx = Institution.insti_idx_find(Var.search_institution_3)
        # Select Institution Code #1
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), Var.search_institution_3))
        try:
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), Var.search_institution_3))
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
            time.sleep(1)
            # save
            driver.find_element(By.CSS_SELECTOR, "#institutions-modify-save-btn").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            # no
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), Var.search_institution_3+"_re"))
            no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[1]/h3").get_property("textContent")
            # save
            driver.find_element(By.CSS_SELECTOR, "#institutions-modify-save-btn").click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2")))

            del driver.requests
            time.sleep(1)

            # yes
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))
            # find
            idx = Institution.insti_idx_find(Var.search_institution_3+"_re")
            if (idx == 0 or 
                msg != "수정하시겠습니까?" or 
                no_msg != "Institutions Modify") :
                testResult = False
                Result_msg += "#3 "

            # Select Institution Code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), Var.search_institution_3))
            driver.find_element(By.CSS_SELECTOR, "#institutions-modify-institution-name").clear()
            driver.find_element(By.CSS_SELECTOR, "#institutions-modify-institution-name").send_keys(Var.search_institution_3)

            time.sleep(1)#
            # Center X #5
            temp = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[1]/div[3]/div/div[2]/div/ul/li[1]/span").get_property("outerText")
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[1]/div[3]/div/div[2]/div/ul/li[1]/a").click()
            driver.find_element(By.CSS_SELECTOR, "#institutions_modify_center_code_list_chosen > ul > li.search-field > input[type=text]").click()
            time.sleep(1)
            child = driver.find_element(By.CSS_SELECTOR, "#institutions_modify_center_code_list_chosen > div > ul").get_property("childElementCount")
            check = False
            for n in range (1, child+1):
                if temp == driver.find_element(By.CSS_SELECTOR, "#institutions_modify_center_code_list_chosen > div > ul > li:nth-child("+str(n)+")").text:
                    
                    check = True
                    break
            if check == False:
                testResult = False
                Result_msg += "#5 "

            # Center Select #4
            driver.find_element(By.CSS_SELECTOR, "#institutions_modify_center_code_list_chosen > ul > li.search-field > input[type=text]").send_keys(temp)
            driver.find_element(By.CSS_SELECTOR, "#institutions_modify_center_code_list_chosen > ul > li.search-field > input[type=text]").send_keys(Keys.ENTER)
            
            elements = driver.find_elements(By.CSS_SELECTOR, "#institutions_modify_center_code_list_chosen > ul > li.search-choice > span")
            check = False
            for n in elements:
                if temp == n.get_property("outerText"):
                    check = True
                    break
            if check  == False:
                testResult = False
                Result_msg += "#4 "

            # Report Mode, Delay Time, Save #6 7 13
            ori_RM = driver.find_element(By.CSS_SELECTOR, "#institutions_modify_report_mode_chosen > a > span").text
            ori_RDT = driver.find_element(By.CSS_SELECTOR, "#institutions_modify_report_time_chosen > a > span").text
            ori_comment = driver.find_element(By.CSS_SELECTOR, "#institutions-modify-use-referring-comment2").get_property("checked")
            ori_revised = driver.find_element(By.CSS_SELECTOR, "#institutions-modify-enable-revised").get_property("checked")
            ori_discard = driver.find_element(By.CSS_SELECTOR, "#institutions-modify-enable-discard").get_property("checked")
            ori_request = driver.find_element(By.CSS_SELECTOR, "#institutions-modify-enable-request").get_property("checked") 

            #driver.find_element(By.CSS_SELECTOR, "#institutions-modify-institution-name").send_keys("")

            temp = Institution.Modify_ToWL(1, "", 1, "0분")
            if temp != "":
                testResult= False
                Result_msg += temp

            # Find
            idx = Institution.insti_idx_find(Var.search_institution_3)
        
            # select institution code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), Var.search_institution_3))

            temp = Institution.Modify_ToWL(2, "Overwrite", 2, "30분")
            if temp != "":
                testResult= False
                Result_msg += temp

            # Find
            idx = Institution.insti_idx_find(Var.search_institution_3)
        
            # select institution code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), Var.search_institution_3))

            temp = Institution.Modify_ToWL(3, "Addendum", 3, "60분")
            if temp != "":
                testResult= False
                Result_msg += temp

            # Find
            idx = Institution.insti_idx_find(Var.search_institution_3)
        
            # select institution code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), Var.search_institution_3))

            temp = Institution.Modify_ToWL(4, "Prohibition", 4, "120분")
            if temp != "":
                testResult= False
            Result_msg += temp 

            # Find
            idx = Institution.insti_idx_find(Var.search_institution_3)
        
            # select institution code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), Var.search_institution_3))

            temp = Institution.Modify_ToWL(4, "Prohibition", 5, "180분")
            if temp != "":
                testResult= False
                Result_msg += temp 

            # Find
            idx = Institution.insti_idx_find(Var.search_institution_3)
        
            # select institution code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), Var.search_institution_3))

            # Comment, Revised, Discard, Request  #8 9 10 11
            # comment - check
            if ori_comment == driver.find_element(By.CSS_SELECTOR, "#institutions-modify-use-referring-comment2").get_property("checked") == False:
                driver.find_element(By.CSS_SELECTOR, "#not-use-default-refer-comment > div:nth-child(6) > div > div > label").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#institution-modify-refer-comment-select-box > li > span"), "+ Create New Comment"))

            del driver.requests
            time.sleep(1)

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
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))

            del driver.requests
            time.sleep(1)
            
            # refer
            element = driver.find_element(By.CSS_SELECTOR, "#tab-refer > a")
            driver.execute_script("arguments[0].click()",element)
            driver.wait_for_request(".*/GetReferCountsByInstitution.*")
            time.sleep(0.5)

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
            driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            driver.wait_for_request(".*/GetAllAssignedList.*")
            time.sleep(0.5)

            del driver.requests
            time.sleep(1)
            
            driver.find_element(By.CSS_SELECTOR, "#tab_all_list > a").click()
            driver.wait_for_request(".*/GetAllList.*")
            time.sleep(0.5)

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
            time.sleep(1)

            # Configuration
            driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
            driver.implicitly_wait(5)

            # Institution
            driver.find_element(By.CSS_SELECTOR, "#institutions-btn").click()
            driver.wait_for_request('.*/GetInstitutionsList.*')
            time.sleep(0.5)

            # Find
            idx = Institution.insti_idx_find(Var.search_institution_3)

            del driver.requests
            time.sleep(1)
        
            # select institution code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), Var.search_institution_3))

            # delete comment
            driver.wait_for_request(".*/LoadReferringComments")
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[4]/div/div/div[2]/div[2]/div/div[2]/ul/li[2]/button")))
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
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
            # ok
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#institutions-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn")))

            del driver.requests
            time.sleep(1)
            
            # refer
            element = driver.find_element(By.CSS_SELECTOR, "#tab-refer > a")
            driver.execute_script("arguments[0].click()",element)
            driver.wait_for_request(".*/GetReferCountsByInstitution.*")
            time.sleep(0.5)

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > a > span").click()
            driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
            driver.find_element(By.CSS_SELECTOR, "#refer_search_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
            driver.wait_for_request(".*/GetAllAssignedList.*")
            time.sleep(0.5)

            del driver.requests
            time.sleep(1)
            
            driver.find_element(By.CSS_SELECTOR, "#tab_all_list > a").click()
            driver.wait_for_request(".*/GetAllList.*")
            time.sleep(0.5)

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
            time.sleep(1)

            # Configuration
            driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
            driver.implicitly_wait(5)

            # Institution
            driver.find_element(By.CSS_SELECTOR, "#institutions-btn").click()
            driver.wait_for_request('.*/GetInstitutionsList.*')
            time.sleep(0.5)

            # Find
            idx = Institution.insti_idx_find(Var.search_institution_3)

            del driver.requests
            time.sleep(1)
        
            # select institution code
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(idx)+"]/td[2]/a").click()
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#institutions-modify-institution-name"), Var.search_institution_3))
            
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
            time.sleep(1)
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
            time.sleep(1)
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

        # Institution_Modify결과 전송 ##
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2072, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2072, testPlanID, buildName, 'p', "Institution_Modify Test Passed")

#GroupCode_Test
#ReportCode_Test
# Add > GroupAdd > GroupModify > Modify > Delete
class StandardReport:
    def GroupAdd():
        print("ITR-89: Configuration > Standard Report > Group Add")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()
        time.sleep(1)

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # StandardReport
        driver.find_element(By.CSS_SELECTOR, "#standard-report-btn").click()
        driver.wait_for_request('.*/StandardReport.*')
        time.sleep(0.5)
        
        # None Select Group Add #1
        if driver.find_element(By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn.group-add-btn.disabled").value_of_css_property("cursor") != "not-allowed":
            testResult = False
            Result_msg += "#1 "

        # Find & Select
        check = False
        while(1):
            request = driver.wait_for_request('.*/GetStandardReportList.*')
            time.sleep(0.5)
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
        time.sleep(1)

        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.5)
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
            time.sleep(1)
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
        time.sleep(1)
        # yes
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        time.sleep(0.5)
        if driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text != "등록하였습니다.":
            testResult = False
            Result_msg += "#2 "
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        driver.wait_for_request('.*/StandardReport.*')
        time.sleep(0.5)

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
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-group-add-close-btn")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[5]/div/div/div[1]/h3").get_property("textContent")
        # close
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-add-close-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        # yes
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.add-btn.group-add-btn")))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "#standard-report-tab-name").get_property("textContent")
        if (msg != "등록을 취소하시겠습니까?" or
            no_msg != "Standard Report Group Registration" or
            yes_msg != "Standard Report List"):
            testResult = False
            Result_msg += "#3 "

        # StandardReport_GroupAdd결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2091, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2091, testPlanID, buildName, 'p', "StandardReport_GroupAdd Test Passed")

    def Add():
        print("ITR-90: Configuration > Standard Report > Add")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # StandardReport
        driver.find_element(By.CSS_SELECTOR, "#standard-report-btn").click()
        driver.wait_for_request('.*/StandardReport.*')
        time.sleep(0.5)

        del driver.requests

        # Add #1
        driver.find_element(By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a:nth-child(2) > span").click()
        driver.wait_for_request('.*/GetStandardReportCreatorID')
        if driver.find_element(By.CSS_SELECTOR, "#standard-report-add-creator").get_property("value") != Var.adminID:
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
        time.sleep(1)

        ## yes
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[14]/div[7]/div/button"), "OK"))
        ok_msg = driver.find_element(By.XPATH, "/html/body/div[14]/h2").get_property("textContent")
        driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()

        check = False
        while(1):
            request = driver.wait_for_request('.*/GetStandardReportList.*')
            time.sleep(0.5)
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
            time.sleep(1)
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
        time.sleep(0.5)

        # Alreay Report Code #4
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-report-code").send_keys("ReportCode_Test")
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-add-report-code"), "ReportCode_Test"))
        # save
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-add-save-btn")))
        element = driver.find_element(By.CSS_SELECTOR, "#standard-report-add-save-btn")
        driver.execute_script("arguments[0].click()",element)
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
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-add-creator"), Var.adminID))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#addStandartReportLabel").get_property("textContent")
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-close-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.visible.showSweetAlert > div.sa-button-container > div > button"), "Yes"))
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr[1]/td[4]/a")))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "#standard-report-tab-name").get_property("textContent")
        if (msg != "등록을 취소하시겠습니까?" or 
            no_msg != "Standard Report Registration" or 
            yes_msg != "Standard Report List"):
            testResult = False
            Result_msg += "#10 "

        # StandardReport_Add결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2096, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2096, testPlanID, buildName, 'p', "StandardReport_Add Test Passed")

    def Delete():
        print("ITR-91: Configuration > Standard Report > Delete")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # StandardReport
        driver.find_element(By.CSS_SELECTOR, "#standard-report-btn").click()
        driver.wait_for_request('.*/StandardReport.*')
        time.sleep(0.5)

        # Non-Select Delete #1
        if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/div[1]/a[3]").value_of_css_property("cursor") != "not-allowed":
            testResult = False
            Result_msg += "#1 "

        # Select Delete #2
        # Find & Select
        check = False
        check2 = False
        while(1):
            request = driver.wait_for_request('.*/GetStandardReportList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in data:
                if n["ReportCode"] == "ReportCode_Test":
                    check = True
                    num = data.index(n) + 1
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num)+"]/td[1]/label").click()
                if n["ReportCode"] == "ReportCode_Test3":
                    check2 = True
                    num2 = data.index(n) + 1
                    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num2)+"]/td[1]/label").click()
                    break
            if check == True and check2 == True:
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
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a.dt-button.btn.btn-xs.waves-effect.delete-btn")))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#standard-report-tab-name").get_property("textContent")
        # Delete
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/div[1]/a[3]").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        del driver.requests
        time.sleep(1)
        # yes
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a:nth-child(2)")))

        # 패킷으로 지움확인
        check = False
        request = driver.wait_for_request('.*/GetStandardReportList.*')
        time.sleep(0.5)
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
            time.sleep(1)

            if a+1 == total:
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
        time.sleep(0.5)
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

        # StandardReport_Delete결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2108, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2108, testPlanID, buildName, 'p', "StandardReport_Delete Test Passed")

    # ReportCode_Test Search
    def ReportSearch(total):
        num = 0
        for a in range(1, total+1):
            request = driver.wait_for_request('.*/GetStandardReportList.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)["data"]

            for n in data:
                if "ReportCode_Test" in n["ReportCode"]:
                    num = data.index(n) + 1
                    break

            if num != 0:
                break
            
            del driver.requests
            time.sleep(1)

            if a == total:
                break
            driver.find_element(By.CSS_SELECTOR, "#standard-report-list_next > a").click()

        return num


    def GroupModify():
        print("ITR-92: Configuration > Standard Report > Group Modify")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        del driver.requests
        time.sleep(1)

        # StandardReport
        driver.find_element(By.CSS_SELECTOR, "#standard-report-btn").click()
        request = driver.wait_for_request('.*/GetStandardReportList.*')
        time.sleep(0.5)
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
        time.sleep(0.5)
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
        time.sleep(1)

        # yes
        time.sleep(0.5)
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
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#standard-report-add-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[14]/div[7]/div/button"),"Yes"))
        del driver.requests
        time.sleep(1)
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
        time.sleep(0.5)
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
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-modify-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))

        del driver.requests
        time.sleep(1)

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
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[6]/div/div/div[1]/h3")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[6]/div/div/div[1]/h3").get_property("textContent")
        # close
        driver.find_element(By.CSS_SELECTOR, "#standard-report-group-modify-close-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        # yes
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-btn")))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "#standard-report-tab-name").get_property("textContent")
        if (msg != "수정을 취소하시겠습니까?" or 
            no_msg != "Standard Report Group Modify" or 
            yes_msg != "Standard Report List"):
            testResult = False
            Result_msg += "#4 "

        # StandardReport_GroupModify결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2114, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2114, testPlanID, buildName, 'p', "StandardReport_GroupModify Test Passed")

    def Modify():
        print("ITR-93: Configuration > Standard Report > Modify")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)

        # StandardReport
        driver.find_element(By.CSS_SELECTOR, "#standard-report-btn").click()
        request = driver.wait_for_request('.*/GetStandardReportList.*')
        time.sleep(0.5)
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        
        num = StandardReport.ReportSearch(total)

        # Report Code Click #1
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num+1)+"]/td[4]/a").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-creator"), Var.adminID))
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
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-creator"), Var.adminID))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[4]/div/div/div[1]/h3").get_property("textContent")
        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        # yes
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        ok_msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # ok
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-list_wrapper > div.dt-buttons > a:nth-child(2)")))

        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num+1)+"]/td[4]/a").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-creator"), Var.adminID))
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
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-creator"), Var.adminID))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[4]/div/div/div[1]/h3").get_property("textContent")
        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        # yes
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        yes_msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # ok
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-modify-save-btn")))
        if (msg != "수정하시겠습니까?" or 
            no_msg != "Standard Report Modify" or 
            yes_msg != "수정을 실패하였습니다." or 
            driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[4]/div/div/div[1]/h3").get_property("textContent") != "Standard Report Modify"):
            testResult = False
            Result_msg += "#4 "

        time.sleep(0.5)
        # new #5
        driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-report-code").send_keys("3")
        # save
        element = driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-save-btn")
        driver.execute_script("arguments[0].click()",element)
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-creator"), Var.adminID))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[4]/div/div/div[1]/h3").get_property("textContent")

        del driver.requests
        time.sleep(1)

        # save
        driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-save-btn").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        # yes
        time.sleep(1)
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

        request = driver.wait_for_request('.*/GetStandardReportList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        
        num = StandardReport.ReportSearch(total)
        
        # Close #10
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/table/tbody/tr["+str(num+1)+"]/td[4]/a").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#standard-report-modify-creator"), Var.adminID))
        # close
        element = driver.find_element(By.CSS_SELECTOR, "#standard-report-modify-close-btn")
        driver.execute_script("arguments[0].click()",element)
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "Yes"))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # no
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#standard-report-modify-close-btn")))
        no_msg = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[4]/div/div/div[1]/h3").get_property("textContent")
        # close
        time.sleep(0.5)
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

        # StandardReport_Modify결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2120, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2120, testPlanID, buildName, 'p', "StandardReport_Modify Test Passed")
    
    def All():
        StandardReport.Add()
        StandardReport.GroupAdd()
        StandardReport.GroupModify()
        StandardReport.Modify()
        StandardReport.Delete()

class MultiReadingCenterRule:
    def SearchFilter():
        print("ITR-94: Configuration > Multi Reading Center Rule > Search Filter")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

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
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-search").click()
        request = driver.wait_for_request('.*/GetMultiReadingCenterRuleList.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)["data"]
        time.sleep(1)
        for n in range (1, len(data)+1):
            if driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[2]/div/table/tbody/tr["+str(n)+"]/td[4]").get_property("textContent") != modal:
                testResult = False
                Result_msg += "#3 "
                break

        # MultiReadingCenterRule_SearchFilter결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2133, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2133, testPlanID, buildName, 'p', "MultiReadingCenterRule_SearchFilter Test Passed")

    def Add():
        print("ITR-95: Configuration > Multi Reading Center Rule > Add")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

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
        time.sleep(0.25)
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
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_institution_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        # Center
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > div > div > input[type=text]").send_keys(Var.search_center)
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
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_add_center_chosen > div > div > input[type=text]").send_keys(Var.search_center_2)
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
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        try:
            time.sleep(0.25)
            driver.find_element(By.XPATH, "/html/body/div[14]/div[7]/div/button").click()
        except:
            testResult = False
            Result_msg += "#11 "
 
        # MultiReadingCenterRule_Add결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2140, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2140, testPlanID, buildName, 'p', "MultiReadingCenterRule_Add Test Passed")

    def Delete():
        print("ITR-96: Configuration > Multi Reading Center Rule > Delete")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # Configuration
        driver.find_element(By.CSS_SELECTOR, "#tab-config > a").click()
        driver.implicitly_wait(5)
        time.sleep(0.15)

        # MultiReadingCenterRule
        driver.find_element(By.CSS_SELECTOR, "#multiReadingCenterRule-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi_center_rule_search_modality_chosen > a > span")))

        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_institutioncode_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_institutioncode_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_institutioncode_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_centercode_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_centercode_chosen > div > div > input[type=text]").send_keys(Var.search_center_2)
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

        # MultiReadingCenterRule_Delete결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2154, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2154, testPlanID, buildName, 'p', "MultiReadingCenterRule_Delete Test Passed")

    def Modify():
        print("ITR-97: Configuration > Multi Reading Center Rule > Modify")
        run_time = time.time()
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

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
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_institutioncode_chosen > div > div > input[type=text]").send_keys(Var.search_institution_2)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_institutioncode_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_centercode_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_centercode_chosen > div > div > input[type=text]").send_keys(Var.search_center_2)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_centercode_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)                    
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
        time.sleep(0.25)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#modifyCenterRuleLabel")))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#modifyCenterRuleLabel").get_property("textContent")
        # left
        driver.find_element(By.CSS_SELECTOR, "#modify-multi-center-rule-modality-remove-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#multi-center-rule-modify-save-btn")))
        # save
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modify-save-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        # yes
        time.sleep(0.25)
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

        # Modal Right
        driver.find_element(By.CSS_SELECTOR, "#modify-multi-center-rule-modality-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modify-multi-center-rule-modality-remove-btn")))
        # Center Right
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_center_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_center_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#modify-multi-center-rule-center-add-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modify-multi-center-rule-center-remove-btn")))

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
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#selected_multi_center_rule_modify_center_chosen > a > span"),Var.search_center))
        no_msg = driver.find_element(By.CSS_SELECTOR, "#modifyCenterRuleLabel").get_property("textContent")
        # change to on save
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_modality_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_modality_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#modify-multi-center-rule-modality-add-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modify-multi-center-rule-modality-remove-btn")))
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

        del driver.requests
        time.sleep(1)

        # search
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_centercode_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_centercode_chosen > div > div > input[type=text]").send_keys(Var.search_center_2)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_search_centercode_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-search").click()

        driver.wait_for_request('.*/GetMultiReadingCenterRuleList.*')

        # institution name click
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[2]/div/table/tbody/tr[1]/td[2]/a")))
        driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[11]/div[2]/div/table/tbody/tr[1]/td[2]/a").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#modifyCenterRuleLabel")))
        # modality check
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_center_chosen > a > span").click()
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_center_chosen > div > div > input[type=text]").send_keys(Var.search_center)
        driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_center_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)

        if (msg != "수정하시겠습니까?" or
            no_msg != "Multi Reading Center Rule Modify" or
            yes_msg != "수정하였습니다." or 
            driver.find_element(By.CSS_SELECTOR, "#multi_center_rule_modify_center_chosen > a > span").text != Var.search_center_2):
            testResult = False
            Result_msg += "#4 "

        # left
        driver.find_element(By.CSS_SELECTOR, "#modify-multi-center-rule-center-remove-btn").click()
        if (one_remain == "not-allowed" or
            driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modify-save-btn").value_of_css_property("cursor") != "not-allowed"):
            testResult = False
            Result_msg += "#5 "

        ## Change Save #8 #보류

        # Close #9
        # close
        driver.find_element(By.CSS_SELECTOR, "#multi-center-rule-modify-close-btn").click()
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#modifyCenterRuleLabel")))
        msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").get_property("textContent")
        # no
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#selected_multi_center_rule_modify_center_chosen > a > span"), Var.search_center_2))
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
        
        # MultiReadingCenterRule_Modify결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            Common_Var.form.update_failed()
            Common_Var.run_status = "Failed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2157, testPlanID, buildName, 'f', Result_msg)            
        else:
            Common_Var.form.update_passed()
            Common_Var.run_status = "Passed"
            Common_Var.runtime = str(round((int(time.time() - run_time)/60),2))
            Common_Var.form.update_table()
            if Common_Var.planid != "":
                testlink.reportTCResult(2157, testPlanID, buildName, 'p', "MultiReadingCenterRule_Modify Test Passed")

    def All():
        MultiReadingCenterRule.Add()
        MultiReadingCenterRule.Modify()
        MultiReadingCenterRule.Delete()