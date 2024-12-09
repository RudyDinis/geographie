import shapefile
import fltk
import random


sf = shapefile.Reader("data/departements-20180101")
sf.records()


LARGEUR_FENETRE = 1000
HAUTEUR_FENETRE = 1100

fltk.cree_fenetre(1800, HAUTEUR_FENETRE)

DOM_TOM = ('971', '972', '973', '974', '975', '976')


x_min_global, y_min_global = float('inf'), float('inf')
x_max_global, y_max_global = float('-inf'), float('-inf')

for indice, element in enumerate(sf.records()):
    if element[0] not in DOM_TOM:  
        departement = sf.shape(indice)
        bbox = departement.bbox

        x_min_global = min(x_min_global, bbox[0])
        y_min_global = min(y_min_global, bbox[1])
        x_max_global = max(x_max_global, bbox[2])
        y_max_global = max(y_max_global, bbox[3])


largeur_carte = x_max_global - x_min_global
hauteur_carte = y_max_global - y_min_global


facteur_x = LARGEUR_FENETRE / largeur_carte
facteur_y = HAUTEUR_FENETRE / hauteur_carte
facteur_echelle = min(facteur_x, facteur_y)  


offset_x = (LARGEUR_FENETRE - (largeur_carte * facteur_echelle)) / 2
offset_y = (HAUTEUR_FENETRE - (hauteur_carte * facteur_echelle)) / 2


for indice, element in enumerate(sf.records()):
    if element[0] not in DOM_TOM:  
        departement = sf.shape(indice)
        points_departement = departement.points
        parties = departement.parts  
        parties.append(len(points_departement))  

        
        for i in range(len(parties) - 1):
            tableau_final = []
            for j in range(parties[i], parties[i + 1]):
                x = (points_departement[j][0] - x_min_global) * facteur_echelle + offset_x
                y = (points_departement[j][1] - y_min_global) * facteur_echelle + offset_y
                y = HAUTEUR_FENETRE - y  
                tableau_final.append((x, y))

            
            fltk.polygone(tableau_final, couleur="black", epaisseur='1', tag=indice)


while True:
    
    ev = fltk.donne_ev()
    tev = fltk.type_ev(ev)

    if tev == "ClicGauche":
        print("Clic gauche au point", (fltk.abscisse(ev), fltk.ordonnee(ev)))

    fltk.mise_a_jour()

fltk.attend_ev()