# JAMXSS (Just A Monster XSS Scanner)

JAMXSS is a powerful tool designed to test for reflected XSS vulnerabilities in web applications. Leveraging machine learning, it predicts contexts for reflections and suggests appropriate payloads, with options for executing them to test vulnerabilities.

## Features

- **Machine Learning Powered**: Utilizes machine learning to predict the context of reflections and generate suitable payloads.
- **Stealth Mode**: Suggests payloads without executing them, useful for safe scanning.
- **Attack Mode**: Executes suggested payloads to actively test for vulnerabilities.
- **Single Scan Mode**: Allows for a quick scan of a single URL.
- **Multi-threaded**: Efficiently handles multiple URLs concurrently.
- **Custom Headers**: Supports custom cookie headers and user-agent strings for requests.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/jamxss.git
    cd jamxss
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

```bash
python3 jamxss.py -u <target_url> [options]
```

## Options

- `-u, --url` (required): Target URL of the web application.
- `--single-scan`: Perform a single scan on the provided URL only.
- `--stealth-mode`: Only suggest payloads without executing them.
- `--attack-mode`: Execute suggested payloads to test for vulnerabilities.
- `--cookie`: Custom cookie header to use for the requests.
- `--user-agent`: Custom user agent string. Default is Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36.

## Examples

### Single scan with stealth mode:

```bash
python3 jamxss.py -u http://example.com --single-scan --stealth-mode
```

### Full scan with attack mode:

```bash
python3 jamxss.py -u http://example.com --attack-mode
```

## How It Works

- **Crawler**: The tool crawls the provided URL to collect links.
- **Reflections Testing**: Tests for reflections in the collected links.
- **Context Prediction**: Uses machine learning to predict the context of the reflections.
- **Payload Generation**: Generates suitable payloads based on the predicted context.
- **Payload Execution (Attack Mode)**: Executes the generated payloads to test for vulnerabilities.

## Screenshot

![JAMXSS on Action](https://github.com/0xh4ty/JAMXSS/blob/main/images/JAMXSS.png?raw=true)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.

## Contact

For any issues or suggestions, please open an issue on the [GitHub repository](https://github.com/0xh4ty/JAMXSS).
