"""Import and generate translations."""

import json
import requests
from typing import Literal

t_url = "https://patrick762.github.io/bluetti-registers/translations.json"
p_url = "https://patrick762.github.io/bluetti-registers/protocols.json"

t_json: dict[str, dict[str, str]] = requests.get(t_url).json()

t_en = {
    "config": {
        "abort": {
            "already_configured": "[%key:common::config_flow::abort::already_configured_device%]",
            "unsupported_device": "Unsupported device",
            "no_unconfigured_devices": "No unconfigured devices",
        },
        "step": {
            "user": {"description": "Do you want to add this device?"},
            "reconfigure": {"description": "Do you want to reconfigure this device?"},
        },
    },
    "entity": {},
}

t_de = {
    "config": {
        "abort": {
            "already_configured": "",
            "unsupported_device": "Gerät wird nicht unterstützt",
            "no_unconfigured_devices": "Keine unkonfigurierten Geräte",
        },
        "step": {
            "user": {"description": "Möchtest du das Gerät hinzufügen?"},
            "reconfigure": {"description": "Möchtest du das Gerät neu konfigurieren?"},
        },
    },
    "entity": {},
}

type EntityType = Literal["binary_sensor", "sensor", "switch", "select"]
type EntityTranslations = dict[EntityType, dict[str, dict[Literal["name"], str]]]


def get_type(field_name: str) -> EntityType:
    # TODO
    return "sensor"


t_entity: EntityTranslations = {}

for locale, translations in t_json.items():
    for field_name, value in translations.items():
        f_type = get_type(field_name)

        if f_type not in t_entity.keys():
            t_entity.setdefault(f_type, {})

        t_entity[f_type].setdefault(field_name, {})
        t_entity[f_type][field_name]["name"] = value

    match (locale):
        case "en":
            t_en["entity"] = t_entity
        case "de":
            t_de["entity"] = t_entity

with open("custom_components/bluetti_bt/strings.json", "w") as f:
    json.dump(t_en, f, indent=4)
    f.close()

# Custom component only

with open("custom_components/bluetti_bt/translations/en.json", "w") as f:
    json.dump(t_en, f, indent=4)
    f.close()

with open("custom_components/bluetti_bt/translations/de.json", "w") as f:
    json.dump(t_de, f, indent=4)
    f.close()
