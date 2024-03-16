import akai_fire_library
import time
import random

akai_fire_library.clear()
akai_fire_library.drawpad(11,[120,0,0])
akai_fire_library.showLCD(["ABCDEFG","1","left","14","arial","false"])
akai_fire_library.showLCD(["HIJKLMN","2","center","14","verdana","false"])
akai_fire_library.showLCD(["OPQRSTU","3","right","14","times","false"])
akai_fire_library.showLCD(["12345678HIJKLMN12345678","4","center","14","arial","false"])
def showLCD(message):
    akai_fire_library.showLCD([message,"4","center","14","arial","false"])

while True:
    # for r in range(0,120,10):
    #     for g in range(0,120,10):
    #         for b in range(0,120,10):
    #             for c in range(16):
    #                 for r in range(4):
    #                     akai_fire_library.drawpad(c+r*16,[r,g,b])
    #                     time.sleep(0.001)    
    red = int(random.random() * 120)
    green = int(random.random() * 120)
    blue  = int(random.random() * 120)
    direction = int(random.random() * 6)
    if direction == 0:
        #left to rigit
        showLCD("left to rigit")
        for col in range(16):
            for row in range(4):
                akai_fire_library.drawpad(col + row * 16,[red,green,blue])
            time.sleep(0.05)    
    elif direction == 1:
        #rigit to left
        showLCD("rigit to left")
        for col in range(16):
            for row in range(4):
                akai_fire_library.drawpad(15 - col + row * 16,[red,green,blue])
            time.sleep(0.05)    
    elif direction == 2:
        #center to side
        showLCD("center to side")
        for col in range(8):
            for row in range(4):
                akai_fire_library.drawpad(7 - col + row * 16,[red,green,blue])
                akai_fire_library.drawpad(8 + col + row * 16,[red,green,blue])
            time.sleep(0.1)    
    elif direction == 3:
        #side to center
        showLCD("side to center")
        for col in range(8):
            for row in range(4):
                akai_fire_library.drawpad(col + row * 16,[red,green,blue])
                akai_fire_library.drawpad(15 - col + row * 16,[red,green,blue])
            time.sleep(0.1)    
    elif direction == 4:
        #top to buttom
        showLCD("top to buttom")
        for row in range(4):
            for col in range(8):
                akai_fire_library.drawpad(col + row * 16,[red,green,blue])
                akai_fire_library.drawpad(15 - col + row * 16,[red,green,blue])
            time.sleep(0.1)    
    elif direction == 5:
        #buttom to top
        showLCD("buttom to top")
        for row in range(4):
            for col in range(8):
                akai_fire_library.drawpad(col + (3-row) * 16,[red,green,blue])
                akai_fire_library.drawpad(15 - col + (3-row) * 16,[red,green,blue])
            time.sleep(0.1)    
