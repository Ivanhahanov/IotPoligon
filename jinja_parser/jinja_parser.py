from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('arduino_templates'))
template = env.get_template('example.ino')
output_render = template.render(ssid='your_ssid', password='your_pass', ip_mqtt_server='your_ip', mqtt_user='mqttuser',
                                mqtt_password='mqttpass')

with open('parsed_example.ino', 'w') as pe:
    pe.write(output_render)
