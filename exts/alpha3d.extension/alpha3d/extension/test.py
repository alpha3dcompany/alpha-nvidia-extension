import base64
import uuid
from io import BytesIO
from PIL import Image
import os
from login import Login
from product_service import ProductService


def base64_to_image(thumbnail, image_file):
    # Decode the base64 string to bytes
    binary_data = base64.b64decode(thumbnail)

    byte_stream = BytesIO(binary_data)
    image = Image.open(byte_stream)
    image.save(image_file)

username = "ilayda+admin@alpha3d.io"
password = "E4yR7Gz4q!"

# Login
login = Login(username, password)
token = login.sign_in()

file_format = "GLB"
product_service = ProductService(token, file_format)

image_uuid = uuid.uuid4()

# Viewing asset browser
asset_list = product_service.browse_assets()
model_file = os.path.join(os.getcwd(),  str(image_uuid) + ".glb")

decoded_model_content = base64.b64decode(asset_list[0]['assetFiles'][0]['base64'])

print(asset_list)
with open(model_file, 'wb') as model_file_obj:
    model_file_obj.write(decoded_model_content)
    print(image_uuid)

# self.base64_to_image(asset_files[0]['base64'], model_file)
#print(asset_list)