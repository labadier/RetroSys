from params import params
import xml.etree.ElementTree 
import pandas as pd, numpy as np
import itertools, os
from file_read_backwards import FileReadBackwards
import json

values = []

def getChildDataByName(name, tree, path):

  for i, child in enumerate(tree):
    if child.tag == name:
      return (True, tree[i])
    ans = getChildDataByName(name, tree[i], path + [i])
    if ans[0] == True:
      return (True, ans[1])

  return (False, [])


def getChildsInfo(node, level, depth, target = None):

  if level == depth and (target == None or node.tag == target):
    values.append(node.text)
    return

  for i in node:
    getChildsInfo(i, level+1, depth, target)

def get_data(resource, df, depth_attribute, resource_details, target = {}):
  
  from prestapyt import PrestaShopWebService
  prestashop = PrestaShopWebService('https://h-dsieblamalaga.com/api', params.WEBSERVICE_KEY)
  tree = prestashop.get(resource)
  
  df['id'] = [child.attrib['id'] for child in tree[0][:99]]

  date_features = dict()
  for i in depth_attribute:
    if i in params.date_featrues:
      for j in ['year', 'month', 'day']:
        date_features['_'.join([i, j])] = []
      df[i] = 'date'

  print(f'Fetching {resource} data')
  perc = 0
  for index, i in enumerate(df['id']):
    if index/len(df['id']) - perc >= 0.01:
      perc = index*1.0/len(df['id'])
      print(f'\r{perc*100.0:.2f}% Fetched', end = "")

    try:
      tree = prestashop.get(resource_details,  resource_id=i)
    except:
      for j in depth_attribute.keys():
        if df[j] != 'date':
          df[j].append(None)
        else:
          for prop in ['year', 'month', 'day']:
            date_features[f'{j}_{prop}'].append(None)
      continue

    for j in depth_attribute.keys():
      node = getChildDataByName(j, tree, [])

      if node[0] == False:
        df[j].append(None)
        continue
    
      getChildsInfo(node[1], 0, depth_attribute[j], (target[j] if j in target.keys() else None))
      
      if df[j] == 'date':
        for k, prop in enumerate(['year', 'month', 'day']):
          date_features[f'{j}_{prop}'].append(';'.join([x.split('-')[k] for x in values if x is not None]))
      elif depth_attribute[j] < 2:
        df[j].append(values[0])
      else: df[j].append(';'.join(values))
      values.clear()

  print(f'\r100% Fetched')
  for i in depth_attribute:
    if df[i] == 'date':
      df.pop(i)
  df.update(date_features)
  df = pd.DataFrame(df)
  df.to_csv(f'data/{resource}.csv')


def get_profiling(step=2):

  from mautic import MauticBasicAuthClient, Contacts
  import csv
  mautic = MauticBasicAuthClient('https://harley.identiaicdp.com/', 'rafael', "Rafael*12345")
  contacts = Contacts(client=mautic)

  with open('data/perfilado.csv', 'wt', newline='', encoding="utf-8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["id"] + params.profiling_cols + ['ach', 'ben', 'con', 'dir', 'hed', 'pow', 'sec', 'sti', 'tra', 'uni', 'cha', 'clo', 'cur', 'est', 'exc', 'exp', 'har', 'ide', 'lib', 'lov', 'pra', 'str'])
    
    index = 0
    print("Fetching Profiling Data")
    while True:
      contacts_data =  contacts.get_list(search="segment:contactos-perfilados", start=index, limit=step, order_by="firstname")["contacts"].values()
      if not len(contacts_data):
        break
      for data in contacts_data:
        values = [(x['label'], x['count']) for x in json.loads(data['fields']['core']['all_values']['value'])['values_all']];values.sort()
        needs = [(x['label'], x['count']) for x in json.loads(data['fields']['core']['all_values']['value'])['needs_all']];needs.sort()
        spamwriter.writerow([data["id"]] + [data["fields"]["core"][field]["value"] for field in params.profiling_cols] + \
                              [item[1] for item in values] +  [item[1] for item in needs])
      break

  
def build_products_association(index = 5167697, threshold = 0.3):

  df = pd.read_csv('data/products.csv')
  product = df[df['id'] == index]
  if not len(product):
    return []
  assosiations = list(map(int, (product.iloc[0]['accessories'] if product['accessories'].isnull().values.any() == False else '-1').split(';')))
  categories = list(map(int, (product.iloc[0]['categories'] if product['categories'].isnull().values.any() == False else '-1').split(';')))

  df = pd.read_csv('data/categories.csv')
  for i in categories:
    category = df[df['id'] == i]
    assosiations += list(map(int, (category.iloc[0]['products'] if category['products'].isnull().values.any() == False else '-1').split(';')))
  assosiations = set(assosiations) 

  data = pd.read_csv('data/orders.csv',usecols=['order_rows'])
  data = data[data['order_rows'].str.contains(f';{index}|{index};')]['order_rows'].str.split(';', expand=True).fillna(-1).astype(str)

  frequencies = {}
  for i in data.iloc:
    for j in set(i.to_list()):
      if j not in frequencies:
        frequencies[j] = 1
      else: frequencies[j] += 1

  assosiations |= set([i for i in frequencies if frequencies[i]/len(data) >= threshold])

  # print(data)
  # tokens = list(set(itertools.chain.from_iterable([data[i].to_list() for i in data.columns])))
  # tokens = {x:y for y, x in enumerate(tokens)}

  # with open(f'data/data.names', 'w') as file:
  #   file.write('dsoodion.frequentSimilarPatternMining.similarityFunctions.IdentitySimilarityFunction\n')

  #   for token in tokens.keys():
  #     file.write(f'{token} dsoodion.frequentSimilarPatternMining.features.IntegerFeature dsoodion.frequentSimilarPatternMining.similarityFunctions.IdentityComparationCriteria\n')

  # with open(f'data/data.data', 'w') as file:
  #   for i in data.iloc:
  #     z = np.zeros(len(tokens), dtype=int)
  #     z[[tokens[x] for x in i.to_list()]] = 1
  #     z = '\t'.join(z.astype(str))
  #     file.write(f'{z}\n')
  
  # os.system(f'java -jar tools/STreeDCMiner.jar data/ data.data data.names out {threshold} -1 -1')
      
  # with open(f'data/data.data.data.namesout.STreeDCMiner_{threshold}_-1__-1', 'r') as file:

  #   patterns = False
  #   for i, line in enumerate(file):
  #     patterns ^= (patterns and line == "\n")

  #     if patterns and line.count(f'{index}=1') and line.count('=1') > 1:
  #       assosiations |= set([int(x[:-2]) for x in line.split(" ")[:-3] if x.count("=1") and x != f'{index}=1'])
  #     patterns |= (not patterns and line == "Frequent SubDescriptions: \n")      
  assosiations.remove(-1)
  assosiations.remove(index)
  return assosiations

def compute_segments( index, threshold = 0.6):
  
  associations = [index] + build_products_association(index)

  data = pd.read_csv('data/orders.csv',usecols=['id_customer', 'order_rows'])
  data_entries = []
  for entry in associations:
    data_entries += data[data['order_rows'].str.contains(f';{entry}|{entry};')]['id_customer'].to_list()

  data_entries_set = list(set(data_entries))

  data = pd.read_csv('data/perfilado.csv')
  psycologyc_data = data[data['id'].isin(data_entries_set)] 
  data = pd.read_csv('data/customers.csv',usecols=['id', 'id_gender', 'is_guest', 'birthday_year','birthday_month'],dtype=str)
  data["id"] = data["id"].astype(int)
  data = pd.merge(psycologyc_data, data[data['id'].isin(data_entries_set)])[["id"] + params.mining_cols]

  with open(f'data/data.names', 'w') as file:
    file.write('dsoodion.frequentSimilarPatternMining.similarityFunctions.IdentitySimilarityFunction\n')
    for token, type, criteria in zip(params.mining_cols, params.mining_type, params.mining_criteria):
      file.write(f'{token} dsoodion.frequentSimilarPatternMining.features.{type} dsoodion.frequentSimilarPatternMining.similarityFunctions.{criteria}\n')

  with open(f'data/data.data', 'w') as file :
    for entry in data_entries:
      z = "\t".join(data[data["id"] == entry].iloc[0].astype(str).to_list()[1:])
      file.write(f'{z} \n')
      
  os.system(f'java -jar tools/STreeDCMiner.jar data/ data.data data.names out {threshold} -1 -1')

  segments = []
  with FileReadBackwards(f'data/data.data.data.namesout.STreeDCMiner_{threshold}_-1__-1', encoding="utf-8") as frb:
      foot = True; head = False
      topcover = -1
      for line in frb:

        if head:
          break

        splited = line.split(" ")[:-3]
        head |= (topcover > len(splited))

        if not foot and not head:
          topcover = len(splited)
          segments.append(splited)

        foot &= not (line == "")
        head |= (line == "Frequent SubDescriptions: " )

  return segments
  
def get_products():
  df = {'id':[], 'categories':[], 'name':[], 'price':[], 'type':[], 'accessories':[]}
  depth_attribute = {'categories':2, 'name':1, 'price':0, 'type':0, 'accessories':2}
  get_data('products', df, depth_attribute, resource_details='products')

def get_customers():
  df = {'id':[], 'firstname': [], 'lastname':[], 'id_gender':[], 'birthday':[], 'is_guest':[], 'id_shop_group':[], 'groups':[]}
  depth_attribute = {'firstname': 0, 'lastname':0, 'id_gender':0, 'birthday':0, 'is_guest':0, 'id_shop_group':0, 'groups':2}
  get_data('customers', df, depth_attribute, resource_details='customers')

def get_orders():
  df = {'id':[], 'id_cart':[], 'id_currency':[], 'id_customer':[], 'current_state':[], 'order_rows':[], 'total_paid':[], 'total_products':[]}
  target = {'order_rows': 'product_id'}
  depth_attribute = { 'id_cart':0, 'id_currency':0, 'id_customer':0, 'current_state':0, 'order_rows':2, 'total_paid':0, 'total_products':0}
  get_data('orders', df, depth_attribute, resource_details='orders', target=target)

def get_categories():
  df = {'id':[], 'products':[]}
  depth_attribute = {'products':2}
  get_data('categories', df, depth_attribute, resource_details='categories')
