#!/usr/bin/python3
import time
import paho.mqtt.client as paho
broker = "solaranzeige"
#broker="iot.eclipse.org"
#define callback
def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =",str(message.payload.decode("utf-8")))

client = paho.Client("client-001") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
######Bind function to callback
client.on_message=on_message
#####
print("connecting to broker ",broker)
client.connect(broker, 1883, 60)#connect
client.loop_start() #start loop to process received messages
print("subscribing ")
client.subscribe("rfbridge/relay/4")#subscribe
time.sleep(2)
print("publishing on")
client.publish("rfbridge/relay/4/set","1")#publish
time.sleep(4)
print("publishing off")
client.publish("rfbridge/relay/4/set","0")#publish
time.sleep(4)
client.disconnect() #disconnect
client.loop_stop() #stop loop
