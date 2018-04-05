import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

root_url = 'http://www.supremenewyork.com'
all_url = 'http://www.supremenewyork.com/shop/all'
root_types = []
checkout_url = "https://www.supremenewyork.com/checkout"

driver = webdriver.Chrome('C:/chromedriver.exe')

buyerName='Mahdi Haji'
buyerMail='dmd9042@gmail.com'
buyerTele='6072542'
buyerAdress='236 Champlain Street'
buyerCity='Rochester'
buyerZIP='14608'
buyerState = 'NY'
buyerCountry='USA'
buyerCardType='Visa'
buyerCardNumber='4060645434329715'
buyerCardExpMonth='03'
buyerCardExpYear='2021'
buyerCardCVV = '017'

buyerMaxPrice = 500
currentPrice = 0

currentItems = 0
maxItems = 1
cart_list = []

url_list = []

def showInfo():
    """
    Displays the settings the bot is runing
    :return:
    """
    global currentItems, currentPrice, buyerMaxPrice, maxItems, url_list

    print("Items: "+str(currentItems)+"/"+str(maxItems)+"\nPrice: $"+str(currentPrice)+"/"+str(buyerMaxPrice)+"\nURLS(in cart): ")
    for url in url_list:
        print("\t http://www.supremenewyork.com" + url)

def clearMemory():
    """
    Clears the bots memory of URLS
    :return:
    """
    global url_list, cart_list, currentItems, currentPrice
    url_list = []
    cart_list = []
    currentPrice = 0
    currentItems = 0

def clearCart():
    """
    Clear the cart from the console
    :return: A clear cart
    """
    global cart_list, currentItems, currentPrice
    currentItems = 0
    currentPrice = 0
    driver.get(root_url+"/shop/cart")
    byes = driver.find_elements_by_class_name("intform")

    for bye in byes:
        bye.submit()
        print(bye.text)


def decode(message):
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    message = str(message).replace('a', 'b')
    message = str(message).replace('B', '8')
    message = str(message).replace('c', '1')
    message = str(message).replace('d', 'Y')
    message = str(message).replace('D', 'o')
    message = str(message).replace('e', 'T')

    message = str(message).replace('G', 'Q')
    message = str(message).replace('g', 't')
    message = str(message).replace('S', 'h')
    message = str(message).replace('h', 'S')
    message = str(message).replace('i', 'i')
    message = str(message).replace('k', '5')
    message = str(message).replace('m', 'M')
    message = str(message).replace('M', 'm')
    message= str(message).replace('N', 's')
    message = str(message).replace('o', 'D')
    message = str(message).replace('P', '2')
    message = str(message).replace('p', 'f')
    message = str(message).replace('r', '0')
    message = str(message).replace('R', 'R')
    message = str(message).replace('s', 'N')
    message = str(message).replace('u', '9')
    message = str(message).replace('v', 'j')
    message = str(message).replace('y', 'y')
    message = str(message).replace('h', 'S')
    message = str(message).replace('g', 't')
    message = str(message).replace('t', 'g')
    message = str(message).replace('N', 's')
    message = str(message).replace('F', 'l')
    message = str(message).replace('l', 'F')
    message = str(message).replace('S', 'h')
    message = str(message).replace('h', 'S')
    print("\tEncrypted: {"+message+"}")
    return message

def check_size(url, size):
    """
    Takes the URL and will return if it contains the specific size
    :param url: URL to check
    :param size: Size to check for
    :return: True or False
    """
    driver.get("http://www.supremenewyork.com" + url)
    try:
        sizes = driver.find_element_by_id("s")
        options = [x for x in sizes.find_elements_by_tag_name("option")]
        if (len(options) == 0):
            return True
        for element in options:
            if (size == element.text):
                return True
        print("ERROR: NOT AVAILABLE IN " + size + " SIZE")
    except NoSuchElementException:
        print("ERROR: No Sizes to display")

    return False



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
    if (len(url_list) == 0):
        return True
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
                    #print("Already viewed this item/style")
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

def get_description(url):
    """
    Takes a URL and return the description of the product
    :param url: URL to investigate
    :return: String of the description
    """
    driver.get("http://www.supremenewyork.com" + url)
    harvest = driver.find_elements_by_class_name("description")
    desc = harvest[0].text
    return desc

def add_item(url, size=None):
    """
    Adds an item to the cart using a url and a size or style if available
    :param url: URL of the clothing to buy
    :param size: Size of the clothing to buy (if any)
    :return: An item in the shopping cart
    """
    driver.get("http://www.supremenewyork.com" + url)
    if(size!=None):
        try:
            Select(driver.find_element_by_id('s')).select_by_visible_text(size)
        except NoSuchElementException:
            print("\t\t"+url+": DID NOT HAVE A " + size + " IN STOCK!")
            return 0
    try:
        global currentPrice, currentItems, cart_list, buyerMaxPrice
        cart_list.append(url)
        prices = driver.find_elements_by_class_name("price")
        price = int(prices[0].text[1:4])
        if((currentPrice+price)<buyerMaxPrice):
            driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').click()
            print("Added " + url + " to the cart\n--------------------------------------------------------\n\t($"
                  +str(currentPrice)+"+$"+str(price)+") < $"+str(buyerMaxPrice) + "\n")
            currentPrice += price
            currentItems+=1
        else:
            print("\tERROR: TOO EXPENSIVE FOR MAXIUMUM PRICE!\n\t-----------------------------------------------------"
                  "\n\t\t($"+str(currentPrice)+"+$"+str(price)+") > $"+str(buyerMaxPrice) + "\n")
            return 0
    except NoSuchElementException:
        print("Error: This is sold out!/Already in your cart!")

def checkout():
    """
    Take the session to checkout and autofill it with the information found in the header of the file
    (Ensure that this information is 100% correct before checkout)
    :return: A Captcha or Checkout items for the session
    """
    print("--------------------------------------------------------\nAttempting to checkout... \n...\n...")
    time.sleep(.3)
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
        ord_terms = driver.find_element_by_id('order_terms')
        ord_terms.send_keys(" ")
        driver.find_element_by_tag_name("form").submit()
    except NoSuchElementException:
        print("Error: Could not Checkout!")
    global currentPrice, currentItems
    print("CHECKOUT:\n\t("+str(currentItems)+"/"+str(maxItems) +") ITEMS: " + "$"+str(currentPrice)+"/"+str(buyerMaxPrice)
          +"\n--------------------------------------------------------")

def item_target(item, size=None, keyWords=[], color=None, maxPrice=None, print_messages=False):
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
    global maxItems
    new_url = all_url+"/"+item
    source = requests.get(new_url).text
    soup = BeautifulSoup(source, 'html.parser')
    items = soup.find_all("div", class_='inner-article')
    itemCount=0
    keywordCount=0
    for item in items:
        s = str(item).split('"')
        key = str(item).split(">")
        item_keys = key[6][:-3].split(" ")
        item_color = key[10][:-3]
        if("sold_out_tag" in s):
            sold_keys = key[8][:-3].split(" ")
            for key in sold_keys:
                for our in keyWords:
                    if (key.upper() == our.upper()):
                        keywordCount+=1
                        print("Successful keywork match: " + our + " is SOLD OUT!")
        else:
            #print(item)
            url = s[3]
            if(url in url_list):
                #print("Already viewed URL")
                pass
            else:
                if(print_messages):
                    print("FOUND ITEM: " + str(' '.join(item_keys)) + "\n\tColor: "+item_color +
                      "\n\tURL: http://www.supremenewyork.com/"+url + "\n\tDescription: "+get_description(url))
                for key in item_keys:
                    for our in keyWords:
                        if(key.upper()==our.upper() and (size==None or check_size(url, size)) and check_unique(url) and (maxItems>itemCount)):
                            print("\nKEYWORK MATCH: "+ key + ":"+our)
                            add_item(url, size)
                            update_url(url)
                            itemCount+=1
                if(len(cart_list)==maxItems):
                    print("\nReached Maximum Item Limit!")
                    checkout()
                    return 0

    if(itemCount>0):
        print("\nYou never reached your maximum item limit")
        checkout()
    else:
        print("\nYour Keywords DID NOT MATCH")
        if(keywordCount>0):
            print("\t"+str(keywordCount)+" sold out items that returned True")


def view_all(inStock=False):
    """
    View all of the instock items and add them to the cart
    :param inStock: Boolean flag (Will print different text)
    :param maxItems: Maximum amount of items to buy
    :return:
    """
    global maxItems
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
            #print("Color: "+get_color(url))
            if check_unique(url):
                add_item(url)
            if(url in url_list):
            #    print("Already viewed URL")
                pass
            else:
                update_url(url)
            if(maxItems!=None and len(cart_list)==maxItems):
                checkout()
                return
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
    print("You have sucessfully updated your information\n")

def bot_behavior(time_delay, on=False):
    """
    Main logic for the bot
    :param time_delay: Time delay between checking for the items
    :return:
    """
    print("\t\t\t  Welcome to Supreme Bot 2018\n--------------------------------------------------------\n"
          "\t\t\tType help for a list of commands\n--------------------------------------------------------")
    cmd=""
    global maxItems, buyerMaxPrice
    start_time=time.time()
    while(cmd!="quit"):
        print("\t\t------- %s seconds -------" % (time.time() - start_time))
        cmd=input("> ")
        if(cmd=="item"):
            item = input("Input your preferred item[Jackets/Shirts/Hoodies]: ")
            size = input("Input your preferred size[Small/Medium/Large/XLarge]: ")

            if(size == "xlarge" or size == "Xlarge"):
                size = "XLarge"
            else:
                if (size == " " or size == ""):
                    size = None
                else:
                    size = size.capitalize()
            color = input("Input your preferred color[Gold/Silver/Red/Blue]: ")
            keys = []
            key = "e"
            print("\tINPUT 'end' TO EXIT")
            while (key != "end"):
                key = input("Enter a keyword to search for: ")
                if(key!="end"):
                    key2 = decode(key.capitalize())
                    keys.append(key2)
            live = input("Do you want this to be live[y/N]: ")
            start_time = time.time()
            if(live=='y'):
                on=True
            else:
                on=False
            if(on):
                while(True):
                    item_target(item, size, keys, color, maxPrice=buyerMaxPrice)
                    time.sleep(time_delay)
            else:
                item_target(item, size, keys, color, maxPrice=buyerMaxPrice)
        elif(cmd=="viewall"):
            start_time = time.time()
            view_all()
        elif(cmd=="maxitems"):
            maxItems=int(input("Enter the maximum amount of items: "))
        elif(cmd=="maxprice"):
            buyerMaxPrice = int(input("Enter the maximum amount to spend: "))
        elif(cmd=="showinfo"):
            showInfo()
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
            start_time = time.time()
            update_info(name,phone,address,city, state, zip, cardNumber, cardExpMonth, cardExpYear, cardCVV)
        #elif(cmd=="viewallstock"):
        #    view_all(True)
        elif(cmd=="clearcart"):
            clearCart()
        elif(cmd=="clearmemory"):
            clearMemory()
        elif(cmd=="help"):
            print("--------------------------------------------------------\nitem: Search for a specific item with "
                  "specific conditions\nviewall: Find any new items regardless "
                  "of keywords\nupdate: Allow you to update the console information\n"
                  "maxitems: Update the maximum items the bot can buy\nmaxprice: Update the maximum price the box can "
                  "buy\n--------------------------------------------------------")
        else:
            print(cmd+" is not a recognized command!")

"""Main Logic Call"""
bot_behavior(.5, False)