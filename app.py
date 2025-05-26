from flask import Flask, request, render_template, redirect, url_for, flash
from mega import Mega
import requests
import os
import tempfile

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # استبدلها بمفتاح سري حقيقي

# بيانات تسجيل الدخول إلى MEGA
MEGA_EMAIL = 'your_mega_email@example.com'
MEGA_PASSWORD = 'your_mega_password'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file_url = request.form.get('file_url')
        if not file_url:
            flash('الرجاء إدخال رابط الملف.')
            return redirect(url_for('index'))

        try:
            # تنزيل الملف مؤقتًا
            response = requests.get(file_url, stream=True)
            response.raise_for_status()
            filename = file_url.split('/')[-1]
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        tmp_file.write(chunk)
                temp_file_path = tmp_file.name

            # تسجيل الدخول إلى MEGA
            mega = Mega()
            m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)

            # رفع الملف
            uploaded_file = m.upload(temp_file_path, dest_filename=filename)
            file_link = m.get_upload_link(uploaded_file)

            # حذف الملف المؤقت
            os.remove(temp_file_path)

            flash(f'تم رفع الملف بنجاح. الرابط: {file_link}')
            return redirect(url_for('index'))

        except Exception as e:
            flash(f'حدث خطأ: {str(e)}')
            return redirect(url_for('index'))

    return render_template('index.html')
