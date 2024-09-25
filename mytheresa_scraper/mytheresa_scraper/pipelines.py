import sqlite3

class MytheresaPipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('mytheresa.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                name TEXT,
                price TEXT,
                brand TEXT,
                description TEXT,
                size TEXT,
                color TEXT
            )
        ''')

    def close_spider(self, spider):
        self.connection.commit()
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT INTO products (name, price, brand, description, size, color)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            item['name'],
            item['price'],
            item['brand'],
            item['description'],
            ','.join(item['size']),
            item['color']
        ))
        return item
