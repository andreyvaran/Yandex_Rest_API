from typing import List

from pydantic import BaseModel, validator


class CourierSchema(BaseModel):
    courier_id: int
    courier_type: str
    regions: List[int]
    working_hours: List[str]

    @validator('working_hours')
    def check_time(cls, value):
        for time in value:
            if len(time) !=11:
                raise ValueError('ERROR: wrong time format')
            else:
                st = time.split('-')[0]
                ft = time.split('-')[1]
                if st < ft:
                    continue

                else:
                    raise ValueError('ERROR: wrong time format')
        return value
class CompleteOrderSchema(BaseModel):
    order_id: int
    courier_id: int
    complete_time : str

class OrderSchema(BaseModel):
    order_id: int
    weight: float
    region: int
    delivery_hours: List[str]

    @validator('delivery_hours')
    def check_time(cls, value):
        for time in value:
            if len(time) !=11:
                raise ValueError('ERROR: wrong time format')
            else:
                st = time.split('-')[0]
                ft = time.split('-')[1]
                if st < ft:
                    continue

                else:
                    raise ValueError('ERROR: wrong time format')
        return value