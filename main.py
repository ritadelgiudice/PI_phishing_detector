# ============================================
#  main.py – Integração da IA com a Interface
# ============================================

import re
import docx
import PyPDF2

from detector import treinar_modelo, classificar_texto


# ================================
#  TREINAR O MODELO AO INICIAR
# ================================
try:
    modelo, vetorizador = treinar_modelo()
    print("Modelo de IA carregado com sucesso.")
except Exception as e:
    modelo = None
    vetorizador = None
    print("Erro ao carregar o modelo:", e)


# ================================
#  FUNÇÃO: LIMPAR DADOS PESSOAIS
# ================================
def censurar_dados_pessoais(texto):
    """
    Aplica censura automática a dados sensíveis
    como CPF, RG, telefone, e-mail, CEP etc.
    """

    regras = {
        r"\b\d{3}\.\d{3}\.\d{3}\-\d{2}\b": "[CPF REDIGIDO]",
        r"\b\d{2}\.\d{3}\.\d{3}\-\d\b": "[RG REDIGIDO]",
        r"\b\d{5}\-\d{3}\b": "[CEP REDIGIDO]",
        r"\b(\(?\d{2}\)?\s?)?\d{4,5}\-\d{4}\b": "[TELEFONE REDIGIDO]",
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+": "[EMAIL REDIGIDO]"
    }

    texto_filtrado = texto

    for padrao, substituicao in regras.items():
        texto_filtrado = re.sub(padrao, substituicao, texto_filtrado)

    return texto_filtrado


# ================================
#  FUNÇÃO: PROCESSAR TEXTO
# ================================
def processar_texto(texto_original):
    """
    Esta função é chamada pela interface quando o usuário
    clica no botão "Testar Texto/URL".
    Ela:
    - classifica o texto como seguro/suspeito
    - detecta e censura dados pessoais
    - retorna um relatório formatado
    """

    if modelo is None:
        return "❌ A IA não está disponível (erro ao carregar modelo)."

    # Censura dados pessoais
    texto_censurado = censurar_dados_pessoais(texto_original)

    # Classificação IA
    classificacao = classificar_texto(modelo, vetorizador, texto_original)

    # Build do Relatório
    relatorio = [
        "===== ANÁLISE DA IA =====\n",
        f"🔍 Classificação da mensagem: **{classificacao.upper()}**\n",
        "===== TEXTO COM DADOS PROTEGIDOS =====\n",
        texto_censurado,
        "\n======================================"
    ]

    return "\n".join(relatorio)


# Regex para detectar URLs
REGEX_URL = r"(https?://[^\s]+)"

def analisar_links(texto, modelo, vetorizador):
    """
    Retorna uma lista de dicionários:
    [
      {"url": "http://...", "status": "SEGURO"},
      {"url": "http://...", "status": "MALICIOSO"}
    ]
    """

    links = re.findall(REGEX_URL, texto)
    resultado = []

    for link in links:
        classificacao = classificar_texto(modelo, vetorizador, link)

        resultado.append({
            "url": link,
            "status": classificacao.upper()
        })

    return resultado


# ================================
#  FUNÇÃO: LER ARQUIVO PDF
# ================================
def ler_pdf(caminho):
    try:
        with open(caminho, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            texto = ""
            for pagina in reader.pages:
                texto += pagina.extract_text() + "\n"
            return texto
    except Exception as e:
        return f"[ERRO AO LER PDF] {e}"


# ================================
#  FUNÇÃO: LER ARQUIVO DOCX
# ================================
def ler_docx(caminho):
    try:
        doc = docx.Document(caminho)
        return "\n".join(par.text for par in doc.paragraphs)
    except Exception as e:
        return f"[ERRO AO LER DOCX] {e}"


# ================================
#  FUNÇÃO: PROCESSAR ARQUIVO
# ================================
def processar_arquivo(caminho):
    """
    Lê PDF ou DOCX, censura dados pessoais, classifica via IA,
    e devolve um relatório completo.
    """

    # Detectar extensão
    if caminho.lower().endswith(".pdf"):
        texto = ler_pdf(caminho)

    elif caminho.lower().endswith(".docx"):
        texto = ler_docx(caminho)

    else:
        return "⚠ Arquivo inválido. Apenas PDF e DOCX são suportados."

    # Censurar
    texto_censurado = censurar_dados_pessoais(texto)

    # Classificação
    classificacao = classificar_texto(modelo, vetorizador, texto)

    relatorio = [
        "======= ANÁLISE DE ARQUIVO =======\n",
        f"📄 Arquivo: {caminho}",
        f"🔍 Classificação IA: **{classificacao.upper()}**\n",
        "======= TEXTO COM DADOS PROTEGIDOS =======\n",
        texto_censurado,
        "\n====================================="
    ]

    return "\n".join(relatorio)
