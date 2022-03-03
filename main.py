#%%
from utils import get_products, get_customers, build_products_association
from file_read_backwards import FileReadBackwards
from utils import get_orders, get_categories, get_profiling
from params import params
import pandas as pd, numpy as np
import itertools
import xml.etree.ElementTree 
import json
import os

get_products()
get_customers()
get_orders()
get_categories()
get_profiling()
# %%
