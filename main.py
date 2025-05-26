from flask import Flask, request, render_template_string
from mega import Mega
import requests
import os

app = Flask(__name__)

# بيانات تسجيل الدخول لحساب MEGA - استبدلها بحسابك
MEGA_EMAIL = 'your_email@example.com'
MEGA_PASSWORD = 'your_password'

@app.route('/', methods=['GET', 'POST'])
def upload_to_mega():
    message = ''
    if request.method == 'POST':
        file_url = request.form.get('file_url')
        if file_url:
            try:
                # تحميل الملف مؤقتاً
                local_filename = file_url.split('/')[-1]
                r = requests.get(file_url, stream=True)
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                # تسجيل الدخول إلى MEGA
                mega = Mega()
                m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)

                # رفع الملف
                m.upload(local_filename)

                # حذف الملف المحلي بعد الرفع
                os.remove(local_filename)

                message = f'تم رفع الملف {local_filename} إلى حساب MEGA بنجاح!'
            except Exception as e:
                message = f'حدث خطأ: {str(e)}'
        else:
            message = 'يرجى إدخال رابط ملف صالح.'

    # واجهة بسيطة جداً
    html = '''
    <h2>رفع ملف إلى MEGA من رابط</h2>
    <form method="post">
      رابط الملف: <input type="text" name="file_url" style="width:300px;" required>
      <button type="submit">ارفع</button>
    </form>
    <p>{{ message }}</p>
    '''
    return render_template_string(html, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
