# 🎓 Certificate Generator

A Flask web application that automatically generates personalized certificates in PNG and PDF format from a provided certificate template and participant CSV file.

---

## 🚀 Features

* Upload a **certificate template (PNG)** and a **CSV file** with participant data.
* Automatically generate certificates with name, semester, year, and serial number.
* Download generated certificates as **PNG**, **PDF**, or a **ZIP archive**.
* Generates unique serial numbers for verification using SHA-1 hashing.
* Automatically detects CSV encoding (UTF-8, UTF-16, etc.).
* Built-in Bootstrap UI for easy web usage.

---

## 🧩 Tech Stack

* **Flask** (Python web framework)
* **Pandas** (CSV handling)
* **Pillow (PIL)** (Image editing)
* **Chardet** (Encoding detection)
* **Gunicorn** (Production WSGI server for Render)

---

## 🗂️ Folder Structure

```
certificate-generator/
│
├── app.py                 # Main Flask app
├── requirements.txt       # Dependencies
├── Procfile               # Render startup command
├── runtime.txt            # Python version
└── arialbd.TTF            # Font used for text placement
```

---

## ⚙️ Installation (Local Setup)

1. Clone this repository:

   ```bash
   git clone https://github.com/jackchew93/certificate-generator.git
   cd certificate-generator
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app locally:

   ```bash
   python app.py
   ```

4. Open your browser and go to:

   ```
   http://127.0.0.1:5000
   ```

---

## ☁️ Deployment on Render

1. Push your repository to GitHub.

2. Go to [Render.com](https://render.com) → **New Web Service**.

3. Connect your GitHub account.

4. Select `certificate-generator` repository.

5. Use these settings:

   * **Environment:** Python 3
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `gunicorn app:app`

6. Deploy 🚀

---

## 📄 Example CSV Format

| Name       | Matric | Semester | Year |
| ---------- | ------ | -------- | ---- |
| John Doe   | A12345 | 1        | 2024 |
| Jane Smith | A67890 | 2        | 2024 |

---

## 🧠 Notes

* Font file (`arialbd.TTF`) must be included in the project directory.
* Maximum upload size is limited by Render’s free tier (~100 MB).
* Certificates and temporary files are automatically cleaned up after download.

---

## 🛡️ License

MIT License © 2025 Jackel Chew
