# Name: Ariel Gutierrez
# Student ID: 2318163
# Email: arigutierrez@chapman.edu
# Course and Section: 408-01
# Assignment: Final Project


# imports
from helper import helper
from db_operations import db_operations
import csv

# connection to cloud instance
db_ops = db_operations(host="35.222.150.170", user="root", password="D@rkB3ach")


def start_screen():
    print("\n\nWelcome to the California COVID Vaccination Progress Dashboard!\n")


# show user options
def options():
    print("\nSelect from the following menu options:\n1 Find county record\n" \
    "2 Modify county total doses\n3 Delete county record\n4 Create county record " \
    "\n5 View demographic statistics\n6 View all county statistics \n7 Exit\n")
    return helper.get_choice([1,2,3,4,5,6,7])


# function that returns -1 if value is in table, else returns the ID
def in_table(value, table, condition):
    query = "SELECT "+value+" FROM "+table+" WHERE "+condition
    if (db_ops.single_record(query) == None):
        return -1
    else:
        return (db_ops.single_attr(query, 0))

# function that finds the most recent county record
def find_county_record():
    query = '''
    SELECT DISTINCT name
    FROM county;
    '''
    print("Counties in database:")

    counties = db_ops.single_attribute(query)
    # show counties in table, also create dictionary for choices
    choices = {}
    for i in range(len(counties)):
        print(i,counties[i])
        choices[i] = counties[i]
    index = helper.get_choice(choices.keys()) +1

    # prepare query and show results for county with closest date
    query = """SELECT c.name, cd.adminDate, cd.partiallyVaccinated,
    cd.cumulativePartiallyVaccinated, cd.fullyVaccinated,
    cd.cumulativeFullyVaccinated, cd.boosterCount,
    cd.cumulativeBoosterCount, cv.pfizerDoses, cv.modernaDoses, cv.jj_doses
    FROM county AS c
    INNER JOIN countyData AS cd
    ON c.countyID = cd.countyID
    INNER JOIN countyVaccineType as cv
    ON cv.countyID = c.countyID AND
    cv.countyID = cd.countyID AND
    cv.id = cd.id
    WHERE c.countyID = """+str(index)+"""
    AND cd.flag = 0
    ORDER BY adminDate DESC LIMIT 1;
    """
    helper.row_print(db_ops.single_record(query))


# function that modifies the most recent county record
def modify_county_record():
    query = '''
    SELECT DISTINCT name
    FROM county;
    '''
    print("Counties in database:")

    counties = db_ops.single_attribute(query)
    # show counties in table, also create dictionary for choices
    choices = {}
    for i in range(len(counties)):
        print(i,counties[i])
        choices[i] = counties[i]
    index = helper.get_choice(choices.keys()) +1

    # prompt for new daily total
    new_value = input("Enter the new daily total: ")
    while new_value.isdigit() == False:
        print("Error. Insert an integer value.")
        new_value = input("Enter the new daily total: ")

    query = "SELECT adminDate FROM countyData WHERE countyID ="+str(index)+" AND flag = 0 ORDER BY adminDate DESC LIMIT 1;"
    date = db_ops.single_record(query)[0]

    query = """
    UPDATE countyData SET totalDoses = %s
    WHERE countyID = %s and adminDate = %s;"""

    id = (new_value, index, date)
    db_ops.single_execute(query,id)
    print("----------------UPDATE COMPLETE-----------------\n")


# function that deletes a record from the countyData and countyVaccineType
def delete_county_record():
    # prompt for which county they want to delete from
    query = '''
    SELECT DISTINCT name
    FROM county;
    '''
    print("Counties in database:")

    counties = db_ops.single_attribute(query)
    # show counties in table, also create dictionary for choices
    choices = {}
    for i in range(len(counties)):
        print(i,counties[i])
        choices[i] = counties[i]
    index = helper.get_choice(choices.keys()) +1

    # prompt for date they want to delete, if not in database, then reprompt for date
    date = helper.get_date_format()
    while True:
        query = """
            SELECT *
            FROM countyData
            WHERE countyID = %s AND adminDate = %s AND flag = 0;"""
        id = (index, date)
        result = db_ops.single_execute(query, id)
        if result != 0:
            break

    query = """
        START TRANSACTION;
        UPDATE countyData SET flag = 1
        WHERE countyID = %s and adminDate = %s;
        UPDATE countyVaccineType SET flag = 1
        WHERE countyID = %s;
        COMMIT;"""
    id = (index,date,index)
    db_ops.single_execute_placeholder_multi(query, id)
    # delete from county vaccine type using the id.
    print("-----------------RECORD DELETED-----------------\n")


def create_county_record():
    # prompt for which county they want to create a record for
    query = '''
    SELECT DISTINCT name
    FROM county;
    '''
    print("Counties in database:")

    counties = db_ops.single_attribute(query)
    # show counties in table, also create dictionary for choices
    choices = {}
    for i in range(len(counties)):
        print(i,counties[i])
        choices[i] = counties[i]
    index = helper.get_choice(choices.keys())+1

    date = helper.get_date_format()

    totalDoses = input("Total doses for the day: ")
    while totalDoses.isdigit() == False:
        totalDoses = input("Total doses for the day: ")

    partiallyVaccinated = input("Total partially vaccinated doses for the day: ")
    while partiallyVaccinated.isdigit() == False:
        partiallyVaccinated = input("Total partially vaccinated doses for the day: ")
    partiallyVaccinated = int(partiallyVaccinated)

    query = " SELECT SUM(partiallyVaccinated) FROM countyData WHERE countyID = "+str(index)+" AND flag = 0;"
    cumPV = db_ops.single_record(query)

    fullyVaccinated = input("Total fully vaccinated doses for the day: ")
    while fullyVaccinated.isdigit() == False:
        fullyVaccinated = input("Total fully vaccinated doses for the day: ")
    fullyVaccinated = int(fullyVaccinated)

    query = " SELECT SUM(fullyVaccinated) FROM countyData WHERE countyID = "+str(index)+" AND flag = 0;"
    cumFV = db_ops.single_record(query)

    booster = input("Total booster doses for the day: ")
    while booster.isdigit() == False:
        booster = input("Total booster doses for the day: ")
    booster = int(booster)

    query = " SELECT SUM(boosterCount) FROM countyData WHERE countyID = "+str(index)+" AND flag = 0;"
    cumBoost = db_ops.single_record(query)

    pfizer = input("Total Pfizer doses for the day: ")
    while pfizer.isdigit() == False:
        pfizer = input("Total Pfizer doses for the day: ")
    pfizer = int(pfizer)

    moderna = input("Total Moderna doses for the day: ")
    while moderna.isdigit() == False:
        moderna = input("Total Moderna doses for the day: ")
    moderna = int(moderna)

    jj = input("Total Johnson&Johnson doses for the day: ")
    while jj.isdigit() == False:
        jj = input("Total Johnson&Johnson doses for the day: ")
    jj = int(jj)

    query = """
        START TRANSACTION;
        INSERT INTO countyData(countyID, adminDate, totalDoses,
            partiallyVaccinated, cumulativePartiallyVaccinated,
            fullyVaccinated, cumulativeFullyVaccinated, boosterCount,
            cumulativeBoosterCount, flag)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        INSERT INTO countyVaccineType(countyID, pfizerDoses, modernaDoses, jj_doses, flag)
        VALUES (%s,%s,%s,%s,%s);
        COMMIT;

        ;"""
    id = (index,date,totalDoses,partiallyVaccinated,cumPV[0],fullyVaccinated,cumFV[0],booster,cumBoost[0],0,index,pfizer,moderna,jj,0)
    db_ops.single_execute_placeholder_multi(query, id)
    print("-----------------RECORD CREATED-----------------\n")

def demographic_stats():
    # prompt for which demographic they would like to view
    query = '''
    SELECT DISTINCT category
    FROM demographic;
    '''
    print("Demographics in Database:")

    demos = db_ops.single_attribute(query)
    # show counties in table, also create dictionary for choices
    choices = {}
    for i in range(len(demos)):
        print(i,demos[i])
        choices[i] = demos[i]
    index = helper.get_choice(choices.keys())

    query = """
        SELECT d.categoryValue, SUM(totalDoses), SUM(partiallyVaccinated), SUM(fullyVaccinated)
        FROM demographic AS d
        INNER JOIN demographicData AS dd ON d.demographicID = dd.demographicID
        WHERE d.demographicID IN (SELECT demographicID
	    FROM demographic
	    WHERE category = '"""+str(choices[index])+"""') AND flag = 0
        GROUP BY categoryValue;"""
    data = db_ops.data_records(query)
    print("----------------------------------------------------RESULTS---------------------------------------------------\n")
    helper.table_print(data,("Category","Total Doses", "Partially Vaccinated", "Fully Vaccinated"))
    print("\n------------------------------------------------END OF RESULTS----------------------------------------------\n")


    while True:
        userInput = input("Would you like a csv file of the table? (y/n): ")
        if userInput == "y":
            # Create the csv file
            fileName = str(choices[index]).replace(" ", "") + "demographicStats.csv"
            with open(fileName, 'w', newline='') as f_handle:
                writer = csv.writer(f_handle)
                # Add the header/column names
                header = ['Category', 'Total Doses', 'Partially Vaccinated', 'Fully Vaccinated']
                #writer.writerow(header)
                # Iterate over `data`  and  write to the csv file
                for row in data:
                    writer.writerow(row)
            break
        elif userInput == "n":
            break
        else:
            print("Incorrect input. Try again.")



def all_county_stats():
    # print out current whole of california stats
    query = """
    SELECT * FROM vCumulativeCountyVaccineTotals;
    """
    data = db_ops.data_records(query)
    print("------------------------------------------------------------------------------------RESULTS-----------------------------------------------------------------------------------\n")
    helper.table_print(data,("County","Total Partially Vaccinated", "Total Fully Vaccinated", "Total Booster Count", "Total Pfizer", "Total Moderna", "Total Johnson&Johnson"))
    print("\n--------------------------------------------------------------------------------END OF RESULTS------------------------------------------------------------------------------\n")

    while True:
        userInput = input("Would you like a csv file of the table? (y/n): ")
        if userInput == "y":
            # Create the csv file
            with open('countyStats.csv', 'w', newline='') as f_handle:
                writer = csv.writer(f_handle)
                # Add the header/column names
                header = ["County","Total Partially Vaccinated", "Total Fully Vaccinated", "Total Booster Count", "Total Pfizer", "Total Moderna", "Total Johnson&Johnson"]
                #writer.writerow(header)
                # Iterate over `data`  and  write to the csv file
                for row in data:
                    writer.writerow(row)
            break
        elif userInput == "n":
            break
        else:
            print("Incorrect input. Try again.")



# main program
start_screen()
while True:
    user_choice = options()
    if user_choice == 1:
        find_county_record()
    elif user_choice == 2:
        modify_county_record()
    elif user_choice == 3:
        delete_county_record()
    elif user_choice == 4:
        create_county_record()
    elif user_choice == 5:
        demographic_stats()
    elif user_choice == 6:
        all_county_stats()
    elif user_choice == 7:
        print("\n\nThank you for using the California COVID Vaccination Progress Dashboard!")
        print("Get vaccinated!")
        print("Goodbye!")
        break
