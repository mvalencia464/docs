# GoHighLevel Bulk Setup Scripts

This folder contains Python and Node.js scripts for automating GoHighLevel configuration and deployment.

## Scripts

### `deploy_ghl_email_template.js` (Node.js)
**New!** A robust script for deploying email templates that uses a "2-Step Upsert" method (Create Shell -> Patch Content) to ensure HTML content is saved correctly.

**Use for:**
- Creating new email templates
- Updating existing templates without duplication
- Managing email copy as code

**Usage:**
```bash
# 1. Duplicate template
cp deploy_ghl_email_template.js deploy-my-new-offer.js

# 2. Edit content in new file
# ...

# 3. Run
node deploy-my-new-offer.js
```

### `create_ghl_custom_fields.py` (Python)
Batch creates custom fields (dropdowns, multi-select, text fields) for contact data capture.

**Use for:**
- Primary Service selection
- Additional Services checkboxes
- Lead source tracking
- Project categorization

### `create_ghl_custom_values.py` (Python)
Batch creates custom values (reusable data snippets) for use in workflows and templates.

**Use for:**
- Support phone numbers
- Booking calendar links
- Standard pricing
- Brand colors and assets
- Legal text snippets

## Quick Start

### Python Scripts
1. **Install Python 3.7+**
2. **Install requests:** `pip install requests`
3. **Configure & Run:** `python create_ghl_custom_fields.py`

### Node.js Scripts
1. **Install Node.js 14+**
2. **Configure & Run:** `node deploy_ghl_email_template.js`

## Documentation

- **Email Deployment SOP:** [Read the full guide](./email-deployment.md)
- **Bulk Setup:** [Bulk Custom Fields Setup Guide](/integrations/gohighlevel-bulk-setup)

## Security

⚠️ **Never commit your API tokens to version control!**

Consider using environment variables:
```python
import os
ACCESS_TOKEN = os.getenv("GHL_API_TOKEN")
```
