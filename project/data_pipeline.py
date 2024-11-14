import os
import kaggle
import pandas as pd
import sqlite3

# Download dataset from Kaggle
def download_dataset(dataset_name, download_path, file_name):
    # Check Kaggle API
    kaggle.api.authenticate()
    
    # Download and unzip the dataset
    kaggle.api.dataset_download_files(dataset_name, path=download_path, unzip=True)
    print(f"Dataset {dataset_name} downloaded to data folder.")

    return os.path.join(download_path, file_name)

# Function to process the first dataset
def process_us_estimated_crimes(input_path):
    # Load the dataset
    df = pd.read_csv(input_path)
    
    # Select required columns: year, state_name, population, violent_crime, homicide, rape_legacy, robbery, property_crime, burglary, larceny, motor_vehicle_theft
    df = df[['year', 'state_name', 'population', 'violent_crime', 'homicide', 'rape_legacy', 'robbery', 'property_crime', 'burglary', 'larceny', 'motor_vehicle_theft']]

    # Remove NULL data
    df = df.dropna()

    df['year'] = df['year'].astype(int)
    df['state_name'] = df['state_name'].astype(str)
    df['population'] = df['population'].astype('int64')
    df['violent_crime'] = df['violent_crime'].astype('int64')
    df['homicide'] = df['homicide'].astype('int64')
    df['rape_legacy'] = df['rape_legacy'].astype('int64')
    df['robbery'] = df['robbery'].astype('int64')
    df['property_crime'] = df['property_crime'].astype('int64')
    df['burglary'] = df['burglary'].astype('int64')
    df['larceny'] = df['larceny'].astype('int64')
    df['motor_vehicle_theft'] = df['motor_vehicle_theft'].astype('int64')

    return df

# Function to process the second dataset
def process_chicago_crime_data(input_path):
    # Load the specific CrimeDate (1).csv dataset
    df = pd.read_csv(input_path)
    
    # Select required columns: date, primary_type, crime_count, arrest_count, false_count
    df = df[['date', 'primary_type', 'crime_count', 'arrest_count', 'false_count']]

    # Remove NULL data
    df = df.dropna()
    
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df['primary_type'] = df['primary_type'].astype(str)
    df['crime_count'] = df['crime_count'].astype(int)
    df['arrest_count'] = df['arrest_count'].astype(int)
    df['false_count'] = df['false_count'].astype(int)

    return df

# Function to create SQLite file
def save_to_sqlite(df, db_name, table_name):
    conn = sqlite3.connect(db_name)  # Use .sqlite extension

    # Insert data
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"{table_name}.sqlite file created.")

    conn.commit()
    conn.close()


def run_pipeline():
    # Ensure ../data directory exists
    parent_data_dir = os.path.join("..", "data")
    if not os.path.exists(parent_data_dir):
        os.makedirs(parent_data_dir)

    # Paths to download and process datasets
    us_estimated_crimes_path = os.path.join(parent_data_dir, 'us_estimated_crimes.zip')
    chicago_crime_data_path = os.path.join(parent_data_dir, 'CrimeDate (1).csv')

    # Download the US Estimated Crimes dataset
    download_dataset('tunguz/us-estimated-crimes', parent_data_dir, 'estimated_crimes_1979_2019.csv')
    
    # Download the Chicago Crime Data and get main data file
    crime_data_file_path = download_dataset('elijahtoumoua/chicago-analysis-of-crime-data-dashboard', parent_data_dir, 'CrimeDate (1).csv')

    # Delete unused data files if they exist
    files_to_delete = ['CrimeDesc.csv', 'CrimeLocation.csv']
    for filename in files_to_delete:
        file_path = os.path.join(parent_data_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    # Process the datasets
    us_estimated_crimes_df = process_us_estimated_crimes(os.path.join(parent_data_dir, 'estimated_crimes_1979_2019.csv'))
    chicago_crime_data_df = process_chicago_crime_data(crime_data_file_path)

    # Save the data to SQLite with .sqlite extension in the data folder
    save_to_sqlite(us_estimated_crimes_df, os.path.join(parent_data_dir, 'us_estimated_crimes.sqlite'), 'us_estimated_crimes_table')
    save_to_sqlite(chicago_crime_data_df, os.path.join(parent_data_dir, 'chicago_crime_data.sqlite'), 'chicago_crime_data_table')
    
    files_to_rename = { 'CrimeDate (1).csv': 'chicago_crime_data.csv', 'estimated_crimes_1979_2019.csv': 'us_estimated_crimes.csv'}
    
    for old_name, new_name in files_to_rename.items():
        old_path = os.path.join(parent_data_dir, old_name)
        new_path = os.path.join(parent_data_dir, new_name)
        
        if os.path.exists(new_path):
            os.remove(new_path)
            
        if os.path.exists(old_path):
            os.rename(old_path, new_path)


# Run the pipeline
if __name__ == "__main__":
    run_pipeline()