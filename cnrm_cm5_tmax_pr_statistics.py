"""
Calculate April Tmax and Annual PR for CNRM-CM5 1981-2000 avg and 2081-2100 avg. 

Neil Berg, October 2017
"""

import os
import xarray as xr

gcm = 'CNRM-CM5'

def april_tmax(exp, strt_yr, end_yr):
	""" Climatoligical April Tmax (warmest day during April) """

	src_dir = '/data/public/gcm/cmip5/native/day/{0}/tas/'.format(exp)
	dest_dir = '/work/nberg/doe_downscaling/data/'
	
	all_data = xr.open_mfdataset(src_dir+'air2m_day_'+gcm+'_'+exp+'_r1i1p1_????.nc')
	sliced_data = all_data.sel(TIME=slice(str(strt_yr), str(end_yr)))
	april_maxes = sliced_data.groupby('TIME.month').max('TIME').sel(month=4)
	
	if exp == 'historical':
		out_pfx = 'hist'
	else:
		out_pfx = 'fut'

	dest_fl = dest_dir+'cnrm_cm5_{0}_{1}-{2}_tmax_april.nc'.format(out_pfx, strt_yr, end_yr)
	if os.path.exists(dest_fl):
		os.remove(dest_fl)
	
	april_maxes.to_netcdf(dest_fl)
	print(dest_fl)

def annual_pr(exp, strt_yr, end_yr):
	""" Climatoligical annual precip """

	src_dir = '/data/public/gcm/cmip5/native/day/{0}/pr/'.format(exp)
	dest_dir = '/work/nberg/doe_downscaling/data/'

	all_data = xr.open_mfdataset(src_dir+'pr_day_'+gcm+'_'+exp+'_r1i1p1_????.nc')
	sliced_data = all_data.sel(TIME=slice(str(strt_yr), str(end_yr)))
	clim_annual_mean = sliced_data.resample(TIME='1AS').mean('TIME').mean('TIME')
	
	if exp == 'historical':
		out_pfx = 'hist'
	else:
		out_pfx = 'fut'

	dest_fl = dest_dir+'cnrm_cm5_{0}_{1}-{2}_annual_pr.nc'.format(out_pfx, strt_yr, end_yr)
	if os.path.exists(dest_fl):
		os.remove(dest_fl)
	
	clim_annual_mean.to_netcdf(dest_fl)
	print(dest_fl)


if __name__=='__main__':

	#april_tmax('historical', 1981, 2000)
	#april_tmax('rcp85', 2081, 2100)
	annual_pr('historical', 1981, 2000)
	annual_pr('rcp85', 2081, 2100)
