#%%
from utils import get_products
from params import params
import pandas as pd

get_products()
# import xml.etree.ElementTree 

# from prestapyt import PrestaShopWebService, PrestaShopWebServiceDict
# prestashop = PrestaShopWebService('https://h-dsieblamalaga.com/api', params.WEBSERVICE_KEY)
# #%%
# tree = prestashop.get('customers')
# df = {'id':[], 'firstname': [], 'lastname':[], 'id_gender':[], 'birthday':[], 'is_guest':[], 'id_shop_group':[]}
# depth_attribute = {'categories':2, 'name':1, 'price':0, 'type':0}

# for child in tree[0]:
#   df['id'].append(child.attrib['id'])
# #%%

# tree = prestashop.get('customers/1')
# # %%
# print(xml.etree.ElementTree.dump(tree))
# # %%
