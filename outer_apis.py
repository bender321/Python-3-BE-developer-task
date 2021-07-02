import requests
import os


class AppliftingAPI:
    """
    Class that represents API from Applifting
    """

    def __init__(self, file_name, base_url=os.getenv('BASE_URL')):
        self.file_name = file_name
        self.base_url = base_url
        self.token = self.__get_token()

    def __pull_token(self):
        """
        Private method that takes care of pulling access token from outer API.
        Generating file with token to preserve it for future usage.

        :return: token
        """

        try:
            url = self.base_url + '/auth'
            res = (requests.post(url)).json()
            token = res['access_token']

            with open(self.file_name, 'w+') as f:
                f.write(token)
        except Exception as e:
            return str(e)
        else:
            return token

    def __get_token(self):
        """
        Private method that takes care of getting token from file
        or asking for token outside if needed.

        :return: token
        """

        if os.path.isfile(self.file_name):
            try:
                with open(self.file_name, 'r') as f:
                    token = f.read()
            except Exception as e:
                return str(e)
            else:
                if token == "":
                    token = self.__pull_token()
                else:
                    return token
        else:
            token = self.__pull_token()

        return token

    def register_product(self, product_info):
        """
        Method that takes care of registering product to outer API.

        :param product_info: json {id, name, description}
        :return: response -> json
        """

        url = self.base_url + '/products/register'
        try:
            res = (requests.post(url, json=product_info, headers={"Bearer": self.token})).json()

        except Exception as e:
            return str(e)
        else:
            return res

    def get_product_offers(self, product_id):
        """
        Method that takes care of getting and returning all
        offers associated with specific product.

        :param product_id: int, str
        :return: response -> json
        """
        try:
            url = self.base_url + '/products/' + str(product_id) + '/offers'
            res = (requests.get(url, headers={"Bearer": self.token})).json()
        except Exception as e:
            return str(e)
        else:
            return res
