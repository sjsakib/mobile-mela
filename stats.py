from variables import *
import json

def get_stats_table(data,con):
    t1 = int(data['t1'])
    t2 = int(data['t2'])

    cur = con.execute("""select sum(buyingprice+profit),sum(profit) 
        from items inner join sales on sales.item_id=items.id 
        where dt>={} and dt<={}""".format(t1,t2))
    res = cur.fetchone()
    print res
    if(res and len(res) == 2 and res[0] and res[1]):
        totalsold = res[0]
        totalprofit = res[1]
    else:
        totalsold = 0;
        totalprofit = 0;
    cur = con.execute("""select sum(amount) from exp 
        where dt>={} and dt<={} and type="buying" """.format(t1,t2))
    res = cur.fetchone()
    print res
    if(res and res[0]):
        bexp = res[0]
    else:
        bexp = 0
    cur = con.execute("""select sum(amount) from exp
        where dt>={} and dt<={} and type!="buying" and type!="withdraw" """.format(t1,t2))
    res = cur.fetchone()
    print res
    if(res and res[0]):
        exp = res[0]
    else:
        exp = 0
    cur = con.execute("""select sum(amount) from exp
        where dt>={} and dt<={} and type="withdraw" """.format(t1,t2))
    res = cur.fetchone()
    print res
    if(res and res[0]):
        withdraw = res[0]
    else:
        withdraw = 0
    return stattabletem.format(totalsold,bexp,exp,bexp+exp,totalprofit-exp,withdraw)



def get_stats(data,con):
    t1 = int(data['t1'])
    t2 = int(data['t2'])
    cur = con.execute("""select sum(buyingprice+profit),sum(profit) 
        from items inner join sales on sales.item_id=items.id 
        where dt>={} and dt<={}""".format(t1,t2))
    res = cur.fetchone()
    if(res and res[0]):
        totalprofit = res[1]
    else:
        totalprofit = 0;
    cur = con.execute("""select sum(amount) from exp
        where dt>={} and dt<={} and type!="buying" and type!="withdraw" """.format(t1,t2))
    res = cur.fetchone()
    if(res and res[0]):
        exp = res[0]
    else:
        exp = 0
    avexp = exp/((t2-t1)/86400)

    ret = {}
    ret['proTime'] = []

    t11 = t1;
    t22 = t1+86399

    while(t22 <= t2):
        cur = con.execute("""select sum(profit) 
        from items inner join sales on sales.item_id=items.id 
        where dt>={} and dt<={}""".format(t11,t22))
        pr = cur.fetchone()[0]
        if(not pr): pr = 0
        pr -= avexp
        ret['proTime'].append({'dt':t11,'profit':pr})
        t11+=86400
        t22+=86400

    ret['byBrand'] = []
    cur = con.execute("""select brand,sum(profit) 
        from items inner join sales on sales.item_id=items.id 
        where dt>={} and dt<={} group by brand""".format(t1,t2))
    res = cur.fetchall()
    for row in res:
        ret['byBrand'].append({'y':row[1],'indexLabel':row[0]})


    ret['byType'] = []
    cur = con.execute("""select type,sum(profit) 
        from items inner join sales on sales.item_id=items.id 
        where dt>={} and dt<={} group by type""".format(t1,t2))
    res = cur.fetchall()
    for row in res:
        ret['byType'].append({'y':row[1],'indexLabel':row[0]})


    return json.dumps(ret)

def get_sales_graph(data,con):
    t1 = int(data['t1'])
    t2 = int(data['t2'])

    ret = []

    t11 = t1;
    t22 = t1+86399
    while(t22 <= t2):
        cur = con.execute("""select sum(buyingprice+profit) 
        from items inner join sales on sales.item_id=items.id 
        where dt>={} and dt<={}""".format(t11,t22))
        pr = cur.fetchone()[0]
        if(not pr): ret.append({'dt':t11,'sales': 0,'open':False})
        else: ret.append({'dt':t11,'sales':pr,'open':True})
        t11+=86400
        t22+=86400
    return json.dumps(ret)