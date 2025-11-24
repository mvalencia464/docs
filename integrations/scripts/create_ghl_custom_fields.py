import requests
import time

# -------------------------------------------------------------------
# 1. API Configuration
# -------------------------------------------------------------------
# Replace these with your actual values
ACCESS_TOKEN = "pit-99e89478-392e-4803-a62b-598ea490cf24"
LOCATION_IDS = [
    "wnfQfg2IIyeI7768WeGf",
    # Add more location IDs here as needed
]

BASE_URL_TEMPLATE = "https://services.leadconnectorhq.com/locations/{location_id}/customFields"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Version": "2021-07-28",
    "Content-Type": "application/json"
}

def create_custom_fields():
    """
    Batch create Custom Fields in GoHighLevel (GHL) for multiple locations.
    """
    
    # -------------------------------------------------------------------
    # 3. Special Instruction for Standard Fields
    # -------------------------------------------------------------------
    # NOTE: Property Address, Email, and Phone must be mapped to GHL system fields 
    # (contact.email, contact.phone, contact.address1) during the contact creation process.
    # We do NOT create custom fields for these.

    for location_id in LOCATION_IDS:
        print(f"Processing Location ID: {location_id}")
        url = BASE_URL_TEMPLATE.format(location_id=location_id)

        # -------------------------------------------------------------------
        # 2. Field Requirements (JSON Payloads)
        # -------------------------------------------------------------------

        # Field A: "Primary Service"
        primary_service_payload = {
            "name": "Primary Service",
            "dataType": "SINGLE_OPTIONS",
            "options": [
                "Christmas Lights",
                "Mowing",
                "Cleanups",
                "Summer Maintenance",
                "Winter Services"
            ]
        }

        # Field B: "Additional Services"
        additional_services_payload = {
            "name": "Additional Services",
            "dataType": "MULTIPLE_OPTIONS",
            "options": [
                "Spring Cleanup",
                "Weekly Mowing",
                "Fertilizer Program",
                "Weed Control",
                "Fall Cleanup",
                "Debris Removal",
                "Snow Plowing (Starts at $55)",
                "Plow Driveway",
                "Walkway Clearing",
                "Sanding (Starts at $85)",
                "Ice Control",
                "Roofline Lighting",
                "Tree Wrapping",
                "Wreaths & Garland",
                "Removal & Storage",
                "Timer/Automation"
            ]
        }

        fields_to_create = [primary_service_payload, additional_services_payload]

        for field in fields_to_create:
            try:
                print(f"  Creating field: {field['name']}...")
                response = requests.post(url, headers=HEADERS, json=field)
                
                # Check for HTTP errors
                response.raise_for_status()
                
                print(f"  [SUCCESS] Created field '{field['name']}': {response.json()}")
                
            except requests.exceptions.RequestException as e:
                print(f"  [ERROR] Failed to create field '{field['name']}': {e}")
                if 'response' in locals() and response is not None:
                     print(f"  Response content: {response.text}")

            # Handle Rate Limiting: Sleep 0.5s between requests
            time.sleep(0.5)

if __name__ == "__main__":
    create_custom_fields()
