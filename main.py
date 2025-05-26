from flask import Flask, request, jsonify
from mega import Mega
import os

app = Flask(__name__)

# بيانات حساب MEGA (ضع بيانات حسابك هنا)
MEGA_EMAIL = "your_email@example.com"
MEGA_PASSWORD = "your_password"

mega = Mega()
m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)

@app.route("/")
def home():
    return "خدمة رفع الملفات إلى MEGA جاهزة"

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "لم يتم إرسال ملف"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "لم يتم اختيار ملف"}), 400

    try:
        # حفظ الملف مؤقتاً
        filepath = os.path.join("/tmp", file.filename)
        file.save(filepath)

        # رفع الملف إلى MEGA
        upload = m.upload(filepath)

        # حذف الملف المؤقت
        os.remove(filepath)

        return jsonify({"message": "تم رفع الملف بنجاح", "link": upload.get_public_url()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
