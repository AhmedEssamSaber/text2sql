from app.db_models import Customer, Product, Category, Order, OrderItem
from app.core.database import engine
from sqlalchemy import inspect
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)


def get_primary_keys(insp, table_name):
    return insp.get_pk_constraint(table_name).get('constrained_columns', [])


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
    texts = []

    for table in schema:
        table_name = table["table"]
        col_names = [col["name"] for col in table["columns"]]

        # Table description
        texts.append(
            f"Table {table_name} has columns: {', '.join(col_names)}"
        )

        # Primary keys
        for col in table["columns"]:
            if col["primary_key"]:
                texts.append(
                    f"{table_name}.{col['name']} is primary key"
                )

        # Important columns
        for col in table["columns"]:
            if col["name"] in ["name", "email", "price", "total_amount", "country", "status"]:
                texts.append(
                    f"{table_name}.{col['name']} represents {col['name'].replace('_', ' ')}"
                )

        # JOIN relationships (IMPORTANT)
        for rel in table["relationships"]:
            texts.append(
                f"Table {table_name} joins {rel['to_table']} ON "
                f"{table_name}.{rel['from_column']} = "
                f"{rel['to_table']}.{rel['to_column']}"
            )

            texts.append(
                f"Join condition: {table_name}.{rel['from_column']} = "
                f"{rel['to_table']}.{rel['to_column']}"
            )

    # HARDCODED SQL HINTS (game changer)
    texts.append(
        "To find orders from a specific country, join orders and customers using "
        "orders.customer_id = customers.id and filter customers.country"
    )

    texts.append(
        "To calculate revenue, use orders.total_amount"
    )

    texts.append(
        "To find customers without orders, use NOT EXISTS with orders.customer_id"
    )

    texts.append(
        "orders.customer_id = customers.id is used to join orders with customers"
    )
    
    texts.append(
        "order_items.product_id = products.id is used to join order_items with products"
    )

    return texts


if __name__ == "__main__":
    schema = get_schema()
    texts = schema_to_text(schema)

    with open(os.path.join(DATA_DIR, "schema.json"), "w") as f:
        json.dump(schema, f, indent=2)

    with open(os.path.join(DATA_DIR, "schema_texts.txt"), "w", encoding="utf-8") as f:
        for t in texts:
            f.write(t + "\n\n")

    print("Schema and texts saved successfully.")