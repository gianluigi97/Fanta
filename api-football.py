import requests
import pandas as pd
import json
from dotenv import load_dotenv
import os
from tqdm import tqdm
import pandas as pd

required_stats = ['games-played', 'goals', 'assists', 'yellow-cards', 'red-cards', 'dribble-percentage', 'goals-conceded', 'penalty-attempts', 'penalties-successful', 'Xg', 'tackles-won-perc', 'penalty-conceded', 'Substitute On', 'Substitute Off']

load_dotenv(r"C:\GianC\Fanta\key.env") #WIN
seasonId="serie-a::Football_Season::ed7fdc2a3e7b408b942ec177b7b956b5"
url = f"https://api-sdp.legaseriea.it/v1/serie-a/football/seasons/{seasonId}/stats/players?page=current_page"


headers = {
  'User-Agent': "Mozilla/5.0",
}
players = []

for current_page in tqdm(range(1, 15),desc="download players",unit=" pagina", ncols=100):

   response = requests.get(url.replace("current_page", str(current_page)), headers=headers, timeout=30)
   response.raise_for_status()

   result = response.json()
   players_list = result.get("players", []) or []

   for g in players_list: 

      if not g.get("bibNumber"):
        continue

      stats=[s for s in g.get("stats", []) if s.get("statsId") in required_stats]

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

      players.append(row)



df = pd.DataFrame(data=players)
df.to_csv(r"C:/GianC/Fanta/stats_giocatori_2.csv", index=False)
print(df)

# print(players)

