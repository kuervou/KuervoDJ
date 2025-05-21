
# 🎧 KuervoDJ v1.0

**KuervoDJ** es una aplicación de escritorio para Windows que permite controlar el volumen de las aplicaciones abiertas, hacer crossfades suaves entre ellas y reproducir efectos de sonido con atajos personalizados. Inspirado en el mezclador de volumen nativo de Windows, pero con *estilo, onda y control total*.

![Logo KuervoDJ](./KuervoFondo.png)

---

## 🚀 Características Principales

- 🔊 **Control de volumen por app** usando la API de audio de Windows (`pycaw`).
- 🎚️ **Crossfade entre dos aplicaciones activas** (ej: Chrome y Spotify).
- 🧠 **Fades suaves multithread** para transiciones más naturales.
- 🖱️ **Interfaz gráfica moderna** con [`ttkbootstrap`](https://ttkbootstrap.readthedocs.io/) y tema `darkly`.
- 🎵 **Botonera de sonidos** que carga dinámicamente desde la carpeta `./audios`.
- ⌨️ **Atajos de teclado** para los primeros 20 sonidos (`F1-F10`, `1-0`).
- 🖼️ **Logo animado al pasar el mouse** con link directo a [hernancabara.com](https://hernancabara.com).
- ✨ **UI con firma de autor, estilo dark elegante, sin distracciones.**

---

## 🖼️ Interfaz de Usuario

- **KuervoDJ.png**: logo principal.
- **KuervoDJ2.png**: versión con pico abierto que se activa al pasar el mouse.
- **Botonera**: muestra el nombre del archivo de audio + su atajo.
- **Footer**: indica versión y link del autor, con efecto hover.

---

## 📂 Estructura

```
KuervoDJ/
├── KuervoDJ.py
├── KuervoDJ.ico
├── KuervoDJ.png
├── KuervoDJ2.png
├── audios/
│   ├── scratch.mp3
│   ├── sirena.wav
│   └── ...
```

---

## 📦 Requisitos

- Python 3.10 o superior
- Dependencias (instalar con pip):

```bash
pip install ttkbootstrap pygame pycaw comtypes pillow
```

---

## 🛠️ Cómo ejecutar

```bash
python KuervoDJ.py
```

---

## 💡 Ideas futuras (v1.1)

- ▶️⏸️ Controles universales de **Play / Pause / Next** para apps multimedia.
- 🎛️ Panel de salidas de audio (principal/secundaria).
- 🌈 Efectos visuales en tiempo real.

---

## 🐣 Nacimiento del proyecto

> La idea original surgió de replicar el mezclador de volumen de Windows…  
> pero con personalidad.  
> Y KuervoDJ fue tomando forma.

---

## 📸 Autor

Creado con pasión por [Hernán Cabara](https://hernancabara.com)  
🖤 [@hernancabara](https://github.com/kuervou)
