# m3DataConversion

## Overview

m3DataConversion is a set of reusable and customizable scripts designed to help migrate data from the **Dancik Flooring System** to **Infor M3 CloudSuite Distribution Enterprise**. The project automates data extraction, transformation, and loading (ETL) processes to streamline the conversion effort.

## Features

- Extracts data from Dancik Flooring System (AS400-based ERP).
- Transforms data to match Infor M3 CloudSuite requirements.
- Loads transformed data into M3 CloudSuite using predefined templates.
- Provides reusable helper modules for database interactions, Excel handling, and configuration management.

## Project Structure

```
├── config/                     # Configuration files
│   ├── config.ini              # Main configuration file
│   ├── config.ini.example      # Example configuration file
│
├── queries/                    # SQL query files for data extraction
│   ├── active_items.sql
│   ├── crs025.sql
│   ├── dancik_rolls.sql
│   └── ...
│
├── templates/                  # Excel templates for API data loading
│   ├── API_CRS025MI_AddItemGroup.xlsx
│   ├── API_CRS035MI_AddProductGroup.xlsx
│   └── ...
│
├── transformers/               # Data transformation scripts
│   ├── crs025_transformer.py
│   ├── crs035_transformer.py
│   ├── mms200_transformer.py
│   └── ...
│
├── dancik/                     # Modules for processing Dancik system data
│   ├── dancik_rolls.py
│   ├── dancik_uom.py
│   └── ...
│
├── m3/                         # Modules for interacting with M3 CloudSuite
│   ├── item_number_lookup.py
│   ├── mms015_converter.py
│   └── ...
│
├── m3Models/                   # M3 CloudSuite data models
│   ├── MMS200_Types.py
│   ├── mms015_type1_entry.py
│   └── ...
│
├── main scripts                # Data processing scripts
│   ├── 000_as400_build_active_items_spreadsheet.py
│   ├── 010_load_items_to_db.py
│   ├── 100_export_priceclass_as_crs025.py
│   └── ...
│
├── config_reader.py            # Configuration file reader
├── database.py                 # Database interaction module
├── excel_helper.py             # Helper for Excel file handling
├── path_manager.py             # File path manager
├── plugin_manager.py           # Plugin-based execution framework
│
├── requirements.txt            # Required Python dependencies
└── README.md                   # Project documentation
```

## Installation

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd m3DataConversion
   ```
2. **Create a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Configuration

- Modify `config/config.ini` with database connection details, file paths, and system-specific settings.
- An example configuration file (`config.ini.example`) is provided.

## Usage

Run individual scripts to perform specific tasks, such as:

```sh
python 000__build_active_items_spreadsheet.py
python 010_load_items_to_db.py
```

## Contributing

If you'd like to contribute, feel free to submit a pull request or open an issue.

## License

This software, **m3DataConversion**, is a personal project developed and owned by [Your Name]. It is **licensed and not sold**. The software is provided exclusively to a specific list of authorized companies approved by the author.

- **Authorized Companies:** Only companies explicitly approved by the author may use, modify, and deploy this software for internal operations.
- **No Redistribution:** Redistribution, sublicensing, or public sharing of this software, in whole or in part, **is strictly prohibited** without prior written consent from the author.
- **No Unauthorized Commercial Use:** The software **may not** be used for any commercial purposes outside of authorized organizations.
- **Modification for Internal Use:** Authorized companies may modify the software **only for internal purposes** but **cannot** distribute modifications to external parties.

For full license details or to request authorization, please contact the author directly.

## Contact

For inquiries, please contact the project maintainers.

