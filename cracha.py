from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry

def ajustar_tamanho_fonte(draw, texto, largura_maxima, fonte_inicial):
    fonte = fonte_inicial
    while True:
        largura_texto = draw.textbbox((0, 0), texto, font=fonte)[2]
        if largura_texto <= largura_maxima:
            break
        novo_tamanho = fonte.size - 1
        fonte = ImageFont.truetype("arial.ttf", novo_tamanho)
    return fonte

def criar_cracha(nome, validade, caminho_qr, caminho_cracha):
    largura = int(5 * 37.795)
    altura = int(9 * 37.795)

    cracha = Image.new('RGB', (largura, altura), color='white')
    draw = ImageDraw.Draw(cracha)

    try:
        fonte_inicial = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        fonte_inicial = ImageFont.load_default()

    nome_fonte = ajustar_tamanho_fonte(draw, nome, largura - 20, fonte_inicial)
    texto_bbox = draw.textbbox((0, 0), nome, font=nome_fonte)
    texto_largura = texto_bbox[2] - texto_bbox[0]
    
    validade_texto = f"Válido até: {validade}"
    validade_fonte = ajustar_tamanho_fonte(draw, validade_texto, largura - 20, fonte_inicial)
    validade_bbox = draw.textbbox((0, 0), validade_texto, font=validade_fonte)
    validade_largura = validade_bbox[2] - validade_bbox[0]

    qr_img = Image.open(caminho_qr).convert("RGBA")
    qr_img = qr_img.resize((110, 110))

    altura_total_texto_qr = texto_bbox[3] + 20 + validade_bbox[3] + 20 + 110
    posicao_base = (altura - altura_total_texto_qr) // 2

    draw.text(((largura - texto_largura) / 2, posicao_base), nome, fill="black", font=nome_fonte)
    draw.text(((largura - validade_largura) / 2, posicao_base + texto_bbox[3] + 20), validade_texto, fill="black", font=validade_fonte)
    cracha.paste(qr_img, ((largura - 110) // 2, posicao_base + texto_bbox[3] + 20 + validade_bbox[3] + 20), qr_img)

    cracha.save(caminho_cracha)

def selecionar_qr_code():
    caminho_qr = filedialog.askopenfilename(title="Selecione a imagem do QR Code", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
    entry_qr_code.delete(0, tk.END)
    entry_qr_code.insert(0, caminho_qr) 

def gerar_cracha():
    nome = entry_nome.get() 
    validade = entry_validade.get()
    caminho_qr = entry_qr_code.get() 

    if not (nome and validade and caminho_qr):
        messagebox.showwarning("Entrada inválida", "Por favor, preencha todos os campos.")
        return

    ano_atual = datetime.now().year
    nome_arquivo = f"{nome.replace(' ', '_')}_{ano_atual}.png" 

    caminho_cracha = filedialog.asksaveasfilename(defaultextension=".png",
                                                  initialfile=nome_arquivo,
                                                  filetypes=[("PNG files", "*.png")],
                                                  title="Salvar Crachá como")
    
    if not caminho_cracha:  
        return

    criar_cracha(nome, validade, caminho_qr, caminho_cracha)
    messagebox.showinfo("Sucesso", f"Crachá gerado com sucesso: {caminho_cracha}")

def show_game_info(event):
    license_text = (
        "Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License\n\n"
        "Copyright (c) 2024 Carlos Boaventura\n\n"
        "Você é livre para: compartilhar — copiar e redistribuir o material em qualquer meio ou formato.\n\n"
        "Sob as seguintes condições:\n"
        "Atribuição — Você deve dar o devido crédito, fornecer um link para a licença e indicar se foram feitas alterações.\n"
        "Não Comercial — Você não pode usar o material para fins comerciais.\n"
        "Sem Derivações — Você não pode remixar, transformar ou criar a partir do material.\n\n"
        "Você não pode aplicar legalmente medidas adicionais que restrinjam legalmente outros de fazer qualquer coisa que a licença permita.\n\n"
        "Para mais informações, visite: https://creativecommons.org/licenses/by-nc-nd/4.0/"
    )

    messagebox.showinfo("Informações do Software", f"Gerador de Crachás\n"
                                                "Versão 1.0.1\n"
                                                "© 2024 Carlos Boaventura\n\n"
                                                f"{license_text}")

root = tk.Tk()
root.title("Gerador de Crachás")
root.geometry("400x390") 

# Organiza os elementos à esquerda
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, anchor='w')  # Mantém o alinhamento à esquerda

# Nome
label_nome = tk.Label(frame, text="Nome:", font=("Arial", 14), anchor='w') 
label_nome.pack(pady=(10, 5), anchor='w')
entry_nome = tk.Entry(frame, font=("Arial", 14), width=30)
entry_nome.pack(pady=(0, 10), anchor='w')

# Validade
label_validade = tk.Label(frame, text="Validade:", font=("Arial", 14), anchor='w') 
label_validade.pack(pady=(10, 5), anchor='w')
entry_validade = DateEntry(frame, font=("Arial", 14), width=29, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
entry_validade.pack(pady=(0, 10), anchor='w')

# QR Code
label_qr_code = tk.Label(frame, text="QR Code:", font=("Arial", 14), anchor='w')
label_qr_code.pack(pady=(10, 5), anchor='w')
entry_qr_code = tk.Entry(frame, font=("Arial", 14), width=30)
entry_qr_code.pack(pady=(0, 10), anchor='w')

# Botão para selecionar QR Code
botao_selecionar_qr = tk.Button(frame, text="Selecionar QR Code", command=selecionar_qr_code, font=("Arial", 12), bg="#4CAF50", fg="white")
botao_selecionar_qr.pack(pady=(10, 5), anchor='w')

# Botão Gerar Crachá
botao_gerar = tk.Button(frame, text="Gerar Crachá", command=gerar_cracha, font=("Arial", 12), bg="#2196F3", fg="white")
botao_gerar.pack(pady=(10, 10), anchor='w')

label_copyright = tk.Label(root, text="Copyright (c) 2024 Carlos Boaventura", font=("Arial", 10), fg="blue", cursor="hand2")
label_copyright.pack(side=tk.BOTTOM, pady=(10, 5))
label_copyright.bind("<Button-1>", show_game_info)

root.mainloop()
