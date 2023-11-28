import tkinter as tk
import folium
import webbrowser
import numpy as np
from sklearn.cluster import DBSCAN

def perform_clustering(coordinates, epsilon):
    kms_per_radian = 6371.0088
    epsilon = epsilon / kms_per_radian
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coordinates))
    return db.labels_

def on_button_click():
    user_input = coordinates_entry.get()
    epsilon_input = epsilon_entry.get()

    try:
        user_coordinates = np.array([list(map(float, coord.split(','))) for coord in user_input.split(';')])
        epsilon_value = float(epsilon_input)

        labels = perform_clustering(user_coordinates, epsilon_value)

        result_label.config(text=f"Resultados do Clustering:\n{labels}")

        map_clusters = folium.Map(location=[np.mean(user_coordinates[:, 0]), np.mean(user_coordinates[:, 1])], zoom_start=4)
        unique_labels = set(labels)
        for cluster_label in unique_labels:
            cluster_points = user_coordinates[labels == cluster_label]
            if cluster_label == -1:
                add_markers(map_clusters, cluster_points, 'Outlier')
            else:
                add_markers(map_clusters, cluster_points, f'Cluster {cluster_label}')

        map_clusters.save('user_cluster_map.html')
        webbrowser.open('user_cluster_map.html')
    except ValueError:
        result_label.config(text="Erro: Certifique-se de inserir coordenadas válidas e um valor numérico para o raio.")

def on_window_close():
    window.destroy()

def add_markers(map, points, label):
    for coord in points:
        folium.Marker(location=[coord[0], coord[1]], popup=label).add_to(map)

window = tk.Tk()
window.title("Clustering Form")

# Estilo
font_style = ("Arial", 12)
background_color = "#F0F0F0"

window.configure(bg=background_color)

# Widgets
coordinates_label = tk.Label(window, text="Coordenadas:", font=font_style, bg=background_color)
coordinates_label.pack(pady=10)

coordinates_entry = tk.Entry(window, font=font_style, width=30)
coordinates_entry.pack(pady=10)

epsilon_label = tk.Label(window, text="Raio de Distância (em km):", font=font_style, bg=background_color)
epsilon_label.pack(pady=10)

epsilon_entry = tk.Entry(window, font=font_style, width=10)
epsilon_entry.pack(pady=10)

button = tk.Button(window, text="Realizar Conjunto", command=on_button_click, font=font_style, bg="#4CAF50", fg="white")
button.pack(pady=10)

result_label = tk.Label(window, text="Resultados do Conjunto:", font=font_style, bg=background_color)
result_label.pack(pady=10)

window.protocol("WM_DELETE_WINDOW", on_window_close)  # funcao que serve para fechar a janela no windows 

window.geometry("400x400")
window.mainloop()