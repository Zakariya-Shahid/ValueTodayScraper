import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv

url = 'https://www.value.today/?title=&field_company_category_primary_target_id&field_headquarters_of_company_target_id=All&field_company_website_uri=&field_market_value_jan072022_value=&page=10'
count = 0
def parser(text):
    global count
    soup = BeautifulSoup(text, 'html.parser')
    mcap = 'N/A'
    annual_rev = 'N/A'
    number_of_employees = 'N/A'
    cname = 'N/A'
    ceo = 'N/A'
    hq = 'N/A'
    stock_exchange = 'N/A'
    business = 'N/A'

    divs = soup.find_all('div', class_ = 'well node node--type-listed-companies node--view-mode-search-index ds-2col-stacked clearfix')
    # iterating through all the tables
    for Maindiv in divs:
        cname = Maindiv.find('h1', class_='clearfix col-sm-12').text
        cname = cname.strip()
        HeaderDivs = Maindiv.find_all('div', class_ = 'clearfix group-header')
        if len(HeaderDivs) != 0:
            for HeaderDiv in HeaderDivs:
                MarkCapDivs = HeaderDiv.find_all('div', class_ = 'clearfix col-sm-6 field field--name-field-market-value-jan072022 field--type-float field--label-above')
                if len(MarkCapDivs) != 0:
                    for MarkCapDiv in MarkCapDivs:
                        MarkCap = MarkCapDiv.find('div', class_ = 'field--item')
                        if MarkCap is not None:
                            mcap = MarkCap.text
                        else:
                            mcap = 'N/A'
                            #print(mcap)
                            break
                else:
                    mcap = 'N/A'
        else:
            mcap = 'N/A'

        LeftDivs = Maindiv.find_all('div', class_ = 'clearfix group-left')
        if len(LeftDivs) != 0:
            for LeftDiv in LeftDivs:
                AnnualRevDivs = LeftDiv.find_all('div', class_ = 'clearfix col-sm-12 field field--name-field-revenue-in-usd field--type-float field--label-inline')
                if len(AnnualRevDivs) != 0:
                    for AnnualRevDiv in AnnualRevDivs:
                        AnnualRev = AnnualRevDiv.find('div', class_ = 'field--item')
                        if AnnualRev is not None:
                            annual_rev = AnnualRev.text
                            # print(annual_rev)
                        else:
                            annual_rev = 'N/A'
                        break
                else:
                    annual_rev = 'N/A'

                HqDivs = LeftDiv.find_all('div', class_ = 'clearfix col-sm-12 field field--name-field-headquarters-of-company field--type-entity-reference field--label-inline')
                if len(HqDivs) != 0:
                    for HqDiv in HqDivs:
                        Hq = HqDiv.find('div', class_ = 'field--item')
                        if Hq is not None:
                            hq = Hq.text
                            #print(hq)
                        else:
                            hq = 'N/A'
                        break
                else:
                    hq = 'N/A'
                StockExchangeDivs = LeftDiv.find_all('div', class_ = 'clearfix col-sm-12 field field--name-field-stock-exchange-lc field--type-entity-reference field--label-inline')
                if len(StockExchangeDivs) != 0:
                    for StockExchangeDiv in StockExchangeDivs:
                        StockExchangeList = StockExchangeDiv.find('div', class_ = 'field--items')
                        if StockExchangeList is not None:
                            StockExchange = StockExchangeList.find_all('div', class_ = 'field--item')
                            if len(StockExchange) != 0:
                                stock_exchange = ''
                                for StockExchangeItem in StockExchange:
                                    stock_exchange += StockExchangeItem.text + ', '
                                #print(stock_exchange)
                            else:
                                stock_exchange = 'N/A'
                        else:
                            stock_exchange = 'N/A'
                        break
        else:
            annual_rev = 'N/A'
            hq = 'N/A'
            stock_exchange = 'N/A'

        RightDivs = Maindiv.find_all('div', class_ = 'clearfix group-right')
        if len(RightDivs) != 0:
            for RightDiv in RightDivs:
                EmployeeDivs = RightDiv.find_all('div', class_ = 'clearfix col-sm-12 field field--name-field-employee-count field--type-integer field--label-above')
                if len(EmployeeDivs) != 0:
                    for EmployeeDiv in EmployeeDivs:
                        Employee = EmployeeDiv.find('div', class_ = 'field--item')
                        if Employee is not None:
                            number_of_employees = Employee.text
                            #print(number_of_employees)
                        else:
                            number_of_employees = 'N/A'
                        break
                else:
                    number_of_employees = 'N/A'

                CeoDivs = RightDiv.find_all('div', class_ = 'clearfix col-sm-12 field field--name-field-ceo field--type-entity-reference field--label-above')
                if len(CeoDivs) != 0:
                    for CeoDiv in CeoDivs:
                        CeoList = CeoDiv.find('div', class_ = 'field--items')
                        if CeoList is not None:
                            Ceo = CeoList.find_all('div', class_ = 'field--item')
                            if len(Ceo) != 0:
                                ceo = ''
                                for CeoItem in Ceo:
                                    ceo += CeoItem.text + ', '
                                #print(ceo)
                            else:
                                ceo = 'N/A'
                        else:
                            ceo = 'N/A'
        else:
            number_of_employees = 'N/A'
            ceo = 'N/A'

        FooterDivs = Maindiv.find_all('div', class_ = 'clearfix group-footer')
        if len(FooterDivs) != 0:
            for FooterDiv in FooterDivs:
                BuisnessDivs = FooterDiv.find_all('div', class_ = 'clearfix col-sm-12 field field--name-field-company-sub-category- field--type-entity-reference field--label-above')
                if len(BuisnessDivs) != 0:
                    for BuisnessDiv in BuisnessDivs:
                        BuisnessList = BuisnessDiv.find('div', class_ = 'field--items')
                        if BuisnessList is not None:
                            Buisness = BuisnessList.find_all('div', class_ = 'field--item')
                            if len(Buisness) != 0:
                                buisness = ''
                                for BuisnessItem in Buisness:
                                    if 'S&P 500' in BuisnessItem.text:
                                        continue
                                    else:
                                        buisness += BuisnessItem.text + ', '
                                #print(buisness)
                            else:
                                buisness = 'N/A'
                        else:
                            buisness = 'N/A'
                else:
                    buisness = 'N/A'
        else:
            buisness = 'N/A'

        # replacing Billion USD and Million USD with zeros and removing . from the numbers
        if 'Billion' in mcap:
            mcap = mcap.replace('Billion USD', '')
            mcap = mcap.replace('.', '')
            mcap = mcap.replace(' ', '')
            mcap = mcap + '000000000'
        elif 'Million' in mcap:
            mcap = mcap.replace('Million USD', '')
            mcap = mcap.replace('.', '')
            mcap = mcap + '000000'
        else:
            mcap = mcap.replace('.', '')
        if 'Billion' in annual_rev:
            annual_rev = annual_rev.replace('Billion USD', '')
            annual_rev = annual_rev.replace('.', '')
            annual_rev = annual_rev.replace(' ', '')
            annual_rev = annual_rev + '000000000'
        elif 'Million' in annual_rev:
            annual_rev = annual_rev.replace('Million USD', '')
            annual_rev = annual_rev.replace('.', '')
            annual_rev = annual_rev + '000000'
        else:
            annual_rev = annual_rev.replace('.', '')

        # print('Company = ',cname,'\n', 'Header Quarters = ',hq,'\n','Market Capital = ',mcap,'\n',
        # 'Annual Revenue = ', annual_rev,'\n','Number of Employees = ', number_of_employees,'\n',
        #       'Stock Exchange = ',stock_exchange,'\n', 'CEO = ', ceo,'\n', 'Buisness Sectors= ', buisness,'\n',)

        # writing to csv file with columns names
        with open('value_today.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            # writing column names
            writer.writerow([cname, hq, mcap, annual_rev, number_of_employees, stock_exchange, ceo, buisness])



with open('value_today.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    # writing column names
    writer.writerow(['Company Name', 'Headquarters', 'Market Capital', 'Annual Revenue', 'Number of Employees', 'Stock Exchange', 'CEO', 'Buisness Sectors'])
for i in range(1068, 1069):
    url = 'https://www.value.today/?title=&field_company_category_primary_target_id&field_headquarters_of_company_target_id=All&field_company_website_uri=&field_market_value_jan072022_value=&page=' + str(i)
    print('Parsing page: ',i, url)
    r = requests.get(url)
    parser(r.text)
