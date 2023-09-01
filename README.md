# Tenant query understanding and response generation API

This project contains a Flask API for generating tenant information and response based on dialogue history.

## How to use

### Install Dependencies

First, make sure you have Python and the required dependencies installed.

```bash
pip install -r requirements.txt

### Run Flask App

```bash
nohup python flask_api.py


## API Endpoint

URL: /generate_tenant_data

Method: POST

Response Format: JSON

```bash
curl -X POST \
  http://your-api-host/generate_tenant_data \
  -H 'Content-Type: application/json' \
  -d '{
    "dialogue_history": "Tenant Q: Can I book a viewing for the property at 56 Mortimer road tomorrow at 3pm?\nAgent: OK, let me check some information first. Do you intend to rent a property with your kids?\nTenant Q: yes\nAgent: Do you keep any pets\nTenant: Yes, we have a dog."
  }'
```bash

## Response Example

The API will return a JSON response containing generated tenant information data.

```bash
{
  "intent": {
    "address": "56 Mortimer Road",
    "guarantor": null,
    "monthly_rent": "asked",
    "family_friend": "asked",
    "max_tenants number": "asked",
    "minimum_tenancy number?": "asked",
    "pet_friend": "asked",
    "bills": null
  },
  "sql": "SELECT * FROM properties WHERE address = '56 Mortimer Road' AND family_friend = 1 AND pet_friend = 1",
  "db_result": "The property at 56 Mortimer Road is ready for rent. Up to 2 tenants are allowed. Minimum tenancy period is 12 months. Your pet is allowed.",
  "generated_reply": "Based on our records, the property at 56 Mortimer Road is ready for rent. Your pet is allowed. Please feel free to contact us for more details. Thank you!"
}
```bash

