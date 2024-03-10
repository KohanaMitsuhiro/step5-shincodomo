from sqlalchemy.orm import Session
from sqlalchemy import func,Integer
from sqlalchemy.sql.expression import cast

from fastapi.encoders import jsonable_encoder
from . import models, schemas



# ===グラフ用データ=================================================================================
def get_Graph_data(db: Session,date_range:schemas.DateRange):

    # ===実績(基本的には空で返ってくるはず。)=========================================================
    # 日付範囲とステータス"Done"を満たすレコードを結合して取得
    resultsdata = db.query(models.ResultsGraphData).join(models.ProductStatus).filter(
        models.ProductStatus.status == "Done",
        models.ResultsGraphData.date >= date_range.start_date,
        models.ResultsGraphData.date <= date_range.end_date
    ).all()
    # 取得したデータを辞書に変換し、"status": "Done"を各辞書に追加
    resultsLIST= []
    for data in resultsdata:
        data_dict = {**data.__dict__}
        data_dict.pop("_sa_instance_state", None)  # SQLAlchemyインスタンスの状態情報を削除
        data_dict['status'] = 'Done'  # 'status'キーを追加
        resultsLIST.append(data_dict)

    # ===見積り====================================================================================
    # 日付範囲とステータス"Quote"を満たすレコードを結合して取得
    quotedata = db.query(models.QuoteGraphData).join(models.ProductStatus).filter(
        models.ProductStatus.status == "Quote",
        models.QuoteGraphData.date >= date_range.start_date,
        models.QuoteGraphData.date <= date_range.end_date
    ).all()
    # 取得したデータを辞書に変換し、"status": "Quote"を各辞書に追加
    quoteLIST= []
    for data in quotedata:
        data_dict = {**data.__dict__}
        data_dict.pop("_sa_instance_state", None)  # SQLAlchemyインスタンスの状態情報を削除
        data_dict['status'] = 'Quote'  # 'status'キーを追加
        quoteLIST.append(data_dict)

    # ===予測======================================================================================
    # 日付範囲とステータス"Predict"を満たすレコードを結合して取得
    predictiondata = db.query(models.PredictionGraphData).join(models.ProductStatus).filter(
        models.ProductStatus.status == "Predict",
        models.PredictionGraphData.date >= date_range.start_date,
        models.PredictionGraphData.date <= date_range.end_date
    ).all()
    # 取得したデータを辞書に変換し、"status": "Predict"を各辞書に追加
    predictionLIST= []
    for data in predictiondata:
        data_dict = {**data.__dict__}
        data_dict.pop("_sa_instance_state", None)  # SQLAlchemyインスタンスの状態情報を削除
        data_dict['status'] = 'Predict'  # 'status'キーを追加
        predictionLIST.append(data_dict)

    # 取得データの統合
    GraphDataList=[]
    GraphDataList.extend(resultsLIST)
    GraphDataList.extend(quoteLIST)
    GraphDataList.extend(predictionLIST)

    # JSON応答として適切にシリアライズ
    json_compatible_GraphDataList = jsonable_encoder(GraphDataList)
    return json_compatible_GraphDataList


# ===実績系統======================================================================================
# 工事番号(product_id)から実績番号の取得
def get_results_by_id(db: Session, id: int):
    return db.query(models.ResultsManHours).filter(models.ResultsManHours.product_id == id).first()

# 実績取得
def get_results_data(db: Session,date_range:schemas.DateRange):
    return db.query(models.ResultsManHours).filter(
        models.ResultsManHours.end_day >= date_range.start_date,
        models.ResultsManHours.end_day <= date_range.end_date    
    ).all()

# グラフ作成用の実績取得
def get_results_Graph_data(db: Session,date_range:schemas.DateRange):

    # 日付範囲とステータス"Done"を満たすレコードを結合して取得
    return db.query(models.ResultsGraphData).join(models.ProductStatus).filter(
        models.ProductStatus.status == "Done",
        models.ResultsGraphData.date >= date_range.start_date,
        models.ResultsGraphData.date <= date_range.end_date
    ).all()


# ===見積り系統======================================================================================
# 工事番号(product_id)から見積り番号の取得
def get_quote_by_id(db: Session, id: int):
    return db.query(models.QuoteManHours).filter(models.QuoteManHours.product_id == id).first()

# 見積り取得
def get_quote_data(db: Session,date_range:schemas.DateRange):
    return db.query(models.QuoteManHours).filter(
        models.QuoteManHours.end_day >= date_range.start_date,
        models.QuoteManHours.end_day <= date_range.end_date    
    ).all()

# グラフ作成用の見積り取得
def get_quote_Graph_data(db: Session,date_range:schemas.DateRange):

    # 日付範囲とステータス"Quote"を満たすレコードを結合して取得
    return db.query(models.QuoteGraphData).join(models.ProductStatus).filter(
        models.ProductStatus.status == "Quote",
        models.QuoteGraphData.date >= date_range.start_date,
        models.QuoteGraphData.date <= date_range.end_date
    ).all()


# ===予測系統======================================================================================
# 工事番号(product_id)から予測番号の取得
def get_prediction_by_id(db: Session, id: int):
    return db.query(models.PredictionManHours).filter(models.PredictionManHours.product_id == id).first()

# 予測取得
def get_prediction_data(db: Session,date_range:schemas.DateRange):
    return db.query(models.PredictionManHours).filter(
        models.PredictionManHours.end_day >= date_range.start_date,
        models.PredictionManHours.end_day <= date_range.end_date    
    ).all()

# グラフ作成用の予測取得
def get_prediction_Graph_data(db: Session,date_range:schemas.DateRange):

    # 日付範囲とステータス"Quote"を満たすレコードを結合して取得
    return db.query(models.PredictionGraphData).join(models.ProductStatus).filter(
        models.ProductStatus.status == "Predict",
        models.PredictionGraphData.date >= date_range.start_date,
        models.PredictionGraphData.date <= date_range.end_date
    ).all()

# IDの一番大きなものを取得する
def get_max_predid(db:Session):
    # 予測ID(PRE01025)の数値部分を取り出し、最大値を取得するクエリ
    maxid = db.query(func.max(cast(func.substr(models.PredictionManHours.Prediction_id,4),Integer))).scalar()    
    return maxid

# product_idの一番大きなモノを取得する
def get_max_productid(db:Session):
    # 最大値を取得するクエリ
    maxid = db.query(func.max(models.PredictionManHours.product_id)).scalar()    
    return maxid

# 受け取ったデータを予測DBに書き込む
def create_prediction_data(db: Session,writeData:schemas.PredictionManHours):
    db.add(writeData)
    db.commit()
    db.refresh(writeData)


# 部門名から限界時間の取得
def get_division_capacity(db:Session,id:str):
    return db.query(models.DivisionCapacity).filter(models.DivisionCapacity.division_id==id).first()

# 部門名から限界時間の取得
def get_division_capacity_all(db:Session):
    return db.query(models.DivisionCapacity).all()
