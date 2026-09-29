from fastapi import FastAPI
from data import pincode_db
from models import BulkRequest,BulkResponse,LocationResponse
from exceptions import pincode_not_found,InvalidPincode,PincodeNotFound,invalid_pincode


app = FastAPI(
    title="Pincode lookup API",
    description=(
        "Looks up for Indian pincode and autofills the city and state"
    )
)

app.add_exception_handler(PincodeNotFound,pincode_not_found)
app.add_exception_handler(InvalidPincode,invalid_pincode)


@app.get('/',tags=['system'])
def root():
    return {
        'message':"Server is up and running"
    }

@app.get('/pincode/{code}',response_model=LocationResponse,tags=['pincode lookup'])
def lookup(code : str):
    if len(code) != 6 or not code.isdigit():
        raise InvalidPincode(code,"Pincode should be exactly 6 digits")
    if code not in pincode_db:
        raise PincodeNotFound(code)
    return pincode_db[code]


@app.post('/pincode/bulk',response_model=BulkResponse,tags=['pincode lookup'])
def bulk_lookup(request: BulkRequest):
    results = []
    missing = []

    for code in request.pincodes:
        if code not in pincode_db:
            missing.append(code)
        else: 
            results.append(pincode_db[code])

    return BulkResponse(
        found=len(results),not_found=len(missing),locations=results,missing=missing
    )



