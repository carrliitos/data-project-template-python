from pathlib import PurePath
from utils.office365_api import SharePoint
import re
import sys
import os

def save_file(file_name, file_obj, folder_dest):
  """
  Save the file object to the specified file name.

  Args:
  - file_name (str): The name of the file to save.
  - file_obj (bytes): The file object to save.
  - folder_dest (str): The local folder destination.
  """
  file_dir_path = PurePath(folder_dest, file_name)
  with open(file_dir_path, "wb") as input_file:
    input_file.write(file_obj)

def get_file(file_name, folder, folder_dest):
  """
  Download a file from SharePoint and save it.

  Args:
  - file_name (str): The name of the file to download.
  - folder (str): The folder in SharePoint where the file is located.
  - folder_dest (str): The local folder destination.
  """
  file_obj = SharePoint().download_file(file_name, folder)
  save_file(file_name, file_obj, folder_dest)

def get_files(folder, folder_dest):
  """
  Download all files from a folder in SharePoint.

  Args:
  - folder (str): The folder in SharePoint from which to download files.
  - folder_dest (str): The local folder destination.
  """
  files_list = SharePoint()._get_files_list(folder)
  for file in files_list:
    get_file(file.name, folder, folder_dest)

def get_files_by_pattern(keyword, folder, folder_dest):
  """
  Download files from SharePoint that match a specified pattern in their name.

  Args:
  - keyword (str): The pattern to match in file names.
  - folder (str): The folder in SharePoint from which to download files.
  - folder_dest (str): The local folder destination.
  """
  files_list = SharePoint()._get_files_list(folder)
  for file in files_list:
    if re.search(keyword, file.name):
      get_file(file.name, folder, folder_dest)

def get_file_content(file_path):
  """
  Read a file and return its content.

  Args:
  - file_path (str): The path to the file to read.

  Returns:
  - bytes: The content of the file.
  """
  with open(file_path, "rb") as file_input:
    return file_input.read()

def get_list_of_files(local_folder):
  """
  Get a list of files in a local folder (excluding subfolders).

  Args:
  - local_folder (str): The path to the local folder.

  Returns:
  - list: A list of tuples containing file names and their full paths.
  """
  file_list = []
  folder_item_list = os.listdir(local_folder)
  
  for item in folder_item_list:
    item_full_path = PurePath(local_folder, item)
    if os.path.isfile(item_full_path):
      file_list.append([item, item_full_path])

  return file_list

def upload_files(local_folder, sharepoint_folder_name, keyword=None):
  """
  Upload files from a local folder to a SharePoint folder based on specified 
  criteria.

  Args:
  - local_folder (str): The path to the local folder containing the files to 
  upload.
  - sharepoint_folder_name (str): The name of the SharePoint folder to 
  upload to.
  - keyword (str): The pattern to match in file names. Use None to upload all 
  files.
  """
  files_list = get_list_of_files(local_folder)
  for file in files_list:
    if keyword is None or keyword == 'None' or re.search(keyword, file[0]):
      file_content = get_file_content(file[1])
      SharePoint().upload_file(file_name=file[0],
                               folder_name=sharepoint_folder_name,
                               content=file_content)

def download(sharepoint_site_folder_name,
             folder_dest,
             file_name,
             file_name_pattern):
  """
  Download files from SharePoint based on specified criteria.

  This function allows you to download files from a SharePoint site to a local 
  folder. You can specify the SharePoint folder name (which may include 
  subfolders), the destination folder on your local machine, and either a 
  specific file name or a pattern to match in file names.

  Usage Example: Download all Tableau workbooks that has PrEP in its name.
  ```
  download(sharepoint_site_folder_name="Tableau/Workbooks", 
       folder_dest="./data/", 
       file_name=None, 
       file_name_pattern="PrEP")
  ```

  Args:
  - sharepoint_site_folder_name (str): The SharePoint folder name. May include 
  subfolders (e.g., Tableau/Workbooks).
  - folder_dest (str): The destination folder where files will be saved.
  - file_name (str): The specific file name to download. Use None to download 
  all files.
  - file_name_pattern (str): The pattern to match in file names. Use None to 
  download all files.
  """
  if file_name:
    get_file(file_name, sharepoint_site_folder_name, folder_dest)
  elif file_name_pattern:
    get_files_by_pattern(file_name_pattern,
                         sharepoint_site_folder_name,
                         folder_dest)
  else:
    get_files(sharepoint_site_folder_name, folder_dest)

def upload(root_dir, sharepoint_folder_name, filename_pattern):
  """
  Upload files to SharePoint based on specific criteria.

  This function uploads files from a root directory to a SharePoint folder. 
  You can specify a filename pattern to upload only files that match the 
  pattern.

  Usage Example: Upload main.log to Tableau/Workbooks
  ```
  office365_sharepoint.upload(root_dir=f"{directory}/routine_daily/logs",
                sharepoint_folder_name="Tableau/Workbooks",
                filename_pattern="main.log")
  ```

  Args:
  - root_dir (str): The root directory path of the files to upload.
  - sharepoint_folder_name (str): The SharePoint folder name. May include 
  subfolders to upload to.
  - filename_pattern (str): Only upload files with a specific pattern in their name.
  """
  upload_files(root_dir, sharepoint_folder_name, filename_pattern)
