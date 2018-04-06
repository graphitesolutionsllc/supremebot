"""
Supreme® Bot 2018
Author: Daniel Duffy

Using BeautifulSoup and selenium for web-browser control, a predictive keyword searching bot
that will be able to adaptively overcome the site's security by learning it, itself.

    Python:          3.6.4
    BeautifulSoup4:  4.5.0
    Requests:        2.18.4
    Selenium:        3.11.0
"""
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, WebDriverException


root_url = 'http://www.supremenewyork.com'  # Helper to print URLs with only the partial
all_url = 'http://www.supremenewyork.com/shop/all'  # Main entrance point
checkout_url = "https://www.supremenewyork.com/checkout"  # Checkout URL

driver = webdriver.Firefox()  # Driver for FireFox | driver = webdriver.Chrome() # Driver for Chrome

buyerName = 'Bob Evans'  # Dummy information to be replaced on startup
buyerMail = 'fake_email@gmail.com'
buyerTele = '60725423300'
buyerAdress = '236 Champlain Street'
buyerCity = 'Wheelchair'
buyerZIP = '14610'
buyerState = 'FL'
buyerCountry = 'USA'
buyerCardType = 'Visa'
buyerCardNumber = '4111111111111111'
buyerCardExpMonth = '03'
buyerCardExpYear = '2021'
buyerCardCVV = '917'

buyerMaxPrice = 1000  # Default Max Price
moneyMode = False  # Will ignore maxPrice and listen to itemNumbers strictly (when False)
currentPrice = 10  # This starts at 10 due to the ship and handle fee

encryp = False  # Scrambling user input to website
decryp = False  # De-Scrambling website input to user
printMessages = False  # Message print boolean flag

currentItems = 0  # Current number of items in the cart
maxItems = 5  # Maximum amount of items allowed to checkout

cart_list = []  # URLs that are in my cart
url_list = []  # URLs that I have viewed in this session


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
    :return: Prints the settings to the users console
    """
    global currentItems, currentPrice, buyerMaxPrice, maxItems, url_list, encryp, decryp, \
        printMessages, moneyMode

    print("Items: \t\t{"+str(currentItems)+"/"+str(maxItems)+"}\nPrice: \t\t{$"+str(currentPrice)+"/$"+
          str(buyerMaxPrice)+"}\nEncrypt: \t"+str(encryp)+"\nDecrypt: \t"+str(decryp) + "\nMoney Priority: "
          + str(moneyMode) + "\nPrint Messages: "+str(printMessages)+"\nItems in cart: ")
    if len(url_list) == 0: print("\t\t{NONE}")
    for url in cart_list:
        print("\t\t{"+get_title(url) + "(Color: "+get_color(url)+")} ")


def clear_memory():
    """
    Clears the bots memory of URLS
    :return: List locations wiped clean and reset global variables
    """
    global url_list, cart_list, currentItems, currentPrice, printMessages
    url_list = list()
    cart_list = list()
    currentPrice = 10
    currentItems = 0
    if printMessages:
        print("MEMORY IS DELETED: Billing and card info has not been changed")


def check_stock(url):
    """
    Returns a boolean if it is in stock
    :param url: (String) URL of item
    :return: (Bool) True or False
    """
    source = requests.get(root_url + url).text
    soup = BeautifulSoup(source, 'html.parser')
    sold_raw = str(soup.find_all("b", class_="button sold-out"))
    if sold_raw is not None:
        if printMessages:
            print("{" + get_title(url) + "(Color: " + get_color(url) + ")} IN STOCK!")
        return True
    else:
        if printMessages:
            print("{" + get_title(url) + "(Color: " + get_color(url) + ")} OUT OF STOCK!")
        return False


def check_size(url, size):
    """
    Takes the URL and will return if it contains the specific size
    :param url: (String) URL to check
    :param size: (String) Size to check for
    :return: (Bool) True or False
    """
    if size.upper() == "XLARGE" or size.upper() == "LARGE" or size.upper() == "MEDIUM" or size.upper() == "SMALL":
        try:
            source = requests.get(root_url + url).text
            soup = BeautifulSoup(source, 'html.parser')
            options = soup.find_all("Select", class_='s')
            if len(options) == 0:
                return True
            for element in options:
                if size == element.text:
                    return True
            if printMessages:
                print("\tERROR: {" + get_title(url) + "(" + get_color(url) + ")" +
                      "}\n\t\t\t*NOT AVAILABLE IN {" + size + "} SIZE")
        except NoSuchElementException:
            print("ERROR: No Sizes to display")
    if printMessages: print("\nERROR: {"+size+"} SIZE IS NOT CORRECT!")
    return False


def get_cart():
    """
    Prints the cart (item title and color) for the user
    :return:
    """
    global currentItems
    print("    --------------------Cart---------------------")
    if len(cart_list) == 0: print("\t-{NOTHING IN CART}")
    for item in cart_list:
        print("  \t-{" + get_title(item)+"}: {Color: " + get_color(item)+"}")
    print("\n")


def get_root(urls):
    """
    Returns the root of the url that is unique
    :param urls: (String) URL to manipulate
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
    source = requests.get(root_url + url).text
    soup = BeautifulSoup(source, 'html.parser')
    return str(soup.find_all("p", class_='style protect')).split(">")[1].split("<")[0]


def get_title(url):
    """
    Takes the URL and gives the title back
    :param url: (String) URL of the item to obtain title from
    :return:(String) Title of the item
    """
    source = requests.get(root_url+url).text
    soup = BeautifulSoup(source, 'html.parser')
    title = str(soup.find_all("h1", class_='protect')).split(">")[1].split("<")[0]
    return title


def check_unique(url):
    """
    *REMEMBER YOU REMVED THE SHOP FROM BANG*
    Acts as a way to tell if we have seen this type of style before in another color
    :param url: (String) URL of the item to check
    :return: (Bool) True or False if we have seen it while alive
    """
    global url_list
    if len(url_list) == 0:
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
                if b == s:
                    return False
    return True


def similar_style(url, color):
    """
    Determines the color of the other styles to check against the users preferred color
    :param url: (String) URL of first item
    :return:
    """



def update_url(url):
    """
    Updates the global url_list array
    :param url: (String) Url to update the array
    :return: Updated global url_list array
    """
    global url_list
    check_unique(url)
    url_list.append(url)


def add_item(url, size=None):
    """
    Adds an item to the cart using a url and a size or style if available
    You can buy up to 10 items at a time
    :param url: (String) URL of the clothing to buy
    :param size: (String) Size of the clothing to buy (if any)
    :return: An item in the shopping cart
    """
    global currentPrice, currentItems, cart_list, buyerMaxPrice, printMessages, moneyMode
    driver.get("http://www.supremenewyork.com" + url)
    source = requests.get(root_url+url).text
    soup = BeautifulSoup(source, 'html.parser')
    price = int(soup.find("p", class_='price').text[1:4])
    if moneyMode and ((currentPrice+price)*1.07545) > buyerMaxPrice:
        if printMessages:
            print("\tUNABLE TO ADD TO CART: TOO EXPENSIVE")
        return 0
    if size is not None:
        try:
            Select(driver.find_element_by_id('s')).select_by_visible_text(size)
        except NoSuchElementException:
            if printMessages :
                print("{"+get_title(url)+"(Color: "+get_color(url)+")}: DID NOT HAVE A " + size + " IN STOCK!")
            return 0
        if printMessages:
            print("ERROR: UNABLE TO ADD TO CART")
    try:
        driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').click()
        cart_list.append(url)
        if printMessages:
            print("\nADDED: {" + get_title(url) + "} to the cart\n\tColor: " + get_color(url) +
                  "\n--------------------------------------------------------\n\t($" +
                  str(currentPrice) + "+$" + str(price) + ") < $" + str(buyerMaxPrice) + "\n")
        currentPrice += price
        currentItems += 1
    except NoSuchElementException:
        if printMessages:
            print("ERROR: ITEM IS SOLD OUT/UNAVAILABLE")


def checkout():
    """
    Take the session to checkout and autofill it with the information found in the header of the file
    (Ensure that this information is 100% correct before checkout)
    :return: A Captcha or Checkout items for the session
    """
    try:
        driver.get(checkout_url)
    except WebDriverException:
        print("ERROR: Could not retreive the page")
    global currentPrice, currentItems
    print("--------------------------------------------------------\nAttempting to checkout... \n...\n...\n...")
    final = "%0.2f" % (float(currentPrice * 1.0754))
    try:
        ord_billing_name = driver.find_element_by_id('order_billing_name')
        ord_billing_name.send_keys(buyerName)
    except WebDriverException:
        print("ERROR: Could not find the Billing Name Text Field")
    ord_email = driver.find_element_by_id('order_email')
    ord_email.send_keys(buyerMail)
    ord_tele = driver.find_element_by_id('order_tel')
    ord_tele.send_keys(buyerTele)
    ord_adress = driver.find_element_by_id('bo')
    ord_adress.send_keys(buyerAdress)
    ord_zip = driver.find_element_by_id('order_billing_zip')
    ord_zip.send_keys(buyerZIP)
    ord_billing_city = driver.find_element_by_id('order_billing_city')
    ord_billing_city.send_keys(buyerCity)
    Select(driver.find_element_by_id('order_billing_state')).select_by_visible_text(buyerState)
    Select(driver.find_element_by_id('order_billing_country')).select_by_visible_text(buyerCountry)
    ord_cnb = driver.find_element_by_id("nnaerb")
    ord_cnb.send_keys(buyerCardNumber)
    Select(driver.find_element_by_id('credit_card_month')).select_by_visible_text(buyerCardExpMonth)
    Select(driver.find_element_by_id('credit_card_year')).select_by_visible_text(buyerCardExpYear)
    ord_cvv = driver.find_element_by_id("orcer")
    ord_cvv.send_keys(buyerCardCVV)
    element = driver.find_element_by_xpath(".//*[@id='order_terms']")
    webdriver.ActionChains(driver).move_to_element(element).move_by_offset(10, 10).click(element).perform()
    driver.find_element_by_tag_name("form").submit()

    print("CHECKOUT COMPLETE:\n\t("+str(currentItems)+"/"+str(maxItems) + ") ITEMS: " + "$"+str(final)+"/$"
          + str(buyerMaxPrice)+"\n--------------------------------------------------------")


def item_target(item, size=None, key_words=[], color=None):
    """
    Target a certain type of item, by manipulating the all_url and adding the item
    word at the end you will arrive the the catagory to scrape, then it will check to see if the
    item matches any keywords, if so it adds it to the cart. When the max items or price is reached
    then the function does a checkout
    :param item: (String) The string we will be modifying the URL with
    :param size: (String) Requested size of the item
    :param key_words: (List of Strings) Array of keywords to search with
    :param color: (String) Requested color of the item
    :return:
    """
    global maxItems, buyerMaxPrice, printMessages, currentItems
    source = requests.get(all_url+"/"+item).text
    soup = BeautifulSoup(source, 'html.parser')
    items = soup.find_all("div", class_='inner-article')
    key_count = 0
    hits = []
    for item in items:
        s = str(item).split('"')
        url = s[3]
        key = str(item).split(">")
        item_keys = key[6][:-3].split(" ")
        item_color = key[10][:-3]

        if "sold_out_tag" in s:
            sold_keys = key[8][:-3].split(" ")
            for key in sold_keys:
                key = key.replace("®", "")
                for our in key_words:
                    if(key.upper() == our.upper()) and (get_root(url) not in hits):
                        key_count += 1
                        if printMessages:
                            print("\nSuccessful keywork match: \n\t(" + get_title(url) +
                                  "{Color: "+get_color(url)+") is SOLD OUT!\n\tURL: http://www.supremenewyork.com"+url)
                        hits.append(get_root(url))
        else:
            print("HOWDY: " + item_color.upper() + ":" + color.upper())
            if str(item_color.upper()) == str(color.upper()):
                if printMessages:
                    print("COLOR MATCH: ADDED TO CART")
                add_item(url, size)
            if url in url_list:
                pass
            else:
                if printMessages:
                    print("\nSuccessful keywork match: \n\t(" + get_title(url)
                          + "{Color: " + get_color(url) + "}) is IN STOCK!\n\tURL: http://www.supremenewyork.com" + url)
                for key in item_keys:
                    key.replace("®", "")
                    for our in key_words:
                        if(key.upper() == our.upper() and (size is None or check_size(url, size)) and check_unique(url)
                                and (maxItems>currentItems) and check_stock(url)):
                            if printMessages: print("KEYWORK MATCH: " + key + ":"+our)
                            add_item(url, size)
                            update_url(url)
                if len(cart_list) == maxItems:
                    print("\nReached Maximum Item Limit!")
                    checkout()
                    return 0
    if len(cart_list) > 0:
        print("\nChecked all URLS:\n\t\t\t\t{"+str(currentItems)+"/"+str(maxItems)+"} URLs MATCHED")
        checkout()
    else:
        print("\nNO ITEMS WERE AVAILABLE FOR PURCHASE:")
        if key_count > 0:
            print("\t("+str(key_count)+") MATCHED SOLD OUT ITEMS")


def view_all():
    """
    View all of the instock items and add them to the cart
    :return:
    """
    global maxItems, url_list, printMessages, currentItems
    source = requests.get(all_url).text
    soup = BeautifulSoup(source, 'html.parser')
    items = soup.find_all("div", class_='inner-article')
    for item in items:
        s = str(item).split('"')
        if "sold_out_tag" in s:
            pass
        else:
            url = s[3]
            if check_unique(url) and check_stock(url):
                add_item(url)
            if url in url_list:
                if printMessages: print("Already viewed URL")
            else:
                update_url(url)
            if len(cart_list) == maxItems:
                if printMessages:
                    print("\nReached Maximum Item Limit! ("+str(maxItems)+"/"+str(maxItems)+")")
                checkout()
                return 0
    if printMessages: print("\nChecked all URLS:\n\t\t\t\t{"+str(currentItems)+"/"+str(maxItems)+"} MATCHED")
    if len(cart_list) > 0:
        checkout()


def update_info():
    """
    Allows the user of the shell to update all of the information for checkout
    :return: Updated checkout fields
    """
    global buyerName, buyerAdress, buyerCity, buyerCountry, buyerMail, buyerState, buyerCardCVV, buyerCardExpMonth
    global buyerCardExpYear, buyerCardNumber, buyerZIP,  buyerTele

    buyerName= input("Enter your card name: ")
    buyerTele = input("Enter a valid 10 digit phone number: ")
    buyerAdress = input("Enter your street address: ")
    buyerZIP = input("Enter your zip code: ")
    buyerCity = input("Enter your city: ")
    buyerState = input("Enter your state (Caps two characters): ")
    buyerCardNumber = input("Enter a valid card number: ")
    buyerCardExpMonth = input("Enter the month the card expires (01/02/...): ")
    buyerCardExpYear = input("Enter the year the card expires (2020/2021/...): ")
    buyerCardCVV = input("Enter the CVV for the card: ")

    print("You have successfully updated your information\n")


def bot_behavior(time_delay, on=False):
    """
    Main logic for the bot
    :param time_delay: Time delay between checking for the items
    :return:
    """
    print("\t\t  Welcome to Supreme Bot 2018\n--------------------------------------------------------\n"
          "\t\tType help for a list of commands\n--------------------------------------------------------")
    cmd=""
    global maxItems, buyerMaxPrice, encryp, decryp, printMessages, moneyMode
    start_time = time.time()
    while cmd != "quit":
        print("------------------- %.6f seconds -------------------" % (time.time() - start_time))
        cmd = input("> ")
        if cmd == "item":
            item = input("Input your preferred item[Jackets/Shirts/Hoodies]: ")
            size = input("Input your preferred size[Small/Medium/Large/XLarge]: ")
            if size == "xlarge" or size == "Xlarge":
                size = "XLarge"
            elif size == " " or size == "":
                size = None
            else:
                size = size.capitalize()
            color = input("Input your preferred color[Gold/Silver/Red/Blue]: ")
            keys = []
            key = "e"
            print("\tINPUT 'end' TO EXIT")
            while key != "end":
                key = input("Enter a keyword to search for: ")
                if key != "end" and encryp:
                    key = encrypt(key.capitalize())
                    if printMessages: print("\tEncrypted: {" + key + "}")
                keys.append(key.capitalize())
            live = input("Do you want this to be live[y/N]: ")
            start_time = time.time()
            if live == 'y':
                on = True
            else:
                on = False
            if on:
                while True:
                    item_target(item, size, keys, color)
                    time.sleep(time_delay)
            else:
                item_target(item, size, keys, color)
        elif cmd == "viewall":
            start_time = time.time()
            view_all()
        elif cmd == "items":
            start_time = time.time()
            maxItems = int(input("Enter the maximum amount of items: "))
        elif cmd == "price":
            start_time = time.time()
            buyerMaxPrice = int(input("Enter the maximum amount to spend: $"))
        elif cmd == "info":
            start_time = time.time()
            show_info()
        elif cmd == "cart":
            start_time = time.time()
            get_cart()
        elif cmd == "encrypt":
            start_time = time.time()
            if encryp:
                print("ENCRYPTION: OFF")
                encryp = False
            else:
                print("ENCRYPTION: ON\n\t{Messages are encrypted within the indexes}")
                encryp = True
        elif cmd == "decrypt":
            start_time = time.time()
            if decryp:
                print("DECRYPTION: OFF")
                decryp = False
            else:
                print("DECRYPTION: ON\n\t{Messages are decrypted within the indexes}")
                decryp = True
        elif cmd == "update":
            start_time = time.time()
            update_info()
        elif cmd == "clearmemory":
            start_time = time.time()
            clear_memory()
        elif cmd == "money":
            start_time = time.time()
            if moneyMode:
                print("MONEY PRIORITY: OFF")
                moneyMode = False
            else:
                print("MONEY PRIORITY: ON\n\t\t\t{$"+str(buyerMaxPrice)+"}")
                moneyMode = True
        elif cmd == "print":
            start_time = time.time()
            if printMessages:
                print("MESSAGE PRINTING: OFF")
                printMessages = False
            else:
                print("MESSAGE PRINTING: ON")
                printMessages = True
        elif cmd == "help":
            start_time = time.time()
            print("--------------------------------------------------------\nitem: Search for a specific item with "
                  "specific conditions\n\t\t{Type/Size/Color/Keywords}\nviewall: Find any new items regardless "
                  "of keywords\nupdate: Allow you to update the console information\n"
                  "items: Update the maximum items the bot can buy\n"
                  "price: Update the maximum price the box can buy\ncart: Display the currents items in cart"
                  "\nencrypt: Change keywords to predictive scrambled keywords\n"
                  "decrypt: Read all encrypted keywords normally on drop\n"
                  "money: Toggle the priority between items and price\n"
                  "info: Displays settings for the current bot\n"
                  "print: Displays more messages of the backend\n"
                  "quit: Closes the browser and exits the loop\n"
                  "--------------------------------------------------------")
        elif cmd == "quit":
            print("Closing Mozilla FireFox\n\tEnding processes...")
            time.sleep(1)
            driver.quit()
        else:
            print(cmd + ": is not a recognized command!")


"""
Main Logic Call with half of a second of rest between iterations,
    starting off turned off for debugging reasons. A False start
    makes this act like a shell, a True start and whatever the first
    command is, it will repeat
"""
bot_behavior(.5, False)