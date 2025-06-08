import requests
import json
from time import sleep
from .db import insert_company_dump
import math
import os


def fetch_companies(page):
    try:
        url = os.getenv('SCRAPER_URL')
        query = {
            'searchFacadeParams':
            {
                'page': page,
                "companyPastOrPresent": "1",
                "isCertified": "include",
                "sortBy": "Revenue,company_id",
                # "sortOrder": "asc,asc",
                "sortOrder": "desc,desc",
                "excludeDefunctCompanies": True,
                "confidenceScoreMin": 85,
                "confidenceScoreMax": 99,
                "outputCurrencyCode": "USD",
                "inputCurrencyCode": "USD",
                "excludeNoCompany": "false",
                "returnOnlyBoardMembers": False,
                "excludeBoardMembers": True,
                "fetchLeadIndicator": True,
                "timestamp": 1749379104890,
                "country": "United States",
                "employeeSizeMin": 5,
                "revenueMinIn000s": 40000,
                "revenueMaxIn000s": 45600,
                "searchType": 1,
                "contactRequirements": "",
                "searchUUID": "75d2e386-1d6e-4f0d-a7fb-9d4481fdca29",
                "locationSearchType": "HQ",
                "rpp": 50,
                "useUnifiedSearch": True
            }
        }

        query = json.dumps(query)

        payload = "{\"query\":\"query companySearch($searchFacadeParams: CompanyArgs) {\\n  companySearch(searchFacadeParams: $searchFacadeParams) {\\n    emptyResponseReasonIntent\\n    maxResults\\n    totalResults\\n    facetData {\\n      facets {\\n        name\\n        counts {\\n          id\\n          name\\n          displayName\\n          count\\n          searchValue\\n        }\\n      }\\n    }\\n    data {\\n      icpScore\\n      companyID: id\\n      companyLogo: logo\\n      companyName: name\\n      location: address {\\n        Street\\n        City\\n        State\\n        Zip\\n        CountryCode\\n      }\\n      revenue\\n      revenueRange\\n      employees: employeeCount\\n      employeesRange\\n      companyDomain: domain\\n      companyDescription: description\\n      companyPhone: phone\\n      companyPhoneBlocked\\n      companyPhoneBlockedReason\\n      companyRevenueIn000s\\n      doziIndustry {\\n        displayName\\n        name\\n        isPrimary\\n        score\\n      }\\n      companyType: type\\n      certified\\n      certificationDate\\n      topLevelIndustry\\n      totalFundingAmountIn000s\\n      isDefunct\\n      funding {\\n        amountIn000s\\n        date\\n        investors {\\n          companyName\\n          investorName\\n          investorDomain\\n          investorCompanyId\\n        }\\n        round\\n      }\\n      isMasked: masked\\n      isTagged: tagged\\n      subscribed\\n      universalTagged\\n      accountLevelIntentsList {\\n        accountLevelIntentsScore\\n        topicId\\n        clusterId\\n        signalLocations\\n      }\\n      orgUniversalTagged {\\n        tagName\\n        value\\n      }\\n    }\\n  }\\n}\\n\",\"variables\":" + query + "}"
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'session-token': '1',
            'user': '32916257',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'x-datadog-origin': 'rum',
            'x-datadog-parent-id': '2244881626225545519',
            'x-datadog-sampling-priority': '0',
            'x-datadog-trace-id': '8590516587827117603',
            'x-sourceid': 'ZI_LITE',
            'x-ziaccesstoken': 'eyJraWQiOiJndTM2elFSUVJjdERzbjRGaDU1Vk1kWHdWV0RNazZ2amhDUDN4cE84RGlRIiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULjRMbGlhUnZYMDRlTmJpVV93VDdUcmFqMW5XY1ZqRTF6OWExaXpMUWt5Mkkub2FyMnJ3dG55NWZkS2NTcjU2OTciLCJpc3MiOiJodHRwczovL29rdGEtbG9naW4uem9vbWluZm8uY29tL29hdXRoMi9kZWZhdWx0IiwiYXVkIjoiYXBpOi8vZGVmYXVsdCIsInN1YiI6ImFtcnV0aEByZXNpemVyLnRlY2giLCJpYXQiOjE3NDkzNzg2NDgsImV4cCI6MTc0OTQ2NTA0OCwiY2lkIjoiMG9hOTlkc21ibkF4bGV2RjM2OTYiLCJ1aWQiOiIwMHVyZGN1NnJuQk5URWV4RjY5NyIsInNjcCI6WyJvZmZsaW5lX2FjY2VzcyIsIm9wZW5pZCIsImVtYWlsIiwicHJvZmlsZSJdLCJhdXRoX3RpbWUiOjE3NDkzNzg2NDYsImxhc3ROYW1lIjoiS3VudGFtYWxsYSIsInppU2Vzc2lvblR5cGUiOi0zLCJ6aUdyb3VwSWQiOjAsInppQ29tcGFueVByb2ZpbGVJZCI6IiIsInppUGxhdGZvcm1zIjpbIkNPTU1VTklUWSJdLCJ6aUFkbWluUm9sZXMiOiIiLCJ6aVVzZXJuYW1lIjoiYW1ydXRoQHJlc2l6ZXIudGVjaCIsImZpcnN0TmFtZSI6IkFtcnV0aCIsInppUm9sZXMiOiJCcVFnUnNnNWdFRUF3QmdBd0dVQUFBQUVBQUFBQUFBUUFBQUFBQUFBQUFBQUFBQkFBQUFBQUFBd0FBQUFBQUFBQUFBSSIsInppVXVpZCI6IjM1NTc4YTE1LWNjOGItNDExNi05MGYxLTQ3ODlkOGU0MDE2MiIsInppVXNlcklkIjozMjkxNjI1Nywic2ZDb250YWN0SWQiOiIwMDM3eTAwMDAxOGF1eHZBQUEiLCJ6aUluYWN0aXZpdHkiOjYwNDgwMCwiemlUZW5hbnRJZCI6MjEyODMxOTAsImVtYWlsIjoiYW1ydXRoQHJlc2l6ZXIudGVjaCIsInNmQWNjb3VudElkIjoiMDAxN3kwMDAwMUEwWURBQUEzIiwiemlNb25nb1VzZXJJZCI6IjMyOTE2MjU3In0.BwDaLGvi2vH2CIKEFjeBwrBTgbWum4yA6vvxpc_KTClbrs-JZwewvDo63iccaNGRYnorrNHDgRCrU1uP1_fZ9FH62bqRCN6O3woVbt4axM5JEXbJonAcAhZJ1z9FoRVHzsxyTv7gmjC1g89yBi-x0n2rQeQjGxVOmRbG7pgg0J1-dP594SIPsH37SbiThHC3vFTqcp_IFgA_jtj5gWgiscx_tbKjr8kLpjbAzx3G-gdWPwGc4mwpTA9cN4XPlv-hrZX-w9pEEU42WfXQPEmj_xVDaeLuA8Eo0q-H3_U3_GQif7bIq6opZb_l5d-jK_Yc4TlPju4ca0eVS1bt_iUNyQ',
            'x-ziid': 'KlJWa5T4OvqzMOb2ROYZDjUMrs9VxAeIyJeZKP9Zs1KL7bBpBcRyv-tRW4MZmY_lvjARoGCeOBeHTc8UiIFyug',
            'x-zisession': 'KlJWa5T4OvqzMOb2ROYZDjUMrs9VxAeIyJeZKP9Zs1KL7bBpBcRyv-tRW4MZmY_lvjARoGCeOBfJCd7lkY0vmQ3SGGWHjsOY7slYR3OxmqstJWY9JVr_16bersyAvwk0',
        }
        response = requests.request(
            "POST", url, headers=headers, data=payload)
        response = response.json()
        total_results = response['data']['companySearch']['maxResults']
        return response['data']['companySearch']['data'], total_results
    except Exception as e:
        print(f'[Scraper API] Error fetching companies on page {page}: {e}')
        return [], 0


def start_scraping():
    try:
        print('[Scraper API] Starting scraping...')

        results_fetched = 0
        current_page = 1
        total_results = 5000
        while results_fetched <= total_results:
            print(f'Fetching page {current_page*50}/{total_results}...')
            batch, t = fetch_companies(current_page)
            total_results = t
            if not batch:
                print('No more results found.')
                break
            results_fetched += len(batch)
            sanitized_companies = []
            for company in batch:
                industries = []
                if "topLevelIndustry"not in company:
                    print('No industries found for this company.')
                else:
                    industries.extend(company['topLevelIndustry'])

                if "doziIndustry"not in company:
                    print('No top level industry found for this company.')
                else:
                    for industry in company['doziIndustry']:
                        if industry not in industries:
                            industries.append(industry['displayName'])

                sanitized_companies.append({
                    'companyID': company['companyID'],
                    'companyName': company['companyName'],
                    'companyDomain': company['companyDomain'],
                    'revenue': company['revenue'],
                    'revenueRange': company['revenueRange'],
                    'employees': company['employees'],
                    'employeesRange': company['employeesRange'],
                    'companyLogo': company['companyLogo'],
                    'location': company['location'],
                    'companyDescription': company['companyDescription'],
                    "industry": industries,
                    'companyType': company['companyType'],
                    'website': company['companyDomain'],

                })
            insert_company_dump(sanitized_companies)

            # randomly sleep to avoid rate limiting
            sleep(4)

            current_page += 1

        print('[Scraper API] Scraping completed successfully.')
    except Exception as e:
        print('[Scraper API] An error occurred during scraping.', e)


start_scraping()
