# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

from urllib2 import urlopen
from websocket import create_connection
import paho.mqtt.client as mqtt

__author__ = 'Dark5ide'

LOGGER = getLogger(__name__)

class Esp8266Skill(MycroftSkill):

    def __init__(self):
        super(Esp8266Skill, self).__init__(name="Esp8266Skill")
        self.esp_units = self.config.get("units")
        if type(self.esp_units) == unicode:
            self.esp_units = [self.esp_units]
        self.protocol = self.config.get("protocol")
        
        # websocket parameter
        self.ws = None
        self.ws_port = self.config.get("ws-port")
        
        # mqtt parameter
        self.mqtt_host = self.config.get("mqtt-host")
        self.mqtt_port = self.config.get("mqtt-port")
        self.mqtt_auth = self.config.get("mqtt-auth")
        self.mqtt_user = self.config.get("mqtt-user")
        self.mqtt_pass = self.config.get("mqtt-pass")    
    
    def initialize(self):
        self.load_data_files(dirname(__file__))
        self. __build_single_command()        
        
    def __build_single_command(self):
        intent = IntentBuilder("Esp8266CmdIntent").require("CommandKeyword").require("ModuleKeyword").optionally("ActionKeyword").build()
        self.register_intent(intent, self.handle_single_command)
        
    def handle_single_command(self, message):
        cmd_name = message.data.get("CommandKeyword")
        mdl_name = message.data.get("ModuleKeyword")
        act_name = message.data.get("ActionKeyword")
        esp_mdl_name = mdl_name.replace(' ', '_')
        
        if act_name:
            cmd_name += '_' + act_name

        try:
            if (self.protocol == "ws"):
                if self.ws is None:
                    self.ws = [create_connection("ws://" + u + ":81/") for u in self.esp_units]
                for ws_connect in self.ws:
                    ws_connect.send(esp_mdl_name + "-" + cmd_name)
            elif (self.protocol == "mqtt"):
                mqttc = mqtt.Client("MycroftAI")
                if (self.mqtt_auth == "yes"):
                    mqttc.username_pw_set(username=str(self.mqtt_user), password=str(self.mqtt_pass))
                mqttc.connect(host=str(self.mqtt_host), port=self.mqtt_port)
                mqttc.publish("/mycroft/" + esp_mdl_name, cmd_name) # todo : use json to send module and command name
                mqttc.disconnect()
            else:
                to_esp = esp_mdl_name + "?cmd=" + cmd_name
                # exemple : http://esp8266.local/led0?cmd=turn_on
                for u in self.esp_units:
                    urlopen("http://" + u + "/" + to_esp)
                #urlopen("http://esp8266.local/" + to_esp)
            self.speak_dialog("cmd.sent")
        except Exception as e:
            self.ws = None
            self.speak_dialog("not.found", {"command": cmd_name, "action": act_name, "module": mdl_name})
            LOGGER.error("Error: {0}".format(e))
        
    def stop(self):
        pass
        
def create_skill():
    return Esp8266Skill()
