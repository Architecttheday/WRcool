#!/usr/bin/python3
from influxdb import InfluxDBClient
client = InfluxDBClient(host='solaranzeige', port=8086)
client.switch_database('solaranzeige')
tempschwelle = 29.5
leistungsschwelle = 800

rs = client.query('SELECT last("Temperatur") from Service')
# print ("Result: {0}".format(rs))
rs2 = client.query('SELECT last("Leistung") from AC')

points = rs.get_points()
for item in points:
    print (item['last'])

points = rs2.get_points()
for item2 in points:
    print (item2['last'])

if (item['last']) > tempschwelle:
    print ('Temperatur > ', tempschwelle)

if (item2['last']) > leistungsschwelle:
    print ('Leistung > ', leistungsschwelle)


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
