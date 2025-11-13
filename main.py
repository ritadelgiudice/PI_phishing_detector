from detector import treinar_modelo, classificar_texto

# Treinar o modelo
modelo, vetorizador = treinar_modelo()

print("=== Detector de Phishing ===\n")
texto = input("Digite o texto do e-mail ou mensagem: ")

resultado = classificar_texto(modelo, vetorizador, texto)

print(f"\nClassificação: {resultado.upper()}")
