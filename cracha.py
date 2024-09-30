from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry

def criar_cracha(nome, validade, caminho_qr, caminho_cracha):
    # Dimensões do crachá em pixels (9cm x 5cm)
    largura = int(9 * 37.795)  # 9cm em pixels
    altura = int(5 * 37.795)    # 5cm em pixels

    # Cria uma imagem em branco
    cracha = Image.new('RGB', (largura, altura), color='white')  # Fundo branco
    draw = ImageDraw.Draw(cracha)

    # Fonte para o nome e validade (ajuste o caminho da fonte conforme necessário)
    try:
        fonte = ImageFont.truetype("arial.ttf", 24)  # Altere o tamanho conforme necessário
    except IOError:
        fonte = ImageFont.load_default()

    # Centraliza o texto do nome
    texto_nome = nome
    # Usando textbbox para obter as dimensões
    texto_bbox = draw.textbbox((0, 0), texto_nome, font=fonte)
    texto_largura = texto_bbox[2] - texto_bbox[0]  # largura
    draw.text(((largura - texto_largura) / 2, 10), texto_nome, fill="black", font=fonte)

    # Adiciona o campo de validade ao crachá
    validade_texto = f"Válido até: {validade}"
    validade_bbox = draw.textbbox((0, 0), validade_texto, font=fonte)
    validade_largura = validade_bbox[2] - validade_bbox[0]  # largura
    draw.text(((largura - validade_largura) / 2, 40), validade_texto, fill="black", font=fonte)

    # Adiciona o QR Code ao crachá
    qr_img = Image.open(caminho_qr).convert("RGBA")  # Converte para RGBA para evitar fundo preto
    qr_img = qr_img.resize((100, 100))  # Ajusta o tamanho do QR Code
    cracha.paste(qr_img, ((largura - 100) // 2, 70), qr_img)  # Usa o QR Code com transparência

    # Salva o crachá
    cracha.save(caminho_cracha)

def selecionar_qr_code():
    caminho_qr = filedialog.askopenfilename(title="Selecione a imagem do QR Code", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
    entry_qr_code.delete(0, tk.END)  # Limpa o campo de entrada
    entry_qr_code.insert(0, caminho_qr)  # Insere o caminho selecionado

def gerar_cracha():
    nome = entry_nome.get()  # Mantém o nome original
    validade = entry_validade.get()
    caminho_qr = entry_qr_code.get()  # Obtém o caminho do QR Code a partir do campo de entrada

    if not nome or not validade or not caminho_qr:
        messagebox.showwarning("Entrada inválida", "Por favor, preencha todos os campos.")
        return

    ano_atual = datetime.now().year
    nome_arquivo = f"{nome.replace(' ', '_')}_{ano_atual}.png"  # Nome automático do arquivo com espaços substituídos por sublinhados

    # Escolher o local para salvar, usando o nome automático
    caminho_cracha = filedialog.asksaveasfilename(defaultextension=".png",
                                                    initialfile=nome_arquivo,
                                                    filetypes=[("PNG files", "*.png")],
                                                    title="Salvar Crachá como")
    
    if not caminho_cracha:  # Verifica se o usuário cancelou o diálogo
        return

    criar_cracha(nome, validade, caminho_qr, caminho_cracha)
    messagebox.showinfo("Sucesso", f"Crachá gerado com sucesso: {caminho_cracha}")

# Criação da interface gráfica
root = tk.Tk()
root.title("Gerador de Crachás")

# Define o ícone da janela
root.iconbitmap("icone_cracha.ico")  # Substitua pelo nome do seu arquivo .ico

# Aumenta o tamanho da janela
root.geometry("400x350")  # Largura x Altura

# Labels e entradas
label_nome = tk.Label(root, text="Nome:", font=("Arial", 14))  # Removido o bg
label_nome.pack(pady=(10, 5))
entry_nome = tk.Entry(root, font=("Arial", 14), width=30)
entry_nome.pack(pady=(0, 10))

label_validade = tk.Label(root, text="Validade:", font=("Arial", 14))  # Removido o bg
label_validade.pack(pady=(10, 5))
entry_validade = DateEntry(root, font=("Arial", 14), width=30, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
entry_validade.pack(pady=(0, 10))

label_qr_code = tk.Label(root, text="QR Code:", font=("Arial", 14))  # Removido o bg
label_qr_code.pack(pady=(10, 5))
entry_qr_code = tk.Entry(root, font=("Arial", 14), width=30)
entry_qr_code.pack(pady=(0, 10))

# Botão para selecionar o QR Code
botao_selecionar_qr = tk.Button(root, text="Selecionar QR Code", command=selecionar_qr_code, font=("Arial", 12), bg="#4CAF50", fg="white")
botao_selecionar_qr.pack(pady=(10, 5))

# Botão para gerar crachá
botao_gerar = tk.Button(root, text="Gerar Crachá", command=gerar_cracha, font=("Arial", 12), bg="#2196F3", fg="white")
botao_gerar.pack(pady=(10, 10))

root.mainloop()
