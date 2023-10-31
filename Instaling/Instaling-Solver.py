import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

from bs4 import BeautifulSoup as bs

import pandas as pd

import pyautogui as pag

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

options = webdriver.EdgeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option('detach', True)
service = EdgeService()

#load up login credentials
cred = open("./src/dbase/cred.txt", "r")
usrnm = cred.readline()
passwert = cred.readline()
pagx = int(cred.readline())
pagy = int(cred.readline())
pagx2 = int(cred.readline())
pagy2 = int(cred.readline())
cred.close()

def center():
    pag.moveTo(pagx2,pagy2)

def centerstr():
    pag.moveTo(pagx,pagy)

#load in the dictionary
global Df
Df = pd.read_csv("./src/dbase/words.csv")

dfpol = Df["pol"]
dfger = Df["ger"]
dfdesc = Df["desc"]
wCount = len(Df.index)
#print(Df)

driver = webdriver.Edge(service=service, options=options)
ac = ActionChains(driver)
driver.maximize_window()

#log in
driver.get('https://instaling.pl/teacher.php?page=login')
login = driver.find_element(By.ID,'log_email')
login.send_keys(usrnm)
password = driver.find_element(By.ID,'log_password')
password.send_keys(passwert)
#THIS BIT SUBMITS PASSWORD
#col12 = driver.find_element(By.CLASS_NAME,"col-12")
#col12.submit()

#begin test
beg1 = driver.find_element(By.PARTIAL_LINK_TEXT, 'sesję')
beg1.click()
WebDriverWait(driver, 5).until(EC.title_is('instaling'))

#to replace with universal method
centerstr()
pag.leftClick()
center()

fillout = 20
while(fillout>0):
    #print(Df)
    #print(wCount)
    #print("fillout:",fillout)
    pol = driver.find_element(By.CLASS_NAME, 'translations')
    pol2 = bs(pol.get_attribute('innerHTML'), 'html.parser')
    desc0 = driver.find_element(By.CLASS_NAME,'usage_example')
    desc = bs(desc0.get_attribute('innerHTML'), 'html.parser')
    #print(desc)
    ger = driver.find_element(By.ID, "answer")
    #print("pol2:",pol2,'\n')
    
    if(pol2 in Df.values):
        #print("jest")
        for i in range(wCount):
            #print(desc,str(Df['desc'][i]))
            if(str(Df['pol'][i]) == str(pol2) and str(Df['desc'][i])==str(desc)):
                #print(dfpol[i])
                #print(dfger[i])
                ans = Df['ger'][i]
                #print(ans)
                ger.send_keys(str(ans))
                #print("fillout")
                #to replace with universal method
                center()
                pag.leftClick()
                pag.leftClick()
                fillout-=1
    else:
        #print("pol2:",pol2)
        
        #to replace with universal method
        pag.leftClick()
        WebDriverWait(driver, 0.2)
        transl = bs(driver.find_element(By.ID, 'word').get_attribute('innerHTML'), 'html.parser')
        #print("transl:", transl)
        newW = pd.DataFrame({'pol':[str(pol2)],'ger':[str(transl)],'desc':[str(desc)]})
        #print(newW)
        Df = pd.concat([Df,newW], ignore_index = True)
        
        #to replace with universal method
        pag.leftClick()
        wCount+=1
        print("Df in Quest:", Df)


print("done")
"""ex2sav = pd.ExcelWriter('words.xlsx', mode='a', if_sheet_exists="replace")
Df.to_excel(ex2sav,'Sheet1', index=False, startcol=0, startrow=0)
ex2sav.save()"""

Df.to_csv("./src/dbase/words.csv",mode='w',index=False)