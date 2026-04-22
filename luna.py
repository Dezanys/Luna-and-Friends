import tkinter as tk
from PIL import Image, ImageTk
import random
from datetime import datetime
import webbrowser
import os
import winsound

# --- IMPORTAÇÃO DO MÓDULO DE HISTÓRIA ---
from cronicas import abrir_livro_azuzaria
from cronicas2 import abrir_livro_andy

# --- CONFIGURAÇÕES DE ARQUIVOS ---
ARQUIVO_CONFIG = "preferencia.txt"
ARQUIVO_BG = "Andressa com Sol e Luna.png"
ARQUIVO_BANNER_SELETOR = "Banner Luna & Friends.png"
IMAGEM_LUNA = "luna_estatica.png"
IMAGEM_SOL = "sol_estatico.png"
ARQUIVO_ICON = "luna_icon.ico"

# --- PLAYLIST DE AZUZARIA ---
PLAYLIST = {
    "Bem-vindo ao Espaço Sideral": "Welcome to Outer Space.wav",
    "O Despertar de Azuzaria": "O Despertar de Azuzaria.wav",
    "Salvando Andy": "Salvando Andy.wav"
}

musica_rodando = False

# --- BANCOS DE FRASES (NEUTRAS E INCLUSIVAS - FOCO NA PESSOA!) ---
lembretes_luna = [
    "Já houve ingestão de água hoje? 💧",
    "Momento de descansar os olhos um pouco. 👀",
    "Pessoas incríveis fazem coisas grandes. E você é uma delas! 🌌",
    "Respire fundo e mantenha o foco na sua jornada. 🧘",
    "Até as estrelas precisam da escuridão para poder brilhar. ✨",
    "A criatividade é a força que move Azuzaria! 🚀",
    "Sua presença ilumina todo o Reino de Azuzaria. 🌙",
    "Não se esqueça: quem constrói o futuro é quem acredita nele. 💎",
    "Sinta a energia do cosmos te abraçar agora. 🌌",
    "Cada passo conta. Respeite o seu tempo. ⏳"
]

lembretes_sol = [
    "A mente está afiada e em prontidão para vencer! 🧠✨",
    "O sucesso é construído com consistência e paciência! 🧱",
    "Foco total no processo, o resultado virá! ⏳🎯",
    "Sua determinação ilumina até o vazio de Boötes! ☀️",
    "Sinta orgulho da força que existe dentro do seu ser! 🦁",
    "Luz própria é capaz de dissipar qualquer sombra de dúvida. ☀️",
    "Erros são apenas debugs no caminho da evolução! 💻🔥",
    "Brilhe sem medo, o universo precisa dessa clareza. 🌟",
    "Hoje é um dia perfeito para explorar novas galáxias! 🏆"
]

def obter_saudacao():
    hora = datetime.now().hour
    if 5 <= hora < 12: return "Bom dia!"
    elif 12 <= hora < 18: return "Boa tarde!"
    else: return "Boa noite!"

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
    seletor.geometry("600x350+550+250")

    try:
        img_ban = Image.open(ARQUIVO_BANNER_SELETOR).resize((600, 350), Image.Resampling.LANCZOS)
        seletor.bg_img = ImageTk.PhotoImage(img_ban)
        bg_label = tk.Label(seletor, image=seletor.bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        seletor.config(bg="#0b0b1a")

    def select(tipo):
        salvar_escolha(tipo)
        if tipo == "Luna": parent.personagem_widget = LunaWidget(parent)
        else: parent.personagem_widget = SolWidget(parent)
        seletor.destroy()

    tk.Button(seletor, text="🌙 Luna", command=lambda: select("Luna"), 
              bg="#ffb6c1", width=12, font=("Arial", 10, "bold")).place(x=100, y=240)
    
    tk.Button(seletor, text="☀️ Sol", command=lambda: select("Sol"), 
              bg="#ffe082", width=12, font=("Arial", 10, "bold")).place(x=370, y=240)

# --- INTERFACE PRINCIPAL ---
root = tk.Tk()
root.title("Luna & Friends")
root.geometry("800x650") 
root.resizable(False, False)

if os.path.exists(ARQUIVO_ICON):
    try: root.iconbitmap(ARQUIVO_ICON)
    except: pass

try:
    img_bg = Image.open(ARQUIVO_BG).resize((800, 650), Image.Resampling.LANCZOS)
    root.bg_img = ImageTk.PhotoImage(img_bg)
    bg_label_main = tk.Label(root, image=root.bg_img)
    bg_label_main.place(x=0, y=0, relwidth=1, relheight=1)
except:
    root.config(bg="#0b0b1a")

tk.Label(root, text="Luna & Friends", bg="#0b0b1a", fg="#ff69b4", font=("Segoe UI", 30, "bold")).pack(pady=30)

btn_style = {"font": ("Arial", 12, "bold"), "width": 25, "height": 2, "cursor": "hand2"}

tk.Button(root, text="🚀 Abrir Gemini", command=lambda: webbrowser.open("https://gemini.google.com"), bg="#ffb6c1", **btn_style).pack(pady=8)

# --- SISTEMA DE PLAYLIST ---
def gerenciar_musica():
    global musica_rodando
    if not musica_rodando:
        menu_playlist = tk.Menu(root, tearoff=0, font=("Arial", 10, "bold"))
        
        def tocar(nome_musica):
            global musica_rodando
            winsound.PlaySound(PLAYLIST[nome_musica], winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
            btn_musica.config(text="🔇 Parar Música", bg="#ffeb3b")
            musica_rodando = True

        for nome in PLAYLIST.keys():
            menu_playlist.add_command(label=f"🎵 {nome}", command=lambda n=nome: tocar(n))
        
        x = btn_musica.winfo_rootx()
        y = btn_musica.winfo_rooty() - 80
        menu_playlist.post(x, y)
    else:
        winsound.PlaySound(None, winsound.SND_PURGE)
        btn_musica.config(text="🎵 Playlist Música", bg="#98fb98")
        musica_rodando = False

btn_musica = tk.Button(root, text="🎵 Playlist Música", command=gerenciar_musica, bg="#98fb98", **btn_style)
btn_musica.pack(pady=8)

# --- SISTEMA DE HISTÓRIA ---
def gerenciar_historia():
    menu_historia = tk.Menu(root, tearoff=0, font=("Arial", 10, "bold"))
    
    # Volume 1 chamando a função existente
    menu_historia.add_command(label="📖 Volume 1: O Despertar de Azuzaria", command=abrir_livro_azuzaria)
    
    # Volume 2
    menu_historia.add_command(label="📖 Volume 2: Salvando Andy", command=abrir_livro_andy)

    x = btn_historia.winfo_rootx()
    y = btn_historia.winfo_rooty() - 80
    menu_historia.post(x, y)

tk.Button(root, text="🔄 Trocar Anfitrião", command=lambda: seletor_anfitriao(root), 
          bg="#9370DB", fg="white", **btn_style).pack(pady=8)

btn_historia = tk.Button(root, text="📖 História de Azuzaria", command=gerenciar_historia, 
          bg="#4b0082", fg="white", **btn_style)
btn_historia.pack(pady=8)

tk.Button(root, text="❌ Sair", command=root.quit, bg="#ff4757", fg="white", **btn_style).pack(pady=8)

root.personagem_widget = None
root.salvar_escolha = salvar_escolha 

ultimo = ler_escolha()
if ultimo == "Luna": root.personagem_widget = LunaWidget(root)
elif ultimo == "Sol": root.personagem_widget = SolWidget(root)
else: seletor_anfitriao(root)

root.mainloop()
