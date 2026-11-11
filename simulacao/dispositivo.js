const mqtt = require('mqtt');

const SALA = 'ce01';
const BASE = `unifor/iot/sala/${SALA}`;
const TOTAL = Number(process.env.LEITURAS || 40);
const INTERVALO_MS = Number(process.env.INTERVALO_MS || 500);

const cliente = mqtt.connect('mqtt://localhost:1883');
let temperatura = 25;
let umidade = 62;
let ventilador = false;
let enviadas = 0;

cliente.on('connect', () => {
  cliente.subscribe(`${BASE}/ventilador/comando`, { qos: 1 });
  publicarEstado();
  setInterval(ciclo, INTERVALO_MS);
});

cliente.on('message', (topico, mensagem) => {
  let comando;
  try {
    comando = JSON.parse(mensagem.toString());
  } catch {
    return;
  }
  if (comando.acao === 'LIGAR') ventilador = true;
  else if (comando.acao === 'DESLIGAR') ventilador = false;
  else return;
  console.log('comando', comando.acao, comando.motivo);
  publicarEstado();
});

function publicarEstado() {
  cliente.publish(`${BASE}/ventilador/estado`, JSON.stringify({ ligado: ventilador, ts: Math.floor(Date.now() / 1000) }), { retain: true });
}

function ciclo() {
  const aquecimento = 0.55 + Math.random() * 0.3;
  const resfriamento = ventilador ? 1.1 + Math.random() * 0.3 : 0;
  temperatura = Math.round((temperatura + aquecimento - resfriamento) * 10) / 10;
  umidade = Math.round(Math.min(90, Math.max(30, umidade + (Math.random() - 0.5) * 2)) * 10) / 10;
  const carga = { sala: SALA, temperatura, umidade, ts: Math.floor(Date.now() / 1000) };
  cliente.publish(`${BASE}/sensores`, JSON.stringify(carga));
  enviadas += 1;
  console.log(enviadas, JSON.stringify(carga));
  if (enviadas >= TOTAL) setTimeout(() => cliente.end(false, () => process.exit(0)), 1000);
}
