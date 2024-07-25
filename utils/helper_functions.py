from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import re
import math

from constants import REGEX_ONLY_DIGITS

def tranform_int_float(content, index, to_float=False):
    value = float(re.findall(REGEX_ONLY_DIGITS, content)[index])
    rounded_down = math.floor(value)
    return value if to_float == True else int(rounded_down) 

def helper_split_str_data(data, by, index):
    return data.split(by)[index].strip()

def check_element_html(parent_tag, xpath, one_tag=True):
    try:
        return parent_tag.find_element(By.XPATH, xpath) if one_tag else parent_tag.find_elements(By.XPATH, xpath)
    except NoSuchElementException:
        return None

def handle_classes_base_on_url(url):
    classes_base_on_url = {}

    def helper_assign_attribute(**kwargs):
        classes_base_on_url['parent_tag_class'] = kwargs['parent_tag_class']
        classes_base_on_url['parent_image_link_class'] = kwargs['parent_image_link_class']
        
    if 'laptop' in url:
        helper_assign_attribute(parent_tag_class =' item  __cate_44', parent_image_link_class='item-img item-img_44')
    elif 'dtdd' in url:
        helper_assign_attribute(parent_tag_class =' item ajaxed __cate_42', parent_image_link_class='item-img item-img_42')
    elif 'may-tinh-bang' in url:
        helper_assign_attribute(parent_tag_class =' item ajaxed __cate_522', parent_image_link_class='item-img item-img_522')
    elif 'dong-ho-deo-tay' in url:
        helper_assign_attribute(parent_tag_class =' item  __cate_7264', parent_image_link_class='item-img item-img_7264')
    elif 'dong-ho-thong-minh' in url:
        helper_assign_attribute(parent_tag_class =' item  __cate_7077', parent_image_link_class='item-img item-img_7077')

    return classes_base_on_url

