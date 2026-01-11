import os
import shutil 
from pathlib import Path


def get_unique_path(path):
    counter = 1
    original_path = path
    
    
    while path.exists():

        path = original_path.with_name(f"{original_path.stem}_{counter}{original_path.suffix}")
        counter += 1
        
    return path

def mover(source, destiantion):
   if os.path.exists(destiantion):
      path = Path(destiantion)

      new_destination = get_unique_path(path)

      shutil.move(source, new_destination)
   else:
      shutil.move(source, destiantion)
      



def cleaner(File_list,folder_names,DRY_MODE):
   for file in File_list:
       for key, values in folder_names.items():
          extension = os.path.splitext(file)[1]
          for ext in values:
             if extension == ext:
                if os.path.exists(key):
                   if DRY_MODE:
                      print(f'[DRY MODE] Move {os.path.split(file)[1]} --> {key}/{os.path.split(file)[1]} ')
                   else:
                      file_path = Path(file)
                      source = file_path
                      destination = file_path.parent/key/file_path.name
                      mover(source, destination)
                else:
                   if DRY_MODE:
                      print(f'[DRY MODE]Create Folder {key}')
                      print(f'[DRY MODE] Move {os.path.split(file)[1]} --> {key}/{os.path.split(file)[1]}')
                      
                   else:
                      file_path = Path(file)
                      folder = file_path.parent/key
                      source = file_path
                      destination = file_path.parent/key/file_path.name

                      folder.mkdir(parents=True, exist_ok=True)
                      mover(source, destination)


   
folder_names = {
    
    "PDF_Files": [".pdf"],
    "Word_Documents": [".doc", ".docx"],
    "Text_Files": [".txt", ".md"],
    "Presentations": [".ppt", ".pptx"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],

    
    "Images_JPEG": [".jpg", ".jpeg"],
    "Images_PNG": [".png"],
    "Images_SVG": [".svg"],
    "Images_GIF": [".gif"],
    "Images_WEBP": [".webp"],
    "Images_RAW": [".raw", ".nef", ".cr2"],

    
    "Code_Python": [".py"],
    "Code_JavaScript": [".js"],
    "Code_HTML": [".html"],
    "Code_CSS": [".css"],
    "Code_C_CPP": [".c", ".cpp", ".h"],
    "Code_Java": [".java"],
    "Code_Go": [".go"],
    "Code_Rust": [".rs"],
    "Code_SQL": [".sql"],
    "Code_Shell": [".sh"],

    
    "Data_JSON": [".json"],
    "Data_YAML": [".yml", ".yaml"],
    "Data_XML": [".xml"],
    "Config_Files": [".ini", ".cfg", ".conf"],
    "Log_Files": [".log"],

    
    "Video_MP4": [".mp4"],
    "Video_MKV": [".mkv"],
    "Video_MOV": [".mov"],
    "Audio_MP3": [".mp3"],
    "Audio_WAV": [".wav"],
    "Audio_FLAC": [".flac"],

    
    "Archives_ZIP": [".zip"],
    "Archives_RAR": [".rar"],
    "Archives_7Z": [".7z"],
    "Archives_TAR": [".tar"],
    "Archives_GZ": [".gz"],

    
    "Executables_EXE": [".exe"],
    "Installers_DMG": [".dmg"],
    "Installers_PKG": [".pkg"],
    "Installers_MSI": [".msi"],

    
    "Fonts_TTF": [".ttf"],
    "Fonts_OTF": [".otf"],

    
    "No_Extension": [""]
}

print("Input the directory u want to clean")
#DIR = input("> ")
DIR = '/Users/bereket/Desktop/Try/'
Exists = False
if os.path.exists(DIR):
    print(f'The Folder {DIR} exists')
    Exists = True
else:
    print(f'The Folder {DIR} doesn\'t exist')


if Exists:
    path = Path(DIR)

    File_list = []

    for file in path.iterdir():
       if file.is_file():
         File_list.append(file)

    print(f'I found {len(File_list)} unorganized files in this folder')  
    for i in File_list:
      print(f'file -- {i}')

cleaner(File_list, folder_names, DRY_MODE=True)

y = input("Do you want to continue(y/n): ")

if y.capitalize() == 'Y':
   cleaner(File_list,folder_names,DRY_MODE=False)
   print(f"{len(File_list)} files succesfully cleaned")
else:
   print("Cleaning Stopped")











    
                
                      
                   







   