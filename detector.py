import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import re
import webbrowser
import pdfplumber
import docx

# ============================================
# 0. Detectar e censurar dados pessoais
# ============================================
PADROES_SENSIVEIS = {
    "CPF": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",
    "Telefone": r"\b(?:\(\d{2}\)\s*)?(?:9\d{4}|\d{4})-\d{4}\b",
    "Email": r"\b[\w\.-]+@[\w\.-]+\.\w{2,}\b",
    "RG": r"\b\d{2}\.\d{3}\.\d{3}-\d\b",
    "CEP": r"\b\d{5}-\d{3}\b",
    "Data de Nascimento": r"\b\d{2}/\d{2}/\d{4}\b"
}

def censurar_dados(texto):
    encontrado = {}

    texto_censurado = texto
    for nome, padrao in PADROES_SENSIVEIS.items():
        achados = re.findall(padrao, texto)
        if achados:
            encontrado[nome] = achados
            texto_censurado = re.sub(padrao, "***CENSURADO***", texto_censurado)

    return texto_censurado, encontrado


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
# 3. Classificar Texto com o Modelo
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

        if any(e in url_lower for e in encurtadores): suspeita = True
        if url_lower.count(".") > 3: suspeita = True
        if re.search(r"[a-z]+[0-9]+[a-z]+", url_lower): suspeita = True
        if len(url_lower) > 80: suspeita = True
        if any(p in url_lower for p in palavras_suspeitas): suspeita = True

        if suspeita:
            urls_suspeitas.append(url)
        else:
            urls_normais.append(url)

    return urls_normais, urls_suspeitas


# ============================================
# 5. Leitura de PDF
# ============================================
def ler_pdf(caminho):
    try:
        with pdfplumber.open(caminho) as pdf:
            texto = ""
            for pagina in pdf.pages:
                texto += pagina.extract_text() + "\n"
            return texto.strip()
    except:
        return ""


# ============================================
# 6. Leitura de DOCX
# ============================================
def ler_docx(caminho):
    try:
        doc = docx.Document(caminho)
        return "\n".join([p.text for p in doc.paragraphs])
    except:
        return ""


# ============================================
# 7. Execução Principal
# ============================================
if __name__ == "__main__":
    modelo, vetorizador = treinar_modelo()

    while True:
        entrada = input("\nDigite uma mensagem ou caminho de arquivo (ou 'sair'):\n> ")

        if entrada.lower() in ("sair", "exit"):
            break

        # PDF
        if entrada.endswith(".pdf"):
            print("\n📄 Lendo PDF...")
            entrada = ler_pdf(entrada)

        # DOCX
        if entrada.endswith(".docx"):
            print("\n📄 Lendo arquivo .docx...")
            entrada = ler_docx(entrada)

        # CENSURA DE DADOS PESSOAIS
        texto_censurado, dados = censurar_dados(entrada)

        # CLASSIFICA
        resultado = classificar_texto(modelo, vetorizador, entrada)

        print("\n====================================")
        print("RESULTADO DA ANÁLISE")
        print("====================================")
        print(f"Classificação do texto: {resultado.upper()}")

        # MOSTRAR DADOS PESSOAIS
        if dados:
            print("\n⚠ Dados sensíveis encontrados:")
            for tipo, itens in dados.items():
                print(f" - {tipo}: {', '.join(itens)}")
        else:
            print("\nNenhum dado sensível encontrado.")

        print("\nTexto após censura:")
        print(texto_censurado)

        # LINKS
        urls_normais, urls_suspeitas = detectar_links_suspeitos(entrada)

        if urls_normais:
            print("\n✔ Links seguros encontrados:")
            for url in urls_normais:
                print(" -", url)

            for url in urls_normais:
                abrir = input(f"\nDeseja abrir o link seguro abaixo? (s/n)\n{url}\n> ")
                if abrir.lower() in ("s", "sim"):
                    print("Abrindo link...")
                    webbrowser.open(url)

        if urls_suspeitas:
            print("\n⚠ LINKS SUSPEITOS DETECTADOS:")
            for url in urls_suspeitas:
                print(" -", url)

        print("\n------------------------------------")
