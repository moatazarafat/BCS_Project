from datetime import datetime
import string
import json
import random
import Travel_data
import pandas
import os   

class Person:
    def __init__(self,name,age,nationality):
        self.__name = name
        self.__age = age
        self.__nationality = nationality

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @property
    def nationality(self):
        return self.__nationality

    def display_info(self):
        print("--- Person Details ---")
        print(f"Person's Name        : {self.name}")
        print(f"Person's Age         : {self.age}")
        print(f"Person's Nationality : {self.nationality}")

    def update_information(self,new_name,new_age,new_nationality):
        self.__name = new_name
        self.__age = new_age
        self.__nationality = new_nationality

class Passport:
    def __init__(self,passport_number,issue_country,expiry_date):
        self.__passport_number = passport_number
        self.__issue_country = issue_country
        self.__expiry_date = expiry_date

    @property
    def passport_number(self):
        return self.__passport_number

    @property
    def issue_country(self):
        return self.__issue_country

    @property
    def expiry_date(self):
        return self.__expiry_date

    def display_passport(self):
        print("--- Passport Details ---")
        print(f"Passport Number : {self.passport_number}")
        print(f"Issue Country   : {self.issue_country}")
        print(f"Expiry Data     : {self.expiry_date}")
        print(f"Is Forged?      : {self.detect_forgery()}")

    def check_expiry(self):
        now = datetime.today()
        if now > self.expiry_date :
            print("Passport Expired")
            return True
        else:
            return False

    def validate_passport(self):
        if (not self.check_expiry()) and (not self.detect_forgery()):
            print("Valid Passport")
            return True
        else:
            print("Invalid Passport")
            return False

    def detect_forgery(self):
        if (len(self.passport_number) != 9 ) or self.__passport_number[0] not in string.ascii_uppercase:
            return True
        else:
            return False

class Visa:
    def __init__(self,visa_type,expiry_date_visa,country):
        self.__visa_type = visa_type
        self.__expiry_date_visa = expiry_date_visa
        self.__country = country

    @property
    def visa_type(self):
        return self.__visa_type

    @property
    def expiry_date_visa(self):
        return self.__expiry_date_visa

    @property
    def country(self):
        return self.__country

    def display_visa(self):
        print(f"Visa Type   : {self.visa_type}")
        print(f"Expiry Date : {self.expiry_date_visa}")
        print(f"Country     : {self.country}")
        print(f"Is Valid    : {self.validate_visa()}")

    def check_expiry(self):
        now = datetime.today()
        if now > self.expiry_date_visa:
            print("Visa Expired")
            return True
        else:
            return False

    def validate_visa(self):
        if not self.check_expiry() :
            print("Valid Visa")
            return True
        else:
            print("Invalid Visa")
            return False

class Traveler(Person):
    def __init__(self,name,age,nationality,passport=None,visa=None):
        super().__init__(name,age,nationality)
        self.__passport = passport
        self.__visa = visa

    @property
    def passport(self):
        return self.__passport

    @property
    def visa(self):
        return self.__visa

    def display_traveler(self):
        super().display_info()
        if self.passport is not None :
            self.passport.display_passport()
        else:
            print("No Passport Provide")
        if self.visa is not None :
            self.visa.display_visa()
        else:
            print("No Visa Provide")

    def has_required_documents(self):
        if self.passport is None or self.visa is None :
            print("Does Not Has Required Documents")
            return False

        if (self.passport.validate_passport()) and (self.visa.validate_visa()):
            print("Has Required Documents")
            return True
        else:
            print("Does Not Has Required Documents")
            return False

class WantedList:
    def __init__(self,wanted_people):
        self.__wanted_people = wanted_people
    @property
    def wanted_people(self):
        return self.__wanted_people

    def load_data(self):
        with open("wanted_people.json","r") as file:
            data = json.load(file)
            self.__wanted_people = data["wanted_people"]

    def save_to_file(self):
        with open("wanted_people.json", "w") as file:
            json.dump({"wanted_people": self.__wanted_people}, file, indent=2)
        print("Wanted List Saved To File Successfully")
    def search_person(self,passport_number):
        for person in self.__wanted_people:
            if person["passport_number"] == passport_number:
                print("Wanted People Found")
                print(f"Name: {person['name']}")
                print(f"Passport Number: {person['passport_number']}")
                print(f"crime: {person['crime']}")
                return True
        print("Wanted People Not Found")
        return False

    def add_person(self,passport_number,name,crime):
        person={
            "passport_number": passport_number,
            "name": name,
            "crime": crime
        }
        self.__wanted_people.append(person)
        print("Person Added Successfully")

    def remove_person(self,passport_number):
        for person in self.__wanted_people:
            if person["passport_number"] == passport_number:
                self.__wanted_people.remove(person)
                print("Person Removed Successfully")
                return True
        print("person Not Found")
        return False

    def display_wanted_people(self):
        print("-------- Wanted List --------")
        for person in self.__wanted_people:
            print(f"Name: {person['name']}")
            print(f"Passport Number: {person['passport_number']}")
            print(f"Crime: {person['crime']}")
            print("-------------------------")


class Officer:
    def __init__(self,officer_name,employee_id):
        self.__officer_name = officer_name
        self.__employee_id = employee_id

    @property
    def officer_name(self):
        return self.__officer_name

    @property
    def employee_id(self):
        return self.__employee_id

    def display_officer(self):
        print("--- Officer Details ---")
        print(f"Officer's Name   : {self.officer_name}")
        print(f"Employee's ID    : {self.employee_id}")

    def update_officer_information(self,officer_name,employee_id):
        self.__officer_name = officer_name
        self.__employee_id = employee_id

    def inspect_passport(self,traveler):
        if traveler.passport is None :
            print("No Passport Found")
            return False
        return traveler.passport.validate_passport()

    def inspect_visa(self,traveler):
        if traveler.visa is None :
            print("No Visa Found")
            return False
        return traveler.visa.validate_visa()

    def check_wanted_list(self,traveler,wanted_list):
        if traveler.passport is None :
            return False
        return wanted_list.search_person(traveler.passport.passport_number)

    def check_entry(self,traveler,wanted_list):
        if self.check_wanted_list(traveler,wanted_list):
            self.arrest_traveler(traveler)
            return  "Arrested","on Wanted list"
        if traveler.has_required_documents()  and not self.check_wanted_list(traveler,wanted_list):
            return "Allowed","Valid documents"
        return "Rejected","Invalid documents"

    def arrest_traveler(self,traveler):
            print(f"{traveler.name} Has Been Arrested")



class Report:
    def __init__(self):
        self.operations = []

    def save_operation(self, traveler, status, reason):
        if traveler.passport is not None:
            passport = traveler.passport.passport_number
        else:
            passport = "No Passport"
        operation = {
            "name": traveler.name,
            "passport": passport,
            "status": status,
            "reason": reason,
            "time": str(datetime.now())        }
        self.operations.append(operation)
        print("Operation Saved Successfully")

    def generate_daily_report(self):

        print("========== Daily Report ==========")

        if len(self.operations) == 0:
            print("No Operations Today")
            return

        for operation in self.operations:
            print(f"Traveler Name   : {operation['name']}")
            print(f"Passport Number : {operation['passport']}")
            print(f"Status          : {operation['status']}")
            print(f"Reason          : {operation['reason']}")
            print("----------------------------------")

    def generate_final_report(self):
        if len(self.operations) == 0:
            print("No Operations")
            return

        df = pandas.DataFrame(self.operations)
        file_exists = os.path.exists("final_report.csv")
        df.to_csv("final_report.csv", mode="a", index=False, header=not file_exists, encoding="utf-8")
        print("Final Report Generated Successfully (CSV)")
    def show_statistics(self):

        allowed = 0
        rejected = 0
        arrested = 0

        for operation in self.operations:

            if operation["status"] == "Allowed":
                allowed += 1

            elif operation["status"] == "Rejected":
                rejected += 1

            elif operation["status"] == "Arrested":
                arrested += 1

        print("========== Statistics ==========")
        print(f"Total Operations : {len(self.operations)}")
        print(f"Allowed          : {allowed}")
        print(f"Rejected         : {rejected}")
        print(f"Arrested         : {arrested}")



class RandomEvent:
    def __init__(self):
        pass

    def generate_event(self):

        chance = random.randint(1,100)

        if chance > 15:
            return None

        event = random.randint(1,4)

        if event == 1:
            return "emergency"

        elif event == 2:
            return "scanner_failure"

        elif event == 3:
            return "diplomatic_arrival"

        else:
            return "suspicious_traveler"

    def emergency_alert(self):

        print("===== EMERGENCY ALERT =====")
        print("All Border Operations Have Been Stopped")

    def scanner_failure(self):

        print("===== SCANNER FAILURE =====")
        print("Manual Inspection Required")

    def diplomatic_arrival(self):

        print("===== DIPLOMATIC ARRIVAL =====")
        print("Priority Inspection")

    def suspicious_traveler(self):

        print("===== SUSPICIOUS TRAVELER =====")
        print("Extra Security Check Required")


class Database():
    def __init__(self,wanted_people):
        self.report = Report()
        self.wanted_list = WantedList(wanted_people)
    def save_data(self, traveler, status, reason):
        self.report.save_operation(traveler, status, reason)
        Travel_data.travelers=self.report.operations
    def load_data(self):
        print("====== SAVED DATA ======")
        for i in Travel_data.travelers:
            print(f"Traveler Name   : {i['name']}")
            print(f"Passport Number : {i['passport']}")
            print(f"Status          : {i['status']}")
            print(f"Reason          : {i['reason']}")
            print("="*20)

    def show_wanted(self):
        self.wanted_list.load_data()
        print("====== WANTED LIST ======")
        for i in self.wanted_list.wanted_people:
            print(f"Traveler Name   : {i['name']}")
            print(f"Passport Number : {i['passport_number']}")
            print(f"crime          : {i['crime']}")

    def del_add_wanted(self,passport_number,name,crime):
        self.wanted_list.add_person(passport_number,name,crime)
        self.wanted_list.remove_person(passport_number)
        with open("wanted_people.json","r") as file:
            data = json.load(file)

    def add_data(self,name1,passport1,status1,reason1):
        new_operatoion={
            "name":name1,
            "passport":passport1,
            "status":status1,
            "reason":reason1,
        }
        Travel_data.travelers.append(new_operatoion)
        self.report.operations.append(new_operatoion)
        print("Data Added Successfully")

    def update_wanted(self, passport_number, new_name, new_crime):
        self.wanted_list.remove_person(passport_number)
        self.wanted_list.add_person(passport_number, new_name, new_crime)
        self.wanted_list.save_to_file()


