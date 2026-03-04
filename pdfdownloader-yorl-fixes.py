#Imports libaries such as Pandas for data processing and pathlib for handling filesystem paths.
#Urllib is a libary that is used to work with URLs such as fetching werb data, parsing URLs etc. 
#Import os allows us to interact with the operating system.
import pandas as pd # Will not work if Openpyxl is not installed, subdependency should be listed in README.md file 
from pathlib import Path # Nice
import urllib.request # Nice
import os #Nice

#These are variables that contain the locations of the folders that contain the PDFs and the folder where the PDFs needs to be downloaded to.
#The DOWNLOAD_DIR variable contains the output folder with the forward slash operator from pathlib that creates a new folder called "dwn"
#ID_COL and URL_COL are used as variables instead of hardcoding "BRnum" and "pdf_URL" every time. 
INPUT_EXCEL = Path("C:/Users/SPAC-49/Documents/Softwareudvikling/Uge 5/PDF-downloader--main/test-data.xlsx") # Nice
OUTPUT_DIR = Path("C:/Users/SPAC-49/Documents/Softwareudvikling/Uge 5/PDF-downloader--main/output") # Nice
DOWNLOAD_DIR = OUTPUT_DIR / "dwn" #Seems redundant, no? Why not output directly into output directory?
ID_COL = "BRnum" # Nice
URL_COL = "Pdf_URL" # Nice

#This is the main function in which the downloading of the PDFs occurs.
def main():
    print("Program started")
    if INPUT_EXCEL.exists(): # protects against input not found
        pass
    else:
        print("Input not found. Self terminating.")
        quit()
    # Has no error handling, this is not meant to be pedantic
    if OUTPUT_DIR.exists(): # prevents crash occurs if output_dir does not exist
        #print("Output folder already exists") # folder is expected to exist
        pass
    else: 
        OUTPUT_DIR.mkdir()
        print("Created output folder")
    
    if DOWNLOAD_DIR.exists(): #  crash if output folder does not exist, lack of error handling, solved by validating if prev dir exists
        #print("Download folder already exists")
        pass
    else: 
        DOWNLOAD_DIR.mkdir()
        print("Created download folder")


    #df is used to work with table data
    df = pd.read_excel(INPUT_EXCEL) # Requires Openpyxl dependency for writer engine
    print("rows loaded:", df.shape[0]) # these are nice but redundant
    print("Columns:", df.columns) #
    
    #Checks that the column containing IDs exists.
    if ID_COL not in df.columns: # error handling / data check
        print(ID_COL + " ID column is missing")
        quit() #Stops the program because the required column is missing
    #Checks that the column containing URLs exists.
    if URL_COL not in df.columns: # error handling / data check
        print(URL_COL + " URL column is missing")
        quit() #Stops the program if the url column is not present

    # Create an empty set that will store IDs of PDFs that already exist
    #ext defines the file extension used for the downloaded reports
    existing_ids = set()
    ext = (".pdf")

    #This conditional loops through all files that already exist in the download directory
    #It only looks at files that end with ".pdf"
    #It removes the extension and adds the ID to the set of already-downloaded reports
    for existing_id in os.listdir(DOWNLOAD_DIR): # Crash occurs when directory not found
        if existing_id.endswith(ext):
            new_id = existing_id.replace(ext, "")
            existing_ids.add(new_id)
    print(len(existing_ids))


    # Creates a copy of the original dataframe so we don't modify the original data
    df_to_download = df.copy()
    # Keep only rows where the PDF URL column is not empty
    # (i.e., reports that actually have a downloadable PDF)
    df_to_download = df_to_download[ df_to_download[URL_COL].notnull() ] # notnull check is a great way to go about it
    # Remove rows where the report ID already exists in the download folder
    # This prevents downloading the same PDF multiple time
    df_to_download = df_to_download[~df_to_download[ID_COL].isin(existing_ids)] # nice

    print("Remaining PDFs to download:", len(df_to_download)) # Now it shows how many are left to be downloaded

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

        try: # Very good
        # Download the PDF from the URL and save it to the specified path
            urllib.request.urlretrieve(url_value, save_path)
        except:
        # Prints which report failed
            print(f'Failed to download {id_value}, {url_value}')
   
    #print("Remaining PDFs to download:", len(df_to_download)) # Should this not be at the start of the download? Why after?

#This ensures that main() only runs when the script is executed directly
if __name__ == "__main__": # Very nice
    main()