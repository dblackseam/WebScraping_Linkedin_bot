import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import time

############################ DRIVER INSTALLATION #####################################
options = webdriver.ChromeOptions()
options.add_argument(f"--proxy-server={os.environ['PROXY_SERVER']}")
options.add_argument("--start-maximized")

s = Service("C:/Users/danil/Desktop/Coding/Chrome Driver/chromedriver.exe")
driver = webdriver.Chrome(service=s, options=options)

driver.get("https://www.linkedin.com/jobs/search/?f_AL=true&f_E=2&f_WT=2&geo"
           "Id=103644278&keywords=python%20developer&location=United%20States"
           "&sortBy=R")

############################ AUTHORIZATION #####################################
enter_button = driver.find_element(By.CLASS_NAME, "nav__button-secondary")
enter_button.click()

time.sleep(15)

email_bar = driver.find_element(By.NAME, "session_key")
email_bar.send_keys(os.environ["LINKEDIN_EMAIL"])

time.sleep(15)

password_bar = driver.find_element(By.NAME, "session_password")
password_bar.send_keys(os.environ["LINKEDIN_PASSWORD"])
authorization_enter_btn = driver.find_element(By.CLASS_NAME, "btn__primary--large")

time.sleep(5)

authorization_enter_btn.click()

############################ SAVE AND FOLLOW AUTOMATION #####################################
CURRENT_RESULTS_PAGE = 1


def bot():
    global CURRENT_RESULTS_PAGE
    time.sleep(3)
    for number in range(25):
        left_rail_job = driver.find_element(By.CLASS_NAME, f"jobs-search-two-pane__job-card-"
                                                           f"container--viewport-tracking-{number}")
        left_rail_job.click()

        time.sleep(2)

        save_button = driver.find_element(By.CLASS_NAME, "jobs-save-button")
        save_button_text = driver.find_element(By.CSS_SELECTOR, ".jobs-save-button span")
        if save_button_text.text == "Saved":
            pass
        else:
            save_button.click()

        time.sleep(1)

        driver.execute_script(f'document.querySelector(".jobs-search__job-details--container")'
                              f'.scrollTo(0, document.querySelector(".jobs-search__job-details'
                              f'--container").scrollHeight)')

        time.sleep(1)

        try:
            follow_company_btn = driver.find_element(By.CLASS_NAME, "follow")
        except selenium.common.exceptions.NoSuchElementException:
            pass
        else:
            follow_button_text = driver.find_element(By.CSS_SELECTOR, ".follow span")
            if follow_button_text.text == "Following":
                pass
            else:
                follow_company_btn.click()
                time.sleep(2)

        if number == 24:
            CURRENT_RESULTS_PAGE += 1
            driver.execute_script(f'document.querySelector(".jobs-search-results")'
                                  f'.scrollTo(0, document.querySelector(".jobs-search-'
                                  f'results").scrollHeight)')
            result_pages_buttons = driver.find_elements(By.CSS_SELECTOR, ".artdeco-pagination__pages li button")
            result_pages_buttons[CURRENT_RESULTS_PAGE].click()
            bot()


bot()
