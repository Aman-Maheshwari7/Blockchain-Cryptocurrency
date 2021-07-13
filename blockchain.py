# -*- coding: utf-8 -*-
"""
Created on Wed May 12 12:46:19 2021

@author: Aman Maheshwari

CREATING BLOCKCHAIN
"""

#importing libraries

import datetime
import hashlib
import json
from flask import Flask, jsonify

#Building a blockchain

class Blockchain:
    
    def __init__(self):
        self.chain=[] #initialising a list
        self.create_block(proof=1,previous_hash='0') #Genesis block
        
    def create_block(self,proof,previous_hash):
        block={'index': len(self.chain)+1,
               'timestamp': str(datetime.datetime.now()),
               'proof': proof,
               'previous_hash': previous_hash}
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof=1
        check_proof=False
        while(check_proof==False):
            hash_operation=hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest() #can make complex operation to make mining difficult
            if(hash_operation[0:4]=="0000"):
                check_proof=True
            else:
                check_proof=False
                new_proof+=1
        return new_proof
    
    def hash(self, block):
        encoded_block= json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block=chain[0]
        block_index=1
        while(block_index<len(chain)):
            block=chain[block_index] #current block
            if(block['previous_hash']!=self.hash(previous_block)):
                return False
            previous_proof=previous_block['proof']
            current_proof=block['proof']
            hash_operation=hashlib.sha256(str(current_proof**2-previous_proof**2()).encode()).hexdigest() #can make complex operation to make mining difficult
            if(hash_operation[0:4]!="0000"):
                return False
            previous_block=block
            block_index+=1
        return True
    
    
                   #Mining the blockchain
        
#creating a web app
app=Flask(__name__)
        
    
#creating a blockchain
blockchain=Blockchain() #instance of blockchain class

#Mining a new Block
@app.route('/mine_block', methods=['GET']) #before slash would be whole url addres
def mine_block():
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    block=blockchain.create_block(proof, previous_hash)
    response={'message':'Congratulations, you mined a new block.',
              'index':block['index'],
              'timestamp':block['timestamp'],
              'proof':block['proof'],
              'previous_hash':block['previous_hash']}
    return jsonify(response),200 

#Creating a full blockchaijn

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response={'chain': blockchain.chain,
              'length': len(blockchain.chain)}
    return jsonify(response),200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    chain=blockchain.chain
    result={'result':blockchain.is_chain_valid(chain)}
    return jsonify(result),200
    

#Running the App
app.run(host='0.0.0.0',port=5000)

    
    
            
    
                
    
    
    
    
    
    
    
    
    
    
    
    
        
               
        