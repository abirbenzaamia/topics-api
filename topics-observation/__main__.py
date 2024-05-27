from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
from selenium.webdriver.common.keys import Keys
import requests
import pandas as pd
import ast

def accept_cookies(driver):
    # first check if cookies exists 
    
    try:
        cookie_selectors = [
                "//button | a [contains(.,'Allow all')]",      
                "//button | a [contains(.,'Accept all')]",
                "//button | a [contains(.,'Accept All')]",
                "//button | a [contains(.,'Accept all cookies')]",
                "//button | a [contains(.,'Accept')]",   
                "//button | a [contains(.,'Accepter & Fermer')]",   
                "//button | a [contains(.,'Allow')]]",
                "//button | a [contains(.,'consent')]]", 
                "//button | a [contains(.,'Agree')]]", 
                "//button | a [contains(.,'agree')]]",
                "//button | a [contains(.,'Ok')]]",
                "//button | a [contains(.,'OK')]]",
                "//button | a [contains(.,'Go')]]",
                "//button | a [contains(.,'GO')]]",
                "//button | a [contains(.,'ok')]]", 
                "//button | a [contains(.,'go')]]",
                "//button | a [contains(.,'THAT'S OK')]]", 
                "//button | a [contains(.,'Enable')]]",
            ]
        accepted = False
        time.sleep(3)
        # Loop through selectors to find and click the accept cookies button
        for selector in cookie_selectors:
                try:
                    
                    accept_button = driver.find_element(By.XPATH, selector)
                    accept_button.click()
                    accepted = True
                    print('Cookies accepted')
                    break
                except:
                    continue

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        return accepted
 
    
def chrome_configure_experimental_flags(driver):
    driver.get('chrome://flags')  
    enable_ps_api_command = "chrome.send('enableExperimentalFeature',['privacy-sandbox-ads-apis', 'true'])"   
    enable_ps_internal_command = "chrome.send('enableExperimentalFeature',['privacy-sandbox-internals', 'true'])"   
    enable_ps_notice_command = "chrome.send('enableExperimentalFeature',['privacy-sandbox-ads-notice-ui', 'true'])"
    enable_ff_command = "chrome.send('enableExperimentalFeature',['enable-fenced-frames', 'true'])"
    
    driver.execute_script(enable_ps_api_command)    
    driver.execute_script(enable_ps_internal_command)  
    driver.execute_script(enable_ps_notice_command) 
    driver.execute_script(enable_ff_command)   
    driver.get('chrome://flags')                      #Re-load so that we can check
    time.sleep(2)

def open_chrome():
    myOptions = Options()
    #Set disk and media cache size to disable caching
    myOptions.add_argument("--disk-cache-size=1")
    myOptions.add_argument("--media-cache-size=1")

    #Set our own, to be re-used, profile
    profile_folder = '/tmp/' + 'profile_chrome_' + '4'
    myOptions.add_argument("user-data-dir=" + profile_folder)


    #Create driver
    driver = webdriver.Chrome(options=myOptions)
    #Set experimental features
    chrome_configure_experimental_flags(driver)
    #Close and re-build driver with same options (and so same profile, so experimental flags will be kept)

    driver.close()
    driver = webdriver.Chrome(options=myOptions)
    return driver


def simulate_browsing(driver, url):
    try: 
        driver.get(url)
        response = requests.get(url, timeout=5)
        #some websites cannot be reached
        if response.status_code == 404:
            print('Error 404, the website - {} - is not accessible'.format(url))
            return
        else: 
            print('Visiting the website', url)
            time.sleep(2)
            #Accept Cookies 
            acccepted = accept_cookies(driver)

            #)
            #wait for Privacy Sandbox iframe to be loaded
            time.sleep(5)
            for _ in range(random.randint(3, 5)):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 4))
            for i in range(3):
                try:
                    random_elements = driver.find_elements(By.XPATH, "//button | //a")
                    i = random.randint(0, len(random_elements))
                    driver.execute_script("arguments[0].scrollIntoView();", random_elements[i])
                    print(random_elements[i].text)
                    random_elements[i].click()
                    time.sleep(random.uniform(3, 6))
                    driver.refresh()
                    time.sleep(random.uniform(3, 6))
                    break
                except:
                    print('Can not Find an interactable element' )
                    continue
                #return
            if not acccepted:
                print('Can not accept Cookies')
                return 0
    except:
        print('The website - {} - is not accessible or blocked by GET request'.format(url))
        pass
        return


def get_topics_observed_per_adtech(driver, topics):
    ad_techs = []    
    url = 'chrome://topics-internals/'
    driver.get(url)
    time.sleep(2)
    calculate_btn = driver.find_element(By.XPATH, '//*[@id="calculate-now-button"]')
    calculate_btn.click()
    time.sleep(10)
    #This is for the same website 
    for i in range(5):
        topic_id = driver.find_element(By.XPATH, '//*[@id="epoch-div-list-wrapper"]/div[1]/table/tr[{}]/td[1]'.format(i+1)).text
        real_or_random = driver.find_element(By.XPATH, '//*[@id="epoch-div-list-wrapper"]/div[1]/table/tr[{}]/td[3]'.format(i+1)).text

        if real_or_random == "Real" and int(topic_id) in topics:
            #get Adtechs observing the website
            ads = driver.find_elements(By.XPATH, '//*[@id="epoch-div-list-wrapper"]/div[1]/table/tr[{}]/td[4]/span'.format(i+1))
            for ad in ads:
                ad_techs.append(ad.text)
            #print('The topics {} was obserby by {}'.format(topics, ad_techs))
            break
        else:
            continue
            #print('No topic was observed')
    time.sleep(2)
    return ad_techs

# ----------------------------------------- #

# main function 
df = pd.read_csv('topics-observation/data/top-20k-topics.csv')
driver = open_chrome()
ad_df = pd.DataFrame(columns=['domain', 'topics', 'ad_techs'])

for i in range(1500,2000):
    hostname = df['domain'][i]
    topics = ast.literal_eval(df['topics'][i])
    url = 'https://www.' + hostname
    if -2 in topics:
        row = {'domain': hostname, 'topics': topics, 'ad_techs': []}
        ad_df = ad_df._append(row, ignore_index=True)
        continue
    try:
        print(url)
        cookies = simulate_browsing(driver, url)
        ad_techs = get_topics_observed_per_adtech(driver, topics)
        if ad_techs == [] and cookies == 0:
            ad_techs.append("-1")
        row = {'domain': hostname, 'topics': topics, 'ad_techs': ad_techs}
        ad_df = ad_df._append(row, ignore_index=True)
    except NameError:
        print(NameError)
        continue
ad_df.to_csv('topics-observation/data/top-20k-topics-ads-4.csv')
time.sleep(2)
driver.quit()

# finish 

# ----------------------------------------- #




