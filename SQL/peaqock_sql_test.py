import sqlite3
from datetime import datetime, timedelta
import pandas as pd


# funtion to read the data in the tables to have an idea about what are we dealing with 

def show_data_table(table_name):
    #  Connect to the database
    connection = sqlite3.connect('peaqock.db')
    cursor = connection.cursor()

    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        column_names = [column[1] for column in columns_info]
        print(column_names)

        cursor.execute(f'select * from {table_name}')
        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=column_names)
        df = pd.DataFrame(rows)

        print(df)
    except sqlite3.Error as Error:
        print(Error)

    finally:
        cursor.close()
        connection.close()


table_name_1 = 'ImputationsEspeces'
table_name_2 = 'ComptesEspece'
table_name_3 = 'Clients'


# show_data_table(table_name_1)


# ///////////////////////////////////////////////////////
# //////////////////////////////////////////////////////

# Detect the clients who have made suspicious transactions

# C_W_S = clients with suspicious
def c_w_s_transactions(X, specific_date):
    # connect to the sqlite
    connection = sqlite3.connect('peaqock.db')
    cursor = connection.cursor()

    try:
        # python code to calcule te limit date for last 36 months
        # get back by three years from the the date we passed as parameters
        # Three_Years_Ago = last 36 momths

        Last_36_Months = (datetime.strptime(specific_date, '%d-%m-%Y') - timedelta(days=36 * 30)).strftime('%Y-%m-%d')
        specific_date = datetime.strptime(specific_date, '%d-%m-%Y').strftime('%Y-%m-%d')

        print(f"the last 36 months date:{Last_36_Months}")
        print(f'the given date: {specific_date}')


        #  calculate average monthly volume over the last 36 months
        query_avg = """
            SELECT C_Espece.IdClient, AVG(Impu_Especes.Montant) AS average_monthly_volume
            FROM ImputationsEspeces AS Impu_Especes
            INNER JOIN ComptesEspece AS C_Espece ON C_Espece.IdCompte = Impu_Especes.IdCompteEspece
            WHERE Impu_Especes.Sens = 0 AND Impu_Especes.Nature = 'F' AND Impu_Especes.DateEtat >= ? AND Impu_Especes.DateEtat <= ?
            GROUP BY C_Espece.IdClient
        """
        # execute the query_avg
        cursor.execute(query_avg, (Last_36_Months, specific_date))
        # print(cursor.fetchall())
        resultats_avgs = dict(cursor.fetchall())

        # print(resultats_avgs)

        
        # we want to detect clients with a transaction amount greater than or equal to X times the average
        query_suspect = """
            SELECT
                Cln.IdPersonne,
                Cln.RaisonSociale,
                C_Espece.IdClient,
                SUM(Impu_Especes.Montant) AS V_Transaction
            FROM
                Clients AS Cln
                JOIN ComptesEspece AS C_Espece ON Cln.IdPersonne = C_Espece.IdClient
                JOIN ImputationsEspeces AS Impu_Especes ON C_Espece.IdCompte = Impu_Especes.IdCompteEspece
            WHERE
                Impu_Especes.Sens = 0
                AND Impu_Especes.Nature = 'F'
                AND Impu_Especes.DateEtat BETWEEN ? AND ? 
                AND C_Espece.IdClient = ?
            GROUP BY
                Cln.IdPersonne,
                Cln.RaisonSociale,
                C_Espece.IdClient
            HAVING
                V_Transaction >= ?
        """

        # show suspicious clients
        print("Clients who have conducted suspicious transactions:")

        for id_client, average_monthly_volume in resultats_avgs.items():
            cursor.execute(query_suspect, (Last_36_Months, specific_date, id_client, X * average_monthly_volume))
            suspicious_Clients = cursor.fetchall()

            if suspicious_Clients:
                for row in suspicious_Clients:
                    print(f"ID Client: {row[0]}, Raison Sociale: {row[1]}, Transaction Volume: {row[3]}")

    except sqlite3.Error as error:
        print(f"SQLite Error : {error}")

    finally:
        # close the connection
        connection.close()


# test X=2 et Date='01-09-2005' 
c_w_s_transactions(X=2, specific_date='01-09-2005')

# in order to see more clients change the date and x see the example below

# test X=5 et Date='01-09-2010'
# c_w_s_transactions(X=5, specific_date='01-09-2010')




