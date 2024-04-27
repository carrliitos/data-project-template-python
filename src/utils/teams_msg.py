import pymsteams
import os
import json

from utils import context
from utils import vh_config

directory = context.get_context(os.path.abspath(__file__))

def send(logger, message, title):
  try:
    with open(f"{directory}/utils/config/config.json", "r") as conf_file:
      conf = json.load(conf_file)

    url = conf["MSTeams"]["url"]
    
    myTeamsMessage = pymsteams.connectorcard(url) 
    myTeamsMessage.title(title)
    myTeamsMessage.text(message)
    myTeamsMessage.send()
  except Exception as e:
    logger.error(f"Config file was not found: {e}")
