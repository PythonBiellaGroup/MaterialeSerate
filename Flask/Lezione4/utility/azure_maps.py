import aiohttp
import asyncio
import pandas as pd
import datetime
from tqdm import tqdm
from utility import get_folder_path
from yaml_utility import read_yaml_file

config_base_path = get_folder_path('./')
configurations = read_yaml_file(config_base_path, 'azuremaps_config.yml')

client_id = configurations['client_id']
subscription_id = configurations['subscription_id']
subscription_key = configurations['subscription_key']
language = configurations['language']
country = configurations['country']


async def azure_map_geo_search(df, key, columns, config_path='', config_filename='', error_remove=True):
    """
    Search Latitude and Longitude about a city using a query
    This service use Azure Maps so you will need a subscription key for the service
    Please use a yaml file with your subscription keys
    If you want more specifications about yaml file please see your project documentation
    
    For query creation need the dataframe and a specific column used as a Key
    You also need a list of columns for the research (like: Comune, Provincia, Nazione, ...)
    
    Optionally you can remove dataframe rows that return error from the API Call.
    This is usefull to keep only significant features
    
    """

    # Get service configurations from yaml file
    if config_path == '' or config_path is None:
        config_path = get_folder_path('./')

    if config_filename == '' or config_filename is None:
        config_filename = '../../../LAVORO/DataLab/Rework/DatalabV1_Rework/Code/utility/azuremaps_config.yml'

    print(f"Config filename: {config_filename}, config path: {config_path}")
    configurations = read_yaml_file(config_path, config_filename)

    client_id = configurations['client_id']
    subscription_id = configurations['subscription_id']
    subscription_key = configurations['subscription_key']

    language = configurations['language']
    country = configurations['country']

    # Define the default service uri
    # Documentation: https://docs.microsoft.com/en-us/rest/api/maps/search/getsearchaddress
    service_uri = "https://atlas.microsoft.com/search/address/json?subscription-key={}&api-version=1.0&query={}&countrySet={}&language={}"

    # Define usefull lists and variables
    latitude = []
    longitude = []
    errors = []

    # Open the session for API Call
    session = aiohttp.ClientSession()

    for i, el in enumerate(tqdm(df[key].tolist())):

        # Generate the query for the search
        query = ''
        for k, col in enumerate(columns):
            search_object = df.loc[i, columns[k]]
            query = query + str(search_object) + ', '

        request = service_uri.format(subscription_key, query, country, language)

        try:
            response = await (await session.get(request)).json()

            # response['results'][0]['address']['countrySecondarySubdivision']
            latitude.append(response['results'][0]['position']['lat'])
            longitude.append(response['results'][0]['position']['lon'])

        except Exception as message:
            print(f"Impossibile to get information for element {i} about: {query} because: {message}")
            errors.append([i, el])
            continue

    # Close the session
    session = await(session.close())
    print(f"Download completed with {len(errors)} errors. Please check the errors list to see informations")

    # Remove errors (Optional)
    if error_remove:
        print("Removing errors from original dataframe")
        # Remove errors from original dataframe if there are into the previous procedure
        df_no_errors = df.copy()

        if errors != []:
            for i, e in enumerate(errors):
                codice = e[1]

                indexNames = df[df['key'] == codice].index

                # Delete these row indexes from dataFrame
                df.drop(indexNames, inplace=True)

                print(f"Removed errors {codice} in position: {indexNames}")

    # Create columns into the result_dataframe
    df['Latitude'] = latitude
    df['Longitude'] = longitude

    print(f"Result Dataframe Shape: {df_no_errors.shape}")

    return df
