#!/usr/bin/env python3
"""
Teste Bruno
Script para somar dois números.
Lê dois valores (inteiros ou floats) do teclado, trata
erro de conversão e exibe a soma.
"""

def main():
    try:
        a = float(input("Digite o primeiro número: "))
        b = float(input("Digite o segundo número: "))
    except ValueError:
        print("Entrada inválida. Por favor, digite valores numéricos.")
        return

    soma = a + b
    print(f"A soma de {a} e {b} é {soma}")


if __name__ == "__main__":
    main()