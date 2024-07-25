from selenium.webdriver.common.by import By
import re

# IMPORT FILE FROM MY SOURCE
from utils.helper_functions import tranform_int_float, helper_split_str_data
from utils.constants import REGEX_ONLY_DIGITS, REGEX_DIGITS_BEFORE_MM, REGEX_DIGITS_LAPTOP_SCREEN_HZ

class Laptop:
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
        
        self.handle_specifications_tags(specification_tags)
        self.handle_ram_capacity_tags(ram_capacity_tags)
        
    def handle_screen(self, data_screen):
        data_screen = data_screen.split(', ')
        
        self.screen_inch = tranform_int_float(data_screen[0], 0, True)
        # float(re.findall(REGEX_ONLY_DIGITS, data_screen[0])[0])
        self.screen_resolution = data_screen[1]
        
        if len(data_screen) > 2 and bool(re.search(REGEX_DIGITS_LAPTOP_SCREEN_HZ, data_screen[2])):
            self.screen_frequency_Hz = int(data_screen[2].replace('Hz', ''))
    
    def handle_cpu(self, data_cpu):
        data_cpu_splited = data_cpu.split(', ') 
        self.core = data_cpu_splited[0]      
        
        if len(data_cpu_splited) == 2:
            if 'Apple' in self.core:
                self.core_speed =  data_cpu_splited[1]
        elif len(data_cpu_splited) > 2:
            self.core_gen = data_cpu_splited[1]
            self.core_speed = data_cpu_splited[2]
    
    def handle_ram_capacity_tags(self, ram_capacity_tags):
        ram, capacity = [tag.text for tag in ram_capacity_tags]
        self.ram = tranform_int_float(ram, 0)
        self.capacity = tranform_int_float(capacity, 0)
        
                  
    def handle_specifications_tags(self, specification_tags):
        screens, cpu, card, battery, weight = [helper_split_str_data(tag.text, ':', 1) for tag in specification_tags]
        self.handle_screen(screens)
        self.card_screen = card
        self.handle_cpu(cpu)
        self.battery = battery
        self.weight_kg = float(weight.replace(' kg', ''))           
                              
class Phone:
    def __init__(self, product_id, specification_tags, screen_tags):
        self.product_id = product_id
        self.screen_inch = None
        self.secondary_screen_inch = None
        self.screen_resolution = None
        self.chip = None
        self.ram = None
        self.capacity = None
        self.back_camera = None
        self.front_camera = None
        self.battery = None
        self.charge_W = None

        self.handle_specifications_tags(specification_tags)
        self.handle_screen_tags(screen_tags)
        
    def handle_screen_tags(self, screen_tags):
        for tag in screen_tags:
            content = tag.text
            
            # Since two data screen of phone can be reverse, we have to check
            if '"' in content:
                number_screen = re.findall(REGEX_ONLY_DIGITS, content)
                self.screen_inch = float(number_screen[0])
                if len(number_screen) > 1:
                    # Some phone have two screens
                    self.secondary_screen_inch = float(number_screen[1])
            else:
                self.screen_resolution = content.strip()
    
    def handle_specifications_tags(self, specification_tags):
        chip, ram, capacity, back_camera, front_camera, battery_charge = [tag.text for tag in specification_tags]
        
        self.chip = chip.strip()
        self.ram = tranform_int_float(ram, 0)
        self.capacity = tranform_int_float(capacity, 0)
        self.back_camera = helper_split_str_data(back_camera, ':', 1)
        self.front_camera = helper_split_str_data(front_camera, ':', 1)

        battery, charge_W = battery_charge.split(', ')
        self.battery = battery.strip()
        self.charge_W = tranform_int_float(charge_W, 0)
        
class Tablet:
    def __init__(self, product_id, specification_tags, screen_tags):
        self.product_id = product_id
        self.screen_inch = None
        self.screen_type = None
        self.chip = None
        self.ram = None
        self.capacity = None
        self.features_supported = None
        self.battery = None
        self.charge_W = None
        
        self.handle_specifications_tags(specification_tags)
        self.handle_screen_tags(screen_tags)
        
    def handle_screen_tags(self, screen_tags):
        screen_type, screen_inch = [tag.text for tag in screen_tags]        
        self.screen_inch =  float(screen_inch.replace('"', ''))
        self.screen_type = screen_type.strip()
    
    def handle_specifications_tags(self, specification_tags):
        data = [tag.text for tag in specification_tags]
        
        self.chip = data[0].strip()
        self.ram = tranform_int_float(data[1], 0)
        self.capacity = tranform_int_float(data[2], 0)

        if len(data) > 4:
            self.features_supported = data[3].strip()
            self.helper_battery_charge(data[4])
        else:
            self.helper_battery_charge(data[3])
        
    def helper_battery_charge(self, data):
        battery, charge_W = data.split(', ')
        
        self.battery = battery.strip()
        self.charge_W = tranform_int_float(charge_W, 0)
       
class SmartWatch:
    def __init__(self, product_id, specification_tags, name_tag):
        self.product_id = product_id
        self.face_diameter_mm = None
        self.screen = None
        self.health_features_support = None
        self.exercise_modes_support = None
        self.notify_apps_support = None
        
        self.handle_name_tag(name_tag)
        self.handle_specification_tags(specification_tags)
        
    def handle_name_tag(self, name_tag):
        # Since use check_element_html with arguments one_tag=False returns a list, so use index[0]
        title = name_tag[0].text.strip()
        
        face_diameter = re.findall(REGEX_DIGITS_BEFORE_MM, title)
        if len(face_diameter) > 0:
            self.face_diameter_mm = float(face_diameter[0])
            
    def handle_specification_tags(self, specification_tags):
        data = [tag.text for tag in specification_tags]
            
        self.screen = helper_split_str_data(data[0], ':', 1)
        self.health_features_support = helper_split_str_data(data[1], ':', 1)

        if len(data) == 3:
            self.notify_apps_support = helper_split_str_data(data[2], ':', 1)
            
        if len(data) == 4:
            self.exercise_modes_support = helper_split_str_data(data[2], ':', 1)
            self.notify_apps_support = helper_split_str_data(data[3], ':', 1)
 
            
