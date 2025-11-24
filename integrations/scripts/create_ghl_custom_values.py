import requests
import time

# -------------------------------------------------------------------
# 1. API Configuration
# -------------------------------------------------------------------
# Credentials reused from previous task
ACCESS_TOKEN = "pit-99e89478-392e-4803-a62b-598ea490cf24"
LOCATION_IDS = [
    "wnfQfg2IIyeI7768WeGf",
    # Add more location IDs here as needed
]

BASE_URL_TEMPLATE = "https://services.leadconnectorhq.com/locations/{location_id}/customValues"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Version": "2021-07-28",
    "Content-Type": "application/json"
}

def create_custom_values():
    """
    Batch create Custom Values in GoHighLevel (GHL) for multiple locations.
    Includes duplicate prevention logic.
    """

    for location_id in LOCATION_IDS:
        print(f"Processing Location ID: {location_id}")
        url = BASE_URL_TEMPLATE.format(location_id=location_id)

        # -------------------------------------------------------------------
        # 3. Crucial Logic (Duplicate Prevention)
        # -------------------------------------------------------------------
        # First, GET existing custom values to check for duplicates
        existing_values = {}
        try:
            print("  Fetching existing custom values...")
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            
            # Map existing names to their IDs (or just mark as existing)
            if 'customValues' in data:
                for cv in data['customValues']:
                    existing_values[cv['name']] = cv
            
            print(f"  Found {len(existing_values)} existing custom values.")
            
        except requests.exceptions.RequestException as e:
            print(f"  [ERROR] Failed to fetch existing values: {e}")
            if 'response' in locals() and response is not None:
                 print(f"  Response content: {response.text}")
            continue # Skip to next location if we can't check duplicates

        # -------------------------------------------------------------------
        # 2. Custom Values List (JSON Payload)
        # -------------------------------------------------------------------
        values_to_create = [
            {
                "name": "Support Phone",
                "value": "(555) 123-4567"
            },
            {
                "name": "Booking Link",
                "value": "https://api.leadconnectorhq.com/widget/booking/FC66XdrRY6pXKeh3N4AI"
            },
            {
                "name": "Base Price - Mowing",
                "value": "$50"
            },
            {
                "name": "Base Price - Plowing",
                "value": "$75"
            },
            {
                "name": "Brand Color Primary",
                "value": "#10B981"
            }
        ]

        for cv in values_to_create:
            name = cv['name']
            
            if name in existing_values:
                print(f"  Skipped: '{name}' already exists.")
                continue

            try:
                print(f"  Creating value: '{name}'...")
                response = requests.post(url, headers=HEADERS, json=cv)
                
                # Check for HTTP errors
                response.raise_for_status()
                
                print(f"  [SUCCESS] Created value '{name}': {response.json()}")
                
            except requests.exceptions.RequestException as e:
                print(f"  [ERROR] Failed to create value '{name}': {e}")
                if 'response' in locals() and response is not None:
                     print(f"  Response content: {response.text}")

            # -------------------------------------------------------------------
            # 4. Rate Limiting
            # -------------------------------------------------------------------
            time.sleep(0.5)

if __name__ == "__main__":
    create_custom_values()
