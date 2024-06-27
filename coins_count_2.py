import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk

class CoinDetectionApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Detección de Monedas")

        # Inicializa la captura de video desde la cámara web
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            return

        self.paused = False

        # Crea una etiqueta para mostrar el video de la cámara web
        self.label = tk.Label(window)
        self.label.pack()

        # Crea una etiqueta para mostrar la cantidad de monedas detectadas
        self.coin_count_label = tk.Label(window, text="Cantidad de monedas: 0", font=("Arial", 16))
        self.coin_count_label.pack(pady=10)

        # Crea botones para iniciar y pausar la detección de monedas
        self.start_button = tk.Button(window, text="Iniciar", command=self.start_detection)
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.pause_button = tk.Button(window, text="Pausar", command=self.pause_detection)
        self.pause_button.pack(side=tk.LEFT)

        # Inicia el procesamiento del frame de la cámara web
        self.process_frame()

    def process_frame(self):
        # Si no está pausado, lee un frame desde la cámara web
        if not self.paused:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame from webcam.")
                return

            # Convierte el frame de OpenCV a formato de imagen compatible con Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)

            # Detecta y cuenta las monedas en el frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blurred, 30, 150)
            contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            coin_count = sum(1 for contour in contours if cv2.minEnclosingCircle(contour)[1] > 10)

            # Dibuja contornos verdes alrededor de las monedas detectadas
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

            # Actualiza la etiqueta de la GUI con el nuevo frame
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.label.imgtk = imgtk
            self.label.config(image=imgtk)

            # Actualiza la etiqueta de la GUI con la cantidad de monedas detectadas
            self.coin_count_label.config(text=f'Cantidad de monedas: {coin_count}')

        # Programa la próxima actualización del frame después de 10 milisegundos
        self.label.after(10, self.process_frame)

    def start_detection(self):
        # Reinicia la captura de video si estaba pausado
        if self.paused:
            self.cap.release()
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Error: Could not open webcam.")
                return
            self.paused = False

    def pause_detection(self):
        # Pausa la captura de video
        self.paused = True

# Crea la ventana de la GUI
root = tk.Tk()
app = CoinDetectionApp(root)

# Ejecuta el bucle principal de la GUI
root.mainloop()
