import networkx as nx
import matplotlib.pyplot as plt

def build_graph(fichier):
    G = nx.Graph()
    with open(fichier, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]  
        
        F = int(lines[0].split('=')[1])  
        rooms = []
        tunnels = []

        for line in lines[1:]:
            if '-' in line:
                tunnels.append(line)
            else:
                rooms.append(line)

        for room in rooms:
            if '{' in room: 
                room_name, quantity = room.split('{')
                room_name = room_name.strip()
                quantity = int(quantity.strip(' }'))
                G.add_node(room_name, quantity=quantity)
            else:
                G.add_node(room)

        for tunnel in tunnels:
            room1, room2 = tunnel.split(' - ')
            G.add_edge(room1.strip(), room2.strip())

    return G, F

def draw_graph(G):
    pos = nx.spring_layout(G)  
    labels = {node: node for node in G.nodes()} 
    quantities = nx.get_node_attributes(G, 'quantity') 

    nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', font_weight='bold')
    
    capacity_labels = {node: f"Quant: {quantities[node]}" for node in quantities}
    offset_pos = {node: (x, y - 0.05) for node, (x, y) in pos.items()}  
    nx.draw_networkx_labels(G, offset_pos, labels=capacity_labels, font_color='green')

    plt.show()

G, F = build_graph('data/fourmiliere_un.txt')
draw_graph(G)