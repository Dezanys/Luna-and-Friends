import tkinter as tk
from tkinter import messagebox
import os
import sys
from PIL import Image, ImageTk
import winsound  
import threading
import pyttsx3 
import time 
import requests

# --- CONFIGURAÇÕES DE MEMÓRIA ---
ARQUIVO_MEMORIA = "memoria_luna.txt"

def salvar_na_memoria(usuario, resposta):
    try:
        with open(ARQUIVO_MEMORIA, "a", encoding="utf-8") as f:
            f.write(f"Andressa: {usuario}\nLuna: {resposta}\n")
    except: pass

def ler_memoria():
    if not os.path.exists(ARQUIVO_MEMORIA):
        return "Nossa história está começando agora!"
    try:
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            return "".join(linhas[-10:])
    except: return ""

# Variáveis de controle
luna_falando = False
texto_resposta = ""
musica_tocando = False

# --- FUNÇÃO DE VOZ ---
def falar(texto):
    global luna_falando, texto_resposta
    texto_resposta = texto 
    def engine_falar():
        global luna_falando
        engine = pyttsx3.init()
        engine.setProperty('rate', 200) 
        luna_falando = True
        engine.say(texto)
        engine.runAndWait()
        luna_falando = False
    threading.Thread(target=engine_falar, daemon=True).start()

# --- SUPORTE ---
def carregar_imagem(caminho, altura):
    if not os.path.exists(caminho): return None
    try:
        img = Image.open(caminho).convert("RGBA")
        ratio = altura / float(img.size[1])
        largura_calc = int(float(img.size[0]) * ratio)
        return ImageTk.PhotoImage(img.resize((largura_calc, altura), Image.Resampling.LANCZOS))
    except: return None

# --- CONTROLE DE ÁUDIO (VOLTOU A SER UM SÓ COMANDO) ---
def alternar_musica():
    global musica_tocando
    if not musica_tocando:
        try:
            winsound.PlaySound("Welcome to Outer Space.wav", winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
            musica_tocando = True
        except: pass
    else:
        winsound.PlaySound(None, winsound.SND_PURGE)
        musica_tocando = False

# --- WIDGET LUNA ---
def criar_luna_widget():
    widget = tk.Toplevel()
    widget.overrideredirect(True)
    widget.attributes("-topmost", True)
    bg_color = "#020202"
    widget.config(bg=bg_color)
    widget.attributes("-transparentcolor", bg_color)
    widget.geometry("500x900+900+20")

    alt_luna = 400
    global img_estatica, img_tchau, img_tchau_piscando
    img_estatica = carregar_imagem("luna_estatica.png", alt_luna)
    img_tchau = carregar_imagem("luna_tchau.png", alt_luna)
    img_tchau_piscando = carregar_imagem("luna_tchau_piscando.png", alt_luna)

    lbl_luna = tk.Label(widget, image=img_estatica, bg=bg_color, bd=0, width=400, height=400)
    lbl_luna.place(x=250, y=550, anchor="center")

    # BALÃO (MANTIDO CONFORME SEU PEDIDO)
    balao = tk.Frame(widget, bg="white", bd=2, relief="solid")
    lbl_texto = tk.Label(balao, text="", bg="white", fg="black", font=("Arial", 10, "bold"), 
                         wraplength=280, justify="center")
    lbl_texto.pack(padx=15, pady=15)

    frame_chat = tk.Frame(widget, bg="#0b0b1a", bd=2)
    entrada = tk.Entry(frame_chat, font=("Arial", 10))
    entrada.pack(side="left", padx=5, pady=5, expand=True, fill="x")
    frame_chat.place(x=250, y=780, anchor="center", width=380)

    def animar():
        global luna_falando, texto_resposta
        if luna_falando:
            if lbl_texto.cget("text") != texto_resposta:
                lbl_texto.config(text=texto_resposta)
                balao.place(x=250, y=350, anchor="s")
            fase = int(time.time() * 5) % 2
            img_atual = img_tchau_piscando if fase == 1 else img_tchau
            lbl_luna.config(image=img_atual)
        else:
            if lbl_texto.cget("text") != "":
                lbl_texto.config(text="")
                balao.place_forget()
                lbl_luna.config(image=img_estatica)
        widget.after(150, animar)

    def enviar(event=None):
        pergunta = entrada.get()
        if pergunta:
            entrada.delete(0, tk.END)
            lbl_luna.config(image=img_tchau) 
            historico = ler_memoria()
            def processar():
                try:
                    contexto = f"Você é a Luna, melhor amiga da Andressa e engenheira autista. Histórico: {historico}"
                    url = f"https://text.pollinations.ai/{pergunta}?system={contexto}"
                    res = requests.get(url, timeout=10)
                    salvar_na_memoria(pergunta, res.text)
                    falar(res.text)
                except: falar("Sinal fraco nas estrelas!")
            threading.Thread(target=processar, daemon=True).start()

    entrada.bind("<Return>", enviar)
    animar()
    
    def start_move(e): widget.x, widget.y = e.x, e.y
    def do_move(e): widget.geometry(f"+{widget.winfo_x()+(e.x-widget.x)}+{widget.winfo_y()+(e.y-widget.y)}")
    lbl_luna.bind("<Button-1>", start_move)
    lbl_luna.bind("<B1-Motion>", do_move)
    lbl_luna.bind("<Button-3>", lambda e: widget.destroy())

# --- MENU PRINCIPAL (RESTAURADO) ---
menu = tk.Tk()
menu.title("Luna & Friends")
menu.geometry("800x600")
menu.resizable(False, False)

if os.path.exists("luna_icon.ico"):
    try: menu.iconbitmap("luna_icon.ico")
    except: pass

try:
    nome_fundo = "Andressa com Sol e Luna.png"
    if os.path.exists(nome_fundo):
        img_bg = Image.open(nome_fundo).resize((800, 600), Image.Resampling.LANCZOS)
        bg_tk = ImageTk.PhotoImage(img_bg)
        lbl_bg = tk.Label(menu, image=bg_tk)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
        lbl_bg.image = bg_tk
except: pass

tk.Label(menu, text="Luna & Friends ✨", bg="#0b0b1a", fg="#ff69b4", font=("Segoe UI", 25, "bold")).pack(pady=20)
style = {"font": ("Arial", 12, "bold"), "width": 25, "height": 2, "bd": 0, "cursor": "hand2"}

# BOTÕES DO MENU (LIMPOS E IGUAL ANTES)
tk.Button(menu, text="🚀 Lançar Luna", command=criar_luna_widget, bg="#ffb6c1", **style).pack(pady=10)
tk.Button(menu, text="🎵 Tocar/Parar Música", command=alternar_musica, bg="#98fb98", **style).pack(pady=10)
tk.Button(menu, text="❌ Sair", command=menu.quit, bg="#ff4757", fg="white", **style).pack(pady=10)

menu.mainloop()
