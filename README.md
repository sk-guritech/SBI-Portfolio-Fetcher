# SBI-Portfolio-Fetcher
Python-Module to get a list of securities held by SBI SECURITIES <br>
(Currently, only US stocks, Japanese stocks, investment trusts, Japanese yen, and foreign currencies held by the author are supported)

SBI証券で保有している証券のリストを取得するPythonモジュール<br>
(現在、作者が保有している米株現物・日本株現物・投資信託・日本円・外貨のみ対応)

## Donate Me
```
NEM  : NB2DFL2GAI7JVVBYKHKCNBVLSOEQOGJSO4YFVBMN
MONA : MNFghqmEdT5fBRKfsrKgEGwCWcd1sgHcym
ETH  : 0x0dBCD45B11429eAc973e037CF93A373261AB7627
BTC  : 3PDy26ruA9mzKEv4imqsAzEoYr2ANVnVDP
```

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

### Python Library
```
selenium
beautifulsoup4
```

### Software
```
chromedriver
```

## License

Copyright (c) 2021 S.K. Technology Firm, @GuriTech
Released under the MIT License
