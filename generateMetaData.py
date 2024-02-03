import util as ut
import json as j
from datetime import datetime

def saveCountryList():
  """
  To save the list of countries for which data is available as a json file (for static dashboard)
  """
  a,f = ut.get_available_country_list()
  country = { "actual": a, "updatedOn":datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
  with open("data/meta.json", "w") as json_file:
    j.dump(country, json_file)
  #j.dumps("data/meta.json")
  # for cf in f :
  #   updateForecastDataForCountry(cf)


saveCountryList()