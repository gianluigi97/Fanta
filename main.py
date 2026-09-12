from matchesIO import Calendario
from database import Database

cal = Calendario()
db = Database(database="fanta")



db.upsert(table="calendario_serieA", rows=cal.calendar())

