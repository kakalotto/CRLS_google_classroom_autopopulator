import webbrowser
import os #use for new instance of chrome
import time
#urls I want to open in array
URLS = (
    'https://repl.it/join/gmfakhfz-20eman05',
    'https://repl.it/join/ytupppms-agentthree',
    'https://repl.it/@LONSOIRR/APCSP#main.py',
    'https://repl.it/@FAROOZKHANTRUNN/faroooz',
    'https://repl.it/@JeiranKvaitchad/HW#2021_Jeiran_1.040.py',
    'https://repl.it/@ANWESHAMAITY/APCSP1#2021_wisha_1.040.py',
    # mekeyas
    'https://repl.it/@DEREKPRICE/DEREK',
    'https://repl.it/@EliasRegina/Test#.replit',
    'https://repl.it/@SauvikRoy/2020sauvik6021py',
    # zoe
    # grace
    # jiaming
    'https://repl.it/@GostCat/Home-Base#2020_theo_1.040.py',
    "https://repl.it/@CHLOEYANG4/APCSP#2021_cyang_1.040.py",

)
#https://replit.com/join/anwkmkwf-camillepaul

#https://repl.it/join/awyoavmf-camillepaul
#https://repl.it/join/hmrrwond-justincolon
#https://repl.it/join/eeleclou-lidyashewarega
#https://repl.it/@OLAMIDEMARTINS/IntelligentDismalDisassembly
#https://repl.it/@NafisJoy/FlashySereneSolidstatedrive#main.py
# https://repl.it/join/snndyhoy-anthonyariasest
#https://repl.it/@CHRISTIANHERNA8/AcrobaticImmenseDrawings
# https://repl.it/@KERVENCOLO/WhirlwindPoliteFiles

#change chrome_path to the
#chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" #note the double \ syntax
#webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

#firefox_path = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
firefox_path = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'

webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))

#open new instance of chrome
os.system(r'"C:\\Program Files\\Mozilla Firefox\\firefox.exe"')
#os.system(r'"C:\\Program Files (x86)\\arduino\\arduino.exe"')
webbrowser.register('firefox', None, webbrowser.GenericBrowser(firefox_path))
#webbrowser.get('firefox').open('https://espn.com')

#open each url
for url in URLS:

   webbrowser.get('firefox').open(url)
   time.sleep(0.2)