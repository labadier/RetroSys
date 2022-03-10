#%%
from utils import get_products, get_customers, compute_segments
from utils import get_orders, get_categories, get_profiling, log_mining
import argparse, sys


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
    for i in segments:
      print(i)
    # log_mining(index, segments, association, entries, tr, ta)

  if mode == 'fetch':
    # get_orders()
    # get_categories()
    # get_profiling()
    get_products()
    # get_customers()

# %%
