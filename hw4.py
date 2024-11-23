import sys
from idlelib.window import ListedToplevel

from data import CountyDemographics
from typing import Optional
import county_demographics
import build_data

def display(dataset : list[CountyDemographics])->None:
    for county in dataset:
        print("{}, {}".format(county.county, county.state))
        print("\tPopulation: {}".format(county.population["2014 Population"]))
        print("\tAge: ")
        for key in county.age.keys():
            print("\t\t{}: {}%".format(key,county.age[key]))
        print("\tEducation: ")
        for key in county.education.keys():
            print("\t\t{}: {}%".format(key,county.education[key]))
        print("\tEthnicity Percentages")
        for key in county.ethnicities.keys():
            print("\t\t{}: {}%".format(key,county.ethnicities[key]))
        print("\tIncome")
        for key in county.income.keys():
            print("\t\t{}: {}%".format(key,county.income[key]))

demographics: list[CountyDemographics] = build_data.get_data()
if len(sys.argv) == 0:
    print("No arguments when 1 was expected")
    sys.exit()
file_name = sys.argv[1]


try:
    with (open(sys.argv[1], "r") as operation):
        operation_cont: list[str] = operation.readlines()
        new_data = []

        for i in range(len(operation_cont)):
            current_line = operation_cont[i].strip("\n")
            operation_param: list[str] = operation_cont[i].split(":")

            if len(operation_param) > 3:
                print("Error: Too many inputs")
                continue

            if i == 0:
                print(str(len(demographics)), " records loaded")
            if "filter-state" == operation_param[0]:
                state = operation_param[1].strip("\n")
                try:
                    for county in demographics:
                        if county.state == state.strip("\n"):
                            new_data.append(county)
                    print("Filter: state == ", state, "(", str(len(new_data)), "entries)")
                except KeyError:
                    print("Line:" , i+1, "is not formatted correctly")
            
            if "filter-gt" == operation_param[0]:
                field = operation_param[1]
                val = operation_param[2]
                fields = field.split(".")
                if val.strip("\n").isdigit() == False:
                    print("Line: ", i+1, "is not formatted correctly")
                    continue
                if (float(val) > 0 and float(val) < 100) and len(fields) == 2 and (fields[0] == "Education" or "Ethnicities" or "Income"):
                    try:
                        for county in demographics:
                            if fields[0] == "Education":
                                if county.education[fields[1]] > float(val):
                                    new_data.append(county)
                            elif fields[0] == "Ethnicities":
                                if county.ethnicities[fields[1]] > float(val):
                                    new_data.append(county)
                            elif fields[0] == "Income":
                                if county.income[fields[1]] > float(val):
                                    new_data.append(county)
                            else:
                                print("Incorrect Field")
                        print("Filter: ", str(field), val, "(", str(len(new_data)), "entries)")
                    except KeyError:
                        print("Line: ", i+1, "is not formatted correctly")
                        continue
                else:
                    print("Line: ", i+1, "is not formatted correctly")
                    continue

            if "filter-lt" == operation_param[0]:
                val = operation_param[2]
                field = operation_param[1]
                fields = field.split(".")
                try:
                    if (float(val) > 0 and float(val) < 100) and len(fields) == 2 and (fields[0] == "Education" or "Ethnicities" or "Income"):
                        try:
                            for county in demographics:
                                if fields[0] == "Education":
                                    if county.education[fields[1]] < float(val):
                                        new_data.append(county)
                                elif fields[0] == "Ethnicities":
                                    if county.ethnicities[fields[1]] < float(val):
                                        new_data.append(county)
                                elif fields[0] == "Income":
                                    if county.income[fields[1]] < float(val):
                                        new_data.append(county)
                                else:
                                    print("Invalid Field")
                            print("Filter: ", str(field), val, "(", str(len(new_data)), "entries)")
                        except KeyError:
                            print("Line: ", i+1, " is not formatted correctly")
                    else:
                        print("Line: ", i+1, " is not formatted correctly")
                        continue
                except:
                    print("Line: ", i+1, " is not formatted correctly")
                    continue


            if "population-total" == current_line:
                total = 0
                if len(new_data) > 0:
                    for county in new_data:
                        total += county.population["2014 Population"]
                else:
                    for county in demographics:
                        total += county.population["2014 Population"]
                print("2014 Population: ", str(total))

            if "population" == operation_param[0]:
                pop = 0
                field = operation_param[1].strip("\n")
                fields = field.split(".")
                fields[1] = fields[1].strip("\n")
                if len(operation_param) == 2:
                    try:
                        if new_data:
                            for county in new_data:
                                county_pop = county.population["2014 Population"]
                                if fields[0] == "Education":
                                    pop +=(county_pop * county.education[fields[1]]) / 100
                                elif fields[0] == "Ethnicities":
                                    pop +=(county_pop * county.ethnicities[fields[1]]) / 100
                                elif fields[0] == "Income":
                                    pop +=(county_pop * county.income[fields[1]]) / 100
                                else:
                                    print("Invalid Field")
                        else:
                            for county in demographics:
                                county_pop = county.population["2014 Population"]
                                if fields[0] == "Education":
                                    pop += (county_pop * county.education[fields[1]]) / 100
                                elif fields[0] == "Ethnicities":
                                    pop += (county_pop * county.ethnicities[fields[1]]) / 100
                                elif fields[0] == "Income":
                                    pop += (county_pop * county.income[fields[1]]) / 100
                                else:
                                    print("Invalid Field")
                        print("2014", field, "population", str(pop))
                    except KeyError:
                        print("Line: " , i+1, " is not formatted correctly")
                        continue
                else:
                    print("Line: ", i+1, " is not formatted correctly")
            if "percent" == operation_param[0]:
                pop = 0
                total_pop = 0
                field = operation_param[1].strip("\n")
                fields = field.split(".")
                fields[1] = fields[1].strip("\n")
                if len(operation_param) == 2:
                    try:
                        if new_data:
                            for county in new_data:
                                county_pop = county.population["2014 Population"]
                                total_pop += county_pop
                                if fields[0] == "Education":
                                    pop += (county_pop * county.education[fields[1]]) / 100
                                elif fields[0] == "Ethnicities":
                                    pop += (county_pop * county.ethnicities[fields[1]]) / 100
                                elif fields[0] == "Income":
                                    pop += (county_pop * county.income[fields[1]]) / 100
                                else:
                                    print("Invalid Field")
                        else:
                            for county in demographics:
                                county_pop = county.population["2014 Population"]
                                total_pop += county_pop
                                if fields[0] == "Education":
                                    pop += (county_pop * county.education[fields[1]]) / 100
                                elif fields[0] == "Ethnicities":
                                    pop += (county_pop * county.ethnicities[fields[1]]) / 100
                                elif fields[0] == "Income":
                                    pop += (county_pop * county.income[fields[1]]) / 100
                                else:
                                    print("Invalid Field")
                        print("2014", field, "percentage", (pop/total_pop)*100)
                    except KeyError:
                        print("Line: ", i+1, "is not formatted correctly")
                        continue
                else:
                    print("Line: ", i+1, " is not formatted correctly")

            if "display" == current_line:
                if new_data:
                    display(new_data)







except IOError as e:
    print("Error: ", e)
except IndexError as e:
    print("Error: ", e)
