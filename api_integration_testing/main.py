import json
import os
import logging
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_test.log'),
        logging.StreamHandler()
    ]
)

def load_postman_collection(postman_api_key,postman_collection_uid):
    """
    Load and parse the Postman collection JSON from an API call.

    Args:
        api_url (str): The URL to the Postman API collection.
        access_key (str): The access key to authenticate the request.

    Returns:
        dict: Parsed JSON content of the Postman collection.
    """
    logging.info('Loading Postman collection from API')
    url = f"https://api.getpostman.com/collections/{postman_collection_uid}"

    # Set up the headers with the API key
    headers = {
        'X-Api-Key': postman_api_key,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers,timeout=20)
        response.raise_for_status()  # Raise an error for bad status codes
        postman_collection = response.json()
        logging.info('Successfully loaded Postman collection')
        return postman_collection
    except requests.exceptions.RequestException as e1:
        logging.error("Error loading Postman collection: %s", e1)
        raise

def extract_info(postman_collection):
    """
    Extract relevant information from the Postman collection.

    Args:
        postman_collection (dict): The parsed JSON content of the Postman collection.

    Returns:
        list: A list of dictionaries containing API endpoint information.
    """
    logging.info('Extracting information from Postman collection')
    api_endpoints = []

    def process_item(item):
        """
        Process a single item from the Postman collection.

        Args:
            item (dict): An item from the Postman collection.
        """
        # Extract relevant information from each item
        name = item.get('name')
        request = item.get('request', {})
        response = item.get('response', [])

        method = request.get('method')
        url = request.get('url', {})
        path = url.get('raw')
        headers = request.get('header', [])
        body = request.get('body', {}).get('raw')  # Extract request body

        # Extract expected responses
        expected_response = {}
        if response:
            expected_response['status'] = response[0].get('code')
            expected_response['body'] = response[0].get('body')

        # Add extracted information to the list of API endpoints
        api_endpoints.append({
            'name': name,
            'method': method,
            'url': path,
            'headers': headers,
            'body': body,
            'expected_response': expected_response
        })

    items = postman_collection.get('collection', {}).get('item', [])
    for item in items:
        process_item(item)

    logging.info('Successfully extracted information from Postman collection')
    return api_endpoints

def save_extracted_info(api_endpoints, output_file):
    """
    Save the extracted API endpoint information to a file.

    Args:
        api_endpoints (list): A list of dictionaries containing API endpoint information.
        output_file (str): The path to the output file where the information will be saved.
    """
    logging.info('Saving extracted information to %s', output_file)
    try:
        with open(output_file, 'a', encoding='utf-8') as file:
            for endpoint in api_endpoints:
                file.write(json.dumps(endpoint, indent=2))
                file.write('\n\n')
        logging.info('Successfully saved extracted information')
    except IOError as e2:
        logging.error('Error saving extracted information: %s', e2)
        raise

# Example usage
POSTMAN_UID=os.getenv("POSTMAN_COLLECTION_ID")
API_KEY = os.getenv("POSTMAN_API_KEY_3")
OUTPUT_FILE_PATH = 'extracted_info.txt'

try:
    POSTMAN_COLLECTION = load_postman_collection(API_KEY,POSTMAN_UID)
    API_ENDPOINTS = extract_info(POSTMAN_COLLECTION)
    save_extracted_info(API_ENDPOINTS, OUTPUT_FILE_PATH)
    logging.info("Extracted information saved to %s", OUTPUT_FILE_PATH)
except Exception as e:
    logging.error('Failed to process Postman collection: %s', e)