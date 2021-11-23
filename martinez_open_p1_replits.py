import webbrowser
import os #use for new instance of chrome
import time
#urls I want to open in array
URLS = (
    'https://replit.com/join/cwyjhhfnwa-milobell',
    'https://replit.com/join/zlhoiaiypc-eyalben-dov',
    'https://replit.com/join/ykdocbzech-elliemberman',
    'https://replit.com/join/huptiizwii-deanbittker',
    'https://replit.com/join/gnorjkhbza-henrybonney',
    'https://replit.com/join/qqeiigekln-kristenchun1',
    'https://replit.com/join/zjpucylnzy-justincolon',
    'https://replit.com/join/aaojtgiste-uridarom',
    'https://replit.com/join/snuwrsqhxh-benjamindavis11',
    'https://replit.com/join/tbyhrfdlrk-evanfay',
    'https://replit.com/join/smuhhfbxqa-aniahearn',
    'https://replit.com/join/wklvbdprzs-alexandramahaja',
    'https://replit.com/join/oarqnxfkgk-mohammedalial10',
    'https://replit.com/join/dpgfvcnqng-thomasmoraine-r',
    'https://replit.com/join/bgmcatgtmg-emmarandalljarr',
    'https://replit.com/join/uabfcsqvty-camillerheault',
    'https://replit.com/join/rujrikknmr-addisonrosenblu',
    'https://replit.com/join/jdznfnjrvv-iloraroy',
    'https://replit.com/join/thcocbblbj-alexanderwarre2',
    'https://replit.com/@NasreenWashingt/apcsp-2021-22#main.py',



#
#
# https://replit.com/join/umxvtmvaud-brayzenchase
# https://replit.com/join/smbzvrwoob-farhankalam
# https://replit.com/join/rpvdqayctf-keanufeik
# https://replit.com/join/tvdhzvpxdr-moniquebennett
# https://replit.com/join/xswphjbtrn-maeghanfischer
# https://replit.com/join/thidpscvyz-ninaaubourg
# https://replit.com/join/vflzxfizoz-arilavine
# https://replit.com/join/ciizlqttjs-riverdoyle
# https://replit.com/join/scmwbhwqur-jamesrochberg
# https://replit.com/join/umrskjmgqo-simonmebatsion
# https://replit.com/join/vmgzllecuy-sarasabry
# https://replit.com/join/bjgjhuyznw-jacobbronstein
# https://replit.com/join/pqtlgzqizd-ethanromaine
# https://replit.com/join/drtgxwkghv-michaelzaccagni
# https://replit.com/join/cfijpavvkq-robeltedla1
# https://replit.com/join/gagjoswzte-lavaslug
# https://replit.com/join/mhsjqmzuuv-kputr

     )

#https://repl.it/join/awyoavmf-camillepaul
#https://repl.it/join/hmrrwond-justincolon

# https://repl.it/@LidyaShewarega/BriskGlumCustomers#main.py
#https://repl.it/@NafisJoy/FlashySereneSolidstatedrive#main.py
#https://repl.it/join/fzinflql-danielhailemich
#https://repl.it/@CHRISTIANHERNA8/AcrobaticImmenseDrawings

#change chrome_path to the
chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" #note the double \ syntax
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

#firefox_path = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
#firefox_path = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'

#webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))

#open new instance of chrome
#os.system(r'"C:\\Program Files\\Mozilla Firefox\\firefox.exe"')
#os.system(r'"C:\\Program Files (x86)\\arduino\\arduino.exe"')
#webbrowser.register('firefox', None, webbrowser.GenericBrowser(firefox_path))
#webbrowser.get('firefox').open('https://espn.com')

#open each url
for url in URLS:
    webbrowser.get('chrome').open(url)
    time.sleep(0.2)