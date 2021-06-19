# running strategies and sending broker signal every time new price is appended to db

import os
from binance.client import Client
import numpy as np
import pandas as pd
#import btalib
from datetime import datetime
import time
import math

on database update:
    action = strategy(params)
    call_api_binance(action)
    update action column in database















