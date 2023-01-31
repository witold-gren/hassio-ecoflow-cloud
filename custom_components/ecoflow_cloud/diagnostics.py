from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import DOMAIN
from .mqtt.ecoflow_mqtt import EcoflowMQTTClient


def _to_serializable(x):
    t = type(x)
    if t is dict:
        x = {y: _to_serializable(x[y]) for y in x}
    if t is timedelta:
        x = x.__str__()
    return x


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry):
    client: EcoflowMQTTClient = hass.data[DOMAIN][entry.entry_id]
    values = {
        'data': dict(sorted(client.data.params.items())),
        'override': dict(sorted(client.data.params_override.items())),
        'set_commands': {k: v.diagnostic_dict() for k, v in client.data.set_commands.items()},
        'get_commands': {k: v.diagnostic_dict() for k, v in client.data.get_commands.items()},
        'raw_data': client.data.raw_data,
    }
    return values
