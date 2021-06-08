# cov19-vaccine-tracker
This script can be used to find available covid19 vaccine slot by pincode or by district.

District id can be found from :
1] Get state id using URL: https://cdn-api.co-vin.in/api/v2/admin/location/states
2] Get district id : by using URL: https://cdn-api.co-vin.in/api/v2/admin/location/districts/<state id>
  
Script parameters can be found by using ' python find_cov_vaccine_slot_script.py --help'
  
'age' and ('pin' or 'district_id') are mandatory script parameters.
  
 For running script pre-requisites are:
 
  1] python 2.17
  2] pip
  3] pip install pygame, requests
