from flask import Flask, request, render_template
from mega import Mega
import requests
import os

app = Flask(__name__)

# بيانات حساب MEGA
EMAIL = 'your_email@example.com'
PASSWORD = 'your_password'

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        url = request.form['url']
        if url:
            filename = url.split('/')[-1]
            try:
                # تحميل الملف
                r = requests.get(url, stream=True)
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                # تسجيل الدخول إلى MEGA
                mega = Mega()
                m = mega.login(EMAIL, PASSWORD)

                # رفع الملف
                m.upload(filename)

                # حذف الملف بعد الرفع
                os.remove(filename)

                message = f"تم رفع الملف {filename} بنجاح إلى MEGA."
            except Exception as e:
                message = f"حدث خطأ: {str(e)}"
        else:
            message = "يرجى إدخال رابط مباشر."
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
