from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import re

def check_element_html(parent_tag, xpath, one_tag=True):
    try:
        return parent_tag.find_element(By.XPATH, xpath) if one_tag else parent_tag.find_elements(By.XPATH, xpath)
    except NoSuchElementException:
        return None

def handle_classes_base_on_url(url):
    classes_base_on_url = dict()

    def helper_assign_attribute(**kwargs):
        classes_base_on_url['parent_tag_class'] = kwargs['parent_tag_class']
        classes_base_on_url['parent_image_link_class'] = kwargs['parent_image_link_class']
        
    if 'laptop' in url:
        helper_assign_attribute(parent_tag_class =' item  __cate_44', parent_image_link_class='item-img item-img_44')
    elif 'dtdd' in url:
        helper_assign_attribute(parent_tag_class =' item ajaxed __cate_42', parent_image_link_class='item-img item-img_42')
    elif 'may-tinh-bang' in url:
        helper_assign_attribute(parent_tag_class =' item ajaxed __cate_522', parent_image_link_class='item-img item-img_522')

    return classes_base_on_url

def tranform_int(regex, content, index):
    return int(re.findall(regex, content)[index])  