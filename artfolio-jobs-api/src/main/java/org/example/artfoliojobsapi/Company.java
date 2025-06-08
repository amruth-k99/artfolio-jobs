package org.example.artfoliojobsapi;

import org.springframework.data.annotation.Id;


//{
//        "companyID": 545744184,
//        "companyName": "New York State",
//        "companyDomain": "www.ny.gov",
//        "revenue": "$292 Billion",
//        "revenueRange": "Over $5 bil.",
//        "employees": 223760,
//        "employeesRange": "Over 10,000",
//        "companyLogo": null,
//        "location": {
//        "Street": "1 Commerce Pl 99",
//        "City": "Albany",
//        "State": "New York",
//        "Zip": "12231",
//        "CountryCode": "United States"
//        },
//        "companyDescription": "The State of New York provides government services to residents, focusing on public safety, health, and education. Founded in 1788, it operates in the public administration sector.",
//        "industry": [
//        "Government",
//        "State",
//        "Government"
//        ],
//        "companyType": "PRIVATE",
//        "website": "www.ny.gov"
//}


public class Company {
    @Id
    public String companyID;
    public String companyName;
    public Company(String companyID, String companyName) {
        this.companyID = companyID;
        this.companyName = companyName;
    }

    public String getCompanyID() {
        return companyID;
    }

}
