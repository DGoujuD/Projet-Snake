from upemtk import *
from time import sleep
from random import *

# dimensions du jeu

taille_case = 15
largeur_plateau = 60  # en nombre de cases
hauteur_plateau = 50  # en nombre de cases

def case_vers_pixel(case) :
    """
    Fonction recevant les coordonnées d'une case du plateau sous la forme
    d'un couple d'entiers (ligne, colonne) et renvoyant les coordonnées du
    pixel se trouvant au centre de cette case. Ce calcul prend en compte la
    taille de chaque case, donnée par la variable globale taille_case.
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes(pommes) :
    """
    Fonction qui permet d'afficher les pommes
    """
    x, y = case_vers_pixel(pommes)

    cercle(x, y, taille_case/2,couleur='darkred', remplissage='red')
    rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7, couleur='darkgreen', remplissage='darkgreen')

def chgt_couleur() :
    """ 
    Cette fonction génère une couleur aléatoire parmi une liste proposée 
    """
    liste_couleurs = ['green','red','yellow','blue','cyan','purple','grey','pink','black','white']
    couleur = liste_couleurs[randint(0,len(liste_couleurs)-1)]
    return couleur

def affiche_serpent(serpent,couleur) : 
    """
    Fonction qui permet d'afficher les plusieurs partie du corps
    """
    x, y = case_vers_pixel(serpent)

    cercle(x, y, taille_case/2 + 1,couleur='darkgreen', remplissage=couleur)

def change_direction1(direction, touche) :
    """
    Fonction qui permet de changer de direction avec les touches et qui grâce à la boucle principale
    de le faire en continu
    """
    if touche == 'Up' :
        return [0, -1]
    elif touche == 'Down' :
        return [0, 1]
    elif touche == 'Left' :
        return [-1, 0]
    elif touche == 'Right' :
        return [1, 0]
    else:
        return direction

def change_direction2(direction, touche) :
    """ 
    Cette fonction permet au joueur 2 de jouer avec zqsd (attention à la minuscule)
    """
    if touche == 'z' :
        # flèche z pressée
        return [0, -1]
    elif touche == 's' :
        return [0,1]
    elif touche == 'q' :
        return[-1,0]
    elif touche == 'd' :
        return[1,0]
    else :
        # pas de changement !
        return direction

def deplace_serpent(serpent, direction) :
    """ 
    Cette fonction ajoute une nouvelle tête et supprime la queue pour donner l'impression de déplacement 
    """
    serpent[0][0] += direction[0]
    serpent[0][1] += direction[1]
    new_head = [serpent[0][0],serpent[0][1]]
    serpent.pop()
    serpent.insert(0,new_head)

def agrandir_serpent(serpent) :
    """
    Cette fonction permet de créer un nouveau rond vert du serpent
    """
    serpent.append([serpent[0][0],serpent[0][1]])
    return serpent

def teleportation(serpent) :
    """ 
    Cette fonction permet de passer d'un côté du mur et de réapparaître de l'autre 
    """
    if 0 > serpent[0][0] :
        serpent[0][0] = 60
    elif serpent[0][0] > 59 :
        serpent[0][0] = 0
    elif  0  > serpent[0][1] :
        serpent[0][1] = 50
    elif serpent[0][1]> 49 :
        serpent[0][1] = 0

def fenetre(mot) :
    """ 
    cette fonction affiche à la fin le score du serpent ou le joueur qui a gagné
    """
    cree_fenetre(400, 400)
    chaine = mot
    police = "Verdana"
    taille = "30"
    texte(200, 200, chaine,police=police, taille=taille, couleur="red",ancrage='center')
    longueur, hauteur = taille_texte(chaine, police, taille)
    attend_ev()


if __name__ == "__main__" : 
    
    mod = 1
    score1 = 0
    speed = 0.60
    pommes = [randint(0,58),randint(0,48)]
    couleur1 = chgt_couleur()
    couleur2 = chgt_couleur()
    framerate = 10
    direction1 = [0, 0]
    direction2 = [0, 0]
    serpent1 = [[0,0]]
    serpent2 = [[59,49]]
    
    cree_fenetre(taille_case * largeur_plateau,taille_case * hauteur_plateau)

    print("\n-pour un joueur tapez 1 \n-pour deux joueurs tapez 2\n")
    n = int(input('nombre de joueur : '))
    while True :
        efface_tout()
        affiche_pommes(pommes)
        affiche_serpent(serpent1[0],couleur1)
        
        if n == 2 :
            affiche_serpent(serpent2[0],couleur2)

        mise_a_jour()
        
        if pommes == serpent1[0]  :
            score1 += 10
            speed -= 0.02
            couleur1 = chgt_couleur()
            if pommes in serpent1[0:] :
                pommes = [randint(0,58),randint(0,48)]
            else:
                pommes = [randint(0,58),randint(0,48)]
            serpent1 = agrandir_serpent(serpent1)
            
        if n == 2 :
            if pommes == serpent2[0]  :
                speed -= 0.02
                couleur2 = chgt_couleur()
                if pommes in serpent1[0:]:
                    pommes = [randint(0,58),randint(0,48)]
                else:
                    pommes = [randint(0,58),randint(0,48)]
                serpent2 = agrandir_serpent(serpent2)
                
        deplace_serpent(serpent1,direction1)
        if n == 2:
            deplace_serpent(serpent2,direction2)
        if mod == 1:
            teleportation(serpent1)
            if n == 2:
                teleportation(serpent2)
        
        # gestion des événements
        
        ev = donne_ev()
        ty = type_ev(ev)
        
        if ty == 'Quitte':
            break
        
        elif ty == 'Touche':
            print(touche(ev))
            direction1 = change_direction1(direction1, touche(ev))
            direction2 = change_direction2(direction2, touche(ev))
        
        if mod == 1:
            if serpent1[0] in serpent1[2:] or serpent1[0] in serpent2[0:] :
                ferme_fenetre()
                if n == 2 :
                    mot = "serpent2 gagne !!"
                    fenetre(mot)
                else :
                    mot = score1
                    fenetre(mot)
                break
            if n == 2 :
                if serpent2[0] in serpent2[2:]  or serpent2[0] in serpent1[0:]  :
                    mot = "serpent1 gagne !!"
                    fenetre(mot)
                    ferme_fenetre()
                    break
        
        sleep(speed/framerate)
ferme_fenetre()