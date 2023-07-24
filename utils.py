import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import numpy as np
import pandas as pd
from datetime import datetime,timezone

def scrape_results_site(driver, link, scroll_amount_px, scroll_wait, scroll_iterations):

    driver.get(link)

    # scrolling through page and getting the data
    for i in range(scroll_iterations):
        driver.execute_script("window.scrollBy(0, {});".format(scroll_amount_px))
        time.sleep(scroll_wait)

    odds_style = driver.find_elements("xpath", "//p[contains(@class, 'text-orange-main self-center text-xs')]")[0].text
    time_zone = driver.find_elements("id",'timezone-p')[0].text
    game_dates = driver.find_elements("xpath","//div[contains(@class, 'text-black-main font')]")
    game_times = driver.find_elements("xpath","//p[(@class = 'whitespace-nowrap') and @*[contains(name(), 'data')]]")
    team_names = driver.find_elements("xpath","//div[contains(@class, 'relative block truncate') and @*[contains(name(), 'data')]]")
    game_odds = driver.find_elements("xpath","//p[contains(@class, 'height-content') and @*[contains(name(), 'data')]]")

    # reformatting the data into long lists
    game_dates_str = [date.text for date in game_dates]
    game_dates_y_loc = [date.location['y'] for date in game_dates]
    game_times_str = [time.text for time in game_times]
    team_names_str = [name.text for name in team_names]
    team_names_y_loc = [name.location['y'] for name in team_names]
    game_odds_str = [odd.text for odd in game_odds][1:]

    # reformatting the data into structured ("2d") lists
    ngames = int(len(game_odds_str) / 3)

    if ngames != len(game_times_str):
        print("problem with webelements dimensions:")
        print("number of game odds retrieved from site: " + str(len(game_odds_str)))
        print("number of game times retrieved from site: " + str(len(game_times_str)))
        return

    if ngames != int(len(team_names_str) / 2):
        print("problem with webelements dimensions:")
        print("number of game odds retrieved from site: " + str(len(game_odds_str)))
        print("number of team names retrieved from site: " + str(len(team_names_str)))
        return

    if ngames != int(len(team_names_y_loc) / 2):
        print("problem with webelements dimensions:")
        print("number of game odds retrieved from site: " + str(len(game_odds_str)))
        print("number of team name y locations retrieved from site: " + str(len(team_names_y_loc)))
        return

    teams_odds_list = []
    for i in range(0, ngames):
        teams_odds_list.append([game_times_str[i]] + team_names_str[i*2:i*2+2] + game_odds_str[i*3:i*3+3] + [team_names_y_loc[i*2]])
    game_dates_list = []
    for i in range(len(game_dates)):
        game_dates_list.append([game_dates_str[i]] + [game_dates_y_loc[i]])

    # reformatting the data into pandas dataframes and merging of different dimensions
    teams_odds_df = pd.DataFrame(teams_odds_list, columns = ['game_time', 'team_1', 'team_2', '1', 'X', '2', 'game_info_y_loc'])
    teams_odds_df['game_date'] = np.nan
    games_dates_df = pd.DataFrame(game_dates_list, columns = ['game_date', 'game_info_y_loc'])
    final_df = pd.concat([teams_odds_df, games_dates_df], axis = 0)
    final_df = final_df.sort_values('game_info_y_loc')
    final_df.loc[:, 'game_date'] = final_df.loc[:, 'game_date'].ffill()
    final_df.dropna(inplace = True)
    final_df['time_download_processor_utctime'] = datetime.now(timezone.utc)
    final_df['time_download_website_clock'] = time_zone.split(',')[0]
    final_df['time_zone_website'] = time_zone.split(',')[1]
    final_df['odds_style'] = odds_style
    final_df['link'] = link
    driver.quit()

    return final_df

if __name__ == "__main__":

    DRIVER_LOCATION = "/Users/balintbojko/PycharmProjects/chromedriver"
    service = Service(executable_path="/usr/local/bin/chromedriver")
    chrome = webdriver.Chrome(service=service)

    odds_df = scrape_results_site(driver=chrome,
                        link='https://www.oddsportal.com/hockey/usa/nhl-2020-2021/results/#/page/8',
                        scroll_amount_px=1000,
                        scroll_wait=1,
                        scroll_iterations=3)

    print(odds_df)
    print("done")