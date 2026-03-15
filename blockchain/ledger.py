import sqlite3
from blockchain.block import Block

DB="database/healthcare.db"

class Blockchain:

    def __init__(self):
        self.chain=[]
        self.load_chain()

    def load_chain(self):
        con=sqlite3.connect(DB)
        cur=con.cursor()
        cur.execute("SELECT * FROM blockchain_ledger ORDER BY id")
        rows=cur.fetchall()
        prev="0"
        for r in rows:
            self.chain.append(Block(r[0],r[1],prev))
            prev=r[2]
        if not self.chain:
            genesis=Block(0,"Genesis","0")
            self.save_block(genesis)

    def save_block(self,block):
        con=sqlite3.connect(DB)
        cur=con.cursor()
        cur.execute("INSERT INTO blockchain_ledger(data,hash,previous_hash) VALUES(?,?,?)",
        (block.data,block.hash,block.previous_hash))
        con.commit()
        con.close()
        self.chain.append(block)

    def add_block(self,data):
        prev=self.chain[-1]
        block=Block(len(self.chain),data,prev.hash)
        self.save_block(block)
