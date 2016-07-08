import pandas as pd
import util as dfmt
import logging
import timeit
from dateutil import relativedelta


class LcDataExtractor:
    """
    A simple data extractor that takes in a pandas data frame and then cleans it up and returns proper data frame back

    """

    @dfmt.timed
    @dfmt.memoize
    def create(self, file_name):
        self.potential_features = ['member_id', 'annual_inc', 'application_type', 'delinq_2yrs', 'delinq_amnt',
                                   'desc', 'dti', 'earliest_cr_line', 'emp_length', 'grade', 'home_ownership',
                                   'inq_last_6mths', 'installment',
                                   'issue_d', 'int_rate', 'last_credit_pull_d', 'loan_amnt', 'loan_status',
                                   'mths_since_last_delinq', 'open_acc', 'pub_rec', 'revol_bal', 'revol_util',
                                   'sub_grade', 'total_acc', 'verification_status', 'pub_rec_bankruptcies']

        normalizers = {'annual_inc': self.parse_annual_inc,
                       'annual_inc_joint': self.parse_annual_inc,
                       'delinq_2yrs': self.parse_delinq_2yrs,
                       'desc': self.parse_desc,
                       'dti': self.parse_dti,
                       'emp_length': self.parse_emp_length,
                       'earliest_cr_line': self.parse_earliest_cr_line,
                       'inq_last_6mths': self.parse_inq_last_6mths,
                       'int_rate': self.parse_int_rate,
                       'last_credit_pull_d': self.parse_last_credit_pull_d,
                       'loan_amnt': self.parse_loan_amnt,
                       'loan_status': self.parse_loan_status,
                       'mths_since_last_delinq': self.parse_mths_since_last_delinq,
                       'open_acc': self.parse_open_acc,
                       'pub_rec': self.parse_pub_rec,
                       'revol_bal': self.parse_revol_bal,
                       'revol_util': self.parse_revol_util,
                       'total_acc': self.parse_total_acc,
                       'pub_rec_bankruptcies': self.parse_pub_rec_bankruptcies}

        csv_df = pd.read_csv(file_name, skiprows=1, skipfooter=2, engine='python')
        df = csv_df[self.potential_features]

        for c in self.potential_features:
            f = lambda: self.identity(df)
            if c in normalizers:
                f = normalizers[c](df)
            else:
                f()

        self.create_new_features(df)
        return df

    def identity(self, df):
        return df

    @dfmt.timed
    def parse_annual_inc(self, df):
        df.annual_inc = df.annual_inc.fillna(0.0).astype(float)

    @dfmt.timed
    def parse_delinq_2yrs(self, df):
        df.delinq_2yrs = df.delinq_2yrs.fillna(0).astype(int)

    @dfmt.timed
    def parse_delnq_amt(self, df):
        df.delinq_amnt = df.delinq_amnt.fillna(0.0).astype(float)

    @dfmt.timed
    def parse_loan_amnt(self, df):
        df.loan_amnt = df.loan_amnt.fillna(df.loan_amnt.mean()).astype(float)

    @dfmt.timed
    def parse_desc(self, df):
        df.desc_length = df.desc.map(lambda x: dfmt.ret_string_len_if_str_zero_ifnot(x))

    @dfmt.timed
    def parse_dti(self, df):
        """
        Just for dti, I will use the average since there is only one row.
        :param df:
        :return:
        """
        df.dti = df.dti.astype(float).fillna(df.dti.mean())

    @dfmt.timed
    def parse_earliest_cr_line(self, df):
        # logging.debug(df.earliest_cr_line.item())
        df.earliest_cr_line = df.earliest_cr_line.map(lambda x: dfmt.convert_to_date(x))

    @dfmt.timed
    def parse_last_credit_pull_d(self, df):
        df.last_credit_pull_d = df.last_credit_pull_d.map(lambda x: dfmt.convert_to_date(x))

    @dfmt.timed
    def parse_emp_length(self, df):
        df.emp_length = df.emp_length.map(lambda x: dfmt.convert_less_than_yr_to_zero_or_num_otherwise(x))

    @dfmt.timed
    def parse_inq_last_6mths(self, df):
        df.inq_last_6mths = df.inq_last_6mths.fillna(df.inq_last_6mths.mean()).astype(int)

    @dfmt.timed
    def parse_int_rate(self, df):
        df.int_rate = df.int_rate.map(lambda x: dfmt.parse_float_with_percent(x))

    @dfmt.timed
    def parse_issue_d(self, df):
        df.issue_d = df.issue_d.map(lambda x: dfmt.convert_to_date(x)).fillna(df.issue_d.mean())

    @dfmt.timed
    def parse_loan_status(self, df):
        default_status = {'Fully Paid': 1, 'Charged Off': 0, 'Current': 1, 'In Grace Period': 0,
                          'Late (31-120 days)': 0, 'Default': 0,
                          'Does not meet the credit policy. Status:Fully Paid': 1,
                          'Does not meet the credit policy. Status:Charged Off': 0, 'Late (16-30 days)': 0}
        df['Target'] = df.loan_status.map(default_status)

    @dfmt.timed
    def parse_mths_since_last_delinq(self, df):
        df.mths_since_last_delinq = df.mths_since_last_delinq.fillna(0).astype(int)

    @dfmt.timed
    def parse_mths_since_last_record(self, df):
        df.mths_since_last_record = df.mths_since_last_record.fillna(0).astype(int)

    @dfmt.timed
    def parse_open_acc(self, df):
        df.open_acc = df.open_acc.fillna(0).astype(int)

    @dfmt.timed
    def parse_pub_rec(self, df):
        df.pub_rec = df.pub_rec.fillna(0).astype(int)

    @dfmt.timed
    def parse_revol_bal(self, df):
        df.revol_bal = df.revol_bal.fillna(0.0).astype(float)

    @dfmt.timed
    def parse_revol_util(self, df):
        df.revol_util = df.revol_util.map(lambda x: dfmt.parse_float_with_percent(x))

    @dfmt.timed
    def parse_total_acc(self, df):
        df.total_acc = df.total_acc.fillna(0).astype(int)

    @dfmt.timed
    def parse_verification_status(self, df):
        v_status = {'Not Verified': 'NV', 'Verified': 'V', 'Source Verified': 'SV'}
        df.verification_status = df.verification_status.map(v_status)

    @dfmt.timed
    def parse_pub_rec_bankruptcies(self, df):
        df.pub_rec_bankruptcies = df.pub_rec_bankruptcies.fillna(0.0).astype(int)

    @dfmt.timed
    def create_new_features(self, df):
        ##Drop the loan status , use the target variable ...as the target.
        df.drop('loan_status', axis=1, inplace=True)
        df['credit_length'] = df.apply(lambda row: dfmt.find_length_diff_in_months(row['issue_d'],row['earliest_cr_line']),axis=1)


