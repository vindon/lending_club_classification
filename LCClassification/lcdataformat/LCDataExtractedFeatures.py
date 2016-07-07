import pandas as pd
import dataformats as dfmt


class LcDataExtractor:
    """
    A simple data extractor that takes in a pandas data frame and then cleans it up and returns proper data frame back

    """

    def create(self, df):
        self.potential_features = ['annual_inc', 'annual_inc_joint', 'application_type', 'delinq_2yrs', 'delinq_amnt',
                                   'desc', 'dti', 'earliest_cr_line', 'emp_length','grade','home_ownership','inq_last_6mths','installment',
                                   'issue_d','int_rate',
                                   'last_credit_pull_d', 'last_fico_range_high', 'last_fico_range_low',
                                   'application_type', 'fico_range_high', 'fico_range_low', 'earliest_cr_line',
                                   'loan_amnt', 'funded_amnt', 'funded_amnt_inv', 'term', 'int_rate', 'grade',
                                   'installment', 'sub_grade', 'emp_length', 'home_ownership', 'annual_inc',
                                   'mths_since_last_delinq', 'inq_last_6mths', 'open_acc', 'open_acc_6m', 'open_il_12m',
                                   'pub_rec_bankruptcies', 'pub_rec', 'revol_util', 'delinq_2yrs', 'mo_sin_old_il_acct',
                                   'mo_sin_old_rev_tl_op', 'mo_sin_rcnt_rev_tl_op', 'mo_sin_rcnt_tl', 'mort_acc',
                                   'mths_since_last_delinq', 'num_accts_ever_120_pd', 'num_tl_30dpd']

        normalizers = {'annual_inc': self.parse_annual_inc(df), 'annual_inc_joint': self.parse_annual_inc(df),
                       'delinq_2yrs': self.parse_delinq_2yrs(df), 'desc': self.parse_desc(df),
                       'dti': self.parse_dti(df), 'emp_length': self.parse_emp_length(df),
                       'earliest_cr_line': self.parse_earliest_cr_line(df), 'inq_last_6mths':self.parse_inq_last_6mths(df), 'int_rate':self.parse_int_rate(df)}

    def parse_annual_inc(self, df):
        df.annual_inc = df.annual_inc.astype(float).fillna(0.0)

    def parse_delinq_2yrs(self, df):
        df.delinq_2yrs = df.delinq_2yrs.astype(int).fillna(0)

    def parse_delnq_amt(self, df):
        df.delinq_amnt = df.delinq_amnt.astype(float).fillna(0.0)

    def parse_desc(self, df):
        df.desc_length = df.desc.map(lambda x: len(x))

    def parse_dti(self, df):
        """
        Just for dti, I will use the average since there is only one row.
        :param df:
        :return:
        """
        df.dti = df.dti.astype(float).fillna(df.dti.mean())

    def convert_to_period(x):
        if x is not None:
            return pd.Period(x, 'M')

    def parse_earliest_cr_line(self, df):
        df.earliest_cr_line = df.earliest_cr_line.map(lambda x: self.parse_earliest_cr_line(x)).fillna(
            df.earliest_cr_line.mean())

    def parse_emp_length(self, df):
        df.emp_length = df.emp_length.map(lambda x: dfmt.convert_less_than_yr_to_zero_or_num_otherwise(x))

    def parse_inq_last_6mths(self, df):
        df.inq_last_6mths =  df.inq_last_6mths.astype(int).fillna(df.inq_last_6mths.mean())

    def parse_int_rate(self, df):
        df.int_rate =  df.int_rate.map(lambda x:dfmt.format_interest_rate(x))

    def parse_issue_d(self,df):
        df.issue_d =  df.issue_d.map(lambda x: self.convert_to_period(x)).fillna(df.issue_d.mean())


