from flask import Flask
from router import create_app
import pytest
import json


# TEST VARIABLES
# Product
product_id = 1
product_name = "Test"
product_descript = "Test description."

# general
content_type = 'API/json'
headers = {"Content-Type": content_type}
code_ok = 200
code_not_found = 404
redirect_code = 308

# UPDATE VARIABLES
update_name = "Test Product (updated)"
update_descript = "I was created from pytest (updated)."

# ROUTE URLS
BASE_URL = '/product'
product_id_url = BASE_URL + '/' + str(product_id)  # /product/<product_id>
product_offers_url = '/offer/' + BASE_URL + str(product_id)  # /offer/product/<product_id>


# JSON REQUEST TEST SAMPLES
json_req_product_data = {
                            "name": product_name,
                            "description": product_descript
                        }

json_req_update_product = {
                            "name": update_name,
                            "description": update_descript
                          }

# JSON RESPONSE TEST SAMPLES
json_res_get = {
                    "description": product_descript,
                    "id": product_id,
                    "name": product_name
                }

json_res_update = {
                        "description": update_descript,
                        "id": product_id,
                        "name": update_name
}


json_res_delete = {
                        "code": code_ok,
                        "msg": "Item deleted."
                  }

json_res_not_found = {
                        "status": "ERROR",
                        "code": 404,
                        "msg": "Not found"
                    }


# SUPPORT FUCNTIONS
def json_of_response(response):
    """
    Decode json from response
    """
    return json.loads(response.data)


# TESTS
@pytest.fixture
def client():
    app = Flask(__name__)
    create_app(app)
    client = app.test_client()
    yield client


def test_add_product(client):
    """
    Tests adding product to the database.
    """
    response = client.post(BASE_URL, data=json.dumps(json_req_product_data), headers=headers)
    assert response.content_type == content_type
    assert response.status_code == code_ok


def test_get_products(client):
    """
    Tests getting products from the database.
    """
    response = client.get(BASE_URL)
    assert response.status_code == code_ok or response.status_code == code_not_found
    assert response.content_type == content_type


def test_get_product(client):
    """
    Tests getting one product from the database.
    """
    response = client.get(product_id_url)
    assert response.status_code == code_ok or response.status_code == code_not_found
    assert response.content_type == content_type
    assert json_of_response(response) == json_res_get or json_of_response(response) == json_res_not_found


def test_get_product_offers(client):
    """
    Tests getting offers for specific product from the database.
    """
    response = client.get(product_offers_url)
    assert response.status_code == redirect_code or response.status_code == code_not_found
    assert response.content_type == content_type


def test_update_product(client):
    """
    Tests updating specific product.
    """
    response = client.put(product_id_url, data=json.dumps(json_req_update_product), headers=headers)
    assert response.status_code == code_ok or response.status_code == code_not_found
    assert response.content_type == content_type
    assert json_of_response(response) == json_res_update or json_of_response(response) == json_res_not_found


def test_delete_product(client):
    """
    Tests deleting specific product from the database.
    """
    response = client.delete(product_id_url)
    assert response.status_code == code_ok
    assert response.content_type == content_type
    assert json_of_response(response) == json_res_delete or json_of_response(response) == json_res_not_found
