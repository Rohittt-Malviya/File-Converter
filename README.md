# Local Convert

Local Convert is a privacy-first file converter that runs entirely in the browser. Files are read, converted, and downloaded locally; there is no server, account, analytics, or upload step.

## Supported conversions

- Text family: TXT, Markdown, CSV, and JSON
- Image family: PNG, JPEG, and WebP
- CSV files can be converted to structured JSON records
- Images use the browser's native Canvas APIs

## Run locally

Any static web server works. For example:

```sh
python3 -m http.server 8080
```

Then open `http://localhost:8080`. The app does not require a build step or runtime dependency.

## Development

```sh
npm test
npm run check
```

## Privacy and security

Conversion is performed in the page using browser APIs. No file contents are sent over the network. For maximum offline use, serve the repository locally or package it with a static desktop shell.
