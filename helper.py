# Name: Ariel Gutierrez
# Student ID: 2318163
# Email: arigutierrez@chapman.edu
# Course and Section: 408-01
# Assignment: Final Project

# module contains miscellaneous functions
import datetime
import os.path
from tabulate import tabulate

class helper():
    # function parses a string and converts to appropriate type
    @staticmethod
    def convert(value):
        types = [int,float,str] # order needs to be this way
        if value == '':
            return None
        for t in types:
            try:
                return t(value)
            except:
                pass

    # function reads file path to clean up data file. Returns a list of tuples,
    # where each tuple is a row of data in the csv file
    @staticmethod
    def data_cleaner(path):
        with open(path,"r",encoding="utf-8") as f:
            data = f.readlines()

        data = [i.strip().split(",") for i in data]
        data_cleaned = []
        for row in data[:]:
            row = [helper.convert(i) for i in row]
            data_cleaned.append(tuple(row))
        return data_cleaned

    # function prints a list of strings nicely
    @staticmethod
    def pretty_print(lst):
        print("Results..")
        for i in lst:
            print(i)
        print("")

    # function prints a row with corresponding attributes for option 1
    @staticmethod
    def row_print(tup):
        # prints county stats for the date
        print("----------------------RESULTS---------------------")
        print("County: "+str(tup[0]))
        print("Date: "+ str(tup[1]))
        print()
        print("Daily Stats:")
        print("Partially Vaccinated: "+ str(tup[2]))
        print("Fully Vaccinated: "+ str(tup[4]))
        print("Booster Shots: "+ str(tup[6]))
        print()
        print("Totals:")
        print("Partially Vaccinated: "+ str(tup[3]))
        print("Fully Vaccinated: "+ str(tup[5]))
        print("Booster Shots: "+ str(tup[7]))
        print()
        print("Vaccine Type Daily Stats:")
        print("Pfizer: "+ str(tup[8]))
        print("Moderna: "+ str(tup[9]))
        print("Johnson & Johnson: "+ str(tup[10]))
        print("------------------END OF RESULTS-----------------")

    # function prints a table with corresponding attributes for option 5
    @staticmethod
    def table_print(lt, header):
        lt.insert(0,header)
        print(tabulate(lt, headers = 'firstrow', tablefmt = 'grid', floatfmt='.10g'))


    # function checks for user input given a list of choices
    @staticmethod
    def get_choice(lst):
        choice = input("Enter choice number: ")
        while choice.isdigit() == False:
            print("Incorrect option. Try again")
            choice = input("Enter choice number: ")

        while int(choice) not in lst:
            print("Incorrect option. Try again")
            choice = input("Enter choice number: ")
        return int(choice)

    # function that checks if user input matches date format
    @staticmethod
    def get_date_format():
        new_value = input("Enter the date of the record (format: YYYY-MM-DD): ")
        while True:
            try:
                date = datetime.datetime.strptime(new_value, "%Y-%m-%d")
                return new_value
            except ValueError as err:
                print("Incorrect format. Try again.")
                new_value = input("Enter the date of the record (format: YYYY-MM-DD): ")
