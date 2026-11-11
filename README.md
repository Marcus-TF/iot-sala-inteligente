# Sala inteligente: atividade de Fundamentos de IoT

Monitoramento de temperatura e umidade de uma sala de aula com ventilação automática.

- `wokwi/`: projeto do ESP32 (`main.py`, `diagram.json`). Use em um novo projeto ESP32 MicroPython no Wokwi.
- `nodered/flows.json`: fluxo do Node-RED (regra, MQTT, dashboard, CSV). Requer `@flowfuse/node-red-dashboard`.
- `simulacao/`: broker local (`broker.js`), dispositivo simulado (`dispositivo.js`) e assinante (`assinante.js`).
- `evidencias/`: captura do dashboard e logs da execução de teste.
- `relatorio/relatorio-iot.pdf`: relatório (edite `relatorio.html` e gere de novo).

Passo a passo completo em `COMO-TESTAR.txt`.

Teste local sem Wokwi: `cd simulacao && npm i`, `node broker.js`, suba o Node-RED com `flows.json` e rode `node dispositivo.js`. Painel em `/dashboard/monitor`.
