import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

root_url = 'http://www.supremenewyork.com/shop'
all_url = 'http://www.supremenewyork.com/shop/all'
root_types = []
checkout_url = "https://www.supremenewyork.com/checkout"

driver = webdriver.Chrome('C:/Users/Duffy/chromedriver.exe')

buyerName='Supreme Buyer'
buyerMail='mydickis14cmlong@nospace.com'
buyerTele='133'
buyerAdress='Area 31'
buyerCity='Nirvana'
buyerZIP='66666'
buyerCountry='USA'
buyerCardType='Mastercard'
buyerCardNumber='4117733984087674'
buyerCardExpMonth='07'
buyerCardExpYear='2021'
buyerCardCVV = '454'

def add_item(url, size=None, style=None):
    driver.get(url)
    if(size!=None):
        try:
            Select(driver.find_element_by_id('s')).select_by_visible_text(size)
        except NoSuchElementException:
            print("          "+url+": DID NOT HAVE A " + size + " IN STOCK!")
    try:
        driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').click()
    except NoSuchElementException:
        print("Error: This is sold out!")

def checkout():
    """
    This will take the session to checkout and autofill it with the information found in the header of the file
    (Ensure that this information is 100% correct before checkout)
    :return: A Captcha or Checkout items for the session
    """
    time.sleep(.2)
    try:
        driver.get(checkout_url)
        ord_billing_name = driver.find_element_by_id('order_billing_name')
        ord_billing_name.send_keys(buyerName)
        ord_email = driver.find_element_by_id('order_email')
        ord_email.send_keys(buyerMail)
        ord_tele = driver.find_element_by_id('order_tel')
        ord_tele.send_keys(buyerTele)
        ord_adress = driver.find_element_by_id('bo')
        ord_adress.send_keys(buyerAdress)
        ord_billing_city = driver.find_element_by_id('order_billing_city')
        ord_billing_city.send_keys(buyerCity)
        ord_zip = driver.find_element_by_id('order_billing_zip')
        ord_zip.send_keys(buyerZIP)
        Select(driver.find_element_by_id('order_billing_country')).select_by_visible_text(buyerCountry)
        ord_cnb = driver.find_element_by_id("nnaerb")
        ord_cnb.send_keys(buyerCardNumber)
        ord_cvv = driver.find_element_by_id("orcer")
        ord_cvv.send_keys(buyerCardCVV)
        Select(driver.find_element_by_id('credit_card_month')).select_by_visible_text(buyerCardExpMonth)
        Select(driver.find_element_by_id('credit_card_year')).select_by_visible_text(buyerCardExpYear)
        ord_terms = driver.find_element_by_id('order_terms')
        ord_terms.click()
        driver.find_element_by_tag_name("form").submit()
    except NoSuchElementException:
        print("Error: Could not Checkout!")

def view_all(inStock=False):
    in_stock = 0
    source = requests.get(all_url).text
    soup = BeautifulSoup(source, 'html.parser')
    #print(soup.prettify())
    url_list = []
    items = soup.find_all("div", class_='inner-article')
    for item in items:
        print(item)
        s = str(item).split('"')
        if("sold_out_tag" in s):
            pass
        else:
            url = "http://www.supremenewyork.com" + s[3]
            url_list.append(url)
            add_item(url)
            in_stock+=1
    """
    for x in url_list:
        if(inStock):
            source_temp = requests.get(x).text
            soup_temp = BeautifulSoup(source_temp, 'html.parser')
            avail = soup_temp.find_all("input", class_="button")
            for a in avail:
                s = str(a)
                b = s.split('"')
                if ('add to cart' in b):
                    in_stock += 1
                    print(x+" IN STOCK")
        else:
            print(x)
    """
    print(str(in_stock) + " items in stock")
    for i in url_list:
        print(i)
    checkout()

def item_run(item, size=None, max_items=None):
    item_list = []
    item_list.append(item)
    source = requests.get(root_url).text
    soup = BeautifulSoup(source, 'html.parser')
    item_num = 0
    item_url = soup.find_all("li", class_=item)
    for sh in item_url:
        s = str(sh.a)
        a=s.split('"')
        item_list.append("http://www.supremenewyork.com"+a[1])
        item_num+=1
    in_stock=0
    in_print=False
    y=0
    for x in item_list:
        if (y == 0):
            print(x + ":")
        else:
            source_temp = requests.get(x).text
            soup_temp = BeautifulSoup(source_temp, 'html.parser')
            avail = soup_temp.find_all("input", class_="button")
            for a in avail:
                s = str(a)
                b = s.split('"')
                if ('add to cart' in b):
                    in_stock += 1
                    in_print = True
            if (in_print):
                print("     " + x + " IN STOCK")
                add_item(x, size)
            else:
                print("     " + x)
            in_print = False
        y = y + 1
    print("\n")
    if(in_stock>0):
        checkout()

def main_run(item, max_items):
    """
    This method gathers all of the items on the supreme website and checks which ones are in stock
    :return: A populated c_types two dimentional array with the titles on the top
    """
    c_types = [['Skate'], ["T-shirts"], ['Shirts'], ['Sweatshirts'], ['Tops/Sweaters'], ['Jackets'], ['Accessories'],
               ['Bags'], ['Hats'], ['Pants']]
    source = requests.get(root_url).text
    soup = BeautifulSoup(source, 'html.parser')
    item_num = 0
    skate_url = soup.find_all("li", class_="skate")
    tshirt_url = soup.find_all("li", class_="t-shirts")
    shirts_url = soup.find_all("li", class_="shirts")
    sweatshirt_url = soup.find_all("li", class_="sweatshirts")
    tops_url = soup.find_all("li", class_="tops/sweaters")
    jackets_url = soup.find_all("li", class_="jackets")
    accessories_url = soup.find_all("li", class_="accessories")
    bags_url = soup.find_all("li", class_="bags")
    hats_url = soup.find_all("li", class_="hats")
    pants_url = soup.find_all("li", class_="pants")

    for sh in skate_url:
        s = str(sh.a)
        a=s.split('"')
        c_types[0].append("http://www.supremenewyork.com"+a[1])
        item_num+=1

    for sh in tshirt_url:
        s = str(sh.a)
        a=s.split('"')
        c_types[1].append("http://www.supremenewyork.com"+a[1])
        item_num+=1

    for sh in shirts_url:
        s = str(sh.a)
        a=s.split('"')
        c_types[2].append("http://www.supremenewyork.com"+a[1])
        item_num+=1

    for sh in sweatshirt_url:
        s = str(sh.a)
        a=s.split('"')
        c_types[3].append("http://www.supremenewyork.com"+a[1])
        item_num+=1

    for sh in tops_url:
        s = str(sh.a)
        a=s.split('"')
        c_types[4].append("http://www.supremenewyork.com"+a[1])
        item_num+=1

    for sh in jackets_url:
        s = str(sh.a)
        a=s.split('"')
        c_types[5].append("http://www.supremenewyork.com"+a[1])
        item_num+=1

    for sh in accessories_url:
        s = str(sh.a)
        a=s.split('"')
        c_types[6].append("http://www.supremenewyork.com"+a[1])
        item_num+=1

    for sh in bags_url:
        s = str(sh.a)
        a=s.split('"')
        c_types[7].append("http://www.supremenewyork.com"+a[1])
        item_num+=1

    for sh in hats_url:
        s = str(sh.a)
        a=s.split('"')
        c_types[8].append("http://www.supremenewyork.com"+a[1])
        item_num+=1

    for sh in pants_url:
        s = str(sh.a)
        a=s.split('"')
        c_types[9].append("http://www.supremenewyork.com"+a[1])
        item_num+=1

    in_stock = 0
    in_print=False
    for type in c_types:
        y=0
        for x in type:
            if(y==0):
                print(x+":")
            else:
                source_temp = requests.get(x).text
                soup_temp = BeautifulSoup(source_temp, 'html.parser')
                avail = soup_temp.find_all("input", class_="button")
                for a in avail:
                    s = str(a)
                    b = s.split('"')
                    if ('add to cart' in b):
                        in_stock+=1
                        in_print=True
                if(in_print):
                    if(type[0]==item):
                        add_item(x, 'Large')
                        checkout()
                    print("     " + x + " IN STOCK")
                else:
                    print("     " + x)
                in_print=False
            y=y+1
        print("\n")
    checkout()
    print("Total number of items online currently: " + str(item_num) + "\nCurrent items in stock: " + str(in_stock))

def bot_behavior(time_delay):
    print("Welcome to Supreme Bot 2018\n---------------------------\n"
          "Type help for a list of commands")
    cmd=""
    while(cmd!="quit"):
        cmd=input(">")
        if(cmd=="item"):
            item = input("Input your preferred item: ")
            size = input("Input your preferred size(if applicable): ")
            item_run(item, size,5)
        elif(cmd=="mainrun"):
            main_run()
        elif(cmd=="viewall"):
            view_all()
        elif(cmd=="viewallstock"):
            view_all(True)
        elif(cmd=="help"):
            print("item: This will start you searching for a specific item in a specific size\n"
                  "mainrun: This will run the main run from the root url\n"
                  "viewall: ")
        else:
            print(cmd+" is not a recognized command!")

bot_behavior(200)