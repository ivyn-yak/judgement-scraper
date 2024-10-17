from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import *

driver = webdriver.Chrome()

driver.get("https://www.singaporelawwatch.sg/Judgments")

title = driver.title
driver.implicitly_wait(10)  

judgements = driver.find_element(By.ID, "dnn_leftPane8")
judgement_types = judgements.find_elements(By.CSS_SELECTOR, "div.eds_containers_NewsMagazine.eds_templateGroup_default.eds_template_Default.eds_style_custom_sw3m9ntp2vf")
for type in judgement_types:
    h2 = type.find_element(By.CSS_SELECTOR, "h2")
    folder_name = "Judgements/" + h2.text
    create_directory(folder_name)

    articles = type.find_elements(By.CSS_SELECTOR, "div.edn__articleListWrapper article h4 a")
    for a in articles:
        href = a.get_attribute('href')  
        article_text = a.text
        file_name = article_text.replace(" ", "_")
        pdf = file_name + ".pdf"

        download_file(href, folder_name, pdf)

driver.quit()