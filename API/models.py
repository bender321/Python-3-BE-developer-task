from flask_sqlalchemy import SQLAlchemy

# Database
db = SQLAlchemy()


# Models
class Product(db.Model):
    """
    Model that represents product.
    """

    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(255))
    offers = db.relationship(
                                'Offer',
                                backref='product',
                                cascade="all,delete",
                                lazy=True
                            )

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Offer(db.Model):
    """
    Model that represents offer of the specific product.
    """

    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    price = db.Column(db.Integer)
    items_in_stock = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
