from fastapi import Request
from fastapi.responses import JSONResponse

class PincodeNotFound(Exception):
    def __init__(self, pincode:str):
        self.pincode = pincode
        
class InvalidPincode(Exception):
    def __init__(self, pincode:str,reason:str):
        self.pincode = pincode
        self.reason = reason


# Custom Exception Handlers
def pincode_not_found(request:Request,exception:PincodeNotFound):
    return JSONResponse(
        status_code=404,
        content={
            'error':"Pincode not found",
            "message":f"Location not found for pincode {exception.pincode}",
            "pincode":exception.pincode
        }
    )

def invalid_pincode(request:Request,exception:InvalidPincode):
    return JSONResponse(
        status_code=400,
        content={
            'error':"Invalid Pincode",
            "message":f"Pincode {exception.pincode} is invalid: {exception.reason}",
            "pincode":exception.pincode
        }
    )

