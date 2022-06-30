import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time

import ISS_Info
from datetime import datetime
import ephem
from psycopg2 import Timestamp 

import math
from math import atan2, degrees


while True:
        
     #POSICION_ACUTAL
    posicion = ISS_Info.iss_current_loc()
    location = ISS_Info.iss_current_loc()
    lat = location['iss_position']['latitude']
    lon = location['iss_position']['longitude']
    
    #EL TIEMPO QUE ESTARA PASANDO EL SATELITE
    pasos = ISS_Info.iss_passes(14.5833, -90.5167, 200, 1)
    pass_list=[]
    for count,item in enumerate(pasos["response"], start=0):
        pass_list.append(pasos['response'][count]['duration'])
        tiempo_de_paso = pass_list[count]
        #print(tiempo_de_paso)
    #LA HORA EN QUE PASARA EL SATELITE
    pass_list1=[]
    for count,item in enumerate(pasos["response"], start=0):
        pass_list1.append(pasos['response'][count]['risetime'])
        hora_de_paso = pass_list1[count]
        hora_de_paso_1 = datetime.fromtimestamp(hora_de_paso)
        #print("hora que pasara el satelite:", hora_de_paso_1)
    
    #HORA ACTUAL
    now = datetime.now()
    tiempo_actual = datetime.timestamp(now)
    #print("hora actual", now)
    #print("hora en timestamp =", tiempo_actual)

    #VARIABLES PARA EL CONTEO DEL TIEMPO QUE ESTARA PASANDO EL SATELITE
    t = 0
    azimut_inicial = 0
    elevacion_inicial = 0
    
    if hora_de_paso <= tiempo_actual <=  hora_de_paso + 20:
        
        while t<tiempo_de_paso/10:
 
            t = t + 1
    
            degrees_per_radian = 180.0 / math.pi
            home = ephem.Observer()
            home.lon = '-90.5167'   # +E
            home.lat = '14.5833'    # +N
            home.elevation = 1489 # meters

            iss = ephem.readtle('ISS',
                '1 25544U 98067A   22174.84926581  .00005844  00000-0  11089-3 0  9992',
                '2 25544  51.6436 303.5894 0004138 295.0107 201.1713 15.49841222346218'
            )

            home.date = datetime.utcnow()
            iss.compute(home)
            Elevacion = '%4.0f' % (iss.alt * degrees_per_radian)
            Azimut =  '%5.0f' % (iss.az * degrees_per_radian)
            Azimut_stepper = int(Azimut)
            Azimut_stepper_calculo = Azimut_stepper * 3200//360
            Elevacion_stepper = int(Elevacion)
            Elevacion_stepper_calculo = Elevacion_stepper * 3200//360
            
            print("------------------------------")
            print('ANGULO DE ELEVACION:', Elevacion)
            print("------------------------------")
            print('AZIMUT:', Azimut)
            print("------------------------------")
        
            
            azimut_movimiento = Azimut_stepper_calculo - azimut_inicial
            elevacion_movimiento = Elevacion_stepper_calculo - elevacion_inicial

            if azimut_movimiento >= 0  :
                    
                #Movimiento del azimut ingresado
                direction= 22 # Direction (DIR) GPIO Pin
                step = 23 # Step GPIO Pin
                EN_pin = 24 # enable pin (LOW to enable)

                mymotortest = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "DRV8825")
                GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output


                GPIO.output(EN_pin,GPIO.LOW) 
                mymotortest.motor_go(False, "1/16" , azimut_movimiento , .0005, False, .05)
                
                azimut_inicial = Azimut_stepper_calculo
                
                GPIO.cleanup()
                
            elif azimut_movimiento <= 0 :
                
                azimut_movimiento = azimut_movimiento * -1
                
                #Movimiento del azimut ingresado
                direction= 22 # Direction (DIR) GPIO Pin
                step = 23 # Step GPIO Pin
                EN_pin = 24 # enable pin (LOW to enable)

                mymotortest = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "DRV8825")
                GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output


                GPIO.output(EN_pin,GPIO.LOW) 
                mymotortest.motor_go(True, "1/16" , azimut_movimiento , .0005, False, .05)
                
                azimut_inicial = Azimut_stepper_calculo

                GPIO.cleanup()
            
            if elevacion_movimiento >= 0  :
        
                #Movimiento del azimut ingresado
                direction= 16 # Direction (DIR) GPIO Pin
                step = 20 # Step GPIO Pin
                EN_pin = 26 # enable pin (LOW to enable)

                mymotortest = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "DRV8825")
                GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output


                GPIO.output(EN_pin,GPIO.LOW) 
                mymotortest.motor_go(True, "1/16" , elevacion_movimiento , .0005, False, .05)
                
                elevacion_inicial = Elevacion_stepper_calculo
                
                GPIO.cleanup()
                
                time.sleep(10)

            elif elevacion_movimiento <= 0 :

                elevacion_movimiento = elevacion_movimiento * -1
                
                #Movimiento del azimut ingresado
                direction= 16 # Direction (DIR) GPIO Pin
                step = 20 # Step GPIO Pin
                EN_pin = 26 # enable pin (LOW to enable)

                mymotortest = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "DRV8825")
                GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output


                GPIO.output(EN_pin,GPIO.LOW) 
                mymotortest.motor_go(False, "1/16" , elevacion_movimiento , .0005, False, .05)
                
                elevacion_inicial = Elevacion_stepper_calculo
                 
                GPIO.cleanup()
                 
                time.sleep(10)
        else:
            
            print("Ultimo angulo de azimut:", Azimut_stepper_calculo)
            print("Ultimo angulo de elevacion:", Elevacion_stepper_calculo)
            
            if Elevacion_stepper_calculo <= 0:
                Elevacion_stepper_calculo = Elevacion_stepper_calculo * -1
                
                direction= 22 # Direction (DIR) GPIO Pin
                step = 23 # Step GPIO Pin
                EN_pin = 24 # enable pin (LOW to enable)

                mymotortest = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "DRV8825")
                GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output

                GPIO.output(EN_pin,GPIO.LOW) 
                mymotortest.motor_go(True, "1/16" , Azimut_stepper_calculo , .0005, False, .05)

                GPIO.cleanup()

                #Movimiento del azimut ingresado
                direction= 16 # Direction (DIR) GPIO Pin
                step = 20 # Step GPIO Pin
                EN_pin = 26 # enable pin (LOW to enable)

                mymotortest = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "DRV8825")
                GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output
                
                GPIO.output(EN_pin,GPIO.LOW) 
                mymotortest.motor_go(True, "1/16" , Elevacion_stepper_calculo , .0005, False, .05)
                
                GPIO.cleanup()
                
            elif Elevacion_stepper_calculo > 0:
                
                direction= 22 # Direction (DIR) GPIO Pin
                step = 23 # Step GPIO Pin
                EN_pin = 24 # enable pin (LOW to enable)

                mymotortest = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "DRV8825")
                GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output

                GPIO.output(EN_pin,GPIO.LOW) 
                mymotortest.motor_go(True, "1/16" , Azimut_stepper_calculo , .0005, False, .05)

                GPIO.cleanup()

                #Movimiento del azimut ingresado
                direction= 16 # Direction (DIR) GPIO Pin
                step = 20 # Step GPIO Pin
                EN_pin = 26 # enable pin (LOW to enable)

                mymotortest = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "DRV8825")
                GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output
                
                GPIO.output(EN_pin,GPIO.LOW) 
                mymotortest.motor_go(True, "1/16" , Elevacion_stepper_calculo , .0005, False, .05)
                
                GPIO.cleanup()
                
            
                time.sleep(5)
                          
               
    elif tiempo_actual  <  hora_de_paso:
        print("------------------------------")
        print("ESPERE EL PASO DEL SATELITE")
        print("------------------------------")
        print("HORA QUE PASARA EL SATELITE:", hora_de_paso_1)
        print("------------------------------")
        print("HORA ACTUAL:", now)
        print("------------------------------")
        print("HORA QUE PASARA EL SATELITE EN TS:", hora_de_paso)
        print("------------------------------")
        print("HORA ACTUAL EN TS:", tiempo_actual)
        print("------------------------------")
        print("TIEMPO QUE ESTARA PASANDO EL SATELITE:" , tiempo_de_paso ,"SEGUNDOS")
        print("------------------------------")
        print("LATITUD",lat)
        print("------------------------------")
        print("LONGITUD", lon)
        print("------------------------------")
        print("++++++++++++++++++++++++++++++")
        
        time.sleep(10.0)
    
        
    elif tiempo_actual  > hora_de_paso + tiempo_de_paso:
        print("------------------------------")
        print("ESPERE EL PASO DEL SATELITE")
        print("------------------------------")
        print("HORA QUE PASARA EL SATELITE:", hora_de_paso_1)
        print("------------------------------")
        print("HORA ACTUAL:", now)
        print("------------------------------")
        print("HORA QUE PASARA EL SATELITE EN TS:", hora_de_paso)
        print("------------------------------")
        print("HORA ACTUAL EN TS:", tiempo_actual)
        print("------------------------------")
        print("TIEMPO QUE ESTARA PASANDO EL SATELITE:" , tiempo_de_paso ,"SEGUNDOS")
        print("------------------------------")
        print("LATITUD",lat)
        print("------------------------------")
        print("LONGITUD", lon)
        print("------------------------------")
       
        time.sleep(10.0)  
    







