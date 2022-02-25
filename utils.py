from dbm import dumb
from params import params
import xml.etree.ElementTree 
import pandas as pd

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
  
  df['id'] = [child.attrib['id'] for child in tree[0]]

  date_features = dict()
  for i in depth_attribute:
    if i in params.date_featrues:
      for j in ['year', 'month', 'day']:
        date_features['.'.join([i, j])] = []
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
        df[j].append(None)
      continue

    for j in depth_attribute.keys():
      node = getChildDataByName(j, tree, [])

      if node[0] == False:
        df[j].append(None)
        continue
    
      getChildsInfo(node[1], 0, depth_attribute[j], (target[j] if j in target.keys() else None))
      
      if df[j] == 'date':
        for k, prop in enumerate(['year', 'month', 'day']):
          date_features[f'{j}.{prop}'].append(';'.join([x.split('-')[k] for x in values if x is not None]))
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
