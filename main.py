# IMPORT FROM PACKAGES
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


# IMPORT FILES
from driver_selenium import run_driver_selenium
from helper_functions import check_element_html, handle_classes_base_on_url

# CLASSES
from products import Product
from products_rating import ProductsRating
from products_group import ProductsGroup
from specifications_product import Laptop, Phone, Tablet

urls = [
    # "https://www.thegioididong.com/may-tinh-bang-samsung"
    # "https://www.thegioididong.com/dtdd-samsung"
    # "https://www.thegioididong.com/dtdd-apple-iphone"
    "https://www.thegioididong.com/laptop-asus"
    # "https://www.thegioididong.com/laptop-apple-macbook#c=44&m=203&o=17&pi=1",
    # "https://www.thegioididong.com/dtdd-samsung#c=42&m=2&o=17&pi=1",
    # "https://www.thegioididong.com/may-tinh-bang-apple-ipad#c=522&m=1028&o=17&pi=1"
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

def main():
    for url in urls:
        # RUN DRIVER SELENIUM TO GET HTMLS OF URL
        driver = run_driver_selenium(url)
        
        # HADNLE CLASSES BASE ON TYPE OF PRODUCT THAT WANT TO GET
        classes_base_on_url = handle_classes_base_on_url(url)
        
        # LISTS HTML TAGS TO GET ALL ANOTHER DATA
        parent_tags_list = check_element_html(driver, f"//li[@class='{classes_base_on_url['parent_tag_class']}']", False)
        if parent_tags_list is None:
            raise ValueError('No tags found. Something went wrong with your xpath "parent_tags_list", please check it.')
        
        i = 0
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
                
            ## Find data of tables "LATOP_SPECIFICATIONS, PHONE_SPECIFICATIONS, TABLET_SPECIFICATIONS" ###
            specifications =  get_specifications_base_on_url({
                'url': url,
                'product_id': product_id,
                'parent_tag': parent_tag,
                'xpaths': [
                    ".//div[@class='utility']//p",
                    "./a[@class='main-contain ']//div[@class='item-compare gray-bg']//span"
                ]
            })
            
            print(specifications.__dict__)
            print(f'############ {i} ############')
            i += 1
            
        driver.quit()
        print('############ NEXT URL ############')
        print('############ NEXT URL ############')
        print('############ NEXT URL ############')
            
main()
# print(list_products)