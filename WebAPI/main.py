from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session
from sql_app import schemas, models,crud
from sql_app.database import db_session, engine


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
