from flask import Flask, render_template, request
import db

app = Flask(__name__)

# 客戶清單
@app.route('/customer/list')
def customer_list(): 
    # 每頁顯示 10 筆資料
    page_size = 10
    # 取得當前頁數，預設為第 1 頁
    page = request.args.get('page', 1, type=int)

    # 計算偏移量 (OFFSET)
    offset = (page - 1) * page_size
    
    # 取得資料庫連線
    connection = db.get_connection()
    
    # 產生執行sql命令的物件
    cursor = connection.cursor()
    
    # 執行 SQL 查詢，限制每頁顯示 10 筆資料
    cursor.execute('SELECT cusno, cusname, address, tel FROM customer ORDER BY cusno LIMIT %s OFFSET %s;', (page_size, offset))
    
    # 取回 SQL 執行後的所有資料
    data = cursor.fetchall()
    
    # 設定參數, 準備傳給網頁
    if data:
        params = [{'cusno': d[0], 'cusname': d[1], 'address': d[2], 'tel': d[3]} for d in data]
    else:
        params = None
    
    # 取得資料庫中客戶的總數
    cursor.execute('SELECT COUNT(*) FROM customer;')
    total_records = cursor.fetchone()[0]
    
    # 計算總頁數
    total_pages = (total_records // page_size) + (1 if total_records % page_size > 0 else 0)
    
    # 關閉資料庫連線
    connection.close()
    
    # 傳遞參數到網頁
    return render_template('/customer/list.html', data=params, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)


#-----------------------
# 啟動Flask網站
#-----------------------
if __name__ == '__main__':
    app.run(debug=True)