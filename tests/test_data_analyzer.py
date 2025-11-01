from pipeline.data_analyzer import Analyzer
import pandas as pd
import pytest


data = pd.DataFrame([
    {"user_name": "alice", "price": 10, "quantity": 2, "revenue": 20},
    {"user_name": "bob", "price": 15, "quantity": 1, "revenue": 15},
    {"user_name": "alice", "price": 20, "quantity": 1, "revenue": 20}
])


@pytest.fixture
def analyzer():
    return Analyzer(data)


def test_total_revenue_per_seller(analyzer):
    total_rev_per_seller = analyzer.total_revenue_per_seller()
    
    assert isinstance(total_rev_per_seller, pd.DataFrame)
    assert ["user_name", "total_revenue"] == list(total_rev_per_seller.columns)
    
    # We Check that revenues are correctly summed
    expected_revenues = {"alice": 40, "bob": 15}
    for _, row in total_rev_per_seller.iterrows():
        assert row["total_revenue"] == expected_revenues[row["user_name"]]

    # Check descending sort order (alice first since 40 > 15)
    assert list(total_rev_per_seller["user_name"]) == ["alice", "bob"]


def test_total_products_per_seller(analyzer):
    total_prod_per_seller = analyzer.total_products_per_seller()
    
    assert isinstance(total_prod_per_seller, pd.DataFrame)
    assert ["user_name", "number_of_products_sold"] == list(total_prod_per_seller.columns)
    
    expected_qnty_sold = {"alice": 3, "bob": 1}
    
    for _, row in total_prod_per_seller.iterrows():
        assert row["number_of_products_sold"] == expected_qnty_sold[row["user_name"]]
        

def test_average_products_price_per_seller(analyzer):
    avg_price_per_seller = analyzer.average_products_price_per_seller()
    
    assert isinstance(avg_price_per_seller, pd.DataFrame)
    assert ["user_name", "average_price_per_seller"] == list(avg_price_per_seller.columns)
    
    expected_avg_price_per_seller = {"alice": 15, "bob": 15}
    
    
    for _, row in avg_price_per_seller.iterrows():
        assert row["average_price_per_seller"] == expected_avg_price_per_seller[row["user_name"]]
        
        
def test_perform_analysis(analyzer):
    merged_df = analyzer.perform_analysis()
    
    assert isinstance(merged_df, dict)
    assert list(merged_df.keys()) == ["user_name", "total_revenue", "number_of_products_sold", "average_price_per_seller"]
    
    