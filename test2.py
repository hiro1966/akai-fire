import akai_fire_library

if __name__ == '__main__':
    akai_fire_library.clear()
    akai_fire_library.drawpad(0,[127,0,0])
    akai_fire_library.drawpad(1,[0,127,0])
    akai_fire_library.drawpad(2,[0,0,127])
    akai_fire_library.drawextra(12,"green")
    while True:
        a = akai_fire_library.callback()
        print("b")
        print( akai_fire_library.message)
        if akai_fire_library.message[2] == "pad":
            if akai_fire_library.message[0] == 32:
                akai_fire_library.drawpad(akai_fire_library.message[1],[127,127,127])
            else:
                akai_fire_library.drawpad(akai_fire_library.message[1],[0,0,0])
        else:
            print(akai_fire_library.message)