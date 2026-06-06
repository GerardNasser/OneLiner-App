# One-Liner

Mac app that turns pasted multi-line text into one clean line. Strips newlines, invisible characters, and exotic Unicode whitespace, then collapses runs of whitespace to single spaces.

Handy for text pulled out of PDFs, hard-wrapped emails, or anywhere you want the words without the line breaks.

## Install

Grab `One-Liner.app` from the [Releases](../../releases) page and drop it into Applications.

The app isn't code-signed, so on first launch macOS will refuse to open it. Right-click the app, choose **Open**, then click **Open** in the warning dialog. After that it opens normally.

Python isn't required on the target Mac — everything is bundled.

## Use

Paste text, click **Flatten to One Line** (or press ⌘+Return), click **Copy Result**.

## Build from source

```
pip3 install customtkinter pyinstaller
pyinstaller One-Liner.spec --clean
```

The bundled app appears in `dist/One-Liner.app`. Builds are architecture-specific (Apple Silicon vs Intel) — build on the matching machine, or pass `--target-arch universal2` if your Python install supports it.

See `One-Liner App — Build & Deploy Guide.md` for the full build and deploy walkthrough, including Windows.

## License

Apache 2.0 — see `LICENSE`.
