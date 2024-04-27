import os

from scripts import extraction
from utils import logger
from utils import context
from utils import emails

directory = context.get_context(os.path.abspath(__file__))
logging = logger.setup_logger("logger", f"{directory}/src/logs/main.log")

def main():
  extraction.extract()

if __name__ == "__main__":
  main()