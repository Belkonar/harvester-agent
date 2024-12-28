from typing import List
import psycopg
from psycopg.rows import dict_row
from itertools import chain
import requests

source_id = 'DFD8FC59-38A8-4F2C-8785-8032C610AC06'
nonce = '2CACC19A-F679-44FF-A4CE-998FD323C49C'

def chunk(lst, size):
    skip = 0
    while True:
        bucket = lst[skip:skip+size]
        if len(bucket) == 0:
            break

        yield bucket
        skip = skip + size

def get_dbs(conn_str) -> List[str]:
    sql_db_list = """
    SELECT datname FROM pg_database
        WHERE datistemplate = false AND datname != 'postgres';
    """

    with psycopg.connect(conn_str, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(sql_db_list)

            return [x["datname"] for x in cur.fetchall()]


def get_fields(conn_str):
    sql = """
    SELECT
        table_catalog || '.' || table_schema || '.' || table_name as table,
        table_schema || '.' || table_name as short_name,
        "column_name", "data_type"
    FROM information_schema.columns
    WHERE
        table_catalog != 'postgres' AND
        NOT table_schema IN ('pg_catalog', 'information_schema');
    """

    with psycopg.connect(conn_str, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)

            return cur.fetchall()

conn_str = "host=localhost dbname={} user=postgres password=garden"
dbs = get_dbs(conn_str.format("postgres"))

all_fields = list(chain.from_iterable((get_fields(conn_str.format(x)) for x in dbs)))
json_fields = [x for x in all_fields if x["data_type"] == "jsonb"]
print(json_fields)

source_req = {
    "id": source_id,
    "name": "test-source"
}

tables_req = {
    "source": source_id,
    "nonce": nonce,
    "names": list(set(x["table"] for x in all_fields))
}

formatted_fields = [{
    "name": x["column_name"],
    "table": x["table"],
    "subfield": False,
    "types": [x["data_type"]]
} for x in all_fields]

fields_req = {
    "source": source_id,
    "nonce": nonce,
    "fields": formatted_fields
}

exit(0)

requests.put("http://localhost:3030/source", json=source_req)
resp = requests.put("http://localhost:3030/tables", json=tables_req)

for fields_chunk in chunk(formatted_fields, 50):
    req = {
        "source": source_id,
        "nonce": nonce,
        "fields": fields_chunk
    }

    resp = requests.put("http://localhost:3030/fields", json=req)
    print(resp.json())

print(resp.text)

