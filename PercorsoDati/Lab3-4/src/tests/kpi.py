import unittest 

import pandas as pd

from kpi.utils import compute_kpi
from config import PRODUCTION_PLANT

class TestKpi(unittest.TestCase):

    def test_rl_qc_len(self):
        if PRODUCTION_PLANT == "fos":
            # TODO extend to other kpis and processes
            df_in = pd.read_csv('./tests/resources/sample_data.csv')
            df_out = compute_kpi(
                'RL_QC_LENGTH', df_in, group_cols='OC_SPI_text', return_df=True
            )
            self.assertAlmostEqual(df_out['RL_QC_LENGTH'].iloc[0], 26.490, 3)
        elif PRODUCTION_PLANT == "dvrn":
            # TODO define a test for almost a kpi
            self.assertTrue(True) 
        else:
            raise NotImplementedError
