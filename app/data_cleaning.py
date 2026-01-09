class DataCleaning:

    def __init__(self):
        pass

    def clean_data(self, data):
        import pandas as pd
        import numpy as np
        import os

        from functools import reduce


        data['Year'] = data['Year'].str.replace('enroll', '')
        data['State or jurisdiction'] = data['State or jurisdiction'].str.replace(r'\.+$', '', regex=True).str.strip()

        df21 = data[data['Year'] == '2021-22']
        df21 = df21[[ 'State or jurisdiction', 'Year','Public', 'Public.1',
        'Public.2',
        'Public.3',
        'Private',
        'Private.1',
        'Private.2',
        'Private.3',
        'Private.4',
        'Private.5',
        'Private.6',
        'Private.7']
        ]
        df21
        df21.columns = ['State or jurisdiction', 'Year', 'Total_ug', '4-year', '2-year',
               'Total_pb', 'Total_pug', 'Nonprofit 4-year_x', 'For-profit 4-year_x',
               'Nonprofit 2-year', 'For-profit 2-year', 'Total_ppb',
               'Nonprofit 4-year_y', 'For-profit 4-year_y']

        df21.dropna(inplace=True)
        df21 = df21.drop([264, 265])
        
        public_undergrad = data[['State or jurisdiction','Year', 'Public', 'Unnamed: 2', 'Unnamed: 3']]
        public_undergrad = public_undergrad.drop([0,1,2])
        public_undergrad.columns = ['State or jurisdiction', 'Year', 'Total_ug','4-year', '2-year'] 
        public_undergrad.dropna(inplace=True)

        public_pb = data[['State or jurisdiction','Year', 'Unnamed: 4']]
        public_pb = public_pb.drop([0,1,2])
        public_pb.columns = ['State or jurisdiction', 'Year', 'Total_pb']
        public_pb.dropna(inplace=True)
        
        private_undergrad = data[['State or jurisdiction','Year','Private' ] + [name for name in data.columns if name.startswith('Unnamed') and name.endswith(('6', '7', '8', '9'))]]
        private_undergrad = private_undergrad.drop([0,1,2])
        private_undergrad.columns = ['State or jurisdiction', 'Year', 'Total_pug', 'Nonprofit 4-year', 'For-profit 4-year', 'Nonprofit 2-year', 'For-profit 2-year']
        private_undergrad.dropna(inplace=True)

        private_pb = data[['State or jurisdiction', 'Year', ] + [name for name in data.columns if name.startswith('Unnamed') and name.endswith(('10', '11', '12'))]]
        private_pb = private_pb.drop([0,1])
        private_pb.columns = ['State or jurisdiction', 'Year', 'Total_ppb', 'Nonprofit 4-year', 'For-profit 4-year']
        private_pb.dropna(inplace=True)

        for df in [public_pb, private_pb, public_undergrad, private_undergrad, df21]:
            df.replace('†', 0, inplace=True)
            df = df.reset_index(drop=True, inplace=True)
        
        dfs = [public_undergrad, public_pb, private_undergrad, private_pb]

        merged_df = reduce(
            lambda left, right: pd.merge(left, right, on=('State or jurisdiction','Year'), how='outer'),
            dfs
        )

        merged_df.dropna(inplace=True)

        merged_df = pd.concat([merged_df, df21])
        merged_df.reset_index(drop=True, inplace=True)

        merged_df.columns = [
            'State or jurisdiction',
            'Year',
            'Total_Pub_Under', 
            '4y_Pub_Under', 
            '2y_Pub_Under', ''
            'Total_Pub_Postbacc',
            'Total_Priv_Under',
            'Np_4y_Priv_Under',
            'Fp_4y_Priv_Under',
            'Np_2y_Priv_Under',
            'Fp_2y_Priv_Under',
            'Total_Priv_Postbacc',
            'Np_4y_Priv_Postbacc',
            'Fp_4y_Priv_Postbacc'
        ]

        merged_df.rename(columns={'State or jurisdiction': 'State'}, inplace=True)
        merged_df['Total_Enrollment'] = merged_df['Total_Pub_Under'] + merged_df['Total_Priv_Under']

        return merged_df