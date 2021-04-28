## For CI
### Get Arduino cli
```
cd UpdateFirmware
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
```
#### Verify installation
```
arduino-cli version
```
#### Update board index
```
arduino-cli core update-index
```
#### Install third-party board support(ESP8266 in our case)
```
sudo nano /home/{username}/.arduino15/arduino-cli.yaml

board_manager:
  additional_urls:
    - https://arduino.esp8266.com/stable/package_esp8266com_index.json
```
#### Update board index again
```
arduino-cli core update-index
```
#### Check for `esp8266` core
```
arduino-cli core search esp8266
```
#### Install core
```
arduino-cli core install esp8266:esp8266
```
#### Check for `esp8266` boards
```
arduino-cli board listall

Board Name                          FQBN
DOIT ESP-Mx DevKit (ESP8285)        esp8266:esp8266:espmxdevkit                
Digistump Oak                       esp8266:esp8266:oak                        
ESPDuino (ESP-13 Module)            esp8266:esp8266:espduino                   
ESPectro Core                       esp8266:esp8266:espectro                   
ESPino (ESP-12 Module)              esp8266:esp8266:espino                     
ESPresso Lite 1.0                   esp8266:esp8266:espresso_lite_v1           
ESPresso Lite 2.0                   esp8266:esp8266:espresso_lite_v2           
Generic ESP8266 Module              esp8266:esp8266:generic                    
Generic ESP8285 Module              esp8266:esp8266:esp8285                    
ITEAD Sonoff                        esp8266:esp8266:sonoff                     
Invent One                          esp8266:esp8266:inventone                  
LOLIN(WEMOS) D1 R2 & mini           esp8266:esp8266:d1_mini                    
LOLIN(WEMOS) D1 mini Lite           esp8266:esp8266:d1_mini_lite               
LOLIN(WEMOS) D1 mini Pro            esp8266:esp8266:d1_mini_pro                
LilyPad Arduino                     arduino:avr:lilypad                        
LilyPad Arduino USB                 arduino:avr:LilyPadUSB                     
Linino One                          arduino:avr:one                            
NodeMCU 0.9 (ESP-12 Module)         esp8266:esp8266:nodemcu                    
NodeMCU 1.0 (ESP-12E Module)        esp8266:esp8266:nodemcuv2                  
Olimex MOD-WIFI-ESP8266(-DEV)       esp8266:esp8266:modwifi                    
Phoenix 1.0                         esp8266:esp8266:phoenix_v1                 
Phoenix 2.0                         esp8266:esp8266:phoenix_v2                 
Schirmilabs Eduino WiFi             esp8266:esp8266:eduinowifi                 
Seeed Wio Link                      esp8266:esp8266:wiolink                    
SparkFun Blynk Board                esp8266:esp8266:blynk                      
SparkFun ESP8266 Thing              esp8266:esp8266:thing                      
SparkFun ESP8266 Thing Dev          esp8266:esp8266:thingdev                   
SweetPea ESP-210                    esp8266:esp8266:esp210                     
ThaiEasyElec's ESPino               esp8266:esp8266:espinotee                  
WeMos D1 R1                         esp8266:esp8266:d1                         
WiFiduino                           esp8266:esp8266:wifiduino                  
WifInfo                             esp8266:esp8266:wifinfo                    
XinaBox CW01                        esp8266:esp8266:cw01     
```
### Install library dependencies
#### Update library index
```
arduino-cli lib update-index
```
#### Search for library
```
arduino-cli lib search ssd1306
```
#### Pick a library and install with
```
arduino-cli lib install "Adafruit SSD1306"
```
#### Confirm it with
```
arduino-cli lib list
```
#### Uninstalling lib
```
arduino-cli lib uninstall "Adafruit SSD1306"
```

## Docs
### Managing arduino libs and board
Filename: **arduino_manage.py**

Usage example:
```
install = ArduinoManage()
install.search_lib("Adafruit NeoPixel")
install.search_board("esp8266")
```

### Update firmware
Filename: **update.py**

Usage example:
```
esp = ESPOptions("esp_test", "192.168.0.136", "esp8266:esp8266:nodemcuv2")
build_result = esp.build()
esp.check_external_libs()
if build_result is True:
    print("Build Successfully Completed")
else:
    print(build_result)
update_result = esp.update()
if update_result == 0:
    print("Upgrade Successfully Completed")
else:
    print("Update failed!")
```