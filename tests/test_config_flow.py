"""Test the Bluetti Bluetooth config flow."""

from homeassistant.helpers.service_info.bluetooth import BluetoothServiceInfo

service_info = BluetoothServiceInfo(
    name="EB3A",
    address="aa:bb:cc:dd:ee:ff",
    rssi=-63,
    manufacturer_data={},
    service_data={},
    service_uuids=["0000ff00-0000-1000-8000-00805f9b34fb"],
    source="local",
)

# TODO
