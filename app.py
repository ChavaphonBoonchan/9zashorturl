from flask import Flask, request, jsonify, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import random
import string
import os

app = Flask(__name__)

# ตั้งค่า SQLAlchemy เพื่อใช้ SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'urls.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# โมเดลฐานข้อมูลสำหรับเก็บ URL
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, long_url, short_url):
        self.long_url = long_url
        self.short_url = short_url

# ฟังก์ชันสร้างลิงก์สั้น
def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# สร้างตารางฐานข้อมูล
@app.before_first_request
def create_tables():
    db.create_all()

# เส้นทางสำหรับหน้าแรก
@app.route('/')
def home():
    return render_template('index.html')  # เรียกหน้า index.html ที่อยู่ในโฟลเดอร์ templates

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    long_url = data.get('longUrl')

    # ตรวจสอบว่าลิงก์นี้เคยถูกย่อแล้วหรือไม่
    existing_url = URL.query.filter_by(long_url=long_url).first()
    if existing_url:
        return jsonify({'shortUrl': f"http://localhost:5000/{existing_url.short_url}"}), 200

    # สร้างลิงก์สั้นและเก็บข้อมูลในฐานข้อมูล
    short_url = generate_short_url()
    new_url = URL(long_url=long_url, short_url=short_url)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({'shortUrl': f"http://localhost:5000/{short_url}"}), 200

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first()
    if url:
        return redirect(url.long_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
