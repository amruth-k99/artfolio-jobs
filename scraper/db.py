
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import pymongo

# load environment variables from .env file
load_dotenv('.env')
uri = os.getenv("MONGO_DB_URI")

global client, db, DB_NAME
DB_NAME = "artfolio_jobs"
db = None

job_object = {
    "companyID": 8110814,
    "companyName": "Cigna",
    "companyDomain": "www.cigna.com",
    "revenue": "$247.1 Billion",
    "revenueRange": "Over $5 bil.",
    "employees": 73500,
    "employeesRange": "Over 10,000",
    "companyLogo": '',
    "location": {
        "Street": "900 Cottage Grove Rd",
        "City": "Bloomfield",
        "State": "Connecticut",
        "Zip": "06002",
        "CountryCode": "United States"
    },
    "companyDescription": "Cigna Corporation, a health services organization, provides insurance and related products and services in the United States and internationally. It operates through Global Health Care, Global Supplemental Benefits, Group Disability and Life, and Other Operations segments. The Global Health Care segment offers medical, dental, behavioral health, vision, and prescription drug benefit plans, as well as health advocacy programs, and other products and services to insured and self-insured customers. This segment also provides Medicare Advantage and Medicare Part D plans to seniors, and Medicaid plans. The Global Supplemental Benefits segment offers supplemental health, life, and accident insurance products. The Group Disability and Life segment provides group long-term and short-term disability, group life, accident, and specialty insurance products and related services. The Other Operations segment offers corporate-owned life insurance products that are permanent insurance contracts sold to corporations to provide life coverage; and run-off settlement annuity contracts. The company distributes its products and services through insurance brokers and insurance consultants; and directly to employers, unions and other groups, or individuals, as well as through direct response television and the Internet. Cigna Corporation was founded in 1982 and is headquartered in Bloomfield, CT.",
    "industry": [
        "Insurance",
        "Insurance"
    ],
    "companyType": "PRIVATE",
    "website": "www.cigna.com"
}

if not uri:
    raise ValueError(
        "MONGO_DB_URI environment variable is not set. Please set it in your .env file.")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


def connect_to_mongodb():
    """
    Connect to MongoDB using the provided URI.
    """
    try:
        client.server_info()  # Trigger a connection
        print("MongoDB connection successful.")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        raise


try:
    print("Connecting to MongoDB...")
    db = client[DB_NAME]
    # create a collection if it doesn't exist
    if 'companies' not in db.list_collection_names():
        db.create_collection('companies')
    # Ensure companyName is unique
    db["companies"].create_index("companyID", unique=True)
    print(f"Connected to database: {DB_NAME}")
except Exception as e:
    print(e)
    print("Failed to connect to MongoDB. Please check your connection string and network settings.")


def check_if_company_exists(company_name):
    """
    Check if a company exists in the database.

    :param company_name: Name of the company to check.
    :return: True if the company exists, False otherwise.
    """
    companies = db['companies']
    return companies.count_documents({"companyName": company_name}) > 0


def insert_company_dump(companies):
    """
    Insert a list of companies into the database.

    :param companies: List of companies to insert.
    """
    collection = db['companies']
    try:
        # Insert many companies into the collection
        duplicate_ids = []
        try:

            print(
                f"[{companies[0]['revenue']}]")
            # check if exists
            checks = collection.find(
                {"companyID": {"$in": [company['companyID']
                                       for company in companies]}},
                {"companyID": 1}
            )
            existing_ids = {doc['companyID'] for doc in checks}
            companies = [
                company for company in companies if company['companyID'] not in existing_ids]

            print(
                f"Found {len(existing_ids)} existing companies. Inserting {len(companies)} new companies...")

            if not companies:
                return True
            res = collection.insert_many(companies, ordered=False)
            print(
                f"Inserting {len(res.inserted_ids)} new companies...")
        except pymongo.errors.BulkWriteError as e:
            print('Bulk write error occurred. Attempting to insert one by one...')
            for error in e.details['writeErrors']:
                if error['code'] == 11000:
                    print(
                        f"Duplicate key error for companyID: {error['op']['companyID']}. Skipping this company.")
                    duplicate_ids.append(error['op']['companyID'])
        except Exception as e:
            print(f"An error occurred while inserting companies: {e}")
            return False
        return True
    except pymongo.errors.BulkWriteError as e:
        # Handle duplicate key errors
        print(
            f"Bulk write error: {len(e.details['writeErrors'])} documents failed to insert due to duplicate keys.")
        return True

    except Exception as e:
        print(e)
        # Handle any other exceptions that may occur
        print(f"An error occurred while inserting companies: {e}")
        return False


def create_company(company):
    """
    Create a new company in the database.

    :param company: Company object to insert.
    :return: The inserted company object.
    """
    if not check_if_company_exists(company['companyName']):
        collection = db['companies']
        result = collection.insert_one(company)
        print(f"Inserted company with ID: {result.inserted_id}")
        return company
    else:
        print(f"Company {company['companyName']} already exists.")
        return None
