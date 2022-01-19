'''
Shopify Backend Developer Intern 
Challenge - Summer 2022
'''

from os import error
import sqlite3
import sys

connection = sqlite3.connect('inventory.db')
c = connection.cursor()


def table_exists(table_name):
    c.execute(
        "SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = '{}' ".format(table_name))
    if c.fetchone()[0] == 1:
        return True
    return False


def main_menu():
    print("\n")
    print("   === Your Super Special Inventory ===    ")
    print("-------------------------------------------")
    print("| 1. Create Item    | 2.   Update Item    |")
    print("-------------------------------------------")
    print("-------------------------------------------")
    print("| 3.  Delete Item   | 4.   View Items     |")
    print("-------------------------------------------")
    print("-------------------------------------------")
    print("| 5.  View Category | 6.       Exit       |")
    print("-------------------------------------------")

    q = input('What would you like to do? ')
    if q == '1':
        create_item()
    elif q == '2':
        update_item()
    elif q == '3':
        delete_item()
    elif q == '4':
        show_inventory()
    elif q == '5':
        show_category()
    elif q == '6':
        sys.exit("Closing inventory...")
    else:
        print('Invalid Option')


def create_item():
    item_name = input("Enter the name of your product: ")
    item_id = input("Enter the unique ID of your product: ")
    item_category = input("Enter the category of your product: ")
    item_price = input("Input the price of your product: ")
    params = (item_name, item_id, item_category, item_price)
    c.execute("INSERT INTO inventory VALUES (?, ?, ?, ?)", (params))
    connection.commit()
    c.close()


def update_item():
    show_inventory()

    change = input("Enter ID of item you would like to change: ")
    print("Retrieving data...\n")
    get_item(change)

    print(
        f'Item Name: {change[0]}  |  Item Category: {change[2]}  |  Item Price: {change[3]}')

    to_change = input(
        "Which of the following would you like to update?\n1) Item Name | 2) Item Category | 3) Item Price\n")
    new_val = input("Enter the new value you would like: ")

    if(to_change == '1'):
        sql = "UPDATE inventory SET item_name = ? WHERE item_id = ?"
    elif(to_change == '2'):
        sql = "UPDATE inventory SET item_category = ? where item_id = ?"
    elif(to_change == '3'):
        sql = "UPDATE inventory SET item_price = ? where item_id = ?"

    try:
        connection.execute(sql, (str(new_val), str(change)))
        connection.commit()
        print("Item successfully updated!")
    except error as e:
        print(e)
        pass


def get_item(item_id):
    c.execute("SELECT * FROM inventory WHERE item_id = '{}'".format(item_id))
    item = []
    for row in c.fetchall():
        item.append(row)
    print(item)
    return item


def delete_item():
    trash = input("ID of item you are deleting: ")
    try:
        sql = "DELETE FROM inventory WHERE item_id =?"
        connection.execute(sql, (str(trash)))
        connection.commit()
        print("Delete Successful!")
    except NameError as e:
        print(e)
        pass


def show_inventory():
    c.execute("SELECT * FROM inventory")
    for row in c.fetchall():
        print(
            f'Item: {row[0]} | ID: {row[1]} | Category: {row[2]} | Price: {row[3]}')


def show_category():
    cat = input("Choose item category: ")
    c.execute(
        "SELECT * FROM inventory WHERE item_category = '{}'".format(cat))
    for row in c.fetchall():
        print(
            f'Item: {row[0]} | ID: {row[1]} | Category: {row[2]} | Price: {row[3]}')


if not table_exists('inventory'):
    c.execute('''
        CREATE TABLE inventory(
            item_name STRING,
            item_id STRING,
            item_category STRING,
            item_price FLOAT
        )
    ''')

while True:
    main_menu()
