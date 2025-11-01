from pipeline.data_enricher import DataEnricher
import pandas as pd


def test_convert_products_to_df_returns_df():
    mock_products_data = [{
        "id": 1,
        "category": "mens-clothing",
        "price": 29.99,
        "rating": {"rate": 4.5, "count": 100}
    }]
    
    enricher = DataEnricher(mock_products_data, users_data = [])
    mock_products_df = enricher._convert_products_to_df()
    
    assert isinstance(mock_products_df, pd.DataFrame)
    assert list(mock_products_df.columns) == ["id", "category", "price", "quantity", "rating"]
    assert mock_products_df.loc[0, "id"] == mock_products_data[0]["id"]
    assert mock_products_df.loc[0, "quantity"] == mock_products_data[0]["rating"]["count"]
    assert mock_products_df.loc[0, "rating"] == mock_products_data[0]["rating"]["rate"]
    assert len(mock_products_df) == 1
    

def test_convert_products_to_df_missing_keys_returns_none():
    mock_products_data = [{
        "id": 1,
        "category": "mens-clothing",
        "price": 29.99
    }]
    
    enricher = DataEnricher(mock_products_data, users_data = [])
    mock_products_df = enricher._convert_products_to_df()
    

    assert mock_products_df.loc[0, "id"] == mock_products_data[0]["id"]
    assert mock_products_df.loc[0, "quantity"] == None
    assert mock_products_df.loc[0, "rating"] == None
    
# Next we test _convert_users_to_df
def test_convert_users_to_df_returns_df():
    mock_users_data = [{
        "id": 1,
        "email": "john@gmail.com",
        "username": "johnd",
        "password": "m38rmF$",
        "name": {
            "firstname": "john",
            "lastname": "doe"}
    }]
    
    enricher = DataEnricher(products_data = [], users_data = mock_users_data)
    mock_users_df = enricher._convert_users_to_df()
    
    assert isinstance(mock_users_df, pd.DataFrame)
    assert list(mock_users_df.columns) == ["id", "email", "user_name", "first_name", "last_name"]
    assert mock_users_df.loc[0, "id"] == mock_users_data[0]["id"]
    assert mock_users_df.loc[0, "email"] == mock_users_data[0]["email"]
    assert mock_users_df.loc[0, "user_name"] == mock_users_data[0]["username"]
    assert mock_users_df.loc[0, "first_name"] == mock_users_data[0]["name"]["firstname"]
    assert mock_users_df.loc[0, "last_name"] == mock_users_data[0]["name"]["lastname"]
    assert len(mock_users_df) == 1
    

def test_convert_users_to_df_missing_keys_returns_none():
    mock_users_data = [{
        "id": 1,
        "rating": 2
    }]
    
    enricher = DataEnricher(products_data= [], users_data = mock_users_data)
    mock_users_df = enricher._convert_users_to_df()
    
    assert list(mock_users_df.columns) == ["id", "email", "user_name", "first_name", "last_name"]
    assert mock_users_df.loc[0, "id"] == mock_users_data[0]["id"]
    assert mock_users_df.loc[0, "email"] == None
    assert mock_users_df.loc[0, "user_name"] == None
    assert mock_users_df.loc[0, "first_name"] == None
    assert mock_users_df.loc[0, "last_name"] == None


# Next we test for _join_data
def test_join_data_performs_left_merge_correctly():

    mock_products_data = [
        {"id": 1, "category": "electronics", "price": 100, "rating": {"rate": 4.5, "count": 10}},
        {"id": 2, "category": "clothing", "price": 50, "rating": {"rate": 4.0, "count": 5}}
    ]

    mock_users_data = [
        {"id": 1, "email": "user1@mail.com", "username": "user1", "name": {"firstname": "John", "lastname": "Doe"}}
    ]

    enricher = DataEnricher(mock_products_data, mock_users_data)
    
    result_df = enricher._join_data()
    
    # Assert
    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) == 2 
    assert "email" in result_df.columns
    assert result_df.loc[result_df["id"] == 1, "email"].iloc[0] == "user1@mail.com"
    assert pd.isna(result_df.loc[result_df["id"] == 2, "email"]).iloc[0]


def test_enrich_data_creates_revenue_column_correctly():

    mock_products_data = [
        {"id": 1, "category": "electronics", "price": 100, "rating": {"rate": 4.5, "count": 10}},
        {"id": 2, "category": "clothing", "price": 50, "rating": {"rate": 4.0, "count": 5}}
    ]
    mock_users_data = [
        {"id": 1, "email": "user1@mail.com", "username": "user1", "name": {"firstname": "John", "lastname": "Doe"}}
    ]

    enricher = DataEnricher(mock_products_data, mock_users_data)
    enriched_df = enricher.enrich_data()

    assert isinstance(enriched_df, pd.DataFrame)
    assert "revenue" in enriched_df.columns
    assert len(enriched_df) == 2

    expected_revenue_product_1 = 100 * 10  # price * quantity
    expected_revenue_product_2 = 50 * 5
    assert enriched_df.loc[enriched_df["id"] == 1, "revenue"].iloc[0] == expected_revenue_product_1
    assert enriched_df.loc[enriched_df["id"] == 2, "revenue"].iloc[0] == expected_revenue_product_2

    # Confirm unmatched users still appear (id=2 should have NaN user fields)
    assert pd.isna(enriched_df.loc[enriched_df["id"] == 2, "email"]).iloc[0]
