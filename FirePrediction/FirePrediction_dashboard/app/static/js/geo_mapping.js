var Map = {
        map: null,
        path: null,
        g: null,
        centered: null,
        default_center: [40.64, -74.00],
        default_zoom: 10,
        default_radius: 10,
        city_name: 'nyc',
        api_url: '/get_city_preds/',
        map: null,
        window_timer: 60 * 60 * 24 * 1000, //1 day;
        width: $(window).width(),
        height: $(window).width(),
        init: function() {
            //$("#map_wrapper #map").css("width", $(window).width());
            //$("#map_wrapper #map").css("height", $(window).height());
            window.onresize = Map.fix_map;

            Map.map = L.map('map',).setView(Map.default_center, Map.default_zoom);

            if (CONFIG.MAP_TYPE === 'mapbox') {
                return L.mapbox.tileLayer(CONFIG.MAP_ID, {
                    accessToken: CONFIG.ACCESS_TOKEN,
                    attribution: '<a href="http://openstreetmap.org/copyright">Map data: © OpenStreetMap</a> | <a href="http://mapbox.com/map-feedback/" class="mapbox-improve-map">Improve this map</a>'
                }).addTo(Map.map);
            } else {
                return L.tileLayer(CONFIG.TILE_URL, {
                    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>',
                    maxZoom: 18
                }).addTo(Map.map);


            }

        },

        fix_map: function() {
            $("#map").css("width", $(window).width());
            $("#map").css("height", $(window).height());
        },
        style: function(feature) {
            return {
                weight: 2,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.7,
                fillColor: Map.GetColor(feature.properties.density)
            };
        },
        highlight_feature: function(e) {
            var layer = e.target;

            layer.setStyle({
                weight: 3,
                color: '#666',
                dashArray: '',
                fillOpacity: 0.7
            });

            if (!L.Browser.ie && !L.Browser.opera) {
                layer.bringToFront();
            }

            //info.update(layer.feature.properties);
        },
        reset_highlight: function(e) {
            Map.geojson.resetStyle(e.target);
            //info.update();
        },
        zoom_to_feature: function(e) {
            Map.map.fitBounds(e.target.getBounds());
            console.log(e.target);
        },
        on_each_feature: function(feature, layer) {
            if (feature.properties && feature.properties.sensor_id) {
                layer.bindPopup("Tract ID:" + feature.properties.tract_id + "<br> Prediction:" +  feature.properties.pred_score);
            }

            layer.on({
                mouseover: Map.highlight_feature,
                mouseout: Map.reset_highlight,
                click: Map.zoom_to_feature
            });
        },


        building_pred_literal: function(pred_score) {

            if (pred_score == 1) {
                return 'Dangerous';
            } else {
                return 'Safe';
            }
        },

        // get color depending 
        get_color: function(d) {
            var green_color = '#27ae60';
            var red_color = '#c0392b';
            var other_cases = '#f39c12';


            console.log(d);
            if (d == -1) {
                return other_cases;
            }
            if (d == 1) {
                return red_color;
            }
            if (d == 0) {
                return green_color;
            }
        },

        launch_firecaster: function(api_url) {

            $.getJSON(api_url, function(data, response_text, jqXHR) {

                if (jqXHR.status != 204) {
                    if (jqXHR.status != 204) {
                        console.log(data);
                    }
                }
            });

        },

        run: function() {
            Map.launch_firecaster(Map.api_url + Map.city_name);
        }
};