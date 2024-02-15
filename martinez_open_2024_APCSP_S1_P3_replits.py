import webbrowser
import os #use for new instance of chrome
import time
#urls I want to open in array
URLS = (
    'https://replit.com/join/ngjsecuokk-aayanahmad3',
    'https://replit.com/join/kfjlgjhhcr-tushaarashar',
    'https://replit.com/join/fdirrwlvze-ayanbashir',
    'https://replit.com/join/bvvfmgpjct-hendersoncampus',
    'https://replit.com/join/aojcfbvrnb-nolac',
    'https://replit.com/join/grzwvncdxw-pauldottin-camp',
    'https://replit.com/join/gprzmjxxtn-afredenburg',
    'https://replit.com/join/rrvpadxovg-jeffreygao8',
    'https://replit.com/join/cndmqpjohk-nohagolem',
    'https://replit.com/join/gbfqzrbmhh-cookieman123',
    'https://replit.com/join/eymeqsfbfv-namirajara',
    'https://replit.com/join/tyztrxowre-paulkim75',
    'https://replit.com/join/pjruslcvvd-zoyakumar-warik',
    'https://replit.com/join/newkgcqtcn-samuelmayle',
    'https://replit.com/join/cntftuitja-anaispite',
    'https://replit.com/join/gtmaufyrri-hanoroughley',
    'https://replit.com/join/gprzmjxxtn-afredenburg',
    'https://replit.com/join/nnzmwkmsig-maazshaikh15',
    'https://replit.com/join/mopnbwnvce-hermelashimeli1',
    'https://replit.com/join/jvcjpadvlf-clemenssummersg',
    'https://replit.com/join/ngplreqcnz-isaiahthomas-ed',
    'https://replit.com/join/gnyvwgcrqm-tayathoms',
    'https://replit.com/join/klsgfridjs-kayleeyung',
    'https://replit.com/join/wsgcnmwciw-hendersoncampus',
    'https://replit.com/join/nkkaelooed-nohagolem',
    'https://replit.com/join/krpvqaummz-amannehela',
    'https://replit.com/join/tnmkegzvoy-suleymansuleym6',
    'https://replit.com/join/veolloebnf-isaiahthomas-ed',
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
    time.sleep(5)