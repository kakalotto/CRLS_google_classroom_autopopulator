import webbrowser
import os #use for new instance of chrome
import time
#urls I want to open in array
URLS = (
    'https://replit.com/join/cyohbjxtao-eyalben-dov',  # new one
    'https://replit.com/join/zffrihjpct-sylvesterbroich',  # new one
    'https://replit.com/join/krolqgnqvz-lyraericson',
    'https://replit.com/join/pffdbmebxy-estellefraley',
    'https://replit.com/join/sbufbgpbgy-sulavghimire1',
   'https://replit.com/join/ndgafrlkuq-nohagolem',
    'https://replit.com/join/lqobgyuwnj-corbingonsalves',
    'https://replit.com/join/tklxijxgur-rebekahgonzalez',
    'https://replit.com/join/xnaqqlotkp-egaljama1',
    'https://replit.com/@Draconic-Null/2023arilavinewebdev#html/climate.html',
    'https://replit.com/join/ezceeyzsqs-thomasmoraine-r',
    'https://replit.com/join/xdcxsfmwuy-muhaiminulmugdh?authuser=0',   # nothing
    'https://replit.com/join/elzhrjcfau-nathanoconnell3',
    'https://replit.com/join/ybaqimzaxb-ethanoren1',
    'https://replit.com/join/tyvcotqyfx-mayarosen',
    'https://replit.com/join/keecpcmlld-robeltedla1',
    'https://replit.com/join/jxujetrzbt-teanotcoffee',
    'https://replit.com/join/kepbsdxefp-fitsumwoldemesk',
    'https://replit.com/join/vfwzcefxtr-draconic-null',
    'https://replit.com/join/ekzrasptrf-estebanperez6',

    # "https://replit.com/join/dgdjkyxxyy-claudiaharmer",
    # "https://replit.com/join/zbeeyrnghw-jaylenramirez1",
    # "https://replit.com/join/gnhwadhspd-lyricemartin",
    # "https://replit.com/join/gxfrxyeexk-marwa17",
    # "https://replit.com/join/ipjzwbgjzv-zavierpoklop",
    # "https://replit.com/@habaman/HTML1html#css/style.css",
    # "https://replit.com/join/oxzketokkr-josiahpizarro",
    # "https://replit.com/join/baudfobvap-edwinjm27",
    # "https://replit.com/join/cpdbsiwtst-nianjahson",
    # "https://replit.com/join/mlicgeymmj-miladmansour",

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