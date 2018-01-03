import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
# available since 2.26.0
from selenium.webdriver.support import expected_conditions as EC

# Create a new instance of the Firefox driver
driver = webdriver.Edge(
    executable_path='C:\Local\selenium\MicrosoftWebDriver.exe')
# go to the google home page
driver.get("file:///" + os.getcwd() + "/index.html")

# the page is ajaxy so the title is originally this:
print(driver.title)

# find the element that's name attribute is q (the google search box)
source = driver.find_element_by_id("forward")
target = driver.find_element_by_id("main")
print(source.get_attribute('draggable'))
#drag_and_drop(source, target).perform()
try:
    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
    #WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))

    # WebDriverWait(driver, 10)
    ActionChains(driver).click_and_hold(source)\
        .move_to_element_with_offset(target, 10, 20)\
        .release()\
        .perform()
   # You should see "cheese! - Google Search"
    print(driver.title)

finally:
    driver.quit()
