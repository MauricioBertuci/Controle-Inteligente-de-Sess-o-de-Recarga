from machine import Pin
from time import sleep

# CONFIGURACAO DOS PINOS
led_verde = Pin(9, Pin.OUT)
led_amarelo = Pin(5, Pin.OUT)
led_vermelho = Pin(1, Pin.OUT)

# Limite didatico definido para permitir uma recarga normal no prototipo.
POTENCIA_MINIMA_RECARGA = 1000  # watts

# FUNCAO PARA DESLIGAR TODOS OS LEDS
def desligar_leds():
    led_verde.off()
    led_amarelo.off()
    led_vermelho.off()

# REPRESENTACAO NUMERICA
def mostrar_representacao(valor):
    print("\n--- REPRESENTACAO DE DADOS ---")
    print("Dado escolhido: potencia disponivel")
    print("Decimal:    ", valor)

    if valor >= 0:
        print("Binario:    ", bin(valor)[2:])
        print("Hexadecimal:", hex(valor)[2:].upper())
    else:
        # Para valores negativos, usamos sinal e magnitude para facilitar
        # a leitura didatica no Monitor Serial.
        print("Binario:     -{}".format(bin(abs(valor))[2:]))
        print("Hexadecimal: -{}".format(hex(abs(valor))[2:].upper()))

# PROCESSAMENTO DA SESSAO
def processar_recarga(geracao, consumo):

    energia_disponivel = geracao - consumo

    desligar_leds()

    if energia_disponivel >= POTENCIA_MINIMA_RECARGA:
        status = "RECARGA AUTORIZADA"
        led_verde.on()

    elif energia_disponivel > 0:
        status = "RECARGA REDUZIDA"
        led_amarelo.on()

    else:
        status = "RECARGA BLOQUEADA"
        led_vermelho.on()

    print("\n================================")
    print("   SMART ENERGY CONTROLLER")
    print("================================")

    print("GERACAO:    ", geracao, "W")
    print("CONSUMO:    ", consumo, "W")
    print("DISPONIVEL: ", energia_disponivel, "W")

    print("\nSTATUS:")
    print(status)

    mostrar_representacao(energia_disponivel)

    print("================================")

    return energia_disponivel, status

# TESTES
cenarios = [
    {
        "nome": "SITUACAO 1 - ENERGIA SUFICIENTE",
        "geracao": 4000,
        "consumo": 1500
    },

    {
        "nome": "SITUACAO 2 - ENERGIA LIMITADA",
        "geracao": 1800,
        "consumo": 1500
    },

    {
        "nome": "SITUACAO 3 - ENERGIA INSUFICIENTE",
        "geracao": 1000,
        "consumo": 1800
    }
]

def main():
    while True:

        for cenario in cenarios:

            print("\n\n")
            print(cenario["nome"])

            processar_recarga(
                cenario["geracao"],
                cenario["consumo"]
            )

            sleep(5)

            desligar_leds()
            sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        desligar_leds()
        print("\nSimulacao encerrada.")
