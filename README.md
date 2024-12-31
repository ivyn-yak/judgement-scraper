# Extension: Automation of Biweekly Newsletter

Established a cron job using GitHub Actions to scrape the [Supreme Court Judgements](https://www.singaporelawwatch.sg/Judgments) every 14 days. The workflow also triggers an automated email, with the PDFS attached, to the recipient using SMTP.

## Run Locally

### Install Selenium Webdriver

Selenium requires a compatible [WebDriver](https://www.selenium.dev/downloads/) to interact with your chosen browser. This scraper is configured for Google Chrome.

### Project Setup

Setup virtual environment

```bash
  python3 -m venv venv
  source venv/bin/activate 
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Create `.env` file

```bash
  SENDER_EMAIL={{ SENDER_EMAIL }}
  SENDER_PASSWORD={{ SENDER_PASSWORD }}
  RECIPIENT_EMAIL={{ RECIPIENT_EMAIL }}
  PERSONAL_EMAIL={{ PERSONAL_EMAIL }}
```

Run scraper

```bash
  python3 newsletter.py
```

# Initial Project: PDF Scraper in Python and Selenium

Scraped 10,000 PDF copies of the Supreme Court Judgements from [Singapore Law Watch.](https://www.singaporelawwatch.sg/Judgments)

### Install Selenium Webdriver

Selenium requires a compatible [WebDriver](https://www.selenium.dev/downloads/) to interact with your chosen browser. This scraper is configured for Google Chrome.

### Project Setup

Setup virtual environment

```bash
  python3 -m venv venv
  source venv/bin/activate 
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Run scraper

```bash
  python3 scraper.py
```
