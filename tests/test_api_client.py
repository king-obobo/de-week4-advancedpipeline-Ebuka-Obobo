from pipeline.api_client import APIClient
import pytest
from unittest.mock import patch, Mock
import requests

# We start with the _paginate data as it is the easiest
@pytest.mark.parametrize(
    "data, limit",
    [
        ([{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}], 3), # Data > limit
        ([{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}],10), #Data < limit
        ([{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}], 2), #Data is not divisible by Limit
        ([], 10) #Data is empty
    ]
)
def test_paginate_various_data_cases(data, limit):
    client = APIClient.__new__(APIClient)
    result = client._paginate(data, limit)
    
    assert result == data
    
@pytest.mark.parametrize("invalid_limit", [0, -1, None, "ten"])
def test_paginate_with_invalid_limits(invalid_limit):
    data = [{"id": 1}, {"id": 2}, {"id": 3}]
    client = APIClient.__new__(APIClient)
    
    with pytest.raises((ValueError, TypeError)):
        client._paginate(data, invalid_limit)
    
    
# We buid a fake config manager class and save our settings
class FakeConfigManager:
    def __init__(self):
        self.setting = {"API": {"base_url": "https://fake.api"}, "PAGINATION": {"limit": "10"}}
        
    def get(self, section, key):
        return self.setting[section][key]
    
    def settings(self):
        return self.setting


def test_api_client_initialization_with_fake_config():
    fake_config = FakeConfigManager()
    APIClient.CONFIGMANAGER = FakeConfigManager()
    client = APIClient()
    
    assert client.base_url == fake_config.get("API", "base_url")
    assert client.limit == int(fake_config.get("PAGINATION", "limit"))
    assert client.get_config_settings == fake_config.settings()
    

# Testing the get_all_products method    
@patch("pipeline.api_client.requests.get")
def test_get_all_products_returns_paginated_data(mock_get):
    fake_response = Mock()
    fake_response.json.return_value = [
        { "id": 1,
            "title": "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops",
            "price": 109.95,
            "description": "Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in the padded sleeve, your everyday",
            "category": "men's clothing",
            "image": "https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_t.png",
            "rating": {
            "rate": 3.9,
            "count": 120}
        }]
    fake_response.raise_for_status.return_value = None
    mock_get.return_value = fake_response
    
    APIClient.CONFIGMANAGER = FakeConfigManager()
    client = APIClient()
    
    result = client.get_all_products()
    
    mock_get.assert_called_once_with(f"{client.base_url}/products")
    
    assert result == [
        {   "id": 1,
            "title": "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops",
            "price": 109.95,
            "description": "Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in the padded sleeve, your everyday",
            "category": "men's clothing",
            "image": "https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_t.png",
            "rating": {
            "rate": 3.9,
            "count": 120}
        }]

# Testing the get_all_products method error
@patch("pipeline.api_client.requests.get")
def test_get_all_products_request_exception(mock_get, capsys):
    # fake_response = Mock()
    mock_get.side_effect = requests.exceptions.RequestException("Network Failure")
    
    APIClient.CONFIGMANAGER = FakeConfigManager()
    client = APIClient()
    
    result = client.get_all_products()
    readout = capsys.readouterr()
    
    assert result == None
    assert "An error occurred here:" in readout.out
    
# Testing the get_all_users method
@patch("pipeline.api_client.requests.get")
def test_get_all_users_returns_data(mock_get):
    fake_response = Mock()
    fake_response.json.return_value = [
        {
            "address": {
            "geolocation": {"lat": "-37.3159", "long": "81.1496"},
            "city": "kilcoole",
            "street": "new road",
            "number": 7682,
            "zipcode": "12926-3874"
                        },
            "id": 1,
            "email": "john@gmail.com",
            "username": "johnd",
            "password": "m38rmF$",
            "name": {
            "firstname": "john",
            "lastname": "doe"
                    },
            "phone": "1-570-236-7033",
            "__v": 0
        }]
    fake_response.raise_for_status.return_value = None
    mock_get.return_value = fake_response
    
    APIClient.CONFIGMANAGER = FakeConfigManager()
    client = APIClient()
    
    result = client.get_all_users()
    
    mock_get.assert_called_once_with(f"{client.base_url}/users")
    assert result == [
        {
            "address": {
            "geolocation": {"lat": "-37.3159", "long": "81.1496"},
            "city": "kilcoole",
            "street": "new road",
            "number": 7682,
            "zipcode": "12926-3874"
                        },
            "id": 1,
            "email": "john@gmail.com",
            "username": "johnd",
            "password": "m38rmF$",
            "name": {
            "firstname": "john",
            "lastname": "doe"
                    },
            "phone": "1-570-236-7033",
            "__v": 0
        }
    ]
    
@patch("pipeline.api_client.requests.get")
def test_get_all_users_exception(mock_get, capsys):
    mock_get.side_effect = requests.exceptions.RequestException("Network failure")
    
    APIClient.CONFIGMANAGER = FakeConfigManager()
    client = APIClient()
    
    result = client.get_all_users()
    readout = capsys.readouterr()
    
    assert result == None
    assert "An error occured here:" in readout.out