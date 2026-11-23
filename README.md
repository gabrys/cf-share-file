# cf-share-file

Share one file over the internet using a Cloudflare quick tunnel. The command
starts a local HTTP server, launches `cloudflared`, and prints the public file
URL to standard output. Press Ctrl+C to stop sharing.

## Installation

Requires Python 3.10 or newer and the standalone
[`cloudflared` executable](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
on your `PATH`. Installing this package does not install `cloudflared`.

```sh
uvx cf-share-file --help
```

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).
`uvx` downloads the package and runs it in an isolated environment.
For a persistent command, use `uv tool install cf-share-file`.

## Usage

```sh
uvx cf-share-file ./report.pdf
uvx cf-share-file ./report.pdf --auth 'alice:change-this-password'
uvx cf-share-file --help
```

With a persistent installation, you can run `cf-share-file` directly.
The local server listens on `127.0.0.1`; the port is always chosen automatically.
Only the selected file path is served. GET and HEAD are supported.
Logs go to standard error; the public URL goes to standard output.

The package includes `qrcode` and displays a terminal QR code for the public
file URL on standard error. Scan it to open the file on another device.
With `--auth`, the browser still requires credentials; they are not in the QR code.

You can also run the downloaded script without any Python dependencies:

```sh
python3 cf_share_file.py ./report.pdf
```

If `qrcode` is not installed, the script prints the URL and skips the QR code.
The external `cloudflared` executable is still required in both modes.

Without `--auth`, anyone who knows the public URL can download the file.
With `--auth`, requests require HTTP Basic authentication. Command-line
credentials may be visible in shell history or process listings.
The temporary tunnel depends on Cloudflare's service. The URL may need a few
seconds before it becomes reachable.

## Development

```sh
uv run python -m unittest discover -s tests -v
uvx --from build pyproject-build
uvx twine check --strict dist/*
```

## Publishing

The current version is `0.3.0`. Build from a clean checkout using the commands
above, ensuring `dist/` contains only the current release. Upload to TestPyPI:

```sh
uvx twine upload --repository testpypi dist/*
```

Verify the TestPyPI release in an isolated environment:

```sh
uvx --isolated --index https://test.pypi.org/simple/ --default-index https://pypi.org/simple/ cf-share-file@0.3.0 --help
```

Then upload the same artifacts to PyPI:

```sh
uvx twine upload dist/*
```

Use an API token when Twine prompts for credentials. Never commit credentials.
For subsequent releases, update the version in `pyproject.toml` and build fresh
artifacts; PyPI does not allow replacing an existing release file.
GitHub Actions runs tests and validates distributions; publishing is manual.

## License

MIT; see [LICENSE](LICENSE).
