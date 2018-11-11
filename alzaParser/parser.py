# -*- coding: utf-8 -*-
import requests
from lxml import html, etree


class Category():
    name = ""
    link = ""

    def __init__(self, name, link):
        self.name = name
        self.link = link

alza_root = 'https://www.alza.cz'

def write(text):
    f = open('report.txt', "a+", encoding="utf-8")
    f.write(text)
    f.close()


def parse_product_page(tree, categrory, page):

    product_list = tree.xpath("//div[@id='boxes']/div[contains(@class,'browsingitem')]")
    print(len(product_list))

    record = ""
    separator = '|'
    for product in product_list:
        prod_name = product.xpath(".//a[contains(@class, 'name')]/text()")[0]
        prod_link = product.xpath(".//a[contains(@class, 'name')]/@href")[0]

        try:
            prod_price = product.xpath(".//span[@class='c2']/text()")[0]
        except IndexError:
            prod_price = 'not available'
        prod_price = prod_price.replace(u'\xa0', ' ')
        record += categrory + \
                  separator + \
                  prod_name + \
                  separator + \
                  str(page) + \
                  separator + \
                  prod_price + \
                  separator + \
                  alza_root + prod_link + '\n'
        print(prod_name)
        print(prod_link)
        print(prod_price)
    write(record)

    next_button = tree.xpath("//div[@id='pagerbottom']//a[contains(@class,'next')]")
    if len(next_button) == 0:
        print('Last page on for the category: '+categrory)
        return -1



def get_prod_group_def():
    r = requests.get("https://www.alza.cz/wearables/18855068.htm")
    print('Status code: ' + str(r.status_code))
    tree = html.fromstring(r.text.encode('UTF-8'))

    cat_root = tree.xpath("//div[@id='content0']//div[@class='catlistContainer subCatIncluded']")[0]
    cat_list = cat_root.xpath(".//a[not(@id)]")
    print(len(cat_list))

    cat_list_o = []
    for cat in cat_list:
        cat_name = cat.xpath(".//span/span/span/text()")[0]
        cat_link = cat.xpath("./@href")[0]
        print(cat_link)
        cat_o = Category(cat_name, cat_link)
        cat_list_o.append(cat_o)

    return cat_list_o


categories = get_prod_group_def()

for cat in categories:

    page = 1
    result = 0

    while result != -1:
        link = alza_root + cat.link
        r = requests.get(link)
        print('Status code: ' + str(r.status_code))
        # need to check if there was any kind of page redirection
        try:
            location = (r.history[0]).headers['Location']
            # exist location -> there was a redirection
            if link != location:
                link = location
                link = link.replace('.htm', '-p%d.htm')
                link = link % (page)
        except IndexError:
            # no redirection
            link = link.replace('.htm', '-p%d.htm')
            link = link % (page)

        print(link)

        new_r = requests.get(link)
        tree = html.fromstring(new_r.text.encode('UTF-8'))
        result = parse_product_page(tree, cat.name, page)
        page += 1
