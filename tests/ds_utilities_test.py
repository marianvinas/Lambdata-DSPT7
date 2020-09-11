import unittest
import pandas as pd
from my_lambdata.ds_utilities import get_business_info


class TestDsUtilityMethods(unittest.TestCase):

    def test_business_info(self):
        test_df = get_business_info('fast food', 'denver', 'FL')
        self.assertGreaterEqual(len(test_df.iloc[0]['Phone_No']), 10)


if __name__ == '__main__':
    unittest.main()