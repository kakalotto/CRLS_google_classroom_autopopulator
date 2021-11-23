import webbrowser
import os #use for new instance of chrome
import time
#urls I want to open in array
URLS = (
    'https://replit.com/join/fwocufyteo-eleanoraminoff',
    'https://replit.com/join/thidpscvyz-ninaaubourg',
    'https://replit.com/join/tvdhzvpxdr-moniquebennett',
    'https://replit.com/join/bjgjhuyznw-jacobbronstein',
    'https://replit.com/join/umxvtmvaud-brayzenchase',
    'https://replit.com/join/ciizlqttjs-riverdoyle',
    'https://replit.com/join/rpvdqayctf-keanufeik',
    'https://replit.com/join/xswphjbtrn-maeghanfischer',
    'https://replit.com/join/smbzvrwoob-farhankalam',
    'https://replit.com/join/ixlnocfmyx-abdiladifgurhan',
    'https://replit.com/join/lsrbesllqy-evakaufman',
    'https://replit.com/join/vflzxfizoz-arilavine',
    'https://replit.com/join/umrskjmgqo-simonmebatsion',
    'https://replit.com/join/mhsjqmzuuv-kputr',
    'https://replit.com/join/scmwbhwqur-jamesrochberg',
    'https://replit.com/join/pqtlgzqizd-ethanromaine',
    'https://replit.com/join/vmgzllecuy-sarasabry',
    'https://replit.com/join/cfijpavvkq-robeltedla1',
    'https://replit.com/join/gagjoswzte-lavaslug',
    'https://replit.com/join/drtgxwkghv-michaelzaccagni',


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