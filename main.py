# IMPORT FROM PACKAGES
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

# IMPORT FILES
from driver_selenium import run_driver_selenium
from utils.helper_functions import check_element_html, handle_classes_base_on_url

# CLASSES
from products import Product
from products_rating import ProductsRating
from products_group import ProductsGroup
from products_specifications import Laptop, Phone, Tablet, SmartWatch

urls = [
    "https://www.thegioididong.com/laptop-apple-macbook#c=44&m=203,118,128,133,119,122,120&o=17&pi=15",
    # "https://www.thegioididong.com/dtdd-vivo#c=42&m=2,80,1971,2235,2236,36747,1541,2283,17201&o=17&pi=7",
    # "https://www.thegioididong.com/may-tinh-bang#c=522&m=1028,1101,29147,35263,2150,37840,1226,5203&o=17&pi=2",
    # "https://www.thegioididong.com/dong-ho-thong-minh-xiaomi#c=7077&m=17197,17188,17189,19546,17190,20482,18653,18727,36914,19817,18728,17196,36984&o=17&pi=6"
]

def get_specifications_base_on_url(args):
    url, product_id, parent_tag, xpaths = args.values()
    
    tag_utility = check_element_html(parent_tag, xpaths[0], False)
    other_tag_specification = check_element_html(parent_tag, xpaths[1], False)
    if tag_utility is None or other_tag_specification is None:
        raise ValueError('No tags found. Something went wrong with your xpaths, please check it.')

    if 'laptop' in url:
        return Laptop(product_id, tag_utility, other_tag_specification)
    elif 'dtdd' in url:
        return Phone(product_id, tag_utility, other_tag_specification)
    elif 'may-tinh-bang' in url:
        return Tablet(product_id, tag_utility, other_tag_specification)
    elif 'dong-ho-thong-minh' in url:
        return SmartWatch(product_id, tag_utility, other_tag_specification)

def main():
    data = []
    for url in urls:
        # RUN DRIVER SELENIUM TO GET HTMLS OF URL
        driver = run_driver_selenium(url)
        
        # HADNLE CLASSES BASE ON TYPE OF PRODUCT THAT WANT TO GET
        classes_base_on_url = handle_classes_base_on_url(url)
        
        # LISTS HTML TAGS TO GET ALL ANOTHER DATA
        parent_tags_list = check_element_html(driver, f"//li[@class='{classes_base_on_url['parent_tag_class']}']", False)
        if parent_tags_list is None:
            raise ValueError('No tags found. Something went wrong with your xpath "parent_tags_list", please check it.')
        
        for parent_tag in parent_tags_list:
            ### Find tags for multiple tables ###
            product_id = parent_tag.get_attribute('data-id')
            
            ### Find data of table "PRODUCTS" ###
            # product = Product(product_id, parent_tag, classes_base_on_url['parent_image_link_class'])
            # print(product.__dict__)
            
            ### Find data of table "PRODUCTS_RATING" ###
            # product_rating = ProductsRating(product_id, parent_tag)
            # print(product_rating.__dict__)
            
            ### Find data of table "PRODUCTS_GROUPS" ###
            # group_tag = check_element_html(parent_tag, "./a[@class='main-contain ']//div[@class='prods-group']")
            # if group_tag is not None:
            #     products_group = ProductsGroup(product_id, group_tag)
            #     print(products_group.__dict__)
                
            ### Find data of tables 
            # "LATOP_SPECIFICATIONS, 
            # PHONE_SPECIFICATIONS, 
            # TABLET_SPECIFICATIONS, 
            # SMARTWATCH_SPECIFICATIONS,
            # WATCH_SPECIFICATIONS" ###
            
            xpath_tag_utility = ".//div[@class='utility']//p"
            xpath_other_tag_specification = "./a[@class='main-contain ']//div[@class='item-compare gray-bg']//span"
            if 'dong-ho-' in url:
                xpath_other_tag_specification = "./a[@class='main-contain ']//h3"
                
            specifications =  get_specifications_base_on_url({
                'url': url,
                'product_id': product_id,
                'parent_tag': parent_tag,
                'xpaths': [xpath_tag_utility, xpath_other_tag_specification]
            })
            
            data.append([
                specifications.product_id,
                specifications.screen_inch,
                specifications.screen_resolution,
                specifications.screen_frequency_Hz,
                specifications.card_screen,
                specifications.core,
                specifications.core_gen,
                specifications.core_speed,
                specifications.ram,
                specifications.capacity,
                specifications.battery,
                specifications.weight_kg])
            
            # print(specifications.__dict__)
            # print(f'############ {i} ############')
            # i += 1
        
            
        driver.quit()
        print('############ NEXT URL ############')
        print('############ NEXT URL ############')
        print('############ NEXT URL ############')
        
    return data
            
data = main()
df = pd.DataFrame(data, columns=[
    'product_id',
    'screen_inch',
    'screen_resolution',
    'screen_frequency_Hz',
    'card_screen',
    'core',
    'core_gen',
    'core_speed',
    'ram',
    'capacity',
    'battery',
    'weight_kg',])

df.to_csv('./csv/laptops2.csv', index=False)
# print(list_products)