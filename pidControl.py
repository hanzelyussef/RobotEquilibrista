
class PID:

    last_error = 0
    integrated_error = 0
    errorLowLimit = -100000
    errorHighLimit = 100000
    outLowLimit = -100000
    outHighLimit = 100000
    kp = 0.5
    ki = 0.01
    kd = 0.1
    K  = 1

    #funcion de inicialización del control PID con cada una de sus componentes
    def __init__(self, kp,ki,kd, K):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.K = K

    def errorLimits(self, lower, upper):
        self.errorLowLimit = lower
        self.errorHighLimit = upper

    def outLimits(self, lower, upper):
        self.outLowLimit = lower
        self.outHighLimit = upper

    def setKp(self, kp):
        self.kp = kp

    def setKi(self, ki):
        self.ki = ki

    def setKd(self, kd):
        self.kd = kd

    def compute(self, setpoint, feedback):
        error = feedback - setpoint
        #error = setpoint - feedback
        pTerm = self.kp * error

        self.integrated_error = self.integrated_error + error
        if self.integrated_error > self.errorHighLimit:
             self.integrated_error = self.errorHighLimit
        if self.integrated_error < self.errorLowLimit:
             self.integrated_error = self.errorLowLimit
        iTerm = self.ki * self.integrated_error

        dTerm = self.kd * (error - self.last_error)
        self.last_error = error

        speed = self.K*(pTerm + iTerm + dTerm)
        #speed = 100-speed
        if(speed>self.outHighLimit):
            speed = self.outHighLimit
        if(speed < self.outLowLimit):
            speed = self.outLowLimit
        return speed
