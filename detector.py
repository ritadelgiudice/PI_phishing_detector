import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def carregar_dataset():
    with open("dataset/suspeitos.txt", "r", encoding="utf-8") as f:
        suspeitos = f.read().splitlines()

    with open("dataset/seguros.txt", "r", encoding="utf-8") as f:
        seguros = f.read().splitlines()

    textos = suspeitos + seguros
    rotulos = ["suspeito"] * len(suspeitos) + ["seguro"] * len(seguros)

    return textos, rotulos


from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def treinar_modelo():
    textos, rotulos = carregar_dataset()

    vetorizador = CountVectorizer()
    X = vetorizador.fit_transform(textos)
    y = rotulos

    # Dividir dataset em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42)

    modelo = MultinomialNB()
    modelo.fit(X_train, y_train)

    # Avaliação do modelo
    y_pred = modelo.predict(X_test)
    print("=== Relatório de Desempenho ===")
    print(classification_report(y_test, y_pred))

    return modelo, vetorizador



def classificar_texto(modelo, vetorizador, texto):
    texto_vetor = vetorizador.transform([texto])
    pred = modelo.predict(texto_vetor)[0]
    return pred
