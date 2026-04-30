import re


class SQLValidator:

    @staticmethod
    def basic_check(sql: str) -> bool:
        if not sql:
            return False

        sql = sql.strip()

        # remove prefix like "SQL:"
        sql = re.sub(r"^sql\s*:\s*", "", sql, flags=re.IGNORECASE)

        sql_lower = sql.lower()

        # must contain select
        if "select" not in sql_lower:
            return False

        # prevent dangerous queries
        forbidden = ["drop", "delete", "update", "insert", "alter"]

        for word in forbidden:
            if re.search(rf"\b{word}\b", sql_lower):
                return False

        return True

    @staticmethod
    def fix_format(sql: str) -> str:
        sql = sql.strip()

        sql = re.sub(r"^sql\s*:\s*", "", sql, flags=re.IGNORECASE)

        if not sql.endswith(";"):
            sql += ";"

        return sql