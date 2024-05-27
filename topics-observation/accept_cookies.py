import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import random,time,os,sys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def chrome_configure_experimental_flags(myDriver):
    myDriver.get('chrome://flags')  
    enable_ps_api_command = "chrome.send('enableExperimentalFeature',['privacy-sandbox-ads-apis', 'true'])"   
    enable_ps_internal_command = "chrome.send('enableExperimentalFeature',['privacy-sandbox-internals', 'true'])"   
    enable_ps_internal_command = "chrome.send('enableExperimentalFeature',['privacy-sandbox-ads-notice-ui', 'true'])"
    enable_ps_internal_command = "chrome.send('enableExperimentalFeature',['enable-fenced-frames', 'true'])"
    
    myDriver.execute_script(enable_ps_api_command)        
    myDriver.get('chrome://flags')                      #Re-load so that we can check
    time.sleep(2) 


# chrome_local_state_prefs = {
#     "browser": {
#         "enabled_labs_experiments": [
#             "privacy-sandbox-ads-apis",
#             "privacy-sandbox-ads-notice-ui",
#             "privacy-sandbox-internals",
#             "enable-fenced-frames"
#         ],
#     }
# }

#chrome_options.add_experimental_option("flags", chrome_local_state_prefs)
#chrome_options.add_argument("--disable-popup-blocking")

#chrome_options.add_argument("--profile-directory=Default")

#chrome_options.add_argument("--ignore-certificate-errors")

#chrome_options.add_argument("--disable-plugins-discovery")

#chrome_options.add_argument("--incognito")

#chrome_options.add_argument("user_agent=DN")
#chrome_options = webdriver.ChromeOptions()

# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--disk-cache-size=1")
# chrome_options.add_argument("--media-cache-size=1")

# #Set our own, to be re-used, profile
# profile_folder = '/tmp/' + 'profile_chrome_' + time_string
# chrome_options.add_argument("user-data-dir=" + profile_folder)

# driver = webdriver.Chrome(options=chrome_options)
# #Set experimental features
# chrome_configure_experimental_flags(driver)
# time.sleep(10)
# #Set experimental features
# relunch_btn = driver.find_element(By.XPATH, '//*[@id="experiment-restart-button"]')
# relunch_btn.click()
# driver = webdriver.Chrome(options=chrome_options)
myOptions = Options()

driver = webdriver.Chrome(options=myOptions)
#
# #Close and re-build driver with same options (and so same profile, so experimental flags will be kept)
#driver.close()

#chrome_options = webdriver.ChromeOptions()

#chrome_options.add_argument("--disable-extensions")
#driver = uc.Chrome(chrome_options)
#driver.delete_all_cookies()

#driver.get("https://www.google.com/accounts/Login")


try:
    # driver.find_element(By.ID,"identifierId").send_keys(GMAIL)
    # time.sleep(2)
    # driver.find_element(By.XPATH,"//button[.//span[text()='Next']]").click()
    # time.sleep(2)
    # driver.find_element(By.NAME,"Passwd").send_keys(PASSWORD)
    # time.sleep(2)
    # driver.find_element(By.XPATH,"//button[.//span[text()='Next']]").click()
    # time.sleep(2)
    # #accept_btn = driver.find_element(By.XPATH , '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[2]/div/div/button/div[3]')
    # #accept_btn.click()
    # time.sleep(20)
    print('Login Successful...!!')
    url = "https://www.t-mobile.com/"
    driver.get(url)
    print(driver.get_cookies())


    time.sleep(60)

    
    #calculate_btn.click()

except NameError:
    print(NameError)
    print('Login Failed')

time.sleep(10)