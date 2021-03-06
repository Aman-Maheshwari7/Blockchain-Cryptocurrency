#importing libraries
#request- connecting nodes in a decentralised blockchain

import datetime
import hashlib
import json
from flask import Flask, jsonify,request
import requests
from uuid import uuid4
from urllib.parse import urlparse



#Building a blockchain

class Blockchain:
    
    def __init__(self):
        self.chain=[] #initialising a list
        self.transactions=[]
        self.create_block(proof=1,previous_hash='0') #Genesis block
        self.nodes=set()
        self.orphaned_transactions=[]
        
        
        
        
        
    def create_block(self,proof,previous_hash):
        block={'index': len(self.chain)+1,
               'timestamp': str(datetime.datetime.now()),
               'proof': proof,
               'previous_hash': previous_hash,
               'transaction': self.transactions}
        self.transactions=[]
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
            hash_operation=hashlib.sha256(str(current_proof**2-previous_proof**2).encode()).hexdigest() #can make complex operation to make mining difficult
            if(hash_operation[0:4]!="0000"):
                return False
            previous_block=block
            block_index+=1
        return True
    
    def add_transaction(self, sender,receiver,amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block=self.get_previous_block()
        return previous_block['index']+1  #new block will have index+1 of last block
   
    
    def add_node(self, address):
        parsed_url=urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    def replace_chain(self):
        network=self.nodes
        longest_chain=None
        max_l=len(self.chain)
        flag1=False
        flag2=False
        for nodes in network:
            response=requests.get("http://{}/get_chain".format(nodes))
            if(response.status_code==200):
                length=response.json()['length']
                chain=response.json()['chain']
                
                
                if(length>max_l and self.is_chain_valid(chain)):
                    max_l=length
                    longest_chain=chain
                    flag1=True
                
                if(flag1==True and flag2==False):    
                    for i in self.orphaned_transactions:
                        self.transactions.append(i)
                    self.orphaned_transactions=[]
                    
                #Handling the orphaned Block case to keep the fund transfers safe
                if(len(self.chain)==max_l):
                    last_block=self.chain[-1]
                    last_block_other=chain[-1]
                    if(last_block['transaction']!=last_block_other['transaction']):
                        for i in last_block['transaction']:
                            self.orphaned_transactions.append(i)
                            flag2=True
            
        if(flag1==False and flag2==False):
            self.orphaned_transactions=[]
                    
                    
                            
            
                
                
                
                
        if longest_chain:
            self.chain=longest_chain
            return True
        return False
    
    
                   #Mining the blockchain
        
#creating a web app
app=Flask(__name__)

#creating an address for the node on Port 5000
node_address=str(uuid4()).replace('-','') #uuu\id geberated random addresses


        
    
#creating a blockchain
blockchain=Blockchain() #instance of blockchain class

#Mining a new Block
@app.route('/mine_block', methods=['GET']) #before slash would be whole url addres
def mine_block():
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address,receiver='Bhide',amount=0.5)
    block=blockchain.create_block(proof, previous_hash)
    
    
    response={'message':'Congratulations, you mined a new block.',
              'index':block['index'],
              'timestamp':block['timestamp'],
              'proof':block['proof'],
              'previous_hash':block['previous_hash'],
              'transactions': block['transaction']}
    
    return jsonify(response),200 

#Creating a full blockchaijn

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response={'chain': blockchain.chain,
              'length': len(blockchain.chain)}
    return jsonify(response),200

@app.route('/get_connected_nodes', methods=['GET'])
def get_connected_nodes():
    response={'nodes': blockchain.nodes}
    return jsonify(response),200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    chain=blockchain.chain
    result={'result':blockchain.is_chain_valid(chain)}
    return jsonify(result),200


#Adding a new transaction to the blockchain
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json=request.get_json()
    transaction_keys=['sender','receiver','amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing',400 #400-bad request
    index=blockchain.add_transaction(json['sender'],json['receiver'],json['amount'])
    response={'message': 'This transaction will be added to Block {}'.format(index)}
    
    return jsonify(response),201

#Decentralising our blockchain
    
#connecting new nodes
@app.route('/connect_node', methods=['POST'])
def connect_node():
    json=request.get_json()
    nodes=json.get('nodes')
    if(nodes is None):
        return "No node",400
    for i in nodes:
        blockchain.add_node(i)
    response={'message':'All the nodes are now connected. Anycoin blockchain. ',
              'total nodes': list(blockchain.nodes)}
    return jsonify(response),201

#Replacing the chain by the lngest chain if needed
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced=blockchain.replace_chain()
    if is_chain_replaced:
        response={'message': 'The chain replaced by longest one',
                  'new_chain' : blockchain.chain}
    else:
        response={'message': 'The chain is itself the largest',
                  'actual_chain': blockchain.chain}
    return jsonify(response),200 
        


    
    

#Running the App
app.run(host='0.0.0.0',port=5001)