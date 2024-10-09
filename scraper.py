import os
from dotenv import load_dotenv
from selenium.webdriver import Remote, ChromeOptions as Options
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection as Connection
from bs4 import BeautifulSoup

load_dotenv()
AUTH = os.getenv('AUTH')
SBR_WEBDRIVER = f'https://{AUTH}'

def scrape_website(website):

    if AUTH == 'USER:PASS':
        raise Exception('Provide Scraping Browsers credentials in AUTH ' +
                        'environment variable or update the script.')
    

    print('Connecting to Browser...')
    server_addr = f'https://{AUTH}@brd.superproxy.io:9515'
    connection = Connection(server_addr, 'goog', 'chrome')
    driver = Remote(connection, options=Options())
    try:
        print(f'Connected! Navigating to {website}...')
        driver.get(website)
        
        print('Navigated! Waiting captcha to detect and solve...')
        result = driver.execute('executeCdpCommand', {
            'cmd': 'Captcha.waitForSolve',
            'params': {'detectTimeout': 10 * 1000},
        })
        status = result['value']['status']
        print(f'Captcha status: {status}')

        html = driver.page_source
        return html
    finally:
        driver.quit()


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    body_content = soup.body

    if body_content:
        return str(body_content)
    return ""

def clean_extracted_body(body_content):
    #clean by removing scripts and styles
    soup = BeautifulSoup(body_content, "html.parser")

    for scripts_styles in soup(['script', 'style']):
        scripts_styles.extract()

    cleaned_content = soup.get_text(separator='\n')
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content

def chunk_dom_content(dom_content, max_length = 6000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length) 
    ]