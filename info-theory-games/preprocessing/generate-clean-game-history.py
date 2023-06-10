import pandas as pd

'''
Download dataset from 
https://data.world/maxstrange/diplomacyboardgame

Per the comments it appears to be zipped twice. 
To load it into MySQL:
gunzip diplomacy.sql.gz
mv diplomacy.sql diplomacy.sql.gz 
gunzip diplomacy.sql.gz

Open MySQL Workbench, use data import and execute .SQL script 

Did select * for each table and exported to CSV. Had to reformat a bit as export was ;-delimited and saved without headers. Final clean versions of tables saved in this drive folder https://drive.google.com/drive/u/0/folders/1SJx_UAtef-tQt3sxQfA9sKtXvoIS7KEf  
'''


units = pd.read_csv('diplomacy.units.csv', sep=';', header=None)
units.columns = ['game_id', 'country', 'type', 'start_turn', 'end_turn', 'unit_id']
units.to_csv('diplomacy.units.csv', index=False)

turns = pd.read_csv('diplomacy.turns.csv', sep=';', header=None)
turns.columns = ['game_id',
                    'turn_num',
                    'phase',
                    'year',
                    'season', 
                    'scs_england',
                    'scs_france',
                    'scs_italy',
                    'scs_russia',
                    'scs_turkey',
                    'scs_germany',
                    'scs_austria']
turns.to_csv('diplomacy.turns.csv', index=False)

players = pd.read_csv('diplomacy.players.csv', sep=';', header=None)
players.columns = ['game_id',
                'country', 
                'won', 
                'num_supply_centers',
                'eliminated',
                'start_turn',
                'end_turn']
players.to_csv('diplomacy.players.csv', index=False)

orders = pd.read_csv('diplomacy.orders.csv', delimiter=';', header=None)
orders.columns = ['game_id', 
                    'unit_id', 
                    'unit_order', 
                    'location', 
                    'target', 
                    'target_dest',  
                    'success', 
                    'reason', 
                    'turn_num']
orders.to_csv('diplomacy.orders.csv', index=False)

game_orders = orders.merge(units[['game_id', 'unit_id', 'country']], on=['game_id', 'unit_id'])
go_check = game_orders.groupby(['game_id', 'unit_id', 'turn_num']).size().reset_index()


# 334 games appear to have something weird going on with dupe moves per unit 
# We are just going to remove these games

len(go_check[go_check[0] > 1]['game_id'].unique())

orders = orders[~orders['game_id'].isin(go_check[go_check[0] > 1]['game_id'].unique())]
units = units[~units['game_id'].isin(go_check[go_check[0] > 1]['game_id'].unique())]
game_orders = orders.merge(units[['game_id', 'unit_id', 'country', 'type']], on=['game_id', 'unit_id'])
game_orders.to_csv('clean-game-history.csv', index=False)
