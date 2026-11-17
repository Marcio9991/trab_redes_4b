#!/usr/bin/env python3
"""Calculadora manual de sub-redes IPv4 para uso no terminal."""


def para_ipv4(numero):
    """Converte um inteiro de 32 bits para a notação IPv4 pontuada."""
    return ".".join(
        str((numero >> deslocamento) & 255)
        for deslocamento in (24, 16, 8, 0)
    )


def ler_entrada():
    while True:
        entrada = input("Digite o IPv4 e o prefixo (ex.: 192.168.001.010/24): ").strip()

        partes_barra = entrada.split("/")
        if len(partes_barra) != 2:
            print("Erro: use exatamente o formato 000.000.000.000/00. Tente novamente.\n")
            continue

        endereco_texto, prefixo_texto = partes_barra
        octetos_texto = endereco_texto.split(".")

        if len(octetos_texto) != 4 or any(not octeto.isdigit() or not 1 <= len(octeto) <= 3 for octeto in octetos_texto):
            print("Erro: digite quatro octetos IPv4 de 1 a 3 algarismos, por exemplo 192.168.1.10/24. Tente novamente.\n")
            continue

        if not prefixo_texto.isdigit() or len(prefixo_texto) > 2:
            print("Erro: o prefixo deve ser um número entre 0 e 32. Tente novamente.\n")
            continue

        octetos = [int(octeto) for octeto in octetos_texto]
        prefixo = int(prefixo_texto)

        if any(octeto > 255 for octeto in octetos):
            print("Erro: cada octeto deve estar entre 000 e 255. Tente novamente.\n")
            continue

        if prefixo > 32:
            print("Erro: o prefixo deve estar entre 00 e 32. Tente novamente.\n")
            continue

        return octetos, prefixo


def calcular(octetos, prefixo):
    # Monta o endereço IPv4 como um inteiro de 32 bits.
    endereco_numero = 0
    for octeto in octetos:
        endereco_numero = (endereco_numero << 8) | octeto

    # Cria a máscara sem usar módulos externos.
    if prefixo == 0:
        mascara_numero = 0
    else:
        mascara_numero = (0xFFFFFFFF << (32 - prefixo)) & 0xFFFFFFFF

    rede_numero = endereco_numero & mascara_numero
    broadcast_numero = rede_numero | (0xFFFFFFFF ^ mascara_numero)
    bits_hosts = 32 - prefixo

    # Para /31, os dois endereços podem ser usados em enlaces ponto a ponto;
    # para /32, o único endereço é o próprio host.
    if prefixo == 31:
        quantidade_hosts = 2
        primeiro_host = rede_numero
        ultimo_host = broadcast_numero
    elif prefixo == 32:
        quantidade_hosts = 1
        primeiro_host = rede_numero
        ultimo_host = rede_numero
    else:
        quantidade_hosts = (1 << bits_hosts) - 2
        primeiro_host = rede_numero + 1
        ultimo_host = broadcast_numero - 1

    faixa = "não há"
    if quantidade_hosts > 0:
        faixa = f"{para_ipv4(primeiro_host)} - {para_ipv4(ultimo_host)}"

    endereco_formatado = ".".join(str(octeto) for octeto in octetos)
    print("\n--- Resultado ---")
    print(f"Endereço: {endereco_formatado}")
    print(f"Máscara: {para_ipv4(mascara_numero)}")
    print(f"Prefixo: /{prefixo:02d}")
    if prefixo == 31:
        print("Rede: não há (os dois endereços são utilizáveis)")
        print("Broadcast: não há")
    elif prefixo == 32:
        print(f"Rede: {para_ipv4(rede_numero)}")
        print("Broadcast: não há")
    else:
        print(f"Rede: {para_ipv4(rede_numero)}")
        print(f"Broadcast: {para_ipv4(broadcast_numero)}")
    print(f"Quantidade de Hosts: {quantidade_hosts}")
    print(f"Faixa de Endereços disponíveis: {faixa}")


def main():
    try:
        octetos, prefixo = ler_entrada()
    except (EOFError, KeyboardInterrupt):
        print("\nOperação encerrada.")
        return

    calcular(octetos, prefixo)


if __name__ == "__main__":
    main()
