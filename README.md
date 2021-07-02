# Python-3-BE-developer-task

## Requirements:
- Those can be found [there](https://github.com/bender321/Python-3-BE-developer-task/blob/main/API/requirements.txt).

## Database:
- PostgreSQL (hosting created on remote server)
- Setup is configured with all requirements in app_settings.py

## Important:
- you can change database option to which you like or just setup your own database
- if you want to install this app you have to make sure that you have clean database ready without any remaining tables

## Instalation:
- create virtual enviroment
- activate virtual enviroment
- make sure that all requirements are satisfied
- make sure that you are located in API directory
- make sure that you have database ready and correctly edited app_settings.py
- run command: ```python db_maker.py``` to make all tables in prepared database 
- run command: ```python app.py``` to run application

## Usage:
- preferably use [Postman](https://www.postman.com/) for interacting with application
- do not forget setup right Content-Type header for passing json into body of request via Postman
- code should do aswell
- in file .env is possible to change env variable which represents base URL of outer MS

### Routes:
### Any route that is not listed:
#### Response:
- NOT FOUND 404 {
  "code": 404, 
  "msg": "Invalid route", 
  "status": "Error"
}
### Products:
#### POST /product
##### Headers: 
- Content-Type: application/json
##### Request: 
- {
    "name": "Name of product",
    "description": "Description of the product"
}
##### Response:
- 200 OK {
    "code": 200,
    "msg": "Product added to the database successfully.",
    "status": "OK"
}
- 500 ERROR {
                        "status": "ERROR",
                        "code": 500,
                        "msg": "Error during registration of the product."
                    }

#### GET /product
##### Headers:
- None
##### Request:
- None
##### Response:
- 200 OK[
    {
        "description": "description of the product",
        "id": ID of the product,
        "name": "Name of the product"
    },
    {...},
    {...},
    ...
]
- 404 NOT FOUND {"status": "ERROR", "code": 404, "msg": "Not found"}
- 500 ERROR {"status": "ERROR", "code": 500, "msg": "Exeption msg which caused error"}

#### GET /product/<product_id>
##### Headers:
- None
##### Request:
- ID in path
##### Response:
- 200 OK {
    "description": "description of product",
    "id": ID of the product,
    "name": "Name of product"
}
- 500 ERROR {"status": "ERROR", "code": 500, "msg": "Exeption msg which caused error"}
- 404 NOT FOUND{"status": "ERROR", "code": 404, "msg": "Not found"}

#### PUT /product/<product_id>
##### Headers:
- Content-Type: application/json
##### Request:
- ID in path 
- {
    "name": "Updated name of the product",
    "description": "Updated description of the product"
}
##### Response:
- 200 OK {
    "description": "Updated description of the product",
    "id": ID of the product,
    "name": "Updated name of the product"
}
- 404 NOT FOUND {"status": "ERROR", "code": 404, "msg": "Not found"}
- 500 ERROR {"status": "ERROR", "code": 500, "msg": "Exeption msg which caused error"}

#### DELETE /product/<product_id>
##### Headers:
- None
##### Request:
- ID in path
##### Response:
- 200 OK {
    "code": 200,
    "msg": "Item deleted."
}
- 404 NOT FOUND {"status": "ERROR", "code": 404, "msg": "Not found"}
- 500 ERROR {"status": "ERROR", "code": 500, "msg": "Exeption msg which caused error"}

### Offers:
#### GET /offer/product/<product_id>
##### Headers:
- None 
##### Request:
- Id in path
##### Response:
- 200 OK [
    {
        "id": ID of the offer,
        "items_in_stock": count of items in stock,
        "price": price per unit
    },
    {...},
    {...},
    ...
 ]
- 404 NOT FOUND {"status": "ERROR", "code": 404, "msg": "Not found"}
- 500 ERROR {"status": "ERROR", "code": 500, "msg": "Exeption msg which caused error"}
#### GET /offer/<offer_id>
##### Headers:
- None
##### Request:
- ID in path
##### Response:
- 200 OK {
                    "product.name" : "Name of the product",
                    "product.description": "description of the product",
                    "id": "ID of offer",
                    "price": "price per unit",
                    "items_in_stock": "count of items in stock"
}
- 404 NOT FOUND {"status": "ERROR", "code": 404, "msg": "Not found"}
- 500 ERROR {"status": "ERROR", "code": 500, "msg": "Exeption msg which caused error"}

### Tests:
- In tests.py there some test that focus on testing routes
- in file are also testing variables and jsons as reference to tests
- so for testing you have to rewrite those variables and jsons which data you wish to test
- or just run command ```python tests.py``` after command ```python db_maker.py``` to work with default values in tests.py






