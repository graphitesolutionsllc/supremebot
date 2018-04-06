import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

root_url = 'http://www.supremenewyork.com'
all_url = 'http://www.supremenewyork.com/shop/all'
root_types = []
checkout_url = "https://www.supremenewyork.com/checkout"

driver = webdriver.Chrome('C:/chromedriver.exe')

alphabet1 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
alphabet2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

customAlphabet = []
key = ""

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

buyerMaxPrice = 1000
#This starts at 10 due to the ship and handle fee
currentPrice = 10

encryp = False
decryp = False
printMessages = False

currentItems = 0
maxItems = 5
cart_list = []

url_list = []

def create_alphabet(english, scrambled):
    """
    Taking a scrambled and plain text version of the same word we will calculate the code and create a alphabet
    to translate kewyords
    :param english: (String) English version of the word
    :param scrambled: (String) Scrambled version of the word
    :return: global customAlphabet and key will be populated
    """
    pass

def encrypt(message):
    """
    Given a string scramble it in able to search the site on launch
    :param message: (String) English word the user typed in to be encrypted
    :return message: (String) Scrambled english the site can search with
    """
    return message

def decrypt(message):
    """
    Read scrambled messages and translate them into english for reading
    :param message: (String) Scrambled english
    :return: (String) Readable English
    """
    return message

def show_info():
    """
    Displays the settings the bot is running
    :return:
    """
    global currentItems, currentPrice, buyerMaxPrice, maxItems, url_list, encrypt, decrypt, printMessages

    print("Items: "+str(currentItems)+"/"+str(maxItems)+"\nPrice: $"+str(currentPrice)+"/$"+str(buyerMaxPrice)+
          "\nEncrypt: "+str(encryp)+"\nDecrypt: "+str(decryp)
          +"\nPrint Messages: "+str(printMessages)+"\nURLS(in cart): ")
    for url in url_list:
        print("\t http://www.supremenewyork.com" + url)

def clear_memory():
    """
    Clears the bots memory of URLS
    :return: List locations wiped clean and reset global variables
    """
    global url_list, cart_list, currentItems, currentPrice
    url_list = list()
    cart_list = list()
    currentPrice = 10
    currentItems = 0

def empty_cart():
    """
    Clear the cart from the console
    :return: An empty cart
    """
    global cart_list, currentItems, currentPrice
    for x in range(0, currentItems):
        driver.get(root_url + "/shop/cart")
        byes = driver.find_elements_by_class_name("intform")
        for bye in byes:
            bye.submit()
            print("Removed from cart")
    currentItems = 0
    currentPrice = 0
    clear_memory()

def check_stock(url):
    """
    Returns a boolean if it is in stock
    :param url: (String) URL of item
    :return: (Bool) True or False
    """
    source = requests.get(root_url + url).text
    soup = BeautifulSoup(source, 'html.parser')
    sold_raw = str(soup.find_all("b", class_="button sold-out"))
    if(sold_raw!=None):
        return True
    else:
        return False

def check_size(url, size):
    """
    Takes the URL and will return if it contains the specific size
    :param url: (String) URL to check
    :param size: (String) Size to check for
    :return: (Bool) True or False
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

def get_root(urls):
    """
    Returns the root of the url that is unique
    :param url: (String) URL to manipulate
    :return: (String) simplified url
    """
    a = str(urls).split("/")
    a = a[2:4]
    a = ''.join(a)
    return a

def get_color(url):
    """
    Takes the URL and gives the color back
    :param url: (String) URL to obtain the color from
    :return: (String) Color of the item
    """
    color = ""
    source = requests.get(root_url + url).text
    soup = BeautifulSoup(source, 'html.parser')
    color_raw = str(soup.find_all("p", class_='style protect'))
    colorr = color_raw.split(">")
    color = colorr[1].split("<")[0]
    return color

def get_title(url):
    """
    Takes the URL and gives the title back
    :param url: (String) URL of the item to obtain title from
    :return:(String) Title of the item
    """
    source = requests.get(root_url+url).text
    soup = BeautifulSoup(source, 'html.parser')
    title_raw = str(soup.find_all("h1", class_='protect'))
    titlee = title_raw.split(">")
    title = titlee[1].split("<")[0]
    return title

def check_unique(url):
    """
    Acts as a way to tell if we have seen this type of style before in another color
    :param url: (String) URL of the item to check
    :return: (Bool) True or False if we have seen it while alive
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
        for b in bang:
            for s in spl:
                if(b==s):
                    #print("Already viewed this item/style")
                    return False
    return True

def update_url(url):
    """
    Updates the global url_list array
    :param url: (String) Url to update the array
    :return: Updated global url_list array
    """
    global url_list
    check_unique(url)
    url_list.append(url)

def get_description(url):
    """
    Takes a URL and return the description of the product
    :param url: (String) URL to investigate
    :return: String of the description
    """
    driver.get("http://www.supremenewyork.com" + url)
    harvest = driver.find_elements_by_class_name("description")
    desc = harvest[0].text
    return desc

def add_item(url, size=None):
    """
    Adds an item to the cart using a url and a size or style if available
    You can buy up to 10 items at a time
    :param url: (String) URL of the clothing to buy
    :param size: (String) Size of the clothing to buy (if any)
    :return: An item in the shopping cart
    """
    driver.get("http://www.supremenewyork.com" + url)
    if(size!=None):
        try:
            Select(driver.find_element_by_id('s')).select_by_visible_text(size)
        except NoSuchElementException:
            print("\t\t"+url+": DID NOT HAVE A " + size + " IN STOCK!")
            return 0
    wait = WebDriverWait(driver, 2)
    something = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="add-remove-buttons"]/input')))
    driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').click()
    time.sleep(.03)
    global currentPrice, currentItems, cart_list, buyerMaxPrice, printMessages
    cart_list.append(url)
    prices = driver.find_elements_by_class_name("price")
    price = int(prices[0].text[1:4])
    if(printMessages):
        print("ADDED: {" + get_title(url) + "} to the cart\n\tColor: "+get_color(url)+
              "\n--------------------------------------------------------\n\t($"
                  +str(currentPrice)+"+$"+str(price)+") < $"+str(buyerMaxPrice) + "\n")
    currentPrice += price
    currentItems+=1
    return 0


def checkout():
    """
    Take the session to checkout and autofill it with the information found in the header of the file
    (Ensure that this information is 100% correct before checkout)
    :return: A Captcha or Checkout items for the session
    """
    print("--------------------------------------------------------\nAttempting to checkout... \n...\n...\n...")
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
    final = "%0.2f" % (float((currentPrice)*1.07495))
    print("CHECKOUT COMPLETE:\n\t("+str(currentItems)+"/"+str(maxItems) +") ITEMS: " + "$"+str(final)+"/$"+str(buyerMaxPrice)
          +"\n--------------------------------------------------------")


def item_target(item, size=None, keyWords=[], color=None):
    """
    Target a certain type of item, by manipulating the all_url and adding the item
    word at the end you will arrive the the catagory to scrape, then it will check to see if the
    item matches any keywords, if so it adds it to the cart. When the max items or price is reached
    then the function does a checkout
    :param item: (String) The string we will be modifying the URL with
    :param size: (String) Requested size of the item
    :param keyWords: (List of Strings) Array of keywords to search with
    :param color: (String) Requested color of the item
    :return:
    """
    global maxItems, buyerMaxPrice, printMessages
    new_url = all_url+"/"+item
    source = requests.get(new_url).text
    soup = BeautifulSoup(source, 'html.parser')
    items = soup.find_all("div", class_='inner-article')
    itemCount = 0
    keywordCount =0
    hits = []
    for item in items:
        s = str(item).split('"')
        url = s[3]
        key = str(item).split(">")
        item_keys = key[6][:-3].split(" ")
        item_color = key[10][:-3]
        if("sold_out_tag" in s):
            sold_keys = key[8][:-3].split(" ")
            for key in sold_keys:
                key = key.replace("®", "")
                for our in keyWords:
                    if ((key.upper() == our.upper()) and (get_root(url) not in hits)):
                        keywordCount+=1
                        if(printMessages):
                            print("Successful keywork match: \n\t(" + get_title(url)
                              + "{Color: "+get_color(url)+") is SOLD OUT!\n\tURL: http://www.supremenewyork.com"+url)
                        hits.append(get_root(url))
        else:
            # print(item) #DEBUG LINE
            if(url in url_list):
                if(printMessages): print("Already viewed URL")
                pass
            else:
                if(printMessages):
                    print("Successful keywork match: \n\t(" + get_title(url)
                          + "{Color: " + get_color(url) + "}) is IN STOCK!\n\tURL: http://www.supremenewyork.com" + url)
                for key in item_keys:
                    key = key.replace("®","")
                    for our in keyWords:
                        if(key.upper()==our.upper() and (size==None or check_size(url, size)) and check_unique(url)
                                and (maxItems>itemCount) and check_stock(url)):
                            if(printMessages): print("\nKEYWORK MATCH: "+ key + ":"+our)
                            add_item(url, size)
                            update_url(url)
                            itemCount+=1
                if(len(cart_list)==maxItems):
                    print("\nReached Maximum Item Limit!")
                    checkout()
                    return 0

    if(len(cart_list)>0):
        print("\nYou never reached your maximum item limit")
        checkout()
    else:
        print("\nYour Keywords DID NOT MATCH")
        if(keywordCount>0):
            print("\t"+str(keywordCount)+" SOLD OUT items returned True")


def view_all():
    """
    View all of the instock items and add them to the cart
    :return:
    """
    global maxItems, url_list, printMessages
    source = requests.get(all_url).text
    soup = BeautifulSoup(source, 'html.parser')
    items = soup.find_all("div", class_='inner-article')
    for item in items:
        #print(item) #DEBUG LINE
        s = str(item).split('"')
        if("sold_out_tag" in s):
            pass
        else:
            url = s[3]
            if check_unique(url) and check_stock(url):
                add_item(url)
            if(url in url_list):
                if(printMessages): print("Already viewed URL")
            else:
                update_url(url)
            if(len(cart_list)==maxItems):
                if(printMessages): print("\nReached Maximum Item Limit! ("+str(maxItems)+"/"+str(maxItems)+")")
                checkout()
                return 0
    if(printMessages): print("CHECKED ALL URLs")
    if(len(cart_list)>0): checkout()

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
    :return: Updated checkout fields
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
    global maxItems, buyerMaxPrice, encryp, decryp, printMessages
    start_time=time.time()
    while(cmd!="quit"):
        print("------------------- %.5f seconds -------------------" % (time.time() - start_time))
        cmd=input("> ")
        if(cmd=="item"):
            item = input("Input your preferred item[Jackets/Shirts/Hoodies]: ")
            size = input("Input your preferred size[Small/Medium/Large/XLarge]: ")
            if(size == "xlarge" or size == "Xlarge"):
                size = "XLarge"
            elif (size == " " or size == ""):
                size = None
            else:
                size = size.capitalize()
            color = input("Input your preferred color[Gold/Silver/Red/Blue]: ")
            keys = []
            key = "e"
            print("\tINPUT 'end' TO EXIT")
            while (key != "end"):
                key = input("Enter a keyword to search for: ")
                if(key!="end") and encryp:
                    key=encrypt(key.capitalize())
                    if(printMessages): print("\tEncrypted: {" + key + "}")
                keys.append(key.capitalize())
            live = input("Do you want this to be live[y/N]: ")
            start_time = time.time()
            if(live=='y'):
                on=True
            else:
                on=False
            if(on):
                while(True):
                    item_target(item, size, keys, color)
                    time.sleep(time_delay)
            else:
                item_target(item, size, keys, color)
        elif(cmd=="viewall"):
            start_time = time.time()
            view_all()
        elif(cmd=="items"):
            maxItems=int(input("Enter the maximum amount of items: "))
        elif(cmd=="price"):
            buyerMaxPrice = int(input("Enter the maximum amount to spend: "))
        elif(cmd=="info"):
            show_info()
        elif(cmd=="encrypt"):
            if(encryp):
                print("TURNING OFF ENCRYPTION")
                encryp=False
            else:
                print("TURNING ON ENCRYPTION")
                encryp=True
        elif(cmd=="decrypt"):
            if (decryp):
                print("TURNING OFF DECRYPTION")
                decryp = False
            else:
                print("TURNING ON DECRYPTION")
                decryp = True
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
        elif(cmd=="emptycart"):
            empty_cart()
        elif(cmd=="clearmemory"):
            clear_memory()
        elif(cmd=="print"):
            if(printMessages):
                print("MESSAGE PRINTING: OFF")
                printMessages=False
            else:
                print("MESSAGE PRINTING: ON")
                printMessages=True
        elif(cmd=="help"):
            print("--------------------------------------------------------\nitem: Search for a specific item with "
                  "specific conditions\n\t(Type/Size/Color/Keywords)\nviewall: Find any new items regardless "
                  "of keywords\nupdate: Allow you to update the console information\n"
                  "items: Update the maximum items the bot can buy\nemptycart: empty the cart from the shell\n"
                  "price: Update the maximum price the box can "
                  "buy\nencrypt: Change keywords to predictive scrambled keywords\n"
                  "\t(Using your own dictionary, site updates at 8:30AM)\n"
                  "decrypt: Read all encrypted keywords normally on drop\n"
                  "info: Displays settings for the current bot\n"
                  "print: Displays more messages of the backend\n"
                  "--------------------------------------------------------")
        else:
            print(cmd+": is not a recognized command!")

"""Main Logic Call"""
bot_behavior(.5, False)