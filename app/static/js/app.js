/**
 * Created by joao on 17/05/16.
 */

$(document).ready(function(){
    namespace = '/weather_data';

    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

    socket.on('connect', function() {
            socket.emit('my event', {data: 'I\'m connected!'});
            });

    socket.on('my response', function(msg) {
                console.log(msg);
                $('#collected_at').text(msg.payload["collected_at"]).html();
                $('#bmp180_temp').text(msg.payload["bmp180_temp"]).html();
                $('#bmp180_alt').text(msg.payload["bmp180_alt"]).html();
                $('#bmp180_press').text(msg.payload["bmp180_press"]).html();
                $('#ds18b20_temp').text(msg.payload["ds18b20_temp"]).html();
                $('#dht22_temp').text(msg.payload["dht22_temp"]).html();
                $('#dht22_humid').text(msg.payload["dht22_humid"]).html();
                $('#bh1750_illuminance').text(msg.payload["bh1750_illuminance"]).html();
                $('#analog_soil_moisture').text(msg.payload["analog_soil_moisture"]).html();
            });


});