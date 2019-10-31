# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), '../../../../../tmp'))
	print(os.getcwd())
except:
	pass
# %%
import os
import git2net

print(os.path)

sqlite_db_file = '/home/luc/pip/git2net/ds_gw_1/git2net_tutorial.db'

#check, if database file is there; remove if yes
if os.path.exists(sqlite_db_file):
    os.remove(sqlite_db_file)
    print('sqlite_db_file removed!')


#set variable to whatever folder the to-be-mined git repository is located:
repo_dir = '/home/luc/pip/git2net/ds_gw_1/TLP'


# %%


#mining process: 
#repo_dir: to-be-mined git repository
#sqlite_db_file: to-be-stored values in database

git2net.mine_git_repo(repo_dir, sqlite_db_file)


# %%
git2net.mining_state_summary(repo_dir, sqlite_db_file)


# %%
#draws nodes for visualization:
#t = Pathpy temporal network
#node_info = Information about node
#edge_info = Information about edges

t, node_info, edge_info = git2net.get_coediting_network(sqlite_db_file)
t


# %%


print(t)
print('\n')
print(node_info)
print('\n')
print(edge_info)
print('\n')


# %%
import pathpy as pp

#returns a Graph, with an edge pointing from node A to node B whenever A changed a line of original author B: 
pp.Network.from_temporal_network(t)


# %%


#visualize which files the authors collaborated on:
t, node_info, edge_info = git2net.get_bipartite_network(sqlite_db_file)
n = pp.Network.from_temporal_network(t)
n


# %%
#colour the author nodes light blue and the collaboration files dark blue:
colour_map = {'author': '#73D2DE', 'file': '#2E5EAA'}
node_colour = {node: colour_map[node_info['class'][node]] for node in n.nodes}
pp.visualisation.plot(n, node_color=node_colour)


# %%


#draw graph showing authors working collaborating on same files:
#all information of direction of edges is lost:
n, node_info, edge_info = git2net.get_coauthorship_network(sqlite_db_file)
n


# %%
from datetime import datetime

time_from = datetime(2019, 5, 1)
t, node_info, edge_info = git2net.get_bipartite_network(sqlite_db_file, time_from=time_from)

print(node_info)

n = pp.Network.from_temporal_network(t)
colour_map = {'author': '#73D2DE', 'file': '#2E5EAA'}
node_colour = {node: colour_map[node_info['class'][node]] for node in n.nodes}
pp.visualisation.plot(n, node_color=node_colour)


# %%
import sqlite3

#connect to created database file:
con = sqlite3.connect(sqlite_db_file)
#create cursor to access database (queries etc.)
c = con.cursor()


# %%
#take all rows with edit_type=replacement
#use placeholder to avoid SQL-injections
c.execute("SELECT * FROM edits WHERE edit_type=?", ('replacement',))

#print(c.fetchmany(2)[1][3])

#print(c.fetchmany(2))

rows = c.fetchall()

for row in rows:
    print(row)


# %%
import pandas as pd

#connect to database file:
con = sqlite3.connect(sqlite_db_file)

#select only subparts of the database:
#in particular: subparts of table "edits":
query1 = """
    SELECT 
    commit_hash,
    edit_type,
    levenshtein_dist    
    FROM edits
    WHERE
    edit_type = 'replacement'
"""

#turn into panda dataframe:
df1 = pd.read_sql_query(query1, con=con)

print(df1.head())
print(df1.shape)


# %%
#turn pandas dataframe table "edits" back into a database for viewing:
sqlite_db_file_1 = '/home/luc/pip/git2net/ds_gw_1/db1.db'

conn = sqlite3.connect(sqlite_db_file_1)

df1.to_sql('edits', conn, if_exists='replace')


# %%
#select only subparts of the database:
#in particular: subparts of table "commits":
query2 = """
    SELECT
    hash,
    committer_name,
    committer_date
    FROM commits
"""
#turn into pandas dataframe:
df2 = pd.read_sql_query(query2, con=con)

print(df2.head())
print(df2.shape)


# %%
#turn pandas dataframe table "commits" back into a database for viewing:
sqlite_db_file_2 = '/home/luc/pip/git2net/ds_gw_1/db2.db'

conn = sqlite3.connect(sqlite_db_file_2)

df2.to_sql('commits', conn, if_exists='replace')


# %%
#merge dataframes:

data = df2.merge(df1, left_on='hash', right_on='commit_hash')
data


# %%
print(data.shape)


# %%
#print rows:
for i in range(data.shape[0]):
    print(data.apply(lambda column: column[i], axis=0))
    print('\n')
    print(i)
    print('\n')
    j = i
    for j in range(j,data.shape[0]):
        print(data.apply(lambda column: column[j], axis=0))
        print('\n')
        print(j)
        print('\n')
        if j==3:
            print('break!')
            break
    print('\n')
    if i == 3:
        break


# %%
for i in range(10):
    print('i=',i)
    for j in range(i,10):
        print('j=',j)
    


# %%
#print rows:
for i in range(data.shape[0]):
    print(data.apply(lambda column: column[i], axis=0))
    print('\n')
    print(i)
    print('\n')
    j = i
    for j in range(j,data.shape[0]):
        print(data.apply(lambda column: column[j], axis=0))
        print('\n')
        print(j)
        print('\n')
        if j==3:
            print('break!')
            break
    print('\n')
    if i == 3:
        break


# %%

def adding_up(data):
    #print(data)
    #print(data.shape[0])
    if data.shape[0] == 1:
        return data
    for i in range(data.shape[0]):
        #print('i=',i)        
        for j in range(i+1, data.shape[0]):
            if data.iloc[i]['hash'] < data.iloc[j]['hash']:
                #print(data.iloc[i]['levenshtein_dist'])
                #print(data.iloc[j]['levenshtein_dist'])
                tmp = data.iloc[i]['levenshtein_dist'] + data.iloc[j]['levenshtein_dist']
                data.iloc[i]['levenshtein_dist'] = tmp
                #print(data.iloc[i]['levenshtein_dist'])
                #print('Es wird gedropped, anschließend Indexreset:\n')
                data = data.drop(data.index[j])        
                data = data.reset_index(drop=True)
                #print(data)
                #print(type(df))
                return data


# %%
# def adding_up(data):
#     if data.shape[0] == 1:
#         return data
#     for i in range(data.shape[0]):
#         for j in range(i+1, data.shape[0]):
#             if data.iloc[:,(i,'hash')] < data.iloc[:,(j,'hash')]:
#                 tmp = data.iloc[:,(i,'levenshtein_dist')] + data.iloc[:,(j,'levenshtein_dist')]
#                 data.iloc[:,(i,'levenshtein_dist')] = tmp
#                 data = data.drop(data.index[j])        
#                 data = data.reset_index(drop=True)
#                 return data


# %%
tmp_data = data

i=0

while True:
    i+=1
    print(i)
    #print(type(tmp_data))
    something = adding_up(tmp_data)
    #print(type(something))
    if something.shape == tmp_data.shape:
        break
    tmp_data = something

print('done')


# %%
print(data)


# %%

# for i in range(data.shape[0]):
#     x = data.apply(lambda column: column[i], axis=0)
#     print(x)
#     print('\n')
#     print(i)
#     print('\n')
#     j = i+1
#     for j in range(j,data.shape[0]):
#         y= data.apply(lambda column: column[j], axis=0)
#         print(y)
#         print('\n')
#         print(j)
#         print('\n')
#         if x['hash'] == y['hash']:
#             x['levenshtein_dist']=x['levenshtein_dist']+y['levenshtein_dist']
#             data.drop([j], axis=0, inplace=True)
#         if j==3:
#             print('break!')
#             break
#     print('\n')
#     if i == 3:
#         break


# %%
for i in range(data.shape[0]):
    #print(data.iloc[i]['hash'])
    for j in range(i+1,data.shape[0]):
        if data.loc[i]['hash'] == data.loc[j]['hash']:
        #if data.iloc[:,(i,'hash')] == data.iloc[:,(j,'hash')]:
            print('same!')
            data.loc[i]['levenshtein_dist'] += data.loc[j]['levenshtein_dist']
            #data.iloc[:,(i,'levenshtein_dist')] += data.iloc[:,(j,'levenshtein_dist')]
            data.drop([j], inplace=True)

