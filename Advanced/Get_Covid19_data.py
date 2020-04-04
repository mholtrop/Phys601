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

def Get_County_GEO():
    # fips_state_code_url="https://www2.census.gov/programs-surveys/popest/geographies/2018/state-geocodes-v2018.xlsx"
    # pd_states=pd.read_excel(fips_state_code_url,header=5)
    # fips_county_codes=url="https://www2.census.gov/programs-surveys/popest/geographies/2018/all-geocodes-v2018.xlsx"
    # pd_counties=pd.read_excel("/Users/maurik/Downloads/all-geocodes-v2018.xlsx",header=4)
    geo_url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
    geo_dat = requests.get(geo_url)
    return geo_dat.json()


def Get_NYT_USA_Data(from_web=True):
    if from_web:
        # NYT Data from web:
        NYT_covid_counties = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
        data_counties = pd.read_csv(NYT_covid_counties, parse_dates=[1], dtype={"fips": str})
        NYT_covid_states = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
        data_states = pd.read_csv(NYT_covid_states, parse_dates=[1])
    else:
        # If you got the data locally using: git clone https://github.com/nytimes/covid-19-data.git
        # then use these lines to read it in. Otherwise, comment out these lines and use the ones above.
        data_states=pd.read_csv("covid-19-data/us-states.csv")
        data_counties=pd.read_csv("covid-19-data/us-counties.csv")

    state_name_to_abbrev, abbrev_to_state_name = Get_Abbrevs()
    # add abbreviation to each state.
    data_states.loc[:, 'st'] = [state_name_to_abbrev[name.title()] for name in data_states.loc[:, "state"]]
    data_counties.loc[:, 'st'] = [state_name_to_abbrev[name.title()] for name in data_counties.loc[:, "state"]]
    #
    # Add hover text
    #
    data_states.loc[:, 'text'] = [data_states.loc[d, 'state'] + '<br>' + \
                                  'cases:' + str(data_states.loc[d, 'cases']) + ' deaths:' + \
                                  str(data_states.loc[d, 'deaths']) \
                                  for d in data_states.index]
    data_counties.loc[:, 'text'] = [data_counties.loc[d, 'county'] + ', ' + data_counties.loc[d, 'st'] + '<br>' + \
                                    'cases:' + str(data_counties.loc[d, 'cases']) + ' deaths:' + \
                                    str(data_counties.loc[d, 'deaths']) \
                                    for d in data_counties.index]
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

def Get_Country_Codes():
    """Get the 3 letter country code abbreviations, and fix up that data"""
    # Get a list of Names with the 3 letter country codes.
    # See: https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes
    # And: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
    #
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
    return country_codes


def Get_Global_data(country_codes):
    """Get the global COVID19 data from John Hopkins University."""
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

    return data_global, deaths_global, recovered_global


def Sum_data(data_global,deaths_global,recovered_global,country_codes):
    """Return the data summed over the country codes, so all data from the same country is added up."""
    sum_global = data_global.groupby(['code']).sum()
    sum_global.drop(columns=['Lat', 'Long'], inplace=True)
    sum_deaths = deaths_global.groupby(['code']).sum()
    sum_deaths.drop(columns=['Lat', 'Long'], inplace=True)
    sum_recovered = recovered_global.groupby(['code']).sum()
    sum_recovered.drop(columns=['Lat', 'Long'], inplace=True)

    this_date = data_global.this_date
    sum_global.this_date = this_date
    sum_deaths.this_date = this_date
    sum_recovered.this_date = this_date
    
    sum_global['text'] = [country_codes.loc[country_codes['alpha-3'] == c, 'name'].iloc[-1] + '<br>' + \
                          ' cases:' + str(sum_global.loc[c, this_date]) + '<br>' + \
                          ' deaths:' + str(sum_deaths.loc[c, this_date]) + '<br>' + \
                          ' recoveded:' + str(sum_recovered.loc[c, this_date]) for c in sum_global.index]

    return sum_global,sum_deaths,sum_recovered

