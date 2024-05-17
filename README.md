NFT Cat Generator
================

NFT Cat Generator is a simple Python application that allows you to generate a specified number of NFTs (Non-Fungible Tokens) with random attributes and upload the images and metadata to Pinata, an IPFS (InterPlanetary File System) pinning service.

Requirements
------------

* Python 3.x
* Pillow (Python Imaging Library)
* requests
* tkinter

Installation
------------

1. Clone the repository: `git clone https://github.com/cloverfield11/PNG-generator-Pinata`
2. Install the required packages: `pip install -r requirements.txt`
3. Replace the `PINATA_API_KEY` and `PINATA_SECRET_KEY` placeholders in the code with your actual Pinata API key and secret key.

Usage
-----

1. Run the application: `python main.py`
2. Enter the number of NFTs you want to generate in the "Count of NFT's" field.
3. Click the "Generate NFT" button.
4. The application will generate the specified number of NFTs with random attributes, save the images and metadata to the "Cat NFT" directory, and upload the images and metadata to Pinata.
5. If the NFTs are generated and uploaded successfully, a "Success NFT generation" message will be displayed.

File Structure
---------------

* `nft_cat_generator.py`: The main Python script that contains the logic for generating the NFTs and uploading them to Pinata.
* `requirements.txt`: A list of the required Python packages.
* `Cat NFT/`: The directory where the generated images and metadata are saved.
* `metadata_cids.txt`: A file that contains the Content IDs (CIDs) of the uploaded metadata.

Acknowledgments
---------------

* Pinata (<https://pinata.cloud/>) for providing the IPFS pinning service.
* The Pillow (Python Imaging Library) developers (<https://pillow.readthedocs.io/en/stable/>) for creating the library used for working with images in this project.
* The requests library developers (<https://requests.readthedocs.io/en/latest/>) for creating the library used for making HTTP requests in this project.
* The tkinter library developers (<https://docs.python.org/3/library/tkinter.html>) for creating the library used for creating the GUI in this project.
