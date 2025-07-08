import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
  file_path_rel = os.path.join(working_directory, file_path)
  file_path_abs = os.path.abspath(file_path_rel)

  if not file_path_abs.startswith(os.path.abspath(working_directory)):
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.isfile(file_path_abs):
    return f'Error: File not found or is not a regular file: "{file_path}"'
  
  try:
    with open(file_path_abs) as file:
      file_content = file.read(MAX_CHARS)
      if len(file_content) >= 10000:
        return file_content + f'[...File "{file_path}" truncated at 10000 characters]'
      return file_content

  except Exception as e:
    return f'Error: {e}'
  


