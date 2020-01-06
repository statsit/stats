import unittest
import pandas as pd
import numpy as np

from src.stats import Stats


def genDataFrame(size: int)-> pd.DataFrame:
    try:
        if size%20 !=0:
            raise ValueError("The size must be in 20, or any number that can be divided by 20")
        data = np.arange(size).reshape(5,4)
        colName = ['col one', 'col two', 'col three', 'col four']
        return pd.DataFrame(data, columns=colName)
    except ValueError as e:
        return e
    
data = genDataFrame(20)
stats = Stats(data)

class TestStats(unittest.TestCase):
        
    
    def test_checkFeatureMissingValues(self):
        result = ['colone', 'coltwo', 'colthree', 'colfour']
        self.assertEqual(self.stats.removeSpaceHeader(), result, "Failed")
        
    def test_checkFeatureMissingValues(self):
        result = {'col one':'0.0%', 'col two':'0.0%', 'col three':'0.0%', 'col four':'0.0%'}
        self.assertEqual(stats.checkFeatureMissingValues(), result, "Failed")
        
if __name__=='__main__':
    unittest.main()
        
        
    
    
    