# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class ChefaaPipeline:
    """
    Pipeline to process and clean the scraped items.
    """
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        
        # Strip whitespace from all fields except 'url'
        for field in field_names:
            if field != "url":
                value = adapter.get(field)
                adapter[field] = value.strip()
        
        # Extract and convert the price to a float
        price_plus = adapter.get("price")
        price_plus = price_plus.split(" ")
        price = price_plus[0]   
        adapter["price"] = float(price)
        
        return item

class ChefaaToMySQL:
    """
    Pipeline to store the scraped items into a MySQL database.
    """
    def __init__(self):
        # Establish a connection to the MySQL database
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='010010sH',
            database='chefaav2'
        )
        self.curr = self.conn.cursor()
        
        # Create the meds table if it does not exist
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS meds(
                id INT NOT NULL AUTO_INCREMENT, 
                name VARCHAR(255),
                price DECIMAL,
                brand VARCHAR(255),
                prescription VARCHAR(255),
                stock VARCHAR(255),
                category VARCHAR(255),
                url TEXT,
                PRIMARY KEY(id)
            )
        """)
        
    def process_item(self, item, spider):
        # Insert the item into the meds table
        self.curr.execute("""
            INSERT INTO meds
            (
                name,
                price,
                brand,
                prescription,
                stock,
                category,
                url
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            item['name'],
            item['price'],
            item['brand'],
            item['prescription'],
            item['stock'],
            item['category'],
            item['url']
        ))
        self.conn.commit()
        
        return item
        
    def close_spider(self, spider):
        # Close the cursor and connection when the spider is closed
        self.curr.close()
        self.conn.close()