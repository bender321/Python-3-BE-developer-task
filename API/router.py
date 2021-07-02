from flask import jsonify, request
from schemas import ma, ProductSchema, OfferSchema, OffersSchema
from models import db, Product, Offer
from outer_apis import AppliftingAPI
# from tasker import make_celery


def create_app(app):
    """
    Function that takes care of initialization
    of Flaks API router with configuration and Schemas.
    :param app: Flask app object

    :return: app
    """
    app.config.from_pyfile('app_settings.py')
    db.init_app(app)
    ma.init_app(app)
    # app.config.update(CELERY_BROKER_URL='redis://localhost:6379')

    outer_api = AppliftingAPI('token.txt')

    # Setup celery
    # celery = make_celery(app)

    # ma setup
    product_schema = ProductSchema(many=False)
    products_schema = ProductSchema(many=True)
    offer_schema = OfferSchema(many=False)
    offers_schema = OffersSchema(many=True)

    # Routes
    @app.errorhandler(404)
    def invalid_route(e):
        return jsonify({"status": "Error", "code": 404, "msg": "Invalid route"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"status": "Error", "code": 500, "msg": "Internal server error"}), 500

    @app.route('/product', methods=['POST'])
    def add_product():

        name = request.json['name']
        description = request.json['description']
        new_product = Product(name, description)
        db.session.add(new_product)
        db.session.commit()

        product_to_register = {
                                "id": new_product.id,
                                "name": name,
                                "description": description
                                }

        res = outer_api.register_product(product_to_register)

        if res['id'] == str(new_product.id):

            offers = outer_api.get_product_offers(new_product.id)
            for index in range(len(offers)):
                new_offer = Offer(
                    id=offers[index]['id'],
                    price=offers[index]['price'],
                    items_in_stock=offers[index]['items_in_stock'],
                    product=new_product
                )

                db.session.add(new_offer)

            db.session.commit()

            return jsonify({
                        "status": "OK",
                        "code": 200,
                        "msg": "Product added to the database successfully."
                    }), 200
        else:
            return jsonify({
                        "status": "ERROR",
                        "code": 500,
                        "msg": "Error during registration of product."
                    }), 500

    @app.route('/product', methods=['GET'])
    def get_products():

        try:
            all_products = Product.query.all()
            res = products_schema.dump(all_products)
            if not res:
                return jsonify({"status": "ERROR", "code": 404, "msg": "Not found"}), 404

        except Exception as e:
            return jsonify({"status": "ERROR", "code": 500, "msg": str(e)}), 500
        else:
            return jsonify(res), 200

    @app.route('/product/<product_id>', methods=['GET'])
    def get_product(product_id):

        try:
            one_product = Product.query.get(product_id)
            if one_product is not None:
                res = product_schema.jsonify(one_product)
            else:
                return jsonify({"status": "ERROR", "code": 404, "msg": "Not found"}), 404
        except Exception as e:
            return jsonify({"status": "ERROR", "code": 500, "msg": str(e)}), 500
        else:
            return res, 200

    @app.route('/product/<product_id>', methods=['PUT'])
    def update_product(product_id):

        try:
            product_to_update = Product.query.get(product_id)
            if product_to_update is None:
                return jsonify({"status": "ERROR", "code": 404, "msg": "Not found"}), 404
            else:
                name = request.json['name']
                description = request.json['description']

                product_to_update.name = name
                product_to_update.description = description
                db.session.commit()

        except Exception as e:
            return jsonify({"status": "ERROR", "code": 500, "msg": str(e)}), 500
        else:
            return product_schema.jsonify(product_to_update), 200

    @app.route('/product/<product_id>', methods=['DELETE'])
    def delete_product(product_id):

        try:
            one_product = Product.query.get(product_id)
            if one_product is None:
                return jsonify({"status": "ERROR", "code": 404, "msg": "Not found"}), 404
            else:
                db.session.delete(one_product)
                db.session.commit()

        except Exception as e:
            return jsonify({"status": "ERROR", "code": 500, "msg": str(e)}), 500
        else:
            return jsonify({"code": 200, "msg": "Item deleted."}), 200

    @app.route('/offer/product/<product_id>', methods=['GET'])
    def get_product_offers(product_id):

        try:
            offers = Offer.query.filter_by(product_id=product_id).all()
            res = offers_schema.dump(offers)
            if not res:
                return jsonify({"status": "ERROR", "code": 404, "msg": "Not found"}), 404

        except Exception as e:
            return jsonify({"status": "ERROR", "code": 500, "msg": str(e)}), 500
        else:
            return jsonify(res), 200

    @app.route('/offer/<offer_id>', methods=['GET'])
    def get_offer(offer_id):

        try:
            offer = Offer.query.get(offer_id)
            if offer is None:
                return jsonify({"status": "ERROR", "code": 404, "msg": "Item not found"}), 404

        except Exception as e:
            return jsonify({"status": "ERROR", "code": 500, "msg": str(e)}), 500
        else:
            return offer_schema.jsonify(offer), 200

    return app

