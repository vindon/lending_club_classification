import pandas as pd


class LcDataExtractor:
    """
    A simple data extractor that takes in a pandas data frame and then cleans it up and returns proper data frame back

    """
    def create(self,df):

        self.potential_features = ['all_util','acc_now_delinq','acc_open_past_24mths','bc_util','issue_d','last_credit_pull_d','last_fico_range_high','last_fico_range_low','application_type','fico_range_high','fico_range_low','earliest_cr_line','loan_amnt','funded_amnt','funded_amnt_inv','term','int_rate','grade','installment','sub_grade','emp_length','home_ownership','annual_inc','mths_since_last_delinq','inq_last_6mths','open_acc','open_acc_6m','open_il_12m','pub_rec_bankruptcies','pub_rec','revol_util','delinq_2yrs','mo_sin_old_il_acct','mo_sin_old_rev_tl_op','mo_sin_rcnt_rev_tl_op','mo_sin_rcnt_tl','mort_acc','mths_since_last_delinq','num_accts_ever_120_pd','num_tl_30dpd']
