# GoHighLevel Bulk Setup Scripts

This folder contains Python scripts for automating GoHighLevel configuration across multiple locations.

## Scripts

### `create_ghl_custom_fields.py`
Batch creates custom fields (dropdowns, multi-select, text fields) for contact data capture.

**Use for:**
- Primary Service selection
- Additional Services checkboxes
- Lead source tracking
- Project categorization

### `create_ghl_custom_values.py`
Batch creates custom values (reusable data snippets) for use in workflows and templates.

**Use for:**
- Support phone numbers
- Booking calendar links
- Standard pricing
- Brand colors and assets
- Legal text snippets

## Quick Start

1. **Install Python 3.7+**
   ```bash
   python --version
   ```

2. **Install required package**
   ```bash
   pip install requests
   ```

3. **Configure scripts**
   - Add your Private Integration token
   - Add your Location IDs
   - Customize fields/values as needed

4. **Run scripts**
   ```bash
   python create_ghl_custom_fields.py
   python create_ghl_custom_values.py
   ```

## Documentation

For complete documentation, see: [Bulk Custom Fields Setup Guide](/integrations/gohighlevel-bulk-setup)

## Security

⚠️ **Never commit your API tokens to version control!**

Consider using environment variables:
```python
import os
ACCESS_TOKEN = os.getenv("GHL_API_TOKEN")
```

## Support

For issues or questions, refer to:
- [GoHighLevel API Documentation](https://highlevel.stoplight.io/)
- [Main Integration Guide](/integrations/gohighlevel)
