# smart-switcher
This git-project is a software side of a hardware IoT project that gets fixed on circuit breakers and 
switches them remotely and get information from them using sensor data.  
Project consists of ESP32 code using Arduino IDE, Flask website that a client uses to control circuit 
breaker and a side that deals with communicationg with the microcontroller.

# how-to
import as pycharm project, requirements.txt should do the rest
# Data/data.json
to read it you can use this command:
`awk '{gsub(/\\n/,"\n")}1' data.json | awk '{gsub(/\\/,"")}1'`
