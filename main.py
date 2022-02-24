#%%
from utils import get_products
from params import params
import pandas as pd

df = get_products()
#%%
# import numpy as np
# import pandas as pd
# from mlxtend.preprocessing import TransactionEncoder
# from mlxtend.frequent_patterns import apriori, association_rules
# from sklearn import tree
# from params import params

# # products_cols = ['ced_last_products', 'ced_products']
# products_cols = ['ced_products']
# data = pd.read_csv('data/transaction.csv',usecols=params.COLS).fillna(-1).astype(str)

# # produse = pd.concat([data[i].str.split(';', expand=True) for i in products_cols], axis=1).fillna(-1).astype(str)
# data = data.apply(lambda x: x.astype(str).str.lower()).set_index([ i for i in params.COLS if i not in products_cols]).apply(lambda x: x.str.split(';').explode()).reset_index()    
# #%%
# name = 'interactions'
# with open(f'{name}.names', 'w') as file:
#   file.write('dsoodion.frequentSimilarPatternMining.similarityFunctions.IdentitySimilarityFunction\n\n')

#   for name, type, criteria in zip(params.COLS, params.type, params.criteria):
#     file.write(f'{name} dsoodion.frequentSimilarPatternMining.features.{type} dsoodion.frequentSimilarPatternMining.similarityFunctions.{criteria}\n')
# #%%
# #%%

# freq = {}
# prods = []
# base_thresh = -1
# for i in range(len(produse.keys())):
#   prods += list(produse.iloc[:,i].str.lower())

# for i in set(prods) - {'-1'}:
#   freq[i] = prods.count(i)/len(produse)
#   base_thresh = min(base_thresh, freq[i])

# #%%

# data = pd.concat([data.loc[:, ~data.columns.isin(['ced_last_products', 'ced_products', 'interests'])], data['ced_last_products'].str.split(';', expand=True), data['ced_products'].str.split(';', expand=True), data['interests'].str.split('|', expand=True)], axis=1).fillna(-1)
# data = data.apply(lambda x: x.astype(str).str.lower())
# raw = [list(data.iloc[i]) for i in range(len(data))]

# TE = TransactionEncoder()
# TE_data = TE.fit(raw).transform(raw)
# one_hot = pd.DataFrame(TE_data,columns=TE.columns_)
# one_hot = one_hot.replace(False,0).replace(True,1)


# rules = apriori(one_hot, min_support = 0.05, use_colnames = True, verbose = 1, low_memory=True)
# rules.to_csv('rules.csv')
# # %%

# # %%
# interests = data['interests'].str.split('|', expand=True)

# data = data.loc[:, ~data.columns.isin(['interests'])]
# data[[f'interest {i}' for i in range(len(interests))]] = interests

# # %%



# #%%

