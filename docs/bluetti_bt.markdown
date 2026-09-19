---
title: Bluetti BT
description: Instructions on setting up Bluetti Bluetooth devices within Home Assistant.
ha_category:
  - Energy
  - Sensor
ha_iot_class: Local Polling
ha_release: 0.111
ha_config_flow: true
ha_codeowners:
  - '@Patrick762'
ha_domain: bluetti_bt
ha_platforms:
  - sensor
ha_integration_type: device
---

The **Bluetti BT** {% term integration %} allows you to integrate your [Bluetti Devices](https://bluetti.com/products) into Home Assistant.

## Supported devices

The following devices are known to be supported by the integration:
- AC70
- AC180
- EB3A
- EP600
- Handsfree 1

## Unsupported devices

The following devices are not supported by the integration:
- Balco260

## Prerequisites

Before setting up the integration, make sure you have a {% term %}

## Configuration

To add the **Bluetti BT** device to your Home Assistant instance, configure the discovered device.

Manual configuration is **not** possible.

## Supported functionality

There is currently support for the following device types within Home Assistant:

- [Sensor](#sensor)

### Sensor

The following sensors are added for each Bluetti device:

- Charge - Percent charge remaining in %

## Known Limitations

- Some devices don't support the bluetooth protocols used by this integration. Those devices might get detected by the integration but you don't get any data from them.
- Since this integration is based on reverse engineering results, firmware updates might break this integration without any warning. In that case you can try to reconfigure the integration. If this doesn't help you can create a new issue.
