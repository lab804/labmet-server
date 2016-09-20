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
                $('#temperatura').text(msg.payload).html();
            });


});