import os
import random
import requests
from PIL import Image, ImageTk # Libraries for working with images
import json
import tkinter as tk # GUI library

PINATA_API_KEY = "PINATA_API_KEY" # Replace with your Pinata API Key
PINATA_SECRET_KEY = "PINATA_SECRET_KEY" # Replace with your Pinata Secret Key

metadata_cids = [] # List to store the Content IDs (CIDs) of the uploaded metadata
metadata_cids_file_path = "metadata_cids.txt"

def upload_to_pinata(file_path): # Function to upload a file to Pinata and return its IPFS hash.
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_KEY
    }

    with open(file_path, "rb") as file:
        response = requests.post(url, files={"file": file}, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result["IpfsHash"]
        else:
            return None
        
def update_metadata_image_url(metadata, ipfs_hash): # Function to update the 'image' field in the metadata with the IPFS URL.
    metadata["image"] = f"https://ipfs.io/ipfs/{ipfs_hash}"

def upload_metadata_to_pinata(metadata): # Function to upload metadata to Pinata and return its IPFS hash.
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_KEY
    }

    response = requests.post(url, json=metadata, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result["IpfsHash"]
    else:
        return None
    
def save_metadata_cids_to_file(cids): # Function to save the Content IDs (CIDs) of the uploaded metadata to a file.
    with open(metadata_cids_file_path, "w") as file:
        file.writelines([f"'{cid}',\n" for cid in cids])
    
def generate_nft(num_images): # Function to generate a specified number of NFTs with random attributes.
    global metadata_cids

    body_parts = { #Dictionary containing the file names and probabilities for each body part
        "body": [
            {"file": "part/body1.png", "probability": 0.2},
            {"file": "part/body2.png", "probability": 0.2},
            {"file": "part/body3.png", "probability": 0.2},
            {"file": "part/body4.png", "probability": 0.2},
            {"file": "part/body5.png", "probability": 0.2}
        ],
        "head": [
            {"file": "part/head1.png", "probability": 0.2},
            {"file": "part/head2.png", "probability": 0.2},
            {"file": "part/head3.png", "probability": 0.2},
            {"file": "part/head4.png", "probability": 0.2},
            {"file": "part/head5.png", "probability": 0.2}
        ],
        "tail": [
            {"file": "part/tail1.png", "probability": 0.19},
            {"file": "part/tail2.png", "probability": 0.19},
            {"file": "part/tail3.png", "probability": 0.19},
            {"file": "part/tail4.png", "probability": 0.19},
            {"file": "part/tail5.png", "probability": 0.19},
            {"file": "part/tail6.png", "probability": 0.05}
        ],
        "background": [
            {"file": "part/bkg1.png", "probability": 0.3},
            {"file": "part/bkg2.png", "probability": 0.4},
            {"file": "part/bkg3.png", "probability": 0.2},
            {"file": "part/bkg4.png", "probability": 0.1}
        ],
        "butterfly": [
            {"file": "part/fly1.png", "probability": 0.2},
            {"file": "part/fly2.png", "probability": 0.6},
            {"file": "part/fly3.png", "probability": 0.2},
        ]
    }

    output_dir = "Cat NFT"  # Output directory for the generated NFTs
    image_dir = os.path.join(output_dir, "Images")  # Directory for the generated images
    metadata_dir = os.path.join(output_dir, "Metadata")  # Directory for the metadata files

    # Create the directories if they don't exist
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    if not os.path.exists(metadata_dir):
        os.makedirs(metadata_dir)

    for i in range(num_images):
        generated_images = set()
        while True:
            body = random.choices(
                [part["file"] for part in body_parts["body"]],
                [part["probability"] for part in body_parts["body"]]
            )[0]
            head = random.choices(
                [part["file"] for part in body_parts["head"]],
                [part["probability"] for part in body_parts["head"]]
            )[0]
            tail = random.choices(
                [part["file"] for part in body_parts["tail"]],
                [part["probability"] for part in body_parts["tail"]]
            )[0]
            background = random.choices(
                [part["file"] for part in body_parts["background"]],
                [part["probability"] for part in body_parts["background"]]
            )[0]
            butterfly = random.choices(
                [part["file"] for part in body_parts["butterfly"]],
                [part["probability"] for part in body_parts["butterfly"]]
            )[0]

            combination = (body, head, tail, background, butterfly)
            if combination not in generated_images:
                generated_images.add(combination)
                break
        
        metadata = { # Dictionary containing the metadata for the generated NFT
            "name": f"Cat#{i+1}",
            "description": f"Cool cat #{i+1} yours!",
            "image": "",
            "attributes": {
                "body": body,
                "head": head,
                "tail": tail,
                "background": background,
                "butterfly": butterfly
            }
        }

        image = Image.new("RGBA", (458, 458)) # Create a new

        # Create a new RGBA image with the specified dimensions (458x458 pixels)
        image.paste(Image.open(background), (0, 0), mask=Image.open(background).convert("RGBA"))
        image.paste(Image.open(tail), (0, 0), mask=Image.open(tail).convert("RGBA"))
        image.paste(Image.open(body), (0, 0), mask=Image.open(body).convert("RGBA"))
        image.paste(Image.open(head), (0, 0), mask=Image.open(head).convert("RGBA"))
        image.paste(Image.open(butterfly), (0, 0), mask=Image.open(butterfly).convert("RGBA"))
        # Paste the images of the different body parts and the background onto the new image, using the RGBA channels as a mask
        
        filename = f"Sberkot{i+1}.png"
        file_path = os.path.join(image_dir, filename)

        image.save(file_path) # Save the generated image to the file

        ipfs_hash = upload_to_pinata(file_path)
        if ipfs_hash:
            update_metadata_image_url(metadata, ipfs_hash)
        else:
            status_label.config(text="Pinata png upload error!")
            return

        metadata_file_path = os.path.join(metadata_dir, f"Sberkot{i+1}.json") # Create the full file path for the metadata file
        with open(metadata_file_path, "w") as metadata_file:
            json.dump(metadata, metadata_file, indent=4)

        ipfs_hash_metadata = upload_metadata_to_pinata(metadata)
        if not ipfs_hash_metadata:
            status_label.config(text="Pinata metadata upload error")
            return

        metadata_cids.append(ipfs_hash_metadata) # Add the IPFS hash of the metadata to the list of Content IDs (CIDs)

        metadata_file_path = os.path.join(metadata_dir, f"Sberkot{i+1}.json")
        with open(metadata_file_path, "w") as metadata_file:
            json.dump(metadata, metadata_file, indent=4)

    save_metadata_cids_to_file(metadata_cids)

def generate_button_clicked():
    num_images = int(entry_num_images.get())
    generate_nft(num_images)
    status_label.config(text="Success NFT generation")

root = tk.Tk()
root.title("NFT Cat Generator")

label_num_images = tk.Label(root, text="Count of NFT's:")
entry_num_images = tk.Entry(root)
generate_button = tk.Button(root, text="Generate NFT", command=generate_button_clicked)
status_label = tk.Label(root, text="")

label_num_images.grid(row=0, column=0, sticky="E")
entry_num_images.grid(row=0, column=1)
generate_button.grid(row=1, column=0, columnspan=2)
status_label.grid(row=2, column=0, columnspan=2)

root.mainloop()
