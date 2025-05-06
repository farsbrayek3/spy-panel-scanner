# Mr Spy's Ultimate Panel Scanner

![kawaii-banner](https://user-images.githubusercontent.com/your-banner-path/banner.png)

## 🕵️‍♂️ Kawaii Mode Activated!

Mr Spy's Ultimate Panel Scanner is a powerful, fast and fun tool for scanning, extracting, and checking various types of panel and SMTP credentials from text files. With a dash of anime style, it helps you find cPanel, Webmail, WordPress, WHM, and SMTP panels efficiently, then validate access to them — all from your terminal!

---

## ✨ Features

- **Anime-Style Banner:** Every scan starts with kawaii encouragement!
- **Extractors:** Finds and saves URLs for:
  - cPanel
  - Webmail
  - WordPress
  - WHM
  - SMTP credentials (`smtp://host:user:pass`)
- **Checkers:** Validates credentials for:
  - cPanel
  - Webmail
  - WordPress
  - WHM (panel up)
  - SMTP (login test with multiple ports)
- **Multi-threaded:** Fast scanning and checking!
- **Result Files:** Saves valid and invalid credentials in `Results/` directory.
- **Colorful CLI:** Clear status with color-coded output.

---

## 🛠️ Installation

1. **Clone this repo:**

   ```bash
   git clone https://github.com/yourusername/spy-panel-scanner.git
   cd spy-panel-scanner
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   > Requirements:
   >
   > - Python 3.x
   > - `requests`, `colorama`, `urllib3`

3. **(Optional) Add more User-Agents:**  
   Edit or add to `lib/ua.txt` for random UA rotation.

---

## 🚀 Usage

1. **Run the tool:**

   ```bash
   python main.py
   ```

2. **Choose what you want to do from the menu:**

   - Extract panel URLs or SMTP lines from your `.txt` files.
   - Check credentials for validity.
   - Extract all types at once.
   - Results will be saved in `Results/` (e.g., `cpanels_valid.txt`, `smtps_invalid.txt`, ...).

3. **Panel extraction works on any `.txt` file in the folder** (except output files).

---

## 📝 Input Formats

- **cPanel:** `http(s)://site:2082|username|password`
- **Webmail:** `http(s)://site:2095|username|password`
- **WordPress:** `http(s)://site|username|password`
- **WHM:** `http(s)://site:2086`
- **SMTP:** `smtp://host:username:password`
  - Tool will try ports 587, 465, and 25.

---

## 📁 Output Files

- Extracted panel URLs:
  - `cpanels.txt`, `webmails.txt`, `wordpress.txt`, `whms.txt`, `smtps.txt`
- Results (inside `Results/`):
  - For each type: `*_valid.txt`, `*_invalid.txt`

---

## 🖼️ Example Run

```shell
$ python main.py

────────────────────────────────────────────────────
   Mr Spy's Ultimate Panel Scanner: Kawaii Mode Activated!
────────────────────────────────────────────────────
  Scan, check, and hack with style – Stay stealthy, agent!

Select an option:
1. Extract cPanel URLs Only
...
12. Exit

Enter your choice (1-12): 6
[!] Working in file: combos.txt [cPanel]
[+] Scraped line in combos.txt (line 5): https://example.com:2083
[✔] Extracted cPanel URLs have been saved to cpanels.txt
```

---

## ⚡ Tips

- **Add your combos or dumps as `.txt` files in the folder.**
- **The app skips lines with `localhost` for WordPress extractions.**
- **SMTP output format is the same as input, making it easy to re-use.**

---

## ⚠️ Disclaimer

This tool is for **educational, research, and authorized testing purposes only**.  
Do **not** use it to access systems or accounts you do not own or have explicit permission to test.

---

## 💡 Credits

- Built by [YourName or Team]
- ASCII art inspired by the anime community
- Open Source: [LICENSE](LICENSE)
