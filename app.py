from selenium import webdriver
from tempfile import mkdtemp
from utils import scrape_results_site

def handler(event=None, context=None):

    for key in event.keys():

        options = webdriver.ChromeOptions()
        options.binary_location = '../opt/chrome/chrome'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")
        chrome = webdriver.Chrome("../opt/chromedriver",
                                  options=options)

        oddsportal_link = key
        save_url_s3 = event[key]

        odds_df = scrape_results_site(driver = chrome,
                                      link = oddsportal_link,
                                      scroll_amount_px = 1000,
                                      scroll_wait = 1,
                                      scroll_iterations = 5)
        odds_df.to_parquet(save_url_s3)
        print('success in saving odds from link: ' + oddsportal_link)

    return