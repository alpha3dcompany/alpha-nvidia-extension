import requests
from .mocked import Mocked

class ProductService:
    def __init__(self, bearer_token, file_format, mocked=False):
        self.bearer_token = bearer_token
        self.file_format = file_format
        self.params = {
            "fileFormat": self.file_format
        }
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {self.bearer_token}'
        }
        self.mocked = mocked

    def do_request(self, url):
        response = requests.get(url, headers=self.headers, params=self.params)

        if response.status_code == 200:
            print("Request is proceed successfully!")
            return response.json()
        else:
            print("Request could not be proceed successfully!")
            print(f"{response.status_code}: {response.content}")

    def browse_assets(self):
        if self.mocked:
            return  Mocked.mocked_assets()
        assets = self.do_request("https://app.alpha3d.io/alphaar/api/ext/product/approved")
        for index, asset in enumerate(assets):
            _uuid = asset['uuid']
            assets[index]['assetFiles'] = self.retrieve_asset_files(_uuid)
        return assets

    def retrieve_asset_files(self, product_uuid):
        if self.mocked:
            return Mocked.mocked_asset_files()
        return self.do_request("https://app.alpha3d.io/alphaar/api/ext/asset/" + product_uuid)





