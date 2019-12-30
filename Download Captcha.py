from selenium import webdriver
import time
import pytesseract
url="http://www2.sums.ac.ir/portal/login.php"
for i in range(41,100):
	driver=  webdriver.Chrome("D:\programming\PROJECT\-----SOURCE-----\chromedriver.exe")
	driver.minimize_window()
	driver.get(url)
	Name=str(i)+".png"
	driver.find_element_by_xpath('//*[@id="flogin"]/div/img').screenshot(Name)
	driver.close()