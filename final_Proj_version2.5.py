#Gabriel Quiroz 100840010
#MPRO Lab 5D
from machine import Pin, PWM, ADC, I2C
import sh1106
import utime
import time

pot1 = ADC(Pin(28)) #(GPIO pins) - potentiomiter position

pot2 = ADC(Pin(26)) #(GPIO pins) - potentiomiter position

i2c = I2C(0,scl=Pin(1), sda=Pin(0), freq=400000) #WAS 5, 4 RESPECTULLY
display = sh1106.SH1106_I2C(128, 64, i2c)
display.sleep(False)
display.flip(1)
#OUTPUT

servo = PWM(Pin(16)) #(GPIO pins) Servo Analog Input

mFWD = PWM(Pin(5)) #(GPIO pins) Servo Analog Input

mREV = PWM(Pin(13)) #(GPIO pins) Servo Analog Input

button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
##mFWD = PWM(Pin(0, Pin.OUT)) #(GPIO pins) Servo Analog Input

##mREV = PWM(Pin(1, Pin.OUT)) #(GPIO pins) Servo Analog Input

#led_red = machine.Pin(0, machine.Pin.OUT)

#led_green = machine.Pin(1, machine.Pin.OUT)

servo.freq(50)
mFWD.freq(1000)
mREV.freq(1000)
#Pot = ADC(0)              # Pot at channel 0
#Out = Pin(2, Pin.OUT)     # Output at GP2

#ch = PWM(Pin(0))          # Set ch to PWM using GP2
#ch.freq(1000)              # Set Frequency = 1000Hz

#ch2 = PWM(Pin(1))          # Set ch to PWM using GP2
#ch2.freq(1000)              # Set Frequency = 1000Hz

#while True:                # Do forever
    #duty = Pot.read_u16()  # Copy pot Raw value to duty
    #ch.duty_u16(duty)      # Change duty cycle, range 0-6553

# .duty_16(#) TAKES VALUES OF 0 TO 65535 FOR DUTY CYCLE OF 0 TO 100
# The sG90 has 2 % duty cycle for 0 degrees, 12.5 % for 180 degrees

# a .duty_u16 value of about 1350 is zero degrees, 8200 is 180 degrees
# and for (1350 + (pot.read_u16()/9.57)) scales 0 to 65535 to 1350 to 8200 (the zero & span values)- obtained by value 9.57 = 65535/(8200 - 1350)

#last_state = False
#current_state=False


while True:
    display.fill(0)
    display.text("Welcome to the HMS MPRO")  #character size default = 8x8 pixels
    display.text("Check speed")   #second line in this case starts as row 12 (pixel from top)
    display.show()
    time.sleep(0.75)
    #current_state = button.value()
    value1 = int(1350 + (pot1.read_u16()/9.57)) #add's tje required offset to raw value of pot
    servo.duty_u16(value1) # the final value needed a bit of tweaking (all servo's vary)
    value2 = int(pot2.read_u16())
    utime.sleep(0.02)
    #current_state = button.value()
    logic_state = button.value()
    logic_state2 = button2.value()
    percentage = (value2/65535)*100
    ##if last_state == 0 and current_state == 1:
    if logic_state == True:
        mFWD.duty_u16(value2)
        mREV.duty_u16(0)
        print("----------------------------------------------------------------") 
        print("You are going Forward","\nspeed",percentage,"%    ", "\npotentiometer at", value2)
        print("----------------------------------------------------------------") 
       # mFWD.toggle()
        #utime.sleep(0.2)
        #last_state = current_state
        #led_green.value(1)
        #led_red.value(0)
        #duty = pot2.read_u16()  # Copy pot Raw value to duty
        #ch.duty_u16(duty)      # Change duty cycle, range 0-6553
    #elif last_state == 0 and current_state == 1:
    elif logic_state == False:
        mREV.duty_u16(value2)
        mFWD.duty_u16(0)
        if percentage < 30:
            print("----------------------------------------------------------------") 
            print("You are in reverse and in range ", percentage,"%    ",  "\npotentiometer at", value2)
            print("----------------------------------------------------------------")           #value2 = 1966.05
        if percentage > 30:
            print("----------------------------------------------------------------")
            print("For your safety you canot go over 30% in reverse ", "\nspeed", percentage,"%"  ,"\nFixed PWM 16bit output 19876"  "\npotentiometer at", value2)
            print("----------------------------------------------------------------")           #value2 = 1966.05
            mREV.duty_u16(19876)
            time.sleep(0.5)
            if percentage < 30:
                mREV.duty_u16(value2)
            if logic_state2 == False:
                print("Original brightness without limit, wach the Red LED")
                mREV.duty_u16(value2)
                time.sleep(3)
   # elif logic_state2== False:
               #mREV.duty_u16(value2)
               #print("on")
        #mFWD.duty_u16(0)
            #time.sleep(2)
        #mREV.toggle()
        #utime.sleep(0.2)
       # last_state = current_state
       # led_green.value(0)
       # led_red.value(1)
       # duty = pot2.read_u16()  # Copy pot Raw value to duty
        #ch2.duty_u16(duty)      # Change duty cycle, range 0-6553
    
# Various things that can be displayed - recommend one at a time.

    # print(f'Mark time = {round(Mark,1)}')
    # print(f'Space time = {round(Space,1)}')
    #print(f'Duty Cycle time = {round(duty,1)}')
    # print(f'Frequency (kHz)= {round(freqkHz,1)}')
    
    #print("You have exceeded 30%")
    #time.sleep(2)
    
    #LOG
    #added button to demo original light and to limit PWM with duty cycle
    #_____
    #currently can control server motor
    #can control LED with button
    #lacking memory with button to keep RED on when pressed and green off and vice versa
    #issue with motor. Wires detached. Still not sure how to control speed and direction
    #resolved project clarification. no motor needed. motor needs at least 5V
    #stuck on latch for button. how to have it retain memore in software. Thinking of doing it through a counter.