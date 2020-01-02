import math


# calc PWM on exponential scale start low and 
# increase rate exponentially


def calcPwm(temp):

    pwm = 0

    if temp >= 50:
        if temp >= 60:
            pwm = 100
        else:
            diff = (temp - 50) * 2
            pwm = 80 + diff

    return pwm      
    


