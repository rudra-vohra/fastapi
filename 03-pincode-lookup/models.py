from typing import List
from pydantic import BaseModel,field_validator


class PincodeRequest(BaseModel):
    pincode:int

    @field_validator('pincode')
    @classmethod
    def check(cls,value):
        if len(value) != 6 or not value.isdigit():
            raise ValueError('Pincode must be exactly 6 digits')
        return value

class LocationResponse(BaseModel):
    pincode:str
    city:str
    state:str
    district:str


class BulkRequest(BaseModel):
    pincodes: List[str]

    @field_validator('pincodes')
    @classmethod
    def check(cls,values):
        if len(values) == 0:
            raise ValueError('Atleast one pincode required per request')
        if len(values) > 20:
            raise ValueError('Only 20 pincodes allowed per request')

        for code in values:
            if len(code) != 6 or not code.isdigit():
                raise ValueError('Pincode must be exactly 6 digits')

        return values   

class BulkResponse(BaseModel):
    status:str = 'success'
    found:int
    not_found:int
    locations:List[LocationResponse]
    missing: List[str]

