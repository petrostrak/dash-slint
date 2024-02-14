import sqlite3

connection = sqlite3.connect("Slint.docset/Contents/Resources/docSet.dsidx")

cursor = connection.cursor()
rows = cursor.execute(
    "SELECT * FROM searchIndex WHERE name='Defun' LIMIT 10").fetchall()
print(rows)