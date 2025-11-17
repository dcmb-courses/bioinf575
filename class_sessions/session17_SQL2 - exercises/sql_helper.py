# import pandas so you can see the select results as a dataframe
import pandas as pd

def run_select_query(query, cursor):
    cursor.execute(query)
    data_header = [t[0] for t in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns = data_header)
    return df
    
def check_master_table(cursor):
    select_master = "SELECT name, type FROM sqlite_master;"
    return run_select_query(select_master, cursor)

def run_create_table(sql, cursor, connection):
        cursor.execute(sql)
        connection.commit()