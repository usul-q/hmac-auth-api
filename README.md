=======================================
HMAC Auth Django API
=======================================

A secure Django REST API deployed on Render that includes:
- User registration (/register/)
- Login via Basic Authentication to UPDATE or DELETE (/login/) - All user fields are visible when authenticated
- All user list endpoint (/users/) - Public with limited fields
- Specific user with id list (/user/id) - Public with limited fields
- HMAC-authenticated endpoint (/user/secret/) - Requires signature verification

---------------------------------------
🚀 1. Deployment (Render)
---------------------------------------

Deployed at:
https://hmac-auth-api.onrender.com

Deployment stack:
- Django REST Framework (DRF)
- Render.com (web service)
- Gunicorn for serving

Required files for deployment:
- requirements.txt
- manage.py
- app directory with Django settings
- gunicorn in 'requirements.txt'
- Root Directory: main_project
- Build Command: pip install -r requirements.txt
- Start Command: python manage.py migrate && gunicorn main_project.wsgi:application

---------------------------------------
🧪 2. Testing with Postman
---------------------------------------

🔸 Import this Postman Collection:
👉 'HMAC Auth API.postman_collection.json'

Instructions:
1. Open Postman
2. Click “Import”
3. Upload 'HMAC Auth API.postman_collection.json' (included in this repo)
4. Explore all test cases

Included test scenarios:
- ✅ Register new users
- ✅ Login with Basic Auth
- ✅ Fetch all users
- ✅ Fetch user with specific id
- ✅ Test HMAC-auth endpoint
- ✅ Handle invalid/missing fields
- ✅ Test failed logins & bad signatures
---------------------------------------
🔐 3. Auth Instructions
---------------------------------------

- Basic Authentication:
  - Required for '/login/'

- HMAC Signature (for '/user/secret/'):
  - Include these headers:
    - 'PUBLIC-KEY': your app's public key
    - `Signature': generated using HMAC(private_key, request_body)
