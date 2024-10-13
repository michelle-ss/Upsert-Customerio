# Customer.io Sync Tool

A Python script to synchronize user data with Customer.io using a specified configuration and data files. The script identifies (upserts) users in Customer.io based on the provided mappings and handles retries in case of network errors.

## Features

- Load configuration and data from JSON files.
- Map user attributes based on a defined schema.
- Upsert user data to Customer.io with retry logic for network errors.
- Parallel processing of user upsert requests for improved performance.

## Requirements

- Python 3.6+
- `requests` library
- `customerio` library (installable via pip)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>

2. Install the required packages:
    ```bash
    pip install requests customerio

## Usage
### Configuration File
Create a JSON configuration file (e.g., config.json) with the following structure:

    ```json
    {
        "site-id": "your_site_id",
        "api-key": "your_api_key",
        "userId": "user_id_field_name",
        "parallelism": 25,
        "mappings": [
            {
                "from": "computed_ltv",
                "to": "ltv"
            },
            {
                "from": "name",
                "to": "name"
            }
        ]
    }
    ```

### Data File
Create a JSON data file (e.g., data.json) containing the user data you want to sync, structured as an array of user objects:

```json
[
    {
        "user_id_field_name": "123",
        "name": "John Doe",
        "revenue": 100
    },
    {
        "user_id_field_name": "456",
        "name": "Jane Smith",
        "revenue": 150
    }
]
```

### Running the Script
To run the script, use the following command:

```bash
python3 upsert_to_customer_io.py -c path/to/config.json -d path/to/data.json
```
### Example
Assuming you have the configuration file as config.json and the data file as data.json, run:

```bash
python3 upsert_to_customer_io.py -c config.json -d data.json
```
### Error Handling
The script includes error handling for network-related issues during the API calls. In case of a connection timeout, it will retry the request with exponential backoff. Any other errors will be logged with a message indicating the user that caused the error.
