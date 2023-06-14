import omni.ext
import omni.ui as ui
from .login import Login


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

    def on_startup(self, ext_id):
        print("[alpha3d.extension] alpha3d extension startup")

        self._count = 0
        self._show_login = False
        self._show_login_error = False
        self._show_login_error_msg = "Wrong password"
        self._show_assets_error = False
        self._show_assets_error_msg = "No assets available"

        self._window = ui.Window("Alpha3D", width=400, height=400)
        with self._window.frame:
            self.show_content()

    def on_shutdown(self):
        print("[alpha3d.extension] alpha3d extension shutdown")

    def is_logged(self):
        return self.access_token is not None

    def login_button_clicked(self):
        username = self.email_input.model.get_value_as_string()
        password = self.password_input.model.get_value_as_string()

        login = Login(username, password)

        self.access_token = login.sign_in()
        self.show_content()

    def show_content(self):
        if not self.is_logged():
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
            with ui.VStack():
                label_assets_error = ui.Label(self._show_assets_error_msg, alignment=ui.Alignment.CENTER_TOP, height=20,
                                              style={"color": "red"}) if self._show_assets_error else None
                with ui.ScrollingFrame():
                    with ui.VGrid(column_width=100, column_height=100):
                        for i in range(10):
                            def drag(url, thumbnail):
                                with ui.VStack():
                                    ui.Image(thumbnail, width=100, height=100)
                                    ui.Label("Brand name")
                                    ui.Label("Model name")
                                return url

                            def drag_area(thumbnail, url):
                                image = ui.Image(thumbnail, width=100, height=90, style={"margin_width": 5})
                                brand_name = ui.Label("Brand name", alignment=ui.Alignment.CENTER_TOP, height=10,
                                                      style={"font_size": 15})
                                model_name = ui.Label("Model name", alignment=ui.Alignment.CENTER_TOP, height=30,
                                                      style={"font_size": 15})
                                image.set_drag_fn(lambda: drag(url, thumbnail))

                            with ui.VStack():
                                drag_area(
                                    "https://www.clipartkey.com/mpngs/m/269-2698741_clip-art-texture-png-for-bush-tree-png.png",
                                    "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Vegetation/Shrub/Acacia.usd")
