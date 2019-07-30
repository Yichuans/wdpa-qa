import unittest as unittest

from wdpa import qa
import pandas as pd

fields = [u'WDPAID', u'WDPA_PID', u'PA_DEF', u'NAME', u'ORIG_NAME', u'DESIG',
       u'DESIG_ENG', u'DESIG_TYPE', u'IUCN_CAT', u'INT_CRIT', u'MARINE',
       u'REP_M_AREA', u'GIS_M_AREA', u'REP_AREA', u'GIS_AREA', u'NO_TAKE',
       u'NO_TK_AREA', u'STATUS', u'STATUS_YR', u'GOV_TYPE', u'OWN_TYPE',
       u'MANG_AUTH', u'MANG_PLAN', u'VERIF', u'METADATAID', u'SUB_LOC',
       u'PARENT_ISO3', u'ISO3']

# duplicates of PIDs
# invalid values in DESIG_TYPE
data1 = [[40597.0, 40597.0, u'1', u'Lopeichubei', u'Lopeichubei',
        u'Forest Reserve', u'Forest Reserve', u'National', u'Not Reported',
        u'Not Applicable', u'0', 0.0, 0.0, 166.6365, 167.37390617160307,
        u'Not Applicable', 0.0, u'Designated', 1963,
        u'Federal or national ministry or agency', u'Not Reported',
        u'Not Reported', u'Not Reported', u'State Verified', 1708,
        u'Not Reported', u'UGA', u'UGA'],

        [40597.0, 40597.0, u'1', u'Lopeichubei', u'Lopeichubei',
        u'Forest Reserve', u'Forest Reserve', u'National', u'Not Reported',
        u'Not Applicable', u'0', 0.0, 0.0, 166.6365, 167.37390617160307,
        u'Not Applicable', 0.0, u'Designated', 1963,
        u'Federal or national ministry or agency', u'Not Reported',
        u'Not Reported', u'Not Reported', u'State Verified', 1708,
        u'Not Reported', u'UGA', u'UGA']]

data2 = [[40463.0, 40463.0, u'12', u'Agoro - Agu', u'Agoro - Agu',
        u'Forest Reserve', u'Forest Reserve', u'NationalL', u'Not ReportedED',
        u'Not Applicable', u'4', 0.0, 0.0, 263.5165, 264.65263904829055,
        u'Not Applicable', 0.0, u'Designated', 1948,
        u'Federal or national ministry or agency', u'Not Reported',
        u'Not Reported', u'Not Reported', u'State Verified', 1708,
        u'Not Reported', u'UGA', u'UGA'],

       [64669.0, 64669.0, u'1', u'Ayipe', u'Ayipe', u'Forest Reserve',
        u'Forest Reserve', u'Regional', u'Not Reported', u'Not Applicable',
        u'0', 0.0, 0.0, 8.9232, 8.963187352106354, u'Not Applicable', 0.0,
        u'Designated', 1965, u'Federal or national ministry or agency',
        u'Not Reported', u'Not Reported', u'Not Reported',
        u'State Verified', 1708, u'Not Reported', u'UGA', u'UGA'],

       [315109.0, 315109.0, u'1', u'Atiya', u'Atiya', u'Forest Reserve',
        u'Forest Reserve', u'National', u'Not Reported', u'Not Applicable',
        u'0', 0.0, 0.0, 194.0, 188.61335874196823, u'Not Applicable', 0.0,
        u'Designated', 1948, u'Federal or national ministry or agency',
        u'Not Reported', u'Not Reported', u'Not Reported',
        u'State Verified', 1708, u'Not Reported', u'UGA', u'UGA'],

       [40642.0, 40642.0, u'1', u'Wati', u'Wati', u'Forest Reserve',
        u'Forest Reserve', u'National', u'Not Reported', u'Not Applicable',
        u'0', 0.0, 0.0, 7.7195, 7.753119931890161, u'Not Applicable', 0.0,
        u'Designated', 1968, u'Federal or national ministry or agency',
        u'Not Reported', u'Not Reported', u'Not Reported',
        u'State Verified', 1708, u'Not Reported', u'UGA', u'UGA'], 
        
        [40642.0, 40642.0, u'1', u'Wati', u'Wati', u'Forest Reserve',
        u'Forest Reserve', u'National', u'Not Reported', u'Not Applicable',
        u'0', 0.0, 0.0, 7.7195, 7.753119931890161, u'Not Applicable', 0.0,
        u'Designated', 1968, u'Federal or national ministry or agency',
        u'Not Reported', u'Not Reported', u'Not Reported',
        u'State Verified', 1708, u'Not Reported', u'UGA', u'UGA']
        ]


data3 = [
        [315109.0, 315109.0, u'1', u'Atiya', u'Atiya', u'Forest Reserve',
        u'Forest Reserve', u'National', u'Not Reported', u'Not Applicable',
        u'0', 0.0, 0.0, 194.0, 188.61335874196823, u'Not Applicable', 0.0,
        u'Designated', 1948, u'Federal or national ministry or agency',
        u'Not Reported', u'Not Reported', u'Not Reported',
        u'State Verified', 1708, u'Not Reported', u'UGA', u'UGA'],

        [315109.0, 315110.0, u'1', u'Atiya', u'Atiya', u'Forest Reserve NOT',
        u'Forest Reserve NOT', u'National NOT', u'Time is UP!', u'Not Applicable',
        u'0', 0.0, 0.0, 194.0, 188.61335874196823, u'Not Applicable', 0.0,
        u'Designated', 1948, u'Federal or national ministry or agency',
        u'Not Reported', u'Not Reported', u'Not Reported',
        u'State Verified', 1708, u'Not Reported', u'UGA', u'UGA']
        ]


df1 = pd.DataFrame(data1, columns=fields)

df2 = pd.DataFrame(data2, columns=fields)

df3 = pd.DataFrame(data3, columns=fields)


# duplicate PID
class TestDuplicateWDPA_PID(unittest.TestCase):
    def test_duplicate(self):
        self.assertTrue(qa.duplicate_wdpa_pid(df1))

# invalid values in fields
class TestInvalidValues(unittest.TestCase):
	# dummy test by Yichuan - 23 July 2019
	# def test_inconsistent_fields_same_wdpaid(self):
	# 	self.assertEqual(list(inconsistent_fields_same_wdpaid(
    #         df_x, check_field, True)), ['1.234', '2.355']) # these are the output WDPA_PIDs
	
    def test_desig_type(self):
        self.assertTrue(qa.invalid_desig_type(df2))

    def test_marine(self):
        self.assertTrue(qa.invalid_marine(df2))

    def test_iucn_cat(self):
        self.assertTrue(qa.invalid_iucn_cat(df2))

    def test_pa_def(self):
        self.assertTrue(qa.invalid_pa_def(df2))

    def test_desig_eng_regional(self):
        self.assertTrue(qa.invalid_desig_eng_regional(df2))

# inconsistent value for rows sharing the same WDPAID
class TestInconsistentValues(unittest.TestCase):
    def test_inconsistent_desig_same_wdpaid(self):
        self.assertTrue(qa.inconsistent_desig_same_wdpaid(df3))

            
if __name__ == '__main__':
    unittest.main()