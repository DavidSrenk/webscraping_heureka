# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 20:42:28 2019

@author: Standard
"""
import re
import pandas as pd

from copy import deepcopy

from requests import get
url = 'https://notebooky.heureka.cz/apple-macbook-pro-muhn2cz-a/'
response = get(url)
print(response.text[:500])

from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

product_nazev = html_soup.find('div', class_="item js-public-product-id")
print(type(product_nazev))
print(len(product_nazev))
nazev = product_nazev.h1.text
popis = html_soup.find('p', class_='desc').span.text


#___________________________offers

product_container = html_soup.find_all('div', class_= "shoppr verified ")
print(type(product_container))
print(len(product_container))



# 1 produkt
first_product = product_container[0]
first_seller = first_product.find('p', class_='shop-name').a.text
first_url = first_product.find('a', class_='flat-button flat-button--blue flat-button--offer')
first_url = first_url.get('href')
first_delivery = first_product.find('span', class_="dotted").text
first_price = first_product.find('a', class_='pricen').text
first_posting = first_product.find('span', class_="delivery-free ico dotted").text


'''
# metoda na posting dve varianty zdarma/paied
def metod_posting(product):
    if product.find('span', class_="delivery-free ico dotted") is None:
        te = product.find('span', class_ = "pricen").text
    else:
        te = product.find('span', class_="delivery-free ico dotted").text
    return te
 #(product) = metod_posting(product_container[0]) #volani   
'''
 
 # tahle je snad ok
 # metoda na posting dve varianty zdarma/paied
def metod_posting(product):
    if product.find('span', class_="delivery-free ico dotted") is not None:
        te = product.find('span', class_="delivery-free ico dotted").text
        #te = 'doprava zdarma'
    else:
        if product.find('span', class_ = "pricen") is not None:
            te = product.find('span', class_ = "pricen").text
        else:
            te = 'doprava neznama'
        return te
 #(product) = metod_posting(product_container[0]) #volani   
 
 
    
#__________________________________________________________________________________________
    

#__________________________________________________________________________________________________
# list for scraped data
sellers = []
urls = []
deliverys = []
prices = []
postings = []

for container in product_container:
    if container.find('span', class_="dotted").text is not None and '''container.find('span', class_="delivery-free ico dotted") is not None''':
        
    #seller
        seller = container.find('p', class_='shop-name').a.text
        sellers.append(seller)
        
        #url opravit
        url = container.find('a', class_='flat-button flat-button--blue flat-button--offer')
        url = url.get('href')
        urls.append(url)
        
        
        #delivery
        delivery = container.find('span', class_='dotted').text
        deliverys.append(delivery)
        
        # price
        price = container.find('a', class_='pricen').text
        prices.append(price)
        '''
        #posting
        posting = container.find('span', class_="delivery-free ico dotted").text
        postings.append(posting)
        '''
        (posting) = metod_posting(container)
        postings.append(posting)
            
sellers = [s.split() for s in sellers]

pricer = [re.findall('\d+', p) for p in prices]
pricer = [''.join(map(str, p)) for p in pricer]
pricer = [int(i) for i in pricer]


# vytvorim dataFrame
database = pd.DataFrame({
'seller': sellers,
'reference': urls,
'delivery' : deliverys,
'price' : prices,
'posting' : postings, 
'int_price' : pricer,       
})
print(database.info())

#zmena v kodu    