import sqlite3
from datetime import datetime

# prepare variable
connection_path = '/Users/Pathompong/Library/Mobile Documents/com~apple~CloudDocs/Database/my_finance.db'
table  = datetime.now().strftime('%B')
date   = datetime.now().strftime('%d/%m/%y')
bank   = 3786
wallet = 1675

def insert_data(table, date, bank, wallet):
    connection = sqlite3.connect(connection_path)
    cursor = connection.cursor()

    # check if it has the table
    try:
        cursor.execute("""--sql
                    SELECT ID from {};
                    """.format(table))
    except:
        cursor.execute("""--sql
                    CREATE TABLE {} 
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    date TEXT, bank NUMERIC, wallet NUMERIC, 
                    bank_dif NUMERIC, wallet_dif NUMERIC, total_dif NUMERIC);
                    """.format(table))
        
    # read table - check latest id
    cursor.execute("""--sql
                SELECT ID, bank, wallet FROM {}
                ORDER by ID DESC
                """.format(table))
    rows = cursor.fetchmany(2)
    if not rows: id = 0         # if empty, start with 0
    else: id = rows[0][0] + 1   # if has data, increase id

    # calculate difference
    if len(rows) == 2:          # if it has 2 rows that can find difference
        bank_dif   = bank - rows[0][1]
        wallet_dif = wallet - rows[0][2]
        total_dif  = bank_dif + wallet_dif
    else:
        bank_dif   = 0
        wallet_dif = 0
        total_dif  = 0

    # add item to table
    cursor.execute("""--sql
                INSERT INTO {} (ID, date, bank, wallet, bank_dif, wallet_dif, total_dif)
                VALUES ({}, '{}', {}, {}, {}, {}, {});
                """.format(table, id, date, bank, wallet, bank_dif, wallet_dif, total_dif))
    connection.commit()

    # get sum of each differences
    cursor.execute("""--sql
                SELECT SUM(bank_dif), SUM(wallet_dif), SUM(total_dif) FROM {}
                """.format(table))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows[0][0], rows[0][1], rows[0][2]

def show_sum(total_bank, total_wallet, grand_total):
    print('=====================================')
    print('Total bank spending:   ', total_bank, 'THB')
    print('Total wallet spending: ', total_wallet, 'THB')
    print('-------------------------------------')
    print('Total spending:        ', grand_total, 'THB')
    print('=====================================')

t_bank, t_wallet, g_total = insert_data(table, date, bank, wallet)
show_sum(t_bank, t_wallet, g_total)