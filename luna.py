import tkinter as tk
import os
from PIL import Image, ImageTk
import winsound  
import webbrowser 

# --- CONFIGURAÇÕES DE ARQUIVOS ---
ARQUIVO_MUSICA = "Welcome to Outer Space.wav"
ARQUIVO_BG = "Andressa com Sol e Luna.png"
ARQUIVO_ICON = "luna_icon.ico"

musica_tocando = False

def alternar_musica():
    global musica_tocando
    if not musica_tocando:
        if os.path.exists(ARQUIVO_MUSICA):
            try:
                winsound.PlaySound(ARQUIVO_MUSICA, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
                musica_tocando = True
            except: pass
    else:
        winsound.PlaySound(None, winsound.SND_PURGE)
        musica_tocando = False

def carregar_imagem(caminho, altura):
    if not os.path.exists(caminho): return None
    try:
        img = Image.open(caminho).convert("RGBA")
        ratio = altura / float(img.size[1])
        return ImageTk.PhotoImage(img.resize((int(float(img.size[0])*ratio), altura), Image.Resampling.LANCZOS))
    except: return None

def criar_luna_widget():
    widget = tk.Toplevel()
    widget.overrideredirect(True) 
    widget.attributes("-topmost", True)
    
    # Transparência absoluta
    bg_transparente = "#010101" 
    widget.config(bg=bg_transparente)
    widget.attributes("-transparentcolor", bg_transparente)
    
    largura, altura = 350, 400
    pos_x = widget.winfo_screenwidth() - largura - 50
    widget.geometry(f"{largura}x{altura}+{pos_x}+100")

    # Carregar imagens
    global img_estatica, img_tchau, img_tchau_piscando
    img_estatica = carregar_imagem("luna_estatica.png", 320)
    img_tchau = carregar_imagem("luna_tchau.png", 320)
    img_tchau_piscando = carregar_imagem("luna_tchau_piscando.png", 320)

    lbl_luna = tk.Label(widget, bg=bg_transparente, bd=0, cursor="hand2")
    if img_estatica: lbl_luna.config(image=img_estatica)
    lbl_luna.pack()

    # --- ANIMAÇÃO CONTROLADA (Anti-Tremor) ---
    def animar_passo(contador):
        if not widget.winfo_exists(): return
        
        # Sequência de imagens: 0=Piscando, 1=Tchau, 2=Piscando, 3=Tchau...
        if contador > 0:
            widget.update_idletasks() # Sincroniza antes de mudar
            if contador % 2 == 0:
                if img_tchau_piscando: lbl_luna.config(image=img_tchau_piscando)
            else:
                if img_tchau: lbl_luna.config(image=img_tchau)
            
            # Agenda o próximo passo (600ms para estabilidade)
            widget.after(600, lambda: animar_passo(contador - 1))
        else:
            # Volta ao normal
            if img_estatica: lbl_luna.config(image=img_estatica)

    def iniciar_interacao(event):
        animar_passo(4) # Faz 4 trocas de imagem

    # --- MOVIMENTAÇÃO E CLIQUES ---
    widget._drag_data = {"x": 0, "y": 0, "moved": False}

    def iniciar_movimento(event):
        widget._drag_data["x"] = event.x
        widget._drag_data["y"] = event.y
        widget._drag_data["moved"] = False

    def mover_janela(event):
        widget._drag_data["moved"] = True
        deltax = event.x - widget._drag_data["x"]
        deltay = event.y - widget._drag_data["y"]
        widget.geometry(f"+{widget.winfo_x()+deltax}+{widget.winfo_y()+deltay}")

    def clique_esquerdo(event):
        if not widget._drag_data["moved"]:
            webbrowser.open("https://gemini.google.com")

    # Binds
    lbl_luna.bind("<Button-1>", iniciar_movimento)
    lbl_luna.bind("<B1-Motion>", mover_janela)
    lbl_luna.bind("<ButtonRelease-1>", clique_esquerdo) # Clique Esquerdo = Gemini
    lbl_luna.bind("<Button-3>", iniciar_interacao)      # Clique Direito = Tchau/Pisca
    
    widget.bind("<Escape>", lambda e: widget.destroy())
    widget.focus_set()

# --- MENU PRINCIPAL ---
menu = tk.Tk()
menu.title("Luna & Friends")
menu.geometry("800x600")

if os.path.exists(ARQUIVO_ICON):
    try: menu.iconbitmap(ARQUIVO_ICON)
    except: pass

try:
    if os.path.exists(ARQUIVO_BG):
        img_res = Image.open(ARQUIVO_BG).resize((800, 600), Image.Resampling.LANCZOS)
        bg_tk = ImageTk.PhotoImage(img_res)
        tk.Label(menu, image=bg_tk).place(x=0, y=0)
        menu.bg_img = bg_tk 
except: pass

tk.Label(menu, text="Luna & Friends ✨", bg="#0b0b1a", fg="#ff69b4", font=("Segoe UI", 25, "bold")).pack(pady=30)
btn_s = {"font": ("Arial", 12, "bold"), "width": 25, "height": 2}

tk.Button(menu, text="🚀 Lançar Luna", command=criar_luna_widget, bg="#ffb6c1", **btn_s).pack(pady=10)
tk.Button(menu, text="🎵 Tocar/Parar Música", command=alternar_musica, bg="#98fb98", **btn_s).pack(pady=10)
tk.Button(menu, text="❌ Sair", command=menu.quit, bg="#ff4757", fg="white", **btn_s).pack(pady=10)

menu.mainloop()
