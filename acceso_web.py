import pyautogui
import time
import webbrowser
from datetime import datetime, date
import sys
import os

# =========================
# CONFIGURACIÓN GENERAL
# =========================
pyautogui.PAUSE = 1.5
pyautogui.FAILSAFE = True

URL = "https://blocks.asw.edu.co/#/"

# Carpetas de recursos
CARPETA_AVISOS = r"C:\Users\user\Documents\Codica\Programador clases\Fixtures\avisos"
CARPETA_FIXTURES = "Fixtures"

# Carpetas para capturas
IMAGES_FOLDER = "images"
ERROR_FOLDER = os.path.join(IMAGES_FOLDER, "errors")
os.makedirs(IMAGES_FOLDER, exist_ok=True)
os.makedirs(ERROR_FOLDER, exist_ok=True)

# Abrimos log en modo append
log_file = open("programacion_clases_log.txt", "a", encoding="utf-8")

# =========================
# FUNCIONES AUXILIARES
# =========================

def escribir_log(mensaje: str) -> None:
    """Escribe un mensaje con timestamp en el log y lo imprime en consola."""
    tiempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_file.write(f"{tiempo} - {mensaje}\n")
    print(mensaje)


def cerrar_elementos_opcionales(lista_imagenes: list[str]) -> None:
    """Busca y cierra elementos opcionales en pantalla (popups, avisos)."""
    encontrados = 0
    for img in lista_imagenes:
        try:
            location = pyautogui.locateOnScreen(img, confidence=0.97)
            if location:
                pyautogui.click(pyautogui.center(location))
                escribir_log(f"[✓] Se detectó y cerró un elemento: {img}")
                time.sleep(2)
                encontrados += 1
        except Exception as e:
            escribir_log(f"[!] Error buscando imagen {img}: {e}")

    if encontrados == 0:
        escribir_log("[–] No se detectaron elementos opcionales (cerrar, omitir, etc.)")


def clic_imagen(img: str, intentos: int = 3, delay: int = 35) -> bool:
    """Intenta encontrar una imagen en pantalla y hacer clic sobre ella."""
    for intento in range(intentos):
        try:
            location = pyautogui.locateOnScreen(img, confidence=0.8)
            if location:
                pyautogui.click(pyautogui.center(location))
                escribir_log(f"[✓] Se detectó y se seleccionó: {img}")
                time.sleep(3)
                return True
            else:
                escribir_log(f"[~] Intento {intento + 1}: No se detectó la imagen {img}")
                time.sleep(delay)
        except Exception as e:
            escribir_log(f"[!] Error en intento {intento + 1} buscando {img}: {e}")
            time.sleep(1)

    escribir_log(f"[✗] No se logró detectar la imagen {img} después de {intentos} intentos.")
    return False


def obtener_posicion_imagen(imagen_path: str, confianza: float = 0.97):
    """Devuelve la posición (x,y,w,h) de la imagen si se encuentra en pantalla."""
    try:
        location = pyautogui.locateOnScreen(imagen_path, confidence=confianza)
        if location:
            escribir_log(f"[✓] Imagen detectada: {imagen_path} en {location}")
            return location
        else:
            escribir_log(f"[✗] Imagen no encontrada: {imagen_path}")
            return None
    except Exception as e:
        escribir_log(f"[!] Error buscando imagen {imagen_path}: {e}")
        return None


def programar_clase(hora: str, imagenes: list[str], screen: int) -> int:
    """Programa una clase en el horario indicado."""
    # 1. Clic en botón "Programar"
    pyautogui.click(x=371, y=129)
    escribir_log("Click en botón Programar")
    pyautogui.screenshot(os.path.join(IMAGES_FOLDER, f'{screen}_{hora}_programar.png'))
    time.sleep(25)
    cerrar_elementos_opcionales(imagenes)

    # 2. Seleccionar fecha
    if not clic_imagen(os.path.join(CARPETA_FIXTURES, 'fecha.png')):
        escribir_log("No se detectó la imagen 'fecha.png'. Cancelando ejecución.")
        sys.exit(1)

    pyautogui.screenshot(os.path.join(IMAGES_FOLDER, f'{hora}_fecha_slide.png'))

    # Selección de día según el día actual
    hoy = date.today()
    dia = hoy.isoweekday()  # lunes=1 ... domingo=7

    dias = {
        1: "martes.png",
        2: "miercoles.png",
        3: "jueves.png",
        4: "viernes.png",
        5: "lunes.png"
    }

    if not clic_imagen(os.path.join(CARPETA_FIXTURES, dias[dia])):
        escribir_log("No se detectó la imagen de día correspondiente. Cancelando ejecución.")
        sys.exit(1)

    escribir_log("Día seleccionado")
    pyautogui.screenshot(os.path.join(IMAGES_FOLDER, f'{screen}_{hora}_dia.png'))
    screen += 1
    time.sleep(5)

    # 3. Selección de hora
    ruta_imagen = os.path.join(CARPETA_FIXTURES, 'horas', f'{hora}.png')
    pos = obtener_posicion_imagen(ruta_imagen)

    if pos:
        pyautogui.click(x=(pos[0] + 364), y=pos[1])
        escribir_log(f"[✓] Hora {hora} seleccionada")
    else:
        escribir_log(f"[✗] No se encontró la hora {hora}.")
        return screen

    time.sleep(3)
    pyautogui.screenshot(os.path.join(IMAGES_FOLDER, f'{screen}_{hora}_seleccion_franja.png'))
    screen += 1

    # 4. Confirmar programación
    if clic_imagen(os.path.join(CARPETA_FIXTURES, 'programar.png')):
        escribir_log(f"Hora programada {hora}")
    else:
        escribir_log(f"[✗] No se pudo programar la hora {hora}")

    time.sleep(5)
    pyautogui.screenshot(os.path.join(IMAGES_FOLDER, f'{screen}_{hora}_confirmar_horario.png'))
    screen += 1

    return screen

# =========================
# FLUJO PRINCIPAL
# =========================

try:
    escribir_log("Iniciando automatización de programación de clases")
    numero_screen = 0

    # Simular actividad inicial
    pyautogui.moveRel(0, 1)
    time.sleep(0.1)
    pyautogui.moveRel(0, -1)
    pyautogui.press('shift')
    escribir_log("Actividad simulada para activar pantalla")

    pyautogui.moveTo(100, 100)
    escribir_log("Cursor movido para evitar FAILSAFE")

    pyautogui.screenshot(os.path.join(IMAGES_FOLDER, 'prueba_ejecucion_inicio.png'))
    escribir_log(f'{numero_screen}_Captura de pantalla inicial guardada')
    numero_screen += 1

    # Abrir navegador en la URL de ASW
    webbrowser.open(URL)
    escribir_log("Navegador abierto")
    time.sleep(10)
    pyautogui.screenshot(os.path.join(IMAGES_FOLDER, f'{numero_screen}_open.png'))
    numero_screen += 1

    # Revisar si aparece el botón de "Actualizar"
    if clic_imagen(os.path.join(CARPETA_FIXTURES, 'actualizar.png')):
        webbrowser.open(URL)
        escribir_log("Navegador abierto (después de actualizar)")
        time.sleep(10)
        pyautogui.screenshot(os.path.join(IMAGES_FOLDER, f'{numero_screen-1}.1_open.png'))

    # Cerrar posibles avisos publicitarios
    time.sleep(5)
    imagenes = [
        os.path.join(CARPETA_AVISOS, archivo)
        for archivo in os.listdir(CARPETA_AVISOS)
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    cerrar_elementos_opcionales(imagenes)
    pyautogui.screenshot(os.path.join(IMAGES_FOLDER, f'{numero_screen}_publicidad_cerrada.png'))
    numero_screen += 1

    # Programar clases en dos horarios
    numero_screen = programar_clase('10_40am', imagenes, numero_screen)
    pyautogui.click(x=219, y=138)
    numero_screen = programar_clase('12_10pm', imagenes, numero_screen)

    escribir_log("Proceso completado exitosamente")
    sys.exit(0)

except Exception as e:
    escribir_log(f"ERROR: {str(e)}")
    screenshot_name = os.path.join(ERROR_FOLDER, f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    pyautogui.screenshot(screenshot_name)
    escribir_log(f"Captura de pantalla de error guardada como {screenshot_name}")

finally:
    pyautogui.FAILSAFE = True
    log_file.close()
