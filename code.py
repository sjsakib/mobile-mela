import web
import json
import sqlite3
from routines import *

urls = (
    '/','index',
    '/addItem','AddItem',
    '/getBrands','getBrands',
    '/getModels','getModels',
    '/getAllItems','getAllItems',
    '/updateItem','updateItem',
    '/deleteItem','deleteItem',
    '/getPrice','getPrice',
    '/recordSell','recordSell',
    '/recordExpense','recordExpense',
    '/getSales','getSales',
    '/getExpenses','getExpenses',
    '/startDay','startDay',
    '/addDue','addDue',
    '/getDueForm','getDueForm',
    '/updateDue','updateDue',
    '/removeDue','removeDue',
    '/addToCash','addToCash',
    '/getDues','getDues',
    '/getCash','getCash',
    '/initCash','initCash'
)

class index:
    def GET(self):
        return "Server running!"

class initCash:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        dt = int(data['dt'])
        amount = data['amount']
        con.execute("""insert into cash values(null,{},{},{})""".format(dt,amount,amount))
        con.commit()

class AddItem:    
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        try:
            add_item(data,con);
        except:
            con = sqlite3.connect("db/mm.db")
            #return "database error"
        return "OK"

class getBrands:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        try:
            return get_brands(con)
        except:
            raise
            #return []

class getModels:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        try:
            return get_models(data,con)
        except:
            raise

class getAllItems:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        try:
            return get_all_items(con)
        except:
            raise

class updateItem:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        try:
            update_item(data,con)
        except:
            raise

class deleteItem:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        con.execute("""delete from items where id={}""".format(int(data['id'])));
        con.commit()

class getPrice:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        cur = con.execute("""select buyingprice from items where brand="{}" and model="{}" """.format(data['brand'],data['model']))
        res = cur.fetchone()
        if(res):
            return res[0]
        else: return "[Not Found]"

class recordSell:
    def POST(self):
        data = web.input()
        con = sqlite3.connect("db/mm.db")
        record_sell(data,con)

class recordExpense:
    def POST(self):
        data = web.input()
        con = sqlite3.connect("db/mm.db")
        record_expense(data,con)

class getSales:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        return get_sales(data,con)

class getExpenses:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        return get_expenses(data,con)

class startDay:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        start_day(data,con)

class addDue:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        add_due(data,con)

class updateDue:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        id = int(data['id'])
        am = int(data['amount'])
        con.execute("""update due set amount={} where id={}""".format(am,id))
        con.commit()

class getDueForm:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        return get_due_form(con)

class removeDue:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        remove_due(data,con)

class addToCash:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        x = int(data['x'])
        add_to_cash(x,con)

class getDues:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        return get_dues(data,con)

class getCash:
    def POST(self):
        con = sqlite3.connect("db/mm.db")
        data = web.input()
        return get_cash(data,con)

if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()