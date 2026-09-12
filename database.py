from sqlalchemy import create_engine, text, MetaData, Table, select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os


load_dotenv(r"/Users/gianluigimosti/WorkPlace/Fanta/key.env")

class Database:

    def __init__(self, database):

        self.username = os.getenv("DB_USERNAME")
        self.password = os.getenv("DB_PASSWORD") 
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.db = database

        self._engine = None
        self._metadata = MetaData()
        self._tables = {}

    def _get_engine(self):

        if self._engine: 
            return self._engine

        self._engine = create_engine(
            f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}",
            connect_args={'connect_timeout':5}
        )

        return self._engine

    def _get_table(self, table_name):

        if table_name in self._tables:
            return self._tables[table_name]

        table = Table(
            table_name,
            self._metadata,
            autoload_with=self._get_engine()
        )

        self._tables[table_name] = table
        return table

    

    def select(self, table_name):

        table = self._get_table(table_name)

        stmt = select(table)

        with self._get_engine().begin() as conn:
            res = conn.execute(stmt).mappings().all()
            
            return res

    def upsert(self, table, rows):

        table = self._get_table(table_name=table)
        stmt = insert(table).values(rows)

        update_columns = {
            column.name: stmt.inserted[column.name]
            for column in table.columns
            if not column.primary_key
        }

        stmt = stmt.on_duplicate_key_update(**update_columns)
        with self._get_engine().begin() as conn: 
            conn.execute(stmt)



if __name__ == "__main__":

    db = Database(database="fanta")
    result = db.select(table_name="calendario_serieA")

    print(result)
