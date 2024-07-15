# import requests
# from dotenv import load_dotenv
# import os

# # Load environment variables from the .env file
# load_dotenv()

# # Get the Postman API key from the environment
# postman_api_key = os.getenv('POSTMAN_API_KEY_3')
# print(postman_api_key)

# if not postman_api_key:
#     raise ValueError("POSTMAN_API_KEY not set in the environment")

# # Define the Postman API URL for running a collection
# postman_collection_uid = os.getenv("POSTMAN_COLLECTION_ID")
# url = f"https://api.getpostman.com/collections/{postman_collection_uid}"

# # Set up the headers with the API key
# headers = {
#     'X-Api-Key': postman_api_key,
#     'Content-Type': 'application/json'
# }

# # Send the request to run the collection
# response = requests.get(url, headers=headers,timeout=20)

# # Check the response status
# if response.status_code == 200:
#     print("Collection fetched successfully")
#     collection_data = response.json()
#     print(collection_data)
# else:
#     print(f"Failed to fetch collection: {response.status_code}")
#     print(response.text)


##################################################################