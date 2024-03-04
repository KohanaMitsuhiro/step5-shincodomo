from sqlalchemy import Column, ForeignKey, Integer,VARCHAR,DATE
from .database import Base


# SQLデータベース内のテーブル定義

# 部門キャパシティテーブル
class DivisionCapacity(Base):
    __tablename__ = "division_capacity"

    Capacity_id = Column(VARCHAR(10), primary_key=True)
    division_id = Column(VARCHAR(10), unique=True)
    capacity_hours = Column(Integer)

# Productステータステーブル
class ProductStatus(Base):
    __tablename__ = "product"

    product_id = Column(Integer,primary_key=True)
    status = Column(VARCHAR(10))
    end_day = Column(DATE)
    update_day = Column(DATE)


# ===実績系統======================================================================================
class ResultsManHours(Base):
    __tablename__ = "results_man-hours"

    results_id = Column(VARCHAR(10), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.product_id"), unique=True)
    cavity_number = Column(Integer)
    sekkei = Column(Integer)
    seizou1 = Column(Integer)
    seizou2 = Column(Integer)
    seizou3 = Column(Integer)
    seizou4 = Column(Integer)
    kumitate = Column(Integer)
    start_day = Column(DATE)
    end_day = Column(DATE)


class ResultsGraphData(Base):
    __tablename__ = "results_graph"

    results_Graph_id = Column(VARCHAR(10), primary_key=True)
    results_id = Column(VARCHAR(10))
    product_id = Column(Integer, ForeignKey("product.product_id"), unique=True)
    cavity_number = Column(Integer)
    date = Column(DATE)
    division_id = Column(VARCHAR(10))
    man_hours = Column(Integer)


# ===見積り系統======================================================================================
class QuoteManHours(Base):
    __tablename__ = "quote_man-hours"

    quote_id = Column(VARCHAR(10), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.product_id"), unique=True)
    cavity_number = Column(Integer)
    sekkei = Column(Integer)
    seizou1 = Column(Integer)
    seizou2 = Column(Integer)
    seizou3 = Column(Integer)
    seizou4 = Column(Integer)
    kumitate = Column(Integer)
    start_day = Column(DATE)
    end_day = Column(DATE)


class QuoteGraphData(Base):
    __tablename__ = "quote_graph"

    quote_Graph_id = Column(VARCHAR(10), primary_key=True)
    quote_id = Column(VARCHAR(10))
    product_id = Column(Integer, ForeignKey("product.product_id"), unique=True)
    cavity_number = Column(Integer)
    date = Column(DATE)
    division_id = Column(VARCHAR(10))
    man_hours = Column(Integer)


# ===予測系統======================================================================================
class PredictionManHours(Base):
    __tablename__ = "Prediction_man-hours"

    Prediction_id = Column(VARCHAR(10), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.product_id"), unique=True)
    cavity_number = Column(Integer)
    sekkei = Column(Integer)
    seizou1 = Column(Integer)
    seizou2 = Column(Integer)
    seizou3 = Column(Integer)
    seizou4 = Column(Integer)
    kumitate = Column(Integer)
    start_day = Column(DATE)
    end_day = Column(DATE)


class PredictionGraphData(Base):
    __tablename__ = "prediction_graph"

    prediction_Graph_id = Column(VARCHAR(10), primary_key=True)
    prediction_id = Column(VARCHAR(10))
    product_id = Column(Integer, ForeignKey("product.product_id"), unique=True)
    cavity_number = Column(Integer)
    date = Column(DATE)
    division_id = Column(VARCHAR(10))
    man_hours = Column(Integer)

