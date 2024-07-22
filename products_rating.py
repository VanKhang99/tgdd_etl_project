from selenium.webdriver.common.by import By

# IMPORT FILE FROM MY SOURCE
from helper_functions import check_element_html

class ProductsRating:
    def __init__(self, product_id, parent_tag):
        self.parent_tag = parent_tag
        self.product_id = product_id
        
        self.find_data_rating()
    
    def find_data_rating(self):
        avg_stars = None
        number_reviewed = None
        parent_tags_star = check_element_html(self.parent_tag, ".//div[@class='item-rating']")
        
        if parent_tags_star is not None:
            # Calculate avg_stars data
            star_tag_list = parent_tags_star.find_elements(By.XPATH, "./p//i[@class='icon-star']")
            star_half_tag = check_element_html(parent_tags_star, "./p//i[@class='icon-star-half']")
            # Check star of product have half star or not
            avg_stars = len(star_tag_list) + 0.5 if star_half_tag is not None else len(star_tag_list)
            
            # Find number_reviewed data
            number_reviewed = int(parent_tags_star.find_element(By.XPATH, ".//p[@class='item-rating-total']").text)

        self.avg_stars = avg_stars
        self.number_reviewed = number_reviewed
         