# #%% segments by hyperparameters
# import pandas as pd
# import numpy as np
# from tools.utils import compute_segments, build_products_association

# index = 93606835
# ta = 0.1

# with open(f'log_co={ta}.txt', 'a') as file:

#   association, mark_co = build_products_association(index, ta, True)
#   _, _, entries = compute_segments( index, threshold = 1, product_assosiation=ta)
#   df = pd.read_csv('data/products.csv')

#   file.write( f"{'*'*5}  {index}  {'*'*5}\t{df[df['id'] == index].iloc[0]['name']}\n\n{'*'*5}  Entries for mining: {entries} {'*'*5}\n\n{'*'*5}  Associations  {'*'*5}\n\n")

#   for i in association:
#     if i is not None:
#       file.write(f"{'[*]' if i in mark_co else '  '}\t{i}\t{df[df['id'] == int(i)].iloc[0]['name']}\n")
 
#   file.write(f"\n\n")
#   for tr in [0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]:
  
#     file.write(f"{'*'*3}\tminimun-support: {tr}\tminimun-coocurrence frequency: {ta}\t{'*'*3}\n\n")
#     segments, _, _ = compute_segments( index, threshold = tr, product_assosiation=ta)
#     for i in segments:
#       file.write(f'{i}\n')
#     file.write('\n\n')


# #%% 

# # %% SImilarity
# from models.models import Encoder
# import csv, numpy as np, pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity

# with open('similarity.csv', 'wt', newline='', encoding="utf-8") as csvfile:
#   spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#   spamwriter.writerow(['id','name','similarity', 'similar'])

#   data = pd.read_csv('data/products.csv', usecols=['id', 'name'])
#   model = Encoder(weigths_source='offline')
#   descriptions = model.encode(csv_file='data/products.csv')
#   ids = list(descriptions.keys())
#   del model

#   F = [descriptions[i] for i in ids]
#   F = cosine_similarity(np.array(F))

#   for i in range(len(ids)):

#     top = [(F[i][j], ids[j]) for j in range(F.shape[1]) if i != j]
#     top.sort(reverse = True)
#     top = top[:10]
#     iname = data[data['id'] == int(ids[i])].iloc[0]['name']

#     for j in top:
#       spamwriter.writerow([ids[i],iname, j[0], data[data['id'] == int(j[1])].iloc[0]['name']])
# %%

from tools.utils import *

df = {'id':[], 'id_customer':[], 'cart_rows':[], 'date_add':[], 'date_upd':[]}
target = {'cart_rows': 'product_id'}
depth_attribute = { 'id_customer':0, 'date_add':0, 'date_upd':0, 'cart_rows':2}

get_data('carts', df, depth_attribute, resource_details='orders', target=target)

# # %%
# from tools.params import params
# from prestapyt import PrestaShopWebService

# prestashop = PrestaShopWebService('https://h-dsieblamalaga.com/api', params.WEBSERVICE_KEY)
# # tree = prestashop.get(resource)
# # %%
# z = prestashop.search('carts', options={'filter[id]': '[1|5]'})
# # %%
