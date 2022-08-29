from testlink import TestlinkAPIClient, TestLinkHelper
from bs4 import BeautifulSoup
import time
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# User: kyle
URL = 'http://testserver-win:81/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
DevKey = 'adcb86843d0c77e6e0c9950f80a143c0'
# testlink 초기화
tl_helper = TestLinkHelper()
testlink = tl_helper.connect(TestlinkAPIClient) 
testlink.__init__(URL, DevKey)
testlink.checkDevKey()

# 브라우저 설정
baseUrl = 'http://stagingadmin.onpacs.com'
#url = baseUrl + quote_plus(plusUrl)
driver = webdriver.Chrome()
driver.get(baseUrl)
html = driver.page_source
soup = BeautifulSoup(html)
result_list = []

# TestPlanID = AutoTest 버전 테스트
testPlanID = 2996
buildName = 1

# Common var
# testResult = ''

class signInOut:
    def admin_sign_in(id, password):
        driver.find_element(By.ID, 'user-id').clear()
        driver.find_element(By.ID, 'user-id').send_keys(id)
        driver.find_element(By.ID, 'user-password').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        driver.implicitly_wait(5)
    def admin_sign_out():
        driver.find_element(By.CSS_SELECTOR, '.pull-right > span').click()

class windowSize:
    driver.set_window_size(1920, 1080)

class sign:
    def sign_InOut():
        testResult = ''        
        # user ID와 password를 입력하지 않고 sign in을 클릭한다
        signInOut.admin_sign_in('','')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        # This field is required.
        try:
            assert driver.find_element(By.ID, "user-id-error").text == "This field is required."
        except:
            testResult = 'failed'    
        # 잘못된 user ID를 입력하고 sign in을 클릭한다
        signInOut.admin_sign_in('administrator','Server123!@#')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        # User not found
        try:
            assert driver.find_element(By.CSS_SELECTOR, ".validation-summary-errors > ul > li").text == "User not found"
        except:
            print('2')
            testResult = 'failed'        
        # password 미입력 하고 sign in을 클릭한다        
        signInOut.admin_sign_in('administrator',' ')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        # This field is required.
        try:
           assert driver.find_element(By.ID, "user-password-error").text == "This field is required."
        except:
            testResult = 'failed' 
        # admin 유저가 아닌 계정으로 로그인 한다.        
        signInOut.admin_sign_in('yhjeon','1')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()
        # not admin user
        try:
            assert driver.find_element(By.CSS_SELECTOR, ".validation-summary-errors >  ul > li").text == "Not admin user"
        except:
            testResult = 'failed' 
        # 정상적인 계정으로 로그인 한다.
        signInOut.admin_sign_in('INF_JH','Server123!@#')
        driver.find_element(By.CSS_SELECTOR, '.btn').click()        
        try:
            assert driver.find_element(By.CSS_SELECTOR, ".pull-right > span").text == "Sign Out"
        except:
            testResult = 'failed'
        if testResult == 'failed':
            testlink.reportTCResult(1531, testPlanID, buildName, 'f', "Sign In/Out Test Failed")            
        else:
            testlink.reportTCResult(1531, testPlanID, buildName, 'p', "Sign In/Out Test Passed")
    
    def rememeberMe():


sign.sign_InOut()

