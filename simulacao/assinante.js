const mqtt = require('mqtt');
const c = mqtt.connect('mqtt://localhost:1883');
c.on('connect', () => c.subscribe('unifor/iot/sala/ce01/#'));
c.on('message', (t, m) => console.log(t, m.toString()));
