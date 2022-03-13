import numpy as np, pandas as pd, os, torch
from params import params
from sklearn.metrics.pairwise import cosine_similarity
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoModel, AutoTokenizer
import html2text

class RawDataset(Dataset):

  def __init__(self, csv_file):
    self.data_frame = pd.read_csv(csv_file, usecols=['id', 'description', 'description_short'], dtype=str).fillna('-1')
    self.data_frame['description'] = pd.DataFrame.apply(self.data_frame, lambda row: html2text.html2text(row['description']).replace('*', '') if row['description'] != '-1' else row['description_short'], axis=1)


  def __len__(self):
    return len(self.data_frame)

  def __getitem__(self, idx):
    if torch.is_tensor(idx):
      idx = idx.tolist()
    batch = self.data_frame.loc[idx, ['id', 'description']]
    
    
    return {'id':batch['id'].to_list() if len(batch.shape) > 1 else batch['id'], 'text':batch['description'].to_list() if len(batch.shape) > 1 else batch['description']}
 
def HuggTransformer(language, weigths_source):

  if weigths_source == 'online': 
    prefix = '' 
  else: prefix = 'data/'
 
  model = AutoModel.from_pretrained(os.path.join(prefix , params.langaugeModel[language]))
  tokenizer = AutoTokenizer.from_pretrained(os.path.join(prefix , params.langaugeModel[language]), do_lower_case=True, TOKENIZERS_PARALLELISM=True)

  return model, tokenizer

class Encoder(torch.nn.Module):

  def __init__(self, max_length = 150, language="EN", weigths_source='online') -> None:
    
    super(Encoder, self).__init__()
    self.max_length = max_length
    self.encoder, self.tokenizer = HuggTransformer(language, weigths_source)
    
    self.device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
    self.to(device=self.device)

  def forward(self, X):

    X = self.tokenizer(X, return_tensors='pt', truncation=True, padding=True, max_length=self.max_length).to(device=self.device)
    print(X)
    X = self.encoder(**X)[0] 
    return X[:,0]

  def encode(self, csv_file='products.csv'):
    self.eval()    
    loader = DataLoader(RawDataset(csv_file), batch_size=64, shuffle=False, num_workers=8)
 
    with torch.no_grad():
      out = None
      idxs = None
      for k, data in enumerate(loader, 0):
        torch.cuda.empty_cache() 
        inputs, idxs_out = data['text'], data['id']

        enc_out = self.forward(inputs)
        if k == 0:
          out = enc_out
          idxs = idxs_out
        else: 
          out = torch.cat((out, enc_out), 0)
          idxs = torch.cat((idxs, idxs_out), 0)

    out = out.cpu().numpy()
    del loader
    return {idxs[i]:out[i] for i in range(len(idxs))}


class RecSys:

  def __init__(self, data, products_cols):

      self.data = pd.read_csv('data/transaction.csv',usecols=params.profiling_cols)
      self.product_frequency = None
      self.base_tresh = None
      self.products_cols = products_cols
      self.prepareData()

  def prepareData(self):

    produse = pd.concat([self.data[i].str.split(';', expand=True) for i in self.products_cols], axis=1).fillna(-1).astype(str)

    self.product_frequency = {}
    prods = []
    base_thresh = -1
    for i in range(len(produse.keys())):
      prods += list(produse.iloc[:,i].str.lower())

    for i in set(prods) - {'-1'}:
      self.product_frequency[i] = prods.count(i)/len(produse)
      base_thresh = min(base_thresh, self.product_frequency[i])

  def buildInputFile(self, name):
    self.data = self.data.apply(lambda x: x.astype(str).str.lower()).set_index([ i for i in params.profiling_cols if i not in self.products_cols]).apply(lambda x: x.str.split(';').explode()).reset_index()    

    with open(f'{name}.names', 'w') as file:
      file.write('dsoodion.frequentSimilarPatternMining.similarityFunctions.IdentitySimilarityFunction\n\n')

    for name, type, criteria in zip(params.profiling_cols, params.type, params.criteria):
      file.write(f'{name} dsoodion.frequentSimilarPatternMining.features.{type} dsoodion.frequentSimilarPatternMining.similarityFunctions.{criteria}\n')

  def getFrequentPatterns(self):
    os.system(f'java -jar STreeDCMiner.jar data/ input.data data/prueba0511/persona.names out {self.base_tresh} -1 -1')
    
 
  


#%%
# import numpy as np
# import pandas as pd
# from mlxtend.preprocessing import TransactionEncoder
# from mlxtend.frequent_patterns import apriori, association_rules
# from sklearn import tree
# from params import params

# # products_cols = ['ced_last_products', 'ced_products']
# products_cols = ['ced_products']
# data = pd.read_csv('data/transaction.csv',usecols=params.profiling_cols).fillna(-1).astype(str)

# # produse = pd.concat([data[i].str.split(';', expand=True) for i in products_cols], axis=1).fillna(-1).astype(str)
# data = data.apply(lambda x: x.astype(str).str.lower()).set_index([ i for i in params.profiling_cols if i not in products_cols]).apply(lambda x: x.str.split(';').explode()).reset_index()    
# #%%
# name = 'interactions'
# with open(f'{name}.names', 'w') as file:
#   file.write('dsoodion.frequentSimilarPatternMining.similarityFunctions.IdentitySimilarityFunction\n\n')

#   for name, type, criteria in zip(params.profiling_cols, params.type, params.criteria):
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

