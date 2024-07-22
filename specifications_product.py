from selenium.webdriver.common.by import By
import re

# IMPORT FILE FROM MY SOURCE
from helper_functions import helper_tranform_int

class LaptopSpecifications:
    def __init__(self, product_id, specification_tags, ram_capacity_tags):
        self.product_id = product_id
        self.screen_inch = None
        self.screen_resolution = None
        self.screen_frequency_Hz = None
        self.core = None
        self.core_gen = None
        self.core_speed = None
        self.card_screen = None
        self.battery = None
        self.weight_kg = None
        self.ram = None
        self.capacity = None
        
        self.get_ram_capacity(ram_capacity_tags)
        self.get_remaining_specifications(specification_tags)
        
    def handle_data_screen(self, data_screen):
        data_screen = data_screen.split(', ')
        
        self.screen_inch = float(data_screen[0].replace('"', ''))
        self.screen_resolution = data_screen[1]
        
        if len(data_screen) > 2 and bool(re.search(r'[\d]+Hz', data_screen[2])):
            self.screen_frequency_Hz = int(data_screen[2].replace('Hz', ''))
    
    def handle_data_cpu(self, data_cpu):
        data_cpu_splited = data_cpu.split(', ') 
        self.core = data_cpu_splited[0]      
        
        if len(data_cpu_splited) == 2:
            if 'Apple' in self.core:
                self.core_speed =  data_cpu_splited[1]
        elif len(data_cpu_splited) > 2:
            self.core_gen = data_cpu_splited[1]
            self.core_speed = data_cpu_splited[2]
    
    def get_ram_capacity(self, ram_capacity_tags):
        for tag in ram_capacity_tags:
            if 'RAM' in tag.text:
                self.ram = helper_tranform_int('[\d]+', tag.text, 0)
            elif 'SSD' or 'HDD' in tag.text:
                self.capacity = helper_tranform_int('[\d]+', tag.text, 0)
                  
    def get_remaining_specifications(self, specification_tags):
        for tag in specification_tags:
            specification_values = tag.text.split(':')[1].strip()
            
            if 'Màn hình' in tag.text:
                self.handle_data_screen(specification_values)
            elif 'Card' in tag.text:
                self.card_screen = specification_values
            elif 'CPU' in tag.text:
                self.handle_data_cpu(specification_values)
            elif 'Pin' in tag.text:
                self.battery = specification_values
            elif 'Khối lượng' in tag.text:
                self.weight_kg = float(specification_values.replace(' kg', ''))
                                   
class PhoneSpecifications:
    def __init__(self, product_id, screen_tags, specification_tags):
        self.product_id = product_id
        self.main_screen_inch = None
        self.secondary_screen_inch = None
        self.screen_resolution = None
        self.chip = None
        self.ram = None
        self.capacity = None
        self.back_camera = None
        self.front_camera = None
        self.battery_mAh = None
        self.charge_W = None

        self.get_data_screen(screen_tags)
        self.get_remaining_specifications(specification_tags)
        
    def get_data_screen(self, screen_tags):
        for tag in screen_tags:
            content = tag.text
        
            if '"' in content:
                data_screen = re.findall(r'[\d.]+', content)
                self.main_screen_inch = float(data_screen[0])
                
                if len(data_screen) > 1:
                    self.secondary_screen_inch = float(data_screen[1])
            else:
                self.screen_resolution = content.strip()
    
    def get_remaining_specifications(self, specification_tags):
        for tag in specification_tags:
            content = tag.text
            
            if 'Chip' in content:
                self.chip = content.strip()
            elif 'RAM' in content:
                self.ram = helper_tranform_int('[\d]+', tag.text, 0)
            elif 'Dung lượng' in content:
                self.capacity = helper_tranform_int('[\d]+', tag.text, 0)
            elif 'Camera sau' in content:
                self.back_camera = content.split(':')[1].strip()
            elif 'Camera trước' in content:
                self.front_camera = content.split(':')[1].strip()
            elif 'Pin' or 'Sạc' in content:
                data = content.split(', ')
                self.battery_mAh = helper_tranform_int('[\d]+', data[0], 0)
                self.charge_W = helper_tranform_int('[\d]+', data[1], 0)