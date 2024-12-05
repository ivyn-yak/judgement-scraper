from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils import *

FOLDER_PREFIX = "/Volumes/Untitled"

def download_articles(type, folder_name):
    articles = type.find_elements(By.CSS_SELECTOR, "div.edn__articleListWrapper article h4 a")
    for a in articles:
        href = a.get_attribute('href')  
        article_text = a.text

        pdf = sanitize_filename(article_text) 
        file_path = os.path.join(FOLDER_PREFIX, folder_name, pdf)

        if not os.path.exists(file_path):
            download_file(href, file_path)

driver = webdriver.Chrome()

driver.get("https://www.singaporelawwatch.sg/Judgments")

title = driver.title
driver.implicitly_wait(10)  

def main(id, folder_name):
    judgements = driver.find_element(By.ID, "dnn_leftPane8")
    judgement_type = judgements.find_element(By.CSS_SELECTOR, f"div.DnnModule.DnnModule-EasyDNNnewsWidgets.DnnModule-{id}")
    download_articles(judgement_type, folder_name)

    while True:
        try:
            pagination = WebDriverWait(judgement_type, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.article_pager a.next")))
            pagination_href = pagination.get_attribute('href')
            print(f"\nNext page href: {pagination_href}")

            pagination.click() 

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dnn_leftPane8")))
            judgements = driver.find_element(By.ID, "dnn_leftPane8")
            judgement_type = judgements.find_element(By.CSS_SELECTOR, f"div.DnnModule.DnnModule-EasyDNNnewsWidgets.DnnModule-{id}")
            download_articles(judgement_type, folder_name)

        except TimeoutException:
            print(f"\nNo more pages available for id {id}. Files downloaded in {folder_name}.\n")
            break

        except NoSuchElementException:
            print(f"\nPagination element not found for id {id}. It may indicate the end of available pages.\n")
            break

        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            break 

ids = ["452", "451", "450", "449"]
for id in ids:
    judgements = driver.find_element(By.ID, "dnn_leftPane8")
    judgement_type = judgements.find_element(By.CSS_SELECTOR, f"div.DnnModule.DnnModule-EasyDNNnewsWidgets.DnnModule-{id}")
    h2 = judgement_type.find_element(By.CSS_SELECTOR, "h2")
    folder_name = f"{FOLDER_PREFIX}/Judgements/{h2.text}"
    create_directory(folder_name)

    print(f"\n---- Downloading files with id:{id} into {folder_name} ----")
    main(id, folder_name)

driver.quit()