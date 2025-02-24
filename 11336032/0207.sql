-- 創建數據庫 'school'
CREATE DATABASE school;

-- 使用 'school' 數據庫
USE school;

-- 創建學生表格 'students'，包含學生編號和姓名
CREATE TABLE students (
    student_id INT PRIMARY KEY,          -- 學生編號，作為主鍵
    student_name VARCHAR(50) NOT NULL    -- 學生姓名，不能為空
);

-- 創建課程表格 'courses'，包含課程代號、課程名稱、授課老師、上課時間和地點
CREATE TABLE courses (
    course_code INT PRIMARY KEY,         -- 課程代號，作為主鍵
    course_name VARCHAR(50) NOT NULL,    -- 課程名稱，不能為空
    instructor VARCHAR(50) NOT NULL,     -- 授課老師，不能為空
    class_time VARCHAR(50),              -- 上課時間
    class_location VARCHAR(50)           -- 上課地點
);


-- 創建選課關聯表格 'course_selection'，表示學生與課程之間的多對多關係
CREATE TABLE course_selection (
    student_id INT,                      -- 學生編號，外鍵，參照 'students' 表
    course_code INT,                     -- 課程代號，外鍵，參照 'courses' 表
    PRIMARY KEY (student_id, course_code), -- 主鍵由學生編號和課程代號組成
    FOREIGN KEY (student_id) REFERENCES students(student_id),  -- 設置外鍵關聯到 'students' 表
    FOREIGN KEY (course_code) REFERENCES courses(course_code)  -- 設置外鍵關聯到 'courses' 表
);


-- 創建成績表格 'grades'，記錄學生在課程中的成績
CREATE TABLE grades (
    student_id INT,                      -- 學生編號，外鍵，參照 'students' 表
    course_code INT,                     -- 課程代號，外鍵，參照 'courses' 表
    grade INT,                           -- 學生成績
    PRIMARY KEY (student_id, course_code), -- 主鍵由學生編號和課程代號組成
    FOREIGN KEY (student_id) REFERENCES students(student_id),  -- 設置外鍵關聯到 'students' 表
    FOREIGN KEY (course_code) REFERENCES courses(course_code)  -- 設置外鍵關聯到 'courses' 表
);

-- 插入學生數據到 'students' 表
INSERT INTO students (student_id, student_name) VALUES
(123456, '張小明'),
(234567, '李美麗'),
(345678, '王大華'),
(456789, '蔡婷婷'),
(567890, '陳建國');

-- 插入課程數據到 'courses' 表
INSERT INTO courses (course_code, course_name, instructor, class_time, class_location) VALUES
(101, '數學基礎', '張老師', '08:00-10:00', 'A教室'),
(102, '英文閱讀', '李老師', '10:00-12:00', 'B教室'),
(103, '物理實驗', '王老師', '13:00-15:00', 'C教室'),
(104, '化學概論', '蔡老師', '15:00-17:00', 'D教室'),
(105, '資訊導論', '陳老師', '17:00-19:00', 'E教室');

-- 插入學生選課數據到 'course_selection' 表
INSERT INTO course_selection (student_id, course_code) VALUES
(123456, 101),   -- 張小明 選修 數學基礎
(123456, 103),   -- 張小明 選修 物理實驗
(234567, 102),   -- 李美麗 選修 英文閱讀
(234567, 105),   -- 李美麗 選修 資訊導論
(345678, 104),   -- 王大華 選修 化學概論
(345678, 102),   -- 王大華 選修 英文閱讀
(456789, 101),   -- 蔡婷婷 選修 數學基礎
(456789, 105),   -- 蔡婷婷 選修 資訊導論
(567890, 103),   -- 陳建國 選修 物理實驗
(567890, 104);   -- 陳建國 選修 化學概論

-- 插入學生成績數據到 'grades' 表
INSERT INTO grades (student_id, course_code, grade) VALUES
(123456, 101, 85),   -- 張小明 數學基礎 成績 85
(123456, 103, 92),   -- 張小明 物理實驗 成績 92
(234567, 102, 88),   -- 李美麗 英文閱讀 成績 88
(234567, 105, 90),   -- 李美麗 資訊導論 成績 90
(345678, 104, 78),   -- 王大華 化學概論 成績 78
(345678, 102, 80),   -- 王大華 英文閱讀 成績 80
(456789, 101, 91),   -- 蔡婷婷 數學基礎 成績 91
(456789, 105, 89),   -- 蔡婷婷 資訊導論 成績 89
(567890, 103, 95),   -- 陳建國 物理實驗 成績 95
(567890, 104, 83);   -- 陳建國 化學概論 成績 83

--------------------------------------------------------------------

 
-- 查詢所有學生資訊
SELECT * FROM students;


-- 查詢所有學生選修的課程
SELECT students.student_name, courses.course_name
FROM students
JOIN course_selection ON students.student_id = course_selection.student_id
JOIN courses ON course_selection.course_code = courses.course_code;


-- 查詢某位特定學生的選課情況
SELECT students.student_name, courses.course_name
FROM students
JOIN course_selection ON students.student_id = course_selection.student_id
JOIN courses ON course_selection.course_code = courses.course_code
WHERE students.student_name = '李美麗';


--  查詢所有課程的平均成績
SELECT courses.course_name, AVG(grades.grade) AS average_grade
FROM grades
JOIN courses ON grades.course_code = courses.course_code
GROUP BY courses.course_name;









