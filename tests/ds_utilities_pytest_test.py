import pandas as pd
from my_lambdata.ds_utilities import enlarge, get_business_info


def test_business_info():
    test_df = get_business_info('fast food', 'denver', 'FL')
    assert len(test_df.iloc[0]['Phone_No']) >= 10

def test_elarge():
    assert enlarge(3) == 300