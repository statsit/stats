import pandas as pd
from collections import Counter
from dataclasses import dataclass


@dataclass
class Stats:
    df: pd.DataFrame

    def removeSpaceHeader(self) -> list:
        try:
            if type(self.df) != pd.DataFrame:
                raise ValueError('input value is not pandas dataframe')
            features = self.df.columns
            featuresWithNoSpace = [''.join(j for j in i if not j.isspace()) for i in features]
            self.df.columns = features
            return featuresWithNoSpace
        except ValueError as e:
            return e

    def checkFeatureMissingValues(self) -> dict:
        try:
            if type(self.df) != pd.DataFrame:
                raise ValueError('input value is not pandas dataframe')

            missingValue = dict(self.df.isnull().sum())
            return {col : f'{round((missingValue[col]/len(self.df))*100,2)}%' for col in missingValue}
        except ValueError as e:
            return e

    def color_negative_red(self, val) -> str:
        """
        Takes a scalar and returns a string with
        the css property Zfghjkl
        strings, black otherwise.
        """
        color = 'red' if val < 0 else 'black'
        return 'color: %s' % color

    def upper_lower_range(self, num: int) -> dict:
        std_dict = dict(self.df.std())
        mean_dict = dict(self.df.mean())
        result = {col: [round((mean_dict[col] - (num * std_dict[col])), 2),
                        round((mean_dict[col] + (num * std_dict[col])), 2)]
                  for col in std_dict}
        return result

    def summary_neg(self) -> pd.DataFrame:
        return (self.df.describe()
                .style
                .format('{:.0f}')
                .applymap(self.color_negative_red)
                .set_caption("Statistical Summary with negative highlight"))

    def summary_bar(self) -> pd.DataFrame:
        return (self.df.describe()
                .style
                .format('{:.2f}')
                .bar(color=['red', 'lightgreen'], align='zero')
                .set_caption("Statistical Summary with Bar Chart"))

    def summary(self, subset: list = None) -> pd.DataFrame:
        return (self.df.describe()
                .style
                .format('{:.2f}')
                .highlight_max(subset=subset, color='lightgreen')
                .highlight_min(subset=subset, color="red")
                .set_caption("Statistical Summary"))

    def impute(self, col: str) -> str:
        missing_no = len(self.df[self.df[col].isnull()])
        if self.df[col].dtype == 'O':
            new_df = self.df[self.df[col].notnull()]
            mode = Counter(new_df[col]).most_common(1)[0]
            print(mode)
            self.df[col] = self.df[col].fillna(mode[0])
            return f'{missing_no} missing values have been imputed in column {col} with {mode[0]}'
        else:
            avg = self.df[col].mean()
            self.df[col] = self.df[col].fillna(avg)
            return f'Missing value has been imputed with {avg}'

    def remove_duplicate(self):
        no_of_dup = self.df.duplicated().sum()
        if no_of_dup > 0:
            dup = len(self.df[self.df.duplicated()
                              ].drop_duplicates(keep='first'))
            rem_dup = no_of_dup - dup
            self.df = self.df.drop_duplicates(keep='first')
            return f'{rem_dup} has been removed'
        else:
            return f'there is no duplicates'

    def lower_cases(self):
        for col in self.df.columns:
            self.df[col] = self.df[col].apply(lambda x: x.lower())
