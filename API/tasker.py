from celery import Celery


def make_celery(app):
    """
    Function that setups a Celery object with configuration.
    :param app: app object associated with Celery (ex. Flask)
    :return: celery object
    """
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


"""

Celery part, unfinished due to issues with database connection and performance.

@celery.task(ignore_result=True)
def test():

    for row in db.session.query(Product):
        updated_offers = outer_api.get_product_offers(row.id)
        for i in range(len(updated_offers)):
            if (db.session.query(Offer.id).filter_by(id=updated_offers[i]['id']).first() is not None):
                db.session.query(Offer)
                .filter(Offer.id == updated_offers[i]['id'])
                .update({Offer.price: updated_offers[i]['price']})
            else:
                new_offer = Offer(
                    price=updated_offers[i]["price"],
                    items_in_stock=updated_offers[i]["items_in_stock"],
                    product=row
                )

                db.session.add(new_offer)

        db.session.commit()


test.delay()
"""