from selenium import webdriver
from selenium.webdriver.common.by import By
import smtplib
import email.message
import os
import ssl
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless=new')
browser = webdriver.Chrome(options=options)

abtc_application_number = os.environ['abtc_application_number']
gmail_id = os.environ['gmail_id']
to_email_ids = os.environ['to_email_ids']
gmail_password = os.environ['gmail_password']

# 1. Get ABTC status
browser.get('https://www.abtc-aps.org/abtc-core/status/check.html')
apec_economy = browser.find_element(value="economyIcao")
application_number = browser.find_element(value="applicationNumber")
search_button = browser.find_element(value="id_search")

apec_economy.send_keys("HKG")
application_number.send_keys(abtc_application_number)
search_button.click()
output_box = browser.find_element(by=By.CLASS_NAME, value="outputBox")
current_countries = output_box.text.split(sep="\n")

old_precleared_countries = open('precleared_countries.txt', 'r').read().split("\n")
countries_diff = list(set(current_countries) - set(old_precleared_countries))

if countries_diff:
    message = f"!!! New APEC countries precleared: {countries_diff} !!!"

    with open('precleared_countries.txt', 'w') as f:
        f.write('\n'.join(current_countries))
else:
    message = "No new APEC countries precleared :("


# 2. Get random frog img 
browser.get("http://allaboutfrogs.org/funstuff/randomfrog.html")
frog_url = browser.find_element(by=By.TAG_NAME, value="img").get_attribute("src")


# 3. Send email

msg = email.message.Message()
msg['Subject'] = f'APEC update - {message}'
msg.add_header('Content-Type','text/html')
msg.set_payload(f"""
                <p>{message}</p>
                
                <p style="padding-top:20px;padding-bottom:2px">Also, here's a frog pic for ya:</p>
                <img src={frog_url} />
                
                """)

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(gmail_id, gmail_password)
s.sendmail(gmail_id, to_email_ids.split(","), msg.as_string())
s.quit()
