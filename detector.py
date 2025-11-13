import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import re


# ============================================
# 1. Carregar Dataset
# ============================================
def carregar_dataset():
    with open("dataset/suspeitos.txt", "r", encoding="utf-8") as f:
        suspeitos = f.read().splitlines()

    with open("dataset/seguros.txt", "r", encoding="utf-8") as f:
        seguros = f.read().splitlines()

    textos = suspeitos + seguros
    rotulos = ["suspeito"] * len(suspeitos) + ["seguro"] * len(seguros)

    return textos, rotulos


# ============================================
# 2. Treinar Modelo
# ============================================
def treinar_modelo():
    textos, rotulos = carregar_dataset()

    vetorizador = CountVectorizer()
    X = vetorizador.fit_transform(textos)
    y = rotulos

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    modelo = MultinomialNB()
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    print("=== Relatório de Desempenho ===")
    print(classification_report(y_test, y_pred))

    return modelo, vetorizador


# ============================================
# 3. Classificação
# ============================================
def classificar_texto(modelo, vetorizador, texto):
    texto_vetor = vetorizador.transform([texto])
    pred = modelo.predict(texto_vetor)[0]
    return pred


# ============================================
# 4. Detector de Links Suspeitos
# ============================================
def detectar_links_suspeitos(texto):
    padrao_url = r'(https?://[^\s]+)'
    urls = re.findall(padrao_url, texto)

    if not urls:
        return [], []

    urls_suspeitas = []
    urls_normais = []

    encurtadores = [
        "bit.ly", "tinyurl", "t.co", "cutt.ly", "rb.gy",
        "is.gd", "shorte.st", "ow.ly", "buff.ly"
    ]

    palavras_suspeitas = ["login", "verify", "secure", "update", "confirm"]

    for url in urls:
        url_lower = url.lower()
        suspeita = False

        if any(e in url_lower for e in encurtadores):
            suspeita = True

        if url_lower.count(".") > 3:
            suspeita = True

        if re.search(r"[a-z]+[0-9]+[a-z]+", url_lower):
            suspeita = True

        if len(url_lower) > 80:
            suspeita = True

        if any(p in url_lower for p in palavras_suspeitas):
            suspeita = True

        if suspeita:
            urls_suspeitas.append(url)
        else:
            urls_normais.append(url)

    return urls_normais, urls_suspeitas



# ============================================
# 5. Execução principal
# ============================================
if __name__ == "__main__":
    modelo, vetorizador = treinar_modelo()

    import webbrowser

while True:
    entrada = input("\nDigite uma mensagem para classificar (ou 'sair'):\n> ")
    if entrada.strip().lower() in ("sair", "exit", "quit"):
        break

    # CLASSIFICAÇÃO
    resultado = classificar_texto(modelo, vetorizador, entrada)

    print("\n====================================")
    print("RESULTADO DA ANÁLISE")
    print("====================================")
    print(f"Classificação do texto: {resultado.upper()}")

    # LINKS
    urls_normais, urls_suspeitas = detectar_links_suspeitos(entrada)

    if urls_normais:
        print("\n✔ Links seguros encontrados:")
        for url in urls_normais:
            print(" -", url)

        # Perguntar se deseja abrir cada link seguro
        for url in urls_normais:
            abrir = input(f"\nDeseja abrir o link seguro abaixo? (s/n)\n{url}\n> ")
            if abrir.strip().lower() in ("s", "sim"):
                print("Abrindo link...")
                webbrowser.open(url)

    if urls_suspeitas:
        print("\n⚠ LINKS SUSPEITOS DETECTADOS:")
        for url in urls_suspeitas:
            print(" -", url)
        print("\n⚠ Por segurança, links suspeitos não podem ser abertos.")

    print("\n------------------------------------")
