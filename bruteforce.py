import serial
import time
import cv2
import os

cam = cv2.VideoCapture(0)

ser = serial.Serial('COM6', 115200)

def homing():
    time.sleep(2)
    ser.write("G28\r\n".encode('utf-8'))
    ser.write("G1 Z10 F100".encode('utf-8'))
    time.sleep(1)
    #ser.close()

nmbr = 1234

zeit_fuer_drucker_zu_druecken = 3
zeit_zwischen_vollen_eingaben = 1
versuche_bis_sperrung = 4
sperrzeit_in_sek = 5
zeit_bis_bildschirm_aus = 10

zeit_wann_bildschirm_reaktivieren = zeit_bis_bildschirm_aus/3

display_digit_pos = [   "G1 X0 Y-25 F80000\r\n",
                        "G1 X-14 Y12 F80000\r\n","G1 X1 Y12 F80000\r\n","G1 X15 Y12 F80000\r\n",
                        "G1 X-16 Y0 F80000\r\n","G1 X0 Y0 F80000\r\n","G1 X18 Y0 F80000\r\n",
                        "G1 X-15 Y-12 F80000\r\n","G1 X-2 Y-12 F80000\r\n", "G1 X15 Y-12 F80000\r\n"]

ok_btn = ["G1 X22 Y-5 F80000\r\n"]

# zum Testen, ob alle Ziffern angesteuert werden
def durchlauf():
    ser.write(ok_btn[0].encode('utf-8'))
    time.sleep(3)
    for i in display_digit_pos:
        print("Zahl die gewählt wird: " + str(display_digit_pos.index(i)))
        current_index = display_digit_pos.index(i)
        ser.write(display_digit_pos[current_index].encode('utf-8'))
        ser.write("G1 Z-5 F500\r\n".encode('utf-8'))
        ser.write("G1 Z0 F8000\r\n".encode('utf-8'))
        time.sleep(3)

# Drucker drückt auf Ziffer
def press_digit(digit):
    ser.write(display_digit_pos[digit].encode('utf-8'))
    ser.write("G1 Z-5 F500\r\n".encode('utf-8'))
    ser.write("G1 Z0 F8000\r\n".encode('utf-8'))

# Drucker behält das Display am Leben
def verhalten_bei_sperrung():
    print("\n\n##################")
    print("20 Sekunden Pause")

    ser.write(ok_btn[0].encode('utf-8'))


    for i in range(2):
        time.sleep(zeit_wann_bildschirm_reaktivieren)
        print("DRÜCKE BILDSCHIRM")
        ser.write("G1 Z-5 F500\r\n".encode('utf-8'))
        ser.write("G1 Z0 F500\r\n".encode('utf-8'))


    time.sleep(zeit_wann_bildschirm_reaktivieren)
    print("##################")

# Bild von der Eingabe aller 4 Ziffern
def take_screenshot(i):
    ser.write("G1 X40 Y100 F8000\r\n".encode('utf-8'))
    time.sleep(2)
    ret, frame = cam.read()
    img_name = f'{str(i).zfill(4)}.jpg'
    cv2.imwrite(img_name    ,frame)
    print('screenshot taken')


# UI - Versuch Nummer
def display_versuchsnummer(i):
    print("\n\n\n------------------------")
    print("                       |")
    print("PIN: " + str(i).zfill(4)+ "              |")
    print("                       |")
    print("------------------------")


def reverse_number(num):
    global reversed
    reversed = str(num)[::-1]

def get_digit(number):
    for i in range(len(str(number))):
        digit = number // 10**i % 10
        print(digit)
        press_digit(digit)
        time.sleep(zeit_fuer_drucker_zu_druecken)
        #press_digit(digit)
    #return number // 10**n % 10


if(True):
    print("\n### DURCHLAUF ALLER ZIFFERN ###")
    ser.write("G92 X0 Y0 Z-5\r\n".encode('utf-8'))
    ser.write("G1 Z0 F8000\r\n".encode('utf-8'))
    time.sleep(5)
    durchlauf()

    print("\n\n\n### PROGRAMM START ###")
    os.chdir(r'C:\Users\berez\Desktop\sarbinasHandy\env\Scripts\Images')

    for i in range(10000):
        if(i%versuche_bis_sperrung == 0 and i != 0):
            verhalten_bei_sperrung()

        display_versuchsnummer(i)

        reverse_number(str(i).zfill(4))
        get_digit(int(reversed))

        take_screenshot(i)


    cam.release()
    cam.destoryAllWindows()
