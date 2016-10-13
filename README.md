
# Weather monitoring platform with NodeMCU and Raspberry

The weather monitoring platform is composed by NodeMCU clients and one or more RaspberryPi servers. The NodeMCUs captures environmental weather data with its sensors and sends them to the RaspberryPi. The RaspberryPi server treats the collected data by the FAO [AquaCrop](http://www.fao.org/nr/water/docs/irrigationdrainage66.pdf) model and feeds the website, application and database with informations. The project is subdivided in three sub-projects, the [physical implementation](https://github.com/lab804/labmet-weatherstation) of the weather station that is consisted by the electronic circuit and C/C++ low level firmware, the RaspberryPi [Flask](http://flask.pocoo.org/) web server and [MQTT](http://mqtt.org/) broker, hosted [here](https://github.com/lab804), and the AquaCrop model [algorithm implementation](https://github.com/lab804).

![download](https://cloud.githubusercontent.com/assets/22622042/19200013/2f33d736-8c9d-11e6-9320-64f6caaec629.png)

The Raspberry is responsible for receive data collected by NodeMCU through MQTT and send to server this data.  [MQTT](www.mqtt.org) is a machine-to-machine (M2M)/"Internet of Things" connectivity protocol. It was designed as an extremely lightweight publish/subscribe messaging transport. It is useful for connections with remote locations where a small code footprint is required and/or network bandwidth is at a premium. It is ideal for mobile applications because of its small size, low power usage, minimised data packets, and efficient distribution of information to one or many receivers. The intermediary in the communication process is the [mosquitto](https://mosquitto.org/documentation/), a MQTT message Broker, in which requires clients log in username and password authentication. The messages identification (received data) is performed by the broker by means of threads. The server is fed with the Broker. The received data are treated and sent to the website, application and database. The crop yield is calculated using the received data from the server.

The RaspberryPi server treats the collected data by the FAO AquaCrop model and feeds the website, application and database with informations.

The database used to store the data is MongoDB, which receives the Broker data. [MongoDB](https://www.mongodb.com/) (from humongous) is a free and open-source cross-platform document-oriented database program. Classified as a NoSQL database program, MongoDB avoids the traditional table-based relational database structure in favor of JSON-like documents with dynamic schemas (It calls the format BSON), making the integration of data in certain types of applications easier and faster.


Figure 1 Illustrates the operation and the relationship between NodeMCU components, Raspberry Pi, Server, Web, App and MongoDB.

#### Figure 1
![demonstrativo_1_labmet](https://cloud.githubusercontent.com/assets/22622042/19085103/771c335a-8a3f-11e6-8490-23a1b3c566d1.png)


In this example we use only one NodeMCU and one Raspberry. However, multiple NodeMCU can be added to one single Raspberry, so that you have several stations in different locations using a single manager, as observed in figure 2. It is important to mention that the same goes for the Raspberry Pi and servers, where you have a Raspberry Pi and one or more servers.

#### Figure 2
![demonstrativo_2_labmet](https://cloud.githubusercontent.com/assets/22622042/19085120/902669d8-8a3f-11e6-85ad-532257b41262.png)

This condition is only possible if the stations are in the range of the manager's WiFi network, Which is indispensable for the components to work properly.

## Getting Started

#### Requirements
* Raspberry Pi 3
* 5V Power supply

#### Languages
* Python

#### Technologies
* MongoDB
* Flask
* Socket IO
* Mosquitto

#### Installation

1. Just run this [shell script](https://github.com/lab804/generate-ap/blob/master/create.sh)


### Copyright e Licença

Copyright 2016 - Lab804 - All rights reserved.
