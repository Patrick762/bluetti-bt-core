"""Import and generate translations."""

import json
import requests
from typing import Literal

# from custom_components.bluetti_bluetooth.const import EntityDetailsMap
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
            "cannot_connect": "[%key:common::config_flow::error::cannot_connect%]",
            "no_unconfigured_devices": "No unconfigured devices",
            "unreachable": "[%key:common::config_flow::error::cannot_connect%]",
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
            "already_configured": "Gerät ist schon konfiguriert",
            "cannot_connect": "Verbindung fehlgeschlagen",
            "no_unconfigured_devices": "Keine unkonfigurierten Geräte",
            "unreachable": "Verbindung fehlgeschlagen",
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

        args = []
        if "unit" in field:
            args.append(f'unit="{field["unit"]}"')
        if "category" in field and field["category"] != "config":
            args.append(f'category=EntityCategory.{field["category"].upper()}')
        if "sensor" in field:
            args.append(f'device_class=SensorDeviceClass.{field["sensor"].upper()}')
        if "state_type" in field:
            args.append(f'state_class=SensorStateClass.{field["state_type"].upper()}')

        if args:
            body = "".join(f"\n        {a}," for a in args)
            line = f"{f_name}: DetailsMapping({body}\n    ),"
        else:
            line = f"{f_name}: DetailsMapping(),"

        details[f_name] = line

details = [l for l in details.values()]

const_py = f"""\"\"\"Constants for the Bluetti Bluetooth integration.\"\"\"

from dataclasses import dataclass

from bluetti_bt_lib import FieldName

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import EntityCategory

DOMAIN = "bluetti_bluetooth"

CONF_ENCRYPTION = "encryption"
CONF_SERIAL = "serial"


@dataclass
class DetailsMapping:
    \"\"\"Details Mapping for Entities.\"\"\"

    unit: str | None = None
    category: EntityCategory | None = None
    device_class: SensorDeviceClass | None = None
    state_class: SensorStateClass | None = None


ENTITY_DETAILS_MAPPING: dict[FieldName, DetailsMapping] = {{
    {'\n\t'.join(details)}
}}
""".replace("\t", "    ")

with open("custom_components/bluetti_bluetooth/const.py", "w") as f:
    f.write(const_py)
    f.close()


def get_type(field_name: str) -> EntityType:
    # TODO based on p_json
    return "sensor"


needed_fields: set[str] = {
    field["name"]
    for proto in p_json
    if proto["comm_type"] == "bt"
    for field in proto["fields"]
    if field["name"] in FieldName
}


def build_entity_translations(translations: dict[str, str]) -> EntityTranslations:
    t_entity: EntityTranslations = {}

    for field_name, value in translations.items():
        if field_name not in needed_fields:
            continue

        f_type = get_type(field_name)
        t_entity.setdefault(f_type, {})[field_name] = {"name": value}

    return t_entity


for locale, target in (("en", t_en), ("de", t_de)):
    if locale in t_json:
        target["entity"] = build_entity_translations(t_json[locale])

with open("custom_components/bluetti_bluetooth/strings.json", "w") as f:
    json.dump(t_en, f, indent=2)
    f.close()

# Custom component only

with open("custom_components/bluetti_bluetooth/translations/en.json", "w") as f:
    json.dump(t_en, f, indent=2)
    f.close()

with open("custom_components/bluetti_bluetooth/translations/de.json", "w") as f:
    json.dump(t_de, f, indent=2)
    f.close()
