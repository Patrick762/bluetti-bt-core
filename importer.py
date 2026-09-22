"""Import and generate translations."""

import json
import requests
from typing import Literal

# from custom_components.bluetti_bt.const import EntityDetailsMap
from bluetti_bt_lib import FieldName

t_url = "https://patrick762.github.io/bluetti-registers/translations.json"
p_url = "https://patrick762.github.io/bluetti-registers/protocols.json"

t_json: dict[str, dict[str, str]] = requests.get(t_url).json()
p_json: list[dict[Literal["version", "comm_type", "fields"], str | int | dict]] = (
    requests.get(p_url).json()
)

t_en = {
    "config": {
        "abort": {
            "already_configured": "[%key:common::config_flow::abort::already_configured_device%]",
            "no_unconfigured_devices": "No unconfigured devices",
            "unsupported_device": "Unsupported device",
        },
        "step": {
            "reconfigure": {"description": "Do you want to reconfigure this device?"},
            "user": {"description": "Do you want to add this device?"},
        },
    },
    "entity": {},
}

t_de = {
    "config": {
        "abort": {
            "already_configured": "",
            "no_unconfigured_devices": "Keine unkonfigurierten Geräte",
            "unsupported_device": "Gerät wird nicht unterstützt",
        },
        "step": {
            "reconfigure": {"description": "Möchtest du das Gerät neu konfigurieren?"},
            "user": {"description": "Möchtest du das Gerät hinzufügen?"},
        },
    },
    "entity": {},
}

type EntityType = Literal["binary_sensor", "sensor", "switch", "select"]
type EntityTranslations = dict[EntityType, dict[str, dict[Literal["name"], str]]]


details = {}

for proto in p_json:
    if proto["comm_type"] != "bt":
        continue

    for field in proto["fields"]:
        if field["name"] not in FieldName:
            continue

        f_name = FieldName(field["name"])

        line = f"""{f_name}: DetailsMapping(
        unit={f'"{field["unit"]}"' if "unit" in field.keys() else "None"},
        category={f'EntityCategory.{field["category"].upper()}' if "category" in field.keys() else "None"},
        device_class={f'SensorDeviceClass.{field["sensor"].upper()}' if "sensor" in field.keys() else "None"},
        state_class={f'SensorStateClass.{field["state_type"].upper()}' if "state_type" in field.keys() else "None"},
    ),"""

        details[f_name] = line

details = [l for l in details.values()]

const_py = f"""\"\"\"Constants for the Bluetti BT integration.\"\"\"

from dataclasses import dataclass

from bluetti_bt_lib import FieldName

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import EntityCategory

DOMAIN = "bluetti_bt"

CONF_ENCRYPTION = "encryption"
CONF_SERIAL = "serial"


@dataclass
class DetailsMapping:
    \"\"\"Details Mapping for Entities.\"\"\"

    unit: str | None
    category: EntityCategory | None
    device_class: SensorDeviceClass | None
    state_class: SensorStateClass | None


ENTITY_DETAILS_MAPPING: dict[FieldName, DetailsMapping] = {{
    {'\n\t'.join(details)}
}}
""".replace(
    "\t", "    "
)

with open("custom_components/bluetti_bt/const.py", "w") as f:
    f.write(const_py)
    f.close()


def get_type(field_name: str) -> EntityType:
    # TODO based on p_json
    return "sensor"


def is_needed(field_name: str) -> bool:
    # TODO check if translation is needed for bluetooth
    result = False

    for proto in p_json:
        if proto["comm_type"] != "bt":
            continue

        for field in proto["fields"]:
            if field["name"] == field_name:
                result = True

    return result


t_entity: EntityTranslations = {}

for locale, translations in t_json.items():
    for field_name, value in translations.items():
        if not is_needed(field_name):
            continue

        f_type = get_type(field_name)

        if f_type not in t_entity.keys():
            t_entity.setdefault(f_type, {})

        t_entity[f_type].setdefault(field_name, {})
        t_entity[f_type][field_name]["name"] = value

    match (locale):
        case "en":
            t_en["entity"] = t_entity
            break
        case "de":
            t_de["entity"] = t_entity
            break

with open("custom_components/bluetti_bt/strings.json", "w") as f:
    json.dump(t_en, f, indent=2)
    f.close()

# Custom component only

with open("custom_components/bluetti_bt/translations/en.json", "w") as f:
    json.dump(t_en, f, indent=2)
    f.close()

with open("custom_components/bluetti_bt/translations/de.json", "w") as f:
    json.dump(t_de, f, indent=2)
    f.close()
