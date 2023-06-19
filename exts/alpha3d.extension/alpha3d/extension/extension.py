import base64, os
from io import BytesIO
from PIL import Image
import uuid
import omni.ext
import omni.ui as ui
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

    def create_temp_dir(self):
        temp_dir = os.path.join(os.getcwd(), r'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

    def remove_temp_dir(self):
        temp_dir = os.path.join(os.getcwd(), r'temp')
        if not os.path.exists(temp_dir):
            os.removedirs(temp_dir)

    def on_shutdown(self):
        self.remove_temp_dir()
        print("[alpha3d.extension] alpha3d extension shutdown")

    def is_logged(self):
        return self.access_token is not None
    
    def base64_to_image(self, thumbnail, image_file):
    # Decode the base64 string to bytes
        binary_data = base64.b64decode(thumbnail)

        byte_stream = BytesIO(binary_data)
        image = Image.open(byte_stream)
        image.save(image_file)

    def login_button_clicked(self):
        #username = self.email_input.model.get_value_as_string()
        #password = self.password_input.model.get_value_as_string()

        #login = Login(username, password)

        # self.access_token = login.sign_in()
        self.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpbGF5ZGErYWRtaW5AYWxwaGEzZC5pbyIsInVzZXJfbmFtZSI6ImlsYXlkYSthZG1pbkBhbHBoYTNkLmlvIiwic2NvcGUiOlsiZXh0ZXJuYWwiLCJyZWFkIiwid3JpdGUiXSwicm9sZXMiOlsiUk9MRV9BRE1JTiJdLCJjb21wYW55IjoiQWxwaGEgQVIgT8OcIiwiZXhwIjoxNjg3Mjk0MDU4LCJ1dWlkIjoiMWQwYjk0N2MtMWRjZS00MjVhLTg3ZTAtNzc5YjQ3MDhiMjkwIiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9BRE1JTiJdLCJqdGkiOiIzV0N3Zl9zaGhzbnFYWnlfR0MzOGdtUHVpXzAiLCJlbWFpbCI6ImlsYXlkYSthZG1pbkBhbHBoYTNkLmlvIiwiY2xpZW50X2lkIjoic2VsZi1zZXJ2aWNlIiwic3RhdHVzIjoiQUNUSVZFIn0._BSSQawbNhohuScx9NbQK1U9GZQmZjPtffqMZ5V-V4w"

        if self.is_logged(): 
            #product_service = ProductService(self.access_token, "USD")
            # self.assets = product_service.browse_assets()
            self.assets = [
                {'uuid': '11be3b68-49ae-4f8d-b2f4-ff6d16458f5b', 'brandName': 'Nike', 'modelName': 'Air Force 1',
                
                
                 'thumbnail': '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AKbx/wDxVAHJEjB68HFJgE49q6w/C3x7tYDw3Jknj9/H/wDFUp+F/jzfkeG5cY6efHn/ANCoA5LIxmnfxbe+M11I+F3j7bg+GpCc9fPj/wDiqkHwu8el93/CNyjjH/HxF/8AFUAcjnKg84Jx0p3cjnIGa64fCnx4VAPh+Qc5/wBfF/8AFVIPhN46JJ/sNgTx/r4uP/H6AOMByFPPzU5eQSVcgZzjp+ddsnwf8bkKDpGAo7zxc/8Aj1WIfgt4xY/vLSJAfWdP6GgDglJUZ2DPu3+fat/wZ4Yn8Y+JbfTI1c25Ie5kXjZCCAxBIPJHAyDyRXc6d8ENXWRXvFibH8BuOP0Gf1r0bw54Iu/D8HlWiWlqpChvJGC+Om44yx56nNIDvVG1QMk4GOTS1Qtre+jAEk6t+v8ASrwyBycmgBaKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/9k='}
            ]

        self.show_content()

    def show_content(self):
        if not self.is_logged():
            with self._window.frame:
                with ui.VStack(spacing=4):
                    label = ui.Label("Log in", alignment=ui.Alignment.CENTER_BOTTOM, height=40, style={"font_size": 40})
                    label_alpha = ui.Label("with your Alpha3D account", alignment=ui.Alignment.CENTER_TOP, height=50)

                    label_login_error = ui.Label(self._show_login_error_msg, alignment=ui.Alignment.CENTER_TOP, height=20,
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
                    label_assets_error = ui.Label(self._show_assets_error_msg, alignment=ui.Alignment.CENTER_TOP, height=20,
                                                  style={"color": "red"}) if self._show_assets_error else None
                    with ui.ScrollingFrame():
                        with ui.VGrid(column_width=100, column_height=100):
                            for asset in self.assets:
                                brand_name = asset["brandName"]
                                model_name = asset["modelName"]
                                thumbnail = asset["thumbnail"]
                                image_uuid = uuid.uuid4()
                                import os
                                image_file = os.path.join(os.getcwd(), r'temp') + "/" + str(image_uuid) + ".png"
                                self.base64_to_image(thumbnail, image_file)

           



                                def drag(image_file, model_url):

                                    with ui.VStack():
                                        ui.Image(image_file, width=100, height=100)
                                        ui.Label(brand_name)
                                        ui.Label(model_name)
                                    return image_file

                                def drag_area(url, model_url):
                                    image = ui.ImageWithProvider(image_file, width=100, height=90,  style={"margin_width": 5})
                                    _brand_name = ui.Label(brand_name, alignment=ui.Alignment.CENTER_TOP, height=10,
                                                      style={"font_size": 15})
                                    _model_name = ui.Label(model_name, alignment=ui.Alignment.CENTER_TOP, height=30,
                                                              style={"font_size": 15})
                                    image.set_drag_fn(lambda: drag(url, model_url))

                                with ui.VStack():
                                    drag_area(
                                        image_file,
                                        "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Vegetation/Shrub/Acacia.usd")

