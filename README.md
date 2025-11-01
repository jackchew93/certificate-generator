# 🎓 Certificate Generator Web App

A Flask-based web application for generating personalized certificates automatically from a PNG template and a CSV file.
The app overlays participant details (Name, Matric, Semester, Year) and generates serial numbers automatically, producing both PNG and PDF certificates.
Users can preview certificates online and download all outputs in a single ZIP file.

---

## 🚀 Features

* 🧟‍♂️ Reads participant data from a CSV file.
* 🖼️ Uses a certificate PNG template.
* 🔢 Automatically generates unique serial numbers:

  ```
  FKI-RMC-<Year>-S<Semester>-<Index>-<Hash>
  ```
* 🧾 Exports all certificates in both PNG and PDF formats.
* 📦 Bundles everything into one ZIP file for easy download.
* 🧮 Detects file encoding automatically (UTF-8 or others).
* 💾 Produces a new CSV with verification serials for record keeping.

---

## 🧮 Technologies Used

| Component               | Library      |
| ----------------------- | ------------ |
| Web Framework           | Flask        |
| Data Handling           | Pandas       |
| Image Processing        | Pillow (PIL) |
| Encoding Detection      | Chardet      |
| Web Server (Production) | Gunicorn     |

---

## 📁 Project Structure

```
certificate-generator/
│
├── app.py              # Main Flask app
├── requirements.txt    # Dependencies
├── Procfile            # Render deployment configuration
├── README.md           # Project documentation
└── arialbd.ttf         # Font file (optional)
```

---

## ⚙️ Installation (Local Run)

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/certificate-generator.git
   cd certificate-generator
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Mac/Linux
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**

   ```bash
   python app.py
   ```

5. **Open your browser at**
   👉 [http://localhost:5000](http://localhost:5000)

---

## ☁️ Deployment on Render

1. Push the project to GitHub.
2. Go to [https://render.com](https://render.com) → **New Web Service**.
3. Connect your GitHub repo.
4. Set the following parameters:

   * **Environment:** Python
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `gunicorn app:app`
5. Click **Deploy** and wait 2–4 minutes.
6. Once deployed, you’ll get a public link like:

   ```
   https://certificate-generator.onrender.com
   ```

---

## 🧑‍💻 Author

**Developed by:**
Dr. Jackel Chew Vui Lung
Faculty of Computing and Informatics, Universiti Malaysia Sabah (UMS)

---

## 📜 License

This project is open-source and distributed under the MIT License.
