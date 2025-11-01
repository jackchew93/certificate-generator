# 🎓 Certificate Generator

A Flask web application that automatically generates personalized certificates (PNG & PDF) from a provided certificate template and participant CSV file.
You can deploy this project online for free using [Render](https://render.com).

---

## 🚀 Key Features

* Upload a **certificate template (PNG)** and a **CSV file** with participant information.
* Automatically generate certificates with **Name**, **Semester**, **Year**, and a **unique serial number**.
* Download generated certificates as **PNG**, **PDF**, or a **ZIP** archive.
* Automatically detect CSV encoding (UTF-8, UTF-16, etc.).
* Clean Bootstrap web interface for quick usage.
* Ready to deploy on **Render** in minutes.

---

## 🧩 Tech Stack

* **Flask** – Python web framework
* **Pandas** – CSV handling
* **Pillow (PIL)** – Image editing
* **Chardet** – Encoding detection
* **Gunicorn** – Production WSGI server (for Render)

---

## 🗂️ Folder Structure

```
certificate-generator/
│
├── app.py                 # Main Flask application
├── arialbd.TTF            # Font used for text placement
├── Procfile               # Render startup command
├── requirements.txt       # Python dependencies
├── runtime.txt            # Python version for Render
└── README.md              # Project documentation
```

---

## ⚙️ Run Locally

1. **Clone this repository:**

   ```bash
   git clone https://github.com/jackchew93/certificate-generator.git
   cd certificate-generator
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask app:**

   ```bash
   python app.py
   ```

4. **Open in your browser:**

   ```
   http://127.0.0.1:5000
   ```

---

## ☁️ Deploy on Render (Free Hosting)

Follow these exact steps to host your own version online:

1. **Push the project to your GitHub account**

   ```bash
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/<your-username>/certificate-generator.git
   git push -u origin main
   ```

2. **Go to [Render.com](https://render.com)**

   * Sign up (free) and connect your GitHub account.
   * Click **New + → Web Service**.

3. **Choose your GitHub repository** (`certificate-generator`).

4. **In Render settings, use:**

   * **Environment:** Python 3
   * **Build Command:**

     ```
     pip install -r requirements.txt
     ```
   * **Start Command:**

     ```
     gunicorn app:app
     ```

5. **Deploy 🚀**
   Render will build and launch your app at a public URL such as
   `https://your-app-name.onrender.com/`.

---

## 📄 Example CSV Format

| Name       | Matric | Semester | Year |
| ---------- | ------ | -------- | ---- |
| John Doe   | A12345 | 1        | 2024 |
| Jane Smith | A67890 | 2        | 2024 |

---

## ⚠️ Important Disclaimer

This web app processes uploaded image and CSV files in memory.
If you deploy it publicly or share your Render URL, please remind users **not to upload private or confidential data.**
The service does **not** permanently store any uploaded files or generated certificates, and all files are deleted automatically after generation.

---

## 🧠 Notes

* Keep the `arialbd.TTF` font file inside the same directory as `app.py`.
* Render’s free plan may “sleep” after 15 minutes of inactivity — the first load can be slow.
* Uploaded templates and CSV files are temporarily processed and then cleaned up automatically.
* For private use, you can add a password or token check in Flask (optional).

---

## 🛡️ License

MIT License © 2025 [Jackel Chew](https://github.com/jackchew93)
