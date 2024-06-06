import os
import sys

from dotenv import load_dotenv

sys.dont_write_bytecode = True

load_dotenv()

SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_PORT = int(os.getenv('SERVER_PORT')) # type: ignore
IS_PROD = bool(os.getenv('IS_PROD'))