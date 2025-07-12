import os
from google.genai import types

def get_files_info(working_directory, directory=None):
  """Function for AI. It will return all directories and files in directory (which must be inside working_directory), its names, file size and if it is file or directory.
  It's best practice to limit access for AI - here it's working_directory and if not target_dir.startswith() condition. 

  Args:
      working_directory (string): Directory to which AI has access - this limitation is a must hava, so AI doesn't have access to all or confidential data
      directory (string, optional): Directory to look. Defaults to None.

  Returns:
      string: file_name, file size and boole if directory (or file)
  """
  abs_working_dir = os.path.abspath(working_directory)
  target_dir = abs_working_dir
    
  if directory:
    target_dir = os.path.abspath(os.path.join(working_directory, directory))
  
  if not target_dir.startswith(abs_working_dir):
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
  if not os.path.isdir(target_dir):
    return f'Error: "{directory}" is not a directory'
    
  try:
    files_info = []
    for filename in os.listdir(target_dir):
      filepath = os.path.join(target_dir, filename)
      file_size = 0
      is_dir = os.path.isdir(filepath)
      file_size = os.path.getsize(filepath)
      files_info.append(
        f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
      )
    return "\n".join(files_info)
  
  except Exception as e:
    return f"Error listing files: {e}"
  
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
