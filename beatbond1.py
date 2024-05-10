'''
Proyecto Final
Sistema de recomendaciones de canciones empleando grafos

Autoras: Cortés Samantha y García Arantza

Version: 2.1 (Posibles actualizaciones futuras)

Materia: Estructura de Datos y Algoritmos 
        prof: Luis Eduardo Arenas Deseano

09 de Mayo de 2024
'''

#bibliotecas empleadas
import pandas as pd #database
import networkx as nx #manejo de grafos
import customtkinter as ctk #interfaz
import tkinter as tk #interfaz
import matplotlib.pyplot as plt #visualizacion del grafo
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #canvas del grafo
from matplotlib.figure import Figure
from PIL import Image, ImageTk #manejo de las imagenes
import numpy as np #manejo de arreglos
import sys #gestion de la memoria
import time #medicion de tiempos
from pympler import asizeof #medicion de recursps

#clase de la aplicacion
class BeatBondApp:
    def __init__(self):
        # Crear una instancia de la ventana principal utilizando la clase CTk
        self.mainpage = ctk.CTk()
        # Establecer el título de la ventana principal como "BeatBond"
        self.mainpage.title("BeatBond")
        # Obtener el ancho de la pantalla del dispositivo
        self.width = self.mainpage.winfo_screenwidth()
        # Obtener la altura de la pantalla del dispositivo
        self.height = self.mainpage.winfo_screenheight()
        # Establecer la geometría de la ventana principal usando el ancho y la altura obtenidos anteriormente
        self.mainpage.geometry(f"{self.width}x{self.height}")
        # Crear un marco (frame) para contener todos los elementos de las diferentes páginas de la aplicación
        self.main_frame = ctk.CTkFrame(self.mainpage)
        # Empaquetar el marco dentro de la ventana principal y hacer que se expanda para llenar toda la ventana
        self.main_frame.pack(fill="both", expand=True)
        # Llamar a un método para crear la página principal de la aplicación
        self.create_main_page()

    def create_main_page(self):
        # Crear elementos para la página principal
        
        # Crear una etiqueta para el fondo de la página principal y empaquetarla en el marco principal
        self.mainpage_background_label = ctk.CTkLabel(self.main_frame, text=" ")
        self.mainpage_background_label.pack(fill="both", expand=True)
        
        # Cargar una imagen de fondo
        background_image = ImageTk.PhotoImage(Image.open("images/ondas.jpg"))
        
        # Crear una etiqueta de fondo y empaquetarla en el marco principal
        background_label = ctk.CTkLabel(self.mainpage_background_label, image=background_image, text="")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Crear elementos para la página principal
        
        # Crear una etiqueta para la página principal y empaquetarla en la etiqueta de fondo de la página principal
        mainpage_background_label = ctk.CTkLabel(self.mainpage_background_label, text="Main Page")
        
        # Crear un marco para los botones y colocarlo en la etiqueta de fondo de la página principal
        button_frame = ctk.CTkFrame(self.mainpage_background_label, bg_color="transparent", fg_color="transparent")
        button_frame.place(relx=0.2, rely=0.9, anchor="center")

        # Crear un botón de inicio y empaquetarlo en el marco de botones
        start_button = ctk.CTkButton(button_frame, text="Get Started", corner_radius=32, 
                                        fg_color="#7118C0", hover_color="#8A3DCF", 
                                        border_color='#7118C0', font = ('<Century Gothic>', 40, "bold"),
                                        bg_color="transparent", command=lambda: self.option_page())
        start_button.pack()

    def option_page(self):
        # Limpiar el marco principal
        self.clear_main_frame()
        
        # Crear elementos para la página de opciones
        
        # Crear una etiqueta para el fondo de la página de opciones y empaquetarla en el marco principal
        self.option_background_label = ctk.CTkLabel(self.main_frame, text=" ")
        self.option_background_label.pack(fill="both", expand=True)
        
        # Cargar una imagen de fondo
        background_image = ImageTk.PhotoImage(Image.open("images/discos.jpg"))
        
        # Crear una etiqueta de fondo y empaquetarla en el marco principal
        background_label = ctk.CTkLabel(self.option_background_label, image=background_image, text="")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Crear botones
        
        # Definir la fuente para los botones
        button_font = ("Impact", 50)
        
        # Crear un botón para explorar y empaquetarlo en el marco principal
        browse_button = ctk.CTkButton(self.main_frame, text="EXPLORAR", command=self.browse_page,
                                    corner_radius=50, fg_color="#7118C0", hover_color="#8A3DCF", 
                                    border_color='#7118C0', font=button_font, bg_color="transparent")
        browse_button.place(relx=0.4, rely=0.5, anchor="center")

        # Crear un botón para géneros y empaquetarlo en el marco principal
        genres_button = ctk.CTkButton(self.main_frame, text="GÉNEROS", command=self.genres_page,
                                    corner_radius=50, fg_color="#7118C0", hover_color="#8A3DCF", 
                                    border_color='#7118C0', font=button_font, bg_color="transparent")
        genres_button.place(relx=0.6, rely=0.5, anchor="center")

    #pagina de busqueda de la cancion
    def browse_page(self):
        # Crear una nueva ventana para explorar canciones
        self.browse_window = ctk.CTk()
        self.browse_window.title("Explorar Canciones")
        self.width = self.browse_window.winfo_screenwidth()
        self.height = self.browse_window.winfo_screenheight()
        self.browse_window.geometry(f"{self.width}x{self.height}")
        self.browse_window.config(background='#292450')
        # Crear un marco para la barra de búsqueda y empaquetarlo en la parte superior de la ventana
        search_frame = ctk.CTkFrame(self.browse_window, fg_color="#292450", bg_color="#292450")
        search_frame.pack(side=tk.TOP, fill=tk.X)
        #carga de datos
        def cargar_datos(archivo_excel):
            return pd.read_excel(archivo_excel)
        #generacion del grafo a partir de los datos generados
        def crear_grafo(datos_canciones):
            grafo = nx.Graph()

            for index, cancion in datos_canciones.iterrows():
                grafo.add_node(cancion['cancion'], genero=cancion['genero'])

                for cancion_relacionada in datos_canciones.loc[datos_canciones['cancion'] != cancion['cancion'], 'cancion']:
                    grafo.add_edge(cancion['cancion'], cancion_relacionada)

            return grafo
        #relaciones entre generos
        relaciones = [
            ('Rock', 'Metal', 0.7),
            ('Rock', 'Heavy metal', 0.6),
            ('Rock', 'Heavy metal', 0.6),
            ('Rock', 'Jazz', 0.4),
            ('Metal', 'Heavy metal', 0.3),
            ('Cumbia', 'Salsa', 0.7),
            ('Bachata', 'Boleros', 0.6),
            ('Reggaeton', 'Old Reggeton', 0.4),
            ('Jazz', 'R&B', 0.3),
            ('Electronica', 'Hiphop', 0.3),
            ('rap', 'Trap', 0.3),
            ('R&B', 'pop', 0.3),
        ]
        #cargar los datos de la base de dstos
        archivo_excel = 'beatbondDB.xlsx'
        datos_canciones = cargar_datos(archivo_excel)
        #grafo de las canciones
        grafo_canciones = crear_grafo(datos_canciones)
        #busqueda de canciones
        def buscar_canciones():
            #obtener la cancion buscada desde la barra de busqueda
            cancion_buscada = search_bar.get() 

            if not cancion_buscada:
                return
            try:
                genero_cancion_buscada = nx.get_node_attributes(grafo_canciones, 'genero')[cancion_buscada]
            except KeyError: # Mostrar mensaje de error si la canción no se encuentra
                related_results_textbox.insert(ctk.END, f"Canción '{cancion_buscada}' no encontrada.\n")
                return
            # Limpiar la lista de resultados
            related_results_textbox.delete("1.0", "end")
            # Generar las canciones del mismo género
            generator = (node for node, attr in grafo_canciones.nodes(data=True) if attr['genero'] == genero_cancion_buscada and node != cancion_buscada)
            #yield 
            for cancion in generator:
                yield cancion

        #relaciones entre las canciones y los generos
        def find_related_genres_and_songs(grafo_canciones, cancion_buscada):
            #genero de cada cancion
            genero_cancion_buscada = nx.get_node_attributes(grafo_canciones, 'genero')[cancion_buscada]

            print(f"Genre of searched song: {genero_cancion_buscada}")
            #encontrar la relacion entre los generos
            related_genres = []
            for relacion in relaciones:
                if genero_cancion_buscada in relacion:
                    related_genres.append(relacion[0 if relacion[0] != genero_cancion_buscada else 1])

            print(f"Related genres: {related_genres}")
            #encontrar la relacion entre las canciones
            related_songs = []
            for node, attr in grafo_canciones.nodes(data=True):
                if attr['genero'] in related_genres:
                    related_songs.append(node)

            print(f"Related songs: {related_songs}")

            return related_genres, related_songs
        #extraer los datos para mostrarlos en los apartados
        def buscar_mostrar():
            inicio = time.time()
            
            related_results_textbox.delete("1.0", "end")
            related_genres_textbox.delete("1.0", "end")
            related_songs_textbox.delete("1.0", "end")
            #buscar la cancion
            for cancion in buscar_canciones():
                related_results_textbox.insert(ctk.END, cancion + "\n")
            # Encontrar géneros y canciones relacionadas

            related_genres, related_songs = find_related_genres_and_songs(grafo_canciones, search_bar.get())
            # Mostrar géneros relacionados
            for genero in related_genres:
                related_genres_textbox.insert("end", f"{genero}\n")
            # Mostrar canciones relacionadas
            for cancion in related_songs:
                related_songs_textbox.insert("end", f"{cancion}\n")
            fin = time.time()
            tiempo_total = fin-inicio
            print("tiempo de ejecucion (con yields) (segundos): ", tiempo_total)
            print("memoria usada con yields: ", sys.getsizeof(buscar_canciones), "bytes")
        #searchbar
        search_bar = ctk.CTkEntry(search_frame, placeholder_text="Buscar canción...", fg_color="#FFFFFF", text_color="black", bg_color="#292450", font=('Century Gothic', 25), width=500, corner_radius=45)
        search_bar.pack(padx=5, pady=10)
        #searchbutton
        search_button = ctk.CTkButton(search_frame, text="🔍", command=buscar_mostrar, fg_color="#339966", bg_color="#292450", hover_color="#5FD198", font=('Century Gothic', 25), width=12, corner_radius=45)
        search_button.pack(pady=5)
        #generos relacionados
        related_genres_frame = ctk.CTkFrame(self.browse_window, width=500, height=100, fg_color="#844178", bg_color="#292450")
        related_genres_frame.place(relx=0.5, rely=0.15, anchor="n")

        related_genres_label = ctk.CTkLabel(related_genres_frame, text="Generos relacionados:", font=('<Century Gothic>', 30, "bold"), text_color="#FFFFFF")
        related_genres_label.pack(pady=10)

        global related_genres_textbox
        related_genres_textbox = ctk.CTkTextbox(related_genres_frame, width=480, height=90, bg_color="#844178", font=('Century Gothic', 25), fg_color="#FFFFFF", text_color="#000000")
        related_genres_textbox.pack(pady=10)
        #canciones del genero

        related_songs_frame = ctk.CTkFrame(self.browse_window, width=600, height=400, fg_color="#339966", bg_color="#292450")
        related_songs_frame.place(relx=0.3, rely=0.66, anchor="center")

        related_songs_label = ctk.CTkLabel(related_songs_frame, text="Canciones relacionadas:", font=('<Century Gothic>', 30, "bold"), text_color="#FFFFFF")
        related_songs_label.pack(pady=10)

        global related_songs_textbox
        related_songs_textbox = ctk.CTkTextbox(related_songs_frame, width=580, height=380, bg_color="#339966", font=('Century Gothic', 25), fg_color="#FFFFFF", text_color="#000000")
        related_songs_textbox.pack(pady=10)
        #canciones del genero relacioando

        related_results_frame = ctk.CTkFrame(self.browse_window, width=600, height=400, fg_color="#339966", bg_color="#292450")
        related_results_frame.place(relx=0.7, rely=0.66, anchor="center")

        related_results_label = ctk.CTkLabel(related_results_frame, text="Canciones del genero:", font=('<Century Gothic>', 30, "bold"), text_color="#FFFFFF")
        related_results_label.pack(pady=10)

        global related_results_textbox
        related_results_textbox = ctk.CTkTextbox(related_results_frame, width=580, height=380, bg_color="#339966", font=('Century Gothic', 25), fg_color="#FFFFFF", text_color="#000000")
        related_results_textbox.pack(pady=10)

        # Iniciar el bucle principal de la ventana de exploración
        self.browse_window.mainloop()


    def genres_page(self):
        # Crear una nueva ventana para la página de géneros
        self.genres_window = ctk.CTk()
        self.genres_window.title("Página de Géneros")
        self.width = self.genres_window.winfo_screenwidth()
        self.height = self.genres_window.winfo_screenheight()
        self.genres_window.geometry(f"{self.width}x{self.height}")
        self.genres_window.config(background='#292450')
        search_frame = ctk.CTkFrame(self.genres_window, fg_color="#292450", bg_color="#292450")
        search_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Leer los datos del archivo Excel
        df = pd.read_excel('beatbondDB.xlsx')
        G = nx.Graph()
        # Agregar géneros como nodos al grafo
        generos = df['genero'].unique()
        G.add_nodes_from(generos)

        # Asumiendo que queremos crear subgráficos para cada género
        for genero in generos:
            sub_nodes = [genero]  # Nodos que queremos en el subgrafo
            for _, vecino in G.edges(genero):
                sub_nodes.append(vecino)  # Agregar los vecinos del género seleccionado
            subgraph = G.subgraph(sub_nodes).copy()  # Hacer una copia del subgrafo para poder modificarlo

            # Agregar las canciones asociadas al género seleccionado al subgrafo
            for _, row in df[df['genero'] == genero].iterrows():
                cancion = row['cancion']
                subgraph.add_node(cancion)
                subgraph.add_edge(genero, cancion)
        
        # Referencia al canvas de matplotlib y a la lista de relaciones
        canvas = None
        relations_listbox = None

        # Dividir la ventana en dos frames
        frame_left = ctk.CTkFrame(self.genres_window, fg_color="#339966", bg_color="#292450", corner_radius=32)
        frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=(20, 20), pady=(20, 20))  # Añadir 20px de relleno a la izquierda, 20px de relleno a la derecha, 20px de relleno en la parte superior y 20px de relleno en la parte inferior
        related_graph_label = ctk.CTkLabel(frame_left, text="Grafo del género:", font=('<Century Gothic>', 30, "bold"), text_color="#FFFFFF")
        related_graph_label.pack(pady=10)


        frame_right = ctk.CTkFrame(self.genres_window, fg_color="#339966", bg_color="#292450",corner_radius=32)
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1, padx=(20, 20), pady=(20, 20))  # Añadir 20px de relleno a la izquierda, 20px de relleno a la derecha, 20px de relleno en la parte superior y 20px de relleno en la parte inferior
        related_music_label = ctk.CTkLabel(frame_right, text="Canciones del género:", font=('<Century Gothic>', 30, "bold"), text_color="#FFFFFF")
        related_music_label.pack(pady=10)        
        
        # Función para actualizar el grafo y la lista de relaciones
        def update_graph_and_relations(search_query):
            nonlocal canvas, relations_listbox
            
            # Limpiar el área de dibujo anterior y la lista de relaciones si existen
            if canvas:
                canvas.get_tk_widget().destroy()
            if relations_listbox:
                relations_listbox.destroy()
            
            # Filtrar las canciones por el género buscado
            canciones_genero = df[df['genero'].str.lower() == search_query.lower()]
            subgraph = nx.Graph()  # Crear un nuevo grafo vacío
            if not canciones_genero.empty:
                subgraph.add_node(search_query)  # Añadir el nodo del género al grafo
                for cancion in canciones_genero['cancion']:
                    subgraph.add_node(cancion)  # Añadir los nodos de las canciones al grafo
                    subgraph.add_edge(search_query, cancion)  # Conectar cada canción con el género
            boton_fonty = ("Century Gothic", 20)
            
            # Actualizar la lista de relaciones
            relations_listbox = ctk.CTkTextbox(frame_right, fg_color="#FFFFFF", text_color="#000000", font=boton_fonty, corner_radius=32)
            relations_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            
            
            if not canciones_genero.empty:
                relations_listbox.insert(tk.END, f"Las canciones del género '{search_query}' son: \n")
                for cancion in canciones_genero.itertuples():
                    relations_listbox.insert(tk.END, f"\n- {cancion.cancion} - {cancion.artista}\n")
            else:
                relations_listbox.insert(tk.END, f"No se encontraron canciones para el género '{search_query}' ")
            
            # Crear una figura de matplotlib para el grafo
            fig, ax = plt.subplots(figsize=(5, 4))
            # Dibujar el subgrafo del género buscado
            if not canciones_genero.empty:
                pos = nx.spring_layout(subgraph)  # Calcular la posición de los nodos
                ax.set_facecolor('#f2f2f2')  # Establecer el color de fondo a gris claro
                nx.draw(subgraph, ax=ax, pos=pos, with_labels=True, node_color='#DFA0C9', edge_color='black', node_size=1500)
                pos[search_query] = np.array([0, 0])  # Colocar el nodo del género en el centro
                nx.draw_networkx_nodes(subgraph, pos, nodelist=[search_query], node_size=1500, node_color='#C6579A')
            else:
                ax.text(0.6, 0.5, 'El genero no se ha encontrado...\n Revise que esté escrito correctamente', transform=ax.transAxes, ha='center', va='center')
            
            # Crear el canvas de matplotlib y añadirlo al frame izquierdo
            canvas = FigureCanvasTkAgg(fig, master=frame_left)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        
        # Barra de búsqueda para buscar géneros
        search_bar = ctk.CTkEntry(search_frame, placeholder_text="Buscar género...", fg_color="#FFFFFF", text_color="black", bg_color="#292450", font=('Century Gothic', 25), width=500, corner_radius=45)
        search_bar.pack(padx=5, pady=10)

        # Botón de búsqueda para actualizar el grafo y la lista de relaciones
        search_button = ctk.CTkButton(search_frame, text="🔍", command=lambda: update_graph_and_relations(search_bar.get()), fg_color="#339966", bg_color="#292450", hover_color="#5FD198", font=('Century Gothic', 25), width=12, corner_radius=45)
        search_button.pack(padx=15)
        self.genres_window.mainloop()

    def clear_main_frame(self):
        # Limpia los widgets de la mainpage
        for widget in self.main_frame.winfo_children():
            widget.destroy()

#instancia de la pagina principal
if __name__ == "__main__":
    app = BeatBondApp()
    app.mainpage.mainloop()