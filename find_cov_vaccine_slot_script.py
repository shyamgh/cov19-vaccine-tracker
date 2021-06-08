'''
Script: Covid Vaccine Slot Availability Display
By: Shyam Hushangabadkar
'''

from optparse import OptionParser
import requests
from pygame import mixer 
from datetime import datetime, timedelta
import time

play_sound = True
min_vaccines = 1


def _process_request(actual_dates, base_url, age, dose=1, print_flag='Y'):

    if dose == 2:
        dose_param = "available_capacity_dose2"
    else:
        dose_param = "available_capacity_dose1"


    counter=0
    # base_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}"
    for given_date in actual_dates:
        URL = base_url+"&date={}".format(given_date)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

        try:
            result = requests.get(URL, headers=header)
        except:
            result.ok = None

        if result.ok:
            response_json = result.json()
            if response_json["centers"]:
                if (print_flag.lower() == 'y'):
                    for center in response_json["centers"]:
                        for session in center["sessions"]:
                            if (session["min_age_limit"] <= age and session[dose_param] > min_vaccines):
                                print('Pincode: {}'.format(center['pincode']))
                                print("Available on: {}".format(session['date']))
                                print("\t", center["name"])
                                print("\t", center["block_name"])
                                print("\t Price: ", center["fee_type"])
                                print("\t Availablity : ", session["available_capacity"])

                                if (session["vaccine"] != ''):
                                    print("\t Vaccine type: ", session["vaccine"])
                                print("\n")
                                counter = counter + 1
        else:
            print("No Response!")

    return counter


def check_availability_by_district(dis_id, age, num_days, sleep_time, num_of_iterations):
    print_flag = 'Y'

    print("-------- Starting search for Covid vaccine slots! --------")

    actual = datetime.today()
    list_format = [actual + timedelta(days=i) for i in range(num_days)]
    actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

    if num_of_iterations == -1:  # run large number of times
        num_of_iterations = 100000

    for i in range(num_of_iterations):
        print("Search try {} ...".format(i+1))
        base_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}".format(dis_id)
        counter = _process_request(actual_dates, base_url, age, print_flag)

        if counter == 0:
            print("No Vaccination slot available!")
        else:
            if play_sound:
                mixer.init()
                mixer.music.load('sound/bensound-happyrock.mp3')
                mixer.music.play()
                time.sleep(5)
                mixer.music.stop()
            print("Search Completed! Exiting....")

        # sleep
        for t in range(sleep_time):
            time.sleep(1)


def check_availability_by_pincode(age, pincodes, num_days, sleep_time, num_of_iterations):
    print_flag = 'Y'

    print("-------- Starting search for Covid vaccine slots! --------")

    actual = datetime.today()
    list_format = [actual + timedelta(days=i) for i in range(num_days)]
    actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

    if num_of_iterations == -1:  # run large number of times
        num_of_iterations = 100000

    for i in range(num_of_iterations):
        counter = 0
        print("Search try {} ...".format(i+1))

        for pincode in pincodes:
            base_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}".format(pincode)
            counter = _process_request(actual_dates, base_url, age, print_flag)

        if counter == 0:
            print("No Vaccination slot available!")
        else:
            mixer.init()
            mixer.music.load('sound/bensound-happyrock.mp3')
            mixer.music.play()
            time.sleep(5)
            mixer.music.stop()
            print("Search Completed! Exiting....")
            break

        # sleep
        for t in range(sleep_time):
            time.sleep(1)


if __name__ == '__main__':
    # argument parsing
    parser = OptionParser()
    parser.add_option('--search', dest='search',type='int',  default=1, help='Enter 1 for search by pin; Enter 2 for search by district')
    parser.add_option('--age', dest='age', type="int", help='Current age of person opting for vaccine')
    parser.add_option('--pin', dest='pincodes', action='append', default=[],
                      help='Space separated pincodes. Example: --pin=1234,1235,1236')
    parser.add_option('--district_id', dest='district_id', type='int', default=363,
                      help='Enter district id. District id can be found from typing below URL in browser:'
                           'https://cdn-api.co-vin.in/api/v2/admin/location/states'
                           'https://cdn-api.co-vin.in/api/v2/admin/location/districts/<id of your state>')

    parser.add_option('--days', dest='num_days', type="int", default=3,
                      help='number of future days to search vaccine slot')
    parser.add_option('--nexttrywait', dest='sleep_time', type="int", default=30,
                      help='time to wait before next search try')
    parser.add_option('--retrycount', dest='num_of_iterations', type="int", default=5,
                        help='Number of times to try search before exit script')
    options, args = parser.parse_args()

    if options.age is None:
        parser.error("parameter age is required. Please try 'python script.py --help'")
    if (options.pincodes is None) and (options.district_id is None):
        parser.error("parameter pin or district_id is required. Please try 'python script.py --help'")

    age = options.age

    if options.pincodes:
        pins = options.pincodes[0].split(",")
        pincodes = [int(ele) if ele.isdigit() else ele for ele in pins]
    district_id = options.district_id

    num_days = options.num_days
    sleep_time = options.sleep_time
    num_of_iterations = options.num_of_iterations

    if options.search == 1:
        check_availability_by_pincode(age, pincodes, num_days, sleep_time, num_of_iterations)
    else:
        check_availability_by_district(district_id, age, num_days, sleep_time, num_of_iterations)

