import os

def sandbox():
    try:
        # Define the root folder path
        root_folder = 'api-test'

        # Define the folder structure relative to the root folder
        folders = [
            'src/main/java/com/example/api/utils',
            'src/test/java/com/example/api/base',
            'src/test/java/com/example/api/tests',
            'resources'
        ]

        # Create the directories under the root folder
        for folder in folders:
            os.makedirs(os.path.join(root_folder, folder), exist_ok=True)
        
        # Define the files to be created with their paths relative to the root folder
        files = [
            'src/main/java/com/example/api/utils/ConfigManager.java',
            'src/main/java/com/example/api/utils/ApiUtils.java',
            'src/main/java/com/example/api/utils/ResponseValidator.java',
            'src/test/java/com/example/api/base/BaseTest.java',
            'resources/config.properties',
            'testng.xml',
            'pom.xml'
        ]

        # Create the files under the root folder
        for file in files:
            open(os.path.join(root_folder, file), 'w').close()  # Create an empty file

        return True, os.path.abspath(root_folder)  # Return True and the absolute path of the root folder
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, None  # Return False and None if an error occurs