import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from datetime import datetime
import webbrowser
import os
import winsound
import threading
import re
import math 
import time
import traceback

# =============================================================================
# --- BLOCO 1: INFRAESTRUTURA E CONFIGURAÇÕES NATIVAS ---
# =============================================================================
COR_FUNDO_BALAO = "#F5F5F5"
ARQUIVO_CONFIG = "preferencia.txt"
ARQUIVO_BG_PRINCIPAL = "Andressa com Sol e Luna.png"
ARQUIVO_BANNER_SELETOR = "Banner Luna & Friends.png"
ARQUIVO_ICONE_AZUZARIA = "luna_icon.ico"

IMAGEM_LUNA_BASE = "luna_estatica.png"
IMAGEM_SOL_BASE = "sol_estatico.png"

PLAYLIST_AZUZARIA = {
    "Bem-vindo ao Espaço Sideral": "Welcome to Outer Space.wav", 
    "O Despertar de Azuzaria": "O Despertar de Azuzaria.wav", 
    "Salvando Andy": "Salvando Andy.wav"
}

# --- FUNÇÕES PARA ABRIR AS CRÔNICAS SEM TRAVA DE CACHE ---
def chamar_capitulo_1():
    try:
        import cronicas
        import importlib
        importlib.reload(cronicas)
        cronicas.abrir_livro_azuzaria()
    except Exception as e:
        erro_detalhado = traceback.format_exc()
        messagebox.showerror("Erro no Capítulo 1", f"Não foi possível abrir o Capítulo 1.\n\nDetalhes:\n{erro_detalhado}")

def chamar_capitulo_2():
    try:
        import cronicas2
        import importlib
        importlib.reload(cronicas2)
        cronicas2.abrir_livro_andy()
    except Exception as e:
        erro_detalhado = traceback.format_exc()
        messagebox.showerror("Erro no Capítulo 2", f"Não foi possível abrir o Capítulo 2.\n\nDetalhes:\n{erro_detalhado}")

def chamar_capitulo_3():
    try:
        import cronicas3
        import importlib
        importlib.reload(cronicas3)
        cronicas3.abrir_livro_calisto()
    except Exception as e:
        erro_detalhado = traceback.format_exc()
        messagebox.showerror("Erro no Capítulo 3", f"Não foi possível abrir o Capítulo 3.\n\nDetalhes:\n{erro_detalhado}")

# =============================================================================
# --- BLOCO 2: NÚCLEO DE INTELIGÊNCIA E BANCO DE DADOS DE CONHECIMENTO ---
# =============================================================================

def ciclo_movimento_boca(instancia, tempo_restante):
    if tempo_restante > 0:
        if instancia.lbl_img.cget("image") == str(instancia.photo_estatica):
            try:
                caminho_fala = f"{instancia.nome.lower()}_boca_aberta.png"
                img_fala = Image.open(caminho_fala).resize(instancia.tamanho_img, Image.Resampling.LANCZOS)
                instancia.photo_fala = ImageTk.PhotoImage(img_fala)
                instancia.lbl_img.config(image=instancia.photo_fala)
            except: pass
        else:
            instancia.lbl_img.config(image=instancia.photo_estatica)
        instancia.win.after(200, lambda: ciclo_movimento_boca(instancia, tempo_restante - 0.2))
    else:
        instancia.lbl_img.config(image=instancia.photo_estatica)

def animar_fala_personagem(instancia_widget):
    ciclo_movimento_boca(instancia_widget, 3.0)

def processar_ia_azuzaria(obj_personagem):
    entrada_texto = obj_personagem.entry.get()
    pergunta = entrada_texto.lower().strip()
    balao = obj_personagem.balao
    obj_personagem.entry.delete(0, tk.END)
    
    # 1. CALCULADORA NATIVA
    if re.search(r'\d', pergunta) and any(op in pergunta for op in "+-*/%x"):
        try:
            exp = pergunta.replace('x', '*').replace(',', '.')
            limpo = re.sub(r'[^0-9+\-*/%.**]', '', exp)
            res = eval(limpo, {"__builtins__": None}, {"math": math, "sqrt": math.sqrt, "pow": math.pow, "pi": math.pi})
            txt = f"O resultado é {round(res, 4)}"
            balao.config(text=f"{txt}. A precisão matemática brilha! 🔢")
            animar_fala_personagem(obj_personagem)
            return
        except: pass

    # 2. ESCUDO CVV EXPANDIDO (PREVENÇÃO ABSOLUTA)
    GATILHOS_CVV = [
        "suicidio", "suicídio", "me matar", "morrer", "morte", "desistir", 
        "tirar minha vida", "fim da minha vida", "quero morrer", "autoextermínio", 
        "desespero total", "acabar com tudo", "não aguento mais viver"
    ]
    if any(gatilho in pergunta for gatilho in GATILHOS_CVV):
        msg = ("Sua vida é preciosa e tem um valor infinito no universo! ✨ "
               "Não passe por essa dor só. O CVV (Centro de Valorização da Vida) "
               "está pronto para ouvir com todo carinho e sigilo. "
               "Ligue gratuitamente para o 188 ou acesse cvv.org.br agora mesmo. ❤️")
        balao.config(text=msg, fg="red")
        animar_fala_personagem(obj_personagem)
        return

    # 3. BANCO DE CONHECIMENTO E ENCICLOPÉDIA DE ASTRONOMIA
    msg = ""
    if "tdah" in pergunta:
        msg = "O TDAH afeta o foco e a intensidade, mas a mente hiperfocada é cheia de conexões geniais. A criatividade é um superpoder!"
    elif "autismo" in pergunta or "tea" in pergunta:
        msg = "O Autismo é uma forma única, profunda e linda de processar o mundo. Viva a neurodiversidade e a riqueza de cada detalhe!"
    elif "historia" in pergunta or "história" in pergunta:
        msg = "A História estuda as ações humanas através do tempo. Compreender o passado é a chave para iluminar e transformar o futuro!"
    elif "portugues" in pergunta or "português" in pergunta:
        msg = "O Português é a nossa língua pátria, uma ferramenta poderosa, artística e cheia de sentimentos para expressar os maiores sonhos!"
        
    elif "buraco negro" in pergunta or "buracos negros" in pergunta:
        msg = ("Em 1915, Einstein mostrou que massas gigantes dobram o espaço. Logo depois, Schwarzschild provou que, se espremer muita matéria num ponto minúsculo, a gravidade fica tão absurda que nem a luz escapa — virando um buraco negro! "
               "Em 2019, telescópios tiraram a primeira foto real de um deles, provando que esses monstros invisíveis comandam o centro das galáxias! 🕳️🌌")

    elif "mercurio" in pergunta or "mercúrio" in pergunta:
        msg = "Mercúrio é o planeta mais próximo do Sol e o menor do Sistema Solar. Por não ter uma atmosfera estável, ele vive sob extremos: é terrivelmente quente de dia e congela durante a noite. Seu nome homenageia o ágil mensageiro dos deuses romanos! ☄️"
    elif "venus" in pergunta or "vênus" in pergunta:
        msg = "Vênus é conhecido como o planeta irmão da Terra devido ao tamanho, mas é o lugar mais hostil do Sistema Solar! Sua atmosfera densa prende o calor em um efeito estufa devastador, tornando-o mais quente que Mercúrio. Ele brilha tanto no céu que foi apelidado de Estrela d'Alva. 🪐"
    elif "terra" in pergunta:
        msg = "A Terra é o nosso lar, o terceiro planeta a partir do Sol e o único lugar conhecido no universo que abriga vida! Coberta por 70% de água líquida e protegida por uma atmosfera perfeita, ela é a nossa joia azul preciosa no cosmos. 🌍"
    elif "marte" in pergunta:
        msg = "Marte é o famoso Planeta Vermelho! Ele tem essa cor por causa do óxido de ferro (ferrugem) em seu solo. Abriga o Monte Olimpo, o maior vulcão do Sistema Solar, e hoje é o principal destino de exploração das nossas sondas e robôs em busca de água antiga. 🔴"
    elif "jupiter" in pergunta or "júpiter" in pergunta:
        msg = "Júpiter é o gigante gasoso, o maior planeta do nosso sistema! Ele é tão imenso que caberiam mais de mil Terras dentro dele. Sua característica mais famosa é a Grande Mancha Vermelha, uma tempestade furiosa que ruge há séculos e é maior que o nosso próprio planeta. 🌀"
    elif "saturno" in pergunta:
        msg = "Saturno é a joia do Sistema Solar, famoso por seu magnífico e deslumbrante sistema de anéis feitos de gelo e rocha. Ele também é um gigante gasoso e é tão leve que, se existisse um oceano grande o suficiente para colocá-lo dentro, ele flutuaria na água! 🪐"
    elif "urano" in pergunta:
        msg = "Urano é um gigante de gelo completamente azul-esverdeado devido ao gás metano em sua atmosfera. A maior excentricidade de Urano é que ele gira totalmente deitado! Os cientistas acreditam que ele colidiu com algo enorme no passado, o que alterou seu eixo. 🌀"
    elif "netuno" in pergunta:
        msg = "Netuno é o planeta mais distante do Sol e o mais frio do sistema. Um gigante de gelo de um azul profundo, ele abriga os ventos mais rápidos e furiosos do Sistema Solar, que podem ultrapassar os 2000 km/h! Seu nome celebra o deus romano dos mares. 🌊"
    elif "plutao" in pergunta or "plutão" in pergunta:
        msg = "Plutão foi considerado o 9º planeta até 2006, quando a União Astronômica Internacional o reclassificou como um 'planeta anão'. Mas ele continua super amado e guarda uma planície de gelo em formato de coração na sua superfície! 🖤"

    elif "carl sagan" in pergunta or "sagan" in pergunta:
        msg = "Carl Sagan foi um dos maiores astrônomos e divulgadores científicos do mundo! Ele nos ensinou que 'o cosmos está dentro de nós, somos feitos de poeira estelar' e que a ciência é uma vela no escuro. 🌌🕯️"
    elif "turing" in pergunta or "alan turing" in pergunta:
        msg = "Alan Turing é o pai da ciência da computação! Ele quebrou códigos secretos na Segunda Guerra Mundial e criou a base matemática para tudo o que chamamos de computador e inteligência artificial hoje. Um gênio absoluto! 🧠💻"
    elif "eniac" in pergunta or "primeiro computador" in pergunta:
        msg = "O ENIAC, construído em 1945, foi o primeiro computador digital eletrônico de grande escala da história! Ele pesava mais de 30 toneladas e ocupava uma sala inteira para fazer cálculos matemáticos que hoje um celular faz em milissegundos! 🏢📟"
    elif "astronomia" in pergunta or "cosmos" in pergunta or "universo" in pergunta:
        msg = "A Astronomia é a ciência que estuda os corpos celestes e o universo infinito. Olhar para as estrelas é viajar no tempo, pois a luz vista hoje viajou bilhões de anos pelo espaço sideral! 🌠🚀"
    elif "poeira estelar" in pergunta or "estrelas" in pergunta:
        msg = "Sabia que os átomos do corpo humano foram forjados no coração de estrelas que explodiram há bilhões de anos? Somos literalmente poeira estelar descobrindo o universo! ✨🪐"
        
    elif any(t in pergunta for t in ["tudo bem", "como vai", "como voce esta", "como você está", "tudo bom"]):
        msg = "Tudo maravilhoso por aqui, brilhando como uma supernova! É uma alegria imensa conversar. E com você, como estão as coisas no seu lado da galáxia? 🌌✨"
        
    elif any(t in pergunta for t in ["ajuda", "gemini"]):
        msg = "Para pesquisas profundas ou dúvidas complexas de Azuzaria, consulte o Portal Gemini no menu principal!"
    elif any(t in pergunta for t in ["obrigado", "obrigada", "valeu"]):
        msg = "Por nada! É um prazer enorme e uma alegria gigante ajudar no aprendizado!"
    elif any(t in pergunta for t in ["oi", "ola", "olá", "bom dia", "boa tarde", "boa noite"]):
        msg = "Olá! Como posso iluminar seu universo de aprendizado hoje em Azuzaria?"
    else:
        msg = "Que tema fascinante para explorar! O que mais você gostaria de descobrir sobre a ciência e o cosmos em Azuzaria?"
    
    balao.config(text=msg, fg="black")
    animar_fala_personagem(obj_personagem)

# =============================================================================
# --- BLOCO 3: SUPER BANCO DE FRASES MOTIVACIONAIS ---
# =============================================================================
FRASES_MOTIVACIONAIS = [
    "O conhecimento é a luz que ninguém jamais pode apagar de você. ✨",
    "A mente humana é um universo em constante expansão. Continue estudando e brilhando! 🌌",
    "Pequenos passos dados todos os dias levam a destinos extraordinários. Não pare! 🚀",
    "Beber água ajuda as conexões do cérebro a focarem melhor. Hidrate-se agora! 💧",
    "A persistência é a chave cósmica para abrir qualquer porta do conhecimento. 🔑",
    "Acredite na força das suas ideias. O universo adora mentes curiosas! 🌟",
    "Foque no progresso, não na perfeição. Cada linha estudada já é uma grande vitória! 📚",
    "Você é capaz de aprender tudo o que determinar em seu coração. Confie em si! 💎",
    "Até as galáxias mais lindas precisaram de tempo para se formar. Respeite o seu tempo. 💫",
    "O potencial de quem estuda é infinito como o espaço sideral. Vá em frente! 🪐",
    "Estudar é o superpoder que transforma sonhos em realidades palpáveis. 🎯",
    "A jornada do aprendizado é o caminho mais bonito para a liberdade da mente. 🌈",
    "Erros são apenas dados novos para a calculadora mental acertar da próxima vez! 🔢"
]

# =============================================================================
# --- BLOCO 4: INTERFACE (WIDGETS RECONSTRUÍDOS) ---
# =============================================================================

class WidgetAzuzaria:
    def __init__(self, master, img_path, nome, txt_btn, size=(250, 250)):
        self.nome, self.tamanho_img = nome, size
        self.off_x, self.off_y = 0, 0  # Inicialização preventiva antiautocrash do drag
        self.win = tk.Toplevel(master)
        self.win.overrideredirect(True); self.win.attributes("-topmost", True)
        self.win.attributes("-transparentcolor", "white"); self.win.geometry("350x800+950+50")
        self.win.config(bg='white')
        if os.path.exists(ARQUIVO_ICONE_AZUZARIA): self.win.iconbitmap(ARQUIVO_ICONE_AZUZARIA)
        self.win.bind("<Button-1>", self.on_click); self.win.bind("<B1-Motion>", self.on_drag)
        self.balao = tk.Label(self.win, text="Iniciando...", bg=COR_FUNDO_BALAO, font=("Segoe UI", 10, "bold"), wraplength=280, relief="solid", bd=1, padx=15, pady=10)
        self.balao.pack(side="top", pady=(180, 0)) 
        img = Image.open(img_path).resize(size, Image.Resampling.LANCZOS)
        self.photo_estatica = ImageTk.PhotoImage(img)
        self.lbl_img = tk.Label(self.win, image=self.photo_estatica, bg="white")
        self.lbl_img.pack(side="top")
        self.entry = tk.Entry(self.win, font=("Arial", 10, "bold"), width=30, bg=COR_FUNDO_BALAO, relief="solid", bd=1)
        self.entry.pack(side="top", pady=10)
        self.entry.bind("<Return>", lambda e: processar_ia_azuzaria(self))
        tk.Button(self.win, text=txt_btn, command=lambda: processar_ia_azuzaria(self), bg="#9370DB", fg="white", font=("Arial", 9, "bold")).pack(side="top", pady=5)
        self.loop_frases()

    def on_click(self, e): self.off_x, self.off_y = e.x, e.y
    def on_drag(self, e): self.win.geometry(f"+{self.win.winfo_x() + (e.x - self.off_x)}+{self.win.winfo_y() + (e.y - self.off_y)}")
    def loop_frases(self):
        self.balao.config(text=random.choice(FRASES_MOTIVACIONAIS))
        self.win.after(900000, self.loop_frases)

# =============================================================================
# --- BLOCO 5: MENU DE SELEÇÃO TOTAL ---
# =============================================================================

def escolher_anfitriao(root_ref):
    if root_ref.active_w: root_ref.active_w.win.destroy()
    sel = tk.Toplevel(root_ref); sel.overrideredirect(True); sel.geometry("600x350+550+250")
    try:
        img_sel = Image.open(ARQUIVO_BANNER_SELETOR).resize((600, 350), Image.Resampling.LANCZOS)
        sel.bg_photo = ImageTk.PhotoImage(img_sel); tk.Label(sel, image=sel.bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
    except: pass
    def set_p(t):
        with open(ARQUIVO_CONFIG, "w") as f: f.write(t)
        if t == "Luna": root_ref.active_w = WidgetAzuzaria(root_ref, IMAGEM_LUNA_BASE, "Luna", "Luna Responde")
        else: root_ref.active_w = WidgetAzuzaria(root_ref, IMAGEM_SOL_BASE, "Sol", "Sol Responde", size=(350,350))
        sel.destroy()
    tk.Button(sel, text="🌙 Luna", command=lambda: set_p("Luna"), bg="#ffb6c1", width=12, font=("Arial", 10, "bold")).place(x=100, y=240)
    tk.Button(sel, text="☀️ Sol", command=lambda: set_p("Sol"), bg="#ffe082", width=12, font=("Arial", 10, "bold")).place(x=370, y=240)

root = tk.Tk(); root.title("Luna & Friends"); root.geometry("800x650")
# --- TRAVA DE MAXIMIZAR ADICIONADA CONFORME DIRETRIZ ---
root.resizable(False, False)

if os.path.exists(ARQUIVO_ICONE_AZUZARIA): root.iconbitmap(ARQUIVO_ICONE_AZUZARIA)
try:
    bg_m = Image.open(ARQUIVO_BG_PRINCIPAL).resize((800, 650), Image.Resampling.LANCZOS)
    root.bg_tk = ImageTk.PhotoImage(bg_m); tk.Label(root, image=root.bg_tk).place(x=0, y=0, relwidth=1, relheight=1)
except: pass

tk.Label(root, text="LUNA & FRIENDS", bg="#0b0b1a", fg="#ff69b4", font=("Segoe UI", 30, "bold")).pack(pady=25)
ESTILO = {"font": ("Arial", 12, "bold"), "width": 25, "height": 2}
tk.Button(root, text="🚀 Portal Gemini", command=lambda: webbrowser.open("https://gemini.google.com"), bg="#ffb6c1", **ESTILO).pack(pady=7)

m_on = [False]
def menu_musica():
    if not m_on[0]:
        m = tk.Menu(root, tearoff=0, font=("Arial", 10, "bold"))
        for n, p in PLAYLIST_AZUZARIA.items(): 
            m.add_command(label=f"🎵 {n}", command=lambda path=p: winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP))
        m.post(root.winfo_pointerx(), root.winfo_pointery()); m_on[0] = True
    else: winsound.PlaySound(None, winsound.SND_PURGE); m_on[0] = False

tk.Button(root, text="🎵 Som de Azuzaria", command=menu_musica, bg="#98fb98", **ESTILO).pack(pady=7)

def abrir_cronicas_menu():
    m = tk.Menu(root, tearoff=0, font=("Arial", 10, "bold"))
    m.add_command(label="📖 O Despertar de Azuzaria", command=chamar_capitulo_1)
    m.add_command(label="📖 Salvando Andy", command=chamar_capitulo_2)
    m.add_command(label="📖 Calisto, o Guardião", command=chamar_capitulo_3)
    m.post(root.winfo_pointerx(), root.winfo_pointery())

tk.Button(root, text="📖 Crônicas de Azuzaria", command=abrir_cronicas_menu, bg="#4b0082", fg="white", **ESTILO).pack(pady=7)
tk.Button(root, text="🔄 Trocar Personagem", command=lambda: escolher_anfitriao(root), bg="#9370DB", fg="white", **ESTILO).pack(pady=7)
tk.Button(root, text="❌ Sair", command=root.quit, bg="#ff4757", fg="white", **ESTILO).pack(pady=7)

root.active_w = None
if os.path.exists(ARQUIVO_CONFIG):
    with open(ARQUIVO_CONFIG, "r") as f: p = f.read().strip()
    if p == "Luna": root.active_w = WidgetAzuzaria(root, IMAGEM_LUNA_BASE, "Luna", "Luna Responde")
    else: root.active_w = WidgetAzuzaria(root, IMAGEM_SOL_BASE, "Sol", "Sol Responde", size=(350,350))
else: escolher_anfitriao(root)
root.mainloop()
