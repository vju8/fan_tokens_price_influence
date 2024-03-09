from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager            
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver                                   
from unidecode import unidecode
import pandas as pd
import os.path
import time
import csv




def adjust_money_value(fee):
    multiplicator_map = {"k" : 1000,
                         "m" : 1000000}
    if fee != "":
        multiplicator = fee[-1]
        return int(float(fee.split(multiplicator)[0]) * multiplicator_map[multiplicator])
    else:
        return ""


def results_to_csv(season, player_name, age, market_value, team_left, team_joined, transfer_fee):
    headers = ["season", "player_name", "age", "market_value[EUR]", "team_left", "team_joined", "transfer_fee[EUR]"]
    data = [season, unidecode(player_name), age, adjust_money_value(market_value), unidecode(team_left), unidecode(team_joined), adjust_money_value(transfer_fee)]
    
    filename = r"Datasets for Merging/transfer_data_dataset.csv"
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', encoding='UTF8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter = ';', lineterminator = '\n')
        if not file_exists:
            writer.writerow(headers)     # file doesn't exist yet, write a header
        writer.writerow(data)


def driver_init():
    options = Options()
    options.add_experimental_option("detach", True) 
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install(), options = options))
    initial_link = "https://www.transfermarkt.com/transfers/transferrekorde/statistik?saison_id=&land_id=0&ausrichtung=&spielerposition_id=&altersklasse=&leihe=&w_s=&plus=1"
    driver.get(initial_link)   
    driver.maximize_window()
    return driver


def transfer_scrapper(driver):
    # accept cookies if given
    try:
        iframe = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//iframe[@id = 'sp_message_iframe_764226']")))
        driver.switch_to.frame(iframe)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='ACCEPT ALL']"))).click()
    except TimeoutException:
        pass  
    
    driver.switch_to.default_content()
    
    # Choose seasons
    seasons_of_interest = ["18/19", "19/20", "20/21", "21/22", "22/23"]        
    for season in seasons_of_interest: 
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[@href = 'javascript:void(0)'][1]"))).click()
        season_input = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@type = 'search']")))
        season_input.send_keys(season)
        season_input.send_keys(Keys.RETURN)
        
        # click "display selection"
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@class = 'right button small']"))).click()
    
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        for page in range(1, 11): 
            
            if page == 1: 
                time.sleep(3)    
            else:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//ul[@class = 'tm-pagination']/li[@class = 'tm-pagination__list-item tm-pagination__list-item--active']/following-sibling::li[@class = 'tm-pagination__list-item'][1]"))).click()
                time.sleep(5)
                        
            players_name_on_page = [x.text for x in driver.find_elements(By.XPATH, "//table[@class = 'items']//tr[@class = 'odd' or @class = 'even']/td[2]//a")]    
            player_age_on_page = [x.text for x in driver.find_elements(By.XPATH, "//table[@class = 'items']//tr[@class = 'odd' or @class = 'even']/td[3]")]
            player_market_value_on_page = [x.text[1:] for x in driver.find_elements(By.XPATH, "//table[@class = 'items']//tr[@class = 'odd' or @class = 'even']/td[4]")]
            players_left_on_page = [x.text for x in driver.find_elements(By.XPATH, "//table[@class = 'items']//tr[@class = 'odd' or @class = 'even']/td[7]//td[2]/a")] 
            players_joined_on_page = [x.text for x in driver.find_elements(By.XPATH, "//table[@class = 'items']//tr[@class = 'odd' or @class = 'even']/td[8]//td[2]/a")] 
            
            players_transfer_fee_on_page = []
            transfer_fees_xpath = "//table[@class = 'items']//tr[@class = 'odd' or @class = 'even']/td[9]/a"
            for x in driver.find_elements(By.XPATH, transfer_fees_xpath):
                
                if x.text[:9] == "Loan fee:":
                    idx = driver.find_elements(By.XPATH, transfer_fees_xpath).index(x) + 1 
                    loan_fee = driver.find_element(By.XPATH, f"//table[@class = 'items']//tr[@class = 'odd' or @class = 'even'][{idx}]/td[9]/a/i").text[1:]
                    players_transfer_fee_on_page.append(loan_fee)  
                else:
                    players_transfer_fee_on_page.append(x.text[1:])
            
            for row in range(len(players_name_on_page)):
                results_to_csv(season, players_name_on_page[row], player_age_on_page[row], player_market_value_on_page[row], players_left_on_page[row], players_joined_on_page[row], players_transfer_fee_on_page[row])
             
        driver.execute_script("window.scrollTo(0, document.body.scrollTop);")
        time.sleep(2)
    
    driver.quit() 


if __name__ == "__main__": 
    driver = driver_init()
    transfer_scrapper(driver)

    