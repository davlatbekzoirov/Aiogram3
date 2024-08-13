from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN") 
ADMINS = list(map(int,env.list("ADMINS")))    
IP = env.str("ip") 
