from sbi_portfolio_fetcher import SBIPortfolioFetcher
from pprint import pprint
import sys

user_name = sys.argv[1]
password  = sys.argv[2]
chromedriver_executable_path = "./external_softwares/chromedriver"
	
pprint(SBIPortfolioFetcher.fetch(user_name, password,chromedriver_executable_path))