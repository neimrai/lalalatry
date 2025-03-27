import pandas as pd
import json

sales_df = pd.read_csv('data/sales.csv')
students_df = pd.read_csv('data/students.csv')

with open('data/students.json', 'r') as f:
    students_json = json.load(f)

