# Name: Ariel Gutierrez
# Student ID: 2318163
# Email: arigutierrez@chapman.edu
# Course and Section: 408-01
# Assignment: Final Project

import mysql.connector

class db_operations():
    def __init__(self, host, user, password): # constructor with connection path to db
        self.connection = mysql.connector.connect(host=host, user=user, password=password)
        self.cursor = self.connection.cursor(buffered=True)
        self.cursor.execute("USE cpsc408")
        print("connection made to cloud instance..")

    # function that executes multiple queries
    def single_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as e:
            print("duplicates found..")
            print("creating table failed..")


    # function that executes a query with placeholders
    def single_execute(self, query, id):
        try:
            self.cursor.execute(query,id)
            self.connection.commit()
            return self.cursor.fetchone()
        except mysql.connector.Error as e:
            print(e)
            print("duplicates found..")
            print("loading into table failed..")

    # function that executes a query with placeholders
    def single_execute_placeholder(self, query, id):
        try:
            self.cursor.execute(query,id)
            self.connection.commit()
            self.cursor.fetchone()
        except mysql.connector.Error as e:
            print(e)
            print("duplicates found..")
            print("loading into table failed..")

    # multi = True
    def single_execute_placeholder_multi(self, query, id):
        try:
            self.cursor.execute(query,id, multi=True)
            self.connection.commit()
            self.cursor.fetchone()
        except mysql.connector.Error as e:
            print(e)
            print("duplicates found..")
            print("loading into table failed..")

    # function to return all data from a query
    def data_records(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # function to return a single value from table
    def single_record(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()

    # function to return a single attribute values from table
    def single_attribute(self,query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        #results.remove(None)
        return results

    # function to return a single attribute value from table
    def single_attr(self, query, num):
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        result = result[num]
        return result

    # function that checks if a table exists in mySQL
    def table_exists(self, table):
        query = "SHOW TABLES"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if (table,) in results:
            return True
        else:
            return False

    # close connection
    def destructor(self):
        self.connection.close()
        print("connection closed...")
