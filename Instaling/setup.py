import pyautogui as pag
import keyboard
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.EdgeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option('detach', True)
service = EdgeService()

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

driver = webdriver.Edge(service=service, options=options)
driver.get('https://instaling.pl/teacher.php?page=login')
driver.maximize_window()

counter=0
print("Zaloguj sie i wlacz sesje a nastepnie najedz na centralny przycisk po czym wcisnij ` (to cos pod ESC).")
def press(key):
    global pos
    global pos2
    global counter
    global pox2
    global poy2
    if(key.name == "`" and counter ==0 ):
        pos = pag.position()
        #print("pos",pos)
        counter+=1
    elif(key.name == "`" and counter == 1 ):
        pos2 = pag.position()
        pox2 = pos2[0]
        poy2 = pos2[1]
        #print("pos2",pos2)
        counter+=1


keyboard.on_press(press)
keyboard.wait("`")
print('kliknij w ten przycisk(rozpoczni sesje czy cos takiego) i ponownie kliknij ` trzymajac myszke nad przyciskiem sprawdz')
keyboard.wait("`")

pox = pos[0]
poy = pos[1]



"""if(keyboard.read_key('=')):
    pos2 = pag.position()
    print(pos2)"""

log = input("wpisz login do instalinga")
has = input("wpisz haslo do instalinga")

#print('stworz plik "cred.txt" i wklej do niego dane poniżej jednym ciągiem')
"""print(" ")
print(log)
print(has)
print(pox)
print(poy)
print(pox2)
print(poy2,"\n")"""
#close=input("mozesz zamknac program")

file = open("./src/dbase/cred.txt","w")
file.writelines([log,"\n",has,"\n",str(pox),"\n",str(poy),"\n",str(pox2),"\n",str(poy2)])
file.close()