#Imports libaries such as Pandas for data processing and pathlib for handling filesystem paths.
#Urllib is a libary that is used to work with URLs such as fetching werb data, parsing URLs etc. 
#Import os allows us to interact with the operating system.
import pandas as pd
from pathlib import Path 
import urllib.request
import os

#These are variables that contain the locations of the folders that contain the PDFs and the folder where the PDFs needs to be downloaded to.
#The DOWNLOAD_DIR variable contains the output folder with the forward slash operator from pathlib that creates a new folder called "dwn"
#ID_COL and URL_COL are used as variables instead of hardcoding "BRnum" and "pdf_URL" every time. 
INPUT_EXCEL = Path("C:/Users/Spac-43/Desktop/pdf_downloader/excel_files/GRI_2017_2020.xlsx")
OUTPUT_DIR = Path("C:/Users/Spac-43/Desktop/pdf_downloader/output")
DOWNLOAD_DIR = OUTPUT_DIR / "dwn"
ID_COL = "BRnum"
URL_COL = "Pdf_URL"

#This is the main function in which the downloading of the PDFs occurs.
def main():

    #When the program starts, it will check if there is a download folder. If not it will create it.
    print("Program started")
    if DOWNLOAD_DIR.exists(): 
        print("Download folder already exists")
    else: 
        DOWNLOAD_DIR.mkdir()
        print("Created download folder")
    
    #df is used to work with table data
    df = pd.read_excel(INPUT_EXCEL)
    print("rows loaded:", df.shape[0])
    print("Columns:", df.columns)
    
    #Checks that the column containing IDs exists.
    if ID_COL not in df.columns:
        print(ID_COL + " ID column is missing")
        quit() #Stops the program because the required column is missing
    #Checks that the column containing URLs exists.
    if URL_COL not in df.columns:
        print(URL_COL + " URL column is missing")
        quit() #Stops the program if the url column is not present

    # Create an empty set that will store IDs of PDFs that already exist
    #ext defines the file extension used for the downloaded reports
    existing_ids = set()
    ext = (".pdf")

    #This conditional loops through all files that already exist in the download directory
    #It only looks at files that end with ".pdf"
    #It removes the extension and adds the ID to the set of already-downloaded reports
    for existing_id in os.listdir(DOWNLOAD_DIR):
        if existing_id.endswith(ext):
            new_id = existing_id.replace(ext, "")
            existing_ids.add(new_id)
    print(len(existing_ids))


    # Creates a copy of the original dataframe so we don't modify the original data
    df_to_download = df.copy()
    # Keep only rows where the PDF URL column is not empty
    # (i.e., reports that actually have a downloadable PDF)
    df_to_download = df_to_download[ df_to_download[URL_COL].notnull() ]
    # Remove rows where the report ID already exists in the download folder
    # This prevents downloading the same PDF multiple time
    df_to_download = df_to_download[~df_to_download[ID_COL].isin(existing_ids)]

    # Loop through each remaining row in the filtered dataframe
    # Each row represents one report that still needs to be downloaded
    for index, row in df_to_download.iterrows():

        # Extract the report ID from the current row
        # This will be used to name the downloaded PDF
        id_value = row[ID_COL]
        # Extract the URL where the PDF file is located
        url_value = row[URL_COL]

        # Create the full file path where the PDF should be saved
        # Example: output/dwn/BR12345.pdf
        save_path = DOWNLOAD_DIR / (id_value + ext)

        try:
        # Download the PDF from the URL and save it to the specified path
            urllib.request.urlretrieve(url_value, save_path)
        except:
        # Prints which report failed
            print(f'Failed to download {id_value}, {url_value}')
   
    print("Remaining PDFs to download:", len(df_to_download))

#This ensures that main() only runs when the script is executed directly
if __name__ == "__main__": 
    main()