import tkinter as tk
from PIL import Image, ImageTk
import random
from datetime import datetime
import webbrowser
import os
import winsound

# --- CONFIGURAÇÕES DE ARQUIVOS (Foco: Sol e Luna) ---
ARQUIVO_CONFIG = "preferencia.txt"
ARQUIVO_MUSICA = "Welcome to Outer Space.wav"
ARQUIVO_BG = "Andressa com Sol e Luna.png"
ARQUIVO_BANNER_SELETOR = "Banner Luna & Friends.png"
IMAGEM_LUNA = "luna_estatica.png"
IMAGEM_SOL = "sol_estatico.png"
ARQUIVO_ICON = "luna_icon.ico"

musica_rodando = False

# --- BANCOS DE FRASES (Autoajuda e Foco) ---
lembretes_luna = [
    "Já houve ingestão de água hoje? 💧",
    "Momento de descansar os olhos um pouco. 👀",
    "Você é capaz de grandes coisas hoje. 🌌",
    "Respire fundo e mantenha o foco. 🧘"
]

lembretes_sol = [
    "Sua mente está afiada e pronta para vencer! 🧠✨",
    "O sucesso é construído com consistência! 🧱",
    "Concentre-se no processo, o resultado virá! ⏳🎯",
    "Sua energia ilumina sua produtividade! ☀️"
]

def obter_saudacao():
    hora = datetime.now().hour
    if 5 <= hora < 12: return "Bom dia!"
    elif 12 <= hora < 18: return "Boa tarde!"
    else: return "Boa noite!"

# --- FUNÇÕES DE CONFIGURAÇÃO ---
def salvar_escolha(nome):
    try:
        with open(ARQUIVO_CONFIG, "w") as f:
            f.write(nome)
    except: pass

def ler_escolha():
    if os.path.exists(ARQUIVO_CONFIG):
        try:
            with open(ARQUIVO_CONFIG, "r") as f:
                return f.read().strip()
        except: return None
    return None

# --- CLASSE DE WIDGET ---
class PersonagemWidget:
    def __init__(self, parent, imagem_arquivo, banco_frases, tamanho_img=(250, 250), tamanho_janela="350x450"):
        self.win = tk.Toplevel(parent)
        self.win.overrideredirect(True) 
        self.win.attributes("-topmost", True)
        self.win.attributes("-transparentcolor", "white")
        self.win.geometry(f"{tamanho_janela}+950+300") 
        self.win.config(bg='white')

        self.win.bind("<Button-1>", self.iniciar_movimento)
        self.win.bind("<B1-Motion>", self.fazer_movimento)
        self.win.bind("<ButtonRelease-1>", lambda e: self.balao.config(text=f"{obter_saudacao()} - {random.choice(banco_frases)}"))

        texto_inicial = f"{obter_saudacao()} - {random.choice(banco_frases)}"
        self.balao = tk.Label(self.win, text=texto_inicial, bg="#f0f0f0", fg="#333",
                              font=("Segoe UI", 10, "bold"), wraplength=300,
                              relief="solid", bd=1, padx=15, pady=10)
        self.balao.pack(pady=10)

        try:
            img = Image.open(imagem_arquivo).resize(tamanho_img, Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            self.lbl = tk.Label(self.win, image=self.photo, bg="white", cursor="fleur")
            self.lbl.pack()
        except:
            self.lbl = tk.Label(self.win, text="[IMG ERROR]", bg="white")
            self.lbl.pack()

        self.auto_atualizar(banco_frases)

    def iniciar_movimento(self, event):
        self.x, self.y = event.x, event.y

    def fazer_movimento(self, event):
        x = self.win.winfo_x() + (event.x - self.x)
        y = self.win.winfo_y() + (event.y - self.y)
        self.win.geometry(f"+{x}+{y}")

    def auto_atualizar(self, banco_frases):
        saudacao_atual = obter_saudacao()
        if saudacao_atual not in self.balao.cget("text"):
            self.balao.config(text=f"{saudacao_atual} - {random.choice(banco_frases)}")
        self.win.after(900000, lambda: self.auto_atualizar(banco_frases))

class LunaWidget(PersonagemWidget):
    def __init__(self, parent):
        super().__init__(parent, IMAGEM_LUNA, lembretes_luna)

class SolWidget(PersonagemWidget):
    def __init__(self, parent):
        super().__init__(parent, IMAGEM_SOL, lembretes_sol, tamanho_img=(350, 350), tamanho_janela="450x550")

# --- MINI MENU DE SELEÇÃO ---
def seletor_anfitriao(parent):
    if parent.personagem_widget:
        parent.personagem_widget.win.destroy()

    seletor = tk.Toplevel(parent)
    seletor.overrideredirect(True) 
    seletor.geometry("550x250+600+300")
    
    try:
        img_ban = Image.open(ARQUIVO_BANNER_SELETOR).resize((550, 250), Image.Resampling.LANCZOS)
        seletor.bg_img = ImageTk.PhotoImage(img_ban)
        tk.Label(seletor, image=seletor.bg_img).place(x=0, y=0)
    except:
        seletor.config(bg="#0b0b1a")

    def select(tipo):
        salvar_escolha(tipo)
        if tipo == "Luna": parent.personagem_widget = LunaWidget(parent)
        else: parent.personagem_widget = SolWidget(parent)
        seletor.destroy()

    # Sol na Esquerda, Luna na Direita, sem cobrir o rosto
    tk.Button(seletor, text="☀️ Sol", command=lambda: select("Sol"), bg="#ffe082", width=12, font=("Arial", 10, "bold")).place(x=100, y=180)
    tk.Button(seletor, text="🌙 Luna", command=lambda: select("Luna"), bg="#ffb6c1", width=12, font=("Arial", 10, "bold")).place(x=350, y=180)

# --- INTERFACE PRINCIPAL ---
root = tk.Tk()
root.title("Luna & Friends")
root.geometry("800x600")
root.resizable(False, False)

if os.path.exists(ARQUIVO_ICON):
    try: root.iconbitmap(ARQUIVO_ICON)
    except: pass

# AJUSTE DE FUNDO: Preenchimento total para remover a mancha branca
try:
    img_bg = Image.open(ARQUIVO_BG).resize((800, 600), Image.Resampling.LANCZOS)
    root.bg_img = ImageTk.PhotoImage(img_bg)
    # Usando place(relwidth=1, relheight=1) para garantir que cubra TUDO
    bg_label = tk.Label(root, image=root.bg_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    root.config(bg="#0b0b1a")

# Título Principal (Sem estrelinha)
tk.Label(root, text="Luna & Friends", bg="#0b0b1a", fg="#ff69b4", font=("Segoe UI", 30, "bold")).pack(pady=40)

btn_style = {"font": ("Arial", 12, "bold"), "width": 25, "height": 2, "cursor": "hand2"}

tk.Button(root, text="🚀 Abrir Gemini", command=lambda: webbrowser.open("https://gemini.google.com"), bg="#ffb6c1", **btn_style).pack(pady=10)

def gerenciar_musica():
    global musica_rodando
    if not musica_rodando:
        winsound.PlaySound(ARQUIVO_MUSICA, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
        btn_musica.config(text="🔇 Parar Música", bg="#ffeb3b")
        musica_rodando = True
    else:
        winsound.PlaySound(None, winsound.SND_PURGE)
        btn_musica.config(text="🎵 Tocar Música", bg="#98fb98")
        musica_rodando = False

btn_musica = tk.Button(root, text="🎵 Tocar Música", command=gerenciar_musica, bg="#98fb98", **btn_style)
btn_musica.pack(pady=10)

# Botão Roxo para Trocar Anfitrião
tk.Button(root, text="🔄 Trocar Anfitrião", command=lambda: seletor_anfitriao(root), 
          bg="#9370DB", fg="white", **btn_style).pack(pady=10)

tk.Button(root, text="❌ Sair", command=root.quit, bg="#ff4757", fg="white", **btn_style).pack(pady=10)

root.personagem_widget = None
ultimo = ler_escolha()

if ultimo == "Luna": root.personagem_widget = LunaWidget(root)
elif ultimo == "Sol": root.personagem_widget = SolWidget(root)
else: seletor_anfitriao(root)

root.mainloop()
