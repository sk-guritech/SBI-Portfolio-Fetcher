# SBI-Portfolio-Fetcher
SBI証券で保有している証券のリストを取得するモジュール


## Useage
```
from sbi_portfolio_fetcher import SBIPortfolioFetcher
from pprint import pprint
import sys

user_name = sys.argv[1]
password  = sys.argv[2]
chromedriver_executable_path = "./external_softwares/chromedriver"
	
pprint(SBIPortfolioFetcher.fetch(user_name, password,chromedriver_executable_path))
```
## Requirements

### Python Liblary
```
selenium
beautifulsoup4
```

### Software
```
chromedriver
```

## License

Copyright (c) 2020 S.K. Technology Firm, @GuriTech
Released under the MIT License