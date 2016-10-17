# Weather monitoring platform with NodeMCU and Raspberry

The weather monitoring platform is composed by NodeMCU clients and one or more
RaspberryPi servers. The NodeMCUs captures environmental weather data with its
sensors and sends them to the RaspberryPi. The RaspberryPi server treats the
collected data and uses them as input for the FAO
[AquaCrop](http://www.fao.org/nr/water/docs/irrigationdrainage66.pdf) model.
With the processed data, the server feeds the website, application and database.
The project is subdivided in three sub-projects, the
[physical implementation](https://github.com/lab804/labmet-weatherstation)
of the weather station that is consisted by the electronic circuit and C/C++
low level firmware, the RaspberryPi [Flask](http://flask.pocoo.org/) web server
and [MQTT](http://mqtt.org/) broker, hosted [here](https://github.com/lab804),
and the [algorithm implementation](https://github.com/lab804) of the AquaCrop model.

![download](https://cloud.githubusercontent.com/assets/22622042/19200013/2f33d736-8c9d-11e6-9320-64f6caaec629.png)

The Raspberry Pi is responsible for receive data collected by NodeMCU through MQTT
and send to server this data. [MQTT](www.mqtt.org) is a machine-to-machine (M2M)/
"Internet of Things" connectivity protocol. It was designed as an extremely lightweightx
publish/subscribe messaging transport. It is useful for connections with remote
locations where a small code footprint is required and/or network bandwidth is
at a premium. It is ideal for mobile applications because of its small size, low
power usage, minimised data packets, and efficient distribution of information
to one or many receivers. The intermediary in the communication process is the
[mosquitto](https://mosquitto.org/documentation/), a MQTT message Broker, in
which requires clients log in username and password authentication.
The messages identification (received data) is performed by the broker by means
of threads. The server is fed with the Broker. The received data are treated
and sent to the website, application and database. The crop yield is calculated
using the received data from the server.

The Raspberry Pi server handles the data collected and provide relevant information. This information is generated from the definitions of culture together with the data collected. The model used is FAO [AquaCrop](http://www.fao.org/nr/water/docs/irrigationdrainage66.pdf). Basically, AquaCrop is a crop water productivity model developed by the Land and Water Division of FAO. It simulates yield response to water of herbaceous crops, and is particularly suited to address conditions where water is a key limiting factor in crop production. AquaCrop attempts to balance accuracy, simplicity, and robustness.

The [Flask](http://pymbook.readthedocs.io/en/latest/flask.html) web framework was used. This means flask provides you with tools, libraries and technologies that allow you to build a web application.

The database used to store the data is MongoDB, which receives the Broker data.
[MongoDB](https://www.mongodb.com/) (from humongous) is a free and open-source
cross-platform document-oriented database program. Classified as a
[NoSQL](http://nosql-database.org/) database program, MongoDB avoids the traditional
table-based relational database structure in favor of
[JSON](https://www.mongodb.com/json-and-bson)-like documents with dynamic schemas
(It calls the format [BSON](https://www.mongodb.com/json-and-bson)), making the
integration of data in certain types of applications easier and faster.


Figure 1 Illustrates the operation and the relationship between components: NodeMCU,
Raspberry Pi, Server, Web, App and MongoDB.

#### Figure 1
![demonstrativo_1_labmet](https://cloud.githubusercontent.com/assets/22622042/19085103/771c335a-8a3f-11e6-8490-23a1b3c566d1.png)


In this example we use only one NodeMCU and one Raspberry Pi. However, multiple
NodeMCU can be added to one single Raspberry Pi, so that you have several stations
in different locations using a single manager, as observed in figure 2. It is
important to mention that the same goes for the Raspberry Pi and servers,
where you have a Raspberry Pi connected to one or more servers.

#### Figure 2
![demonstrativo_2_labmet](https://cloud.githubusercontent.com/assets/22622042/19085120/902669d8-8a3f-11e6-85ad-532257b41262.png)

This condition is only possible if the stations are in range of the manager's
WiFi network. Remember the Raspberry Pi must be connected to the Internet, so the
data and information are processed in real time, which is indispensable for
the components work properly.

## Getting Started

#### Requirements
* Raspberry Pi 3
* 5V Power supply

#### Languages
* Python

#### Technologies
* MongoDB
* Socket IO
* Mosquitto
* Flask

#### Installation and Configuration

1. Raspberry Pi set up as an access point
  * Access [Generator AP](https://github.com/lab804/generate-ap)

2. Install Mosquitto
  * [Download and Install]((https://mosquitto.org/download/) to your operating system

3. Running App
  * Install Python Requirements with command:

            pip install -r requirements.txt

  * Install [Bower](https://bower.io/) components

  * Install [Supervisor](http://supervisord.org/installing.html) and
  [Configure](http://supervisord.org/configuration.html) to run the APP with system boot

4. Enjoy!


### Copyright & License

Copyright 2016 - Lab804 - All rights reserved.
