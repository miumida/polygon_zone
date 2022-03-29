"""Config flow for Polygon Zone."""
import logging
import json

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, TITLE, VERSION, CONF_ZNAME, CONF_ZPATH, CONF_ZTYPE, CONF_TRACKER, _ZTYPE

_LOGGER = logging.getLogger(__name__)


class PolygonZoneConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Polygon Zone."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize flow."""
        self._zname: Required[str] = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            self._zname = user_input[CONF_ZNAME]
            self._ztype = user_input[CONF_ZTYPE]

            uniqid = 'polygon-zone-{}-{}'.format(self._ztype, self._zname)
            await self.async_set_unique_id(uniqid)

            zTitle = self._zname

            return self.async_create_entry(title=zTitle, data=user_input)

#        if self._async_current_entries():
#            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            schema = vol.Schema(
                {
                    vol.Required(CONF_ZNAME, default=None): str,
                    vol.Required(CONF_ZPATH, default=None): str,
                    vol.Required(CONF_ZTYPE, default="D"): vol.In( _ZTYPE ),
                    vol.Required(CONF_TRACKER, default=None): vol.In( self.getAllDeviceNames(self.hass))
                }
            )

            return self.async_show_form(step_id='user', data_schema=schema)


    async def async_step_import(self, import_info):
        """Handle import from config file."""
        return await self.async_step_user(import_info)

    def getAllDeviceNames(self, hass):
        list = hass.states.async_all()
        result = []
        for state in list:
            entity_id = state.entity_id
            if entity_id.split(".")[0] != "device_tracker":
                continue
            result.append(entity_id)

        return result
