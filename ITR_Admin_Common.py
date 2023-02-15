import time
from testlink import TestlinkAPIClient, TestLinkHelper
# import selenium.webdriver as webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
import math
import Common_Var
from selenium.webdriver.chrome.service import Service

# TestLink User: kyle
URL = 'http://testserver-win:81/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
DevKey = 'adcb86843d0c77e6e0c9950f80a143c0'

# TestLink 초기화
tl_helper = TestLinkHelper()
testlink = tl_helper.connect(TestlinkAPIClient) 
testlink.__init__(URL, DevKey)
testlink.checkDevKey()

# TestPlanID = AutoTest 버전 테스트
testPlanID = Common_Var.planid
buildName = Common_Var.bn

driver = None

# 브라우저 설정
# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# driver = webdriver.Chrome(options=options)
# baseUrl = 'http://stagingadmin.onpacs.com'
# driver.get(baseUrl)
# name = driver.name
# baseUrl = 'http://vm-onpacs:8082'
# baseUrl = Common_Var.base_admin_url

if Common_Var.web_driver == "Edge":
    options = webdriver.EdgeOptions()
    options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    driver = webdriver.Edge(options=options)
    baseUrl = Common_Var.base_admin_url
else:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    if Common_Var.check == "Unchecked":
        options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    baseUrl = Common_Var.base_admin_url

# Notice 창 닫기
if Common_Var.web_driver != None and Common_Var.web_driver != "":
    popup = driver.window_handles
    while len(popup) != 1:
        driver.switch_to.window(popup[1])
        driver.find_element(By.ID, "notice_modal_cancel_week").click()
        popup = driver.window_handles
    driver.switch_to.window(popup[0])
else:
    print("Null")

class Var:
    # 테스트 계정
    adminID = 'testAdmin'
    adminPW = 'Server123!@#'
    stg_adminID = "INF_JH"
    stg_adminPW = "Server123!@#"
    subadminID = 'yhjeonSub'
    subadminPW = 'server123!@#'
    reporterID = 'testReporter'
    reporterPW = 'Server123!@#'
    wk_id = "testInfReporter"
    wk_pw = "Server123!@#"
    wk_id_2 = "ITRTestUsers" #DownloadControl_User_Add / DownloadControl_User_Modify / DownloadControl_Institution_Add / DownloadControl_Institution_Modify / UserManagement_Registartion_Modify
    wk_pw_2 = "1234qwer!@"#DownloadControl_User_Add / DownloadControl_User_Modify / DownloadControl_Institution_Add / DownloadControl_Institution_Modify 
    search_id = "inftest" #DirectMessageBox_Search / DirectMessageSetting_Search
    search_username = "전용혁_Tester" #DirectMessageBox_Search / DirectMessageSetting_Search

    # 공통 변수
    WorklistUrl = 'http://stagingworklist.onpacs.com'
    StagingAdmin = 'http://stagingadmin.onpacs.com/'
    today = datetime.now()
    test_hospital = "CloudTeam"
    test_hospital_code = '997'
    start = time.time()
    search_text = "test" #DirectMessageBox_Search
    search_institution = "INFINITT" #NewDirectMessage_Institution
    search_institution_2 = "Cloud" #MultiReadingCenterRule / Institution_SearchFilter / DownloadControl_Institution_Add / DownloadControl_Institution_Modify / UserManageMent_UserRegistartion_Add
    search_institution_3 = "CloudTeam" #Institution_Modify / DownloadControl_User_Add
    #search_institution_code = "997" #Institution_SearchFilter / Institution_Add
    search_center = "인피니트헬스케어" #NewDirectMessage_Center_Search / MultiReadingCenterRule / Institution_Add / UserManageMent_UserRegistartion_Add
    search_center_2 = "인피니트테스트" #MultiReadingCenterRule
    search_reporter = "inftest" #NewDirectMessage_Center_Reporter
    unauth_search_id = "TEST_MAP" #DirectMessageSetting_Search
    unauth_search_username = "김태호" #DirectMessageSetting_Search
    add_test_id = "TestA" #+난수 # DirectMessageSetting_Authorize / UserManageMent_UserRegistartion_Add / UserMangement_UserRegistartion_Delete / UserManagement_Registration_Add
    add_test_pw = "1234qwer!" #DirectMessageSetting_Authorize / UserManageMent_UserRegistartion_Add
    upload_pic = "C:\\INFINITT\\uploadimage\\uploadtest.png" # NoticeList_NoticeEditBoard
    upload_pic_url = "https://i.ytimg.com/vi/gREpAVOERis/maxresdefault.jpg" # NoticeList_NoticeEditBoards
    specialty = "ITRTest" #DownloadControl_Add / Specialty_SpecialtyList_Search
    specialty_add = "SpTest" #Specialty_SpecialtyList_Add
    vmonpacs_tns = "10.10.61.108:1521/spectra"
    staging_tns = "211.43.8.73:1521/spectra"

class Common:
    def refer_show_entries(num):
        select = Select(driver.find_element(By.CSS_SELECTOR,"#refer-assigned-list_length > label > select"))                
        select.select_by_value(str(num))
    def config_show_entries(num):
        select = Select(driver.find_element(By.CSS_SELECTOR,"#download-list_length > label > select"))
        select.select_by_value(str(num))
    def institution_show_entries(num):
        select = Select(driver.find_element(By.CSS_SELECTOR,"#institutions-list_length > label > select"))
        select.select_by_value(str(num))
    def multicenter_show_entries(num):
        select = Select(driver.find_element(By.CSS_SELECTOR,"#multi-center-rule-list_length > label > select"))
        select.select_by_value(str(num))
    def cnt_pages():
        # 현재 Job list 페이지의 job count 리턴
        temp_cnt = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]").text
        temp_cnt = temp_cnt.split()
        list_cnt = temp_cnt[5]
        pages = math.ceil(int(list_cnt) / 100)
        return pages
    def ReFresh():
        driver.find_element(By.CSS_SELECTOR, "body > nav > div > div:nth-child(1) > a.navbar-brand").click()        
        driver.implicitly_wait(5)