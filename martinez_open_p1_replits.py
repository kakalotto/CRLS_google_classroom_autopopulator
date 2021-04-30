import webbrowser
import os #use for new instance of chrome
import time
#urls I want to open in array
URLS = (
    "https://repl.it/join/gtvqeuks-milosongweiss",
    "https://repl.it/join/ulrdnyaw-robertclemens",
    " https://repl.it/join/dxcpobby-robertclemens",
    "https://repl.it/join/mvhufewc-williamspeight",
    "https://repl.it/@SOPHIAPRICE/SOPHIA#.replit",
    "https://repl.it/join/xgkzzveg-athearling ",
    "https://repl.it/join/vqrrawkf-josephbetancour",
    "https://repl.it/join/nttotywk-isaacwedaman",
    "https://repl.it/join/owitzuia-stephengwoncpsd",
    "https://repl.it/join/aakyvbrr-samuelkim17",
    "https://repl.it/join/ovthbetr-abelteclemariam",
    "https://repl.it/join/nliipkyn-laraartigas",
    "https://repl.it/join/hehzipaf-skylermarks",
    "https://repl.it/join/owitzuia-stephengwoncpsd",
    "https://repl.it/@JOSEPHBETANCOUR/Joeys-code-doc#2020_joey_6.032.py",
    "https://repl.it/join/lxyptqfl-alister123",
    "https://repl.it/@RIVKAZICKLER/2020rivzickpy",
     )

#https://repl.it/join/awyoavmf-camillepaul
#https://repl.it/join/hmrrwond-justincolon

# https://repl.it/@LidyaShewarega/BriskGlumCustomers#main.py
#https://repl.it/@NafisJoy/FlashySereneSolidstatedrive#main.py
#https://repl.it/join/fzinflql-danielhailemich
#https://repl.it/@CHRISTIANHERNA8/AcrobaticImmenseDrawings

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