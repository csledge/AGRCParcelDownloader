# Download parcel data from AGRC and unzip the GDB to the target directory
# This script creates a dictionary object and loops through it for the downloads
# It will delete all files and geodatabases in the target directory, download the files, and unzip them
# Add new county parcels and their Google ID's to the dictionary as needed
# Get the ID's for each county in Utah here: https://drive.google.com/drive/folders/0ByStJjVZ7c7meVNnTThOSzVUeEk

googleIDs = {'BoxElder' : '0ByStJjVZ7c7mQUUzRVh5ZTJfS00',
'Davis' : '0ByStJjVZ7c7mQzVKQ0p3WU5YVUk',
'SaltLake' : '0ByStJjVZ7c7mdUl4akRQZDk4YTg',
'Utah' : '0ByStJjVZ7c7mQnlCNVIwZVZVUUk'
}

theDir = '<target directory>'

import requests, os, zipfile, shutil

def downloadParcels(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

if __name__ == "__main__":
    # Delete all the files in the target Directory
    for the_file in os.listdir(theDir):
        file_path = os.path.join(theDir, the_file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print file_path + " removed"
        except Exception as e:
            print(e)

    # Delete all the geodatabases
        try:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print file_path + " removed"
        except Exception as e:
            print(e)


    # Download the parcels from the AGRC Google Drive
    for the_key, the_value in googleIDs.iteritems():
        print 'Downloading ' + the_key
        downloadParcels(the_value, theDir + "\\" + the_key + '.gdb.zip')

    print "All downloads complete. Unzipping..."

    # Unzip all the files
    for the_file in os.listdir(theDir):
        try:
            zipped = zipfile.ZipFile(theDir + "\\" + the_file, 'r')
            zipped.extractall(theDir)
            zipped.close()
            print the_file + " unzipped"
        except Exception as e:
            print(e)
    print "Everything is unzipped"

print "All done"
