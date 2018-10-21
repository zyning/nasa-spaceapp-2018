var PROD_DEVCONFIG = {
    ACCESS_TOKEN: '',
    ID: '',
    MAP_TYPE: 'mapbox',
    DEBUG: false,
    DEFAULT_LOCALE: 'en',
    TILE_URL: 'http://{s}.tiles.mapbox.com/v3/{mapId}/{z}/{x}/{y}.png'
};

var DEV_CONFIG = {
    API_BASE: 'http://127.0.0.1:5000',
    DEBUG: true,
    DEFAULT_LOCALE: 'en',
    TILE_URL: 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
};

var CONFIG = DEV_CONFIG;