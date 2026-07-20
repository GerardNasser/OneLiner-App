## What was fixed

The `One-Liner.spec` file was missing the `customtkinter` data files. PyInstaller doesn't automatically bundle customtkinter's themes/assets, so the built `.app` would fail. The existing `dist/` build also had a corrupt Python shared library. I updated the spec to include customtkinter's package data and rebuilt cleanly.

#### Prerequisites

Install the following on the **build machine** (the Mac where you compile):

1. **Python 3.10+** — [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. **pip packages:**
    
    ```
    pip3 install customtkinter pyinstaller
    ```
    

#### Building the App

1. Open **Terminal** and navigate to the project folder:
    
    ```
    cd "path/to/remove_linebreak_app"
    ```
    
2. Run PyInstaller with the spec file:
    
    ```
    pyinstaller One-Liner.spec --clean
    ```
    
3. Apply an ad-hoc code signature (prevents the "app is damaged" error on newer macOS; the normal Gatekeeper right-click-to-open warning remains):
    
    ```
    codesign --force --deep -s - dist/One-Liner.app
    ```
    
4. When the build completes, the app bundle is located at:
    
    ```
    dist/One-Liner.app
    ```
    

> **CI alternative:** pushing a `v*` git tag runs `.github/workflows/build.yml`, which tests, builds, signs, zips, and attaches the app to the GitHub release — no local build needed.


#### Deploying to Other Macs

1. Copy the **entire** `dist/One-Liner.app` folder to the target Mac (via AirDrop, USB drive, file share, etc.).
    
2. Place it in the **Applications** folder or anywhere convenient.
    
3. On first launch, macOS will likely block it. The recipient should:
    
    - Right-click (or Control-click) `One-Liner.app` and choose **Open**
    - Click **Open** in the security dialog
    - Alternatively: go to **System Settings > Privacy & Security** and click **Open Anyway**
4. No Python installation is needed on the target Mac — everything is bundled.
    

#### Important Notes

- The built app is **macOS only** and **architecture-specific** (ARM for Apple Silicon, x86 for Intel). To support both, build on the respective hardware or use `--target-arch universal2` (requires a universal2 Python install).
- To build for **Windows**, run the same `pyinstaller` command on a Windows machine with the same pip packages installed. The output will be an `.exe` in `dist/`.
- If you update `main.py`, simply re-run the `pyinstaller One-Liner.spec --clean` command to produce a fresh build.