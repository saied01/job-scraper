from scrapers.scraper_site1 import scrape_site1
from utils.db_utils import update_database, check_database

scrape_site1()

update_database()

check_database()