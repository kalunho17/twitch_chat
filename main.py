import argparse
from datetime import datetime

def get_args():
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--c", type=str, required=True, help="Set channel id")
    return parser.parse_args()
    
# -----------------------------------------------------------------
# Twitch Bot
# -----------------------------------------------------------------
import irc.bot
import requests
from functools import lru_cache

class TwitchBot(irc.bot.SingleServerIRCBot):

    def __init__(self, username, client_id, token, channel):
        self.username = username
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel
       
        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print( 'Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:{0}'.format(token))], username, username)
        
    def on_welcome(self, c, e):
        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        source = e.source.split("!")[0]
        message = e.arguments[0]
        self.log(source, message)
    
    # do stuff with your message here
    def log(self, source, message):
        sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S')
        print(sttime + " " + source + " "+ message)
    
def main():
    # Process arguments
    args = get_args()
    channel = args.c 

    # ---------------------------------------
    # Twitch API
    # ---------------------------------------
    
    # Generate token here
    # client_id: https://dev.twitch.tv/console
    # token: https://twitchapps.com/tmi/
    
    username  = ""
    client_id = ""
    token     = ""
    
    try:
        bot = TwitchBot(username, client_id, token, channel)
        bot.start()
    except KeyboardInterrupt:
        print("closing bot...")

if __name__ == "__main__":
    main()
