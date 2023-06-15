import requests


class ProductService:
    def __init__(self, bearer_token, file_format):
        self.bearer_token = bearer_token
        self.file_format = file_format
        self.params = {
            "fileFormat": self.file_format
        }
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {self.bearer_token}'
        }

    def do_request(self, url):
        response = requests.get(url, headers=self.headers, params=self.params)

        if response.status_code == 200:
            print("Request is proceed successfully!")
            return response.json()
        else:
            print("Request could not be proceed successfully!")
            print(f"{response.status_code}: {response.content}")

    def browse_assets(self):
        return self.do_request("http://localhost:8080/alphaar/api/ext/product/approved")

    def retrieve_asset_files(self, product_uuid):
        return self.do_request("http://localhost:8080/alphaar/api/ext/asset/" + product_uuid)



