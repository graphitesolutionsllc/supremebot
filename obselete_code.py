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

