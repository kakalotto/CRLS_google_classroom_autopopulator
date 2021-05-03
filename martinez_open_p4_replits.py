import webbrowser
import os #use for new instance of chrome
import time
#urls I want to open in array
URLS = (
    "https://repl.it/join/tvswfevs-antoniobarandao",
    "https://repl.it/join/syzsrhbv-nebiyudemie",
    "https://repl.it/join/xtwfabhx-lucyengels",
    "https://repl.it/join/puptgept-elikanner",
    "https://repl.it/join/ykhairng-mahek15",
    "https://repl.it/join/tbqpkmmn-sergeykoenig",
    "https://repl.it/join/jcyecgjw-jinhoho3",
    "https://repl.it/join/vtemevex-cedarlarson",
    "https://repl.it/join/knqauwxr-matthewliu3",
    "https://repl.it/join/sspdcbyk-zaccariamir",
    "https://repl.it/join/nbjdxvik-23munger",
    "https://repl.it/join/eughppjc-tavienpollard",
    "https://repl.it/@EliasEliasElais/2020Elias2032apy",
    "https://repl.it/join/khtpyvpl-clairewang3",

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