from login import Login
from product_service import ProductService

username = "ilayda+admin@alpha3d.io"
password = "E4yR7Gz4q!"

# Login
login = Login(username, password)
token = login.sign_in()

file_format = "USD"
product_service = ProductService(token, file_format)

# Viewing asset browser
asset_list = product_service.browse_assets()

for asset in asset_list:
    # Retrieving asset file(s)
    asset_files = product_service.retrieve_asset_files(asset['uuid'])
