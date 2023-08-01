import base64, os, uuid, shutil
from io import BytesIO

import omni.ext
import omni.ui as ui
from PIL import Image
from pathlib import Path
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

    temp_dir = Path.home() / 'temp'
    temp_dir = temp_dir.as_posix()

    def __init__(self):
        super().__init__()
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
        if not os.path.exists(Alpha3dExtensionExtension.temp_dir):
            os.makedirs(Alpha3dExtensionExtension.temp_dir)

    @staticmethod
    def remove_temp_dir():
        if os.path.exists(Alpha3dExtensionExtension.temp_dir):
            shutil.rmtree(Alpha3dExtensionExtension.temp_dir)

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
        
        self.access_token = login.sign_in()

        if self.is_logged():
            product_service = ProductService(self.access_token, "GLB", mocked=self.mocked)
            self.assets = product_service.browse_assets()
        self.show_content()

    def show_my_assets(self):
        self.show_my_assets()

    def show_library(self):
        self.show_library()

    def show_content(self):
        if not self.is_logged():
            with self._window.frame:
                with ui.VStack(spacing=4):
                    label = ui.Label("Log in", alignment=ui.Alignment.CENTER_BOTTOM, height=40, style={"font_size": 40})
                    label_alpha = ui.Label("with your Alpha3D account", alignment=ui.Alignment.CENTER_TOP, height=5)
                    label_sign_up = ui.Label("If you don't have an account, visit app.alpha3d.io/signup to sign up.",
                                             alignment=ui.Alignment.CENTER_TOP, height=50)

                    label_login_error = ui.Label(self._show_login_error_msg, alignment=ui.Alignment.CENTER_TOP,
                                                 height=20,
                                                 style={"color": "red"}) if self._show_login_error else None

                    email_label = ui.Label("Email:", alignment=ui.Alignment.CENTER_BOTTOM, height=10)
                    self.email_input = ui.StringField(placeholder="Email", height=20, style={"margin_width": 40})

                    password_label = ui.Label("Password:", alignment=ui.Alignment.CENTER_BOTTOM, height=30)
                    self.password_input = ui.StringField(password_mode=True, height=20, style={"margin_width": 40})

                    ui.Button("Log In", height=80, style={"margin_width": 100, "margin_height": 20},
                              clicked_fn=self.login_button_clicked)

                    label_alpha_is = ui.Label("Alpha3D is a generative AI-powered platform that",
                                              alignment=ui.Alignment.CENTER, height=5)
                    label_alpha_is2 = ui.Label("enables users to automatically transform 2D images",
                                               alignment=ui.Alignment.CENTER, height=5)
                    label_alpha_is3 = ui.Label("of real-world objects into 3D digital assets in minutes.",
                                               alignment=ui.Alignment.CENTER, height=5)

        else:
            self.show_my_assets()

    def show_my_assets(self):
        with self._window.frame:
            with ui.VStack(spacing=4):
                with ui.HStack(height=10, spacing=4):
                    ui.Button("My assets", height=10,
                              style={"margin_height": 5, "border_radius": 5, "background_color": "gray"},
                              clicked_fn=self.show_my_assets)
                    ui.Button("Library", height=10, style={"margin_height": 5, "border_radius": 5},
                              clicked_fn=self.show_library)

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

                                image_file = os.path.join(Alpha3dExtensionExtension.temp_dir, str(image_uuid) + ".PNG")
                                model_file = os.path.join(Alpha3dExtensionExtension.temp_dir, str(image_uuid) + ".glb")

                                self.base64_to_image(thumbnail, image_file)

                                if asset_files is not None and len(asset_files) > 0:
                                    decoded_model_content = base64.b64decode(asset_files[0]['base64'])

                                    with open(model_file, 'wb') as model_file_obj:
                                        model_file_obj.write(decoded_model_content)

                                def drag(image_file, url):
                                    with ui.VStack():
                                        ui.Image(image_file, width=100, height=100)
                                        ui.Label(brand_name)
                                        ui.Label(model_name)
                                    return url

                                def drag_area(image_file, url):
                                    image = ui.ImageWithProvider(image_file, width=100, height=90,
                                                                 style={"margin_width": 5})
                                    _brand_name = ui.Label(brand_name, alignment=ui.Alignment.CENTER_TOP, height=10,
                                                           style={"font_size": 15})
                                    _model_name = ui.Label(model_name, alignment=ui.Alignment.CENTER_TOP, height=30,
                                                           style={"font_size": 15})
                                    image.set_drag_fn(lambda: drag(image_file, url))

                                with ui.VStack():
                                    drag_area(
                                        image_file,
                                        model_file)

    def show_library(self):
        with self._window.frame:
            with ui.VStack(spacing=4):
                with ui.HStack(height=10, spacing=4):
                    ui.Button("My assets", height=10, style={"margin_height": 5, "border_radius": 5},
                              clicked_fn=self.show_my_assets)
                    ui.Button("Library", height=10,
                              style={"margin_height": 5, "border_radius": 5, "background_color": "gray"},
                              clicked_fn=self.show_library)

                with ui.ScrollingFrame():
                    with ui.VGrid(column_width=100, column_height=100):
                        def drag(model_name, brand_name, url, thumbnail):
                            with ui.VStack():
                                ui.Image(thumbnail, width=100, height=100)
                                ui.Label(brand_name)
                                ui.Label(model_name)
                            return url

                        def drag_area(model_name, thumbnail, url, brand_name=""):
                            image = ui.Image(thumbnail, width=100, height=90, style={"margin_width": 5})
                            model = ui.Label(model_name, alignment=ui.Alignment.CENTER_TOP, height=30,
                                             style={"font_size": 15})
                            brand = ui.Label(brand_name, alignment=ui.Alignment.CENTER_TOP, height=10,
                                             style={"font_size": 15})
                            image.set_drag_fn(lambda: drag(model_name, brand_name, url, thumbnail))

                        path = Path(__file__).parent.parent.parent / "data"
                        data_base_path = path.as_posix()

                        library_assets = ["armchair", "baby_bid", "bottle", "bottle_opener", "chair", "couch",
                                          "glasses", "lamp", "mouse_pad", "mug", "ring", "shot_glass", "sideboard",
                                          "sofa", "t_shirt"]

                        for asset in library_assets:
                            with ui.VStack():
                                drag_area(asset, os.path.join(data_base_path, asset + ".PNG"),
                                          os.path.join(data_base_path, asset + ".glb"))
