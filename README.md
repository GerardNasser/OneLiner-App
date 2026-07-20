# One-Liner

Mac app that turns pasted multi-line text into one clean line. Strips newlines, invisible characters, and exotic Unicode whitespace, then collapses runs of whitespace to single spaces.

Handy for text pulled out of PDFs, hard-wrapped emails, or anywhere you want the words without the line breaks.

## Install

Grab `One-Liner.app` from the [Releases](../../releases) page and drop it into Applications.

The app isn't code-signed, so on first launch macOS will refuse to open it. Right-click the app, choose **Open**, then click **Open** in the warning dialog. After that it opens normally.

Python isn't required on the target Mac — everything is bundled.

## Use

One step: press **⌘⇧V** (or click **Paste & Flatten**) — it pastes the clipboard, flattens it, and copies the result back to the clipboard.

Or the manual route: paste text into the input box, click **Flatten** (⌘+Return), then **Copy Result**.

Options:

- **Join hyphenated line breaks** — `exam-`↵`ple` becomes `example` (the classic PDF artifact).
- **Preserve paragraph breaks** — blank lines are kept; only wrapped lines inside each paragraph are joined.

## Build from source

```
pip3 install customtkinter pyinstaller
pyinstaller One-Liner.spec --clean
codesign --force --deep -s - dist/One-Liner.app
```

The `codesign` step applies an ad-hoc signature — it doesn't remove the Gatekeeper warning, but it prevents the "app is damaged" error on newer macOS.

The flattening logic lives in `flatten.py` (pure, no UI); run its tests with `pip3 install pytest && pytest`. Pushing a `v*` tag runs the GitHub Actions workflow, which tests, builds, signs, and attaches the zip to the release automatically.

The bundled app appears in `dist/One-Liner.app`. The app icon lives at `assets/One-Liner.icns`; regenerate it with `python3 assets/make_icon.py` (needs Pillow). Builds are architecture-specific (Apple Silicon vs Intel) — build on the matching machine, or pass `--target-arch universal2` if your Python install supports it.

See `One-Liner App — Build & Deploy Guide.md` for the full build and deploy walkthrough, including Windows.

## License

Apache 2.0 — see `LICENSE`.
