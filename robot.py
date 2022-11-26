from mpu6050 import mpu6050
from L298 import L298
import math
#import PID
import time
import os.path
import pidControl


#definicion de pines de driver L293
IN1 = 26
IN2 = 19
IN3 = 27
IN4 = 17
EN1 = 22
EN2 = 13

kp = 100  #4
ki = 0 #0.08
kd = 0 #2
targetT = 0

err = 0
errI = 0
errD = 0

motor = L298(EN1,IN1,IN2,EN2,IN3,IN4)
senseLevel = mpu6050(0x68)
pid = pidControl.PID(kp, ki, kd, 1)
pid.errorLimits(-100,100)
pid.outLimits(-100,100)
#pid = PID.PID(kp, ki, kd)
#pid.SetPoint = targetT
#pid.setSampleTime(0.001)
#pid.setWindup(30)

timePrev = time.time()

def createConfig ():
    if not os.path.isfile('pid.conf'):
        with open ('pid.conf', 'w') as f:
            f.write('%s,%s,%s,%s'%(targetT,kp,ki,kd))

def readConfig ():
    global targetT
    with open ('pid.conf', 'r') as f:
        config = f.readline().split(',')
        #pid.SetPoint = float(config[0])
    targetT = (float(config[0]))
    pid.setKp (float(config[1]))
    pid.setKi (float(config[2]))
    pid.setKd (float(config[3]))

#funcion que retorna el angulo de inclinación en X y en Y así como la velocidad angular de ambos ejes
def angleCalc():
    accelerometer = senseLevel.get_accel_data()
    aX = accelerometer['x']
    aY = accelerometer['y']
    aZ = accelerometer['z']
    accel_ang_x= math.atan2(aX, math.sqrt( math.pow(aY,2)+math.pow(aZ,2) ) ) * (-180.0/math.pi)
    accel_ang_y= math.atan2(aY, math.sqrt( math.pow(aX,2)+math.pow(aZ,2) ) ) * (180.0/math.pi)
    #accel_ang_x= math.atan2(aX, aY)*-180/math.pi
    return {'degX':accel_ang_x, 'degY':accel_ang_y} 

last_deg = angleCalc()
rotation = senseLevel.get_gyro_data()
gyro_offset_x = rotation['x']
gyro_offset_y = rotation['y']
angX = last_deg['degX']
angY = last_deg['degY']
createConfig()

while(1):
    readConfig()
    #calcula el delta de tiempo
    deltaT = (time.time()-timePrev)/1000
    timePrev = time.time()

    #toma las medidas de angulos y velocidad angular
    try:
        deg = angleCalc()
        rotation = senseLevel.get_gyro_data()
    except:
        print("error")
        pass

    #rotation['x'] = rotation['x'] - gyro_offset_x
    #rotation['y'] = rotation['y'] - gyro_offset_y

    #calcula la tasa de cambio de la rotación
    gyro_x_delta = (rotation['x'] * deltaT)
    gyro_y_delta = (rotation['y'] * deltaT)

    #se aplica filtro Kalman para poder determinar el desplazamiento del giro y reducir el ruido del acelerómetro
    angX = 0.98*(angX + gyro_x_delta) + 0.02*(deg['degX']+0)

    speed = pid.compute(targetT, angX)
    #err = angX - targetT
    #errI = errI + err
    #errD = rotation['x']
    #speed = (kp*err) + (ki*errI) + (kd*errD)
    #if speed > 30:
    #    speed = 30
    #elif speed < -30:
    #    speed = -30

    print("speed: " + str(speed) + ",  angle x: " + str(angX))
    if (angX < -25.0) | (angX > 25.0):
        #motor.Stop()
        pass
    else:
        motor.move(speed, 0.0, 0.0)
    #time.sleep(0.00001)
