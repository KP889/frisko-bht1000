# Frisko BHT-1000
Integracja Home Assistant dla wielu termostatów BHT-1000-M na jednej magistrali Modbus RTU.

## Konfiguracja
Najpierw podaj parametry magistrali (`/dev/ttyUSB0`, 9600, 8N1), następnie dodawaj termostaty pojedynczo: nazwa pomieszczenia + adres Modbus.

## Rejestry
0 zasilanie, 1 temperatura, 3 grzanie, 8 AUTO/RĘCZNY, 9 temperatura zadana. Temperatury są skalowane ×0,5.

> Alpha: wyłącz starą sekcję `modbus:` używającą tego samego portu przed testem.
