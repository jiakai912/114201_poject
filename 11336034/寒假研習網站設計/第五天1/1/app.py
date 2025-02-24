#-----------------------
# 匯入flask及db模組
#-----------------------
from flask import Flask, render_template

#-----------------------
# **匯入藍圖
#-----------------------
from services.customer import customer_bp

#-----------------------
# 產生一個Flask網站物件
#-----------------------
app = Flask(__name__)

#-------------------------
# **註冊藍圖的服務
#-------------------------
app.register_blueprint(customer_bp, url_prefix='/customer')

#-----------------------
# 設定主畫面路由
#-----------------------
#主畫面
@app.route('/')
def index():
    return render_template('index.html')

#-----------------------
# 啟動Flask網站
#-----------------------
if __name__ == '__main__':
    app.run(debug=True)