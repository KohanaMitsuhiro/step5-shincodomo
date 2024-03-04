from sqlalchemy.orm import Session,joinedload
from . import models, schemas


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



# 部門名から限界時間の取得
def get_division_capacity(db:Session,id:str):
    return db.query(models.DivisionCapacity).filter(models.DivisionCapacity.division_id==id).first()

# 部門名から限界時間の取得
def get_division_capacity_all(db:Session):
    return db.query(models.DivisionCapacity).all()
