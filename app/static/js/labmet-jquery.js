/**
 * Created by joao on 17/05/16.
 */

(function($) {
    $.fn.extend({
        'LabMet': function(_options) {
            var _defaulthost = 'http://' + document.domain + ':' + location.port;

            var showMsgDisc = false,
                shoMsgConn = true,
                graphicsData = {},
                lastIndex = 1; // simple example plot x

            var options = $.extend({
                'host': _defaulthost,
                '_ids': [],
                'namespace': 'weather_data',
            }, _options);

            var _ids = options['_ids'];

            var _host = options['host'] + '/' + options['namespace'];

            var socket = io.connect(_host);

            /*
            plot
            */
            var PlotData = function(_id) {
              $.plot($("#flot-"+_id), [
                  graphicsData[_id]['data_obt'], graphicsData[_id]['data_pot']
              ], {
                  series: {
                      lines: {
                          show: true,
                          fill: true
                      },
                      splines: {
                          show: true,
                          tension: 0.4,
                          lineWidth: 1,
                          fill: 0.4
                      },
                      points: {
                          radius: 0,
                          show: true
                      },
                      shadowSize: 2
                  },
                  grid: {
                      hoverable: true,
                      clickable: true,
                      tickColor: "#d5d5d5",
                      borderWidth: 1,
                      color: '#d5d5d5'
                  },
                  colors: ["#1ab394", "#1C84C6"],
                  xaxis: {},
                  yaxis: {
                      ticks: 4
                  },
                  tooltip: false
              });
            };


            if (_ids.length > 0 && _ids.length <= 10) {

              for (var i = 0; i < _ids.length; i++) {
                var _id = _ids[i];

                // creating for populate data
                graphicsData[_id] = {'data_obt': [], 'data_pot':[]};

                var card = ['<div class="browser-mockup" style="background-color: #fff; margin-top: 25px;">',
                '    <div><img class="ico-labmet" src="/static/img/icon.png" /></div>',
                '    <div class="status status-disconnected"><div>',
                '    <div class="row" style="padding: 20px;">',
                '      <div class="col-md-3">',
                '          <h2 style="margin-top: 10px; font-size: 26px;">My Station <small id="id-'+_id+'" class=""></small></h2>',
                '          <div>last update: <small id="collected_at-'+_id+'" style="font-size: 85%"></small></div>',
                '          <ul class="list-group clear-list" style="margin-top: 15px;">',
                '              <li class="list-group-item fist-item" style="padding: 10px 0; border-top: 0; border-left:0; border-right: 0; border-bottom: 0;">',
                '                  <span class="pull-right animated" id="ds18b20_temp-'+_id+'">',
                '                      0',
                '                  </span>',
                '                  <span class="label label-success" style="margin-right: 10px;">OK</span> Temperature',
                '              </li>',
                '              <li class="list-group-item"  style="padding: 10px 0; border-top: 1px solid #e7eaec; border-left:0; border-right: 0; border-bottom: 0;">',
                '                  <span class="pull-right animated" id="bmp180_alt-'+_id+'">',
                '                      0',
                '                  </span>',
                '                  <span class="label label-success" style="margin-right: 10px;">OK</span> Altitude',
                '              </li>',
                '              <li class="list-group-item" style="padding: 10px 0; border-top: 1px solid #e7eaec; border-left:0; border-right: 0; border-bottom: 0;">',
                '                  <span class="pull-right animated" id="bmp180_press-'+_id+'">',
                '                      0',
                '                  </span>',
                '                  <span class="label label-success" style="margin-right: 10px;">OK</span> Pressure',
                '              </li>',
                '              <li class="list-group-item" style="padding: 10px 0; border-top: 1px solid #e7eaec; border-left:0; border-right: 0; border-bottom: 0;">',
                '                  <span class="pull-right animated" id="dht22_humid-'+_id+'">',
                '                      0',
                '                  </span>',
                '                  <span class="label label-success" style="margin-right: 10px;">OK</span> Humidity',
                '              </li>',
                '              <li class="list-group-item" style="padding: 10px 0; border-top: 1px solid #e7eaec; border-left:0; border-right: 0; border-bottom: 0;">',
                '                  <span class="pull-right animated" id="bh1750_illuminance-'+_id+'">',
                '                      0',
                '                  </span>',
                '                  <span class="label label-success" style="margin-right: 10px;">OK</span> Illuminance',
                '              </li>',
                '              <li class="list-group-item" style="padding: 10px 0; border-top: 1px solid #e7eaec; border-left:0; border-right: 0; border-bottom: 0;">',
                '                  <span class="pull-right animated" id="analog_soil_moisture-'+_id+'">',
                '                      0',
                '                  </span>',
                '                  <span class="label label-success" style="margin-right: 10px;">OK</span> Soil Moisture',
                '              </li>',
                '            </ul>',
                '    </div>',
                '    <div class="col-md-6">',
                '      <div class="flot-chart dashboard-chart">',
                '          <div class="labmet-flot" id="flot-'+_id+'"></div>',
                '          <div class="row text-left">',
                '            <div class="col-xs-3">',
                '              <div style="margin-left: 20px;">',
                '                <span class="h4 font-bold" style="display: block !important; margin-top: 15px; font-weight: 600;" id="potential_productivity-'+_id+'">0</span>',
                '                <small class="text-muted" style="display: block !important; margin-bottom: 15px; color: #888888;">Potential Productivity</small>',
                '              </div>',
                '            </div>',
                '            <div class="col-xs-3">',
                '              <div style="margin-left: 20px;">',
                '                <span class="h4 font-bold" style="display: block !important; margin-top: 15px; font-weight: 600;" id="obtainable_productivity-'+_id+'">0</span>',
                '                <small class="text-muted" style="display: block !important; margin-bottom: 15px; color: #888888;">Obtainable Productivity</small>',
                '              </div>',
                '            </div>',
                '            <div class="col-xs-3">',
                '              <div style="margin-left: 20px;">',
                '                <span class="h4 font-bold" style="display: block !important;margin-top: 15px; font-weight: 600;" id="etc-'+_id+'">0</span>',
                '                <small class="text-muted" style="display: block !important;margin-bottom: 15px; color: #888888;">Real Water Usage</small>',
                '              </div>',
                '            </div>',
                '            <div class="col-xs-3">',
                '              <div style="margin-left: 20px;">',
                '                <span class="h4 font-bold" style="display: block !important;margin-top: 15px; font-weight: 600;" id="eto-'+_id+'">0</span>',
                '                <small class="text-muted" style="display: block !important;margin-bottom: 15px; color: #888888;">Potential Water Usage</small>',
                '              </div>',
                '            </div>',
                '          </div>',
                '    </div>',
                '  </div>',
                '  <div class="col-md-3 text-center potato">',
                '    <img src="/static/img/potato.png" id="potato-'+_id+'" class="animated fadeInUp potato-15">',
                '  </div>',
                '</div>'].join("");

                $(this).append(card);

                PlotData(_id);
              }
            }


            /*
            function set unit TODO: "Sorry portuguese; change this!!"

            - Capacidade de água no solo(*mm*)
            - Temperatura do Ar (*°C*)
            - Temperatura do Solo (*°C*)
            - Pressão(*Bar*)
            - Altitude (*m*)
            - Luminosidade (*lx* ou *lux*)
            - Umidade Relativa (*%*)
            - Produtividade (*Kg/m²*)

            */
            var setUnit = function(key) {
                if (key === 'bmp180_press') {
                    return "Bar";
                } else if (key === 'ds18b20_temp') {
                    return "°C*";
                } else if (key === 'dht22_humid') {
                    return "%"
                } else if (key === 'analog_soil_moisture') {
                    return "mm";
                } else if (key === 'bmp180_temp') {
                    return "°C";
                } else if (key === 'bh1750_illuminance') {
                    return "lux";
                } else if (key === 'bmp180_alt') {
                    return "m";
                } else {
                    return "";
                }
            };

            /*
            toPerce
            */
            var toPerce = function(value) {
              var max = 4000; // change this depend culture
              if (value > 0 || value <= 4000) {
                div = value / 60;
                return parseInt(div);
              } else if (value === 4000) {
                return 100;
              }
            }

            /*
            function born
            */
            var born = function(_id, life) {
                _intlife = parseInt(life);
                if (_intlife) {
                    // remove last class
                    $('img#potato-' + _id).removeClass('potato-*');
                    $('img#potato-' + _id).removeClass('fadeInUp');
                    if (_intlife > 0 && _intlife <= 15) {
                        $('img#potato-' + _id).addClass('fadeInUp');
                        $('img#potato-' + _id).addClass('potato-15');
                    } else if (_intlife > 15 && _intlife <= 25) {
                        $('img#potato-' + _id).addClass('fadeInUp');
                        $('img#potato-' + _id).addClass('potato-25');
                    } else if (_intlife > 25 && _intlife <= 50) {
                        $('img#potato-' + _id).addClass('potato-50');
                        $('img#potato-' + _id).addClass('fadeInUp');
                    } else if (_intlife > 50 && _intlife <= 75) {
                        $('img#potato-' + _id).addClass('potato-75');
                        $('img#potato-' + _id).addClass('fadeInUp');
                    } else if (_intlife > 50 && _intlife <= 100) {
                        $('img#potato-' + _id).addClass('potato-100');
                        $('img#potato-' + _id).addClass('fadeInUp');
                    }
                }
            };

            /*
            function set data
            */
            var setData = function(data) {
                // parse
                var _data = data;
                var _id = _data['id'];
                $.each(_data, function(key, value) {
                    if (key === "collected_at") {
                        $('#' + key + '-' + _id).text(value);
                    } else if (key === "id") {
                        $('#' + key + '-' + _id).text("#" + " " + parseInt(value).toString());
                    } else {
                        unit = setUnit(key);
                        $('#' + key + '-' + _id).text(value.toFixed(2).toString() + " " + unit);
                    }
                });

                // populate new data
                graphicsData[_id]['data_pot'].push([lastIndex, _data['potential_productivity']]);
                graphicsData[_id]['data_obt'].push([lastIndex, _data['obtainable_productivity']]);
                PlotData(_id);
                lastIndex = lastIndex + 1; // X coordinate

                window.onresize = function(event) {
                    PlotData(_id);
                }

                var potatoval = toPerce(_data['obtainable_productivity']);
                if (potatoval >= 0 && potatoval <= 100) {
                    born(_id, potatoval);
                }

            };


            socket.on('connect', function() {
                $('.status').removeClass('status-disconnected');
                $('.status').addClass('status-connected');

                if (!shoMsgConn) {
                    $.toaster({
                        message: 'You are online',
                        title: 'Online',
                        priority: 'success'
                    });
                    shoMsgConn = true;
                    showMsgDisc = false;
                }

            });

            socket.on('disconnect', function() {
                $('.status').removeClass('status-connected');
                $('.status').addClass('status-disconnected');

                if (!showMsgDisc) {
                    $.toaster({
                        message: 'You are offline',
                        title: 'Offline',
                        priority: 'danger'
                    });
                    showMsgDisc = true;
                    shoMsgConn = false;
                }

            });

            /*
            receive data from station
            */
            socket.on('station_data', function(msg) {
                setData(msg);
            });

            return this;
        }
    });
})(jQuery);
