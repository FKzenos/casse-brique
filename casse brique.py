import pygame
import sys
#Mokrane glhf
# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
JAUNE_OR = (255, 199, 38)

# Paramètres du jeu
largeur_fenetre = 544
hauteur_fenetre = 600
taille_raquette = 100
hauteur_raquette = 10
taille_brique = 50
hauteur_brique = 20
balle_rayon = 10
balle_couleur = ROUGE

# Paramètres du menu principal
largeur_fenetreMenu = 544
hauteur_fenetreMenu = 600
titre = "Menu Principal"
option_font = pygame.font.SysFont(None, 50)
titre_font = pygame.font.SysFont(None, 80)
options = ["Jouer", "Quitter"]
selected_option = 0


class MenuPrincipal:
    def __init__(self):
        self.selected_option = 0

    def draw(self, fenetre):
        fenetre.fill(BLANC)
        titre_text = titre_font.render("Menu Principal", True, NOIR)
        fenetre.blit(titre_text, (largeur_fenetreMenu // 2 - titre_text.get_width() // 2, 100))
        for i, option in enumerate(options):
            text = option_font.render(option, True, NOIR if i != self.selected_option else ROUGE)
            fenetre.blit(text, (largeur_fenetreMenu // 2 - text.get_width() // 2, 300 + i * 50))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:
                    return "Jouer"
                elif self.selected_option == 1:
                    return "Quitter"
        return None

fenetreMenu = pygame.display.set_mode((largeur_fenetreMenu, hauteur_fenetreMenu))
pygame.display.set_caption(titre)

menu_principal = MenuPrincipal()
# balle
class Balle(pygame.sprite.Sprite):
    def __init__(self, x, y, rayon, couleur):
        super().__init__()
        self.image = pygame.Surface((rayon * 2, rayon * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, couleur, (rayon, rayon),rayon)
        self.rect = self.image.get_rect(center=(x,y))
        self.vitesse_x = 0
        self.vitesse_y = 5

    def update(self):
        self.rect.x += self.vitesse_x
        self.rect.y += self.vitesse_y

        if self.rect.left <= 0 or self.rect.right >= largeur_fenetre:
            self.vitesse_x = -self.vitesse_x
        if self.rect.top <= 0:
            self.vitesse_y = -self.vitesse_y

# raquette
class Raquette(pygame.sprite.Sprite):
    def __init__(self, x, y, largeur, hauteur, couleur):
        super().__init__()
        self.image = pygame.Surface((largeur, hauteur))
        self.image.fill(couleur)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, keys, largeur_fenetre):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < largeur_fenetre:
            self.rect.x += 5

class Brique(pygame.sprite.Sprite):
    def __init__(self, x, y, pv, couleur):
        super().__init__()
        self.pv = pv
        self.couleur = couleur
        self.image = pygame.Surface((taille_brique, hauteur_brique))  # Taille de la brique
        self.image.fill(self.couleur)
        self.rect = self.image.get_rect(topleft=(x, y))

class GrosseBrique(Brique):
    def __init__(self, x, y):
        super().__init__(x, y, 2, JAUNE_OR)
        self.points = 3  # Nouveau attribut

    def get_points(self):
        return self.points


# Liste de briques
briques = []

# Ajout de briques
nombre_briques_ligne = 10
nombre_lignes_briques = 4
espace_entre_briques = 5


# Classe pour le menu de pause
class MenuPause:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 36)
        self.options = ["Reprendre", "Quitter"]
        self.selected_option = 0

    def draw(self, fenetre):
        fenetre.fill(BLANC)
        titre_text = self.font.render("Pause", True, NOIR)
        description_text = self.font.render("(appuyez sur Entrée pour sélectionner)", True, BLEU)
        fenetre.blit(titre_text, (largeur_fenetre // 2 - titre_text.get_width() // 2, 200))
        fenetre.blit(description_text, (50, 400))
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, NOIR if i != self.selected_option else ROUGE)
            fenetre.blit(text, (largeur_fenetre // 2 - text.get_width() // 2, 300 + i * 50))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:
                    return "Reprendre"
                elif self.selected_option == 1:
                    return "Quitter"
        return None

menu_pause = MenuPause()
pause = False

# définit la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Casse-Brique")

# Défini la barre tout en bas de la fenêtre
loseZone = pygame.Rect(0, hauteur_fenetre - 5, largeur_fenetre, 5)



for ligne in range(nombre_lignes_briques):
    for colonne in range(nombre_briques_ligne):
        x = colonne * (taille_brique + espace_entre_briques)
        y = ligne * (hauteur_brique + espace_entre_briques)
        if ligne == 0:
            brique = GrosseBrique(x, y)
        else:
            brique = Brique(x, y, 1, VERT)
        briques.append(brique)

# Création de la balle
balle = Balle(largeur_fenetre // 2, hauteur_fenetre // 2, balle_rayon, balle_couleur)

# Création de la raquette
raquette = Raquette((largeur_fenetre - taille_raquette) // 2, hauteur_fenetre - hauteur_raquette - 2,
                        taille_raquette, hauteur_raquette, BLEU)

# Police texte
font = pygame.font.SysFont(None, 80)



#boucle principale MenuPrincipal
running = False
while not running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                menu_principal.selected_option = (menu_principal.selected_option - 1) % len(options)
            elif event.key == pygame.K_DOWN:
                menu_principal.selected_option = (menu_principal.selected_option + 1) % len(options)
            elif event.key == pygame.K_RETURN:
                if menu_principal.selected_option == 0:
                    # Commencer le jeu
                    running = True
                elif menu_principal.selected_option == 1:
                    # Quitter le jeu
                    pygame.quit()
                    sys.exit()

    # Affichage du menu principal
    menu_principal.draw(fenetreMenu)
    pygame.display.flip()
score=0
# Boucle principale du jeu
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause = not pause

    if pause:
        option = None
        while option is None:
            menu_pause.draw(fenetre)
            pygame.display.flip()
            for event in pygame.event.get():
                option = menu_pause.handle_event(event)
                if option == "Quitter":
                    pygame.quit()
                    sys.exit()
            pygame.time.Clock().tick(30)
        if option == "Reprendre":
            pause = False
            continue

        if not pause:
            menu_principal.draw(fenetreMenu)
            option = None
            for event in pygame.event.get():
                option = menu_principal.handle_event(event)
                if option:
                    break
            if option == "Jouer":
                pause = False
            elif option == "Quitter":
                pygame.quit()
                sys.exit()

    balle_temporisation = 0

    keys = pygame.key.get_pressed()

    # Mise à jour de la raquette
    raquette.update(keys, largeur_fenetre)

    # collision pour la raquette
    if balle.rect.colliderect(raquette.rect):
        # Calcul de la position de la collision par rapport à la raquette
        collision = balle.rect.centerx - raquette.rect.centerx
        proportion = collision / (raquette.rect.width / 2)

        # Ajustement de la direction de la balle en fonction de la position de collision
        balle.vitesse_y = -balle.vitesse_y
        balle.vitesse_x = 5 * proportion

    # loseEvent
    if balle.rect.colliderect(loseZone):
        pygame.draw.rect(fenetre, NOIR, (0, 0, largeur_fenetre, hauteur_fenetre))
        text = font.render("Game Over", True, ROUGE)
        fenetre.blit(text, (largeur_fenetre // 2 - text.get_width() // 2, hauteur_fenetre // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    if len(briques) == 0:
        pygame.draw.rect(fenetre, NOIR, (0, 0, largeur_fenetre, hauteur_fenetre))
        text = font.render("Victory", True, JAUNE_OR)
        fenetre.blit(text,
                     (largeur_fenetre // 2 - text.get_width() // 2, hauteur_fenetre // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    # collisions des briques
    for brique in briques[:]:
        if balle.rect.colliderect(brique.rect):
            if balle_temporisation <= 0:
                brique.pv -= 1
                score += 1
                balle.vitesse_y = -balle.vitesse_y

                if brique.pv == 0:
                    briques.remove(brique)

                balle_temporisation = 0.2 * 60
    if balle_temporisation > 0:
        balle_temporisation -= 1

    # Dessin de l'arrière-plan
    fenetre.fill(BLANC)

    # Mise à jour de la balle
    balle.update()

    # Dessin de la raquette
    fenetre.blit(raquette.image, raquette.rect)

    # Dessin de la balle
    fenetre.blit(balle.image, balle.rect)

    # Dessin de la barre tout en bas
    pygame.draw.rect(fenetre, NOIR, loseZone)

    # Dessin des briques
    for brique in briques:
         fenetre.blit(brique.image, brique.rect)

    # Affichage du score (dans la boucle principale)
    score_text = font.render("Score: " + str(score), True, NOIR)
    fenetre.blit(score_text, (0, 300))  # Positionnez le texte en haut à gauche

    # Mise à jour de l'affichage
    pygame.display.flip()

    # Limiter la vitesse de la boucle
    pygame.time.Clock().tick(60)


pygame.quit()
sys.exit()
