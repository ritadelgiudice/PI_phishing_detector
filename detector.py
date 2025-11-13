import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def treinar_modelo():
    # Exemplos iniciais (podemos expandir depois)
    dados = {
        'texto': [
            "Clique aqui para atualizar sua conta bancária",
            "Você ganhou um prêmio! Envie seus dados agora",
            "Reunião agendada para amanhã às 14h",
            "Pagamento confirmado, obrigado pela compra",
            "Sua senha expirou, redefina agora mesmo",
            "Confirme seus dados para evitar bloqueio da conta"
        ],
        'rotulo': ['suspeito', 'suspeito', 'seguro', 'seguro', 'suspeito', 'suspeito']
    }

    df = pd.DataFrame(dados)

    # Converte texto em números (vetorização)
    vetorizador = CountVectorizer()
    X = vetorizador.fit_transform(df['texto'])
    y = df['rotulo']

    # Treina o modelo
    modelo = MultinomialNB()
    modelo.fit(X, y)

    return modelo, vetorizador


def classificar_texto(modelo, vetorizador, texto):
    texto_vetor = vetorizador.transform([texto])
    predicao = modelo.predict(texto_vetor)[0]
    return predicao
