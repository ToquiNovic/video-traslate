import speech_recognition as sr
from googletrans import Translator
import threading

# Crear un objeto de reconocimiento de voz
r = sr.Recognizer()

# Configurar el dispositivo de entrada de audio
mic = sr.Microphone()

# Crear un objeto de traductor
translator = Translator()

def reconocer():
    # Iniciar la captura de audio en tiempo real
    with mic as source:
        # Ajustar el nivel de ruido de fondo para una mejor captura de audio
        r.adjust_for_ambient_noise(source)

        # Leer el audio del micrófono en tiempo real
        print("Comenzando la captura de audio...")
        while True:
            try:
                audio = r.listen(source, timeout=0.2)  # Tiempo de espera

                # Utilizar el reconocimiento de voz para convertir el audio en texto
                text = r.recognize_google(audio, language="es-ES")
                print("Texto reconocido (español):", text)

                # Traducir el texto al inglés
                translation = translator.translate(text, src='es', dest='en')
                print("Translated text (English):", translation.text)
            except sr.UnknownValueError:
                print("No se pudo reconocer el audio")
            except sr.RequestError as e:
                print("Error al realizar la solicitud al servicio de reconocimiento de voz:", str(e))
            except sr.WaitTimeoutError:
                print("Tiempo de espera agotado. No se detectó habla.")

# Crear un hilo para la función de reconocimiento
speech_thread = threading.Thread(target=reconocer)
speech_thread.start()
