from selenium.webdriver.common.by import By

# IMPORT FILE FROM MY SOURCE
# from helper_functions import check_element_html

class ProductsGroup:
    def __init__(self, product_id, parent_tag):
        self.product_id = product_id
        self.ids_merged = parent_tag.get_attribute('data-lstarranged').strip()
        self.blocks_showed = self.find_blocks_showed(parent_tag)
        
    def find_blocks_showed(self, parent_tag):
        childs_tag = parent_tag.find_elements(By.XPATH, "./ul/li")
        return ','.join(c.text for c in childs_tag)