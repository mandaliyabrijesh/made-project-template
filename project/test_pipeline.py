import unittest
import os
import subprocess
import sys
import sqlite3
from data_pipeline import run_pipeline

class AutoTestPipeline(unittest.TestCase):
    pipeline_run = False
    db_path = os.path.join("..", "data", "crime_data.sqlite")

    def setUp(self):
        if not AutoTestPipeline.pipeline_run:
            subprocess.run([sys.executable, "data_pipeline.py"], check=True)
            AutoTestPipeline.pipeline_run = True

    def test_datafile_exists(self):
        # Check crime_data.sqlite file is in the data folder or not.
        self.assertTrue(os.path.isfile(AutoTestPipeline.db_path), f"File not found at {AutoTestPipeline.db_path}")

    def test_tables_have_data(self):
        
        dbconnection = sqlite3.connect(AutoTestPipeline.db_path)
        dbcursor = dbconnection.cursor()

        # Check if us_estimated_crimes table has data
        dbcursor.execute("SELECT COUNT(*) FROM us_estimated_crimes")
        us_estimated_crimes_count = dbcursor.fetchone()[0]
        self.assertGreater(us_estimated_crimes_count, 0, "The 'us_estimated_crimes' table has no data.")

        # Check if chicago_crime_data table has data
        dbcursor.execute("SELECT COUNT(*) FROM chicago_crime_data")
        chicago_crime_data_count = dbcursor.fetchone()[0]
        self.assertGreater(chicago_crime_data_count, 0, "The 'chicago_crime_data' table has no data.")

        dbconnection.close()

    def test_no_negative_values(self):

        dbconnection = sqlite3.connect(AutoTestPipeline.db_path)
        dbcursor = dbconnection.cursor()

        # Check if negative values in us_estimated_crimes table
        dbcursor.execute("SELECT COUNT(*) FROM us_estimated_crimes WHERE population < 0 OR population < 0 OR violent_crime < 0 OR homicide < 0 OR rape_legacy < 0 OR robbery < 0 OR property_crime < 0 OR burglary < 0 OR larceny < 0 OR motor_vehicle_theft < 0")
        negative_us_estimated = dbcursor.fetchone()[0]
        self.assertEqual(negative_us_estimated, 0, "The 'us_estimated_crimes' table contains negative values.")

        # Check if negative values in chicago_crime_data table
        dbcursor.execute("SELECT COUNT(*) FROM chicago_crime_data WHERE false_count < 0 OR crime_count < 0 OR arrest_count < 0 ")
        negative_chicago_crime = dbcursor.fetchone()[0]
        self.assertEqual(negative_chicago_crime, 0, "The 'chicago_crime_data' table contains negative values.")

        dbconnection.close()

if __name__ == "__main__":
    unittest.main()