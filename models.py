from distutils.command.build import build
from multiprocessing.spawn import prepare
import numpy as np
import pandas as pd, os
from params import params
from sklearn.metrics.pairwise import cosine_similarity

class RecSys:

  def __init__(self, data, products_cols):

      self.data = pd.read_csv('data/transaction.csv',usecols=params.COLS)
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
    self.data = self.data.apply(lambda x: x.astype(str).str.lower()).set_index([ i for i in params.COLS if i not in self.products_cols]).apply(lambda x: x.str.split(';').explode()).reset_index()    

    with open(f'{name}.names', 'w') as file:
      file.write('dsoodion.frequentSimilarPatternMining.similarityFunctions.IdentitySimilarityFunction\n\n')

    for name, type, criteria in zip(params.COLS, params.type, params.criteria):
      file.write(f'{name} dsoodion.frequentSimilarPatternMining.features.{type} dsoodion.frequentSimilarPatternMining.similarityFunctions.{criteria}\n')



  def getFrequentPatterns(self):
    os.system(f'java -jar STreeDCMiner.jar data/ input.data data/prueba0511/persona.names out {self.base_tresh} -1 -1')
    
 
  


