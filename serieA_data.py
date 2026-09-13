import requests
import pandas as pd
import json
import os
from tqdm import tqdm
import pandas as pd



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


class Stats: 


    REQ_STATS = ['games-played', 'goals', 'assists', 'yellow-cards', 'red-cards', 'dribble-percentage', 'goals-conceded', 'penalty-attempts', 'penalties-successful', 'Xg', 'tackles-won-perc', 'penalty-conceded', 'Substitute On', 'Substitute Off']

    def __init__(self):

        self.url = "https://api-sdp.legaseriea.it"
        self._seasonId = "serie-a::Football_Season::ed7fdc2a3e7b408b942ec177b7b956b5" 
        self.players = []
        self._headers={'User-Agent': "Mozilla/5.0"}

    def _request(self, current_page):

        url = self.url + f"/v1/serie-a/football/seasons/{self._seasonId}/stats/players?page=current_page"

        response = requests.get(url.replace("current_page", str(current_page)), headers=self._headers, timeout=30)
        response.raise_for_status()
        return response.json()

        
    def update_stats(self):

        for current_page in tqdm(range(1, 15),desc="download players",unit=" pagina", ncols=100):

            result = self._request(current_page=current_page)
            players_list = result.get("players", []) or []


            for g in players_list: 

                if not g.get("bibNumber"):
                    continue

                stats=[s for s in g.get("stats", []) if s.get("statsId") in self.REQ_STATS]

                key = g.get("playerId").split("::")[-1]
                row = {
                    "key" : key,
                    "name": g.get("shortName"),
                    "team" : (g.get("team") or {}).get("shortName"),
                    "role" : g.get("role"),
                    "number" : g.get("bibNumber"),
                }

                row.update({
                    s.get("statsId"): s.get("statsValue") 
                    for s in stats
                    })

                self.players.append(row)


    def prepare_csv(self):

        self.update_stats()
        df = pd.DataFrame(data=self.players)
        df.to_csv(r"C:/GianC/Fanta/stats_giocatori_2.csv", index=False)
































if __name__ == "__main__":

    cal = Calendario()
    calendario = cal.calendar()

    print(calendario)
    