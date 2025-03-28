import serial
import pandas as pd
from datetime import datetime
import time

try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)
    datos = []
    
    print("Sistema listo. Monitoreando sensores...")
    
    while True:
        if arduino.in_waiting > 0:
            linea = arduino.readline().decode('utf-8').strip()
            
            if linea and all(key in linea for key in ["RFID:", "PIR:", "US:", "LDR:"]):
                registro = {'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                for parte in linea.split(','):
                    clave, valor = parte.split(':', 1)
                    registro[clave] = valor
                
                datos.append(registro)
                print("Datos:", registro)
                
                if len(datos) % 10 == 0:
                    pd.DataFrame(datos).to_csv('datos_sensores.csv', index=False)

except KeyboardInterrupt:
    arduino.close()
    pd.DataFrame(datos).to_csv('datos_sensores.csv', index=False)
    print("Datos guardados exitosamente.")
