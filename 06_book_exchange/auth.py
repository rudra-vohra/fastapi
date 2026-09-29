from fastapi import Header, HTTPException

API_KEY = "my_secret_api_key"


def verify_api_key(x_api_key: str = Header()):
    '''Verify the request's API key against the expected value.'''
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key


