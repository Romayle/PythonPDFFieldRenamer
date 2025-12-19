# How to set up the Project

1. Run `python -m venv pdfenv` on a Powershell or CMD terminal.
2. Run `.\pdfenv\Scripts\Activate.ps1` to start the virtual environment
3. Run `pip install -r requirements.txt` to install all the dependencies mentioned in the requirements.txt file. (make sure that these dependencies are installed once your venv is running).

# Purpose of each file

1. inspect_fields.py
   To log all the input fields in the PDF.

2. generate_mapping.py
   To generate the new field names and see a log of the comparision between the old and new field names.
   (Format logged - "old_field_name" : "new_field_name")

3. rename_fields.py
   Renames the input fields in the PDF to a match it's description.

4. verify_rename.py
   Logs the new input field names (limited only up to 10 fields for the moment). 

# To Start the application

1. Run this in a powershell terminal (starts the virtual environment) - `.\pdfenv\Scripts\Activate.ps1`

2. To run any file enter - `python file_name`

3. To stop the programme run - `deactivate`
