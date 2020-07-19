import json
import pandas as pd

df = pd.read_csv('data.csv')

column_name = df.columns.values
df3 = pd.DataFrame()
df4 = pd.DataFrame()
df6 = pd.DataFrame()
for i, eachC in enumerate(column_name):
    if i <= 4:
        df3 = pd.concat([df3, df[eachC]], axis = 1)
    else:
        df4[eachC] = df[eachC].apply(lambda x : dict(eval(x)))
        df5 = df4[eachC].apply(pd.Series)
        column_names = df5.columns.values
        column_tuple = []
        for eachColumn in column_names:
            new_tuple = [eachC]
            new_tuple.append(eachColumn)
            new_tuple = tuple(new_tuple)
            column_tuple.append(new_tuple)
        a = column_tuple
        df5.columns = pd.MultiIndex.from_tuples([('', x[0]) if pd.isnull(x[1]) else x for x in a])
        df6 = pd.concat([df6, df5], axis = 1)

# df3_column = df3.columns.values
# empty_dict = {}
# for eachName in df3_column:
#     empty_dict[eachName] = ''

# empty_df = pd.DataFrame(empty_dict, index=[0])

# df3 = pd.concat([empty_df, df3 ], axis = 0)

final_df = pd.concat([df3, df6], axis = 1)
final_df_column = final_df.columns.values
final_df_column_tuple = []
for eachColumn in final_df_column:
    
    if type(eachColumn) == str:
        new_tuple = (eachColumn,'')
    else:
        new_tuple = eachColumn
    # new_tuple.append(eachColumn)
    # new_tuple = tuple(new_tuple)
    final_df_column_tuple.append(new_tuple)


a = final_df_column_tuple

print(a)

final_df.columns = pd.MultiIndex.from_tuples([('', x[0]) if pd.isnull(x[1]) else x for x in a])


df6.to_csv('t6.csv')
df3.to_csv('t3.csv')
final_df.to_csv('tf.csv')

