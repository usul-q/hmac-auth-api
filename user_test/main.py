import os
from dotenv import load_dotenv
import signature

dotenv_path = os.path.join(os.path.dirname(__file__), 'api_key.env')
load_dotenv(dotenv_path=dotenv_path)

private_key = os.getenv('PRIVATE_KEY')

if not private_key:
    raise ValueError('PRIVATE_KEY not set in environment variables')

generated_signature = signature.generate_signature(private_key)

print(generated_signature)