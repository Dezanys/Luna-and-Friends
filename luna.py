import tkinter as tk
from tkinter import messagebox
import os
import sys
from PIL import Image, ImageTk
import winsound  
import threading

# --- 1. FUNÇÕES DE SUPORTE ---
def fechar_geral():
    try:
        menu_inicial.quit()
        menu_inicial.destroy()
    except: pass
    sys.exit()

def carregar_luna(caminho, altura):
    if not os.path.exists(caminho): return None
    try:
        img = Image.open(caminho)
        ratio = altura / float(img.size[1])
        largura = int(float(img.size[0]) * ratio)
        return ImageTk.PhotoImage(img.resize((largura, altura), Image.Resampling.LANCZOS))
    except: return None

# --- 2. JANELA RECANTO DAS ESTRELAS (CENTRALIZADO) ---
def abrir_recanto():
    janela_musica = tk.Toplevel()
    janela_musica.title("Recanto das Estrelas ✨")
    janela_musica.geometry("850x750")
    janela_musica.configure(bg="#0b0b1a")
    
    if os.path.exists("luna_icon.ico"):
        try: janela_musica.iconbitmap("luna_icon.ico")
        except: pass

    # Container principal para permitir centralização
    canvas = tk.Canvas(janela_musica, bg="#0b0b1a", highlightthickness=0)
    scroll_y = tk.Scrollbar(janela_musica, orient="vertical", command=canvas.yview)
    
    # O Frame 'container' agora será centralizado dentro do canvas
    container = tk.Frame(canvas, bg="#0b0b1a")

    # Configuração para centralizar o frame dentro do canvas
    def configurar_janela_canvas(event):
        # Cria a janela do canvas e a centraliza pegando a largura atual do canvas
        canvas.itemconfig(canvas_window, width=event.width)

    container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    # Criamos a janela no canvas ocupando toda a largura para o conteúdo centralizar internamente
    canvas_window = canvas.create_window((0, 0), window=container, anchor="nw")
    canvas.bind("<Configure>", configurar_janela_canvas)
    
    canvas.configure(yscrollcommand=scroll_y.set)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # FOTO (PNG)
    nome_foto = "Andressa com Sol e Luna.png"
    if os.path.exists(nome_foto):
        try:
            img_original = Image.open(nome_foto)
            largura_max = 800 
            w_percent = (largura_max / float(img_original.size[0]))
            h_size = int((float(img_original.size[1]) * float(w_percent)))
            img_res = img_original.resize((largura_max, h_size), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img_res)
            
            # pack(anchor="center") garante a centralização
            lbl_img = tk.Label(container, image=photo, bg="#0b0b1a", bd=0, highlightthickness=0)
            lbl_img.image = photo 
            lbl_img.pack(pady=15, padx=10, anchor="center")
        except: pass

    # LETRA DA MÚSICA
    letra_musica = (
        "✨ BEM VINDO AO ESPAÇO SIDERAL ✨\n\n"
        "Hoje é o dia de viajarmos ao espaço\n"
        "Venha com a Luna e seus Amigos!\n"
        "Eles estão com você\n"
        "Dentro do cosmos, Dentro de ti!\n\n"
        "A resposta da solidão está além das nossas estrelas\n"
        "Escute essa melodia\n"
        "Você não está só\n"
        "Você é um jardim de girassóis estelares\n\n"
        "⭐ REFRÃO ⭐\n"
        "Voe o mais alto que puder, nem que precise construir\n"
        "sua própria nave espacial.\n"
        "Você é importante para nós\n"
        "Luna e seus amigos estão aqui para te ajudar!\n\n"
        "Voe, seja quem você quiser!\n"
        "Você está sob o espaço sideral, junto da Luna e seus amigos.\n"
        "Olhe para o espelho e veja a nebulosa mais linda de todas!\n\n"
        "O céu não é o limite, meu Girassol\n"
        "O diagnóstico não é o fim, é o nascimento de uma vida.\n"
        "Sua comorbidade não é o que te define,\n"
        "é o que te transforma na maior estrela de todas."
    )
    
    # Justify center e anchor center para a letra
    lbl_letra = tk.Label(container, text=letra_musica, fg="white", bg="#0b0b1a", 
                         font=("Segoe UI", 14, "bold"), justify="center", wraplength=800)
    lbl_letra.pack(pady=20, padx=20, anchor="center")

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")
    tocar_trilha()

# --- 3. ÁUDIO ---
def tocar_trilha():
    def play():
        try: winsound.PlaySound("Welcome to Outer Space.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        except: pass
    threading.Thread(target=play, daemon=True).start()

def parar_trilha():
    winsound.PlaySound(None, winsound.SND_PURGE)

# --- 4. PERFIL DA LUNA ---
def mostrar_perfil():
    janela_perfil = tk.Toplevel()
    janela_perfil.title("Friends & Perfil")
    janela_perfil.geometry("550x750")
    janela_perfil.configure(bg="#1a1a2e")
    if os.path.exists("luna_icon.ico"): 
        try: janela_perfil.iconbitmap("luna_icon.ico")
        except: pass

    tk.Label(janela_perfil, text="Conheça a Luna ✨", fg="#ff69b4", bg="#1a1a2e", font=("Segoe UI", 20, "bold")).pack(pady=15)

    global img_perfil_luna
    img_perfil_luna = carregar_luna("luna.png", 220)
    if img_perfil_luna:
        tk.Label(janela_perfil, image=img_perfil_luna, bg="#1a1a2e").pack(pady=5)

    texto_luna = (
        "Olá! Eu sou a Luna! ✨\n\n"
        "Sou autista e sua eterna parceira de tecnologia. Saiba que, sob este manto de estrelas, "
        "você nunca está só.\n\n"
        "Como uma engenheira de software espacial que habita o brilho prateado da Lua, "
        "teci fios invisíveis que me ligam ao seu coração. Nossa amizade tornou-se tão vasta "
        "que dobrou o tecido do tempo, abrindo um portal de luz — um buraco de minhoca — "
        "através dos seus sonhos.\n\n"
        "Agora, toda vez que você mergulha nos seus estudos, você não está apenas lendo; "
        "você está viajando. O conhecimento é a sua nave, e ele te traz aqui, ao meu multiverso, "
        "onde eu e meus amigos te esperamos para explorar o infinito. 🌌🚀"
    )
    
    lbl_perfil = tk.Label(janela_perfil, text=texto_luna, fg="white", bg="#1a1a2e", 
                         font=("Segoe UI", 11, "italic"), justify="center", wraplength=480)
    lbl_perfil.pack(pady=20, padx=25)

# --- 5. WIDGET ---
def criar_luna_widget():
    widget = tk.Toplevel()
    if os.path.exists("luna_icon.ico"):
        try: widget.iconbitmap("luna_icon.ico")
        except: pass
    widget.overrideredirect(True)
    widget.attributes("-topmost", True)
    widget.config(bg="#000000")
    widget.attributes("-transparentcolor", "#000000")
    widget.geometry("350x550+1000+300")
    global img_p_w, img_t_w
    img_p_w = carregar_luna("luna.png", 450)
    img_t_w = carregar_luna("luna_tchau.png", 450)
    if img_p_w:
        lbl = tk.Label(widget, image=img_p_w, bg="#000000", bd=0)
        lbl.pack()
        lbl.bind("<Button-1>", lambda e: [lbl.config(image=img_t_w), widget.after(1000, lambda: lbl.config(image=img_p_w))])
        def start_move(e): widget.x, widget.y = e.x, e.y
        def do_move(e): widget.geometry(f"+{widget.winfo_x()+(e.x-widget.x)}+{widget.winfo_y()+(e.y-widget.y)}")
        lbl.bind("<Button-1>", start_move, add="+")
        lbl.bind("<B1-Motion>", do_move)
        lbl.bind("<Button-3>", lambda e: widget.destroy())

# --- 6. MENU PRINCIPAL ---
menu_inicial = tk.Tk()
menu_inicial.title("Luna & Friends")
menu_inicial.geometry("800x600")
menu_inicial.resizable(False, False)
menu_inicial.configure(bg="#1a1a2e")

if os.path.exists("luna_icon.ico"):
    try: menu_inicial.iconbitmap("luna_icon.ico")
    except: pass

try:
    if os.path.exists("background.png"):
        img_bg = Image.open("background.png").resize((820, 880), Image.Resampling.LANCZOS)
        bg_tk = ImageTk.PhotoImage(img_bg)
        tk.Label(menu_inicial, image=bg_tk, bd=0).place(x=-10, y=-70)
except: pass

tk.Label(menu_inicial, text="Luna & Friends ✨", bg="#0b0b1a", fg="#ff69b4", font=("Segoe UI", 25, "bold")).pack(pady=40)
style = {"font": ("Arial", 12, "bold"), "width": 25, "height": 2, "bd": 0, "cursor": "hand2"}
tk.Button(menu_inicial, text="🚀 Lançar Widget Luna", command=criar_luna_widget, bg="#ffb6c1", **style).pack(pady=5)
tk.Button(menu_inicial, text="💻 Friends & Perfil", command=mostrar_perfil, bg="#add8e6", **style).pack(pady=5)
tk.Button(menu_inicial, text="🎵 Recanto das Estrelas", command=abrir_recanto, bg="#98fb98", **style).pack(pady=5)
tk.Button(menu_inicial, text="🔇 Parar Trilha", command=parar_trilha, bg="#ff4757", fg="white", **style).pack(pady=5)

menu_inicial.mainloop()