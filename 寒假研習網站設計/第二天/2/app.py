#-----------------------
# 匯入Flask類別
#-----------------------
from flask import Flask, render_template

#-----------------------
# 產生Flask物件
#-----------------------
app = Flask(__name__)

#-----------------------
# 定義路由
#-----------------------
#主畫面
@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/customer/list')
def list():
    return render_template('list.html') 
#-----------------------
# 執行Flask網站
#-----------------------
if __name__ == '__main__':
    app.run(debug=True)