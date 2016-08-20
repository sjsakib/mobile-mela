import json
from variables import *
from datetime import datetime

def get_items(con):
    ret = "<h5>Smart:</h5>"
    cur = con.execute("""select brand,sum(count) as cc from items where type="Smartphone" group by brand order by cc desc""")
    res = cur.fetchall()
    for row in res:
        if(row[1]):
            ret+=smarttem.format(row[0],row[1])

    ret+="<h5>Feature:<h5>"
    cur = con.execute("""select brand,sum(count) as cc from items where type="Feature Phone" group by brand order by cc desc""")
    res = cur.fetchall()
    for row in res:
        if(row[1]):
            ret+=featuretem.format(row[0],row[1])
    return ret


def add_to_cash(x,con):
    cur = con.execute("""select max(id) from cash""");
    res = cur.fetchone()
    today = res[0]
    con.execute("""update cash set lst=lst+{} where id={}""".format(x,today))

def add_item(data,con):
    model = data['model']
    brand = data['brand']
    type = data['type']
    buyingprice = int(data['buyingprice'])
    count = int(data['count'])
    date = int(data['dt'])
    fromcash = bool(data['fromcash'])
    print fromcash

    if(fromcash):
        add_to_cash(count*buyingprice*-1,con)
        con.execute("""insert into exp values(null,{},"buying","Buying {} {} {}",{})""".format(date,count,brand,model,count*buyingprice))

    cur = con.cursor()
    cur.execute("""select id from items where brand='{}' and model='{}'""".format(brand,model))
    res = cur.fetchall()
    if(not res):
        cur.execute("""insert into items values(null,'{}','{}','{}',{},{})""".format(model,brand,type,buyingprice,count));
    else:
        print res
        id = res[0][0];
        cur.execute("""update items set count=count+{} where id={}""".format(count,id))
    con.commit()

def update_item(data,con):
    id = data['id']
    brand = data['brand']
    model = data['model']
    type = data['type']
    buyingprice = int(data['buyingprice'])
    count = int(data['count'])

    cur = con.execute("""select buyingprice,count,brand,model from items where id={}""".format(id))
    res = cur.fetchone()
    bpr = res[0]
    c = res[1]
    br = res[2]
    mo = res[3]
    add_to_cash((bpr*c)-(buyingprice*count),con)
    sql = """update exp set amount={}, details="Buying {} {} {}" where details="Buying {} {} {}" """.format(buyingprice*count,count,brand,model,c,br,mo)
    con.execute(sql)
    con.execute("""update items set brand="{}", model="{}", type="{}", buyingprice={}, count={} where id={}""".format(brand,model,type,buyingprice,count,id))
    con.commit()

def get_brands(con):
    cur = con.execute("""select distinct brand from items""")
    res = cur.fetchall()
    if(res):
        l = [r[0] for r in res]
        return json.dumps(l)
    else: return json.dumps([])

def get_models(data,con):
    brand = data['brand']
    cur = con.execute("""select model from items where brand='{}'""".format(brand))
    res = cur.fetchall()
    if(res):
        l = [r[0] for r in res]
        return json.dumps(l)
    else: return json.dumps([])


def get_all_items(con):
    cur = con.execute("select * from items order by count desc")
    data = cur.fetchall()

    ret = ""
    for row in data:
        ret = ret+allitemstem.format(row[0],row[0],row[2],row[1],row[3],row[4],row[5]);
    return ret;

def get_sales_form(data,con):
    t1 = int(data['t1'])
    t2 = int(data['t2'])
    cur = con.execute("select sales.id,sales.dt,items.brand,items.model,items.buyingprice+sales.profit from items inner join sales on sales.item_id=items.id where sales.dt>={} and sales.dt<={}".format(t1,t2))
    data = cur.fetchall()

    ret = ""
    for row in data:
        time = datetime.fromtimestamp(int(row[1])).strftime("%I:%M")
        ret = ret+salesitemstem.format(row[0],row[0],time,row[2],row[3],row[4]);
    return ret;

def update_sales(data,con):
    id = data['id']
    pr = int(data['price'])
    cur = con.execute("""select buyingprice,profit from items inner join sales on sales.item_id=items.id where sales.id={}""".format(id))
    res = cur.fetchone()
    buyingprice = int(res[0])
    profit = int(res[1])
    nPro = pr - buyingprice
    con.execute("""update sales set profit={} where id={}""".format(nPro,id))
    add_to_cash(nPro-profit,con)
    con.commit()

def get_exp_form(data,con):
    t1 = int(data['t1'])
    t2 = int(data['t2'])
    cur = con.execute("select * from exp where dt>={} and dt<={}".format(t1,t2))
    data = cur.fetchall()

    ret = ""
    for row in data:
        ret = ret+expitemstem.format(row[0],row[0],row[3],row[2],row[4]);
    return ret;

def update_exp(data,con):
    id = data['id']
    cur = con.execute("""select amount from exp where id={}""".format(id))
    am = int(cur.fetchone()[0])
    amount = int(data['amount'])
    type = data['type']
    details = data['details']
    add_to_cash(am-amount)
    con.execute("""update exp set amount={},type='{}',details='{}' where id={}""".format(amount,type,details,id))
    con.commit()


def record_sell(data,con):
    brand = data['brand']
    model = data['model']
    profit = int(data['profit'])
    seller = data['seller']
    dt = int(data['dt'])

    cur = con.execute("""select id,buyingprice from items where brand='{}' and model='{}' """.format(brand,model))
    res = cur.fetchall()
    item_id = res[0][0]
    sellingprice = res[0][1]+profit

    add_to_cash(sellingprice,con)

    sql = """insert into sales values(null,{},{},{},"{}")""".format(dt,item_id,profit,seller)
    con.execute(sql)
    con.commit()

def record_expense(data,con):
    details = data['details']
    type = data['type']
    amount = int(data['amount'])
    dt = int(data['dt'])

    sql = """insert into exp values(null,{},"{}","{}",{})""".format(dt,type,details,amount)
    con.execute(sql)
    add_to_cash(amount*-1,con)
    con.commit()

def get_sales(data,con):
    t1 = int(data['t1'])
    t2 = int(data['t2'])

    cur = con.execute("""select * from sales as s inner join items on s.item_id=items.id where s.dt>={} and s.dt<={}""".format(t1,t2))
    res = cur.fetchall()
    ret = ""
    total = 0;
    for row in res:
        time = datetime.fromtimestamp(row[1]).strftime("%I:%M %p")
        price = row[3]+row[9]
        total+=price
        ret+= salestem.format(time,row[7],row[6],price)
    ret+=salestotaltem.format(total)

    return ret

def get_expenses(data,con):
    t1 = int(data['t1'])
    t2 = int(data['t2'])

    cur = con.execute("""select * from exp where dt>={} and dt<={}""".format(t1,t2))
    res = cur.fetchall()
    ret = ""
    total = 0;
    for row in res:
        total+=row[4]
        ret+= exptem.format(row[3],row[4])
    ret+=exptotaltem.format(total)

    return ret

def start_day(data,con):
    day = int(data['day'])
    cur = con.execute("select dt from cash where dt={}".format(day))
    res = cur.fetchall()
    if(not res):
        cur = con.execute("""select lst from cash where id=(select max(id) from cash)""")
        last = int(cur.fetchall()[0][0])
        con.execute("""insert into cash values(null,{},{},{})""".format(day,last,last))
        con.commit()

def add_due(data,con):
    name = data['details']
    amount = int(data['amount'])
    dt = int(data['dt'])
    con.execute("""insert into due values(null,{},null,'{}',{})""".format(dt,name,amount))
    add_to_cash(amount*-1,con)
    con.commit()

def get_due_form(con):
    cur = con.execute("""select id,dt1,details,amount from due where dt2 is null""")
    res = cur.fetchall()
    ret = ""
    for row in res:
        date = datetime.fromtimestamp(row[1]).strftime("%d/%m")
        ret+=dueformtem.format(row[0],date,row[2],row[3])
    return ret

def remove_due(data,con):
    id = int(data['id'])
    date = int(data['date'])
    amount = int(data['amount'])
    add_to_cash(amount,con)
    con.execute("""update due set dt2={} where id={}""".format(date,id))
    con.commit()

def get_dues(data,con):
    t1 = int(data['t1'])
    t2 = int(data['t2'])
    ret = ""
    cur = con.execute("""select details,amount from due where dt1>={} and dt1<={}""".format(t1,t2))
    res = cur.fetchall()

    for row in res:
        ret+=duestem.format("New",row[0],row[1])
    cur = con.execute("""select details,amount from due where dt2 is not null and dt2>={} and dt2<={}""".format(t1,t2))
    res = cur.fetchall()

    for row in res:
        ret+=duestem.format("Finished",row[0],row[1])

    return ret

def get_cash(data,con):
    t1 = int(data['t1'])
    t2 = int(data['t2'])
    cur = con.execute("""select strt,lst from cash where dt>={} and dt<={}""".format(t1,t2))
    res = cur.fetchall()
    print res
    start = res[0][0]
    last = res[0][1]
    totin = 0
    totout = 0
    cur = con.execute("""select items.buyingprice,sales.profit from items inner join sales on sales.item_id=items.id where sales.dt>={} and sales.dt<={}""".format(t1,t2))
    res = cur.fetchall()

    if res:
        for row in res:
            totin+=(row[0]+row[1])
    cur = con.execute("""select amount from due where dt2>={} and dt2<={}""".format(t1,t2))
    res = cur.fetchall()
    if res:
        for row in res:
            totin+=row[0]

    cur = con.execute("""select amount from due where dt1>={} and dt1<={}""".format(t1,t2))
    res = cur.fetchall()
    if res:
        for row in res:
            totout+=row[0]
    cur = con.execute("""select amount from exp where dt>={} and dt<={}""".format(t1,t2))
    res = cur.fetchall()
    if res:
        for row in res:
            totout+=row[0]

    return cashtem.format(start,totin,totout,last)