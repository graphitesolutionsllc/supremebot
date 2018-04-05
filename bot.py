import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from string import ascii_uppercase

root_url = 'http://www.supremenewyork.com/shop'
all_url = 'http://www.supremenewyork.com/shop/all'
root_types = []
checkout_url = "https://www.supremenewyork.com/checkout"

driver = webdriver.Chrome('C:/chromedriver.exe')

buyerName='Supreme Buyer'
buyerMail='dmd9042@gmail.com'
buyerTele='1337879009'
buyerAdress='Area 31'
buyerCity='Nirvana'
buyerZIP='66666'
buyerState = 'NY'
buyerCountry='USA'
buyerCardType='Mastercard'
buyerCardNumber='4117733984087777'
buyerCardExpMonth='07'
buyerCardExpYear='2020'
buyerCardCVV = '450'

buyerMaxPrice = 0
currentPrice = 0

url_list = []


def get_color(url):
    """
    Takes the URL and gives the color back
    :param url:
    :return:
    """
    driver.get("http://www.supremenewyork.com" + url)
    color_raw = driver.find_element_by_xpath("//*[@class='style protect']")
    color = color_raw.text
    return color

def check_unique(url):
    """
    Acts as a way to tell if we have seen this type of style before in another color
    :param url: URL of the item to check
    :return: True or False if we have seen it while alive
    """
    global url_list
    bang = str(url).split("/")
    bang.remove("shop")
    bang = bang[2:4]
    for url in url_list:
        spl = str(url).split("/")
        spl.remove("shop")
        spl = spl[2:4]
        #print(" ".join(bang)+"\n"+" ".join(spl))
        for b in bang:
            for s in spl:
                if(b==s):
                    print("Already viewed this style")
                    return False
    return True

def update_url(url):
    """
    Updates the global url_list array
    :param url: Url to update the array
    :return: Updated global url_list array
    """
    global url_list
    check_unique(url)
    url_list.append(url)

def add_item(url, size=None):
    """
    Adds an item to the cart using a url and a size or style if available
    :param url: URL of the clothing to buy
    :param size: Size of the clothing to buy (if any)
    :return: An item in the shopping cart
    """
    driver.get("http://www.supremenewyork.com" + url)
    if (size == " " or size == ""):
        size = None
    if(size!=None):
        size = size.capitalize()
        try:
            Select(driver.find_element_by_id('s')).select_by_visible_text(size)
        except NoSuchElementException:
            print("\t\t"+url+": DID NOT HAVE A " + size + " IN STOCK!")
    try:
        driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').click()
        print("Added " + url + " to the cart")
        global currentPrice
        prices = driver.find_elements_by_class_name("price")
        price = int(prices[0].text[1:4])
        currentPrice += price
    except NoSuchElementException:
        print("Error: This is sold out!/Already in your cart!")

def checkout():
    """
    Take the session to checkout and autofill it with the information found in the header of the file
    (Ensure that this information is 100% correct before checkout)
    :return: A Captcha or Checkout items for the session
    """
    #time.sleep(.2)
    try:
        driver.get(checkout_url)
        try:
            ord_billing_name = driver.find_element_by_id('order_billing_name')
            ord_billing_name.send_keys(buyerName)
        except WebDriverException:
            print("ERROR: Could not find the Billing Name")
        ord_email = driver.find_element_by_id('order_email')
        ord_email.send_keys(buyerMail)
        ord_tele = driver.find_element_by_id('order_tel')
        ord_tele.send_keys(buyerTele)
        ord_adress = driver.find_element_by_id('bo')
        ord_adress.send_keys(buyerAdress)
        ord_billing_city = driver.find_element_by_id('order_billing_city')
        ord_billing_city.send_keys(buyerCity)
        Select(driver.find_element_by_id('order_billing_state')).select_by_visible_text(buyerState)
        ord_zip = driver.find_element_by_id('order_billing_zip')
        ord_zip.send_keys(buyerZIP)
        Select(driver.find_element_by_id('order_billing_country')).select_by_visible_text(buyerCountry)
        ord_cnb = driver.find_element_by_id("nnaerb")
        ord_cnb.send_keys(buyerCardNumber)
        ord_cvv = driver.find_element_by_id("orcer")
        ord_cvv.send_keys(buyerCardCVV)
        Select(driver.find_element_by_id('credit_card_month')).select_by_visible_text(buyerCardExpMonth)
        Select(driver.find_element_by_id('credit_card_year')).select_by_visible_text(buyerCardExpYear)
        ord_terms = driver.find_element_by_id("order_terms")

        try:
            ord_terms.click()
        except WebDriverException:
            print("ERROR: Could not click the term button!!")
        driver.find_element_by_tag_name("form").submit()
    except NoSuchElementException:
        print("Error: Could not Checkout!")
    global currentPrice
    print("ATTEMPTED TO CHECKOUT: " + str(currentPrice))

def item_target(item, size=None, keyWords=[], color=None,maxItems=1, maxPrice=None):
    """
    Target a certain type of item, by manipulating the all_url and adding the item
    word at the end you will arrive the the catagory to scrape, then it will check to see if the
    item matches any keywords, if so it adds it to the cart. When the max items or price is reached
    then the function does a checkout
    :param item: The string we will be modifying the URL with
    :param size: Requested size of the item
    :param keyWords: Array of keywords to search with
    :param color: Requested color of the item
    :param maxItems: Maximum amonunt of items
    :param maxPrice: Maximum price for the order
    :return:
    """
    new_url = all_url+"/"+item
    source = requests.get(new_url).text
    soup = BeautifulSoup(source, 'html.parser')
    items = soup.find_all("div", class_='inner-article')
    itemCount=0
    for item in items:
        s = str(item).split('"')
        if("sold_out_tag" in s):
            pass
        else:
            #print(item)
            url = s[3]
            if(url in url_list):
                print("Already viewed URL")
            else:
                update_url(url)
                key = str(item).split(">")
                item_keys = key[6][:-3].split(" ")
                item_color = key[10][:-3]
                print("FOUND ITEM: " + str(' '.join(item_keys)) + "\n\tColor: "+item_color)
                for key in item_keys:
                    for our in keyWords:
                        if(key.upper()==our.upper() and check_unique(url)):
                            add_item(url, size)
                            itemCount+=1
                            if(maxItems==itemCount):
                                checkout()
                                return



def view_all(inStock=False, maxItems=None):
    """
    View all of the instock items and add them to the cart
    :param inStock: Boolean flag (Will print different text)
    :param maxItems: Maximum amount of items to buy
    :return:
    """
    in_stock = 0
    source = requests.get(all_url).text
    soup = BeautifulSoup(source, 'html.parser')
    #print(soup.prettify())
    global url_list
    items = soup.find_all("div", class_='inner-article')
    for item in items:
        #print(item)
        s = str(item).split('"')
        if("sold_out_tag" in s):
            pass
        else:
            i = s[3].split('/')
            url = s[3]
            print("Color: "+get_color(url))
            if check_unique(url):
                add_item(url)
            if(url in url_list):
                print("Already viewed URL")
            else:
                update_url(url)
            in_stock+=1
            if(maxItems!=None and in_stock==maxItems):
                checkout()
                return
    print(str(in_stock) + " items in stock")
    #for i in url_list:
    #    print(i)
    checkout()

def update_info(name, phone, address, city, state, zip, cardNumber, cardExpMonth, cardExpYear, cardCVV, country='USA'):
    """
    Allows the user of the shell to update all of the information for checkout
    :param name: Name on card
    :param phone: Phone for order
    :param address: Billing and Shipping address
    :param city: Billing City
    :param state: Billing State
    :param zip: Billing Zip
    :param cardNumber: Billing Card Number
    :param cardExpMonth: Billing Card Expiration Month
    :param cardExpYear: Billing Card Expiration Year
    :param cardCVV: Billing Card CVV
    :param country: Billing Country (USA default)
    :return: Updated checkout feilds
    """
    global buyerName, buyerAdress, buyerCity, buyerCountry, buyerMail, buyerState, buyerCardCVV, buyerCardExpMonth
    global buyerCardExpYear, buyerCardNumber, buyerZIP,  buyerTele
    buyerName=name
    buyerTele=phone
    buyerAdress=address
    buyerCity=city
    buyerState=state
    buyerZIP=zip
    buyerCountry=country
    buyerCardNumber=cardNumber
    buyerCardExpYear=cardExpYear
    buyerCardExpMonth=cardExpMonth
    buyerCardCVV=cardCVV

def bot_behavior(time_delay, on=False):
    """
    Main logic for the bot
    :param time_delay: Time delay between checking for the items
    :return:
    """
    print("\t\t\t  Welcome to Supreme Bot 2018\n--------------------------------------------------------\n"
          "\t\t\tType help for a list of commands\n--------------------------------------------------------")
    cmd=""
    """
    buyerMaxPrice = int(input("Please enter the maximum you would like to spend: "))
    global buyerName
    buyerName = input("Enter your card name: ")
    global buyerCardCVV
    buyerCardCVV = '666'
    """
    while(cmd!="quit"):
        cmd=input("> ")
        if(cmd=="item"):
            item = input("Input your preferred item: ")
            size = input("Input your preferred size: ")
            color = input("Input your preferred color: ")
            keys = []
            key = ""
            print("\tINPUT 'end' TO EXIT")
            while (key != "End"):
                key = input("Enter a keyword to search for: ")
                key = key.capitalize()
                keys.append(key)
            print("\n")
            if(on):
                while(True):
                    item_target(item, size, keys, color, maxPrice=buyerMaxPrice)
                    time.sleep(time_delay)
            else:
                item_target(item, size, keys, color, maxPrice=buyerMaxPrice)
        elif(cmd=="viewall"):
            view_all()
        elif(cmd=="update"):
            name = input("Enter your card name: ")
            phone = input("Enter a valid 10 digit phone number: ")
            address = input("Enter your street address: ")
            zip = input("Enter your zip code: ")
            city = str(input("Enter your city: "))
            state = str(input("Enter your state (Caps two characters): "))
            cardNumber = input("Enter a valid card number: ")
            cardExpMonth = input("Enter the month the card expires (01/02/...): ")
            cardExpYear = input("Enter the year the card expires (2020/2021/...): ")
            cardCVV = input("Enter the CVV for the card: ")
            update_info(name,phone,address,city, state, zip, cardNumber, cardExpMonth, cardExpYear, cardCVV)
            print("You have sucessfully updated your information\n")
        #elif(cmd=="viewallstock"):
        #    view_all(True)
        elif(cmd=="help"):
            print("--------------------------------------------------------\nitem: This will start you searching "
                  "for a specific item\n\t\t\t\twith specific conditions\nviewall: This will find any new items regardless "
                  "of keywords\nupdate: This will allow you to update the information the console is running with\n"
                  "--------------------------------------------------------")
        else:
            print(cmd+" is not a recognized command!")

"""Main Logic Call"""
bot_behavior(.5, True)