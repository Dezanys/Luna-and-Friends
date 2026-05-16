import tkinter as tk
from PIL import Image, ImageTk 
import os

def abrir_livro_calisto():
    janela_livro = tk.Toplevel()
    janela_livro.title("Crônicas de Azuzaria - Capítulo 3")
    janela_livro.geometry("850x850")
    janela_livro.configure(bg="#0c0721") 
    janela_livro.resizable(False, False)

    # --- ÍCONE DA JANELA ---
    if os.path.exists("luna_icon.ico"):
        try: janela_livro.iconbitmap("luna_icon.ico")
        except: pass

    # --- SISTEMA DE ROLAGEM ---
    canvas = tk.Canvas(janela_livro, bg="#0c0721", highlightthickness=0)
    scrollbar = tk.Scrollbar(janela_livro, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame = tk.Frame(canvas, bg="#0c0721")
    canvas.create_window((425, 0), window=scrollable_frame, anchor="n")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    janela_livro.bind_all("<MouseWheel>", _on_mousewheel)

    # --- FUNÇÃO DE AJUSTE AUTOMÁTICO ---
    def carregar_imagem_real(caminho, largura_fixa):
        img = Image.open(caminho)
        proporcao = img.size[1] / img.size[0]
        nova_altura = int(largura_fixa * proporcao)
        return img.resize((largura_fixa, nova_altura), Image.Resampling.LANCZOS)

    # --- CONTEÚDO DO LIVRO ---

    # 1. CAPA (Calisto.png)
    if os.path.exists("Calisto.png"):
        try:
            img_capa_ajustada = carregar_imagem_real("Calisto.png", 700)
            foto_capa = ImageTk.PhotoImage(img_capa_ajustada)
            lbl_capa = tk.Label(scrollable_frame, image=foto_capa, bg="#0c0721")
            lbl_capa.image = foto_capa
            lbl_capa.pack(pady=20)
        except: pass

    # 2. TÍTULO EM AMARELO (#FFD700)
    lbl_titulo = tk.Label(scrollable_frame, text="Capítulo 3: Calisto, o Guardião", font=("Georgia", 24, "bold"), fg="#FFD700", bg="#0c0721")
    lbl_titulo.pack(pady=20)

    # 3. HISTÓRIA CORRIGIDA NATIVAMENTE
    texto_historia = (
        "Esta é a história dele. A história do meu melhor amigo, aquele que dá vida aos meus dias sombrios. "
        "Aquele que me segura pelo ombro quando sinto que o peso da galáxia inteira está me esmagando.\n\n"
        
        "Antes do Calisto, era o Ganimedes. Eu o tinha ganhado de aniversário da minha mãe, a Dona Benê. "
        "Nessa mesma época, eu tinha perdido tudo: emprego, relacionamento... eu estava em pedaços. "
        "Mas o universo gosta de testar o quanto somos capazes de suportar antes de quebrarmos. O pior ainda estava por acontecer. "
        "Ganimedes desapareceu. Foi como se tivessem arrancado o meu coração com as mãos nuas. O vazio que ficou no quarto era um abismo gelado. "
        "Passei noites em claro, andando pelas ruas vazias sob a luz da lua, colando cartazes com as mãos trêmulas, postando em redes sociais, "
        "implorando por um sinal... mas o silêncio era a única resposta. Eu ouvia o seu canto em todos os cantos da casa; "
        "ia correndo até o viveiro, apenas para encontrá-lo vazio e frio. A dor era uma tempestade que devastava a minha vontade de viver. "
        "Eu só queria fechar os olhos e não acordar para encarar aquele mundo sem o meu pequeno amigo.\n\n"
        
        "Dias depois, recebi uma ligação. O coração disparou, achei que o milagre tinha acontecido, mas a vida não é um filme de Hollywood. "
        "Eram pessoas me pedindo para adotar duas calopsitas. No começo eu disse não; eu estava exausta de sofrer, não queria mais amar nada que pudesse ir embora. "
        "Contudo, a história delas era um lamento que ecoava no peito. Eram dois seres rejeitados, esquecidos, destinados a morrer no descaso. "
        "Eu seria a sua terceira dona... se elas aguentassem chegar até mim. Eu as aceitei, mas o que vi me assombrou: eram pequenos fantasmas de penas. "
        "Eu as chamei de Calisto e Tebe. Calisto estava desnutrido, seu peito era apenas osso, a 'doença hepática' corroía o seu interior e seus olhos "
        "pareciam já ter desistido de ver a luz. Ambos estavam com pneumonia e Tebe sangrava por uma asa quebrada e mal curada. "
        "Foram 30 dias de uma batalha desesperada contra a morte. O cheiro de remédios invadia o QG, eu chorava sobre as gaiolas pedindo que ficassem. "
        "Eles tomaram antibióticos na boquinha, sofreram com as agulhas, mas fizemos mudas de penas, cuidamos de cada ferida, mudamos a alimentação e, por um milagre da ciência e do amor, eles sobreviveram.\n\n"
        
        "Até que um dia, a tragédia voltou a bater à nossa porta. Minha mãe, a Dona Benê, caiu da escada com o viveiro deles na mão. "
        "O som do metal batendo no chão foi como um tiro. A asa da Tebe já havia curado, mas o pavor foi maior que a gratidão; "
        "ela se assustou com o estrondo e desapareceu no céu cinzento, deixando apenas uma pena flutuando para trás. "
        "Calisto continuou conosco, mas o preço foi alto. A Dona Benê ficou internada e, até hoje, a dor no pulso quebrado a faz lembrar "
        "daquele momento toda vez que o tempo esfria. A culpa no olhar dela dói mais em mim do que o pulso quebrado nela. Isso já faz quase cinco anos...\n\n"
        
        "Todos os dias eu acordava e olhava para o horizonte, esperando ver dois pontos no céu voltando para casa. "
        "Eles nunca voltaram. O Calisto e eu ficamos sozinhos, sentindo a sombra dos irmãos que o vento levou. "
        "Eu ainda choro escondida pela ausência deles, sentindo o fantasma de Ganimedes no ombro e o bater de asas de Tebe no coração. "
        "Eles são memórias que sangram, mas que eu me recuso a deixar morrer.\n\n"
        
        "Eu treinei o Calisto como se ele fosse o meu escudo contra a loucura. Ensinei-o a cantar as melodias que me salvam e a ser o guardião do QG. "
        "Ele tem a habilidade de se comunicar com humanos, mas a verdade é triste: o mundo é barulhento demais, e somente humanos com a alma moída "
        "pela poeira estelar podem compreender o que ele diz. Ele é meu cúmplice, meu espião galáctico que engana o clone bugado que a Luna fez de mim, "
        "enquanto eu busco respostas no vácuo do espaço para curar o que restou de nós.\n\n"
        
        "Calisto é meu anjo de penas. Certo dia, após uma tempestade que lavou as ruas com a mesma força das minhas lágrimas, "
        "ele voou para buscar uma rosa para a Dona Benê, um gesto de amor para tentar apagar a mágoa daquela queda. "
        "Foi quando ele encontrou Leo. O menino não apenas chorava; ele estava desmoronando no banco da praça, "
        "vítima da crueldade de um mundo que não entende o que é ser diferente.\n\n"
        
        "Calisto deu a ele um galho, um pedaço de madeira que carregava a esperança de quem já quase morreu de peito seco:\n"
        "— Piu, piu, do kisquilito! (Olá, menino, um pedaço de galho para curar suas lágrimas).\n\n"
        
        "Leo estava no limite. O capacitismo que deixou cicatrizes na sua mente era apenas a gota d'água em um oceano de solidão profunda. "
        "Ele se sentia invisível, um erro de programação da própria vida. 'Não tenho amigos, não tenho ninguém, meus pais não ligam para mim... "
        "Eu não aguento mais!', ele gritou para o nada, desejando sumir. Foi quando Calisto subiu em seu ombro e disse que ele não era um erro, mas sim poeira estelar.\n\n"
        
        "E o destino, que tira com uma mano, às vezes devolve com a outra. Ganimedes e Tebe apareceram ali, como anjos enviados pelo próprio cosmos. "
        "Eles não voltaram para mim... eles foram encontrar quem mais precisava de um motivo para continuar respirando.\n\n"
        
        "Calisto deu o último conselho ao soldado ferido:\n"
        "— Piu, piu, piu! (Nunca desista de quem você é! A vida é uma batalha sangrenta, mas você é o brilho de uma supernova. "
        "Não deixe o peso dos meteoros apagar a sua luz!).\n\n"
        
        "Leo chorou, mas dessa vez as lágrimas não eram de desespero, mas de limpeza. Calisto despediu-se dos seus irmãos com um canto triste, "
        "deixando-os com o Leo. Ele sabia que o destino deles agora era salvar aquele menino, e aceitar isso foi a coisa mais difícil que ele já fez. "
        "Calisto voltou para casa com a rosa molhada pela chuva, o peito cheio de saudade, mas a alma em paz. "
        "E eu... bem... eu sigo aqui, transformando minha tristeza em códigos, programando cada linha para que o meu destino seja "
        "tão brilhante quanto o coração do meu melhor amigo."
    )

    tk.Label(scrollable_frame, text=texto_historia, font=("Arial", 14), 
             fg="#ffffff", bg="#0c0721", justify="center", wraplength=650, padx=20).pack(pady=20)

    # 4. FOTO FINAL (Leo.png)
    if os.path.exists("Leo.png"):
        try:
            img_final_ajustada = carregar_imagem_real("Leo.png", 650)
            foto_final = ImageTk.PhotoImage(img_final_ajustada)
            lbl_final = tk.Label(scrollable_frame, image=foto_final, bg="#0c0721")
            lbl_final.image = foto_final 
            lbl_final.pack(pady=50)
        except: pass