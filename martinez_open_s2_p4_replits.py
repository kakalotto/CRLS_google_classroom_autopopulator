import webbrowser
import os #use for new instance of chrome
import time
#urls I want to open in array
URLS = (
    "https://repl.it/join/jfinqxpl-adelbaimatova",
    'https://repl.it/@MohamedNabilBen/ParchedBackCircle#main.py',
    'https://repl.it/@fairoozc/fairooz#2020_fairooz_1.040.py',
    'https://repl.it/join/chsokwmn-pcbobo1',
    'https://repl.it/join/raodezry-kiduszdesalegn',
    "https://repl.it/join/vqsauava-maiafeik",
    "https://repl.it/join/kxgghsdt-christophergoul",
    'https://repl.it/@selinahail10/selinahail#2020_selina_1.040.py',
    'https://repl.it/@DANIELHAILEMICH/ScarceSnarlingRuby',
    "https://repl.it/join/uykxcoxb-amelhirwa",
    'https://repl.it/@willk52/ShockingQuickCharacters#.replit',
    "https://repl.it/@NILAKRISHNAMURT/Nilas-CS#main.py",
    "https://repl.it/join/terrsuap-andrewmccarroll",
    "https://repl.it/join/cgoajddj-basemmoustafa",
    'https://repl.it/@Mobro123/Mobros-stuff',
    'https://repl.it/join/sdiznzka-mirandasantiago',


)
p4 = ['https://repl.it/login?goto=/join/yjiayarx-sophiaprice']
#change chrome_path to the
chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" #note the double \ syntax
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

#open new instance of chrome
os.system(r'"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"')
# os.system(r'"C:\\Program Files (x86)\\arduino\\arduino.exe"')

#open each url
for url in URLS:
    webbrowser.get('chrome').open(url)
    time.sleep(0.2)