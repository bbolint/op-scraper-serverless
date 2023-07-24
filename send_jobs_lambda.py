import json
import boto3
import base64
import botocore
from datetime import datetime

config = botocore.config.Config(
    read_timeout=900,
    connect_timeout=900,
    retries={"max_attempts": 0}
)
lambda_client = boto3.client('lambda', region_name = 'eu-west-1',config=config)

def get_event_jsons(source_link, num_pages, save_path_filename_general):
    event_jsons_dict = {}
    for page_id in range(1, num_pages+1):
        dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _link = source_link + str(page_id)
        _save_filename = save_path_filename_general + '_page_' + str(page_id) + '_' + dt_string + '.parquet'
        event_jsons_dict[_link] = _save_filename
    return event_jsons_dict

def send_event_stream_odds_lambda(event_dict):
    event_json = json.dumps(event_dict)
    response = lambda_client.invoke(FunctionName='op-scraper-serverless-dev-hello',
                                     InvocationType='RequestResponse',
                                     LogType='Tail',
                                     Payload=event_json)
    print(response)


if __name__ == "__main__":

    seasons_num_pages =  [['2021-2022', 31],#[['2022-2023', 31],
                         ['2020-2021', 20],
                         ['2019-2020', 27],
                         ['2018-2019', 30],
                         ['2017-2018', 30],
                         ['2016-2017', 29],
                         ['2015-2016', 29],
                         ['2014-2015', 29],
                         ['2013-2014', 29],
                         ['2012-2013', 17],
                         ['2011-2012', 29],
                         ['2010-2011', 29],
                         ['2009-2010', 29],
                         ['2008-2009', 27],
                         ['2007-2008', 27],
                         ['2006-2007', 26],
                         ['2005-2006', 26],
                         ['2003-2004', 10]]


    for season in seasons_num_pages:

        event_dict = get_event_jsons(source_link = 'https://www.oddsportal.com/hockey/usa/nhl-{}/results/#/page/'.format(season[0]),
                                           num_pages = season[1],
                                           save_path_filename_general = 's3://hockey-analytics/structured-odds-data/nhl/1X2-AVG/' + season[0])
        send_event_stream_odds_lambda(event_dict)
        print("season " + season[0] + " processed")


