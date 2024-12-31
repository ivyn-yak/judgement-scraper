from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime, timedelta
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from io import BytesIO
from dotenv import load_dotenv
import os

from utils import *

load_dotenv()

def download_articles(type, new_files):
    current_date = datetime.now().date()

    articles = type.find_elements(By.CSS_SELECTOR, "div.edn__articleListWrapper article")
    for article in articles:
        div = article.find_element(By.CSS_SELECTOR, "div")
        div_text = div.text

        date = get_date(div_text)
        cutoff_date = current_date - timedelta(days=14)

        if cutoff_date <= date < current_date:

            a = article.find_element(By.CSS_SELECTOR, "h4 a")
            href = a.get_attribute('href')  
            article_text = a.text

            pdf = sanitize_filename(article_text) 

            new_files += [(href, pdf)]
            print(date)

        else:
            raise CustomError("No more new articles.")

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)
driver.get("https://www.singaporelawwatch.sg/Judgments")

title = driver.title
driver.implicitly_wait(10)  

def run_scraper(id, new_files):
    judgements = driver.find_element(By.ID, "dnn_leftPane8")
    judgement_type = judgements.find_element(By.CSS_SELECTOR, f"div.DnnModule.DnnModule-EasyDNNnewsWidgets.DnnModule-{id}")

    try:
        download_articles(judgement_type, new_files)

    except CustomError as e:
        print(f"\nAn error occurred: {str(e)}")

    while True:
        try:
            pagination = WebDriverWait(judgement_type, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.article_pager a.next")))
            pagination_href = pagination.get_attribute('href')
            print(f"\nNext page href: {pagination_href}")

            pagination.click() 

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dnn_leftPane8")))
            judgements = driver.find_element(By.ID, "dnn_leftPane8")
            judgement_type = judgements.find_element(By.CSS_SELECTOR, f"div.DnnModule.DnnModule-EasyDNNnewsWidgets.DnnModule-{id}")
            download_articles(judgement_type, new_files)

        except CustomError as e:
            print(f"\nAn error occurred: {str(e)}")
            break

        except TimeoutException:
            print(f"\nNo more pages available for id {id}.\n")
            break

        except NoSuchElementException:
            print(f"\nPagination element not found for id {id}. It may indicate the end of available pages.\n")
            break

        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            break 

def download_and_attach_pdfs(pdf_urls, msg):
    for pdf_info in pdf_urls:
        try:
            # Download PDF into memory
            url, filename = pdf_info
            response = requests.get(url, stream=True)
            response.raise_for_status()
            pdf_data = BytesIO(response.content)

            # Attach the PDF
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(pdf_data.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(part)
            print(f"Attached: {filename}")
        except Exception as e:
            print(f"Error downloading or attaching {filename}: {e}")

def send_email_with_multiple_pdfs(pdf_urls, sender_email, sender_password, recipient_email):
    # Create email
    subject = "Biweekly Newsletter - PDFs Attached"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['Subject'] = subject

    # Add email body
    body = "Hello,\n\nPlease find attached the PDFs for this biweekly update. Have a good day!\n"
    msg.attach(MIMEText(body, 'plain'))

    # Attach all PDFs
    download_and_attach_pdfs(pdf_urls, msg)

    # Send email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    new_files = []
    ids = ["449", "450", "451", "452"]

    for id in ids:
        judgements = driver.find_element(By.ID, "dnn_leftPane8")
        judgement_type = judgements.find_element(By.CSS_SELECTOR, f"div.DnnModule.DnnModule-EasyDNNnewsWidgets.DnnModule-{id}")
        h2 = judgement_type.find_element(By.CSS_SELECTOR, "h2")

        print(f"\n---- Downloading files with id:{id} into {h2.text} ----")
        run_scraper(id, new_files)

    driver.quit()

    send_email_with_multiple_pdfs(
        pdf_urls=new_files,
        sender_email=os.getenv('SENDER_EMAIL'),
        sender_password=os.getenv('SENDER_PASSWORD'),
        recipient_email=[os.getenv('RECIPIENT_EMAIL'), os.getenv('PERSONAL_EMAIL')]
    )

if __name__ == "__main__":
    main()

    