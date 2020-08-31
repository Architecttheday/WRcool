#!/usr/bin/python3
import time
from influxdb import InfluxDBClient
client = InfluxDBClient(host='solaranzeige.fritz.box', port=8086)
client.switch_database('solaranzeige')
tempschwelle = 39.5
leistungsschwelle = 800
#tempcount = 0
#leistungscount = 0
luefterstatus = "off"
import paho.mqtt.client as paho
broker = "solaranzeige.fritz.box"
mqclient = paho.Client("client-001")

while True:
    try:
        rs = client.query('SELECT last("Temperatur") from Service')
        rs2 = client.query('SELECT last("Leistung") from AC')
        tempcount = 0
        leistungscount = 0
        lt = time.localtime()
        points = rs.get_points()
        for item in points:
            print (item['last'])

        points = rs2.get_points()
        for item2 in points:
            print (item2['last'])

        if (item['last']) > tempschwelle:
            print ('Temperatur > ', tempschwelle)
            tempcount = 1

        if (item2['last']) > leistungsschwelle:
            print ('Leistung > ', leistungsschwelle)
            leistungscount = 1

        if tempcount == 1 and leistungscount == 1 and luefterstatus == "off":
            print ('Schalte Lüfter ein!')
            luefterstatus = "on"
            mqclient.connect(broker, 1883, 60)
            mqclient.publish("rfbridge/relay/4/set","1")#publish
            time.sleep(4)
            mqclient.disconnect() #disconnect

        if tempcount == 0 and leistungscount == 0 and luefterstatus == "on":
            print ('Schalte Lüfter aus!')
            luefterstatus = "off"
            mqclient.connect(broker, 1883, 60)
            mqclient.publish("rfbridge/relay/4/set","0")#publish
            time.sleep(4)
            mqclient.disconnect() #disconnect

        fo = open("/var/log/Schaltzustaende.txt", "a+")
        text2write = (time.strftime("%Y-%m-%d_%H:%M:%S" , lt) + ";" + str(tempschwelle) + ";" + str(item['last']) + ";" + str(tempcount) + ";" + str(leistungsschwelle) + ";" + str(item2['last']) + ";" + str(leistungscount) + ";" + luefterstatus + "\n")
        #text2write = (str(tempschwelle) + ";" + str(item['last']) + ";" +  str(tempcount))
        print (text2write)
        fo.write( text2write )
        fo.close()
        time.sleep(60)
    except StopIteration:
      sys.exit()

# Idee:
# wenn beide Werte = 1 dann einschalten
# Wenn beide Werte = 0 und eingeschaltet dann ausschalten


#temp = rs.items()
#print ("Anzahl Items:" , len(temp))
#for x in temp:
#    print (x)

#temp = rs.keys()
#print ("Anzahl Keys:" , len(temp))
#for k in temp:
#    print (k)

#print (rs['Service']['last'])


#def read_energy_data(db, measurement, device):
#    client = InfluxDBClient(pooldb.influx_host, pooldb.influx_port, pooldb.influx_user, pooldb.influx_password, db)
#    results = client.query(("SELECT %s from %s ORDER by time DESC LIMIT 1") % (device, measurement))
#    points = results.get_points()
#    for item in points:
#        return item[device]
