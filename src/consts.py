from time import time
from utils import from_hex

SEED = int(time())
START_ADDRESS = from_hex(200)
DEBUG = True

if DEBUG:
    SEED = 0
