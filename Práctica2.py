import serial # Comunicación serial con Arduino
import pandas as pd # Manejo de datos en CSV
from datetime import datetime # Marca de tiempo
import time # Pausa en la ejecución

try:
    arduino = serial.Serial('COM3', 9600, timeout=1) # Configuración del puerto serial
    time.sleep(2) # Espera para estabilizar la conexión
    datos = []
    
    print("Sistema listo. Monitoreando sensores...")
    
    while True:
        if arduino.in_waiting > 0: # Verifica si hay datos disponibles 
            linea = arduino.readline().decode('utf-8').strip()
            
            if linea and all(key in linea for key in ["RFID:", "PIR:", "US:", "LDR:"]): #Verifica que los datos de la linea son los esperados
                registro = {'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                for parte in linea.split(','): # Procesar cada parte de la linea y extraer clave-valor
                    clave, valor = parte.split(':', 1) # Separar clave y valor
                    registro[clave] = valor # Agregar al diccionario
                
                datos.append(registro) # Guarda el registro en la lista
                print("Datos:", registro) # Muestra los datos en la consola
                
                if len(datos) % 10 == 0: # Guarda datos en CSV cada 10 Registros
                    pd.DataFrame(datos).to_csv('datos_sensores.csv', index=False)

except KeyboardInterrupt:
    arduino.close() # Cierra la conexión
    pd.DataFrame(datos).to_csv('datos_sensores.csv', index=False) # Guarda los datos en CSV
    print("Datos guardados exitosamente.") # Confirma el guardado de datos
