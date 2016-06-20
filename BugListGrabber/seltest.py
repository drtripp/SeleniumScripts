import time
from selenium import webdriver

#website = "https://bugzilla.mozilla.org/buglist.cgi?resolution=---&query_format=advanced&component=Security&product=Firefox"

driver = webdriver.Chrome()
driver.get("http://www.yahoo.com/")
time.sleep(5)



driver.quit()