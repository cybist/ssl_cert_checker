#!/usr/local/bin/python3.7

import logging
import os
import sys
import logging
import subprocess
import datetime
import calendar
import pytz
import dateutil.parser
import pickle
import click
import plyvel
import json
import toml
from pprint import pprint

configs = toml.load(open('../configs/common.toml'))

logger = logging.getLogger('Batch')
logger.setLevel(10)

fh = logging.FileHandler(configs['APP_DIR'] + 'logs/batch.log')
logger.addHandler(fh)

sh = logging.StreamHandler()
logger.addHandler(sh)

format = logging.Formatter('%(asctime)s - [%(levelname)s] (%(lineno)d) %(message)s')
fh.setFormatter(format)
sh.setFormatter(format)

curr_tz = pytz.timezone('Asia/Tokyo')
curr_ts = int(datetime.datetime.now().timestamp())

results = {}
index = 0
is_need_report = False
for brand in configs['DOMAIN_LIST']:
    logger.info(brand + ' >>> start')
    results[brand] = {}
    for fqdn in configs['DOMAIN_LIST'][brand]:
        try:
            limit_at = subprocess.check_output(configs['CHECK_CMD'].format(fqdn = fqdn), shell = True)
            index += 1
            if limit_at != '':
                limit_at = str(limit_at).split(' : ')[1]
                limit_at = limit_at.split('\\n')[0]
                limit_at = dateutil.parser.parse(limit_at)
                limit_ts = calendar.timegm(limit_at.timetuple())

                if limit_ts < curr_ts:
                    status = configs['STATUS_NG']
                elif limit_ts < curr_ts + (60 * 60 * 24 * 25):
                    status = configs['STATUS_NOTE_REPORT']
                    is_need_report = True
                elif limit_ts < curr_ts + (60 * 60 * 24 * 30):
                    status = configs['STATUS_NOTE']
                else:
                    status = configs['STATUS_OK']

                limit_at = limit_at.astimezone(curr_tz).replace(tzinfo=curr_tz)
                limit_at = str(limit_at).split('+')[0].replace('-', '/')
                results[brand][fqdn] = {
                    'index': index,
                    'status': status,
                    'limit_at':limit_at
                }
            else:
                logger.warning(fqnd + ' unable to load certificate')
                results[brand][fqdn] = {
                    'index': index,
                    'status': configs['STATUS_ERROR'],
                    'limit_at':None
                }
        except Exception as e:
            logger.warning(e)
            results[brand][fqdn] = {
                'index': index,
                'status': configs['STATUS_ERROR'],
                'limit_at':None
            }
    logger.info(brand + ' <<< end')

logger.debug(results)

try:
    plyvel.destroy_db(configs['APP_DIR'] + configs['RESULT_DB'])
    result_db = plyvel.DB(configs['APP_DIR'] + configs['RESULT_DB'], create_if_missing=True)
    for brand in results:
        for fqdn, result in results[brand].items():
            result_db.put(str(fqdn).encode(), json.dumps(result).encode())
except Exception as e:
    logger.warning(e)
finally:
    result_db.close()
    if configs['CW_API_TOKEN'] != '' and is_need_report:
        subprocess.check_output('curl -X POST -H "X-ChatWorkToken: ' + configs['CW_API_TOKEN'] + '" -d "body=ssl-check%28bot%29%3A+domains+near+expiration+found&self_unread=1" ' + configs['CW_API_PATH'] + 'rooms/' + configs['CW_ROOM_ID'] + '/messages', shell = True)
