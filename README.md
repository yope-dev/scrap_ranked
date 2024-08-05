# 🐍 Python Project: Trendshift.io Repository Scraper

## 📜 Project Description

This Python project scrapes data from [Trendshift.io repositories](https://trendshift.io/repositories). It extracts the following information for each repository:
- **Name**
- **Link**
- **Website**
- **Stars**
- **Forks**
- **Description**
- **ID** (on the site)
- **Programming Language**

The scraped data is then saved into an Excel file for easy access and analysis.

## 📦 Installation

To install the necessary dependencies for this project, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yope-dev/scrap_ranked.git
    cd scrap_ranked
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 How to Run

1. **Navigate to the project directory**:
    ```bash
    cd scrap_ranked
    ```

2. **Run the script**:
    ```bash
    python main.py
    ```

3. **Check the output**:
    - The script will generate an Excel file named `repositories.xlsx` in the project directory containing the scraped data.

## 📑 Example Usage

```bash
$ python main.py
Scraping data from Trendshift.io...
Saving data to repositories.xlsx...
Done!
Time taken to run the script: 12 seconds
```

## 🛠️ Dependencies

- `requests`
- `beautifulsoup4`
- `openpyxl`

Ensure these are listed in your `requirements.txt` for easy installation.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
