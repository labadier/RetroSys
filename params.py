'''
  NeighborhoodComparationCriteria $epsilon =>> abs(a-b) <= epsilon
  RatioNeighborhoodComparationCriteria	$epsilon =>> abs(a-b)<= epsilon*(max-min)
  IdentityComparationCriteria   =>> a == b
'''
class params:

  WEBSERVICE_KEY = 'D2YF2A9Z2DI38ZCJRKGXWBIN27Q6TTKZ'

  date_featrues = ['birthday']
  profiling_cols = ['fan_value', "neuroticism", "agreeableness", "extraversion", "conscientiousness",
         "openness", "personality", "values_h", "needs", "interests"]
  langaugeModel = {"ES": "dccuchile/bert-base-spanish-wwm-cased", "EN": "vinai/bertweet-base"} # TODO  change bertweet for bert-base
  # mining_cols = ['fan_value', 'neuroticism', 'agreeableness', 'extraversion', 'conscientiousness', 'openness', 
  #      'personality', 'values_h', 'needs',
  #      'ach', 'ben', 'con', 'dir', 'hed', 'pow', 'sec', 'sti',
  #      'tra', 'uni', 'cha', 'clo', 'cur', 'est', 'exc', 'exp', 'har', 'ide',
  #      'lib', 'lov', 'pra', 'str', 'id_gender', 'is_guest', 'birthday.year',
  #      'birthday.month']

  # type = ['IntegerFeature']*6 + ['CategoricalFeature']*3 + ['IntegerFeature']*22 + ['CategoricalFeature']*4


  mining_cols = ['fan_value', 'neuroticism', 'agreeableness', 'extraversion', 'conscientiousness', 'openness', 
      'personality', 'values_h', 'needs', 'id_gender', 'is_guest', 'birthday_year', 'birthday_month']
  mining_type = ['CategoricalFeature'] + ['IntegerFeature']*5 + ['CategoricalFeature']*5 + ['IntegerFeature']*2

  mining_criteria = ['IdentityComparationCriteria'] + ['IdentityComparationCriteria']*5 + ['IdentityComparationCriteria']*5\
                    +['IdentityComparationCriteria 1', 'IdentityComparationCriteria 5']
