from params import params
import xml.etree.ElementTree 

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
  df = {'id':[], 'categories':[], 'name':[], 'price':[], 'type':[]}
  depth_attribute = {'categories':2, 'name':1, 'price':0, 'type':0}

  for child in tree[0]:
    df['id'].append(child.attrib['id'])

  df['id'] = df['id'][:10]###

  print('Fetching Products Data')
  perc = 0
  for index, i in enumerate(df['id']):
    if index/len(df['id']) - perc >= 1:
      perc = index/len(df['id'])
      print(f'\r{perc*100}% Fetched', end = "")

    try:
      tree = prestashop.get('products',  resource_id=i)
    except:
      for j in depth_attribute.keys():
        df[j].append(None)
      continue

    for j in depth_attribute.keys():
      node = getChildDataByName('categories', tree, [])
      if node[0] == False:
        df[j].append(None)
      else:
        getChildsInfo(node[1], 0, depth_attribute[j])
        if j != 'categories':
          df[j].append(values[0])
        else: df[j].append(values.copy())
        values.clear()
    print('\n')
  return df