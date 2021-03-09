from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests

#Needed data to finalize transaction
data = {
    'google_mail': '',
    'google_pass':  '',
    'full_name': '',
    'email':    '',
    'tel':  '',
    'address': '',
    'address2': '',
    'address3': '',
    'city': '',
    'postcode': '',
    'cardnumber': '',
    'cvv': ''
}

product_name = 'Christmas Stocking'

url = 'https://www.supremenewyork.com'


driver = webdriver.Chrome('./chromedriver.exe')

#Required login using gmail to "hack" captcha
url0 = 'https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent'
driver.get(url0)

driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(data['google_mail'])
driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(data['google_pass'])
driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button').click()

#Tab change
driver.execute_script("window.open('about:blank', 'tab2');")
driver.switch_to.window("tab2")


page = requests.get('https://www.supremenewyork.com/shop/all/accessories')
source = page.content

soup = BeautifulSoup(source, features="lxml")
links = soup.find_all('a', {'class': 'name-link'}, text=product_name)
list_links = []

for link in links:
    list_links.append(str(link.attrs['href']))

prod = (url + str(list_links[0]))

driver.get(prod)


#Time counting method
def timeme(method):
    def wrapper(*args, **kw):
        starttime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endtime = int(round(time.time() * 1000))
        print((endtime - starttime)/1000, 's')
        return result
    return wrapper


@timeme
def order():

    #Product choose
    driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="cart"]/a[2]').click()

    #Entering the data
    driver.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(data['full_name'])
    driver.find_element_by_xpath('//*[@id="order_email"]').send_keys(data['email'])
    driver.find_element_by_xpath('//*[@id="order_tel"]').send_keys(data['tel'])
    driver.find_element_by_xpath('//*[@id="bo"]').send_keys(data['address'])
    driver.find_element_by_xpath('//*[@id="oba3"]').send_keys(data['address2'])
    driver.find_element_by_xpath('//*[@id="order_billing_address_3"]').send_keys(data['address3'])
    driver.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(data['city'])
    driver.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(data['postcode'])
    driver.find_element_by_xpath('//*[@id="order_billing_country"]/option[28]').click()
    driver.find_element_by_xpath('//*[@id="cnb"]').send_keys(data['cardnumber'])
    driver.find_element_by_xpath('//*[@id="credit_card_month"]/option[1]').click()
    driver.find_element_by_xpath('//*[@id="credit_card_year"]/option[2]').click()
    driver.find_element_by_xpath('//*[@id="vval"]').send_keys(data['cvv'])
    driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p/label').click()
    #Finalization of the payment
    driver.find_element_by_xpath('//*[@id="pay"]/input').click()


order()
