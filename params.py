'''
  NeighborhoodComparationCriteria $epsilon =>> abs(a-b) <= epsilon
  RatioNeighborhoodComparationCriteria	$epsilon =>> abs(a-b)<= epsilon*(max-min)
  IdentityComparationCriteria   =>> a == b
'''
class params:

  WEBSERVICE_KEY = 'D2YF2A9Z2DI38ZCJRKGXWBIN27Q6TTKZ'

  date_featrues = ['birthday']
  COLS = ['ced_newsletter_subs', 'ced_bill_post_code', #'ced_last_products', 
    'ced_products', 
    'ced_avg_order_value', 'ced_last_order_date', 'ced_avg_days_bt_orders', 'gender', 'age', 'lang', 'interests', 'personality', 
    'values_h', 'needs', 'openness', 'conscientiousness', 'extraversion',
    'agreeableness', 'neuroticism']

  type = ['CategoricalFeature', 'IntegerFeature',  'CategoricalFeature', 
    'IntegerFeature', 'IntegerFeature', 'IntegerFeature', 'CategoricalFeature', 'IntegerFeature', 'CategoricalFeature', 'CategoricalFeature', 
    'CategoricalFeature', 'CategoricalFeature', 'IntegerFeature', 'IntegerFeature', 'IntegerFeature', 'IntegerFeature',
    'IntegerFeature', 'IntegerFeature']

  criteria = ['IdentityComparationCriteria', 'IdentityComparationCriteria', 'IdentityComparationCriteria', 
    'NeighborhoodComparationCriteria 3', 'IdentityComparationCriteria', 'NeighborhoodComparationCriteria 3', 
    'IdentityComparationCriteria', 'NeighborhoodComparationCriteria 2', 'IdentityComparationCriteria', 
    'IdentityComparationCriteria', 'IdentityComparationCriteria', 'IdentityComparationCriteria',
    'NeighborhoodComparationCriteria 3', 'NeighborhoodComparationCriteria 3', 'NeighborhoodComparationCriteria 3', 
    'NeighborhoodComparationCriteria 3', 'NeighborhoodComparationCriteria 3', 'NeighborhoodComparationCriteria 3']

#'ced_categories', 'ced_last_categories'