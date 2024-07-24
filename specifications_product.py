from selenium.webdriver.common.by import By
import re

# IMPORT FILE FROM MY SOURCE
from helper_functions import tranform_int
from constants import REGEX_ONLY_DIGITS

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
        
        self.get_specifications(specification_tags)
        self.get_ram_capacity(ram_capacity_tags)
        
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
        ram, capacity = [tag.text for tag in ram_capacity_tags]
        self.ram = tranform_int(REGEX_ONLY_DIGITS, ram, 0)
        self.capacity = tranform_int(REGEX_ONLY_DIGITS, capacity, 0)
        
                  
    def get_specifications(self, specification_tags):
        screens, cpu, card, battery, weight = [tag.text.split(':')[1].strip() for tag in specification_tags]
        self.handle_data_screen(screens)
        self.card_screen = card
        self.handle_data_cpu(cpu)
        self.battery = battery
        self.weight_kg = float(weight.replace(' kg', ''))           
                              
class Phone:
    def __init__(self, product_id, specification_tags, screen_tags):
        self.product_id = product_id
        self.main_screen_inch = None
        self.secondary_screen_inch = None
        self.screen_resolution = None
        self.chip = None
        self.ram = None
        self.capacity = None
        self.back_camera = None
        self.front_camera = None
        self.battery = None
        self.charge_W = None

        self.get_specifications(specification_tags)
        self.get_data_screen(screen_tags)
        
    def get_data_screen(self, screen_tags):
        data_screens, resolution = [tag.text for tag in screen_tags]
   
        number_screen = re.findall(REGEX_ONLY_DIGITS, data_screens)
        self.main_screen_inch = float(number_screen[0])
        if len(number_screen) > 1:
            self.secondary_screen_inch = float(number_screen[1])
        
        self.screen_resolution = resolution.strip()
    
    def get_specifications(self, specification_tags):
        chip, ram, capacity, back_camera, front_camera, battery_charge = [tag.text for tag in specification_tags]
        
        self.chip = chip.strip()
        self.ram = tranform_int(REGEX_ONLY_DIGITS, ram, 0)
        self.capacity = tranform_int(REGEX_ONLY_DIGITS, capacity, 0)
        self.back_camera = back_camera.split(':')[1].strip()
        self.front_camera = front_camera.split(':')[1].strip()
        
        battery, charge_W = battery_charge.split(', ')
        self.battery = battery.strip()
        self.charge_W = tranform_int(REGEX_ONLY_DIGITS, charge_W, 0)
        
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
        
        self.get_specifications(specification_tags)
        self.get_data_screen(screen_tags)
        
    def get_data_screen(self, screen_tags):
        screen_type, screen_inch = [tag.text for tag in screen_tags]        
        self.screen_inch =  float(screen_inch.replace('"', ''))
        self.screen_type = screen_type.strip()
    
    def get_specifications(self, specification_tags):
        data = [tag.text for tag in specification_tags]
        
        self.chip = data[0].strip()
        self.ram = int(re.findall(r'[\d]+', data[1])[0])
        self.capacity = int(re.findall(r'[\d]+', data[2])[0])

        if len(data) > 4:
            self.features_supported = data[3].strip()
            
            self.helper_battery_charge(data[4])
        else:
            self.helper_battery_charge(data[3])
        
    def helper_battery_charge(self, data):
        battery, charge_W = data.split(', ')
        self.battery = battery.strip()
        self.charge_W = int(re.findall(r'[\d]+', charge_W)[0])
       
class Watch:
    def __init__(self, product_id, specification_tags):
        pass