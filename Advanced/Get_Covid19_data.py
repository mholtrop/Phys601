#!/usr/bin/env python
#
# This set of functions retreives the COVID19 data that is availbale from
# John Hopkins and from the NYT.
#
# Other sources could be added, if the data is available publicly.
#
# The code is implemented to use Pandas, and to simply use some methods
# that return the datasets for use in a Python notebook.
#
import numpy as np
import os
import pandas as pd
import requests
import json
# try:
#     import plotly.express as px
#     import plotly.graph_objects as go
# except:
#     print("No plotly available. No plotting done in this script.")

def Get_Abbrevs():
    #
    # Handy table to map state name to abbreviation.
    #
    state_name_to_abbrev_url = "https://worldpopulationreview.com/static/states/name-abbr.json"
    state_name_to_abbrev = requests.get(state_name_to_abbrev_url).json()
    abbrev_to_state_name_url = "https://worldpopulationreview.com/static/states/abbr-name.json"
    abbrev_to_state_name = requests.get(abbrev_to_state_name_url).json()
    return state_name_to_abbrev, abbrev_to_state_name

def Get_County_GEO(force_web=False):
    """Load the county GEO shapes from the Plotly website. If the file exists locally, read it from
    disk, unless force_we=True."""
    # fips_state_code_url="https://www2.census.gov/programs-surveys/popest/geographies/2018/state-geocodes-v2018.xlsx"
    # pd_states=pd.read_excel(fips_state_code_url,header=5)
    # fips_county_codes=url="https://www2.census.gov/programs-surveys/popest/geographies/2018/all-geocodes-v2018.xlsx"
    # pd_counties=pd.read_excel("/Users/maurik/Downloads/all-geocodes-v2018.xlsx",header=4)

    geo_file_name = "geojson-counties-fips.json"
    try:
        file_info = os.lstat(geo_file_name)
    except:
        file_info = None

    if file_info is None or force_web:
        geo_url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
        geo_dat = requests.get(geo_url)
        with open(geo_file_name,'w') as output:
            json.dump(geo_dat.json(),output)
        return geo_dat.json()

    else:
        with open(geo_file_name) as infile:
            geo_dat_json = json.load(infile)
        return geo_dat_json


def Get_Census_All_data():
    """Get the census data for all counties in the US from the Census bureau.
    Note: that their data does not include the fips code, so we need to add that.
    Note: This data should not change much, so the data is cached"""

    # These are smaller alternatives in Excel format, but they do not include the FIPS codes, making use more difficult.
    # county_census_pol_url="https://www2.census.gov/programs-surveys/popest/tables/2010-2019/counties/totals/co-est2019-annres.xlsx"
    # state_census_pop_url="https://www2.census.gov/programs-surveys/popest/tables/2010-2019/state/totals/nst-est2019-01.xlsx"

    # Census data explanation pdf:
    # https://www2.census.gov/programs-surveys/popest/technical-documentation/
    # file-layouts/2010-2019/co-est2019-alldata.pdf

    detailed_census_data_url = "https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv"
    try:
        file_info = os.lstat("co-est2019-alldata.csv")
    except:
        file_info = None

    if file_info is None:
        census_pop_dat = pd.read_csv(detailed_census_data_url, encoding="ISO-8859-1")
        census_pop_dat.to_csv("co-est2019-alldata.csv")  # Store it to reduce network traffic.
    else:
        census_pop_dat = pd.read_csv("co-est2019-alldata.csv")

    census_pop_dat["fips"] = ["{:02d}{:03d}".format(census_pop_dat.iloc[i, census_pop_dat.columns.get_loc('STATE')],
                                                    census_pop_dat.iloc[i, census_pop_dat.columns.get_loc('COUNTY')])
                              for i in census_pop_dat.index]
    return census_pop_dat

def Get_Census_Data():
    """Get a reduced set of data from the Census for population numbers for 2019.
    Note: This data should not change much, so the data is cached by Get_Census_All_Data().
    Note: The data for Porto Rico (72), Guam (66), Northern Mariana Islands (69), Virgin Islands (78)
          are added 'by hand' (too much trouble to download it!). """

    census_pop_dat = Get_Census_All_data()

    us_pop_dat= census_pop_dat.loc[:, ["SUMLEV", "REGION", "DIVISION", "STATE", "COUNTY", "fips", "STNAME",
                                        "CTYNAME", "CENSUS2010POP", "POPESTIMATE2019"]]

    us_pop_dat = us_pop_dat.append({"SUMLEV":40, "REGION":5, "DIVISION": 1, "STATE": 72, "COUNTY": 0,
                                    "fips":'72000', "STNAME":"Puerto Rico", "CTYNAME":"Puerto Rico",
                                    "CENSUS2010POP": 3726157, "POPESTIMATE2019": 3193694},ignore_index=True)

    us_pop_dat = us_pop_dat.append({"SUMLEV":40, "REGION":5, "DIVISION": 2, "STATE": 66, "COUNTY": 0,
                                    "fips":'66000', "STNAME":"Guam", "CTYNAME":"Guam",
                                    "CENSUS2010POP": 159358, "POPESTIMATE2019": 167294},ignore_index=True)

    us_pop_dat = us_pop_dat.append({"SUMLEV":40, "REGION":5, "DIVISION": 2, "STATE": 69, "COUNTY": 0,
                                    "fips":'69000', "STNAME":"Northern Mariana Islands",
                                    "CTYNAME":"Northern Mariana Islands",
                                    "CENSUS2010POP": 53971, "POPESTIMATE2019": 57216},ignore_index=True)

    us_pop_dat = us_pop_dat.append({"SUMLEV": 40, "REGION": 5, "DIVISION": 2, "STATE": 78, "COUNTY": 0,
                                    "fips": '78000', "STNAME": "Virgin Islands",
                                    "CTYNAME": "Virgin Islands",
                                    "CENSUS2010POP": 106087, "POPESTIMATE2019": 104578}, ignore_index=True)


    return us_pop_dat



def Get_NYT_USA_Data(from_web=True):
    if from_web:
        # NYT Data from web:
        NYT_covid_counties = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
        data_counties = pd.read_csv(NYT_covid_counties, parse_dates=[1], dtype={"fips": str},na_filter=False)
        NYT_covid_states = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
        data_states = pd.read_csv(NYT_covid_states, parse_dates=[1],na_filter=False)
    else:
        # If you got the data locally using: git clone https://github.com/nytimes/covid-19-data.git
        # then use these lines to read it in. Otherwise, comment out these lines and use the ones above.
        data_states=pd.read_csv("us-states.csv", parse_dates=[1], dtype={"fips": str}, na_filter=False)
        data_counties=pd.read_csv("us-counties.csv",parse_dates=[1],na_filter=False)


    # The data has some locations without a fips, so add a fake one.
    data_counties.loc[data_counties["county"] == "New York City", "fips"] = 36999   # New York City region
    data_counties.loc[data_counties["county"] == "Kansas City", "fips"] = 29999
    # The rest are "Unknown" counties
    data_counties.loc[data_counties["fips"] == "", "fips"] = \
        [data_states.loc[data_states["state"] == i, "fips"].values[0] + '998'
         for i in data_counties.loc[data_counties["fips"] == "", "state"]]


    state_name_to_abbrev, abbrev_to_state_name = Get_Abbrevs()
    # add abbreviation to each state.
    data_states.loc[:, 'st'] = [state_name_to_abbrev[name.title()] for name in data_states.loc[:, "state"]]
    data_counties.loc[:, 'st'] = [state_name_to_abbrev[name.title()] for name in data_counties.loc[:, "state"]]
    #
    # Add population counts
    #
    us_pop_dat = Get_Census_Data()
    states_pop_dat = us_pop_dat.loc[us_pop_dat["COUNTY"] == 0]
    # Temporarily add a "STATE" column with integer state codes:
    data_states["STATE"] = [int(i) for i in data_states["fips"]]
    data_states = pd.merge(data_states, states_pop_dat[["STATE", "POPESTIMATE2019"]], on="STATE", how="left")
    # Drop the temporary column
    data_states.drop(columns=["STATE"], inplace=True)
    # rename the new column.
    data_states.rename(columns={"POPESTIMATE2019": "pop"}, inplace=True)  # Temprary rename for merge.

    data_counties = pd.merge(data_counties, us_pop_dat[["fips", "POPESTIMATE2019"]], on="fips", how="left")
    data_counties.rename(columns={"POPESTIMATE2019": "pop"}, inplace=True)

    #
    # The below commented code does the same, adding a population column. Is it more than a 1000 times slower.
    #
    # data_states["pop"] = 1
    # for i in data_states.index:
    #     state = data_states.iloc[i, data_states.columns.get_loc("fips")]
    #     pop = us_pop_dat.loc[(us_pop_dat["STATE"] == state) & (us_pop_dat["COUNTY"] == 0), "POPESTIMATE2019"].values
    #     if len(pop) == 1:
    #         data_states.iloc[i, data_states.columns.get_loc("pop")] = pop[0]
    #     else:
    #         data_states.iloc[i, data_states.columns.get_loc("pop")] = 2
    #
    # data_counties["pop"] = 1
    # for i in data_counties.index:
    #     fips = data_counties.iloc[i, data_counties.columns.get_loc("fips")]
    #     pop = us_pop_dat.loc[(us_pop_dat["fips"] == fips), "POPESTIMATE2019"].values
    #     if len(pop) == 1:
    #         data_counties.iloc[i, data_counties.columns.get_loc("pop")] = pop
    #     else:
    #         data_counties.iloc[i, data_counties.columns.get_loc("pop")] = 2

    #
    # Add hover text
    # This is most time consuming step in this routine, we skip it, because it is
    # not needed for every date, and the needed info may change.
    #
    # data_states.loc[:, 'text'] = [data_states.loc[d, 'state'] + '<br>' +
    #                               'pop:'+ str(data_states.loc[d, 'pop']) + '<br>' +
    #                               'cases:' + str(data_states.loc[d, 'cases']) + ' deaths:' +
    #                               str(data_states.loc[d, 'deaths'])
    #                               for d in data_states.index]
    # data_counties.loc[:, 'text'] = [data_counties.loc[d, 'county'] + ', ' + data_counties.loc[d, 'st'] + '<br>' +
    #                                 'pop:' + str(data_counties.loc[d, 'pop']) + '<br>' +
    #                                 'cases:' + str(data_counties.loc[d, 'cases']) + ' deaths:' +
    #                                 str(data_counties.loc[d, 'deaths'])
    #                                 for d in data_counties.index]
    # Convert the dates to datetime for datetime arithmetic and get a list of dates available
    data_states.loc[:, 'datetime'] = pd.to_datetime(data_states['date'])
    data_counties.loc[:, 'datetime'] = pd.to_datetime(data_counties['date'])
    # Select last available date, add these as an extra member variable to the Pandas Dataframe.
    data_states.this_date = data_states.loc[:, 'date'].unique()[-1]
    data_counties.this_date = data_counties.loc[:, 'date'].unique()[-1]

    return data_states, data_counties

# Fixup some name oddities by adding additional entries
def country_codes_fix(country_codes,old,new):

    if len(country_codes.loc[country_codes['name'] == new ]):
        print("{} is already OK.".format(new))
        return

    add = country_codes.loc[country_codes['name'] == old].copy()
    add['name'] = new
    country_codes = country_codes.append(add, ignore_index=True)
    return country_codes

def Get_Country_Codes(from_web=True):
    """Get the 3 letter country code abbreviations, and fix up that data"""
    # Get a list of Names with the 3 letter country codes.
    # See: https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes
    # And: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
    #
    if from_web:
        url_country_codes="https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/slim-3/slim-3.json"
        country_codes = pd.read_json(url_country_codes)

        # Fixes by adding additional names for countries.
        country_codes = country_codes_fix(country_codes, 'Bolivia (Plurinational State of)', 'Bolivia')
        country_codes = country_codes_fix(country_codes, 'Brunei Darussalam', 'Brunei')
        country_codes = country_codes_fix(country_codes, "Côte d'Ivoire", "Cote d'Ivoire")
        country_codes = country_codes_fix(country_codes, "Iran (Islamic Republic of)", 'Iran')
        country_codes = country_codes_fix(country_codes, "Korea, Republic of", 'Korea, South')
        country_codes = country_codes_fix(country_codes, "Moldova, Republic of", 'Moldova')
        country_codes = country_codes_fix(country_codes, "Russian Federation", "Russia")
        country_codes = country_codes_fix(country_codes, "Taiwan, Province of China", "Taiwan*")
        country_codes = country_codes_fix(country_codes, "Tanzania, United Republic of", "Tanzania")
        country_codes = country_codes_fix(country_codes, "United Kingdom of Great Britain and Northern Ireland",
                                          "United Kingdom")
        country_codes = country_codes_fix(country_codes, "United States of America", "US")
        country_codes = country_codes_fix(country_codes, "Venezuela (Bolivarian Republic of)", "Venezuela")
        country_codes = country_codes_fix(country_codes, "Viet Nam", "Vietnam")
        country_codes = country_codes_fix(country_codes, "Syrian Arab Republic", "Syria")
        country_codes = country_codes_fix(country_codes, "Lao People's Democratic Republic", "Laos")
        country_codes = country_codes_fix(country_codes, "Palestine, State of", "West Bank and Gaza")
        country_codes = country_codes_fix(country_codes, "Myanmar", "Burma")
        country_codes = country_codes=country_codes.append({'name':'Other', 'alpha-3':'XXX', "country-code":999},
                                                           ignore_index=True)
        country_codes = country_codes.append({'name': 'Diamond Princess', 'alpha-3': 'XX1', "country-code": 991},
                                             ignore_index=True)
        country_codes = country_codes.append({'name': 'Kosovo', 'alpha-3': 'XX2', "country-code": 992},
                                             ignore_index=True)
        country_codes = country_codes.append({'name': 'MS Zaandam', 'alpha-3': 'XX3', "country-code": 993},
                                             ignore_index=True)

        country_codes.to_csv("country_codes.csv")
    else:
        country_codes = pd.read_csv("country_codes.csv",index_col=0)

    return country_codes

def Get_World_Pop_Data(from_web=True):
    """Get the data for the world population by country from the worldbank.org"""

    world_pop_url = "http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=excel"
    if from_web:
        world_pop = pd.read_excel(world_pop_url,skiprows=3)
        world_pop.rename(columns={'Country Code': 'code', 'Country Name': 'Country'}, inplace=True)
        world_pop = world_pop.append(
    [{"Country": "Taiwan", "code": "TWN", "Indicator Name": "Population, total","2018": 23816775},
     {"Country": "Holy See", "code": "VAT", "Indicator Name": "Population total","2018":801},
     {"Country": "Western Sahara", "code": "ESH", "Indicator Name": "Population total", "2018":597339}
        ],
            ignore_index=True)

        world_pop.to_csv("world_pop.csv")

    else:
        world_pop = pd.read_csv("world_pop.csv",index_col=0)

    return(world_pop)


def Get_Global_data(country_codes=None,from_web=True):
    """Get the global COVID19 data from John Hopkins University."""

    if from_web:

        if country_codes is None:
            country_codes = Get_Country_Codes()
        
        data_global_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
        data_global = pd.read_csv(data_global_url)
        deaths_global_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
        deaths_global = pd.read_csv(deaths_global_url)
        recovered_global_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
        recovered_global = pd.read_csv(recovered_global_url)

        # Fixup some data inconsistencies.
        try:
            i_fix = data_global.loc[data_global['Country/Region'] == "Congo (Brazzaville)"].index[0]
            data_global.iloc[i_fix, data_global.columns.get_loc('Country/Region')] = 'Congo'
            data_global.iloc[i_fix, data_global.columns.get_loc('Province/State')] = 'Brazzaville'
        except:
            print("You may have run this one before, so data is already fixed?")

        try:
            i_fix = deaths_global.loc[deaths_global['Country/Region'] == "Congo (Brazzaville)"].index[0]
            deaths_global.iloc[i_fix, deaths_global.columns.get_loc('Country/Region')] = 'Congo'
            deaths_global.iloc[i_fix, deaths_global.columns.get_loc('Province/State')] = 'Brazzaville'
        except:
            print("You may have run this one before, so data is already fixed?")

        try:
            i_fix = recovered_global.loc[recovered_global['Country/Region'] == "Congo (Brazzaville)"].index[0]
            recovered_global.iloc[i_fix, recovered_global.columns.get_loc('Country/Region')] = 'Congo'
            recovered_global.iloc[i_fix, recovered_global.columns.get_loc('Province/State')] = 'Brazzaville'
        except:
            print("You may have run this one before, so data is already fixed?")

        try:
            i_fix = data_global.loc[data_global['Country/Region'] == "Congo (Kinshasa)"].index[0]
            data_global.iloc[i_fix, data_global.columns.get_loc('Country/Region')] = 'Congo'
            data_global.iloc[i_fix, data_global.columns.get_loc('Province/State')] = 'Kinshasa'
        except:
            print("You may have run this one before, so data is already fixed?")

        try:
            i_fix = deaths_global.loc[deaths_global['Country/Region'] == "Congo (Kinshasa)"].index[0]
            deaths_global.iloc[i_fix, deaths_global.columns.get_loc('Country/Region')] = 'Congo'
            deaths_global.iloc[i_fix, deaths_global.columns.get_loc('Province/State')] = 'Kinshasa'
        except:
            print("You may have run this one before, so data is already fixed?")

        try:
            i_fix = recovered_global.loc[recovered_global['Country/Region'] == "Congo (Kinshasa)"].index[0]
            recovered_global.iloc[i_fix, recovered_global.columns.get_loc('Country/Region')] = 'Congo'
            recovered_global.iloc[i_fix, recovered_global.columns.get_loc('Province/State')] = 'Kinshasa'
        except:
            print("You may have run this one before, so data is already fixed?")

        data_global.this_date = data_global.keys()[-1]  # Save the last date from the keys.
        deaths_global.this_data = deaths_global.keys()[-1]
        recovered_global.this_data = recovered_global.keys()[-1]

        # Add a new column with the country codes, which we look up from the table.
        data_global['code'] = 'XXX'
        deaths_global['code'] = 'XXX'
        recovered_global['code'] = 'XXX'
        code_id = data_global.columns.get_loc('code')

        for i in range(len(data_global)):
            data_global.iloc[i, code_id] = \
            country_codes.loc[country_codes['name'] == data_global.iloc[i]['Country/Region'], 'alpha-3'].iloc[0]

        code_id = deaths_global.columns.get_loc('code')
        for i in range(len(deaths_global)):
            deaths_global.iloc[i, code_id] = \
            country_codes.loc[country_codes['name'] == deaths_global.iloc[i]['Country/Region'], 'alpha-3'].iloc[0]

        code_id = recovered_global.columns.get_loc('code')
        for i in range(len(recovered_global)):
            recovered_global.iloc[i, code_id] = \
            country_codes.loc[country_codes['name'] == recovered_global.iloc[i]['Country/Region'], 'alpha-3'].iloc[0]

        data_global.to_csv("time_series_covid19_confirmed_global.csv")
        deaths_global.to_csv("time_series_covid19_deaths_global.csv")
        recovered_global.to_csv("time_series_covid19_recovered_global.csv")

    else:
        data_global = pd.read_csv("time_series_covid19_confirmed_global.csv", index_col=0)
        deaths_global = pd.read_csv("time_series_covid19_deaths_global.csv", index_col=0)
        recovered_global = pd.read_csv("time_series_covid19_recovered_global.csv", index_col=0)


    return data_global, deaths_global, recovered_global


def Sum_data(data_global,deaths_global,recovered_global,country_codes):
    """Return the data summed over the country codes, so all data from the same country is added up."""
    sum_global = data_global.groupby(['code'],as_index=False).sum()
    sum_global.drop(columns=['Lat', 'Long'], inplace=True)
    sum_deaths = deaths_global.groupby(['code'],as_index=False).sum()
    sum_deaths.drop(columns=['Lat', 'Long'], inplace=True)
    sum_recovered = recovered_global.groupby(['code'],as_index=False).sum()
    sum_recovered.drop(columns=['Lat', 'Long'], inplace=True)

    # Don't loose the "this_date" if it was added.
    if 'this_date' in data_global.__dict__:
        sum_global.this_date = data_global.this_date

    if 'this_date' in deaths_global.__dict__:
        sum_deaths.this_date = deaths_global.this_date

    if 'this_date' in recovered_global.__dict__:
        sum_recovered.this_date = recovered_global.this_date

    return sum_global, sum_deaths, sum_recovered

def Add_Population_Data(indat,inpop,colpop="2018"):
    """Add a column for population data from inpop data table using column colpop (defaults to '2018')
       Note that inpop must have the matching 'code' for the country codes. This method is a simple merge operation.
       The inpop column is renamed to 'pop' """
    result = pd.merge(indat, inpop[['code', colpop]], on="code", how="left")
    result.rename(columns={colpop:"pop"},inplace=True)

    # Don't loose the "this_date" if it was added.
    if 'this_date' in indat.__dict__ :
        result.this_date = indat.this_date
    return result

