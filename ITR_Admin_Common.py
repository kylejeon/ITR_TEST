from selenium import webdriver

driver = webdriver.Chrome()

def close_popup():
    popup = driver.window_handles
    while len(popup) != 1:
        driver.switch_to.window(popup[1])
        driver.close()
        popup = driver.window_handles
    driver.switch_to.window(popup[0])