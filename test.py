import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class Fourmiliere:
    def __init__(self):
        self.graph = nx.Graph()
        self.salles = []
        self.salle_indices = {}  # Dictionnaire pour les indices des salles
        self.matrice_adjacence = None
    
    def ajouter_salle(self, salle):
        if salle not in self.salles:
            index = len(self.salles)
            self.salles.append(salle)
            self.salle_indices[salle] = index
            self.graph.add_node(salle)
    
    def ajouter_tunnel(self, salle1, salle2):
        self.graph.add_edge(salle1, salle2)
    
    def generer_matrice_adjacence(self):
        taille = len(self.salles)
        self.matrice_adjacence = np.zeros((taille, taille), dtype=int)
        for salle1 in self.salles:
            for salle2 in self.salles:
                if self.graph.has_edge(salle1, salle2):
                    i = self.salle_indices[salle1]
                    j = self.salle_indices[salle2]
                    self.matrice_adjacence[i][j] = 1
    
    def afficher_matrice_adjacence(self):
        if self.matrice_adjacence is None:
            self.generer_matrice_adjacence()
        print("Matrice d'adjacence :")
        print(self.matrice_adjacence)
    
    def afficher_fourmiliere(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=700, node_color="lightblue", font_size=15)
        plt.show()

class Fourmi:
    def __init__(self, id, chemin):
        self.id = id
        self.chemin = chemin
        self.position = chemin[0] if chemin else None
    
    def deplacer(self):
        if self.chemin:
            self.position = self.chemin.pop(0)

class Simulation:
    def __init__(self, fourmiliere):
        self.fourmiliere = fourmiliere
        self.fourmis = {}
        self.etapes = []
    
    def trouver_chemin(self, start, end):
        # Trouver le chemin le plus court en utilisant l'algorithme de Dijkstra
        return nx.shortest_path(self.fourmiliere.graph, source=start, target=end)
    
    def charger_fourmis(self):
        # Trouver les chemins pour toutes les fourmis depuis Sv jusqu'à Sd
        chemins = self.trouver_chemin("Sv", "Sd")
        return chemins
    
    def simuler_deplacements(self):
        chemins = self.charger_fourmis()
        for i, salle in enumerate(chemins):
            self.fourmis[f"F{i+1}"] = Fourmi(f"F{i+1}", chemins[:])
        
        # Déplacer les fourmis en respectant les contraintes
        while any(fourmi.chemin for fourmi in self.fourmis.values()):
            etape = {}
            salle_occupees = set()
            for id_fourmi, fourmi in self.fourmis.items():
                if fourmi.position and fourmi.chemin:
                    next_position = fourmi.chemin[0]
                    if next_position not in salle_occupees:
                        fourmi.deplacer()
                        salle_occupees.add(next_position)
                        etape[id_fourmi] = (fourmi.position, fourmi.chemin[0] if fourmi.chemin else None)
            if not etape:
                break
            self.etapes.append(etape)
    
    def afficher_deplacements(self):
        for index, etape in enumerate(self.etapes):
            print(f"Étape {index + 1}:")
            for id_fourmi, (position, destination) in etape.items():
                print(f"  Fourmi {id_fourmi}: {position} -> {destination}")

def visualiser_deplacements(simulation):
    fig, ax = plt.subplots()
    
    pos = nx.spring_layout(simulation.fourmiliere.graph)  # Obtenir la disposition des nœuds
    nx.draw(simulation.fourmiliere.graph, pos, with_labels=True, node_size=700, node_color="lightgreen", ax=ax)
    
    simulation.simuler_deplacements()
    
    # Visualiser les déplacements
    for index, etape in enumerate(simulation.etapes):
        ax.clear()
        nx.draw(simulation.fourmiliere.graph, pos, with_labels=True, node_size=700, node_color="lightgreen", ax=ax)
        for id_fourmi, (start, end) in etape.items():
            if start and end:
                ax.annotate("", xy=pos[end], xytext=pos[start],
                            arrowprops=dict(facecolor='red', shrink=0.05))
        plt.title(f"Étape {index + 1}")
        plt.pause(1)  # Pause pour montrer les étapes une par une

    plt.show()

def charger_fourmiliere(fichier_fourmiliere):
    fourmiliere = Fourmiliere()
    with open(fichier_fourmiliere, 'r') as file:
        lignes = file.readlines()
        for ligne in lignes:
            ligne = ligne.strip()
            if ' - ' in ligne:
                salle1, salle2 = ligne.split(' - ')
                fourmiliere.ajouter_tunnel(salle1, salle2)
            else:
                fourmiliere.ajouter_salle(ligne)
    return fourmiliere

# Exemple d'utilisation

# Charger la fourmilière à partir du fichier
fourmiliere = charger_fourmiliere("data/fourmiliere_trois.txt")

# Afficher la fourmilière
fourmiliere.afficher_fourmiliere()

# Générer et afficher la matrice d'adjacence
fourmiliere.generer_matrice_adjacence()
fourmiliere.afficher_matrice_adjacence()

# Initialiser la simulation
simulation = Simulation(fourmiliere)

# Simuler les déplacements et afficher
simulation.simuler_deplacements()
simulation.afficher_deplacements()

# Visualiser les déplacements
visualiser_deplacements(simulation)
