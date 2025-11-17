# 🛡️ Projeto: Detector Inteligente de Mensagens, Arquivos e URLs

**Descrição e Desenvolvedores**

Este é um projeto integrado desenvolvido para o módulo de Inteligencia Artificial do curso de Análise e Desenvolvimento de sistemas e Gestão de Tecnologia da informação para a UNIFEOB.

Feito por:
Rita de Cássia Del Giudice Conceição - 24000469

Este projeto utiliza **Python + IA + Interface Gráfica (Tkinter)** para criar um sistema capaz de:

* Classificar mensagens como **seguras** ou **suspeitas** usando Machine Learning
* Detectar e **censurar dados pessoais** (CPF, e-mail, telefone etc.)
* Ler arquivos **PDF** e **DOCX** automaticamente
* Detectar URLs **seguras** e **suspeitas**
* Abrir links seguros com confirmação do usuário
* Interface gráfica moderna com tema **azul e amarelo manteiga**
* Treinar o modelo de IA diretamente pela interface

Este README documenta todo o funcionamento, instalação e uso do sistema.

---

# 1. Funcionalidades Principais

### 1.1 Classificação de Mensagens

O sistema utiliza **Naive Bayes (MultinomialNB)** para classificar textos como:

* **SEGURO**
* **SUSPEITO**

Treinamento feito com os arquivos:

* `dataset/seguros.txt`
* `dataset/suspeitos.txt`

---

### 1.2 Detecção e Censura de Dados Pessoais

O sistema identifica automaticamente:

* CPF
* RG
* E-mail
* Telefone
* CEP
* Data de nascimento

Tudo é substituído por:

```
***CENSURADO***
```

---

### 🔷 1.3 Detector de Links Suspeitos

O programa identifica:

* Encurtadores (bit.ly, tinyurl etc.)
* URLs muito longas
* URLs com caracteres suspeitos
* Palavras perigosas (login, verify, secure...)

Caso o link seja seguro, pergunta ao usuário:

```
Deseja abrir este link seguro? (s/n)
```

---

### 🔷 1.4 Leitura de Arquivos

O sistema lê automaticamente:

📄 **PDF** – usando `pdfplumber`
📝 **DOCX** – usando `python-docx`

O texto é extraído e enviado para análise.

---

### 🔷 2.5 Interface Gráfica Moderna

A interface Tkinter inclui:

* Botões estilizados (azul + amarelo manteiga)
* Campo de texto
* Campo para URL
* Botão para selecionar arquivos
* Área de exibição do resultado

O objetivo final é deixar a interface o mais **bonita e funcional possível**.

---

# 📌 2. Como Usar o Sistema

## ▶️ 2.1 Rodar o Programa

No terminal:

```bash
python interface.py
```

A interface será aberta automaticamente.

---

# 2.2 Funcionalidades da Interface

## Inserir Texto Manualmente

1. Digite um texto ou URL no campo principal
2. Clique em **ANALISAR**
3. O sistema irá:

   * Censurar dados pessoais
   * Classificar o texto
   * Detectar links suspeitos ou seguros

---

## Enviar Arquivo PDF ou DOCX

1. Clique em **CARREGAR ARQUIVO**
2. Escolha um PDF ou DOCX
3. O sistema extrai o texto automaticamente
4. Todo o conteúdo é analisado pela IA

---

## Treinar a IA Novamente

1. Clique em **TREINAR MODELO**
2. O sistema lê:
   * `dataset/seguros.txt`
   * `dataset/suspeitos.txt`
3. Um novo modelo é criado
4. As métricas aparecerão no terminal

---

# 3. Atualizações Futuras

O projeto permite expansão. Alguns passos sugeridos:

* ✓ Melhorar a interface com telas separadas
* ✓ Criar leitura automática dew e-mail
* ✓ Criar sistema de histórico
* ✓ Exportar análises para PDF
* ✓ Treinar modelo com mais dados

---