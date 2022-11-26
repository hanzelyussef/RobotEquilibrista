
import RPi.GPIO as GPIO

class L298:
    #funcion de inicialización del driver L293
    def __init__(self,EN1,IN1,IN2,EN2,IN3,IN4):
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BCM)
        self.IN1 = IN1
        self.IN2 = IN2
        self.IN3 = IN3
        self.IN4 = IN4
        self.EN1 = EN1
        self.EN2 = EN2
        self.GPIO.setup(self.IN1, GPIO.OUT)
        self.GPIO.setup(self.IN2, GPIO.OUT)
        self.GPIO.setup(self.IN3, GPIO.OUT)
        self.GPIO.setup(self.IN4, GPIO.OUT)
        self.GPIO.setup(self.EN1, GPIO.OUT)
        self.GPIO.setup(self.EN2, GPIO.OUT)
        self.PWM1 = GPIO.PWM(self.EN1,100)
        self.PWM1.start(0)
        self.PWM2 = GPIO.PWM(self.EN2,100)
        self.PWM2.start(0)

    #función para actualizar el PWM de los motores y el sentido de giro de cada uno (Driver L298)
    def move(self, speed, left_delta, right_delta):
        left_speed = speed + left_delta
        right_speed = speed + right_delta

        #Motor izquierdo
        if left_speed > 0:
            #print("Adelante: " + str(speed))
            if left_speed > 100:
                left_speed = 100
            self.PWM1.ChangeDutyCycle(speed)
            self.GPIO.output(self.IN1,True)
            self.GPIO.output(self.IN2, False)

        if left_speed < 0:
            #print("Atras: " + str(speed))
            if left_speed < 100:
                left_speed = -100
            self.PWM1.ChangeDutyCycle(-speed)
            self.GPIO.output(self.IN1, False)
            self.GPIO.output(self.IN2, True)

        #Motor Derecho
        if right_speed > 0:
            if right_speed > 100:
                right_speed = 100
            self.PWM2.ChangeDutyCycle(speed)
            self.GPIO.output(self.IN3, True)
            self.GPIO.output(self.IN4, False)

        if right_speed < 0:
            if right_speed < 100:
                right_speed = -100
            self.PWM2.ChangeDutyCycle(-speed)
            self.GPIO.output(self.IN3, False)
            self.GPIO.output(self.IN4, True)
    
    #Funciones de control básico con DT al 100%
    def Front(self):
        self.PWM1.ChangeDutyCycle(30)
        self.PWM2.ChangeDutyCycle(30)
        self.GPIO.output(self.IN1, True)
        self.GPIO.output(self.IN2, False)
        self.GPIO.output(self.IN3, True)
        self.GPIO.output(self.IN4, False)

    def Back(self):
        self.PWM1.ChangeDutyCycle(30)
        self.PWM2.ChangeDutyCycle(30)
        self.GPIO.output(self.IN1, False)
        self.GPIO.output(self.IN2, True)
        self.GPIO.output(self.IN3, False)
        self.GPIO.output(self.IN4, True)

    def Stop(self):
        self.PWM1.ChangeDutyCycle(0)
        self.PWM2.ChangeDutyCycle(0)
        self.GPIO.output(self.IN1, False)
        self.GPIO.output(self.IN2, False)
        self.GPIO.output(self.IN3, False)
        self.GPIO.output(self.IN4, False)

    def QuickStop(self):
        self.PWM1.ChangeDutyCycle(100)
        self.PWM2.ChangeDutyCycle(100)
        self.GPIO.output(self.IN1, True)
        self.GPIO.output(self.IN2, True)
        self.GPIO.output(self.IN3, True)
        self.GPIO.output(self.IN4, True)
