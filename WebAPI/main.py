from fastapi import FastAPI, Depends,File, UploadFile
from typing import Any
import shutil
import tempfile

from sqlalchemy.orm import Session
from sql_app import schemas, models,crud
from sql_app.database import db_session, engine

from stl import mesh
import os
from joblib import load
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from joblib import load
from xgboost import XGBRegressor
from datetime import datetime, timedelta
import pandas as pd
import json
import math

app = FastAPI()

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.get("/test")
# def fastAPI_test( db: Session = Depends(get_db)):
#     append_id = f"PRE0{crud.get_max_predid(db=db)+1}"
#     append_proid = crud.get_max_productid(db=db)+1
#     return {"id":append_id,"proid":append_proid}

# ===グラフ表示用データ=============================================================================    
@app.post("/GraphData/")
async def get_Graph_data(date_range: schemas.DateRange,db: Session = Depends(get_db)):
    return crud.get_Graph_data(db=db,date_range=date_range)


# ===実績系統======================================================================================
# 工事番号から実績データを取得
@app.get("/results/{id}")
async def get_results_by_id(id:int, db: Session = Depends(get_db)):
    return crud.get_results_by_id(db=db, id=id)

# 実績データを取得。ＰＯＳＴで開始日と終了日を貰って、その期間を返す。
@app.post("/results")
async def get_results_all(date_range: schemas.DateRange,db: Session = Depends(get_db)):
    return crud.get_results_data(db=db,date_range=date_range)


# グラフ加工用実績データの取得。ＰＯＳＴで開始日と終了日を貰って、その期間を返す。
@app.post("/results_Graph/")
async def get_results_Graph_data(date_range: schemas.DateRange,db: Session = Depends(get_db)):
    return crud.get_results_Graph_data(db=db,date_range=date_range)


# ===見積り系統======================================================================================
# 工事番号から見積りデータを取得
@app.get("/quote/{id}")
async def get_quote_by_id(id:int, db: Session = Depends(get_db)):
    return crud.get_quote_by_id(db=db, id=id)

# 見積りデータを取得
@app.post("/quote")
async def get_quote_data(date_range: schemas.DateRange,db: Session = Depends(get_db)):
    return crud.get_quote_data(db=db,date_range=date_range)


# グラフ加工用見積りデータの取得。ＰＯＳＴで開始日と終了日を貰って、その期間を返す。
@app.post("/quote_Graph/")
async def get_quote_Graph_data(date_range: schemas.DateRange,db: Session = Depends(get_db)):
    return crud.get_quote_Graph_data(db=db,date_range=date_range)


# ===予測系統======================================================================================
# 工事番号から予測データを取得
@app.get("/prediction/{id}")
async def get_prediction_by_id(id:int, db: Session = Depends(get_db)):
    return crud.get_prediction_by_id(db=db, id=id)

# 予測データを取得。ＰＯＳＴで開始日と終了日を貰って、その期間を返す。
@app.post("/prediction")
async def get_prediction_data(date_range: schemas.DateRange,db: Session = Depends(get_db)):
    return crud.get_prediction_data(db=db,date_range=date_range)


# グラフ加工用予測データの取得。ＰＯＳＴで開始日と終了日を貰って、その期間を返す。
@app.post("/prediction_Graph/")
async def get_prediction_Graph_data(date_range: schemas.DateRange,db: Session = Depends(get_db)):
    return crud.get_prediction_Graph_data(db=db,date_range=date_range)


# 受注確定の予測データをDBに書き込む
@app.post("/writeData")
async def get_max_predid(writedata:schemas.PredictBase,db: Session = Depends(get_db)):
    append_id = f"PRE0{crud.get_max_predid(db=db)+1}"
    append_proid = crud.get_max_productid(db=db)+1
    append_data = models.PredictionManHours(Prediction_id=append_id,
                                  product_id=append_proid,
                                  cavity_number=writedata.cavity_number,
                                  sekkei=writedata.sekkei,
                                  seizou1=writedata.seizou1,
                                  seizou2=writedata.seizou2,
                                  seizou3=writedata.seizou3,
                                  seizou4=writedata.seizou4,
                                  kumitate=writedata.kumitate,
                                  start_day=writedata.start_day,
                                  end_day=writedata.end_day)
    
    crud.create_prediction_data(db=db,writeData=append_data)

    return {"staus":"OK"}


# STLを受け取り予測結果を返信する
@app.post("/stlmodel/{end_day}")
async def calc_prediction(end_day:str, upload_file: UploadFile = File(...), db: Session = Depends(get_db)) -> Any:
# async def calc_prediction(end_day:str, db: Session = Depends(get_db)):
     # suffixは保存するファイルの拡張子を指定（今回は".stl"を指定）
    with tempfile.NamedTemporaryFile(delete=False, dir=".", suffix=".stl") as temp_file:
        shutil.copyfileobj(upload_file.file, temp_file)
        temp_file_path = temp_file.name  # 一時ファイルのパスを保存


    # STLファイルの読み込み
    model_mesh = mesh.Mesh.from_file(temp_file_path)
    # ボリュームと表面積を計算
    volume = model_mesh.get_mass_properties()[0]
    Sarea = model_mesh.areas.sum()

    # 一時ファイルを削除
    # 注: Windowsでは、numpy-stlがファイルをロックするため、
    # from_fileを使用した後にファイルを削除する場合、
    # 明示的にファイルを閉じる必要があります。
    # このステップはLinuxでは不要かもしれませんが、クロスプラットフォームのコードを書く場合は注意が必要です。
    os.remove(temp_file_path)

    return DummyData

    # ===グラフ用データの作成 ==============================================================================
    # end_day_date = datetime.strptime(end_day, '%Y%m%d').date()

    # ===表面積は上手く出せていない為、固定値を返すようにする。==========================
    PredictionModelData = {}
    PredictionModelData["calc_Graph_id"] = "STLModel_id"
    PredictionModelData["product_id"] = 999999
    PredictionModelData["cavity_number"] = 1
    PredictionModelData["sekkei"] = 671
    PredictionModelData["seizou1"] = 499
    PredictionModelData["seizou2"] = 1652
    PredictionModelData["seizou3"] = 304
    PredictionModelData["seizou4"] = 485
    PredictionModelData["kumitate"] = 284
    PredictionModelData["end_day"] = end_day
    # ===============================================================================

    # return calculate_previous_monday(end_day_date)

    # 解析結果を返す
    return  calc_Graph_Data(PredictionModelData,db).to_json(orient='records')
    # return  calc_Graph_Data(PredictionModelData,db)


def calc_Graph_Data(dict_data,db):
    # 部門キャパの読込み
    division_capa_table = crud.get_division_capacity_all(db=db)
    division_capa = {}
    # 各項目をループして新しい辞書に変換
    for item in division_capa_table:
        division_id = item.division_id
        capacity_hours = item.capacity_hours
        division_capa[division_id] = capacity_hours

    # 
    df_ALLData = pd.DataFrame(dict_data,index=[0])

    # Unixタイムスタンプをdatetimeオブジェクトに変換
    df_ALLData['end_day'] = pd.to_datetime(df_ALLData['end_day'])
    df_ALLData['end_week'] = df_ALLData['end_day'].apply(calculate_previous_monday)

    columsList = ["calc_Graph_id","product_id","cavity_number","date","division_id","man-hours"]
    df_Graph_data = pd.DataFrame(columns=columsList)

    for index, row in df_ALLData.iterrows():
        product_id = row["product_id"]

        # 掛かる週数の算出
        week_cnt = {}
        week_cnt["product_id"] = product_id
        week_cnt["sekkei"] = math.ceil(row["sekkei"]/division_capa["sekkei"])
        week_cnt["seizou1"] = math.ceil(row["seizou1"]/division_capa["seizou1"])
        week_cnt["seizou2"] = math.ceil(row["seizou2"]/division_capa["seizou2"])
        week_cnt["seizou3"] = math.ceil(row["seizou3"]/division_capa["seizou3"])
        week_cnt["seizou4"] = math.ceil(row["seizou4"]/division_capa["seizou4"])
        week_cnt["kumitate"] = math.ceil(row["kumitate"]/division_capa["kumitate"])
        week_cnt["MAX_seizou_cnt"] = max(week_cnt["seizou1"],week_cnt["seizou2"],week_cnt["seizou3"],week_cnt["seizou4"])

        df_week_cnt = pd.DataFrame(week_cnt,index=[0])

        # 一週間の稼働時間の算出
        week_hours = {}
        week_hours["product_id"] = product_id
        week_hours["sekkei"] = math.ceil(row["sekkei"]/week_cnt["sekkei"])
        week_hours["seizou1"] = math.ceil(row["seizou1"]/week_cnt["seizou1"])
        week_hours["seizou2"] = math.ceil(row["seizou2"]/week_cnt["seizou2"])
        week_hours["seizou3"] = math.ceil(row["seizou3"]/week_cnt["seizou3"])
        week_hours["seizou4"] = math.ceil(row["seizou4"]/week_cnt["seizou4"])
        week_hours["kumitate"] = math.ceil(row["kumitate"]/week_cnt["kumitate"])

        df_week_hours = pd.DataFrame(week_hours,index=[0])


        # 組立     
        endweek = df_ALLData[df_ALLData["product_id"]==product_id]["end_week"].item()
        for n in range(df_week_cnt[df_week_cnt["product_id"]==product_id]["kumitate"].item()):
            oldestweek=endweek - timedelta(weeks=1*n)
            NEW_row = {"calc_Graph_id":df_ALLData[df_ALLData["product_id"]==product_id]["calc_Graph_id"].item(),
                    "product_id":product_id,
                    "cavity_number":df_ALLData[df_ALLData["product_id"]==product_id]["cavity_number"].item(),
                    "date":oldestweek,
                    "division_id":"kumitate",
                    "man-hours":df_week_hours[df_week_hours["product_id"]==product_id]["kumitate"].item()}

            df_Graph_data = pd.concat([df_Graph_data, pd.DataFrame([NEW_row])], ignore_index=True)

        maxweek=week_cnt["MAX_seizou_cnt"]
    
        # 製造   
        seizou_startweek = oldestweek - timedelta(weeks=1*maxweek)
        for n in range(df_ALLData[df_ALLData["product_id"]==product_id]["seizou1"].item()):
            oldestweek=seizou_startweek + timedelta(weeks=1*n)
            NEW_row = {"calc_Graph_id":df_ALLData[df_ALLData["product_id"]==product_id]["calc_Graph_id"].item(),
                    "product_id":product_id,
                    "cavity_number":df_ALLData[df_ALLData["product_id"]==product_id]["cavity_number"].item(),
                    "date":oldestweek,
                    "division_id":"seizou1",
                    "man-hours":df_week_hours[df_week_hours["product_id"]==product_id]["seizou1"].item()}

            df_Graph_data = pd.concat([df_Graph_data, pd.DataFrame([NEW_row])], ignore_index=True)
            
        for n in range(df_ALLData[df_ALLData["product_id"]==product_id]["seizou2"].item()):
            oldestweek=seizou_startweek + timedelta(weeks=1*n)
            NEW_row = {"calc_Graph_id":df_ALLData[df_ALLData["product_id"]==product_id]["calc_Graph_id"].item(),
                    "product_id":product_id,
                    "cavity_number":df_ALLData[df_ALLData["product_id"]==product_id]["cavity_number"].item(),
                    "date":oldestweek,
                    "division_id":"seizou2",
                    "man-hours":df_week_hours[df_week_hours["product_id"]==product_id]["seizou2"].item()}

            df_Graph_data = pd.concat([df_Graph_data, pd.DataFrame([NEW_row])], ignore_index=True)       
        
        
        for n in range(df_ALLData[df_ALLData["product_id"]==product_id]["seizou3"].item()):
            oldestweek=seizou_startweek + timedelta(weeks=1*n)
            NEW_row = {"calc_Graph_id":df_ALLData[df_ALLData["product_id"]==product_id]["calc_Graph_id"].item(),
                    "product_id":product_id,
                    "cavity_number":df_ALLData[df_ALLData["product_id"]==product_id]["cavity_number"].item(),
                    "date":oldestweek,
                    "division_id":"seizou3",
                    "man-hours":df_week_hours[df_week_hours["product_id"]==product_id]["seizou3"].item()}

            df_Graph_data = pd.concat([df_Graph_data, pd.DataFrame([NEW_row])], ignore_index=True)
            
        for n in range(df_ALLData[df_ALLData["product_id"]==product_id]["seizou4"].item()):
            oldestweek=seizou_startweek + timedelta(weeks=1*n)
            NEW_row = {"calc_Graph_id":df_ALLData[df_ALLData["product_id"]==product_id]["calc_Graph_id"].item(),
                    "product_id":product_id,
                    "cavity_number":df_ALLData[df_ALLData["product_id"]==product_id]["cavity_number"].item(),
                    "date":oldestweek,
                    "division_id":"seizou4",
                    "man-hours":df_week_hours[df_week_hours["product_id"]==product_id]["seizou4"].item()}

            df_Graph_data = pd.concat([df_Graph_data, pd.DataFrame([NEW_row])], ignore_index=True)
            
        # 製造    
        sekkei_startweek = seizou_startweek - timedelta(weeks=1)
        for n in range(df_ALLData[df_ALLData["product_id"]==product_id]["sekkei"].item()):
            oldestweek=sekkei_startweek - timedelta(weeks=1*n)
            NEW_row = {"calc_Graph_id":df_ALLData[df_ALLData["product_id"]==product_id]["calc_Graph_id"].item(),
                    "product_id":product_id,
                    "cavity_number":df_ALLData[df_ALLData["product_id"]==product_id]["cavity_number"].item(),
                    "date":oldestweek,
                    "division_id":"sekkei",
                    "man-hours":df_week_hours[df_week_hours["product_id"]==product_id]["sekkei"].item()}

            df_Graph_data = pd.concat([df_Graph_data, pd.DataFrame([NEW_row])], ignore_index=True)

        # df_Graph_data["end_day"] = df_Graph_data["end_day"].dt.strftime('%Y-%m-%d')
        df_Graph_data["date"] = df_Graph_data["date"].dt.strftime('%Y-%m-%d')

    return df_Graph_data


# 前の週の月曜日を計算し、新しい列に追加する関数
def calculate_previous_monday(date):
    # その週の月曜日を取得
    week_start = date - pd.Timedelta(days=date.weekday())
    # 前の週の月曜日を計算
    previous_monday = week_start - pd.Timedelta(weeks=1)
    return previous_monday


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app,host="127.0.0.1",port=8000)






DummyData=[
    {"cavity_number":1,"date":"2024/8/5","division_id":"kumitate","man-hours":95},
    {"cavity_number":1,"date":"2024/7/29","division_id":"kumitate","man-hours":95},
    {"cavity_number":1,"date":"2024/7/22","division_id":"kumitate","man-hours":95},
    {"cavity_number":1,"date":"2024/7/15","division_id":"seizou1","man-hours":100},
    {"cavity_number":1,"date":"2024/7/8","division_id":"seizou1","man-hours":100},
    {"cavity_number":1,"date":"2024/7/1","division_id":"seizou1","man-hours":100},
    {"cavity_number":1,"date":"2024/6/24","division_id":"seizou1","man-hours":100},
    {"cavity_number":1,"date":"2024/6/17","division_id":"seizou1","man-hours":100},
    {"cavity_number":1,"date":"2024/7/15","division_id":"seizou2","man-hours":331},
    {"cavity_number":1,"date":"2024/7/8","division_id":"seizou2","man-hours":331},
    {"cavity_number":1,"date":"2024/7/1","division_id":"seizou2","man-hours":331},
    {"cavity_number":1,"date":"2024/6/24","division_id":"seizou2","man-hours":331},
    {"cavity_number":1,"date":"2024/6/17","division_id":"seizou2","man-hours":331},
    {"cavity_number":1,"date":"2024/6/24","division_id":"seizou3","man-hours":152},
    {"cavity_number":1,"date":"2024/6/17","division_id":"seizou3","man-hours":152},
    {"cavity_number":1,"date":"2024/7/1","division_id":"seizou4","man-hours":162},
    {"cavity_number":1,"date":"2024/6/24","division_id":"seizou4","man-hours":162},
    {"cavity_number":1,"date":"2024/6/17","division_id":"seizou4","man-hours":162},
    {"cavity_number":1,"date":"2024/6/10","division_id":"sekkei","man-hours":48},
    {"cavity_number":1,"date":"2024/6/3","division_id":"sekkei","man-hours":48},
    {"cavity_number":1,"date":"2024/5/27","division_id":"sekkei","man-hours":48},
    {"cavity_number":1,"date":"2024/5/20","division_id":"sekkei","man-hours":48},
    {"cavity_number":1,"date":"2024/5/13","division_id":"sekkei","man-hours":48},
    {"cavity_number":1,"date":"2024/5/6","division_id":"sekkei","man-hours":48},
    {"cavity_number":1,"date":"2024/4/29","division_id":"sekkei","man-hours":48},
    {"cavity_number":1,"date":"2024/4/22","division_id":"sekkei","man-hours":48},
    {"cavity_number":1,"date":"2024/4/15","division_id":"sekkei","man-hours":48},
    {"cavity_number":1,"date":"2024/4/8","division_id":"sekkei","man-hours":48},
    {"cavity_number":1,"date":"2024/4/1","division_id":"sekkei","man-hours":48},
    {"cavity_number":1,"date":"2024/3/25","division_id":"sekkei","man-hours":48},
    {"cavity_number":1,"date":"2024/3/18","division_id":"sekkei","man-hours":48},
    {"cavity_number":1,"date":"2024/3/11","division_id":"sekkei","man-hours":48},
]			

