from typing import Union
from pydantic import BaseModel,Field
from datetime import date


# pydanticでのモデル定義

# 期間指定用のリクエストモデルの定義
class DateRange(BaseModel):
    start_date: date = Field(...,examples=["2023-03-12"])
    end_date: date = Field(...,examples=["2023-04-12"])

# # stlモデル受取用モデル
# class STLMode(BaseModel):
#     end_date:date = Field(...,examples="2023-04-12")
#     STL-model:UploadFile

class DivisionCapacityModel(BaseModel):
    Capacity_id: str
    division_id: str
    capacity_hours: int

    class Config:
        # orm_mode = True
        from_attributes = True

class QuoteBase(BaseModel):
    pass


class QuoteCreate(QuoteBase):
    pass


class Quote(QuoteBase):
    quote_id : str
    product_id :int
    cavity_number :int 
    sekkei : int
    seizou1 : int
    seizou2 : int
    seizou3 : int
    seizou4 : int
    kumitate : int
    start_day : date
    end_day :date

    class Config:
        orm_mode = True
        from_attributes = True


class PredictBase(BaseModel):

    cavity_number :int 
    sekkei : int
    seizou1 : int
    seizou2 : int
    seizou3 : int
    seizou4 : int
    kumitate : int
    start_day : date
    end_day :date


    pass


class PredictCreate(PredictBase):
    
    pass


class PredictionManHours(PredictBase):
    Prediction_id : str
    product_id : int
    class Config:
        orm_mode = True
        from_attributes = True