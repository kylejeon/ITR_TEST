from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import ITR_Admin_Login
from ITR_Admin_Common import driver
from ITR_Admin_Common import testlink
from ITR_Admin_Common import testPlanID
from ITR_Admin_Common import buildName
from ITR_Admin_Common import Common

class Notice:
    def NoticeList_NoticeEditBoard():
        print("ITR-103: Notice > Notice list > Notice Edit Board")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

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

        ITR_Admin_Login.signInOut.wk_login(wk_id, wk_pw)
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[2])
        driver.implicitly_wait(5)
        if driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/div[2]/div").text != "rnd_board3#_nopublic":
            testResult = False
            Result_msg += "#20 "
        driver.close()
        driver.switch_to.window(driver.window_handles[1])

        driver.find_element(By.CSS_SELECTOR, "#right-sidebar-logout").click()
        driver.implicitly_wait(5)

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
        ITR_Admin_Login.signInOut.admin_sign_in()
        # Notice
        driver.find_element(By.CSS_SELECTOR, "#tab-notice > a").click()
        driver.implicitly_wait(5)
        for n in range (0, 2):
            element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(7) > button")
            driver.execute_script("arguments[0].click()",element)
            WebDriverWait(driver, 0.3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.25)

        # NoticeList_NoticeEditBoard결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2188, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2188, testPlanID, buildName, 'p', "NoticeList_NoticeEditBoard Test Passed")

    def NoticeList_Edit():
        print("ITR-104: Notice > Notice list > Edit")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

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
            time.sleep(1)
            element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(2) > td:nth-child(2) > div > label > span")
            driver.execute_script("arguments[0].click()",element)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            msg = driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > h2").text
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            if (msg != "Notice 정보를 수정하였습니다." or 
                driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(2) > td:nth-child(2) > div > label > input").get_property("checked")==False):
                testResult = False
                Result_msg += "#4 "
            # 2-2 off > on
            time.sleep(1)
            element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(2) > td:nth-child(3) > div > label > span")
            driver.execute_script("arguments[0].click()",element)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
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
            time.sleep(1)
            element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(1) > td:nth-child(2) > div > label > span")
            driver.execute_script("arguments[0].click()",element)
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.15)
            # 2-1 on > off
            time.sleep(1)
            element = driver.find_element(By.CSS_SELECTOR, "#curernt_display_list > tbody > tr:nth-child(2) > td:nth-child(2) > div > label > span")
            driver.execute_script("arguments[0].click()",element)
            WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button")))
            driver.find_element(By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button").click()
            time.sleep(0.15)
            # 2-2 off > on
            time.sleep(1)
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

        # NoticeList_Edit결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2213, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2213, testPlanID, buildName, 'p', "NoticeList_Edit Test Passed")

    def NoticeList_Delete():
        print("ITR-105: Notice > Notice list > Delete")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

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

        # NoticeList_Delete결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2224, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2224, testPlanID, buildName, 'p', "NoticeList_Delete Test Passed")

    def NoticeList_NoticeDisplay():
        print("ITR-106: Notice > Notice list > Display")
        testResult = True
        Result_msg = "failed at "
        
        Common.ReFresh()

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
        time.sleep(1.5)
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

        # NoticeList_NoticeDisplay결과 전송 ##
        print("Test Result: Pass" if testResult != False else Result_msg)
        if testResult == False:
            testlink.reportTCResult(2227, testPlanID, buildName, 'f', Result_msg)            
        else:
            testlink.reportTCResult(2227, testPlanID, buildName, 'p', "NoticeList_NoticeDisplay Test Passed")