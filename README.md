# Automatización de Programación de Clases

Este proyecto automatiza la programación de clases en el sitio [American School Way](https://blocks.asw.edu.co/#/) usando Python y **PyAutoGUI**.

---

## 🖥 Descripción

El script `acceso_web.py` realiza las siguientes tareas:

- Abre el navegador y accede al sitio web.
- Cierra popups y avisos publicitarios automáticamente.
- Selecciona la fecha y el día correspondiente.
- Programa clases en los horarios configurados.
- Genera capturas de pantalla de cada paso del flujo.
- Registra logs detallados en `programacion_clases_log.txt`.

---

## 🔧 Tecnologías y herramientas

- Python 3.x
- PyAutoGUI
- SQLite / PostgreSQL (para proyectos futuros)
- Linux / Windows (WSL recomendado)

---

📁 Estructura del proyecto

Programador-clases/
├── acceso_web.py           # Script principal
├── Fixtures/               # Imágenes y recursos
│   ├── avisos/
│   ├── horas/
│   └── ...
├── images/                 # Capturas de pantalla
│   ├── errors/             # Capturas de errores
│   └── ...
├── programacion_clases_log.txt
└── README.md

---

## ⚙️ Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/JacJaram/Programador-clases.git
cd Programador-clases

python3 -m venv venv
source venv/bin/activate

pip install pyautogui
sudo apt install scrot python3-tk python3-dev -y   # Para Linux/WSL

🚀 Uso

Dentro del entorno virtual:

python acceso_web.py


Las capturas de pantalla se guardan en images/.

Los errores se guardan en images/errors/.

El log se actualiza en programacion_clases_log.txt.
