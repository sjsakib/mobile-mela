 CREATE TABLE items(
    id INTEGER PRIMARY KEY,
    model TEXT,
    brand TEXT,
    type TEXT,
    buyingprice INTEGER,
    count INTEGER
);

CREATE TABLE sales(
    id INTEGER PRIMARY KEY,
    dt INTEGER,
    item_id INTEGER,
    profit INTEGER,
    seller TEXT,
    FOREIGN KEY(item_id) REFERENCES items(id)
);

CREATE TABLE cash (
    id INTEGER PRIMARY KEY,
    dt INTEGER,
    strt INTEGER,
    lst INTEGER
);

CREATE TABLE exp (
    id INTEGER PRIMARY KEY,
    dt INTEGER,
    type TEXT,
    details TEXT,
    amount INTEGER
);

CREATE TABLE due (
    id INTEGER PRIMARY KEY,
    dt1 INTEGER,
    dt2 INTEGER,
    details TEXT,
    amount INTEGER
);

CREATE TABLE brands (
    id INTEGER PRIMARY KEY,
    name TEXT
);