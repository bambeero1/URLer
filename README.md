# Web Scraping Script

This script is designed for web scraping using Playwright, a Python library for browser automation. It extracts URLs from a given website and saves them in either JSON or TXT format. It includes options to skip crawling or saving URLs containing specific keywords.

## Prerequisites

- Python 3.x
- Playwright: `pip install playwright`
- Colorlog: `pip install colorlog`

## Usage

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/web-scraping-script.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd web-scraping-script
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the script with the desired parameters:**

    ```bash
    python main.py <main_url> -o <output_format> --negative_crawl <keywords_to_skip_crawling> --negative_save <keywords_to_skip_saving> --log-level <log_level>
    ```

    - `<main_url>`: The main URL to start scraping.
    - `<output_format>`: Output format (json or txt).
    - `<keywords_to_skip_crawling>`: Keywords to skip crawling if found in the URL.
    - `<keywords_to_skip_saving>`: Keywords to skip saving if found in the URL.
    - `<log_level>`: Logging level (debug or info).

## Example

```bash
python main.py https://example.com -o json --negative_crawl login admin --negative_save logout --log-level info
```

## Options

- `main_url`: The main URL of the website to start crawling.
- `-o`, `--output`: Output format (json or txt). Default is txt.
- `--negative_crawl`: Keywords to skip crawling if found in the URL.
- `--negative_save`: Keywords to skip saving if found in the URL.
- `--log-level`: Logging level (debug or info). Default is info.

## Logging

By default, the script logs at the DEBUG level, providing detailed information during execution. If you prefer to see only important messages, you can set the `--log-level` option to "info".

For colored logs, the script uses `colorlog`. Log colors are based on log levels:
- DEBUG: cyan
- INFO: green
- WARNING: yellow
- ERROR: red
- CRITICAL: red on a white background

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

Feel free to adjust it based on your specific needs.
