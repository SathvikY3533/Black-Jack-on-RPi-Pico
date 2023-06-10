from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import random

WIDTH = 128
HEIGHT = 64
# i2c = I2C(0, sda = Pin(0), scl = Pin(1), freq = 10000)
i2c = I2C(1, sda = Pin(10), scl = Pin(15), freq = 20000)
button = Pin(14, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(15, Pin.IN, Pin.PULL_DOWN)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

oled.fill(0)

print("I2C Address: " + hex(i2c.scan()[0]).upper())
print("I2C Configuration: " + str(i2c))

x = 8
step = 0
response = "Yes"
buttonValue = "OFF"
playerChoice = "Hit"

def startingScreen():
    global x
    oled.fill(0)
    oled.text("<< Black Jack >>", 0, 5)
    oled.text("By: Sathvik Y", 11, 16)
    oled.text("Start in " + str(x), 22, 55)
    oled.show()
    x -= 1

def wait():
    global buttonValue
    while buttonValue == "OFF":
        if button.value() or button2.value():
            buttonValue = "ON"
            value = 0
        else:
            time.sleep(.1)

def rules1():
    oled.fill(0)
    oled.text("<<<  Rule 1  >>>", 0, 5)
    oled.text("Buttons:", 0, 18)
    oled.text("Red = NO/STAY", 5, 28)
    oled.text("Green = YES/HIT", 5, 38)
    oled.text("< Press Button >", 0, 55)
    oled.show()

    
def rules2():
    oled.fill(0)
    oled.text("<<<  Rule 2  >>>", 0, 5)
    oled.text("You have to try", 2, 18)
    oled.text("to get close to", 2, 28)
    oled.text("21 but not too", 2, 38)
    oled.text("high!!", 2, 48)
    oled.show()

def rules3():
    oled.fill(0)
    oled.text("<<<  Rule 3  >>>", 0, 5)
    oled.text("If a person gets", 2, 18)
    oled.text("above 21, they", 2, 28)
    oled.text("automatically", 2, 38)
    oled.text("lose!!", 2, 48)
    oled.show()

while x > -1:
    startingScreen()
    time.sleep(1)
    
if x <= 0:
    oled.fill(0)
    playerCard1 = random.randrange(1, 21)
    computerCard1 = random.randrange(1, 21)
    playerSum = 0
    computerSum = 0
    
    rules1()
    wait()
    if buttonValue == "ON":
        step += 1
        time.sleep(.2)
        
    while step == 1:
        buttonValue = "OFF"
        rules2()
        wait()
        if buttonValue == "ON":
            step += 1
            time.sleep(.2)
    
    while step == 2:
        buttonValue = "OFF"
        rules3()
        wait()
        if buttonValue == "ON":
            step += 1
            time.sleep(.2)
        
    step = 0
    value2 = 0
    x = 3
    value = 1
    step2 = 3
    playerSum = 0
    computerSum = 0
    
    while response == "Yes":
        oled.fill(0)
        oled.text("<< Black Jack >>", 0 , 5)
        oled.text("Giving Cards...", 0, 30)
        oled.show()
        x = random.randrange(2,5)
        time.sleep(x)
        oled.fill(0)
        while value == 1:
            oled.text("<<< Computer >>>", 0, 5)
            oled.text("The Computer got", 0, 30)
            oled.text("    its card   ", 0, 40)
            oled.show()
            buttonValue = "OFF"
            wait()
            if buttonValue == "ON":
                value = 0
        oled.fill(0)
        while playerChoice == "Hit":
            oled.fill(0)
            value = 0
            playerCard = random.randrange(1,21)
            playerSum += playerCard
            computerCard = random.randrange(1,21)
            if computerSum <= 15:
                computerSum += computerCard
                
            while value == 0:
                oled.fill(0)
                oled.text("<<<  Player  >>>", 0, 5)
                oled.text("Your Card: " + str(playerCard), 13, 20)
                oled.text("Total Sum: " + str(playerSum), 13, 30)
                oled.text("-STAY- or -HIT-", 0, 50)
                oled.show()
                time.sleep(.2)
                if button.value():
                    playerChoice = "Hit"
                    oled.fill(0)
                    oled.text("<<<  Player  >>>", 0, 5)
                    oled.text("Your Card: " + str(playerCard), 13, 20)
                    oled.text("Total Sum: " + str(playerSum), 13, 30)
                    oled.text("------ or (HIT)", 0, 50)
                    oled.show()
                    value = 1
                            
                if button2.value():
                    playerChoice = "Stay"
                    oled.fill(0)
                    oled.text("<<<  Player  >>>", 0, 5)
                    oled.text("Your Card: " + str(playerCard), 13, 20)
                    oled.text("Total Sum: " + str(playerSum), 13, 30)
                    oled.text("(STAY) or -----", 0, 50)
                    oled.show()
                    value = 1
                
                if playerSum > 21 or computerSum > 21 or (playerSum > 21 and computerSum > 21):
                    value = 1
                    playerChoice = "Stay"
                    
            time.sleep(.5)
        
        print("Player Sum: " + str(playerSum) + ", Computer Sum: " + str(computerSum))
        buttonValue = "OFF"
        
        while value == 1:
            if playerChoice == "Stay":
                oled.fill(0)
                oled.text("<<<  Result  >>>", 0, 5)
                oled.text("Your Sum: " + str(playerSum), 13, 20)
                oled.text("Computer Sum: " + str(computerSum), 0, 30)
                oled.show()
                
                if playerSum > 21 and computerSum > 21:
                    print("if_1")
                    oled.fill(0)
                    while buttonValue == "OFF":
                        oled.text("<<<  Result  >>>", 0, 5)
                        oled.text("Your Sum: " + str(playerSum), 13, 20)
                        oled.text("Computer Sum: " + str(computerSum), 0, 30)
                        oled.text("It is a Tie!!!", 5, 50)
                        oled.show()
                        if button.value() or button2.value():
                            buttonValue = "ON"
                            value = 2
                
                elif playerSum > 21 and computerSum <= 21:
                    print("if_2")
                    oled.fill(0)
                    while buttonValue == "OFF":
                        oled.text("<<<  Result  >>>", 0, 5)
                        oled.text("Your Sum: " + str(playerSum), 13, 20)
                        oled.text("Computer Sum: " + str(computerSum), 0, 30)
                        oled.text("You went over 21", 0, 45)
                        oled.text(" Computer Wins! ",  0, 55)
                        oled.show()
                        if button.value() or button2.value():
                            buttonValue = "ON"
                            value = 2
                            
                elif computerSum > 21 and playerSum <= 21:
                    print("if_3")
                    oled.fill(0)
                    while buttonValue == "OFF":
                        oled.text("<<<  Result  >>>", 0, 5)
                        oled.text("Your Sum: " + str(playerSum), 13, 20)
                        oled.text("Computer Sum: " + str(computerSum), 0, 30)
                        oled.text("  You Win!!", 10, 50)
                        oled.show()
                        if button.value() or button2.value():
                            buttonValue = "ON"
                            value = 2
                
                elif (21-playerSum) == (21-computerSum):
                    print("if_4")
                    oled.fill(0)
                    while buttonValue == "OFF":
                        oled.text("<<<  Result  >>>", 0, 5)
                        oled.text("Your Sum: " + str(playerSum), 13, 20)
                        oled.text("Computer Sum: " + str(computerSum), 0, 30)
                        oled.text("Equal Sums!!", 15, 45)
                        oled.text("It is a Tie!", 5, 55)
                        oled.show()
                        if button.value() or button2.value():
                            buttonValue = "ON"
                            value = 2
                            
                elif (21-playerSum) < (21-computerSum):
                    print("if_5")
                    oled.fill(0)
                    while buttonValue == "OFF":
                        oled.text("<<<  Result  >>>", 0, 5)
                        oled.text("Your Sum: " + str(playerSum), 13, 20)
                        oled.text("Computer Sum: " + str(computerSum), 0, 30)
                        oled.text("  You Win!!", 10, 50)
                        oled.show()
                        if button.value() or button2.value():
                            buttonValue = "ON"
                            value = 2
                
                elif (21-computerSum) < (21-playerSum):
                    print("if_6")
                    oled.fill(0)
                    while buttonValue == "OFF":
                        oled.text("<<<  Result  >>>", 0, 5)
                        oled.text("Your Sum: " + str(playerSum), 13, 20)
                        oled.text("Computer Sum: " + str(computerSum), 0, 30)
                        oled.text("Computer Wins!!",  0, 50)
                        oled.show()
                        if button.value() or button2.value():
                            buttonValue = "ON"
                            value = 2
          
        while value == 2:
            oled.fill(0)
            oled.text("<<< Question >>>", 0, 5)
            oled.text("Play Again?", 20, 20)
            oled.text("-NO- or -YES-", 10, 40)
            oled.show()
            time.sleep(.2)
            if button.value():
                response = "Yes"
                oled.fill(0)
                oled.text("<<< Question >>>", 0, 5)
                oled.text("Play Again?", 20, 20)
                oled.text("---- or (YES)", 10, 40)
                oled.show()
                time.sleep(2)
                step = 0
                value2 = 0
                x = 3
                value = 1
                step2 = 3
                playerSum = 0
                computerSum = 0
                playerChoice = "Hit"
            if button2.value():
                response = "No"
                oled.fill(0)
                oled.text("<<< Question >>>", 0, 5)
                oled.text("Play Again?", 20, 20)
                oled.text("(NO) or -----", 10, 40)
                oled.show()
                time.sleep(2)
                value = 3
                

while value == 3:
    oled.fill(0)
    oled.text("<<< THE END >>>", 3, 5)
    oled.text("-- Thank You --", 3, 23)
    oled.text("- For Playing -", 3, 38)
    oled.show()
    time.sleep(1)
    value = 100000000
print("done!")
