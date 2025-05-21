# KuervoDJ 🎧🦉

![Logo KuervoDJ](./images/KuervoFondo.png)

**KuervoDJ** es tu mezclador de audio casero para Windows, construido en **Python** con [ttkbootstrap](https://ttkbootstrap.readthedocs.io/), `pygame` y `pycaw`. Controla volumen por aplicación, haz crossfades suaves y reproduce efectos de sonido con atajos, todo desde una interfaz dark elegante.

---

## Capturas de pantalla

![Interfaz KuervoDJ v1.1](./images/V1.1.png)  
*Interfaz principal con crossfade y botonera de sonidos*

---

## Características

- **Control de volumen por aplicación**: Usa la API de audio de Windows (`pycaw`) para ajustar individualmente cualquier app.
- **Crossfade refinado**: Fundido entre dos procesos con sliders verticales o atajos de teclado.
- **Atajos de teclado**:
  - Flechas ↑/↓: volumen App A
  - Shift + ↑/↓: volumen App B
  - ESC: detiene todos los sonidos
  - F1–F12 y 1–0: disparan hasta 22 efectos desde la botonera.
- **Botonera de sonidos dinámica**: Carga automática de todos los `.mp3`/`.wav` en `./audios`.
- **UI moderna y responsiva**: Tema darkly, logo animado al pasar el mouse y footer con firma y enlace al autor.
- **Portable & standalone**: Construible como un único `.exe` con PyInstaller (ver sección “Empaquetado”).

---

## Estructura del proyecto

```
KuervoDJ/
├── KuervoDJ.py
├── KuervoDJ.spec
├── images/
│   ├── KuervoDJ.ico
│   ├── KuervoDJ.png
│   └── KuervoDJ2.png
├── audios/
└── README.md
```

---

## Requisitos e Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/KuervoDJ.git
   cd KuervoDJ
   ```
2. Instala dependencias:
   ```bash
   pip install ttkbootstrap pygame pycaw comtypes Pillow
   ```

---

## Uso en desarrollo

```bash
python KuervoDJ.py
```

---

## Empaquetado a .exe

Para generar un único ejecutable portable (`dist/KuervoDJ.exe`):

```bash
pip install pyinstaller
pyinstaller --onefile --windowed \
  --icon "images/KuervoDJ.ico" \
  --add-data "images;images" \
  --add-data "audios;audios" \
  --hidden-import comtypes \
  --hidden-import pycaw.pycaw \
  KuervoDJ.py
```

---

## Roadmap

- Controles Play/Pause/Next para apps multimedia (Spotify, Chrome).
- Selector de salida de audio (principal/secundaria).
- Actualizaciones automáticas.
- Visualización de niveles de audio en tiempo real.

---

## Autor

**Hernán Cabara** — [hernancabara.com](https://hernancabara.com)  
Sígueme en [GitHub](https://github.com/kuervou) · [Twitter](https://twitter.com/hernancabara)
