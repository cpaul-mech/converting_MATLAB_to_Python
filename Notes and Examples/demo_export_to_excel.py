import pandas as pd
import numpy as np


data = {'Operator':['Vodafone', 'Jio', 'BSNL'],'Data (GB)':[3, 5, 2],'Speed (GB/s)':[1,2,0.5],'Price/month':[300,250,320]}
# change the index for the rows to say "May 2022"

df = pd.DataFrame(data, index=['May 2022', 'May 2023', 'May 2024'])
# print(df)


df.to_excel('demo_export_to_excel.xlsx', sheet_name='Sheet 1', startrow=0, startcol=0)