import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import re

# 🔹 IMPORTAÇÃO DA IA DO SEU ARQUIVO main.py 🔹
from main import processar_texto, processar_arquivo


# ==========================
#  JANELA PRINCIPAL
# ==========================
janela = tk.Tk()
janela.title("Validador IA de Mensagens e Arquivos")
janela.geometry("600x550")
janela.config(bg="#f7f2d7")  # amarelo manteiga

# ==========================
#  ESTILOS
# ==========================
cor_primaria = "#2b6cb0"        # azul
cor_secundaria = "#f7f2d7"       # amarelo manteiga
cor_botoes = "#4a90e2"          # azul claro
cor_texto = "#ffffff"


# ==========================
#  ÁREA DE TEXTO
# ==========================
label_texto = tk.Label(
    janela,
    text="Digite um texto ou URL para testar:",
    bg=cor_secundaria,
    fg="black",
    font=("Arial", 12, "bold")
)
label_texto.pack(pady=10)

entrada_texto = tk.Text(janela, height=5, width=60, font=("Arial", 11))
entrada_texto.pack(pady=5)


# ==========================
#  BOTÃO: TESTAR URL/TEXTO
#  (AGORA COM BLOQUEIO DE LINKS MALICIOSOS)
# ==========================
padrao_links_suspeitos = r"(http[s]?://[^\s]+(?:\.xyz|\.top|\.ru|\.cn|\.club|\.click|\.work|bit\.ly|tinyurl\.com))"


def testar_url():
    texto = entrada_texto.get("1.0", tk.END).strip()

    if not texto:
        messagebox.showwarning("Aviso", "Digite algo antes de testar.")
        return

    # ==========================
    # 1) SE FOR URL, ANALISAR MALICIOSIDADE
    # ==========================
    if texto.startswith("http://") or texto.startswith("https://"):

        # Detectar se a URL é suspeita
        links_suspeitos = re.findall(padrao_links_suspeitos, texto)

        if links_suspeitos:
            # ❌ LINK SUSPEITO — NUNCA ABRIR
            messagebox.showerror(
                "ALERTA DE SEGURANÇA",
                f"⚠️ O link foi identificado como MALICIOSO:\n\n{texto}\n\n"
                "🚫 Por segurança, o sistema NÃO permitirá abrir este link."
            )
            return

        # 🔹 LINK NORMAL → PERGUNTAR SE DESEJA ABRIR
        resposta = messagebox.askyesno("Abrir Link", "O link parece seguro.\nDeseja abrir no navegador?")
        if resposta:
            webbrowser.open(texto)
        return

    # ==========================
    # 2) SE FOR TEXTO, ENVIAR PARA IA
    # ==========================
    try:
        resultado = processar_texto(texto)

        janela_res = tk.Toplevel()
        janela_res.title("Resultado da IA")
        janela_res.geometry("700x600")

        caixa = tk.Text(janela_res, wrap="word", font=("Arial", 11))
        caixa.insert("1.0", resultado)
        caixa.pack(expand=True, fill="both")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante a análise:\n\n{e}")


btn_testar = tk.Button(
    janela,
    text="Testar Texto/URL",
    bg=cor_primaria,
    fg=cor_texto,
    font=("Arial", 12),
    command=testar_url
)
btn_testar.pack(pady=10)


# ==========================
#  ÁREA DE TREINAMENTO DA IA
# ==========================
label_ia = tk.Label(
    janela,
    text="Treinar IA (carregar novos arquivos de dataset):",
    bg=cor_secundaria,
    fg="black",
    font=("Arial", 12, "bold")
)
label_ia.pack(pady=10)

dataset_textos = []


def carregar_dataset():
    arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo .txt",
        filetypes=[("Arquivos de Texto", "*.txt")]
    )

    if not arquivo:
        return

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            texto = f.read()

        links_detectados = re.findall(padrao_links_suspeitos, texto)

        if links_detectados:
            msg = "⚠️ Links suspeitos encontrados:\n\n"
            msg += "\n".join(links_detectados)
            msg += "\n\nDeseja continuar mesmo assim?"

            if not messagebox.askyesno("Aviso!", msg):
                return

        dataset_textos.append(texto)

        messagebox.showinfo(
            "Dataset carregado",
            f"Arquivo carregado:\n{arquivo}\n\nTotal no dataset: {len(dataset_textos)}"
        )

    except Exception as e:
        messagebox.showerror("Erro ao carregar dataset", f"Ocorreu um erro:\n{e}")


btn_dataset = tk.Button(
    janela,
    text="Carregar Dataset",
    bg=cor_primaria,
    fg=cor_texto,
    font=("Arial", 12),
    command=carregar_dataset
)
btn_dataset.pack(pady=10)


# ==========================
#  BOTÃO DE ARQUIVO PDF/DOCX
# ==========================
label_arq = tk.Label(
    janela,
    text="Selecionar arquivo (PDF/DOCX):",
    bg=cor_secundaria,
    fg="black",
    font=("Arial", 12, "bold")
)
label_arq.pack(pady=10)


def selecionar_arquivo():
    arquivo = filedialog.askopenfilename(
        title="Escolha um arquivo",
        filetypes=[
            ("PDF", "*.pdf"),
            ("Word", "*.docx"),
            ("Todos", "*.*")
        ]
    )

    if not arquivo:
        return

    try:
        resultado = processar_arquivo(arquivo)

        janela_res = tk.Toplevel()
        janela_res.title("Resultado do Arquivo")
        janela_res.geometry("700x600")

        caixa = tk.Text(janela_res, font=("Arial", 11), wrap="word")
        caixa.insert("1.0", resultado)
        caixa.pack(expand=True, fill="both")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar o arquivo:\n\n{e}")


btn_arquivo = tk.Button(
    janela,
    text="Selecionar Arquivo",
    bg=cor_primaria,
    fg=cor_texto,
    font=("Arial", 12),
    command=selecionar_arquivo
)
btn_arquivo.pack(pady=15)


# ==========================
#  EXECUTAR JANELA
# ==========================
janela.mainloop()
