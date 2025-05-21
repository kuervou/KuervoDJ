# KuervoDJ 🎧🐦 — v1.1

---

![Logo KuervoDJ](./KuervoFondo.png)

**KuervoDJ** es una aplicación de escritorio construida con `Python`, `ttkbootstrap`, `pygame` y `pycaw`, que actúa como un mezclador de audio casero. Pensado originalmente como una versión extendida del mezclador de volumen de Windows, KuervoDJ permite fundir audio entre dos aplicaciones abiertas y reproducir sonidos personalizados desde una botonera.

---


![Interfaz](./V1.1.png)

## 🆕 Novedades de la versión 1.1

- 🔊 **Crossfade refinado** entre dos aplicaciones seleccionadas.
- 🎛️ **Control de volumen individual** por aplicación, con sliders verticales.
- ⌨️ **Atajos de teclado**:
  - Flechas ↑↓ controlan volumen de App A.
  - Shift + ↑↓ controlan volumen de App B.
  - Tecla ESC detiene todos los sonidos de la botonera.
- 🎹 **Botonera expandida**:
  - 22 sonidos disponibles.
  - Atajos: F1–F12 y 1–0.
  - Estilo `info-outline` para destacar con celeste elegante.
  - Sonidos se **superponen** al reproducirse (no se interrumpen entre sí).
- 🎨 **Mejoras de UI**:
  - Logo interactivo con hover animado.
  - Firma inferior con enlace y efecto.
  - Estética dark, moderna y centrada en DJs y streamers.

---

## 📂 Estructura esperada

```plaintext
KuervoDJ/
├── KuervoDJ.py
├── KuervoDJ.ico
├── KuervoDJ.png
├── KuervoDJ2.png
├── audios/
│   ├── sonido1.mp3
│   ├── sonido2.wav
│   └── ...
```

---

## 🛠️ Requisitos

- Python 3.10+
- `ttkbootstrap`
- `pygame`
- `pycaw`
- `comtypes`
- `Pillow`

Instalación rápida:

```bash
pip install ttkbootstrap pygame pycaw comtypes Pillow
```

---

## 🚀 Uso

```bash
python KuervoDJ.py
```

---

## 🌐 Autor

**KuervoDJ** fue creado por [hernancabara.com](https://hernancabara.com).  
Un viaje creativo desde una idea hasta un software funcional, profesional y con flow propio.

---

## ✨ Próximas versiones

- Controles de reproducción (⏯️ Play/Pause/Siguiente) para apps como Chrome/Spotify.
- Mejora en distribución visual responsive.
