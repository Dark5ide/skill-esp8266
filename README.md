## ESP8266 skill
Communicate with an ESP8266 in the context of home automation.

## Description 
This Skill has been created for the makers and hackers who want to build their own home automation system based on ESP8266. The purpose of this Skill is to be able to use Mycroft to send commands to all ESP8266s on the local network. The communication protocol can be selected (Websocket, MQTT, http GET).

## Examples 
* "Hey Mycroft, can you switch on the mood lamp ?"

* "Hey Mycroft, can you turn off the TV ?"

## Configuration

"Esp8266Skill": {
    "units": "esp8266.local", // Can be an IP Address
    "protocol": "http_get", // Options : ws, mqtt, http_get
    "ws-port": 81,
    "mqtt-host" : "test.mosquitto.org",
    "mqtt-port" : 1883,
    "mqtt-auth" : "no", // yes or no
    "mqtt-user" : "youruser",
    "mqtt-pass" : "yourpass"
},

## Credits 
Dark5ide
