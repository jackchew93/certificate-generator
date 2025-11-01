from flask import Flask, render_template_string, request, send_file, url_for, send_from_directory
import shutil
from flask import after_this_request
import os, zipfile, tempfile
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import chardet
import hashlib
import io
from datetime import datetime

app = Flask(__name__)
PREVIEW_DIR = None

# ---------------- CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "arialbd.TTF")
EXPORT_PDF = True
DPI_FOR_PDF = 300
GOOGLE_DRIVE_TEMPLATE = "https://drive.google.com/drive/folders/1T2iO8yMe5AWCk1UVTLIC9qWADr1JYqDd?usp=drive_link"
GOOGLE_DRIVE_CSV = "https://drive.google.com/file/d/1hT9AtdlnEiuF9MjX9n1LPvz2evDLYg6H/view?usp=drive_link"

# Define placements for text fields on the certificate
PLACEMENTS = {
    "NAME":     {"xy": ("center", 830), "size": 40},
    "SEMESTER": {"xy": ("center", 1200), "size": 40},
    "YEAR":     {"xy": ("center", 1240), "size": 40},
    "SERIAL":   {"xy": ("right", 45),  "size": 28},
}

# ---------------- HELPERS ----------------
def load_font(path, size):
    try:
        return ImageFont.truetype(path, size=size)
    except OSError:
        return ImageFont.load_default()

def center_x(draw, W, text, font):
    w = draw.textlength(text, font=font)
    return int((W - w) / 2)

def place_text(img, key, value):
    W, H = img.size
    draw = ImageDraw.Draw(img)
    cfg = PLACEMENTS[key]
    font = load_font(FONT_PATH, cfg["size"])

    if isinstance(cfg["xy"][0], str):
        if cfg["xy"][0] == "center":
            w = draw.textlength(value, font=font)
            x = (W - w) // 2
        elif cfg["xy"][0] == "right":
            w = draw.textlength(value, font=font)
            x = W - w - 100  # 100px right margin
    else:
        x = cfg["xy"][0]
    y = cfg["xy"][1]

    draw.text((x, y), value, font=font, fill=(0, 0, 0))

def read_csv_with_fallback(csv_file):
    """Try reading CSV with utf-8, if fail detect encoding with chardet."""
    try:
        return pd.read_csv(csv_file, encoding="utf-8")
    except UnicodeDecodeError:
        # Detect encoding
        with open(csv_file, "rb") as f:
            rawdata = f.read(5000)
            result = chardet.detect(rawdata)
            enc = result["encoding"] or "latin1"   # fallback
        return pd.read_csv(csv_file, encoding=enc, encoding_errors="ignore")

def generate_verification_code(name, matric, semester, year, index):
    """Generate a unique serial number using Name, Matric, Semester, Year, and index."""
    prefix = "FKI-RMC"
    # Combine all identifying info to form a unique string
    base = f"{name}-{matric}-{semester}-{year}-{index}".encode("utf-8")
    # Hash it for uniqueness and verification
    short_hash = hashlib.sha1(base).hexdigest().upper()[:5]  # first 5 chars of hash
    # Format: FKI-RMC-2024-SEM1-001-ABCDE
    return f"{prefix}-{year}-S{semester}-{index:03d}-{short_hash}"

def generate_certificates(template_path, csv_file):
    df = read_csv_with_fallback(csv_file)   # <-- use robust reader
    base = Image.open(template_path).convert("RGB")

    temp_dir = tempfile.mkdtemp()
    generated_pngs = []
    generated_files = []

    for i, row in df.iterrows():
        im = base.copy()

        if "SerialNo" in df.columns:
            serial = str(row["SerialNo"])
        else:
            serial = generate_verification_code(row["Name"], row["Matric"], row["Semester"], row["Year"], i + 1)

        place_text(im, "SERIAL", serial)
        place_text(im, "NAME", str(row["Name"]))
        place_text(im, "SEMESTER", f"Semester {row['Semester']}")
        place_text(im, "YEAR", f"Academic Year {row['Year']}")

        safe_name = "".join(c for c in str(row["Name"]) if c.isalnum() or c in " _-").strip().replace(" ", "_")
        png_path = os.path.join(temp_dir, f"{safe_name}.png")
        im.save(png_path, "PNG")
        generated_pngs.append(png_path)
        generated_files.append(png_path)

        if EXPORT_PDF:
            pdf_path = os.path.join(temp_dir, f"{safe_name}.pdf")
            im.save(pdf_path, "PDF", resolution=DPI_FOR_PDF)
            generated_files.append(pdf_path)

    # --- Create the initial ZIP file with generated certificates ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = os.path.join(temp_dir, f"certificates_{timestamp}.zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in generated_files:
            fname = os.path.basename(f)
            if f.lower().endswith(".png"):
                zf.write(f, arcname=os.path.join("PNG_Certificates", fname))
            elif f.lower().endswith(".pdf"):
                zf.write(f, arcname=os.path.join("PDF_Certificates", fname))

    # --- Save verification log (updated CSV with serial numbers) ---
    df["VerificationSerial"] = [
    generate_verification_code(row["Name"], row["Matric"], row["Semester"], row["Year"], i + 1)
    for i, row in df.iterrows()
    ]
    updated_csv_path = os.path.join(temp_dir, "updated_with_serial.csv")
    df.to_csv(updated_csv_path, index=False)

    # Add updated CSV to the existing ZIP
    with zipfile.ZipFile(zip_path, "a", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(updated_csv_path, arcname="updated_with_serial.csv")

    # Return the updated CSV path as well
    return generated_pngs, zip_path, temp_dir, updated_csv_path

# ---------------- ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        template = request.files["template"]
        csv_file = request.files["csv"]

        template_path = os.path.join(tempfile.mkdtemp(), template.filename)
        csv_path = os.path.join(tempfile.mkdtemp(), csv_file.filename)
        template.save(template_path)
        csv_file.save(csv_path)

        pngs, zip_path, temp_dir, updated_csv_path = generate_certificates(template_path, csv_path)
        global PREVIEW_DIR
        PREVIEW_DIR = temp_dir

        previews_html = "<div style='display:flex; flex-wrap:wrap;'>"
        for p in pngs:
            fname = os.path.basename(p)
            base, _ = os.path.splitext(fname)  # e.g. "WANG_ZHANG"

            previews_html += f"""
            <div style="flex: 1 0 20%; box-sizing:border-box; padding:10px; text-align:center;">
                <img src="{url_for('preview_file', filename=fname)}" width="250"><br>
                <b>{base}</b><br>
                <a href="{url_for('download_cert', filename=fname)}">
                    <button>Download PNG</button>
                </a>
            """

            if EXPORT_PDF:  # add PDF button if enabled
                previews_html += f"""
                <a href="{url_for('download_cert', filename=base + '.pdf')}">
                    <button>Download PDF</button>
                </a>
                """

            previews_html += "</div>"
        previews_html += "</div>"

        return render_template_string(f"""
            <style>
                button {{
                    margin: 10px;
                }}
            </style>
            <h2 class="text-center">Preview Certificates</h2>
            {previews_html}
            <br><br>
            <div style="text-align:center;">
                <a href="/download_updated_csv?path={updated_csv_path}">
                    <button class="btn btn-success btn-lg">📄 Download Updated CSV (with Verification Serial)</button>
                </a>
                &nbsp;&nbsp;
                <a href="/download?path={zip_path}">
                    <button class="btn btn-primary btn-lg">📦 Download All Certificates (ZIP)</button>
                </a>
            </div>
        """)

    return render_template_string("""
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Certificate Generator</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">

    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card shadow-lg border-0 rounded-4">
                    <div class="card-body p-5">
                        <h2 class="text-center mb-4">🎓 Certificate Generator</h2>
                        <p class="text-center text-muted">
                            Upload a certificate template and a CSV file to generate personalised certificates.
                        </p>

                        <div class="text-center mb-4">
                            <a href="{{ template_link }}" target="_blank" class="btn btn-outline-primary m-2">
                                📄 View Example Certificate Template (Google Drive)
                            </a>
                            <a href="{{ csv_link }}" target="_blank" class="btn btn-outline-success m-2">
                                🧾 View Example CSV File (Google Drive)
                            </a>
                        </div>

                        <form method="POST" enctype="multipart/form-data">
                            <div class="mb-3">
                                <label class="form-label">Upload Certificate Template (PNG):</label>
                                <input type="file" name="template" accept="image/png" class="form-control" required>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Upload CSV File:</label>
                                <input type="file" name="csv" accept=".csv" class="form-control" required>
                            </div>
                            
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary btn-lg">🚀 Generate Certificates</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>

    </body>
    </html>
    """, template_link=GOOGLE_DRIVE_TEMPLATE, csv_link=GOOGLE_DRIVE_CSV)

@app.route("/preview/<filename>")
def preview_file(filename):
    return send_from_directory(PREVIEW_DIR, filename)

@app.route("/download_cert/<filename>")
def download_cert(filename):
    return send_from_directory(PREVIEW_DIR, filename, as_attachment=True)

@app.route("/download")
def download():
    zip_path = request.args.get("path")

    if not zip_path or not os.path.exists(zip_path):
        return "File not found", 404

    temp_dir = os.path.dirname(zip_path)

    @after_this_request
    def cleanup(response):
        try:
            shutil.rmtree(temp_dir)  # Remove all temporary files and folders
            print(f"Cleaned up: {temp_dir}")
        except Exception as e:
            print(f"Cleanup failed: {e}")
        return response

    return send_file(zip_path, as_attachment=True, download_name="certificates.zip")

@app.route("/download_updated_csv")
def download_updated_csv():
    csv_path = request.args.get("path")

    if not csv_path or not os.path.exists(csv_path):
        return "File not found", 404

    temp_dir = os.path.dirname(csv_path)

    @after_this_request
    def cleanup(response):
        try:
            shutil.rmtree(temp_dir)
            print(f"Cleaned up: {temp_dir}")
        except Exception as e:
            print(f"Cleanup failed: {e}")
        return response

    return send_file(csv_path, as_attachment=True, download_name="updated_with_serial.csv")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
