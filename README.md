# PDF Scraper in Python and Selenium

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
