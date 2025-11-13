import re

def carregar_listas(arquivo_suspeitos="suspeitos.txt", arquivo_seguros="seguros.txt"):
    with open("dataset/suspeitos.txt", "r", encoding="utf-8") as f:
        suspeitas = [linha.strip() for linha in f if linha.strip()]

    with open("dataset/seguros.txt", "r", encoding="utf-8") as f:
        seguras = [linha.strip() for linha in f if linha.strip()]

    return seguras, suspeitas


def analisar_mensagem(texto, seguras, suspeitas):
    texto_lower = texto.lower()

    score_suspeita = 0
    for padrao in suspeitas:
        if padrao.lower() in texto_lower:
            score_suspeita += 1

    score_segura = 0
    for padrao in seguras:
        if padrao.lower() in texto_lower:
            score_segura += 1

    if score_suspeita > score_segura:
        return "SUSPEITA"
    elif score_segura > score_suspeita:
        return "SEGURA"
    else:
        return "INDEFINIDO"

import re

def detectar_links_suspeitos(texto):
    # Captura qualquer URL no texto
    padrao_url = r'(https?://[^\s]+)'
    urls = re.findall(padrao_url, texto)

    if not urls:
        return [], []

    urls_suspeitas = []
    urls_normais = []

    for url in urls:
        url_lower = url.lower()

        # Heurísticas de suspeita
        suspeita = False

        # 1. Links encurtados
        encurtadores = [
            "bit.ly", "tinyurl", "t.co", "cutt.ly", "rb.gy",
            "is.gd", "shorte.st", "ow.ly", "buff.ly"
        ]
        if any(e in url_lower for e in encurtadores):
            suspeita = True

        # 2. Subdomínios estranhos
        if url_lower.count(".") > 3:
            suspeita = True

        # 3. Domínios com números no lugar de letras
        if re.search(r"[a-z]+[0-9]+[a-z]+", url_lower):
            suspeita = True

        # 4. URL extremamente longa
        if len(url_lower) > 80:
            suspeita = True

        # 5. Sinais de phishing (login, verify, secure, update)
        palavras_suspeitas = ["login", "verify", "secure", "update", "confirm"]
        if any(p in url_lower for p in palavras_suspeitas):
            suspeita = True

        if suspeita:
            urls_suspeitas.append(url)
        else:
            urls_normais.append(url)

    return urls_normais, urls_suspeitas


if __name__ == "__main__":
    seguras, suspeitas = carregar_listas()

    texto = input("Digite a mensagem para análise: ")
    resultado = analisar_mensagem(texto, seguras, suspeitas)

    print(f"\nResultado da análise: {resultado}")
