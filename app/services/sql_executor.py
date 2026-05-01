from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError

from app.core.database import SessionLocal


class SQLExecutor:

    def execute(self, sql: str):

        db = SessionLocal()

        try:
            result_proxy = db.execute(text(sql))
            rows = [dict(r._mapping) for r in result_proxy]
            return rows

        except ProgrammingError as e:
            error_msg = str(e.orig)

            # column 
            if "column" in error_msg.lower():
                return [{"error": "Column not found in database"}]

            # table 
            if "relation" in error_msg.lower():
                return [{"error": "Table not found"}]

            return [{"error": error_msg}]

        except Exception as e:
            return [{"error": str(e)}]

        finally:
            db.close()