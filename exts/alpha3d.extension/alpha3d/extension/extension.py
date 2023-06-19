import base64, os, uuid, shutil
from io import BytesIO

import omni.ext
import omni.ui as ui
from PIL import Image

from .login import Login
from .product_service import ProductService


# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[alpha3d.extension] some_public_function was called with x: ", x)
    return x ** x


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class Alpha3dExtensionExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def __init__(self):
        self.email_input = None
        self.password_input = None
        self.access_token = None
        self.mocked = False
        self.assets = []

    def on_startup(self, ext_id):
        print("[alpha3d.extension] alpha3d extension startup")

        self.create_temp_dir()
        self._count = 0
        self._show_login = False
        self._show_login_error = False
        self._show_login_error_msg = "Wrong password"
        self._show_assets_error = False
        self._show_assets_error_msg = "No assets available"

        self._window = ui.Window("Alpha3D", width=400, height=400)
        self.show_content()

    @staticmethod
    def create_temp_dir():
        temp_dir = os.path.join(os.getcwd(), r'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

    @staticmethod
    def remove_temp_dir():
        temp_dir = os.path.join(os.getcwd(), r'temp')
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

    def on_shutdown(self):
        self.remove_temp_dir()
        print("[alpha3d.extension] alpha3d extension shutdown")

    def is_logged(self):
        return self.access_token is not None

    @staticmethod
    def base64_to_image(thumbnail, image_file):
        # Decode the base64 string to bytes
        binary_data = base64.b64decode(thumbnail)

        byte_stream = BytesIO(binary_data)
        image = Image.open(byte_stream)
        image.save(image_file)

    def login_button_clicked(self):
        username = self.email_input.model.get_value_as_string()
        password = self.password_input.model.get_value_as_string()

        login = Login(username, password, mocked=self.mocked)

        #self.access_token = login.sign_in()
        self.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpbGF5ZGErYWRtaW5AYWxwaGEzZC5pbyIsInVzZXJfbmFtZSI6ImlsYXlkYSthZG1pbkBhbHBoYTNkLmlvIiwic2NvcGUiOlsiZXh0ZXJuYWwiLCJyZWFkIiwid3JpdGUiXSwicm9sZXMiOlsiUk9MRV9BRE1JTiJdLCJjb21wYW55IjoiQWxwaGEgQVIgT8OcIiwiZXhwIjoxNjg3MzU5NTM3LCJ1dWlkIjoiMWQwYjk0N2MtMWRjZS00MjVhLTg3ZTAtNzc5YjQ3MDhiMjkwIiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9BRE1JTiJdLCJqdGkiOiJ2NlVyU2wzN3BaUWJMUjNkclp2ZGowdzI2TTAiLCJlbWFpbCI6ImlsYXlkYSthZG1pbkBhbHBoYTNkLmlvIiwiY2xpZW50X2lkIjoic2VsZi1zZXJ2aWNlIiwic3RhdHVzIjoiQUNUSVZFIn0.li8LBqwEWf6MJu-e4kCpxvxhjszwHhfJ9sa1OujjSfY"

        if self.is_logged():
            product_service = ProductService(self.access_token, "USD", mocked=self.mocked)
            self.assets = product_service.browse_assets()
        self.show_content()

    def show_content(self):
        if not self.is_logged():
            with self._window.frame:
                with ui.VStack(spacing=4):
                    label = ui.Label("Log in", alignment=ui.Alignment.CENTER_BOTTOM, height=40, style={"font_size": 40})
                    label_alpha = ui.Label("with your Alpha3D account", alignment=ui.Alignment.CENTER_TOP, height=50)

                    label_login_error = ui.Label(self._show_login_error_msg, alignment=ui.Alignment.CENTER_TOP,
                                                 height=20,
                                                 style={"color": "red"}) if self._show_login_error else None

                    email_label = ui.Label("Email:", alignment=ui.Alignment.CENTER_BOTTOM, height=10)
                    self.email_input = ui.StringField(placeholder="Email", height=20, style={"margin_width": 40})

                    password_label = ui.Label("Password:", alignment=ui.Alignment.CENTER_BOTTOM, height=30)
                    self.password_input = ui.StringField(password_mode=True, height=20, style={"margin_width": 40})

                    ui.Button("Log In", height=80, style={"margin_width": 100, "margin_height": 20},
                              clicked_fn=self.login_button_clicked)

        else:
            with self._window.frame:
                with ui.VStack():
                    label_assets_error = ui.Label(self._show_assets_error_msg, alignment=ui.Alignment.CENTER_TOP,
                                                  height=20,
                                                  style={"color": "red"}) if self._show_assets_error else None
                    with ui.ScrollingFrame():
                        with ui.VGrid(column_width=100, column_height=100):
                            for asset in self.assets:
                                brand_name = asset["brandName"]
                                model_name = asset["modelName"]
                                thumbnail = asset["thumbnail"]
                                asset_files = asset["assetFiles"]

                                image_uuid = uuid.uuid4()

                                image_file = os.path.join(os.getcwd(), r'temp') + "/" + str(image_uuid) + ".png"
                                model_file = os.path.join(os.getcwd(), r'temp') + "/" + str(image_uuid) + ".usd"


                                self.base64_to_image(thumbnail, image_file)
                
                                if asset_files is not None and len(asset_files) > 0:


                                    decoded_model_content = base64.b64decode(asset_files[0]['base64'])

                                    with open(model_file, 'wb') as model_file_obj:
                                        model_file_obj.write(decoded_model_content)
 

                                    #self.base64_to_image(asset_files[0]['base64'], model_file)

                                def drag(image_file, model_file):
                                    with ui.VStack():
                                        ui.Image(image_file, width=100, height=100)
                                        ui.Label(brand_name)
                                        ui.Label(model_name)
                                    return image_file

                                def drag_area(url, model_file):
                                    image = ui.ImageWithProvider(image_file, width=100, height=90,
                                                                 style={"margin_width": 5})
                                    _brand_name = ui.Label(brand_name, alignment=ui.Alignment.CENTER_TOP, height=10,
                                                           style={"font_size": 15})
                                    _model_name = ui.Label(model_name, alignment=ui.Alignment.CENTER_TOP, height=30,
                                                           style={"font_size": 15})
                                    image.set_drag_fn(lambda: drag(url, model_file))

                                with ui.VStack():
                                    drag_area(
                                        image_file,
                                        model_file)
