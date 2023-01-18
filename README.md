# [Home Assistant integration] Losses of the Russian army in a war with Ukraine  

This custom [home assistant](https://www.home-assistant.io) integration provides a way to present a live view of Russian army slaughter in a war with Ukraine.  

![UI Lovelace](https://raw.githubusercontent.com/ALX-TH/ha_russiancrimesinua/master/images/card.png)

<img src="https://raw.githubusercontent.com/ALX-TH/ha_russiancrimesinua/master/images/card.png" width=80%>

## Installation  

To install this integration manually you have to download russiancrimesinua and put its content to `config/custom_components/russiancrimesinua` directory.  

## Configuration

After installation of the custom component, it needs to be configured in `configuration.yaml` file.

### Examples  

```yaml
sensor:
    - platform: russiancrimesinua
      name: russiancrimes
```

### Customisation  

```yaml
    sensor.russiancrimesinua_aircraft:
      friendly_name: Літаки
      icon: mdi:airplane
    sensor.russiancrimesinua_artillery:
      friendly_name: Артилерія
      icon: mdi:train-car-flatbed-tank
    sensor.russiancrimesinua_helicopters:
      friendly_name: Гелікоптери
      icon: mdi:helicopter
    sensor.russiancrimesinua_killed:
      friendly_name: Особовий склад
      icon: mdi:face-man
    sensor.russiancrimesinua_shipsboats:
      friendly_name: Кораблі та катери
      icon: mdi:ferry
    sensor.russiancrimesinua_tanks:
      friendly_name: Танки
      icon: mdi:tank
```  

### UI Lovelace  

```yaml
title: War
icon: mdi:alert-decagram
path: war
id: war
cards:

- type: vertical-stack
  cards:
      - type: vertical-stack
        cards:
         - type: markdown
           content: |
              # Шо там по русні

      - type: vertical-stack
        cards:
        - type: entities
          entities:
            - entity: sensor.russiancrimesinua_aircraft
            - entity: sensor.russiancrimesinua_artillery
            - entity: sensor.russiancrimesinua_helicopters
            - entity: sensor.russiancrimesinua_killed
            - entity: sensor.russiancrimesinua_shipsboats
            - entity: sensor.russiancrimesinua_tanks
```  

### Automatization  

```yaml
- id: telegram_command_russia_slaughter
  alias: Telegram - Get Russian slaughter in a war with Ukraine
  trigger:
    platform: event
    event_type: telegram_command
    event_data:
      command: '/russiaslaughter'
  action:
    service: notify.telegram_bot
    data_template:
      message: |
       🙎‍♂️ Особовий склад: {{ states('sensor.russiancrimesinua_killed') | int(default = 0) }}.
       🚀 Артилерія: {{ states('sensor.russiancrimesinua_artillery') | int(default = 0) }}.
       🛩️ Літаки: {{ states('sensor.russiancrimesinua_aircraft') | int(default = 0) }}.
       🚁 Гелікоптери: {{ states('sensor.russiancrimesinua_helicopters') | int(default = 0) }}.
       🛞 Танки: {{ states('sensor.russiancrimesinua_tanks') | int(default = 0) }}.
       🛳️ Кораблі та катери: {{ states('sensor.russiancrimesinua_shipsboats') | int(default = 0) }}.
      title: "🔥 Орієнтовні втрати росії у війні з Україною"
```
