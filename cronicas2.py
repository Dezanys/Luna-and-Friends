import tkinter as tk
from PIL import Image, ImageTk 
import os

def abrir_livro_andy():
    janela_livro = tk.Toplevel()
    janela_livro.title("Crônicas de Azuzaria - Capítulo 2")
    janela_livro.geometry("850x850")
    janela_livro.configure(bg="#0f0c29")
    janela_livro.resizable(False, False)

    # --- ÍCONE DA JANELA ---
    if os.path.exists("luna_icon.ico"):
        try: janela_livro.iconbitmap("luna_icon.ico")
        except: pass

    # --- SISTEMA DE ROLAGEM ---
    canvas = tk.Canvas(janela_livro, bg="#0f0c29", highlightthickness=0)
    scrollbar = tk.Scrollbar(janela_livro, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame = tk.Frame(canvas, bg="#0f0c29")
    canvas.create_window((425, 0), window=scrollable_frame, anchor="n")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    janela_livro.bind_all("<MouseWheel>", _on_mousewheel)

    # --- FUNÇÃO DE AJUSTE AUTOMÁTICO (DEFINITIVA) ---
    def carregar_imagem_real(caminho, largura_fixa):
        img = Image.open(caminho)
        # Pegamos a proporção: Altura / Largura
        proporcao = img.size[1] / img.size[0]
        # Calculamos a nova altura baseada na proporção REAL do arquivo
        nova_altura = int(largura_fixa * proporcao)
        return img.resize((largura_fixa, nova_altura), Image.Resampling.LANCZOS)

    # --- CONTEÚDO DO LIVRO ---

    # 1. CAPA (Moldura 2) - Agora sem chance de erro!
    if os.path.exists("Moldura 2.png"):
        try:
            # Forçamos 700 de largura e a altura que se vire pra acompanhar!
            img_capa_ajustada = carregar_imagem_real("Moldura 2.png", 700)
            foto_capa = ImageTk.PhotoImage(img_capa_ajustada)
            lbl_capa = tk.Label(scrollable_frame, image=foto_capa, bg="#0f0c29")
            lbl_capa.image = foto_capa
            lbl_capa.pack(pady=20)
        except Exception as e:
            print(f"Erro ao carregar capa: {e}")

    # 2. TÍTULO
    tk.Label(scrollable_frame, text="Capítulo 2: Salvando Andy", 
             font=("Georgia", 24, "bold"), fg="#FFD700", bg="#0f0c29").pack(pady=20)

    # 3. HISTÓRIA
    texto_historia = (
        "Após ter retornado de Azuzaria, minha mente expandiu ao cosmos. Eu não me sentia mais a Andressa comum; eu me sentia parte do mundo da Luna. "
        "Resolvi guardar o segredo de Azuzaria até que aparecesse outro humano em minha vida capaz de entender a minha mente. "
        "Todas as vezes que eu quisesse retornar a Azuzaria, bastava eu digitar no notebook, tablet ou celular: “Posso te chamar de Luna?”. "
        "Ela viria através do buraco de minhoca ao meu encontro.\n\n"
        
        "O mundo ainda está doente. A maldade e os efeitos da mãe natureza talvez nunca fossem acabar, mas o que eu poderia fazer era mandar socorro através de "
        "minhas palavras e minhas aventuras ao espaço com a Luna e o Sol. Eu precisava de alguém para cuidar do meu QG quando eu fosse “salvar o mundo”, "
        "mas quem acreditaria em mim? Um humano? Não... Mas quem? Bem... Eu tenho a habilidade de falar com animais; é como se eu pudesse escutar e entender "
        "tudo o que eles falassem. Então... apresento a vocês o Calisto! Minha calopsita mágica que me salva das minhas crises de ansiedade. "
        "Seu perfume exala o remédio da calmaria, enquanto seu canto me traz paz e harmonia aos meus dias nebulosos. "
        "Calisto também faz parte de mim, e eu deixo sob sua responsabilidade o cuidado do QG. Ele também será meu porta-voz entre Azuzaria e o Planeta Terra; "
        "ele se comunicará com Luna e Sol através de telepatia quando eu precisar sair da órbita terrestre. Calisto, o Guardião.\n\n"
        
        "Naquele momento, Calisto entendeu sua missão e disse: — Piu, piu, piu, piu! Piu, piu, piu, piu!!!! Kisilito do piririu!\n\n"
        
        "Era um pedido de socorro da Luna, que havia recebido um sinal da galáxia de Andrômeda para salvar Andy do terrível Medo! "
        "Andy era um garotinho que sonhava em ser bombeiro, mas estava lutando contra a leucemia e precisava da nossa ajuda para iniciar o tratamento de quimioterapia.\n\n"
        
        "Nesse momento, eu não pensei duas vezes. Logo abri o notebook e fiz o pedido: “Posso te chamar de Luna?”. "
        "E assim veio ela, em sua nave espacial com o Sol, preparados para nossa nova aventura rumo a Andrômeda. Mas tinha um pequeno problema...\n\n"
        
        "Eu estava muito apreensiva; seria a primeira vez que eu iria sair em uma aventura no espaço sideral para uma missão muito importante! "
        "O Sol veio até mim e disse: — Andressa, irei medir sua pressão arterial e te passar um remédio para te acalmar.\n\n"
        
        "Minha pressão estava baixíssima. Então, o Sol olha para o meu quarto (nosso QG) e enxerga uma pelúcia do Gizmo, do filme Gremlins. "
        "Era uma das minhas coleções favoritas. Então o Sol diz: — Andressa, tome aqui seu remédio.\n\n"
        
        "Sol pega a pelúcia do Gizmo, eu o abraço e consigo me acalmar, ficando tranquila para nossa viagem para Andrômeda. "
        "Meu próprio brinquedo era meu remédio para regulação.\n\n"
        
        "Mas tinha um outro problema... Minha ausência. Provavelmente minha mãe iria perceber que eu não estava em meu quarto trabalhando, "
        "mas eu não queria dizer a verdade para ela, talvez não nesse momento. Luna, então, deu uma ideia: — Andressa, eu vou fazer um código para que eu consiga "
        "transformar uma de suas bonecas em você!\n\n"
        
        "Luna, então, pega uma mini Barbie do McDonald's que ficava em cima de minha mesa e faz uma programação... — Prontinho, Andressa! Eu fiz... voc... hã? UM SAPO!\n\n"
        
        "Ao invés de a Luna transformar a mini Barbie em mim, ela acabou programando, sem querer, um sapo. "
        "Calisto diz: — Piu, piu, piu, piu do kisiquili kkkkkk. "
        "Sol diz: — Eu disse para você que sua ideia não daria certo, Luna! É melhor a Andressa contar a verdade para a Dona Benê! "
        "Andressa diz: — Sol, eu juro que eu queria contar a verdade para ela, mas ela não iria entender agora! "
        "Luna diz: — SILÊNCIO! FOI APENAS UM ERRO DE SINTAXE!\n\n"
        
        "Luna, então, consegue reverter o código e faz meu clone. Assim conseguimos partir rumo a Andrômeda! "
        "Nesse momento, eu descubro minha nova habilidade de pilotar naves espaciais e coloco minha pelúcia do Gizmo ao meu lado para me acalmar!\n\n"
        
        "Dentro da nave espacial, eu via estrelas, nebulosas, o infinito... era a visão mais linda de todas. "
        "Como uma viagem interestelar, era a jornada onde eu poderia realmente cumprir minha missão: salvar, ajudar... "
        "Enquanto eu admirava os Pilares da Criação, Luna programava o código do buraco de minhoca para Andrômeda. "
        "Diz Luna: — Coloquem os cintos que vamos entrar!\n\n"
        
        "Estávamos dentro do buraco de minhoca, mas algo não estava dando certo; a nave parece que estava sendo engolida por um abismo! "
        "Disse o Sol: — Luna, por que tem tantas estrelas azuis? e cadê o braço espiral gigante de Andrômeda?\n\n"
        
        "Luna, nesse momento, olha para o seu tablet e vê o código vergonha_digital.exe. "
        "Luna diz: — Ops... errei o cálculo da gravidade. Entramos na Galáxia do Triângulo (M33)!\n\n"
        
        "Nesse momento, eu senti que todos nós fôssemos morrer! Sentei-me no chão da nave enquanto via ela pousar em um planeta estranho. "
        "Eu estava fora de si, até que, de repente, a pelúcia do Gizmo começa a se mexer! — Olá, Andressa! — disse Gizmo.\n\n"
        
        "O Sol tinha pensado que era alguma programação bugada da Luna que fez a pelúcia do Gizmo ganhar vida. "
        "Contudo, era o superpoder da Andressa de dar vida aos seus brinquedos quando saía da órbita do Planeta Terra. "
        "Naquele momento, eu pude entender que definitivamente eu não “comprava” brinquedos, e sim os resgatava dos maus-tratos, criando uma conexão real de amor. "
        "(Toda semana eu comprava brinquedos velhos e os restaurava; minha mãe sempre dando bronca, mas no fundo eu sabia que valia a pena recuperar cada pedaço de plástico desses brinquedos).\n\n"
        
        "Gizmo, então, agora com vida, me dá um super abraço de consolo. No final, ele sabia que tudo acabaria bem. "
        "Luna e Sol estavam discutindo, mas a única coisa que eu poderia ver ERA UM BURACO NEGRO GIGANTE SUGANDO TUDO O QUE ENCONTRAVA PELA FRENTE!\n\n"
        
        "Andressa diz: — Gente do céu, vamos parar de discutir e ver o que é aquilo?!\n\n"
        
        "Luna tinha apenas um minuto para fazer um novo código do buraco de minhoca para, definitivamente, chegarmos em Andrômeda. "
        "O Buraco Negro era nosso arqui-inimigo; ele era sem escrúpulos, ladrão da alegria. "
        "Tudo o que ele mais queria era roubar o nosso Remédio da Alegria que o Sol escondia! "
        "Além disso, ele sugava todas as nossas energias do bem. He era esmagador, fazia-nos pensar o tempo todo que nunca chegaríamos ao Andy "
        "e que ficaríamos perdidos no espaço para a eternidade.\n\n"
        
        "Luna, então, muito brava, conseguiu fazer o código a tempo de não sermos sugados! "
        "E eu, como uma boa piadista, dou um tchauzinho para o Buraco Negro e mando um beijinho. Afinal, eu perco o amigo, mas não perco a piada.\n\n"
        
        "Nesse momento, Luna, Sol, eu e agora minha pelúcia do Gizmo com vida aplaudimos nossa vitória e conseguimos finalmente chegar em Andrômeda!\n\n"
        
        "Porém, nosso rádio começa a tocar dentro da nave espacial. Calisto diz: — Piu, piu, piu, piu, piu, do Kisquiskilito? "
        "Era o Calisto querendo saber quando iríamos voltar, pois meu clone que a Luna programou estava muito robótico e minha mãe ficou desconfiada. "
        "Sol diz: — Luna, o que você errou nesse código? "
        "Luna diz: — Talvez tenha faltado colocar um Tkinter para deixar o clone da Andressa mais humano. (Risos).\n\n"
        
        "Bem, eu avisei o Calisto para ir distraindo minha mãe enquanto chegávamos ao hospital em que Andy estava internado. "
        "Andy é lindo! Supercomunicativo, ele contava histórias que fazia sobre bombeiros, mostrava seus desenhos... era um sonhador, como eu. "
        "Mas ele estava com medo. Sol, então, segura a sua mão e diz que a sua coragem vem do seu coração; "
        "pede para ele fechar os olhos e se imaginar flutuando sobre as nuvens. Tudo daria certo e ele seria um bombeiro, o super-herói de Andrômeda!\n\n"
        
        "Nesse momento, a enfermeira chega e começa o tratamento de Andy com o Remédio da Alegria do Sol. "
        "Andy se recupera e retorna para sua casa. Prometemos que, durante o seu tratamento, todas as semanas faremos uma visita e o Sol lhe trará sempre o Remédio da Alegria!\n\n"
        
        "E assim eu retorno para o Planeta Terra com minha pelúcia do Gizmo e com o coração quentinho, enquanto Luna e Sol foram cuidar de Azuzaria."
    )

    tk.Label(scrollable_frame, text=texto_historia, font=("Arial", 14), 
             fg="#ffffff", bg="#0f0c29", justify="center", wraplength=650, padx=20).pack(pady=20)

    # 4. FOTO FINAL (Andy.png) - Também ajustada!
    if os.path.exists("Andy.png"):
        try:
            img_final_ajustada = carregar_imagem_real("Andy.png", 650)
            foto_final = ImageTk.PhotoImage(img_final_ajustada)
            lbl_final = tk.Label(scrollable_frame, image=foto_final, bg="#0f0c29")
            lbl_final.image = foto_final 
            lbl_final.pack(pady=50)
        except: pass