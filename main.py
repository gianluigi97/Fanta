from serieA_data import Calendario, Stats
from database import Database

cal = Calendario()
stats = Stats()
db = Database(database="fanta")

stats.update_stats()




db.upsert(table="calendario_serieA", rows=cal.calendar())
db.upsert(table="stats_giocatori", rows=stats.players)

