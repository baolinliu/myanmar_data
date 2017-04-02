import pandas as pd

#===============================================================================

# This set of functions will grab and centralize data we will use to describe
# townships in Myanmar.

#===============================================================================
def get_data():
	'''
		This function grabs data from multiple data sources to collect metadata
		about townships in Myanmar and have it in one place.

		NOTE: This function is path sensitive and requires the sourced data to be
		downloaded first.

		INPUT: N/A. Function should not be fed inputs.

		OUTPUT: Pandas dataframe of the township data in Myanmar.
	'''
	# Township pcode location data
	pcodes_full = pd.read_csv('Myanmar PCodes Release-VIII_Aug2015 (Villages).csv')
	cols = ['TS_Pcode', 'Longitude', 'Latitude']
	pcodes = pd.DataFrame(pcodes_full[cols].values)
	pcodes.columns = ['pcode_ts', 'longitude', 'latitude']

	# Township population data
	township_full = pd.read_excel('BaselineData_Census_Dataset_Township_MIMU_16Jun2016_ENG.xlsx')
	township_full.columns = ['t_' + str(i) for i in xrange(township_full.shape[1])]

	cols = ['t_4', 't_5', 't_6', 't_24', 't_54', 't_66', 't_78']
	town = pd.DataFrame(township_full[cols][2:].values)
	town.columns = ['pcode_ts', 'township_name', 'pop_total', 'urban_perc',\
					'literacy_perc_total', 'literacy_perc_urban', 'literacy_perc_rural']

	# Mean household size
	cols = ['pcode_ts', 'mean_hhsize'] + ['hh_' + str(i) for i in xrange(1, 10)]
	mean_hh_full = pd.read_csv('CensusmeanHHsizetsp.csv')
	mean_hh = pd.DataFrame(mean_hh_full[cols].values)
	mean_hh.columns = cols

	# Census data for light sources
	cols = ['pcode_ts', 'light_total', 'l_source_electricity', 'l_source_kerosene',\
			'l_source_candle', 'l_source_lbattery', 'l_source_generator',\
			'l_source_water', 'l_source_solar', 'l_source_other']
	light_source_full = pd.read_csv('Censussourceoflighttsp.csv')
	light_source = pd.DataFrame(light_source_full[cols].values)
	light_source.columns = cols

	# Census transportation data
	cols = ['pcode_ts', 'trans_t', 'trans_car', 'trans_mcyc', 'trans_bicyc',\
			'trans_4wheel', 'trans_canoe', 'trans_mboat', 'trans_cart']
	transportation_full = pd.read_csv('Censustransportationtsp.csv')
	transportation = pd.DataFrame(transportation_full[cols].values)
	transportation.columns = cols

	# Census home ownership data
	cols = ['pcode_ts', 'ownshp_t', 'ownshp_own', 'ownshp_rent', 'ownshp_free',\
			'ownshp_gov', 'ownshp_com', 'ownshp_oth']
	home_ownership_full = pd.read_csv('Censusownershipofhousingtsp.csv')
	home_ownership = pd.DataFrame(home_ownership_full[cols].values)
	home_ownership.columns = cols

	# Census communication data
	cols = ['pcode_ts', 'com_t', 'com_radio', 'com_tv', 'com_lline', 'com_mob', 'com_comp', 'com_int']
	communication_full = pd.read_csv('Censuscommuniationtsp.csv')
	communication_full[cols].head()
	communication = pd.DataFrame(communication_full[cols].values)
	communication.columns = cols

	# Merging
	tables = [mean_hh, light_source, transportation, home_ownership, communication]
	df_all = town.copy()
	for df in tables:
		df_all = pd.merge(df_all, df, on='pcode_ts')

	return df_all

def get_info():
	'''
		This function provides information about the column values for the Myanmar township data.

		INPUT: N/A. Function should not be fed inputs.

		OUTPUT: Pandas dataframe of the column info.
			KEY: column name
			VALUES: datatype, summary of the column, link to the original data source
	'''
	info = {
	'pcode_ts':             ['id', 'unique ids to denote specific townships in Myanmar', 'http://themimu.info/doc-type/census-baseline-data'],
	'township_name':        ['general', 'name of the township', 'http://themimu.info/doc-type/census-baseline-data'],
	'pop_total':            ['general', 'population total', 'http://themimu.info/doc-type/census-baseline-data'] ,
	'urban_perc':           ['general', 'percentage of the township that is urban', 'http://themimu.info/doc-type/census-baseline-data'],
	'literacy_perc_total':  ['literacy', 'percentage of the township that is literate', 'http://themimu.info/doc-type/census-baseline-data'],
	'literacy_perc_urban':  ['literacy', 'percentage of the urban township that is literate', 'http://themimu.info/doc-type/census-baseline-data'],
	'literacy_perc_rural':  ['literacy', 'percentage of the rural township that is literate', 'http://themimu.info/doc-type/census-baseline-data'],
	'mean_hhsize':          ['household', 'mean household size', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'hh_1':                 ['household', 'total households of 1 person', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'hh_2':                 ['household', 'total households of 2 people', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'hh_3':                 ['household', 'total households of 3 people', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'hh_4':                 ['household', 'total households of 4 people', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'hh_5':                 ['household', 'total households of 5 people', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'hh_6':                 ['household', 'total households of 6 people', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'hh_7':                 ['household', 'total households of 7 people', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'hh_8':                 ['household', 'total households of 8 people', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'hh_9':                 ['household', 'total households of 9+ people', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'light_total':          ['light sources', 'total', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'l_source_electricity': ['light sources', 'light generated from electricity', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'l_source_kerosene':    ['light sources', 'kerosene light source', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'l_source_candle':      ['light sources', 'candle light', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'l_source_lbattery':    ['light sources', 'battery-powered lights', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'l_source_generator':   ['light sources', 'private generator', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'l_source_water':       ['light sources', 'private water mill', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'l_source_solar':       ['light sources', 'solar system energy', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'l_source_other':       ['light sources', 'other light source', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'trans_t':              ['transportation', 'total households', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'trans_car':            ['transportation', 'car, truck, or van', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'trans_mcyc':           ['transportation', 'motorcycle moped', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'trans_bicyc':          ['transportation', 'bicycle', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'trans_4wheel':         ['transportation', 'four wheel tractor', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'trans_canoe':          ['transportation', 'canoe boat', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'trans_mboat':          ['transportation', 'motor boat', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'trans_cart':           ['transportation', 'cart pulled by oxen', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'ownshp_t':             ['home ownership', 'total types of home owners', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'ownshp_own':           ['home ownership', 'owner', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'ownshp_rent':          ['home ownership', 'renter', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'ownshp_free':          ['home ownership', 'provided for free', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'ownshp_gov':           ['home ownership', 'government quarters', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'ownshp_com':           ['home ownership', 'private company quarters', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'ownshp_oth':           ['home ownership', 'other', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'com_t':                ['communication', 'total households', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'com_radio':            ['communication', 'radio', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'com_tv':               ['communication', 'television', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'com_lline':            ['communication', 'land line phone', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'com_mob':              ['communication', 'mobile phone', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'com_comp':             ['communication', 'personal computer', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census'],
	'com_int':              ['communication', 'internet at home', 'https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census']
	}
	return pd.DataFrame(info.values(), index=info.keys(), columns=['datatype', 'summary', 'source'])

def main():
	pass

#===============================================================================

if __name__ == '__main__':
	main()