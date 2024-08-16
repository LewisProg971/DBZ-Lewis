import pygame
from random import randint
import math as m

def lire_images():
    # Lecture des images
    images = {}

    # lecture de l'image du perso
    image = pygame.image.load("godgoku.png").convert_alpha()
    images["perso"]=image
    image = pygame.image.load("background1.jpg").convert()
    images["fond"]=image
    image = pygame.image.load("vegeta.png").convert_alpha()
    images["balle"]=image
    image = pygame.image.load("vitesse.png").convert_alpha()
    images["vitesse"]=image
    image = pygame.image.load("vie.png").convert_alpha()
    images["vie"]=image
    image = pygame.image.load("special.png").convert_alpha()
    images["special"]=image

    # Choix de la police pour le texte
    font = pygame.font.Font(None, 34)
    image = font.render('<Escape> Tu quittes MDR', True, (255, 255, 255))
    images["texte1"]=image
    images["Vie"]= None
    return images

def Musique():
        sons = {}
        son = pygame.mixer.music.load("dragonball.mp3")
        sons["dragonball"]=son
        return sons

class ElementGraphique:
    def __init__(self,image,fenetre,x=0, y=0):
        self.image=image
        self.fenetre = fenetre
        self.rect = image.get_rect()
        self.rect.x=x
        self.rect.y=y

    def afficher(self):
        self.fenetre.blit(self.image, self.rect)

    # Fonction de collision
    def collide(self, other):
        distance_x = self.rect.centerx - other.rect.centerx
        distance_y = self.rect.centery - other.rect.centery
        distance = m.sqrt(distance_x**2 + distance_y**2)
        if distance <= (self.rect.width/2 + other.rect.width/2):
            return True
        return False

class Perso(ElementGraphique):
    def __init__(self,image,fenetre,x=0, y=0):
        ElementGraphique.__init__(self,image,fenetre,x,y)
        self.vie = 3
        self.compteur = 0
        self.invulnerable = False

    def appliquer_degats(self):
        if perso.invulnerable is False:
            self.vie -=1

# Methode deplacer pour le personnage
    def move_perso(self, touches):

        if touches[pygame.K_LEFT]:
            self.rect.x-=5
        if touches[pygame.K_RIGHT]:
            self.rect.x+=5
        if touches[pygame.K_DOWN]:
            self.rect.y+=5
        if touches[pygame.K_UP] :
            self.rect.y-=5

# Gestion des bords pour le perso
        if perso.rect.x < 0:
            self.rect.x =0
        if perso.rect.y < 0:
            self.rect.y = 0
        if perso.rect.right > 1000:
            self.rect.right = 1000
        if perso.rect.bottom > 650:
            self.rect.bottom = 650

class Balle(ElementGraphique):
    def __init__(self, image, fenetre, x=randint(25,455), y=randint(25,455)):
        ElementGraphique.__init__(self,image ,fenetre,x,y)
        self.dx = 3
        self.dy = 4

#Methode deplacer de la balle
    def move_balle(self,balle):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Gestion du rebonds pour la balle
        if balle.rect.top < 0 or balle.rect.bottom > 650:
            self.dy = -self.dy
        if balle.rect.left < 0 or balle.rect.right > 1000:
            self.dx = -self.dx

class Bonus(ElementGraphique):
    def __init__(self, image, fenetre, x=randint(25,455), y=0, type=1):
        super().__init__(image, fenetre, x, y)
        self.dy = 4
        self.compteur = 0
        self.rapide = False
        self.type = type
    
    #Fonction de deplacement des bonus
    def deplacer(self, bonus):
        bonus.rect.y +=self.dy
    
     #Fonction de l'effet du bonus de vie
    def effets(self, bonus):
        if perso.collide(bonus) and bonus.type ==1:
            perso.vie +=1
            listeBonus.remove(bonus)

    #Fonction de l'effet du bonus de vitesse
    def effets2(self, bonus):
        if self.rapide is True and self.compteur<=150:
            perso.dx = 10
            perso.dy = 10
            self.compteur+=1
        if self.compteur>150:
            self.rapide = False
            self.compteur = 0
        if self.rapide is False:
            perso.dx = 6
            perso.dy = 6
    
    #Fonction du Malus de points de vie
    def effets3(self, bonusS):
        if perso.collide(bonusS):
                perso.vie = perso.vie - 3
                listeBonusS.remove(bonusS)

# Initialisation de la bibliotheque pygame
pygame.init()

#creation de la fenetre
largeur = 1000
hauteur = 650
fenetre=pygame.display.set_mode((largeur,hauteur))
pygame.display.set_caption("Jeu DragonBall")

images = lire_images()

sons = Musique()
pygame.mixer.music.play()

perso = Perso(images["perso"],fenetre,x=60,y=80)

# lecture de l'image du fond
fond = ElementGraphique(images["fond"],fenetre)

bonus2 = Bonus(images["vitesse"],fenetre,x=randint(5,455),y=0)

listeBonus = []

listeBonusv = []

listeBonusS = []

#création de la liste de balles
listeBalles = []

#Creation premiere balle
balle = Balle(images["balle"],fenetre,x=randint(40,455),y=randint(40,455))
listeBalles.append(balle)

#Creation deuxieme balle
balle2 = Balle(images["balle"],fenetre,x=randint(40,455),y=randint(40,455))
listeBalles.append(balle2)
balle2.dx = 6
balle2.dy = 3

#Creation troisieme balle
balle3 = Balle(images["balle"],fenetre,x=randint(40,455),y=randint(40,455))
listeBalles.append(balle3)
balle3.dx = 9
balle3.dy = 2

texte1 = ElementGraphique(images["texte1"],fenetre,x=10,y=10)
# servira a regler l'horloge du jeu
horloge = pygame.time.Clock()

# la boucle dont on veut sortir :
#   - en appuyant sur ESCAPE
#   - en cliquant sur le bouton de fermeture
i=1;
continuer=True
while continuer == True:

    #affichage de la vie du personnage
    images["Vie"] = pygame.font.Font(None,34).render("Vies : "+str(int(perso.vie)),True,(255,255,255))
    vie = ElementGraphique(images["Vie"],fenetre,x=10,y=50)

    # fixons le nombre max de frames / secondes
    horloge.tick(30)

    i=i+1

    # on recupere l'etat du clavier
    touches = pygame.key.get_pressed();

    #appel de la fonction pour deplacer le personnage
    perso.move_perso(touches)

    # si la touche ESC est enfoncee, on sortira
    # au debut du prochain tour de boucle
    if touches[pygame.K_ESCAPE] :
        continuer=False

    # Affichage du fond
    fond.afficher()

    # Affichage Perso
    perso.afficher()

    balle.afficher()

    # Apparition première balle
    if i >= 30:
        listeBalles[0].afficher()
        listeBalles[0].move_balle(listeBalles[0])

    #Apparition deuxième balle
    if i >= 60:
        listeBalles[1].afficher()
        listeBalles[1].move_balle(listeBalles[1])

    #Apparition troisième balle
    if i >= 90:
        listeBalles[2].afficher()
        listeBalles[2].move_balle(listeBalles[2])

    #Condition de passage à l'invulnerabilite
    if perso.collide(listeBalles[0]) or perso.collide(listeBalles[1]) or perso.collide(listeBalles[2]):
        perso.appliquer_degats()
        perso.invulnerable = True
    if perso.invulnerable is True:
        if (touches[pygame.K_LEFT] or touches[pygame.K_RIGHT] or touches[pygame.K_UP] or touches[pygame.K_DOWN]):
            perso.compteur +=1
    
    #Condition d'annulation de l'invulnerabilite 
    if perso.compteur >= 30:
        perso.compteur = 0
        perso.invulnerable = False

    #Condition d'arret du jeux
    if perso.vie <= 0:
        continuer = False

    #Ajout du bonus de vie
    if len(listeBonus)<2 and randint(1,1000)<=2:
        listeBonus.append(Bonus(images["vie"],fenetre,x=randint(20,455),y=0))

    #Afficher et faire disparaitre le bonus de vie
    for bon in listeBonus:
        bon.deplacer(bon)
        if bon.rect.top >= 480 :
            listeBonus.remove(bon)
        else:
            bon.afficher()
        bon.effets(bon)
    
    #ajout du bonus special
    if len(listeBonusS)<2 and randint(1,1000)<=2:
        listeBonusS.append(Bonus(images["special"],fenetre,x=randint(20,455),y=0))

    for bonusS in listeBonusS:
        bonusS.effets3(bonusS)

    #Afficher et faire disparaitre le bonus de special
    for bon in listeBonusS:
        bon.deplacer(bon)
        if bon.rect.top >= 650 :
            listeBonusS.remove(bon)
        else:
            bon.afficher()
        bon.effets3(bon)

    #Ajout du bonus de vitesse
    if len(listeBonusv)<1 and randint(1,1000)<=3 and bonus2.rapide is False:
        listeBonusv.append(bonus2)

    #Afficher et faire disparaitre le bonus de vitesse
    for bon in listeBonusv:
        bon.deplacer(bon)
        if bon.rect.top >= 650 :
            listeBonusv.remove(bon)
        else:
            bon.afficher()
        if perso.collide(bon):
            listeBonusv.remove(bon)
    
    if perso.collide(bonus2):
        bonus2.rapide = True
    bonus2.effets2(bonus2)
    
    """print(bonus2.compteur)"""
    print(perso.vie)
    
    # Affichage du Texte
    texte1.afficher()
    vie.afficher()
    
    # rafraichissement
    pygame.display.flip()

    # Si on a clique sur le bouton de fermeture on sortira
    # au debut du prochain tour de boucle
    # Pour cela, on parcours la liste des evenements
    # et on cherche un QUIT...
    for event in pygame.event.get():   # parcours de la liste des evenements recus
        if event.type == pygame.QUIT:     #Si un de ces evenements est de type QUIT
            continuer = False	   # On arrete la boucle

# fin du programme principal...
pygame.quit()