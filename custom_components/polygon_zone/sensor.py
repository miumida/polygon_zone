import logging
import requests
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from datetime import timedelta
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, VERSION, CONF_TRACKER, CONF_ZNAME, CONF_ZPATH, CONF_ZTYPE, CONF_LAT, CONF_LON, _ZTYPE, _ZTYPE_ICON

_LOGGER = logging.getLogger(__name__)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ZNAME): cv.string,
    vol.Required(CONF_ZPATH): cv.string,
    vol.Required(CONF_ZTYPE): cv.string,
    vol.Required(CONF_TRACKER): cv.string,
})

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add a entity from a config_entry."""
    sensors = []
    sensors += [PolygonZoneSensor(hass, config_entry)]

    async_add_devices(sensors, True)

class PolygonZoneSensor(Entity):
    """Representation of a Polygon Zone Sensor."""
    def __init__(self, hass, config_entry):
        """Initialize the Polygon Zone sensor."""
        self._hass = hass
        self._config_entry = config_entry

        self._tracker = config_entry.data[CONF_TRACKER]

        self._name = None

        self._zname = config_entry.data[CONF_ZNAME]
        self._zpath = config_entry.data[CONF_ZPATH]
        self._ztype = config_entry.data[CONF_ZTYPE]
        self._entry = hass.states.get(self._tracker)

        self._state = None
        self._zone  = self.path2zone(self._zpath)

    def path2zone(self, path):
        zone = []

        arrPath = path.split(",")

        for i in range(0, len(arrPath), 2):
           point = []
           point.append(float(arrPath[i].strip()))
           point.append(float(arrPath[i+1].strip()))

           zone.append(point)

        return zone

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return 'sensor.polygon_zone_{}_{}'.format(self._ztype, self._zname)

    @property
    def name(self):
        """Return the name of the sensor, if any."""
        if self._name is None:

            self._name = 'polygon_zone_{}_{}'.format(self._ztype, self._zname)
            return self._name
        else:
            return self._zname

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return _ZTYPE_ICON[self._ztype]

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Get the latest state of the sensor."""
        self._entry = self._hass.states.get(self._tracker)

        if self._entry is not None:
            lat = self._entry.attributes[CONF_LAT]
            lon = self._entry.attributes[CONF_LON]

            x = lat
            y = lon

            n = len(self._zone)
            inside = False

            p1x,p1y = self._zone[0]

            for i in range(n+1):
                p2x,p2y = self._zone[i % n]
                if y > min(p1y,p2y):
                    if y <= max(p1y,p2y):
                        if x <= max(p1x,p2x):
                            if p1y != p2y:
                                xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                            if p1x == p2x or x <= xints:
                                inside = not inside
                p1x,p1y = p2x, p2y

            now = 'in' if inside else 'out'
            self._state = now

    @property
    def extra_state_attributes(self):
        """Attributes."""
        data = {}

        data[CONF_TRACKER] = self._tracker

        zpath = []

        for p in self._zone:
            tmp = "({}, {})".format(p[0], p[1])
            zpath.append(tmp)

        if self._entry is not None:
            #if CONF_LAT in self._entry.attributes:
            #    data[CONF_LAT] = self._entry.attributes[CONF_LAT]

            #if CONF_LON in self._entry.attributes:
            #    data[CONF_LON] = self._entry.attributes[CONF_LON]

            data["tracker loaction"]  = [ self._entry.attributes[CONF_LAT], self._entry.attributes[CONF_LON] ]

        data[CONF_ZNAME] = self._zname
        data[CONF_ZTYPE] = _ZTYPE[self._ztype]
        data[CONF_ZPATH] = zpath

        return data


    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._zpath)},
            "name": 'Polygon Zone',
            "manufacturer": 'miumida',
            "sw_version": VERSION,
            "model": f"Polygon Zone({self._zname})",
            "DeviceEntryType": "service",
        }
