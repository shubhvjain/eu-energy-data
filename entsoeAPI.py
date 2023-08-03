import pandas as pd
from datetime import datetime, timedelta
import time
from entsoe import EntsoePandasClient as entsoePandas
import os

def getAPIToken():
  variable_name = "ENTSOE_TOKEN"
  value = os.environ.get(variable_name)
  if value is None:
    raise ValueError(f"The required environment variable '{variable_name}' is not set.")
  return value

# print(getAPIToken())