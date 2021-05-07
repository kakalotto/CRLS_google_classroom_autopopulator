import configparser

config = configparser.ConfigParser()		
config.read("classroom_assignments_to_aspen.ini")
login = config['LOGIN']
username = login['username']
password = login['password']
l.,,,m,
server = config['SERVER']