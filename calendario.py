import requests
import pandas as pd
import json



class Calendario: 

    def __init__(self, giornata=None):

        self.url = "https://www.matchesio.com/it/competition/serie-a-it/export/json/"
        self.giornata = giornata

    def get_calendar(self):

        data = requests.get(url=self.url)
        cal = data.json()

        return cal 




if __name__ == "__main__":

    cal = Calendario()
    calendario = cal.get_calendar()

    x = getattr(cal, "url")
    print(x)