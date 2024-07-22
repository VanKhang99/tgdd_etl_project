from selenium.webdriver.common.by import By
import re

# IMPORT FILE FROM MY SOURCE
from helper_functions import check_element_html

class Product:
    def __init__(self, product_id, parent_tag, parent_image_link_class):
        self.parent_tag = parent_tag
        self.product_id = product_id
        
        self.find_data_product(parent_image_link_class)
    
    def find_data_product(self, parent_image_link_class):
        self.name = self.get_data("./a[@class='main-contain ']", 'data-name')
        self.brand = self.get_data("./a[@class='main-contain ']", 'data-brand')
        self.original_price = self.get_prices("./a[@class='main-contain ']//div[@class='box-p']/p[@class='price-old black']")
        self.current_price = self.get_prices("./a[@class='main-contain ']//strong[@class='price']")
        self.gift = self.get_gift("./a[@class='main-contain ']//p[@class='item-gift']")
        self.percent_discounted = self.get_percent_discounted("./a[@class='main-contain ']//div[@class='box-p']/span[@class='percent']")
        self.installment_zero_percent = self.get_installment_zero_percent("./a[@class='main-contain ']/div[@class='item-label']/span[@class='lb-tragop']")
        self.link = self.get_data("./a[@class='main-contain ']", 'href')
        self.image_link = self.get_image_link(parent_image_link_class)
        
    def get_data(self, xpath, attribute_name_to_get):
        tag_html = check_element_html(self.parent_tag, xpath)
        return tag_html.get_attribute(attribute_name_to_get)
    
    def get_prices(self, xpath):
        tag_html = check_element_html(self.parent_tag, xpath)
        return int(tag_html.text.replace('₫', '').replace('.', '')) if tag_html else None

    def get_gift(self, xpath):
        tag_html = check_element_html(self.parent_tag, xpath)
        return tag_html.text if tag_html else None

    def get_percent_discounted(self, xpath):
        tag_html = check_element_html(self.parent_tag, xpath)
        return int(re.findall(r'[\d]+', tag_html.text)[0]) if tag_html else None

    def get_installment_zero_percent(self, xpath):
        return 1 if check_element_html(self.parent_tag, xpath) else 0

    def get_image_link(self, parent_image_link_class):
        image_tag = self.parent_tag.find_element(By.XPATH, f"./a[@class='main-contain ']//div[@class='{parent_image_link_class}']/img")
        image_link = image_tag.get_attribute('data-src') or image_tag.get_attribute('src')
        return image_link.replace(' ', '%20') if image_link else None
