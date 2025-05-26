from flask import Flask, request, jsonify
from mega import Mega
import os

app = Flask(__name__)

# بيانات حسابك في MEGA
MEGA_EMAIL = "your_email@example.com"
MEGA_PASSWORD = "your_password"

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
        # حفظ الملف مؤقتًا
        filepath = os.path.join("/tmp", file.filename)
        file.save(filepath)

        # تسجيل الدخول ورفع الملف
        mega = Mega()
        m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)
        uploaded_file = m.upload(filepath)

        # حذف الملف المحلي
        os.remove(filepath)

        # الحصول على رابط مشاركة الملف
        public_url = m.get_upload_link(uploaded_file)

        return jsonify({"message": "تم رفع الملف بنجاح", "link": public_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
