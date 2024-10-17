from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://www.singaporelawwatch.sg/Judgments")

title = driver.title

driver.implicitly_wait(10)  

judgement_types = driver.find_elements(By.CSS_SELECTOR, "div.news.NewsMagazine_Style_custom_st5dovjofqg.eds_style_custom_st5dovjofqg.eds_subCollection_latestArticles.eds_subCollection_news.eds_news_NewsMagazine.eds_template_List_Article_Simple-SLW_Judgments")
for type in judgement_types:
    articles = type.find_elements(By.CSS_SELECTOR, "div.edn__articleListWrapper article h4 a")
    for a in articles:
        href = a.get_attribute('href')  
        article_text = a.text
        print(">>>>>>", a.text, "Link: ", href)
driver.quit()