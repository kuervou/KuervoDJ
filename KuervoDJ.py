import ttkbootstrap as ttk  # Biblioteca para UI basada en Bootstrap
from ttkbootstrap.constants import *  # Constantes de estilos y orientaciones
import tkinter as tk  # Biblioteca estándar de GUI de Python

import threading  # Para hilos (crossfade y maximización de audio)
import time  # Para retardos en fade y temporización
import sys, os # Para manejo de directorios y archivos
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume  # Control de volúmenes de aplicaciones en Windows
from comtypes import CLSCTX_ALL  # Contexto de COM requerido por pycaw
import pygame  # Biblioteca para reproducción de audio
from PIL import Image, ImageTk  # Manipulación y empleo de imágenes en Tkinter
import webbrowser  # Para abrir enlaces en el navegador

# Cuando se ejecuta bundleado con PyInstaller, 
# los archivos van a sys._MEIPASS; si no, usamos el dir del .py
if getattr(sys, "frozen", False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(__file__)


# Carpeta donde se almacenan los archivos de audio para la botonera
AUDIO_FOLDER = os.path.join(BASE_PATH, "audios")

# Inicialización del mezclador de Pygame y configuración de canales
pygame.mixer.init()
pygame.mixer.set_num_channels(32)

# Constantes para canales A y B si se desea reproducir en canales específicos
CHANNEL_A = 0
CHANNEL_B = 1


def get_audio_sessions():
    """
    Obtiene todas las sesiones de audio activas en el sistema y devuelve
    una lista de tuplas (nombre_proceso, interfaz_volumen).
    """
    sessions = AudioUtilities.GetAllSessions()
    result = []
    for s in sessions:
        if s.Process:
            name = s.Process.name()
            vol = s._ctl.QueryInterface(ISimpleAudioVolume)
            result.append((name, vol))
    return result


def fade_to(volume_interface, target, duration=0.3, steps=15):
    """
    Ajusta gradualmente el volumen de una interfaz hasta el valor target
    en duration segundos, dividido en steps pasos.
    """
    current = volume_interface.GetMasterVolume()
    delta = (target - current) / steps
    for _ in range(steps):
        current += delta
        volume_interface.SetMasterVolume(max(0.0, min(1.0, current)), None)
        time.sleep(duration / steps)


def crossfade(vol_a, vol_b, level):
    """
    Realiza un crossfade entre dos interfaces de volumen según level (0-100).
    level=0 pone todo en A, level=100 pone todo en B.
    """
    t = float(level) / 100.0
    threading.Thread(target=fade_to, args=(vol_a, 1.0 - t)).start()
    threading.Thread(target=fade_to, args=(vol_b, t)).start()


def play_audio(file_path, volume=1.0, channel=None):
    """
    Reproduce un archivo de audio usando Pygame. Si se especifica channel,
    usa ese canal, si no busca uno libre.
    """
    sound = pygame.mixer.Sound(file_path)
    sound.set_volume(volume)
    if channel is not None:
        pygame.mixer.Channel(channel).play(sound)
    else:
        pygame.mixer.find_channel().play(sound)


def stop_all_audio():
    """
    Detiene toda la reproducción de audio activa.
    """
    pygame.mixer.stop()


class CrossfadeApp:
    """
    Aplicación principal de KuervoDJ que permite:
    - Seleccionar procesos de audio del sistema (A y B)
    - Controlar volúmenes individuales y crossfade
    - Reproducir sonidos predefinidos desde una carpeta de audios
    - Mapear teclas de acceso rápido a dichos sonidos
    """

    def __init__(self, root):
        
        # Configuración básica de la ventana
        self.root = root
        self.root.title("KuervoDJ")
        ico_path = os.path.join(BASE_PATH, "images", "KuervoDJ.ico")
        self.root.iconbitmap(ico_path)
        self.root.geometry("600x850")

        # Carga inicial de sesiones de audio y extracción de nombres únicos
        self.sessions = get_audio_sessions()
        self.names = list(dict.fromkeys(name for name, _ in self.sessions))

        # Marco principal con padding
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        # Sección del logo con hover y enlace
        logo_frame = ttk.Frame(main_frame)
        logo_frame.pack()
        try:
            original = Image.open(os.path.join(BASE_PATH, "images", "KuervoDJ.png")).resize((96,96))
            hover    = Image.open(os.path.join(BASE_PATH, "images", "KuervoDJ2.png")).resize((96,96))
            self.logo_img = ImageTk.PhotoImage(original)
            self.logo_hover_img = ImageTk.PhotoImage(hover)
            self.logo_label = tk.Label(
                logo_frame,
                image=self.logo_img,
                bg="#1e1e1e",
                bd=0,
                cursor="hand2",
            )
            self.logo_label.pack(pady=(10, 5))
            # Efecto hover y click para abrir sitio web
            self.logo_label.bind("<Enter>", lambda e: self.logo_label.config(image=self.logo_hover_img))
            self.logo_label.bind("<Leave>", lambda e: self.logo_label.config(image=self.logo_img))
            self.logo_label.bind("<Button-1>", lambda e: webbrowser.open("https://hernancabara.com"))
        except:
            # Si falla la carga de imágenes, muestra solo texto
            ttk.Label(logo_frame, text="KuervoDJ", font=("Segoe UI", 20, "bold")).pack()

        # Panel de controles de crossfade
        mix_frame = ttk.LabelFrame(main_frame, text="KuervoDJ Control Panel")
        mix_frame.pack(fill=X, pady=10)

        upper_controls = ttk.Frame(mix_frame)
        upper_controls.pack(fill=X)

        # Combobox para seleccionar proceso A y B
        self.combo_a = ttk.Combobox(upper_controls, values=self.names, state="readonly")
        self.combo_a.grid(row=1, column=0, padx=10, pady=(10, 2), sticky="ew")

        self.combo_b = ttk.Combobox(upper_controls, values=self.names, state="readonly")
        self.combo_b.grid(row=1, column=1, padx=10, pady=(10, 2), sticky="ew")

        # Sliders verticales para controlar volumen individual A y B
        self.vol_slider_a = ttk.Scale(upper_controls, from_=100, to=0, orient=VERTICAL, command=self.on_slider_a)
        self.vol_slider_a.set(100)
        self.vol_slider_a.grid(row=0, column=0, padx=10, pady=(0, 2), sticky="ns")

        self.vol_slider_b = ttk.Scale(upper_controls, from_=100, to=0, orient=VERTICAL, command=self.on_slider_b)
        self.vol_slider_b.set(100)
        self.vol_slider_b.grid(row=0, column=1, padx=10, pady=(0, 2), sticky="ns")

        upper_controls.columnconfigure(0, weight=1)
        upper_controls.columnconfigure(1, weight=1)

        # Asociar teclas de flechas y Escape para control rápido
        self.root.bind_all("<Up>", self.volume_a_up)
        self.root.bind_all("<Down>", self.volume_a_down)
        self.root.bind_all("<Shift-Up>", self.volume_b_up)
        self.root.bind_all("<Shift-Down>", self.volume_b_down)
        self.root.bind_all("<Escape>", lambda e: stop_all_audio())

        # Slider horizontal de crossfade
        ttk.Label(mix_frame, text="Volumen Crossfade").pack(pady=(10, 0))
        self.slider = ttk.Scale(mix_frame, from_=0, to=100, orient=HORIZONTAL, command=self.on_slider_move)
        self.slider.pack(fill=X, pady=5)

        # Botón para refrescar lista de apps
        ttk.Button(mix_frame, text="🔄 Refrescar Apps", command=self.refresh_sessions).pack(pady=8)

        self.root.bind("<Left>", self.move_slider_left)
        self.root.bind("<Right>", self.move_slider_right)

        # Sección de botones de audio cargados desde la carpeta
        audio_frame_container = ttk.LabelFrame(main_frame, text="Botonera de Audios")
        audio_frame_container.pack(fill=BOTH, expand=True, pady=10)

        self.audio_frame = ttk.Frame(audio_frame_container)
        self.audio_frame.pack(fill=BOTH, expand=True)

        self.key_bindings = {}  # Mapea teclas a rutas de archivo
        self.load_audio_buttons()  # Genera botones según archivos en AUDIO_FOLDER
        self.bind_audio_keys()  # Asocia eventos de tecla a reproducción

        # Pie de página con información de versión y enlace al sitio
        footer = tk.Label(
            main_frame,
            text="KuervoDJ v1.1 — hernancabara.com",
            font=("Segoe UI", 8),
            fg="#888",
            bg="#212529",
            cursor="hand2",
        )
        footer.pack(pady=(10, 0))
        # Efecto hover para resaltar el enlace
        footer.bind("<Enter>", lambda e: footer.config(fg="#17a2b8", font=("Segoe UI", 8, "underline")))
        footer.bind("<Leave>", lambda e: footer.config(fg="#888", font=("Segoe UI", 8)))
        # Click en el footer abre la web
        footer.bind("<Button-1>", lambda e: webbrowser.open("https://hernancabara.com"))

    def refresh_sessions(self):
        """
        Actualiza la lista de sesiones de audio y refresca los valores
        de los comboboxes A y B con los procesos disponibles.
        """
        self.sessions = get_audio_sessions()
        self.names = list(dict.fromkeys(name for name, _ in self.sessions))
        self.combo_a['values'] = self.names
        self.combo_b['values'] = self.names

    def on_slider_move(self, val):
        """
        Maneja el slider de crossfade y ajusta simultáneamente
        el volumen de A y B según la posición (0-100).
        """
        name_a = self.combo_a.get()
        name_b = self.combo_b.get()
        if not name_a or not name_b:
            return
        vol_a = next((v for n, v in self.sessions if n == name_a), None)
        vol_b = next((v for n, v in self.sessions if n == name_b), None)
        if vol_a and vol_b:
            crossfade(vol_a, vol_b, float(val))

    def on_slider_a(self, val):
        """
        Ajusta directamente el volumen del proceso A según el slider vertical A.
        """
        name_a = self.combo_a.get()
        if not name_a:
            return
        vol = next((v for n, v in self.sessions if n == name_a), None)
        if vol:
            vol.SetMasterVolume(float(val) / 100.0, None)

    def on_slider_b(self, val):
        """
        Ajusta directamente el volumen del proceso B según el slider vertical B.
        """
        name_b = self.combo_b.get()
        if not name_b:
            return
        vol = next((v for n, v in self.sessions if n == name_b), None)
        if vol:
            vol.SetMasterVolume(float(val) / 100.0, None)

    def volume_a_up(self, event):
        """
        Incrementa el volumen de A en 5 unidades y aplica el cambio.
        Ligado a la tecla Up.
        """
        val = min(self.vol_slider_a.get() + 5, 100)
        self.vol_slider_a.set(val)
        self.on_slider_a(val)

    def volume_a_down(self, event):
        """
        Decrementa el volumen de A en 5 unidades y aplica el cambio.
        Ligado a la tecla Down.
        """
        val = max(self.vol_slider_a.get() - 5, 0)
        self.vol_slider_a.set(val)
        self.on_slider_a(val)

    def volume_b_up(self, event):
        """
        Incrementa el volumen de B en 5 unidades y aplica el cambio.
        Ligado a Shift+Up.
        """
        val = min(self.vol_slider_b.get() + 5, 100)
        self.vol_slider_b.set(val)
        self.on_slider_b(val)

    def volume_b_down(self, event):
        """
        Decrementa el volumen de B en 5 unidades y aplica el cambio.
        Ligado a Shift+Down.
        """
        val = max(self.vol_slider_b.get() - 5, 0)
        self.vol_slider_b.set(val)
        self.on_slider_b(val)

    def load_audio_buttons(self):
        """
        Lee los archivos de AUDIO_FOLDER y crea botones con accesos rápidos
        (F1-F12, 1-0) para cada sonido.
        """
        # Limpia widgets anteriores
        for widget in self.audio_frame.winfo_children():
            widget.destroy()

        # Asegura que la carpeta existe
        if not os.path.isdir(AUDIO_FOLDER):
            os.makedirs(AUDIO_FOLDER)

        # Lee archivos mp3/wav
        audio_files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith(('.mp3', '.wav'))]
        self.audio_paths = []
        self.key_bindings.clear()

        # Mapa de teclas de función y números
        key_map = [f"F{i}" for i in range(1, 13)] + list("1234567890")

        # Itera sobre los archivos de audio en la carpeta AUDIO_FOLDER
        for index, audio in enumerate(audio_files):
            full_path = os.path.join(AUDIO_FOLDER, audio)
            self.audio_paths.append(full_path)

            # Asigna atajo de teclado si está dentro del rango de key_map
            shortcut = key_map[index] if index < len(key_map) else ""
            # Etiqueta del botón, p. ej. "[F1] sonido.mp3" o "sonido.mp3"
            label = f"[{shortcut}] {audio}" if shortcut else audio

            # Crea el botón con estilo y acción asociada a reproducir y maximizar
            btn = ttk.Button(
                self.audio_frame,
                text=label,
                bootstyle="info-outline",
                command=lambda path=full_path: self.play_and_maximize(path)
            )
            # Calcula fila y columna para un layout de 3 columnas
            col = index % 3
            row = index // 3
            btn.grid(row=row, column=col, padx=10, pady=5, sticky="ew")

            # Si hay atajo, almacena la combinación de tecla y la ruta de audio
            if shortcut:
                # Para F-keys: "<F1>", para números: "<Key-1>"
                key = f"<F{shortcut[1:]}>" if shortcut.startswith("F") else f"<Key-{shortcut}>"
                self.key_bindings[key] = full_path

        # Ajusta todas las columnas para compartir espacio de forma equitativa
        for i in range(3):
            self.audio_frame.columnconfigure(i, weight=1)

    def bind_audio_keys(self):
        """
        Asocia cada atajo de teclado registrado en self.key_bindings
        al método play_and_maximize, para disparar reproducción rápida.
        """
        for key, path in self.key_bindings.items():
            self.root.bind(key, lambda event, p=path: self.play_and_maximize(p))

    def play_and_maximize(self, path):
        """
        Reproduce el audio y lanza un hilo que espera un momento
        para luego subir el volumen al máximo de la sesión Python/Pygame.
        """
        play_audio(path)
        threading.Thread(target=self.try_maximize_audio_process).start()

    def try_maximize_audio_process(self):
        """
        Tras un breve retardo, recarga sesiones de audio y,
        si identifica la sesión Python o Pygame, fija su volumen a 1.0.
        """
        time.sleep(0.5)
        sessions = get_audio_sessions()
        for name, vol in sessions:
            if "python" in name.lower() or "pygame" in name.lower():
                vol.SetMasterVolume(1.0, None)

    def move_slider_left(self, event):
        """
        Disminuye el valor del slider de crossfade en 5 unidades
        y aplica el cambio llamando a on_slider_move.
        Ligado a la tecla Izquierda.
        """
        current = self.slider.get()
        if current > 0:
            self.slider.set(current - 5)
            self.on_slider_move(current - 5)

    def move_slider_right(self, event):
        """
        Aumenta el valor del slider de crossfade en 5 unidades
        y aplica el cambio llamando a on_slider_move.
        Ligado a la tecla Derecha.
        """
        current = self.slider.get()
        if current < 100:
            self.slider.set(current + 5)
            self.on_slider_move(current + 5)

# Punto de entrada de la aplicación
if __name__ == "__main__":
    # Crea la ventana con tema 'darkly' de ttkbootstrap
    root = ttk.Window(themename="darkly")
    app = CrossfadeApp(root)
    root.mainloop()

