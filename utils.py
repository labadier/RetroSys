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


def getChildsInfo(node, level, depth):

  if level == depth:
    values.append(node.text)
    return

  for i in node:
    getChildsInfo(i, level+1, depth)

def get_products():
  
  from prestapyt import PrestaShopWebService, PrestaShopWebServiceDict
  prestashop = PrestaShopWebService('https://h-dsieblamalaga.com/api', params.WEBSERVICE_KEY)

  tree = prestashop.get('products')
  df = {'id':[], 'categories':[], 'name':[], 'price':[], 'type':[], 'accessories':[]}
  depth_attribute = {'categories':2, 'name':1, 'price':0, 'type':0, 'accessories':2}
  df['id'] = [child.attrib['id'] for child in tree[0]]

  print('Fetching Products Data')
  perc = 0
  for index, i in enumerate(df['id']):
    if index/len(df['id']) - perc >= 0.01:
      perc = index*1.0/len(df['id'])
      print(f'\r{perc*100.0:.2f}% Fetched', end = "")

    try:
      tree = prestashop.get('products',  resource_id=i)
    except:
      for j in depth_attribute.keys():
        df[j].append(None)
      continue

    for j in depth_attribute.keys():
      node = getChildDataByName(j, tree, [])

      if node[0] == False:
        df[j].append(None)
      else:
        getChildsInfo(node[1], 0, depth_attribute[j])
        if j not in ['categories', 'accessories'] :
          df[j].append(values[0])
        else: df[j].append(';'.join(values))
        values.clear()
  print(f'\r100% Fetched')
  df = pd.DataFrame(df)
  df.to_csv('data/products.csv')
