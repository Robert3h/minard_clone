import pandas as pd
import sqlite3


class CreateMinardDB():
    def __init__(self):

        # STEP: Read TXT lines----------------------------------------------------
        with open("data/minard.txt") as f:   
            lines = f.readlines()   # type(lines) # <class 'list'>

        # STEP: Read TXT Headers----------------------------------------------------
        column_names = lines[2] # (lonc latc city$ lont temp days  date$   lonp  latp  surviv  direc$ division)
        column_names_list = column_names.split()    # ['(lonc', 'latc', 'city$', 'lont', 'temp', 'days', 'date$', 'lonp', 'latp', 'surviv', 'direc$', 'division),']

        # STEP: Clean TXT Headers----------------------------------------------------
        patterns_to_be_replaced = ["(", ")" ,"$"]
        adjust_column_names = []

        for column_name in column_names_list:
            for pattern in patterns_to_be_replaced:
                if pattern in column_name:
                    column_name = column_name.replace(pattern, "")  # ['lonc', 'latc', 'city', 'lont', 'temp', 'days', 'date', 'lonp', 'latp', 'surviv', 'direc', 'division,']
            adjust_column_names.append(column_name)

        # STEP: Divide Headers----------------------------------------------------
        self.column_names_city = adjust_column_names[0:3]            # ['lonc', 'latc', 'city']
        self.column_names_temperature = adjust_column_names[3:7]     # ['lont', 'temp', 'days', 'date']
        self.column_names_troop = adjust_column_names[7:]            # ['lonp', 'latp', 'surviv', 'direc', 'division,']
        self.lines = lines

    # STEP: Load data--city----------------------------------------------------
    def create_city_dataframe(self):    
        longitudes, latitudes, cities = [], [], []

        i = 6            # Starting row
        while i <= 25:   # Ending row
            long, lat, city = self.lines[i].split()[0:3] # Split first, select columns later
            longitudes.append(long)
            latitudes.append(lat)
            cities.append(city)
            i += 1

        city_data = (longitudes, latitudes, cities)

        city_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_city, city_data):
            city_df[column_name] = data

        return city_df

    # STEP: Load data--temperature----------------------------------------------------
    def create_temperature_dataframe(self):
        longitudes, temperatures, days, dates = [], [], [], []

        i = 6           # Starting row
        while i <= 14:  # Ending row
            long, temp, day, month, date = self.lines[i].split()[3:8] # Split first, select columns later
            longitudes.append(float(long))      
            temperatures.append(float(temp))    
            days.append(int(day))  

            if i == 10:
                date_str = "Nov 24" 
                dates.append(date_str)
            else:
                date_str = f"{month} {date}"             
                dates.append(date_str)

            i += 1 

        temperature_data = (longitudes, temperatures, days, dates)
                                # ([37.6, 36.0, 33.2, 32.0, 29.2, 28.5, 27.2, 26.7, 25.3], 
                                #  [0.0, 0.0, -9.0, -21.0, -11.0, -20.0, -24.0, -30.0, -26.0], 
                                #  [6, 6, 16, 5, 10, 4, 3, 5, 1], 
                                #  ['Oct 18', 'Oct 24', 'Nov 9', 'Nov 14', 'Nov 24', 'Nov 28', 'Dec 1', 'Dec 6', 'Dec 7'])
        
        temperature_df = pd.DataFrame()

        for column_name, data in zip(self.column_names_temperature, temperature_data):
            temperature_df[column_name] = data
        
        return temperature_df

    # STEP: Load data--troop----------------------------------------------------
    def create_troop_dataframe(self):
        longitudes, latitudes, survivals, directions, divisions = [], [], [], [], []

        i = 6
        while i <= 53:
            line_split = self.lines[i].split()
            long, lat, surv, dir, div = line_split[-5:]

            longitudes.append(float(long))
            latitudes.append(float(lat))
            survivals.append(float(surv))
            directions.append(str(dir))
            divisions.append(int(div))
            i += 1

        troop_tuple = longitudes, latitudes, survivals, directions, divisions
        troop_df = pd.DataFrame()

        for column_name, data in zip(self.column_names_troop, troop_tuple):
            troop_df[column_name] = data

        return troop_df

    # STEP: Create SQLite DB----------------------------------------------------
    def create_database(self):
        city_df = self.create_city_dataframe()
        temperature_df = self.create_temperature_dataframe()
        troop_df = self.create_troop_dataframe()
        
        connection = sqlite3.connect("data/minard.db")

        df_dict = {
            "cities":city_df,
            "temperatures":temperature_df,
            "troops":troop_df
        }

        for key, value in df_dict.items():
            value.to_sql(name=key, con=connection, if_exists="replace", index=False)

        connection.close()


# STEP: Instantization of class
create_minard_db = CreateMinardDB()
create_minard_db.create_database()

