from http import HTTPStatus
import requests
import logging
import asyncio
import aiohttp
import async_timeout

import json
import base64

import voluptuous as vol

import homeassistant.loader as loader
from homeassistant.const import (STATE_UNKNOWN, EVENT_STATE_CHANGED)
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from homeassistant.helpers import discovery

from .const import DOMAIN, CONF_ZNAME, CONF_TRACKER, CONF_LAT, CONF_LON

PLATFORM = 'sensor'

_LOGGER = logging.getLogger(__name__)


def base_config_schema(config: dict = {}) -> dict:
    """Return a shcema configuration dict for Polygon Zone."""
    if not config:
        config = {
            CONF_ZNAME: "xxxxxxxxxxxxxxxxxxxxxxxxxxx",
            CONF_TRACKER: "device_tracker.xxxxxxxxxx",
        }
    return {
        vol.Required(CONF_ZNAME, default=config.get(CONF_ZNAME)): str,
        vol.Required(CONF_TRACKER, default=config.get(CONF_TRACKER)): str,
    }


def config_combined() -> dict:
    """Combine the configuration options."""
    base = base_config_schema()

    return base

CONFIG_SCHEMA = vol.Schema({DOMAIN: config_combined()}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass, config):

    if DOMAIN not in config:
        return True

    return True


async def async_setup_entry(hass, config_entry):
    """Set up this integration using UI."""

    if hass.data.get(DOMAIN) is not None:
        return False

    if config_entry.source == config_entries.SOURCE_IMPORT:
        hass.async_create_task(hass.config_entries.async_remove(config_entry.entry_id))
        return False

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, PLATFORM)
    )

    return True


async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    return await hass.config_entries.async_forward_entry_unload(config_entry, PLATFORM)



