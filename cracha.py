from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry

def criar_cracha(nome, validade, caminho_qr, caminho_cracha):
    largura = int(9 * 37.795) 
    altura = int(5 * 37.795)  

    cracha = Image.new('RGB', (largura, altura), color='white')
    draw = ImageDraw.Draw(cracha)

    try:
        fonte = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        fonte = ImageFont.load_default()

    texto_nome = nome
    
    texto_bbox = draw.textbbox((0, 0), texto_nome, font=fonte)
    texto_largura = texto_bbox[2] - texto_bbox[0]
    draw.text(((largura - texto_largura) / 2, 10), texto_nome, fill="black", font=fonte)

    validade_texto = f"Válido até: {validade}"
    validade_bbox = draw.textbbox((0, 0), validade_texto, font=fonte)
    validade_largura = validade_bbox[2] - validade_bbox[0] 
    draw.text(((largura - validade_largura) / 2, 40), validade_texto, fill="black", font=fonte)

    qr_img = Image.open(caminho_qr).convert("RGBA")
    qr_img = qr_img.resize((100, 100))
    cracha.paste(qr_img, ((largura - 100) // 2, 70), qr_img) 

    cracha.save(caminho_cracha)

def selecionar_qr_code():
    caminho_qr = filedialog.askopenfilename(title="Selecione a imagem do QR Code", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
    entry_qr_code.delete(0, tk.END)
    entry_qr_code.insert(0, caminho_qr) 

def gerar_cracha():
    nome = entry_nome.get() 
    validade = entry_validade.get()
    caminho_qr = entry_qr_code.get() 

    if not nome or not validade or not caminho_qr:
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
root.iconbitmap("icone_cracha.ico")
root.geometry("400x370") 

label_nome = tk.Label(root, text="Nome:", font=("Arial", 14)) 
label_nome.pack(pady=(10, 5))
entry_nome = tk.Entry(root, font=("Arial", 14), width=30)
entry_nome.pack(pady=(0, 10))

label_validade = tk.Label(root, text="Validade:", font=("Arial", 14)) 
label_validade.pack(pady=(10, 5))
entry_validade = DateEntry(root, font=("Arial", 14), width=30, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
entry_validade.pack(pady=(0, 10))

label_qr_code = tk.Label(root, text="QR Code:", font=("Arial", 14))
label_qr_code.pack(pady=(10, 5))
entry_qr_code = tk.Entry(root, font=("Arial", 14), width=30)
entry_qr_code.pack(pady=(0, 10))

botao_selecionar_qr = tk.Button(root, text="Selecionar QR Code", command=selecionar_qr_code, font=("Arial", 12), bg="#4CAF50", fg="white")
botao_selecionar_qr.pack(pady=(10, 5))

botao_gerar = tk.Button(root, text="Gerar Crachá", command=gerar_cracha, font=("Arial", 12), bg="#2196F3", fg="white")
botao_gerar.pack(pady=(10, 10))


label_copyright = tk.Label(root, text="Copyright (c) 2024 Carlos Boaventura", font=("Arial", 10), fg="blue", cursor="hand2")
label_copyright.pack(side=tk.BOTTOM, pady=(10, 5))
label_copyright.bind("<Button-1>", show_game_info)

root.mainloop()
