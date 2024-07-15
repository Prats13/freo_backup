import os

def create_sandbox_env():
    try:
        # Define the folder structure
        folders = [
            'api-test/src/main/java/com/example/api/utils',
            'api-test/src/test/java/com/example/api/base',
            'api-test/src/test/java/com/example/api/tests',
            'api-test/resources'
        ]

        # Define the files to be created
        files = [
            'api-test/src/main/java/com/example/api/utils/ConfigManager.java',
            'api-test/src/main/java/com/example/api/utils/ApiUtils.java',
            'api-test/src/main/java/com/example/api/utils/ResponseValidator.java',
            'api-test/src/test/java/com/example/api/base/BaseTest.java',
            'api-test/resources/config.properties',
            'api-test/testng.xml',
            'api-test/pom.xml'
        ]

        # Create the directories
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
        
        # Create the files
        for file in files:
            with open(file, 'w') as f:
                pass  # Create an empty file

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Call the function and print the result
result = create_sandbox_env()
print(f"Sandbox environment creation successful: {result}")
