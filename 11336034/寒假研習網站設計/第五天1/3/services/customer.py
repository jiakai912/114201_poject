#匯入模組
from flask import request, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Blueprint
from utils import db

#產生客戶服務藍圖
customer_bp = Blueprint('customer_bp', __name__)

#----------------------------------
# 清單
# @login_required表示登入後才能使用
#----------------------------------
#客戶清單
@customer_bp.route('/list')
@login_required
def customer_list(): 
    #取得資料庫連線 
    connection = db.get_connection() 
    
    #產生執行sql命令的物件   
    cursor = connection.cursor() 
    
    #執行SQL    
    cursor.execute('SELECT cusno, cusname, address, tel FROM customer order by cusno;')
    
    #取回SQL執行後的所有資料
    data = cursor.fetchall()
    
    #設定參數, 準備傳給網頁
    if data:
        #如果有資料
        params = [{'cusno': d[0], 'cusname': d[1], 'address': d[2], 'tel': d[3]} for d in data]
    else:
        #如果無資料
        params = None
          
    #關閉資料庫連線    
    connection.close() 
    
    #將參數送給網頁, 讓資料嵌入網頁中  
    return render_template('customer/list.html', data=params)

#------------
# 查詢
#------------
#客戶查詢表單
@customer_bp.route('/read/form')
def customer_read_form():
    return render_template('customer/read_form.html') 

#客戶查詢
@customer_bp.route('/read', methods=['GET'])
def customer_read():    
    #取得資料庫連線    
    connection = db.get_connection()  
    
    #取得執行sql命令的cursor
    cursor = connection.cursor()   
    
    #取得傳入參數
    cusno = request.values.get('cusno').strip()
    
    #執行sql命令並取回資料    
    cursor.execute('SELECT * FROM customer WHERE cusno=%s', (cusno,))
    data = cursor.fetchone()

    if data:
        params = {'cusno':data[0], 'cusname':data[1], 'address':data[4], 'tel':data[8]}
    else:
        params = None
        
    #關閉連線   
    connection.close()  
        
    #回傳網頁
    return render_template('customer/read.html', data=params) 

#------------
# 新增
#------------
#客戶新增表單
@customer_bp.route('/create/form')
@login_required
def customer_create_form():
    return render_template('customer/create_form.html') 

#客戶新增
@customer_bp.route('/create', methods=['POST'])
def customer_create():
    try:
        #取得使用者的輸入值
        cusno = request.form.get('cusno').strip()
        cusname = request.form.get('cusname').strip()
        address = request.form.get('address').strip()

        #取得資料庫連線
        conn = db.get_connection()

        #將資料寫入客戶資料表
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customer (cusno, cusname, address) VALUES (%s, %s, %s)", (cusno, cusname, address))
        
        conn.commit()
        conn.close()

        #回傳成功畫面
        return render_template('customer/create.html', success=True)
    except:
        #回傳失敗畫面
        return render_template('customer/create.html', success=False)
     
#------------
# 刪除
#------------
#客戶刪除表單
@customer_bp.route('/delete/form')
def customer_delete_form():
    return render_template('customer/delete_form.html') 

#客戶刪除
@customer_bp.route('/delete', methods=['GET'])
def customer_delete():
    try:
        #取得使用者的輸入值
        cusno = request.values.get('cusno').strip()
        
        #取得資料庫連線
        conn = db.get_connection()

        #刪除客戶資料
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customer WHERE cusno=%s", (cusno,))
        
        #取得刪除的記錄筆數
        deleted_rows = cursor.rowcount  

        conn.commit()
        conn.close()

        if deleted_rows > 0:
            #回傳成功畫面
            return render_template('customer/delete.html', success=True)
        else:
            #回傳失敗畫面
            return render_template('customer/delete.html', success=False)
    except Exception as e:
        print(e)
        #回傳失敗畫面
        return render_template('customer/delete.html', success=False)
       
#------------
# 更改
#------------
#選取客戶
@customer_bp.route('/update/fetch')
def customer_update_fetch():    
    return render_template('customer/update_fetch.html') 

#取出客戶原始資料
@customer_bp.route('/update/form', methods=['GET'])
def customer_update_form(): 
    connection = db.get_connection() 
    cursor = connection.cursor() 
    
    #執行sql命令並取回資料 
    cusno = request.values.get('cusno').strip()       
    cursor.execute('SELECT * FROM customer WHERE cusno=%s', (cusno,))
    data = cursor.fetchone()

    if data:
        params = {'cusno':data[0], 'cusname':data[1], 'address':data[4], 'tel':data[8]}
    else:
        params = None
        
    #關閉連線/回傳網頁   
    connection.close() 
    return render_template('/customer/update_form.html', data=params) 

#更改客戶資料
@customer_bp.route('/update', methods=['POST'])
def customer_update():
    try:
        #取得使用者的輸入值
        cusno = request.form.get('cusno').strip()
        cusname = request.form.get('cusname').strip()
        address = request.form.get('address').strip()

        #取得資料庫連線
        conn = db.get_connection()

        #將資料寫入客戶資料表
        cursor = conn.cursor()
        cursor.execute("UPDATE customer SET cusname=%s, address=%s WHERE cusno=%s", (cusname, address, cusno))
        
        conn.commit()
        conn.close()

        #回傳成功畫面
        return render_template('customer/update.html', success=True)
    except:
        #回傳失敗畫面
        return render_template('customer/update.html', success=False)