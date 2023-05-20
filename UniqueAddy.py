import json
import requests

def get_stake_address(cardano_address):
    api_key = "blockfrost_project_id"
    base_url = "https://cardano-mainnet.blockfrost.io/api/v0"
    address_endpoint = f"{base_url}/addresses/{cardano_address}"

    headers = {
        "project_id": api_key
    }

    try:
        response = requests.get(address_endpoint, headers=headers)
        response.raise_for_status()
        data = json.loads(response.text)
        stake_address = data["stake_address"]
        return stake_address
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        return None


with open('addresses.json', 'r') as f:
    addresses = json.load(f)


stake_address_counts = {}

for address in addresses:
    cardano_address = address['address']
    stake_address = get_stake_address(cardano_address)
    if stake_address:
        if stake_address not in stake_address_counts:
            stake_address_counts[stake_address] = {
                "address": cardano_address,
                "count": 1
            }
        else:
            stake_address_counts[stake_address]["count"] += 1


unique_stake_addresses = list(stake_address_counts.values())


with open('uAddress.json', 'w') as f:
    json.dump(unique_stake_addresses, f, indent=2)

print("JSON file with address, stake address, and count created successfully.")
