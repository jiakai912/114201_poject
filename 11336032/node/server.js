const express = require('express');
const app = express();

// 設定伺服器監聽的埠號
const PORT = process.env.PORT || 3000;

// 設置靜態文件夾 (如 HTML、CSS、JS)
app.use(express.static('public'));

// 設置首頁
app.get('/', (req, res) => {
    res.send('Welcome to the School Website!');
});

// 設置關於我們頁面
app.get('/about', (req, res) => {
    res.send('About Our School');
});

// 設置聯絡我們頁面
app.get('/contact', (req, res) => {
    res.send('Contact Us');
});

// 啟動伺服器
app.listen(PORT, () => {
    console.log(`School website running on http://localhost:${PORT}`);
});
