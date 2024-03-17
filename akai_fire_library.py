#Based on https://github.com/Vykonn/akaifire.py

#rtmidi is not use rtmidi pakeage
# please use python-rtmidi
from rtmidi import (API_LINUX_ALSA, API_MACOSX_CORE, API_RTMIDI_DUMMY,
                    API_UNIX_JACK, API_WINDOWS_MM, MidiIn, MidiOut,
                    get_compiled_api)
from rtmidi.midiutil import open_midioutput, open_midiinput
import time
import fire_lcd
global message
message = [0, 0, 0]
global stop
global lightupon
global colorid
global oncircle
global eventwhile
global waittime
waittime = 0.01
eventwhile = True
colorid = "00"
oncircle = []
stop = True
lightupon = False
all_processes = []
##def main():
class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        global message
        global eventwhile
        messagee, deltatime = event
        eventwhile = False
        self._wallclock += deltatime
        if messagee[1] in range(54,118): 
            message[0] = messagee[2]
            message[1] = (messagee[1]-54)
            message[2] = "pad"
        else:
            if messagee[1] == 118: #SELECT
                if messagee[2] == 127: message[0] = "left"
                if messagee[2] == 1: message[0] = "right"
                message[2] = "SEELCT"
            elif messagee[1] == 25: #SELECT
                if messagee[2] == 127: message[0] = "on"
                if messagee[2] == 0: message[0] = "off"
                message[2] = "SEELCT"
            elif messagee[1] not in range(16,20): #buttons
                if messagee[0] == 144: message[0] = "on"
                if messagee[0] == 128: message[0] = "off"
                message[2] = "extra"
                firstindex = 43
                for i in reversed(range(43,53)):
                    firstindex = firstindex + 1
                    if firstindex == messagee[1]: message[1] = i - 42
                if messagee[1] == 39: message[1] = 11
                if messagee[1] == 38: message[1] = 12
                if messagee[1] == 37: message[1] = 13
                if messagee[1] == 36: message[1] = 14
                if messagee[1] == 26: message[1] = 29
                if messagee[1] in range(31,36): message[1] = messagee[1] - 7
            else:   #knobs
                if messagee[0] == 144: message[0] = "on"
                if messagee[0] == 128: message[0] = "off"
                if messagee[0] == 176:
                    if messagee[2] == 1: message[0] = "right"
                    if messagee[2] == 127: message[0] = "left"
                message[2] = "knobs"
                message[1] = messagee[1] - 15

apis = {
    API_MACOSX_CORE: "macOS (OS X) CoreMIDI",
    API_LINUX_ALSA: "Linux ALSA",
    API_UNIX_JACK: "Jack Client",
    API_WINDOWS_MM: "Windows MultiMedia",
    API_RTMIDI_DUMMY: "RtMidi Dummy"
}

available_apis = get_compiled_api()
inmain =None
outmain =None
for api, api_name in sorted(apis.items()):
    print(api_name)
    if api in available_apis:
        print("AAA")
        for name, class_ in (("input", MidiIn), ("output", MidiOut)):
            try:
                midi = class_(api)
                ports = midi.get_ports()
            except Exception as exc:
                print("Could not probe MIDI %s ports: %s" % (name, exc))
                continue

            if not ports:
                print("No MIDI %s ports found." % name)
            else:
                port_type = name
                for port, name in enumerate(ports):
                    print(name,port)
                    #if name == "FL STUDIO FIRE %s" % port:
                    if name.startswith('FL STUDIO FIRE'):
                        print("Fire!!")
                        if port_type == "output":
                            outmain = port
                        if port_type == "input":
                            inmain = port
            del midi
if not inmain is None:
    midiin, port_name = open_midiinput(inmain)
    midiin.set_callback(MidiInputHandler(port_name))   
if not outmain is None:
    midiout, port_name = open_midioutput(outmain)
def sethz(hz):
    '''
    Sets the frequency to scan for MIDI inputs.
    The value is in hertz, default is 100 hz.
    '''
    global waittime
    waittime = 1/hz
def drawpad(pad, color):
    """Draws a color on the corresponding pad.

    Parameters:
        pad (int): Position of lighting, left-to-right, top-to-bottom. 0-63.
        color (list): [R, G, B] values.
    """ 
    if len('{0:x}'.format(color[0])) == 1: r = ("0"+'{0:x}'.format(color[0]))
    else: r = ('{0:x}'.format(color[0]))
    if len('{0:x}'.format(color[1])) == 1: g = ("0"+'{0:x}'.format(color[1]))
    else: g = ('{0:x}'.format(color[1]))
    if len('{0:x}'.format(color[2])) == 1: b = ("0"+'{0:x}'.format(color[2]))
    else: b = ('{0:x}'.format(color[2]))
    if len('{0:x}'.format(pad)) == 1: padf = ("0"+'{0:x}'.format(pad))
    else: padf = ('{0:x}'.format(pad))
    data = bytearray.fromhex("F0 47 7F 43 65 00 04 {} {} {} {} F7".format(padf, r, g, b))
    midiout.send_message(data)
def clear(p=0):
        """
        Clears the color on the pad by setting all pads and buttons to off.

        Parameters:
            None

        Returns:
            None
        """
        if p != "buttons": 
            for i in range(0, 64): drawpad(i, [0,0,0])
        if p != "pads":
            for i in range(0,29): drawextra(i, "off")
def drawextra(id, color):
    """
    Draws one of the external lights (Buttons, Rectangle, Circle, etc.)

    Args:
        id (int): ID of light to display, bottom right-to-left, bottom left-to-up, top left-to-right.
                More info: 1-10: Bottom buttons, right-to-left.
                            11-14: SOLO buttons, bottom-to-top 
                            15-19: Rectangle ights, bottom-to-top.
                            20-23: Circular Lights, Bottom to top.
                            24-29: Top buttons, left-to-right.
                Note: Circular buttons will only have one active at a time.
        color (str): Color in text form, "red", "green", "yellow", "off". A "d" in front of the color means dim, e.g "dred".
                    Not all lights support all colors.
                    Color Chart:
                    Red-Only: PAT BACK, PAT NEXT, BROWSER, GRID LEFT, GRID RIGHT, CIRCULAR LIGHTS
                    Green-Only: SOLO BUTTONS
                    Yellow-only: ALT, STOP
                    Yellow-red: STEP, NOTE, DRUM, PERFORM, SHIFT, LOOP REC
                    Yellow-green: PATTERN, PLAY
    """
    colorid = "00"
    circlerun = False
    firstindex = 0
    for i in reversed(range(1,11)):
        firstindex = firstindex + 1
        if firstindex == id:
            id = i + 43
    if id == 11: id = 39
    if id == 12: id = 38
    if id == 13: id = 37
    if id == 14: id = 36
    if id in range(15,20): id = id + 25
    if id in range(20, 24): 
        id = id - 20
        circlerun = True
    if id in range(24,29): id = id + 7

    if circlerun:
        if color == "red": oncircle.append(id)
        if color == "off": 
            if (id in oncircle): oncircle.remove(id)
        midiout.send_message(bytearray.fromhex("B0 1B 10"))
        for currentrespond in oncircle: 
            if len('{0:x}'.format(id)) == 1: showid = ("0"+'{0:x}'.format(currentrespond))
            else: showid = ('{0:x}'.format(currentrespond))    
            print(currentrespond)
            midiout.send_message(bytearray.fromhex("B0 1B {}".format(showid)))
    else:
        if len('{0:x}'.format(id)) == 1: showid = ("0"+'{0:x}'.format(id))
        else: showid = ('{0:x}'.format(id))           
        if color == "red": 
            if id in range(31, 36): colorid = "02"
            if id in range(44, 49) or id == 53: colorid = "03"
        if color == "dred": 
            if id in range(31, 36): colorid = "01"
            if id in range(44, 49) or id == 53: colorid = "01"
        if color == "green":
            if id in range(36,40): colorid = "02"
            if id in range(50, 52): colorid = "03"
        if color == "dgreen":
            if id in range(36,40): colorid = "01"
            if id in range(50,52): colorid = "01"
        if color == "yellow":
            if id == 49 or id == 51: colorid = "04"
        if color == "dyellow":
            if id == 49 or id == 51: colorid = "02"
        if color == "off": colorid = "00"
        midiout.send_message(bytearray.fromhex("B0 {} {}".format(showid, colorid)))  
def callback():
    '''
    Waits until there is a new MIDI message and returns it immediately.

    Returns:
    [state, channel, type]
    
    -Type: Can either be "pad","extra", or "knobs. "pad" is for the pads, "extra" is for the buttons., and "knobs" is for the knobs.
    -Channel: The channel. If the type is "pad", it is 0-63, but if the type is "extra", it is the same format as the drawextra() function, excluding 15-23, which are lights only, and also adding 29, for the user button. If the type is knobs, then it will be 1-4, right-to-left.
    -State: For "pad", the state will be the velocity. For "extra", the state will be "on" or "off". For Knobs, the state will be "left" or "right", or if it is a press, "on" or "off"
    '''
    global eventwhile
    global eventlist
    while eventwhile:
        time.sleep(waittime)
    eventwhile = True
    return message

def sendMessageHex(message):
    data = bytearray.fromhex(message)
    midiout.send_message(data)

def sendMessage(message):
    print("SendMessage")
    print(message)
    midiout.send_message(message)

def showLCD(arguments):
    sendMessage(fire_lcd.create_sysex_message(arguments))