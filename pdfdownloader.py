import pandas as pd
from pathlib import Path 
import urllib.request


INPUT_EXCEL = Path("C:/Users/Spac-43/Desktop/pdf_downloader/excel_files/GRI_2017_2020")
OUTPUT_DIR = Path("C:/Users/Spac-43/Desktop/pdf_downloader/output")
DOWNLOAD_DIR = OUTPUT_DIR / "dwn"
ID_COL = "BRnum"
URL_COL = "Pdf_URL"


def main():
    print("Program started")
    if DOWNLOAD_DIR.exists(): 
        print("Download folder already exists")
    else: 
        DOWNLOAD_DIR.mkdir()
        print("Created download folder")

    df = pd.read_excel(INPUT_EXCEL)
    print("rows loaded:", df.shape[0])
    print("Columns:", df.columns)
    
    if ID_COL not in df.columns:
        print("ID column is missing")
        quit()

    if URL_COL not in df.columns:
        print("ID column is missing")
        quit()
    
    
    print("Column exists")

if __name__ == "__main__": 
    main()