import os
import win32com.client
from tqdm import tqdm


wdFormatPDF = 17

BASE_PATH = os.getcwd()

INPUT_FOLDER = '身份证_docx'
OUTPUT_FOLDER = '身份证_pdf'

INPUT_PATH = os.path.join(BASE_PATH, INPUT_FOLDER)
OUTPUT_PATH = os.path.join(BASE_PATH, OUTPUT_FOLDER)

if OUTPUT_FOLDER not in os.listdir(BASE_PATH):
    os.mkdir(OUTPUT_PATH)

word = win32com.client.Dispatch("Word.Application")

for file in tqdm(os.listdir(INPUT_PATH)):

    inputFile = os.path.abspath(os.path.join(INPUT_PATH, file))
    outputFile = os.path.abspath(os.path.join(OUTPUT_PATH, file.strip('.docx')+'.pdf'))
    
    docx = word.Documents.Open(inputFile)
    docx.SaveAs(outputFile, FileFormat=wdFormatPDF)

docx.Close()
word.Quit()