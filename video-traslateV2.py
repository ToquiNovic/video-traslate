import subprocess
import os
import whisper
from tkinter import Tk, Label, Button, StringVar, OptionMenu, Frame
from tkinter.filedialog import askopenfilename
from moviepy.config import change_settings
from moviepy.video.tools.subtitles import file_to_subtitles, SubtitlesClip
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import imageio_ffmpeg as ffmpeg
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
from PIL import ImageTk, Image

def leer_imagen( path, size): 
        return ImageTk.PhotoImage(Image.open(path).resize(size,  Image.ADAPTIVE))  


change_settings({"IMAGEMAGICK_BINARY": "/opt/homebrew/bin/convert"})

# Actualiza la ruta de FFmpeg
os.environ["FFMPEG_BINARY"] = "/usr/local/bin/ffmpeg"

COLOR_BARRA_SUPERIOR = "#1f2329"
COLOR_MENU_LATERAL = "#2a3138"
COLOR_CUERPO_PRINCIPAL = "#f1faff"
COLOR_MENU_CURSOR_ENCIMA = "#2f88c5"


def mostrar_menu():
    # Crear ventana principal para la selección de tipo de archivo e idioma
    ventana_menu = Tk()
    ventana_menu.title('Snap Edit')
    w, h = 1024, 600        
    util_ventana.centrar_ventana(ventana_menu, w, h)   
               
    barra_superior = Frame(ventana_menu, bg=COLOR_BARRA_SUPERIOR, height=50)
    barra_superior.pack(side='top', fill='both')   
        
    menu_lateral = Frame(ventana_menu, bg=COLOR_MENU_LATERAL, width=250)
    menu_lateral.pack(side='left', fill='both', expand=False) 
        
    cuerpo_principal = Frame(ventana_menu, bg=COLOR_CUERPO_PRINCIPAL)
    cuerpo_principal.pack(side='right', fill='both', expand=True) 
    perfil = leer_imagen("udla1.png", (100, 100))
        
    # barra superiro
    labelTitulo = Label(barra_superior, text="Funciones")
    labelTitulo.config(fg="#fff", font=(
            "Roboto", 12), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
    labelTitulo.pack(side='left')
    
    # Botón del menú lateral
    buttonMenuLateral = Button(barra_superior, text="☰")
    buttonMenuLateral.pack(side='left')
    # Etiqueta de informacion
    labelTitulo = Label(barra_superior, text="tech.dev@udla.edu.co")
    labelTitulo.config(fg="#fff", font=(
            "Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
    labelTitulo.pack(side='right')
    
    # Configuración del menú lateral
    ancho_menu = 20
    alto_menu = 2
         
 # Etiqueta de perfil
    labelPerfil = Label(
    menu_lateral, image=perfil, bg=COLOR_MENU_LATERAL)
    labelPerfil.pack(side='top', pady=10)
    
    buttonDashBoard = Button(menu_lateral)        
    buttonProfile = Button(menu_lateral)        
    buttonSettings = Button(menu_lateral)
    buttonInfo = Button(menu_lateral)        

    buttons_info = [
            ("Video", "\uf109", buttonDashBoard ),
            ("Audio", "\uf007", buttonProfile),
            ("Settings", "\uf013", buttonSettings),
            ("Info", "\uf129", buttonInfo),
        ]
    for text, icon, button in buttons_info:
            configurar_boton_menu(button, text, icon, ancho_menu, alto_menu)
            
        
    # Etiqueta para el tipo de archivo
    label_tipo_archivo = Label(cuerpo_principal, text="Selecciona el tipo de archivo:")
    label_tipo_archivo.pack(side='left')

    # Variable para almacenar el tipo de archivo seleccionado
    tipo_archivo = StringVar(cuerpo_principal)
    tipo_archivo.set("Video")  # Valor predeterminado

    # Opciones para el tipo de archivo (Audio o Video)
    opciones_tipo_archivo = ["Audio", "Video"]
    menu_tipo_archivo = OptionMenu(cuerpo_principal, tipo_archivo, *opciones_tipo_archivo)
    menu_tipo_archivo.pack(side='right')

    # Etiqueta para el idioma
    label_idioma = Label(cuerpo_principal, text="Selecciona el idioma de traducción:")
    label_idioma.pack(side='bottom')

    # Variable para almacenar el idioma seleccionado
    idioma = StringVar(cuerpo_principal)
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
    menu_idioma = OptionMenu(cuerpo_principal, idioma, *dropdown_options)
    menu_idioma.pack(side='bottom')

    # Función para cerrar la ventana al hacer clic en el botón
    def obtener_tipo_archivo_idioma():
        ventana_menu.destroy()

    # Botón para confirmar la selección
    boton_seleccionar = Button(cuerpo_principal, text="Seleccionar", command=obtener_tipo_archivo_idioma)
    boton_seleccionar.pack(side='bottom')

    # Iniciar el bucle principal de la interfaz gráfica
    ventana_menu.mainloop()

    # Obtener los valores seleccionados después de cerrar la ventana
    tipo_archivo = tipo_archivo.get().lower()
    idioma = idioma.get().lower()
    return tipo_archivo, idioma

""" {icon} """
def configurar_boton_menu(button, text, icon, ancho_menu, alto_menu):
        button.config(text=f"   {text}", anchor="w", font=("Roboto", 12),
                      bd=0, bg=COLOR_MENU_LATERAL, fg="black", width=ancho_menu, height=alto_menu,
                    )
        button.pack(side='top')
        bind_hover_events(button)
        
def bind_hover_events( button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: on_enter(event, button))
        button.bind("<Leave>", lambda event: on_leave(event, button))
        
def on_enter( event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='black', font=("Roboto", 12, "bold"))

def on_leave( event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='black', font=("Roboto", 12, "bold"))

        
def abrir_panel_graficas(self):   
    limpiar_panel(self.cuerpo_principal)     
    self.FormularioGraficasDesign(self.cuerpo_principal)   
            
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