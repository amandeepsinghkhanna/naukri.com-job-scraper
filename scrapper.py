import json
import pandas as pd
from time import sleep
from datetime import datetime
from selenium import webdriver

def extract_info(xpath, webdriver, text_only = True):
    found_elements = webdriver.find_elements_by_xpath(xpath)
    text_elements = [element.text for element in found_elements]
    if text_only == True:
        return text_elements
    else:
        url_elements = [element.get_property("href") for element in found_elements]
        return text_elements, url_elements

def scrape_webpage(xpath_dict, webdriver):
    scraped_info = {}
    scraped_info["job-title"], scraped_info["url"] = extract_info(
        xpath=xpath_dict["job-title"], webdriver=webdriver, text_only = False
    )
    scraped_info["company-title"] = extract_info(
        xpath=xpath_dict["company-title"], webdriver=webdriver, text_only = True
    )
    scraped_info["experience"] = extract_info(
        xpath=xpath_dict["experience"], webdriver=webdriver, text_only = True
    )
    scraped_info["salary"] = extract_info(
        xpath=xpath_dict["salary"], webdriver=webdriver, text_only = True
    )
    scraped_info["job-description"] = extract_info(
        xpath=xpath_dict["job-description"], webdriver=webdriver, text_only = True
    )
    scraped_info_df = pd.DataFrame.from_dict(scraped_info, orient="index").transpose()
    return scraped_info_df

timestamp = datetime.now()

with open("config.json") as json_file:
    config = json.load(json_file)

driver = webdriver.Chrome(executable_path=config["web-driver-path"])
driver.get(config["scrape-url"])

scraped_jobs = scrape_webpage(xpath_dict=config["xpaths"], webdriver=driver)

while True:
    try:
        sleep(3)
        next_button = driver.find_elements_by_xpath(config["xpaths"]["next-button"])[0]
        next_button.click()
        sleep(3)
        temp_jobs = scrape_webpage(xpath_dict=config["xpaths"], webdriver=driver)
        scraped_jobs = scraped_jobs.append(temp_jobs)
    except Exception as e:
        print("no more pages")
        break;

scraped_jobs.to_csv("test.csv")