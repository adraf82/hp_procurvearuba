from hp_procurvearuba import HP
import yaml

with open('devices.yml', 'r') as f:
    device_data = yaml.safe_load(f)
    device_data = device_data.pop('devices')
    device_data = device_data

def main():
    for device in device_data:
        hp_obj = HP(**device)
        hp_obj.find_switch_serial_number()
        hp_obj.disconnect()

if __name__=='__main__':
    main()

