import subprocess
import os
import whisper
from tkinter import Tk, Label, Button, StringVar, OptionMenu
from tkinter.filedialog import askopenfilename
from moviepy.config import change_settings
from moviepy.video.tools.subtitles import file_to_subtitles, SubtitlesClip
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import imageio_ffmpeg as ffmpeg

change_settings({"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})

os.environ["FFMPEG_BINARY"] = r"C:/ProgramData/chocolatey/bin/ffmpeg.exe"

def mostrar_menu():
    # Crear ventana principal para la selección de tipo de archivo e idioma
    ventana_menu = Tk()
    ventana_menu.title("Seleccionar tipo de archivo e idioma")

    # Etiqueta para el tipo de archivo
    label_tipo_archivo = Label(ventana_menu, text="Selecciona el tipo de archivo:")
    label_tipo_archivo.pack()

    # Variable para almacenar el tipo de archivo seleccionado
    tipo_archivo = StringVar(ventana_menu)
    tipo_archivo.set("Video")  # Valor predeterminado

    # Opciones para el tipo de archivo (Audio o Video)
    opciones_tipo_archivo = ["Audio", "Video"]
    menu_tipo_archivo = OptionMenu(ventana_menu, tipo_archivo, *opciones_tipo_archivo)
    menu_tipo_archivo.pack()

    # Etiqueta para el idioma
    label_idioma = Label(ventana_menu, text="Selecciona el idioma de traducción:")
    label_idioma.pack()

    # Variable para almacenar el idioma seleccionado
    idioma = StringVar(ventana_menu)
    idioma.set("Español") 

    # Opciones para el idioma
    dropdown_options = [
        'Español',
        'Inglés',
        'Francés',
        'Árabe',
        'Bielorruso',
        'Bosnio',
        'Catalán',
        'Alemán',
        'Griego',
        'Persa',
        'Portugués',
        'Finlandés',
        'Gallego',
        'Indonesio',
        'Islandés',
        'Italiano',
        'Japonés',
    ]

    # Menú desplegable para seleccionar el idioma
    menu_idioma = OptionMenu(ventana_menu, idioma, *dropdown_options)
    menu_idioma.pack()

    # Función para cerrar la ventana al hacer clic en el botón
    def obtener_tipo_archivo_idioma():
        ventana_menu.destroy()

    # Botón para confirmar la selección
    boton_seleccionar = Button(ventana_menu, text="Seleccionar", command=obtener_tipo_archivo_idioma)
    boton_seleccionar.pack()

    # Iniciar el bucle principal de la interfaz gráfica
    ventana_menu.mainloop()

    # Obtener los valores seleccionados después de cerrar la ventana
    tipo_archivo = tipo_archivo.get().lower()
    idioma = idioma.get().lower()
    return tipo_archivo, idioma


def seleccionar_archivo(tipo):
    # Configurar la interfaz de usuario para seleccionar un archivo
    Tk().withdraw()

    # Mostrar el cuadro de diálogo para seleccionar el archivo según el tipo especificado
    if tipo == 'audio':
        archivo = askopenfilename(initialdir="./data", title="Seleccionar archivo de audio", filetypes=(("Archivos de audio", "*.wav"), ("Todos los archivos", "*.*")))
    else:
        archivo = askopenfilename(initialdir="./data", title="Seleccionar archivo de video", filetypes=(("Archivos de video", "*.mp4;*.avi"), ("Todos los archivos", "*.*")))
    
    return archivo

def realizar_traduccion(archivo, idioma):
    print(idioma)
    print("Traduciendo...")

    # Mapeo de nombres de idiomas a códigos
    codigos_idioma = {
        'español': 'es',
        'inglés': 'en',
        'francés': 'fr',
        'árabe': 'ar',
        'bielorruso': 'be',
        'bosnio': 'bs',
        'catalán': 'ca',
        'alemán': 'de',
        'griego': 'el',
        'persa': 'fa',
        'portugués': 'pt',
        'finlandés': 'fi',
        'gallego': 'gl',
        'indonesio': 'id',
        'islandés': 'is',
        'italiano': 'it',
        'japonés': 'ja',
    }

    # Obtener el código del idioma correspondiente o usar inglés como valor predeterminado
    codigo_idioma = codigos_idioma.get(idioma, 'en')

    # Comando para la traducción utilizando el tool "whisper"
    comando = f'whisper "{archivo}" --model small --language {codigo_idioma} --output_dir "./data/translate"'

    # Ejecutar el comando en el shell
    with open(os.devnull, 'w') as null:
        result = subprocess.run(comando, shell=True, stdout=null, stderr=null)

    # Verificar si la traducción se realizó con éxito
    if result.returncode == 0:
        print("La traducción se ha completado con éxito.")
    else:
        print("Error en la traducción. Consulte los mensajes de error para obtener más información.")


def dividir_texto(texto, ancho_disponible, video_ancho):
    palabras = texto.split()
    lineas = []
    linea_actual = ""
    
    for palabra in palabras:
        if TextClip(linea_actual + " " + palabra, fontsize=video_ancho // 20).w > ancho_disponible:
            lineas.append(linea_actual)
            linea_actual = palabra
        else:
            linea_actual += " " + palabra
    
    lineas.append(linea_actual)
    return "\n".join(lineas)

def generar_subtitulos(archivo, ruta_subtitulos):
    video_original = VideoFileClip(archivo)
    video_ancho, video_alto = video_original.size 

    def generator(txt):
        return TextClip(dividir_texto(txt, video_ancho, video_ancho), font='Arial', fontsize=video_ancho // 20, color='white')

    srt_subtitles = file_to_subtitles(ruta_subtitulos)
    subtitles = SubtitlesClip(srt_subtitles, generator)

    return subtitles

def crear_video_con_subtitulos(video_original, subtitles):
    print("Creando Video...")
    try:
        # Intentar escribir el video
        video_salida = "video_con_subtitulos.mp4"
        result = CompositeVideoClip([video_original, subtitles.set_position(('center', 'bottom'))])
        result.write_videofile(video_salida, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)

        print(f"Video creado exitosamente: {video_salida}")

    except Exception as e:
        print(f"Error al escribir el video: {e}")
        
def main():
    tipo_archivo, idioma = mostrar_menu()
    archivo = seleccionar_archivo(tipo_archivo)

    realizar_traduccion(archivo, idioma)

    nombre_archivo_sin_extension = os.path.splitext(os.path.basename(archivo))[0]
    ruta_subtitulos = f"./data/translate/{nombre_archivo_sin_extension}.srt"

    video_original = VideoFileClip(archivo)
    subtitles = generar_subtitulos(archivo, ruta_subtitulos)
    
    crear_video_con_subtitulos(video_original, subtitles)

if __name__ == "__main__":
    main()