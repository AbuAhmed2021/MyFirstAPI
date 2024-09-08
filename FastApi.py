from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()
#-----------------
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#-----------------
class CustomersML(BaseModel):
    custID:             int = None 
    custNameAr:         str
    custNameEn:         str
    custAddressAr:      str
    custAddressEn:      str
    custTelMob:         str
    custCR:             str
    custTaxNo:          str
    custEmail:          str
    custShortName:      str

def setup_database():
    try:
        conn = sqlite3.connect("aminaDB.db")
        cursor = conn.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Customers(
                    custID             INTEGER PRIMARY KEY,
                    custNameAr         TEXT,
                    custNameEn         TEXT,
                    custAddressAr      TEXT,
                    custAddressEn      TEXT,
                    custTelMob         TEXT,
                    custCR             TEXT,
                    custTaxNo          TEXT,
                    custEmail          TEXT,
                    custShortName      TEXT
                )
               ''')
        conn.commit()

        # Invoices Table
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Invoices(
                    InvoiceID          TEXT PRIMARY KEY,
                    dateFrom           DATE NOT NULL,
                    dateTo             DATE NOT NULL,
                    invoDate           DATE NOT NULL,
                    invoTotal          DICEMAL,
                    invoVat            DICEMAL,
                    invoDisc           DICEMAL,
                    invoTotalAfterVat  DICEMAL,
                    customerID         INTEGER,
                    notes              TEXT
                )
               ''')
        conn.commit()

        # Customer_Sites Table
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Sites(
                    siteID             INTEGER PRIMARY KEY,
                    siteAr             TEXT,
                    siteEn             TEXT,
                    unitPrice          DICEMAL,
                    custID             INTEGER,
                    FOREIGN KEY (custID) REFERENCES Customers(custID)
                )
               ''')
        conn.commit()

        # Invoice Details Table
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS InvoiceDetails(
                    invoDetailsID      INTEGER PRIMARY KEY,
                    invoiceID          TEXT,
                    siteID             INTEGER,
                    qty                INTEGER,
                    unit               TEXT,
                    discount           DICEMAL,
                    total              DICEMAL,
                    vat                DICEMAL,
                    totalAfterVat      DICEMAL,
                    stamp              TEXT,
                    FOREIGN KEY (invoiceID) REFERENCES Invoices(InvoiceID),
                    FOREIGN KEY (siteID) REFERENCES Sites(siteID)
                )
               ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database setup error:{e}")

setup_database()

@app.get("/Customers/")
async def read_Customers():
    try:
        conn = sqlite3.connect("aminaDB.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customers")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print(e)
        return{"error": "Failed to fetch Customers"}

@app.post("/Customers/")
async def create_Customer(cust:CustomersML):
    try:
        conn = sqlite3.connect("aminaDB.db")
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Customers
        (custNameAr,custNameEn,custAddressAr,custAddressEn,custTelMob,custCR,custTaxNo,custEmail,custShortName)
        values
        (?,?,?,?,?,?,?,?,?)''',(cust.custNameAr,cust.custNameEn,cust.custAddressAr,cust.custAddressEn,
                                cust.custTelMob,cust.custCR,cust.custTaxNo,cust.custEmail,cust.custShortName))
        conn.commit()
        conn.close()
        return{"message": "Student added successfully"}
    except sqlite3.Error as e:
        print(e)
        return{"error": "Failed to create Customer"}

@app.put("/Customers/{custID}")
async def update_Customer(cust_id:int, cust:CustomersML):
    try:
        conn = sqlite3.connect("aminaDB.db")
        cursor = conn.cursor()
        cursor.execute(''' UPDATE Customers SET
        custNameAr=?,custNameEn=?,custAddressAr=?,custAddressEn=?,custTelMob=?,custCR=?,custTaxNo=?,custEmail=?,custShortName=?''',
        (cust.custNameAr,cust.custNameEn,cust.custAddressAr,cust.custAddressEn,cust.custTelMob,cust.custCR,cust.custTaxNo,cust.custEmail,cust.custShortName))
        conn.commit()
        conn.close()
        return{"id":cust_id,**cust.dict()}
    except sqlite3.Error as e:
        print(e)
        return{"error": "Failed to update Customer"}

@app.delete("/Customers/{custID}")
async def update_Customer(cust_id:int, cust:CustomersML):
    try:
        conn = sqlite3.connect("aminaDB.db")
        cursor = conn.cursor()
        cursor.execute(" DELETE FROM Customers WHERE custID = ?" ,(cust_id,))
        conn.commit()
        conn.close()
        return{"Message":"Customer Deleted"}
    except sqlite3.Error as e:
        print(e)
        return{"error": "Failed to delete Customer"}

