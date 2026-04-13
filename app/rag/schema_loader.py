from app.createdb import Customer, Product, Category, Order, OrderItem
from app.core.database import engine
from sqlalchemy import inspect
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

def get_primary_keys(insp, table_name):
    pk_constraint = insp.get_pk_constraint(table_name)
    return pk_constraint.get('constrained_columns', [])


def get_foreign_keys(insp, table_name):
    fk_constraints = insp.get_foreign_keys(table_name)

    fk_map = {}

    for fk in fk_constraints:
        for col in fk.get('constrained_columns', []):
            fk_map[col] = {
                "referred_table": fk.get('referred_table'),
                "referred_columns": fk.get('referred_columns')
            }

    return fk_map


def get_schema():
    insp = inspect(engine)

    tables = [
        Customer.__tablename__,
        Product.__tablename__,
        Category.__tablename__,
        Order.__tablename__,
        OrderItem.__tablename__
    ]

    schema = []

    for table in tables:
        columns = insp.get_columns(table)
        pk_columns = get_primary_keys(insp, table)
        fk_map = get_foreign_keys(insp, table)

        table_dict = {
            "table": table,
            "columns": [],
            "relationships": []
        }

        for col in columns:
            col_name = col['name']

            column_info = {
                "name": col_name,
                "type": str(col['type']),
                "nullable": col['nullable'],
                "primary_key": col_name in pk_columns
            }

            
            if col_name in fk_map:
                fk_info = fk_map[col_name]

                column_info["foreign_key"] = {
                    "referred_table": fk_info["referred_table"],
                    "referred_column": fk_info["referred_columns"][0]
                }

                table_dict["relationships"].append({
                    "from_column": col_name,
                    "to_table": fk_info["referred_table"],
                    "to_column": fk_info["referred_columns"][0]
                })

            table_dict["columns"].append(column_info)

        schema.append(table_dict)

    return schema


def schema_to_text(schema):
    """
   convert the schema information into a human-readable text format suitable for embedding.
    """
    texts = []

    for table in schema:
        lines = []
        lines.append(f"Table {table['table']}:")

        for col in table["columns"]:
            line = f"- {col['name']} ({col['type']}"

            if col["primary_key"]:
                line += ", PK"

            if "foreign_key" in col:
                fk = col["foreign_key"]
                line += f", FK → {fk['referred_table']}.{fk['referred_column']}"

            line += ")"
            lines.append(line)

        texts.append("\n".join(lines))

    return texts


if __name__ == "__main__":
    schema = get_schema()

    print("====== JSON Schema ======")
    print(json.dumps(schema, indent=2))

    print("\n====== Text for Embedding ======")
    texts = schema_to_text(schema)

    # Save the schema and texts to files for visual understanding and future reference
    with open(os.path.join(DATA_DIR, "schema.json"), "w") as f:
        json.dump(schema, f, indent=2)
    
    with open(os.path.join(DATA_DIR, "schema_texts.txt"), "w", encoding="utf-8") as f:
        for t in texts:
            f.write(t + "\n\n")

    for t in texts:
        print(t)
        print("-" * 50)