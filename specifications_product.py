from selenium.webdriver.common.by import By
import re

# IMPORT FILE FROM MY SOURCE
from constants import RAMS, CAPACITIES

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
        self.ram_id = None
        self.capacity_id = None
        
        self.find_data_specifications(specification_tags, ram_capacity_tags)
        
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
                  
    def find_data_specifications(self, specification_tags, ram_capacity_tags):
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
                
        for tag in ram_capacity_tags:
            if 'RAM' in tag.text:
                self.ram = int(re.findall(r'[\d]+', tag.text)[0])
            elif 'SSD' or 'HDD' in tag.text:
                self.capacity_id = int(re.findall(r'[\d]+', tag.text)[0])
                
