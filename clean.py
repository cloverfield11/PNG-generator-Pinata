import requests  # The library used for making HTTP requests

PINATA_JWT = "PINATA_JWT"  # Replace with your Pinata JWT (JSON Web Token) for authentication

def get_pinned_files(pinata_jwt): #Function to fetch the list of pinned files from Pinata using Pinata JWT.
    url = "https://api.pinata.cloud/data/pinList?pageLimit=100"
    headers = {
        'Authorization': f'Bearer {pinata_jwt}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("rows", [])
    else:
        return []

def delete_from_pinata(pinata_jwt, cid): #Function to delete a file from Pinata using Pinata JWT and Content ID (CID).
    url = f"https://api.pinata.cloud/pinning/unpin/{cid}"
    headers = {
        'Authorization': f'Bearer {pinata_jwt}'
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False

# Fetch the list of pinned files from Pinata
pinned_files = get_pinned_files(PINATA_JWT)

# Iterate through the pinned files and delete them from Pinata
for file in pinned_files:
    cid = file.get("ipfs_pin_hash")
    if cid:
        if delete_from_pinata(PINATA_JWT, cid):
            print(f"File deleted successfully. CID: {cid}")
        else:
            print(f"Failed to delete file. CID: {cid}")
    else:
        print("Failed to get CID for file.")
