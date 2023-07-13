# ALPHA3D EXTENSION Project Template

This project was automatically generated.

- `app` - It is a folder link to the location of your *Omniverse Kit* based app.
- `exts` - It is a folder where you can add new extensions. It was automatically added to extension search path. (Extension Manager -> Gear Icon -> Extension Search Path).

# App Link Setup

If `app` folder link doesn't exist or broken it can be created again. For better developer experience it is recommended to create a folder link named `app` to the *Omniverse Kit* app installed from *Omniverse Launcher*. Convenience script to use is included.

Run:

```
> link_app.bat
```

If successful you should see `app` folder link in the root of this repo.

If multiple Omniverse apps is installed script will select recommended one. Or you can explicitly pass an app:

```
> link_app.bat --app create
```

You can also just pass a path to create link to:

```
> link_app.bat --path "C:/Users/bob/AppData/Local/ov/pkg/create-2021.3.4"
```

_!!! Command lines may change depending on the operating system used._


# Open ALPHA3D EXTENSION

- Look for "ALPHA3D EXTENSION" extension in extension manager and enable it. Try applying changes to any python files, it will hot-reload and you can observe results immediately.


- Alternatively, you can launch your app from console with this folder added to search path and your extension enabled, e.g.:

```
> app\omni.code.bat --ext-folder exts --enable company.hello.world
```

# Login Credentials

- After enabling Alpha3D Extension, a login screen will pop up.

- Users with a user account on the Alpha3D platform can login to this extension. (If not, please contact Alpha3D.)

- After logging in, you can see and use the approved 3d assets on the platform and the assets in the library.