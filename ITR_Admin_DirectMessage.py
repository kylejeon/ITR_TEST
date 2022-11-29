from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import json
import random
import math
from datetime import datetime
import ITR_Admin_Login
from ITR_Admin_Common import driver
from ITR_Admin_Common import testlink
from ITR_Admin_Common import testPlanID
from ITR_Admin_Common import buildName
from ITR_Admin_Common import Var
from ITR_Admin_Common import Common

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
        print("ITR-107: Direct Message > Direct Message Box > Search")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

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
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_value").send_keys(Var.search_id)
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search > i").click()
        
        request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        for current_page in range(0, total):
            for n in range (1, (len(data["data"]) + 1) ):
                if Var.search_id not in driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div[4]/div[2]/table/tbody/tr["+str(n)+"]/td[3]").text:
                        testResult = False
                        Result_msg += "#2 "

            if current_page + 1 == total:
                break
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_value").clear()

        # User Name Search #3
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_type").click()
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_type > option:nth-child(2)").click()
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_value").send_keys(Var.search_username)
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search > i").click()
        
        request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        for current_page in range(0, total):
            for n in range (1, (len(data["data"]) + 1) ):
                if Var.search_username not in driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div[4]/div[2]/table/tbody/tr["+str(n)+"]/td[3]").text:
                        testResult = False
                        Result_msg += "#3 "

            if current_page + 1 == total:
                break
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_value").clear()

        del driver.requests
        time.sleep(1)

        # Msg Text Search #4
        del driver.requests
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_type").click()
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_type > option:nth-child(3)").click()
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search_value").send_keys(Var.search_text)
        driver.find_element(By.CSS_SELECTOR, "#direct_message_search > i").click()
        
        request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
        body = request.response.body.decode('utf-8')
        data = json.loads(body)
        total = math.ceil(data["recordsFiltered"] / data["Length"])
        for current_page in range(0, total):
            for n in range (1, (len(data["data"]) + 1) ):
                if Var.search_text not in driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div[4]/div[2]/table/tbody/tr["+str(n)+"]/td[2]").text.lower():
                    testResult = False
                    Result_msg += "#4 "
                    break

            if (current_page + 1 == total or
                "#4" in Result_msg ):
                break

        # DirectMessageBox_Search결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
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
        print("ITR-108: Direct Message > Direct Message Box > Show Entries")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # 10 #2
        temp = DirectMessage.DirectMessageBox_ShowEntries_fun(10, 2)
        if temp != "":
            testResult = False
            Result_msg += temp

        # 5 #1
        temp = DirectMessage.DirectMessageBox_ShowEntries_fun(5, 1)
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

        # DirectMessageBox_ShowEntries결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
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
        print("ITR-109: Direct Message > Direct Message Box > Sorting")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

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

        # DirectMessageBox_Sorting결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2245, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2245, testPlanID, buildName, 'p', "DirectMessageBox_Sorting Test Passed")
   
    def DirectMessageBox_Badge():
        print("ITR-110: Direct Message > Direct Message Box > Badge")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

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
            request = driver.wait_for_request('.*/GetDirectMessageListForTable.*')
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
            time.sleep(0.5)

            for b in range(1, len(data["data"])+1):
                if driver.find_element(By.CSS_SELECTOR, "#message_list_group > tbody > tr:nth-child("+str(b)+") > td:nth-child(1)").get_property("textContent") == "mail":
                    unread_count += 1
                else:
                    break
            if driver.find_element(By.CSS_SELECTOR, "#message_list_group > tbody > tr:nth-child("+str(len(data["data"]))+") > td:nth-child(1)").get_property("textContent") == "drafts" or a == total:
                break

            del driver.requests
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "#message_list_group_next > a").click()

        try:
            assert(unread_count != driver.find_element(By.CSS_SELECTOR, "#direct_message_total_count").text and
                   unread_count != driver.find_element(By.CSS_SELECTOR, "#unread_dm_cnt").text)
        except:
            testResult = False
            Result_msg += "#1 "
            
        # DirectMessageBox_Badge결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2250, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2250, testPlanID, buildName, 'p', "DirectMessageBox_Badge Test Passed")

    def DirectMessageBox_Message():
        print("ITR-111: Direct Message > Direct Message Box > Message")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        del driver.requests
        time.sleep(1)

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
        try:
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#load_message_text"), target[2]))
            assert(target[0] == driver.find_element(By.CSS_SELECTOR, "#load_message_writer").get_property("value") and 
                   target[1] == driver.find_element(By.CSS_SELECTOR, "#load_message_write_dttm").get_property("value") and
                   target[2] == driver.find_element(By.CSS_SELECTOR, "#load_message_text").get_property("value"))
        except:
            testResult = False
            Result_msg += "#1 "
        
        # DirectMessageBox_Message결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2253, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2253, testPlanID, buildName, 'p', "DirectMessageBox_Message Test Passed")

    # search = Institution, Center, Reporter
    def NewDirectMessage_Search_fun(search, search_target):
        print("ITR-112: Direct Message > Direct Message Box > Institution - Search")
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
        
        Common.ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # NewDirectMessage
        driver.find_element(By.CSS_SELECTOR, "#direct-message-add-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add_direct_message")))

        # Search & Select & Selected select #1 2 3
        driver.find_element(By.CSS_SELECTOR, "#message-add-tab > div:nth-child(2) > div > div.col-lg-5 > div:nth-child(1) > ul > li:nth-child(1) > a").click()
        temp = DirectMessage.NewDirectMessage_Search_fun("Institution", Var.search_institution)
        if temp != "":
            testResult = False
            Result_msg += temp

        # NewDirectMessage_Institution_Search결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2256, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2256, testPlanID, buildName, 'p', "NewDirectMessage_Institution_Search Test Passed")

    def NewDirectMessage_Institution_Message():
        print("ITR-113: Direct Message > Direct Message Box > Institution - Message")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # NewDirectMessage
        driver.find_element(By.CSS_SELECTOR, "#direct-message-add-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add_direct_message")))

        # Send, no input send, Cancel #1, 2, 3
        # search, search_target, num, msg
        temp = DirectMessage.NewDirectMessage_Message_fun("Institution", Var.search_institution, 1)
        if temp != "":
            testResult = False
            Result_msg += temp

        # NewDirectMessage_Institution_Message결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2261, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2261, testPlanID, buildName, 'p', "NewDirectMessage_Institution_Message Test Passed")

    def NewDirectMessage_Center_Search():
        print("ITR-114: Direct Message > Direct Message Box > Center - Search")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # NewDirectMessage
        driver.find_element(By.CSS_SELECTOR, "#direct-message-add-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add_direct_message")))

        # Search & Select & Selected select #1 2 3
        driver.find_element(By.CSS_SELECTOR, "#message-add-tab > div:nth-child(2) > div > div.col-lg-5 > div:nth-child(1) > ul > li:nth-child(2) > a").click()
        temp = DirectMessage.NewDirectMessage_Search_fun("Center", Var.search_center)
        if temp != "":
            testResult = False
            Result_msg += temp

        # NewDirectMessage_Center_Search결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2266, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2266, testPlanID, buildName, 'p', "NewDirectMessage_Center_Search Test Passed")

    def NewDirectMessage_Center_Message():
        print("ITR-115: Direct Message > Direct Message Box > Center - Message")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # NewDirectMessage
        driver.find_element(By.CSS_SELECTOR, "#direct-message-add-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add_direct_message")))

        # Send, no input send, Cancel #1, 2, 3
        # search, search_target, num, msg
        temp = DirectMessage.NewDirectMessage_Message_fun("Center", Var.search_center, 2)
        if temp != "":
            testResult = False
            Result_msg += temp

        # NewDirectMessage_Center_Message결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2271, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2271, testPlanID, buildName, 'p', "NewDirectMessage_Center_Message Test Passed")


    def NewDirectMessage_Reporter_Search():
        print("ITR-116: Direct Message > Direct Message Box > Reporter - Search")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # NewDirectMessage
        driver.find_element(By.CSS_SELECTOR, "#direct-message-add-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add_direct_message")))

        # Search & Select & Selected select #1 2 3
        driver.find_element(By.CSS_SELECTOR, "#message-add-tab > div:nth-child(2) > div > div.col-lg-5 > div:nth-child(1) > ul > li:nth-child(3) > a").click()
        temp = DirectMessage.NewDirectMessage_Search_fun("Reporter", Var.search_reporter)
        if temp != "":
            testResult = False
            Result_msg += temp

        # NewDirectMessage_Reporter_Search결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2276, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2276, testPlanID, buildName, 'p', "NewDirectMessage_Reporter_Search Test Passed")

    def NewDirectMessage_Reporter_Message():
        print("ITR-117: Direct Message > Direct Message Box > Reporter - Message")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # DirectMessageBox
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # NewDirectMessage
        driver.find_element(By.CSS_SELECTOR, "#direct-message-add-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add_direct_message")))

        # Send, no input send, Cancel #1, 2, 3
        # search, search_target, num, msg
        temp = DirectMessage.NewDirectMessage_Message_fun("Reporter", Var.search_reporter, 3)
        if temp != "":
            testResult = False
            Result_msg += temp

        # NewDirectMessage_Reporter_Message결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
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
                if search_target.lower() not in driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div["+str(list_position)+"]/div[3]/div/div/table/tbody/tr["+str(b)+"]/td["+str(a+1)+"]").text.lower():
                    if auth == "unAuth":
                        Result_msg += "#"+str(a)+" "
                    else:
                        Result_msg += "#"+str(a+2)+" "
                    break
        
        return Result_msg

    def DirectMessageSetting_Search():
        print("ITR-118: Direct Message > Direct Message Setting > Search")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # DirectMessage
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # Direct Message Setting
        driver.find_element(By.CSS_SELECTOR, "#direct-message-setting-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search_unAuth_reporter > i")))

        # unAuth / auth Search #1 2 3 4
        temp = DirectMessage.DirectMessageSetting_Search_fun("unAuth", Var.unauth_search_id)
        temp += DirectMessage.DirectMessageSetting_Search_fun("unAuth", Var.unauth_search_username)
        temp += DirectMessage.DirectMessageSetting_Search_fun("auth", Var.search_id)
        temp += DirectMessage.DirectMessageSetting_Search_fun("auth", Var.search_username)

        if temp != "":
            testResult = False
            Result_msg += temp

        # DirectMessageSetting_Search결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2287, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2287, testPlanID, buildName, 'p', "DirectMessageSetting_Search Test Passed")

    def DirectMessageSetting_Authorize():
        print("ITR-119: Direct Message > Direct Message Setting > Authorize")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

        # DirectMessage
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.implicitly_wait(5)

        # Direct Message Setting
        driver.find_element(By.CSS_SELECTOR, "#direct-message-setting-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search_unAuth_reporter > i")))

        # Auth Search
        del driver.requests
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#auth_reporter_search_value").send_keys(Var.search_id)
        driver.find_element(By.CSS_SELECTOR, "#search_auth_reporter").click()
        driver.wait_for_request('.*/GetDirectMessage.*')
        time.sleep(0.5)

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
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#unAuth_reporter_search_value").send_keys(Var.search_id)
        driver.find_element(By.CSS_SELECTOR, "#search_unAuth_reporter").click()
        driver.wait_for_request('.*/GetDirectMessage.*')
        time.sleep(0.5)

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
            test_id = Var.add_test_id+str(random.randrange(0,100000))
            driver.find_element(By.CSS_SELECTOR, "#user-add-id").clear()
            driver.find_element(By.CSS_SELECTOR, "#user-add-id").send_keys(test_id)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-add-validation-btn")))
            driver.find_element(By.CSS_SELECTOR, "#user-add-validation-btn").click()
            #driver.execute_script("arguments[0].click()",element)
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            check = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            if check != "User ID is Exist!":
                break
        driver.find_element(By.CSS_SELECTOR, "#user-add-pw").send_keys(Var.add_test_pw)
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
        driver.find_element(By.CSS_SELECTOR, "#user_add_center_chosen > div > div > input[type=text]").send_keys(Var.search_center)
        driver.find_element(By.CSS_SELECTOR, "#user_add_center_chosen > div > div > input[type=text]").send_keys(Keys.ENTER)
        
        # Save
        driver.find_element(By.CSS_SELECTOR, "#user-add-save-btn").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"), "OK"))
        driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()

        # DirectMessage
        del driver.requests
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#tab-direct-message > a").click()
        driver.wait_for_request(".*/GetUnread.*")
        time.sleep(0.5)

        # Direct Message Setting
        driver.find_element(By.CSS_SELECTOR, "#direct-message-setting-btn").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search_unAuth_reporter > i")))

        # Search
        del driver.requests
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#unAuth_reporter_search_value").send_keys(test_id)
        driver.find_element(By.CSS_SELECTOR, "#search_unAuth_reporter").click()
        driver.wait_for_request('.*/GetDirectMessage.*')
        time.sleep(0.5)

        # Check
        if driver.find_element(By.CSS_SELECTOR, "#center_unauthorized_reporter_list > tbody > tr:nth-child(1) > td:nth-child(2)").text != test_id:
            testResult = False
            Result_msg += "#4 "

        # DirectMessageSetting_Authorize결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2293, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2293, testPlanID, buildName, 'p', "DirectMessageSetting_Authorize Test Passed")

    def DirectMessageSetting_Selection():
        print("ITR-120: Direct Message > Direct Message Setting > Selection")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

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

        # DirectMessageSetting_Selection결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2299, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2299, testPlanID, buildName, 'p', "DirectMessageSetting_Selection Test Passed")
