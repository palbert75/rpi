import math


# calc PWM on exponential scale start low and 
# increase rate exponentially


def calcPwm(temp):

    pwm = 0

    if temp >= 50:
        if temp >= 60:
            pwm = 100
        else:
            y = (temp - 50) / 10
            pwm = math.pow(100, y)

    return pwm      
    


