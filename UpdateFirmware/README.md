## For CI
### Get Arduino cli
```
cd UpdateFirmware
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
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