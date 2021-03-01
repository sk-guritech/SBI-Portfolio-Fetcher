from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import bs4

# Login
def login(driver, user_name, password):
	driver.get("https://www.sbisec.co.jp/ETGate")
	WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME,"user_id")))

	input_user_id = driver.find_element_by_name("user_id")
	input_user_id.send_keys(user_name)
	input_password = driver.find_element_by_name("user_password")
	input_password.send_keys(password)
	driver.find_element_by_name("ACT_login").click()

# Yen Denominated Securities
def get_yen_denominated_securities(driver):
	assets_dict = {}
	WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"logoutM")))

	page = driver.page_source
	soup = BeautifulSoup(page, "html.parser")
	assets_dict["cash"] = {}
	assets_dict["cash"]["JPY"] = [int(soup.find_all("td", class_="tp-td-01")[0].find("span").text.replace(",","")),int(soup.find_all("td", class_="tp-td-01")[0].find("span").text.replace(",",""))]
	assets_dict["cash"]["header"] = ["Balance","YenConversion"]

	driver.get("https://site1.sbisec.co.jp/ETGate/?_ControlID=WPLETacR002Control&_PageID=DefaultPID&_DataStoreID=DSWPLETacR002Control&_SeqNo=1614601428471_default_task_1128_DefaultPID_DefaultAID&getFlg=on&_ActionID=DefaultAID")

	WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"navi02P")))

	page = driver.page_source
	soup = BeautifulSoup(page, "html.parser")
	tables = soup.find("td",align="center",width="778").find_all("table",width="750",cellspacing="0")[3:]

	assets_dict["yen_denominated"] = {}
	for n in range(int(len(tables)/2)):
		asset_class = tables[2*n].find("td").text.split("\xa0")[1].replace("\n","")
		assets_dict["yen_denominated"][asset_class] = {"assets":[],"header":None}
		
		header = [[content if type(content) == bs4.element.NavigableString else content.text for content in td.contents] for td in tables[2*n+1].find_all("tr")[1].find_all("td")]

		header_tmp = []
		header_tmp.append(header[0][0])
		header_tmp.append(header[1][0]+header[1][2])
		header_tmp.append(header[2][0])
		header_tmp.append(header[2][2])
		header_tmp.append(header[3][0])
		header_tmp.append(header[3][2])
		header_tmp.append(header[4][0])

		assets_dict["yen_denominated"][asset_class]["header"] = header_tmp

		assets = tables[2*n+1].find_all("tr")[2:]

		for j, asset in enumerate(assets):
			if j % 2 == 1:
				continue
			detail = [[content.replace("\n","").replace("\xa0","").replace("\u3000"," ") if type(content) == bs4.element.NavigableString else content.text.replace("\n","").replace("\xa0","").replace("\u3000"," ") for content in td.contents] for td in asset.find_all("td")]

			detail_tmp = []
			if len(detail[0]) != 1:
				detail_tmp.append(detail[0][1] + ":" + detail[0][3])
			else:
				detail_tmp.append(detail[0][0])
			detail_tmp.append(int(detail[1][0].replace("口","").replace(",","")))
			detail_tmp.append(int(detail[2][0].replace(",","")))
			detail_tmp.append(int(detail[2][2].replace(",","")))
			detail_tmp.append(int(detail[3][0].replace(",","")))
			detail_tmp.append(int(detail[3][2].replace(",","")))
			detail_tmp.append(int(detail[4][0].replace(",","")))

			assets_dict["yen_denominated"][asset_class]["assets"].append(detail_tmp)

	return assets_dict

# Foreign Denominated Securities
def get_foreign_denominated_securities(driver):
	assets_dict = {"cash":{}}
	
	driver.get("https://site1.sbisec.co.jp/ETGate/?_ControlID=WPLETsmR001Control&_DataStoreID=DSWPLETsmR001Control&_PageID=WPLETsmR001Sdtl12&sw_page=BondFx&sw_param2=02_201&cat1=home&cat2=none&getFlg=on")

	WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"navi02P")))

	page = driver.page_source
	soup = BeautifulSoup(page, "html.parser")
	cash_rates = [float(tr.find_all("td")[1].text) for tr in  soup.find_all("tr",class_="mtext")[:17]] 
	cash_balances = [[tr.find("a").text.split("(")[1].replace(")",""),float(tr.find_all("td")[2].text.replace(",",""))] for tr in  soup.find_all("tr",class_="mtext")[17:34]]

	for n in range(len(cash_rates)):
		assets_dict["cash"][cash_balances[n][0]] = [cash_balances[n][1],cash_balances[n][1]*cash_rates[n]]


	driver.find_element_by_xpath("/html/body/div/table[2]/tbody/tr/td[1]/table/tbody/tr/td[2]/map/area[2]").click()

	WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"navi02P")))

	page = driver.page_source
	soup = BeautifulSoup(page, "html.parser")

	for i in soup.select("br"):
		i.replace_with("\n")

	assets_dict["foreign_denominated"] = {}

	tables = soup.find("td",width="570").find("td",width="568").find_all("table",cellspacing="0")[12:]

	for n in range(int(len(tables)/2)):
		asset_class = tables[2*n].find("td").text.split("\xa0")[1].replace("\n","")
		assets_dict["foreign_denominated"][asset_class] = {"assets":[],"header":None}
		
		header = [td.text.replace("\t","").split("\n") for td in tables[1].find_all("tr")[1].find_all("td")]

		header_tmp = []
		header_tmp.append(header[0][0])
		header_tmp.append(header[1][0]+header[1][1])
		header_tmp.append(header[2][3])
		header_tmp.append(header[3][0])
		header_tmp.append(header[3][1])
		header_tmp.append(header[4][0])
		header_tmp.append(header[4][1])

		assets_dict["foreign_denominated"][asset_class]["header"] = header_tmp

		assets = tables[2*n+1].find_all("tr")[2:]

		for j, asset in enumerate(assets):
			detail = [[content.replace("\n","").replace("\t","").replace("\xa0"," ").replace(",","") for content in td.text.split("\n\n")] for td in assets[j].find_all("td")] 

			detail_tmp = []
			if len(detail[0]) != 1:
				detail_tmp.append(detail[0][0] + ":" + detail[0][1])
			else:
				detail_tmp.append(detail[0][0])
			detail_tmp.append(int(detail[1][0]))
			detail_tmp.append(float(detail[2][0]))
			detail_tmp.append(float(detail[2][1]))
			detail_tmp.append(float(detail[3][0]))
			detail_tmp.append(float(detail[3][1]))
			detail_tmp.append(float(detail[4][1]))
			detail_tmp.append(float(detail[4][3]))

			assets_dict["foreign_denominated"][asset_class]["assets"].append(detail_tmp)

	driver.find_element_by_id("logoutM").click()

	return assets_dict

# Fetch All Balance
def fetch(user_name, password):
	options = Options()
	options.add_argument("--headless")
	driver = webdriver.Chrome(executable_path="./external_softwares/chromedriver",options=options)

	assets_dict = {}
	login(driver, user_name, password)
	assets_dict.update(get_yen_denominated_securities(driver))
	assets_dict.update(get_foreign_denominated_securities(driver))

	return assets_dict


if __name__ == '__main__':
	from pprint import pprint
	import sys

	user_name = sys.argv[1]
	password = sys.argv[2]
	
	pprint(fetch(user_name, password))
