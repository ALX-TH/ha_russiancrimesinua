# Losses of the Russian army in a war with Ukraine  

This custom integration provides a way to present a live view of Russian army slaughter in a war.  

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
