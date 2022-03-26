#%%

import pandas
from tools.params import params
from tools.utils import get_products, get_customers, compute_segments
from tools.utils import get_orders, get_categories, getProfiling
import argparse, sys, json, datetime



def check_params(args=None):
  parser = argparse.ArgumentParser(description='Language Model Encoder')
  
  parser.add_argument('-i', metavar='index', type=int, help='Product index to find segment for')
  parser.add_argument('-tr', metavar='thresh_rules', type=float, default = 0.2, help='Threshold for Support on Rules Mining ranginng in (0, 1]')
  parser.add_argument('-ta', metavar='thresh_asoci', type=float, default = 0.6, help='Threshold for Co-occurency on buying objects')
  parser.add_argument('-mode', metavar='mode', default='mine', help='Mode either mining segments or download data', choices=['mine', 'fetch'])
  
  return parser.parse_args(args)

if __name__ == '__main__':


  parameters = check_params(sys.argv[1:])

  tr = parameters.tr
  ta = parameters.ta
  mode = parameters.mode
  index = parameters.i

  if mode == 'mine':
    segments, association, entries = compute_segments( index, threshold = tr, product_assosiation=ta)
    
    json_out = []
    for pattern in segments:
      json_out.append([])
      for feature in pattern:
        feature = feature.split('=')
        feature_id = params.mining_cols.index(feature[0])
        if params.mining_criteria[feature_id].split()[0] == 'NeighborhoodComparationCriteria':
          json_out[-1].append({'name':feature[0], 'operator': '>', 'field':int(feature[0]),
          'filter':max(0, datetime.date.today().year - int(feature[1]) - 1 - int(params.mining_criteria[feature_id].split()[1])),
          'type': "number"})
          json_out[-1].append({'name':feature[0], 'operator': '<', 'field':int(feature[0]), 
          'filter':datetime.date.today().year - int(feature[1]) + 1 + int(params.mining_criteria[feature_id].split()[1]),
          'type': "number"})
        else: json_out[-1].append({'name':feature[0], 'operator': '=', 'field':feature[0],
          'type': 'select' if params.mining_type[feature_id] == "CategoricalFeature" else "number", 
          'filter': feature[1]})

    with open('output.json', 'w') as file:
      file.write(json.dumps(json_out))
  
    for i in segments:
        print(i)
    # log_mining(index, segments, association, entries, tr, ta)

  if mode == 'fetch':
    get_orders()
    get_categories()
    getProfiling(step=100)
    get_products()
    get_customers()
