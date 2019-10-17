# Fetch course openings by submitting the below form:
# https://www.registrar.usf.edu/ssearch/staff/staff.php

import requests
from pushbullet import Pushbullet
from time import sleep
from bs4 import BeautifulSoup

# staff schedule search
search_url = 'https://usfonline.admin.usf.edu/pls/prodss/wp_staff_search_db'

# Pushbullet Setup (Optional - handles mobile notifications)
SEND_PB_NOTIFICATION = True
PB_API_KEY = ''

# Course Details
search_prefix = 'ENC'
search_number = '3246'


##### DO NOT EDIT BELOW THIS LINE IF YOU ARE A NORMIE #####
###########################################################

# Parameter dictionary
PARAMS = {
    'P_SEMESTER': '201908',  # Fall 2019
    'P_SESSION': '',
    'P_CAMPUS': '',
    'P_DIST': '',
    'P_COL': '',
    'P_DEPT': '',
    'p_status': '',
    'p_ssts_code': '',
    'P_CRSE_LEVL': '',
    'P_REF': '',
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
            data.append([ele for ele in cols if ele])  # Get rid of empty values

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
        sleep(180)  # 3 minutes
    except Exception:
        print("Connection failed")
        sleep(180)
        pass  # important not to swallow other exceptions
