import pygame
import sys
import os
import random

# =============================================================================
# --- BLOCO 1: INICIALIZAÇÃO E CONFIGURAÇÕES ---
# =============================================================================
pygame.init()
pygame.mixer.init()

LARGURA_TELA = 800
ALTURA_TELA = 600

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.RESIZABLE)
pygame.display.set_caption("Luna Run - Módulo Arcade")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL_ESPACIAL = (30, 30, 45)
ROXO_LUNA = (139, 92, 246)
AMARELO_ESTRELA = (255, 223, 0)
CINZA_PAUSA = (50, 50, 65)

fonte_menu = pygame.font.SysFont("Arial", 30, bold=True)
fonte_texto = pygame.font.SysFont("Arial", 20, bold=True)

# Estados do Jogo
MENU = "menu"
SELECAO = "selecao"
INSTRUCOES = "instrucoes"
JOGANDO = "jogando"
PAUSA = "pausa"
GAME_OVER = "game_over"
estado_atual = MENU

personagem_escolhido = None

# =============================================================================
# --- SISTEMA DE ARQUIVO PARA SALVAR O RECORDE ---
# =============================================================================
ARQUIVO_RECORDE = "recorde.txt"

def carregar_recorde():
    if os.path.exists(ARQUIVO_RECORDE):
        try:
            with open(ARQUIVO_RECORDE, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def salvar_recorde(novo_recorde):
    try:
        with open(ARQUIVO_RECORDE, "w") as f:
            f.write(str(novo_recorde))
    except:
        pass

recorde = carregar_recorde()

# =============================================================================
# --- BLOCO 2: TAMANHOS GIGANTES E CARREGAMENTO DE IMAGENS ---
# =============================================================================
# --- AJUSTE FEITO AQUI: AUMENTEI A LUNA E O SOL (PLAYER_W e PLAYER_H) ---
PLAYER_W, PLAYER_H = 220, 230  # Antes era 180, 190. Ficaram grandões!
BOCAO_W, BOCAO_H = 120, 120      
CRISTAL_W, CRISTAL_H = 65, 65
ALTURA_CHAO = 110

def carregar_img(nome):
    return pygame.image.load(nome) if os.path.exists(nome) else None

def carregar_e_ajustar(nome, largura, height):
    if os.path.exists(nome):
        img = pygame.image.load(nome).convert_alpha()
        return pygame.transform.scale(img, (largura, height))
    return None

# Imagens Originais
img_menu_original = carregar_img("Luna Run Menu.png")
img_fundo_original = carregar_img("Fundo do Jogo.png")
img_luna_menu = carregar_img("Luna Sorrindo.png")
img_sol_menu = carregar_img("Sol Sorrindo.png")

# Sprites de Corrida e Pulo
sprites_luna_corrida = []
f1_luna = carregar_e_ajustar("Luna Correndo.png", PLAYER_W, PLAYER_H)
f2_luna = carregar_e_ajustar("Luna Correndo 2.png", PLAYER_W, PLAYER_H)
f3_luna = carregar_e_ajustar("Luna Correndo 3.png", PLAYER_W, PLAYER_H)
if f1_luna: sprites_luna_corrida.append(f1_luna)
if f2_luna: sprites_luna_corrida.append(f2_luna)
if f3_luna: sprites_luna_corrida.append(f3_luna)
img_luna_pulando = carregar_e_ajustar("Luna Pulando.png", PLAYER_W, PLAYER_H)

sprites_sol_corrida = []
f1_sol = carregar_e_ajustar("Sol Correndo.png", PLAYER_W, PLAYER_H)
f2_sol = carregar_e_ajustar("Sol Correndo 2.png", PLAYER_W, PLAYER_H)
f3_sol = carregar_e_ajustar("Sol Correndo 3.png", PLAYER_W, PLAYER_H)
if f1_sol: sprites_sol_corrida.append(f1_sol)
if f2_sol: sprites_sol_corrida.append(f2_sol)
if f3_sol: sprites_sol_corrida.append(f3_sol)
img_sol_pulando = carregar_e_ajustar("Sol Pulando.png", PLAYER_W, PLAYER_H)

# Obstáculos e Coletáveis
img_bocao_original = pygame.image.load("Bocão.png").convert_alpha() if os.path.exists("Bocão.png") else None
img_cristal_original = carregar_e_ajustar("Cristal Luna Run.png", CRISTAL_W, CRISTAL_H)

img_menu_bg = pygame.transform.scale(img_menu_original, (LARGURA_TELA, ALTURA_TELA)) if img_menu_original else None
img_fundo_jogo = pygame.transform.scale(img_fundo_original, (LARGURA_TELA, ALTURA_TELA)) if img_fundo_original else None

if os.path.exists("luna_icon.png"):
    pygame.display.set_icon(pygame.image.load("luna_icon.png"))

# Função auxiliar para garantir o play da música sem travar o jogo
def iniciar_musica_loop():
    try:
        if os.path.exists("Luna Run.wav"):
            if not pygame.mixer.music.get_busy(): # Só dá play se já não estiver tocando
                pygame.mixer.music.load("Luna Run.wav")
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
    except:
        pass

iniciar_musica_loop()

relogio = pygame.time.Clock()
pos_x_fundo = 0
frame_atual_idx = 0
tempo_animacao = 0

# =============================================================================
# --- BLOCO 3: VARIÁVEIS DA FÍSICA E GAMEPLAY ---
# =============================================================================
y_chao_atual = ALTURA_TELA - ALTURA_CHAO

player_x = 80
player_y = y_chao_atual - PLAYER_H
player_vel_y = 0

esta_pulando = False
contador_pulos = 0  
pulo_pressionado = False 

GRAVIDADE = 0.75
FORCA_PULO = -17.5  

bocoes = []
cristais = []

velocidade_jogo = 6  # Modo rápido ativado!
pontuacao = 0
timer_spawn = 0

def reiniciar_jogo():
    global player_y, player_vel_y, esta_pulando, contador_pulos, bocoes, cristais, pontuacao, velocidade_jogo, pos_x_fundo, frame_atual_idx, tempo_animacao
    player_y = (ALTURA_TELA - ALTURA_CHAO) - PLAYER_H
    player_vel_y = 0
    esta_pulando = False
    contador_pulos = 0
    bocoes = []
    cristais = []
    pontuacao = 0
    velocidade_jogo = 6  
    pos_x_fundo = 0
    frame_atual_idx = 0
    tempo_animacao = 0

# =============================================================================
# --- BLOCO 4: FUNÇÕES DE INTERFACE ---
# =============================================================================
def desenhar_botao(texto, x, y, largura, altura, cor_ativa, cor_repouso, tamanho_fonte=30):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    
    fonte_usar = pygame.font.SysFont("Arial", tamanho_fonte, bold=True)
    
    if x + largura > mouse[0] > x and y + altura > mouse[1] > y:
        pygame.draw.rect(tela, cor_ativa, (x, y, largura, altura), border_radius=10)
        if clique[0] == 1:
            pygame.time.delay(150)
            return True
    else:
        pygame.draw.rect(tela, cor_repouso, (x, y, largura, altura), border_radius=10)
    
    txt_surf = fonte_usar.render(texto, True, BRANCO)
    tela.blit(txt_surf, (x + (largura/2 - txt_surf.get_width()/2), y + (altura/2 - txt_surf.get_height()/2)))
    return False

# =============================================================================
# --- BLOCO 5: LOOP PRINCIPAL ---
# =============================================================================
rodando = True

while rodando:
    relogio.tick(60)
    y_chao_atual = ALTURA_TELA - ALTURA_CHAO
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
        elif evento.type == pygame.VIDEORESIZE:
            LARGURA_TELA, ALTURA_TELA = evento.w, evento.h
            tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.RESIZABLE)
            if img_menu_original: img_menu_bg = pygame.transform.scale(img_menu_original, (LARGURA_TELA, ALTURA_TELA))
            if img_fundo_jogo: img_fundo_jogo = pygame.transform.scale(img_fundo_original, (LARGURA_TELA, ALTURA_TELA))
        
        # Tecla P para Pausa
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_p:
                if estado_atual == JOGANDO:
                    estado_atual = PAUSA
                    pygame.mixer.music.pause()
                elif estado_atual == PAUSA:
                    estado_atual = JOGANDO
                    pygame.mixer.music.unpause()

    # --- MÁQUINA DE ESTADOS ---
    
    if estado_atual == MENU:
        iniciar_musica_loop()
        
        if img_menu_bg: tela.blit(img_menu_bg, (0,0))
        else: tela.fill(PRETO)
        pos_x_botao = LARGURA_TELA / 2 - 100
        if desenhar_botao("INICIAR", pos_x_botao, ALTURA_TELA * 0.45, 200, 60, ROXO_LUNA, AZUL_ESPACIAL): estado_atual = SELECAO
        if desenhar_botao("MANUAL", pos_x_botao, ALTURA_TELA * 0.58, 200, 60, ROXO_LUNA, AZUL_ESPACIAL): estado_atual = INSTRUCOES
        if desenhar_botao("SAIR", pos_x_botao, ALTURA_TELA * 0.71, 200, 60, (200,0,0), (100,0,0)): rodando = False

    elif estado_atual == SELECAO:
        tela.fill(AZUL_ESPACIAL)
        txt = fonte_menu.render("QUEM VAI CORRER HOJE?", True, BRANCO)
        tela.blit(txt, (LARGURA_TELA/2 - txt.get_width()/2, ALTURA_TELA * 0.1))
        
        largura_avatar, altura_avatar = int(LARGURA_TELA * 0.18), int(ALTURA_TELA * 0.3)
        pos_x_luna, pos_x_sol = LARGURA_TELA * 0.2, LARGURA_TELA * 0.6
        pos_y_imagens, pos_y_botoes = ALTURA_TELA * 0.25, ALTURA_TELA * 0.6
        
        if img_luna_menu: tela.blit(pygame.transform.scale(img_luna_menu, (largura_avatar, altura_avatar)), (pos_x_luna + 10, pos_y_imagens))
        if img_sol_menu: tela.blit(pygame.transform.scale(img_sol_menu, (largura_avatar, altura_avatar)), (pos_x_sol + 10, pos_y_imagens))
        
        if desenhar_botao("LUNA", pos_x_luna, pos_y_botoes, 200, 60, ROXO_LUNA, PRETO):
            personagem_escolhido = "Luna"
            reiniciar_jogo()
            estado_atual = JOGANDO
        if desenhar_botao("SOL", pos_x_sol, pos_y_botoes, 200, 60, (255, 165, 0), PRETO):
            personagem_escolhido = "Sol"
            reiniciar_jogo()
            estado_atual = JOGANDO
            
        if desenhar_botao("VOLTAR", LARGURA_TELA/2 - 75, ALTURA_TELA * 0.85, 150, 40, (100,100,100), (50,50,50)): estado_atual = MENU

    elif estado_atual == INSTRUCOES:
        tela.fill(PRETO)
        txt_titulo = fonte_menu.render("MANUAL DE INSTRUÇÕES", True, ROXO_LUNA)
        tela.blit(txt_titulo, (LARGURA_TELA/2 - txt_titulo.get_width()/2, 50))
        
        instrucoes = [
            "- Pule os BOCÕES usando a BARRA DE ESPAÇO (Aperte 2x para PULO DUPLO!)",
            "- Colete as ESTRELAS para aumentare sua pontuação",
            "- Aperte 'P' ou clique no botão do canto para PAUSAR o jogo",
            "- Volte para o Menu a qualquer momento apertando 'M'",
            " ",
            "Clique no botão abaixo para voltar."
        ]
        for i, linha in enumerate(instrucoes):
            txt_l = fonte_texto.render(linha, True, BRANCO)
            tela.blit(txt_l, (LARGURA_TELA * 0.05, 150 + (i * 40)))

        if desenhar_botao("ENTENDIDO!", LARGURA_TELA/2 - 100, ALTURA_TELA * 0.8, 200, 50, ROXO_LUNA, AZUL_ESPACIAL): estado_atual = MENU

    elif estado_atual == JOGANDO:
        if img_fundo_jogo:
            pos_x_fundo -= velocidade_jogo * 0.15  
            rel_x = int(pos_x_fundo % LARGURA_TELA)
            tela.blit(pygame.transform.scale(img_fundo_jogo, (LARGURA_TELA, ALTURA_TELA)), (rel_x - LARGURA_TELA, 0))
            if rel_x < LARGURA_TELA:
                pygame.transform.scale(img_fundo_jogo, (LARGURA_TELA, ALTURA_TELA))
                tela.blit(pygame.transform.scale(img_fundo_jogo, (LARGURA_TELA, ALTURA_TELA)), (rel_x, 0))
        else:
            tela.fill(AZUL_ESPACIAL)
        
        pygame.draw.rect(tela, (18, 18, 30), (0, y_chao_atual, LARGURA_TELA, ALTURA_CHAO))
        pygame.draw.rect(tela, ROXO_LUNA, (0, y_chao_atual, LARGURA_TELA, 5))
        
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE]:
            if not pulo_pressionado: 
                if contador_pulos < 2:
                    player_vel_y = FORCA_PULO
                    esta_pulando = True
                    contador_pulos += 1
                pulo_pressionado = True
        else:
            pulo_pressionado = False 

        if teclas[pygame.K_m]: estado_atual = MENU

        player_vel_y += GRAVIDADE
        player_y += player_vel_y
        
        if player_y >= y_chao_atual - PLAYER_H:
            player_y = y_chao_atual - PLAYER_H
            esta_pulando = False
            contador_pulos = 0  
            player_vel_y = 0

        tempo_animacao += 1
        # --- AJUSTE FEITO AQUI: DIMINUÍ A VELOCIDADE DAS PERNINHAS (Aumentei o tempo de troca) ---
        vel_troca_frame = max(6, 14 - int(velocidade_jogo)) # Antes era max(3, 10 - ...)
        if tempo_animacao >= vel_troca_frame: 
            tempo_animacao = 0
            frame_atual_idx += 1

        timer_spawn += 1
        if timer_spawn > random.randint(90, 160): 
            timer_spawn = 0
            if random.choice([True, False]):
                tamanho_bocao = random.randint(100, 220)
                bocoes.append(pygame.Rect(LARGURA_TELA, y_chao_atual - tamanho_bocao, tamanho_bocao, tamanho_bocao))
            else:
                cristais.append(pygame.Rect(LARGURA_TELA, y_chao_atual - random.randint(180, 290), CRISTAL_W, CRISTAL_H))

        rect_player = pygame.Rect(player_x, player_y, PLAYER_W, PLAYER_H)
        rect_player_colisao = rect_player.inflate(-80, -80) 

        if esta_pulando:
            frame_final = img_luna_pulando if personagem_escolhido == "Luna" else img_sol_pulando
            if not frame_final: 
                sprites = sprites_luna_corrida if personagem_escolhido == "Luna" else sprites_sol_corrida
                frame_final = sprites[0] if sprites else None
        else:
            sprites = sprites_luna_corrida if personagem_escolhido == "Luna" else sprites_sol_corrida
            if sprites: 
                frame_final = sprites[frame_atual_idx % len(sprites)]
            else: 
                frame_final = None

        if frame_final: 
            tela.blit(frame_final, (player_x, player_y))
        else: 
            pygame.draw.rect(tela, ROXO_LUNA if personagem_escolhido == "Luna" else (255,165,0), rect_player)

        for bocao in bocoes[:]:
            bocao.x -= velocidade_jogo
            fator_reducao = int(bocao.width * 0.45)
            rect_bocao_colisao = bocao.inflate(-fator_reducao, -fator_reducao) 
            
            if img_bocao_original:
                img_bocao_redimensionada = pygame.transform.scale(img_bocao_original, (bocao.width, bocao.height))
                tela.blit(img_bocao_redimensionada, (bocao.x, bocao.y))
            else:
                pygame.draw.rect(tela, (220, 50, 50), bocao, border_radius=8)
            
            if rect_player_colisao.colliderect(rect_bocao_colisao):
                if pontuacao > recorde:
                    recorde = pontuacao
                    salvar_recorde(recorde)
                estado_atual = GAME_OVER
            
            if bocao.x < -bocao.width: 
                bocoes.remove(bocao)

        for cristal in cristais[:]:
            cristal.x -= velocidade_jogo
            if img_cristal_original:
                tela.blit(img_cristal_original, (cristal.x, cristal.y))
            else:
                pygame.draw.rect(tela, AMARELO_ESTRELA, cristal, border_radius=12)
            
            if rect_player_colisao.colliderect(cristal):
                pontuacao += 1
                cristais.remove(cristal)
                if pontuacao % 3 == 0: velocidade_jogo += 1 
                
            elif cristal.x < -CRISTAL_W:
                cristais.remove(cristal)

        txt_pontos = fonte_texto.render(f"ESTRELAS COLETADAS: {pontuacao}", True, BRANCO)
        txt_recorde_tela = fonte_texto.render(f"PONTUAÇÃO MÁXIMA: {recorde}", True, AMARELO_ESTRELA)
        tela.blit(txt_pontos, (20, 20))
        tela.blit(txt_recorde_tela, (20, 50))

        if desenhar_botao("||", LARGURA_TELA - 60, 20, 40, 40, ROXO_LUNA, CINZA_PAUSA, tamanho_fonte=20):
            estado_atual = PAUSA
            pygame.mixer.music.pause()

    elif estado_atual == PAUSA:
        filtro_escuro = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
        filtro_escuro.set_alpha(5) 
        filtro_escuro.fill(PRETO)
        tela.blit(filtro_escuro, (0,0))

        txt_pausa = fonte_menu.render("JOGO PAUSADO", True, AMARELO_ESTRELA)
        txt_dica = fonte_texto.render("(Dica: Você também pode apertar a tecla 'P')", True, BRANCO)
        tela.blit(txt_pausa, (LARGURA_TELA/2 - txt_pausa.get_width()/2, ALTURA_TELA * 0.3))
        tela.blit(txt_dica, (LARGURA_TELA/2 - txt_dica.get_width()/2, ALTURA_TELA * 0.38))

        pos_x_botao = LARGURA_TELA / 2 - 100
        if desenhar_botao("RETOMAR", pos_x_botao, ALTURA_TELA * 0.48, 200, 50, ROXO_LUNA, AZUL_ESPACIAL):
            estado_atual = JOGANDO
            pygame.mixer.music.unpause()
            
        if desenhar_botao("VOLTAR PRO MENU", pos_x_botao, ALTURA_TELA * 0.59, 200, 50, (150, 150, 150), CINZA_PAUSA, tamanho_fonte=18):
            pygame.mixer.music.unpause() 
            pygame.mixer.music.stop()    
            estado_atual = MENU

    elif estado_atual == GAME_OVER:
        tela.fill(PRETO)
        txt_go = fonte_menu.render("GAME OVER - O BOCÃO TE PEGOU!", True, (255, 0, 0))
        txt_sub = fonte_texto.render(f"Você salvou {pontuacao} estrelas nesta corrida!", True, BRANCO)
        txt_rec_go = fonte_texto.render(f"O Recorde de Azuzaria é: {recorde} estrelas!", True, AMARELO_ESTRELA)
        
        tela.blit(txt_go, (LARGURA_TELA/2 - txt_go.get_width()/2, ALTURA_TELA * 0.25))
        tela.blit(txt_sub, (LARGURA_TELA/2 - txt_sub.get_width()/2, ALTURA_TELA * 0.4))
        tela.blit(txt_rec_go, (LARGURA_TELA/2 - txt_rec_go.get_width()/2, ALTURA_TELA * 0.48))
        
        pos_x_botao = LARGURA_TELA / 2 - 100
        if desenhar_botao("TENTAR DE NOVO", pos_x_botao, ALTURA_TELA * 0.62, 200, 50, ROXO_LUNA, AZUL_ESPACIAL):
            reiniciar_jogo()
            estado_atual = JOGANDO
        if desenhar_botao("MENU", pos_x_botao, ALTURA_TELA * 0.74, 200, 50, (100,100,100), (50,50,50)):
            estado_atual = MENU

    pygame.display.flip()

pygame.quit()
sys.exit()