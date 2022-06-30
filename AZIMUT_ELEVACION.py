import turtle
import time
from math import atan2, degrees
import math
import board
import adafruit_lsm303dlh_mag
import adafruit_lsm303_accel
 
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)

screen = turtle.Screen()
screen.title("Brujula y Elevacion")
screen.setup(880,600)
screen.bgpic("image.png")

angulo_azimut=turtle.Turtle()
angulo_elevacion=turtle.Turtle()
angulo_azimut.goto(-220,0)
angulo_elevacion.goto(215,0)

      
while True:
    
    
    def vector_2_degrees(y, x):
        angle = degrees(atan2(y, x))
        if angle < 0:
            angle += 360
        return angle

    def get_heading(_sensor):
        magnet_x, magnet_y, magnet_z = _sensor.magnetic
        return vector_2_degrees(magnet_y, magnet_x)   

    azimut_1 = get_heading(sensor)


    angulo_azimut.seth(90-azimut_1)
    angulo_azimut.color("yellow")
    angulo_azimut.fd(200)
    print("Angulo de de Azimut del sensor:{:.2f}".format(azimut_1))
    
    accel_x, accel_y, accel_z = accel.acceleration
    dato1_x = accel_x
    dato2_z = accel_z
    dato3 = math.atan(dato1_x /dato2_z)
    Angulo_elevacion = dato3 * (180/math.pi)
    
    if Angulo_elevacion < 0:
        Angulo_elevacion = Angulo_elevacion + 180
    
   
    angulo_elevacion.seth(Angulo_elevacion)
    angulo_elevacion.color("green")
    angulo_elevacion.fd(200)
    
    print("Angulo de Inclinacion del sensor:{:.2f}".format(Angulo_elevacion))
        
    time.sleep(1)

    angulo_azimut.undo()
    angulo_elevacion.undo()
   
    #Impresión de datos
    #print("Acceleration (m/s^2): X=%0.3f Y=%0.3f Z=%0.3f"%accel.acceleration)
    #print("Angulo de Inclinacion:", Angulo_elevacion)
    
   
    

