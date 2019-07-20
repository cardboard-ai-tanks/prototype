import webiopi
GPIO = webiopi.GPIO

leftMotorDrivePWM1 = 4
leftMotorDrivePWM2 = 17
rightMotorDrivePWM1 = 11
rightMotorDrivePWM2 = 9

def setup():
    webiopi.debug("setup")

    GPIO.setFunction(leftMotorDrivePWM1, GPIO.PWM)
    GPIO.setFunction(leftMotorDrivePWM2, GPIO.PWM)
    GPIO.setFunction(rightMotorDrivePWM1, GPIO.PWM)
    GPIO.setFunction(rightMotorDrivePWM2, GPIO.PWM)

@webiopi.macro
def forward():
    webiopi.debug("forward")

    GPIO.pwmWrite(leftMotorDrivePWM1, GPIO.LOW)
    GPIO.pwmWrite(leftMotorDrivePWM2, GPIO.HIGH)
    GPIO.pwmWrite(rightMotorDrivePWM1, GPIO.LOW)
    GPIO.pwmWrite(rightMotorDrivePWM2, GPIO.HIGH)

@webiopi.macro
def reverse():
    webiopi.debug("reverse")

    GPIO.pwmWrite(leftMotorDrivePWM1, GPIO.HIGH)
    GPIO.pwmWrite(leftMotorDrivePWM2, GPIO.LOW)
    GPIO.pwmWrite(rightMotorDrivePWM1, GPIO.HIGH)
    GPIO.pwmWrite(rightMotorDrivePWM2, GPIO.LOW)

@webiopi.macro
def turnLeft():
    webiopi.debug("turnLeft")

    GPIO.pwmWrite(leftMotorDrivePWM1, GPIO.LOW)
    GPIO.pwmWrite(leftMotorDrivePWM2, GPIO.HIGH)
    GPIO.pwmWrite(rightMotorDrivePWM1, GPIO.HIGH)
    GPIO.pwmWrite(rightMotorDrivePWM2, GPIO.LOW)

@webiopi.macro
def turnRight():
    webiopi.debug("turnRight")

    GPIO.pwmWrite(leftMotorDrivePWM1, GPIO.HIGH)
    GPIO.pwmWrite(leftMotorDrivePWM2, GPIO.LOW)
    GPIO.pwmWrite(rightMotorDrivePWM1, GPIO.LOW)
    GPIO.pwmWrite(rightMotorDrivePWM2, GPIO.HIGH)

@webiopi.macro
def stop():
    webiopi.debug("stop")

    GPIO.pwmWrite(leftMotorDrivePWM1, GPIO.LOW)
    GPIO.pwmWrite(leftMotorDrivePWM2, GPIO.LOW)
    GPIO.pwmWrite(rightMotorDrivePWM1, GPIO.LOW)
    GPIO.pwmWrite(rightMotorDrivePWM2, GPIO.LOW)

