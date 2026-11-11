import network
import time
import json
import machine
import dht
from umqtt.simple import MQTTClient

WIFI_SSID = "Wokwi-GUEST"
WIFI_SENHA = ""
BROKER = "broker.hivemq.com"
SALA = "ce01"
CLIENT_ID = "esp32-sala-" + SALA + "-" + str(time.ticks_ms())

TOPICO_SENSORES = b"unifor/iot/sala/" + SALA.encode() + b"/sensores"
TOPICO_COMANDO = b"unifor/iot/sala/" + SALA.encode() + b"/ventilador/comando"
TOPICO_ESTADO = b"unifor/iot/sala/" + SALA.encode() + b"/ventilador/estado"

INTERVALO_S = 5

sensor = dht.DHT22(machine.Pin(15))
rele = machine.Pin(26, machine.Pin.OUT)
led = machine.Pin(2, machine.Pin.OUT)
ventilador_ligado = False


def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_SENHA)
    while not wlan.isconnected():
        time.sleep(0.3)
    print("wifi ok", wlan.ifconfig()[0])


def aplicar_estado(ligado):
    global ventilador_ligado
    ventilador_ligado = ligado
    rele.value(1 if ligado else 0)
    led.value(1 if ligado else 0)
    print("ventilador", "LIGADO" if ligado else "DESLIGADO")


def publicar_estado(cliente):
    carga = json.dumps({"ligado": ventilador_ligado, "ts": time.time()})
    cliente.publish(TOPICO_ESTADO, carga, retain=True)


def ao_receber(topico, mensagem):
    try:
        comando = json.loads(mensagem)
        acao = comando.get("acao")
        print("comando recebido", acao)
    except (ValueError, AttributeError):
        print("comando invalido", mensagem)
        return
    if acao == "LIGAR":
        aplicar_estado(True)
    elif acao == "DESLIGAR":
        aplicar_estado(False)
    else:
        print("acao desconhecida", acao)
        return
    publicar_estado(cliente)


def conectar_broker():
    c = MQTTClient(CLIENT_ID, BROKER, keepalive=60)
    c.set_callback(ao_receber)
    c.connect()
    c.subscribe(TOPICO_COMANDO)
    print("mqtt ok")
    return c


def ler_sensor():
    try:
        sensor.measure()
        return sensor.temperature(), sensor.humidity()
    except OSError as erro:
        print("falha na leitura", erro)
        return None


conectar_wifi()
cliente = conectar_broker()
aplicar_estado(False)
publicar_estado(cliente)

ultima_leitura = 0
while True:
    try:
        cliente.check_msg()
        agora = time.ticks_ms()
        if time.ticks_diff(agora, ultima_leitura) >= INTERVALO_S * 1000:
            ultima_leitura = agora
            leitura = ler_sensor()
            if leitura:
                carga = json.dumps({
                    "sala": SALA,
                    "temperatura": leitura[0],
                    "umidade": leitura[1],
                    "ts": time.time(),
                })
                cliente.publish(TOPICO_SENSORES, carga)
                print("publicado", carga)
        time.sleep_ms(100)
    except OSError as erro:
        print("conexao perdida", erro)
        time.sleep(2)
        cliente = conectar_broker()
