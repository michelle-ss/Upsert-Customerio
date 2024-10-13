# 
# Take Home exercise
# Michelle Song
# Oct 13, 2024
# michellesong0102@gmail.com
# 
 
import argparse
import json
import requests
import time
import concurrent.futures

from customerio import CustomerIO, Regions


def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)


def load_data(data_file):
    with open(data_file, 'r') as f:
        return json.load(f)


def map_user_attributes(user_attributes, user, mappings, user_id):

    for mapping in mappings:
        source_field = mapping['from']
        target_field = mapping['to']

        if source_field in user and source_field != user_id:
            user_attributes[target_field] = user_attributes.pop(source_field)


def send_user_data(config, user):
    cio = CustomerIO(config["site-id"], config["api-key"], region=Regions.US)
    user_id = config['userId']
    retries = 3

    if user_id in user:
        user_attributes = {key: value for key,
                           value in user.items() if key != user_id}
        map_user_attributes(user_attributes, user, config['mappings'], user_id)

        for attempt in range(retries):
            try:
                cio.identify(id=user[user_id], **user_attributes, update=True)
                print(f"User {user[user_id]} upserted successfully")
                break
            except requests.exceptions.ConnectTimeout as e:
                print(
                    f"Network error occurred while upserting user {user_id}: {e}")
                if attempt < retries - 1:
                    time.sleep(2)  # Wait before retrying
            except Exception as e:
                print(
                    f"An error occurred while upserting user {user[user_id]}: {e}")
                break
    else:
        print("User ID not found! Please ensure data contains a unique ID for each user.")
        return None


def upsert_user(config, data):
    # Makes API requests in paralell, as defined by the configuration file
    with concurrent.futures.ThreadPoolExecutor(max_workers=config['parallelism']) as executor:
        executor.map(lambda user: send_user_data(config, user), data)


def main():
    # Set up argument parsing from CLI
    parser = argparse.ArgumentParser(
        description='Sync Customer.io with given data files.')
    parser.add_argument('-c', '--config_file', required=True,
                        help='Path to the configuration file')
    parser.add_argument('-d', '--data_file', required=True,
                        help='Path to the data file')

    args = parser.parse_args()

    config_file = args.config_file
    data_file = args.data_file

    config = load_config(config_file)
    data = load_data(data_file)

    upsert_user(config, data)


if __name__ == "__main__":
    main()
