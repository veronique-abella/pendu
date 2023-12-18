import pygame
import random

# Initialisation de Pygame
pygame.init()

# Définition des constantes
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Charger les mots depuis le fichier
def charger_mots():
    with open("mots.txt", "r") as file:
        mots = file.readlines()
        mots = [mot.strip().lower() for mot in mots]
    return mots

# Choisir un mot aléatoire
def choisir_mot(mots):
    return random.choice(mots)

# Initialiser l'interface Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu du Pendu")
clock = pygame.time.Clock()

# Charger les mots depuis le fichier
mots = charger_mots()

# Choisir un mot aléatoire pour commencer le jeu
mot_a_deviner = choisir_mot(mots)
lettres_deviner = ["_" for _ in range(len(mot_a_deviner))]
lettres_trouvees = []

# Liste des lettres de l'alphabet
lettres_alphabet = "abcdefghijklmnopqrstuvwxyz"

# Liste des éléments du pendu
elements_pendu = []

font = pygame.font.Font(None, 48)

# Positionnement des boutons pour les lettres
lettres_buttons = []
button_x, button_y = 50, 400
button_width, button_height = 40, 40
button_margin = 10
for lettre in lettres_alphabet:
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    lettres_buttons.append((lettre, button_rect))
    button_x += button_width + button_margin
    if button_x > WIDTH - button_width:
        button_x = 50
        button_y += button_height + button_margin

running = True
game_over = False
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key in range(97, 123):  # Vérifier si la touche enfoncée est une lettre de a à z
                lettre = chr(event.key)
                if lettre not in lettres_trouvees:
                    if lettre in mot_a_deviner:
                        lettres_trouvees.append(lettre)
                        for i, char in enumerate(mot_a_deviner):
                            if char == lettre:
                                lettres_deviner[i] = lettre
                    else:
                        # Ajouter l'élément du pendu correspondant à l'erreur
                        elements_pendu.append(len(elements_pendu) + 1)
                        lettres_trouvees.append(lettre)

    # Vérifier si le joueur a gagné
    if "_" not in lettres_deviner:
        game_over = True
        message = "Gagné !"
    # Vérifier si le joueur a perdu
    elif len(elements_pendu) == 10:
        game_over = True
        message = "Perdu ! Le mot était : " + mot_a_deviner

    # Afficher le pendu progressivement
    pendu_x, pendu_y = WIDTH - 300, 50
    for i in range(len(elements_pendu)):
        if i == 0:
            pygame.draw.line(screen, BLACK, (pendu_x, pendu_y + 120), (pendu_x + 80, pendu_y + 120), 5)  # Base du pendu
        elif i == 1:
            pygame.draw.line(screen, BLACK, (pendu_x + 40, pendu_y + 120), (pendu_x + 40, pendu_y + 20), 5)  # Poteau vertical
        elif i == 2:
            pygame.draw.line(screen, BLACK, (pendu_x + 40, pendu_y + 20), (pendu_x + 150, pendu_y + 20), 5)  # Poutre transversale
        elif i == 3:
            pygame.draw.line(screen, BLACK, (pendu_x + 150, pendu_y + 20), (pendu_x + 150, pendu_y + 40), 5)  # Corde
        elif i == 4:
            pygame.draw.circle(screen, BLACK, (pendu_x + 150, pendu_y + 70), 30, 5)  # Tête
        elif i == 5:
            pygame.draw.line(screen, BLACK, (pendu_x + 150, pendu_y + 100), (pendu_x + 150, pendu_y + 200), 5)  # Corps
        elif i == 6:
            pygame.draw.line(screen, BLACK, (pendu_x + 150, pendu_y + 120), (pendu_x + 100, pendu_y + 150), 5)  # Bras gauche
        elif i == 7:
            pygame.draw.line(screen, BLACK, (pendu_x + 150, pendu_y + 120), (pendu_x + 200, pendu_y + 150), 5)  # Bras droit
        elif i == 8:
            pygame.draw.line(screen, BLACK, (pendu_x + 150, pendu_y + 200), (pendu_x + 100, pendu_y + 250), 5)  # Jambe gauche
        elif i == 9:
            pygame.draw.line(screen, BLACK, (pendu_x + 150, pendu_y + 200), (pendu_x + 200, pendu_y + 250), 5)  # Jambe droite

    # Dessiner les boutons pour les lettres
    for lettre, button_rect in lettres_buttons:
        pygame.draw.rect(screen, BLACK, button_rect, 2)
        text = font.render(lettre, True, BLACK)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

    # Afficher le mot à deviner
    mot_text = font.render(' '.join(lettres_deviner), True, BLACK)
    mot_rect = mot_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(mot_text, mot_rect)

    # Afficher les lettres essayées
    lettres_trouvees_text = font.render('Lettres essayées: ' + ', '.join(lettres_trouvees), True, BLACK)
    lettres_trouvees_rect = lettres_trouvees_text.get_rect(midtop=(WIDTH // 2, 20))
    screen.blit(lettres_trouvees_text, lettres_trouvees_rect)

    # Afficher le message de fin de jeu
    if game_over:
        message_text = font.render(message, True, BLACK)
        message_rect = message_text.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
        screen.blit(message_text, message_rect)

    # Mettre à jour l'écran
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
