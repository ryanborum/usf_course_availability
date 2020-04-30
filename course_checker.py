# Fetch course openings by submitting the below form:
# https://www.registrar.usf.edu/ssearch/staff/staff.php

import sys
import requests
#from pushbullet import Pushbullet
from time import sleep
from bs4 import BeautifulSoup

# staff schedule search
search_url = 'https://usfonline.admin.usf.edu/pls/prodss/wp_staff_search_db'

# Pushbullet Setup (Optional - handles mobile notifications)
SEND_PB_NOTIFICATION = False
PB_API_KEY = ''

# Course Details. Use EITHER 'search_prefix' and 'search_number' OR 'search_crn'
search_prefix = 'ABC'
search_number = '1234'
search_crn = '21599'

# Search Details
# YYYY followed by:
# 01 = Spring | 05 = Summer | 08 = Fall
search_term = '202001' #Spring 2020

#Frequency of Check (in seconds)
check_freq = 180

# Parameter dictionary
PARAMS = {
    'P_SEMESTER': search_term,
    'P_SESSION': '',
    'P_CAMPUS': '',
    'P_DIST': '',
    'P_COL': '',
    'P_DEPT': '',
    'p_status': '',
    'p_ssts_code': 'A', #Active Only
    'P_CRSE_LEVL': '',
    'P_REF': search_crn,
    'P_SUBJ': search_prefix,
    'P_NUM': search_number,
    'P_TITLE': '',
    'P_CR': '',
    'p_day_x': 'no_val',
    'p_day': 'no_val',
    'P_TIME1': '',
    'P_INSTRUCTOR': '',
    'P_UGR': ''
}
check_count = 0

while True:
    data = []
    try:
        req = requests.post(search_url, data=PARAMS)
        soup = BeautifulSoup(req.text, 'html.parser')

        results_table = soup.find('table', attrs={'id': 'results'})
        rows = results_table.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])  # strip empty values

        seats_open = []
        CRNs = []
        opening = False
        for x in range(len(data)-1):
            seats_open = int(data[x+1][12])
            if seats_open > 0:
                CRNs.append(data[x+1][3])
                opening = True

        if opening is True:
            print("Course Opening!", (", ".join(map(str, CRNs))))
            if SEND_PB_NOTIFICATION is True:
                pb = Pushbullet(PB_API_KEY)
                pb.push_note("Course Opening!", (",".join(map(str, CRNs))), pb.devices[0])
            break

        check_count += 1
        print("Checked", check_count, "time(s)")
        sleep(check_freq)  # 3 minutes
    except Exception:
        print("Connection failed")
        sleep(check_freq)
        pass  # important not to swallow other exceptions
