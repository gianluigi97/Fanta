import requests
import pandas as pd
import json



class Calendario: 

    def __init__(self, giornata=None):

        self.url = "https://www.matchesio.com/it/competition/serie-a-it/export/json/"
        self.giornata = giornata

    
    def _extract_calendar(self):

        data = requests.get(url=self.url)
        cal = data.json()

        return cal 

    @staticmethod
    def format_team(team):
        return team.replace("AS ", "").replace("AC ", "")

    def calendar(self):

        cal = self._extract_calendar()
        result = []

        for c in cal: 
            if c.get("status") == "Giocata":

                homeTeam = self.format_team(c.get("homeTeam"))
                awayTeam = self.format_team(c.get("awayTeam"))

                partita = {
                    'key' : f'{c.get('matchday')}_{homeTeam.lower()[:3]}_{awayTeam.lower()[:3]}',
                    'giornata' : c.get("matchday"),
                    'data' : c.get('date'),
                    'squadra_casa' : homeTeam,
                    'squadra_ospite' : awayTeam,
                    'stato' : c.get("status"),
                    'score_sq_casa' : c.get("result").split("-")[0],
                    'score_sq_ospite' : c.get("result").split("-")[1],
                }

                result.append(partita)

        return result

if __name__ == "__main__":

    cal = Calendario()
    calendario = cal.calendar()

    for c in calendario: 
        print(c)