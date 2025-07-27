import datetime, hashlib, json
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        self.chain = []
        self.createBlock(proof = 1, previousHash = '0')
        
    def createBlock(self, proof, previousHash):
        block = { 'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previousHash': previousHash
            }
        self.chain.append(block)
        
        return block
    
    def getPreviousBlock(self):
        return self.chain[-1]
    
    def proofOfWork(self, previousProof):
        newProof = 1
        checkProof = False
        
        while checkProof is False:
            hashOperation = hashlib.sha256(str(newProof**2 - previousProof**2).encode()).hexdigest()
            if hashOperation[:4] == '0000':
                checkProof = True
            else:
                newProof += 1
                
        return newProof
    
    def hash(self, block):
        encodedBlock = json.dumps(block, sort_keys = True).encode()
        
        return hashlib.sha256(encodedBlock).hexdigest()
    
    def isChainValid(self, chain):
        previousBlock = chain[0]
        blockIndex = 1
        
        while blockIndex < len(chain):
            block = chain[blockIndex]
            if block['previousHash'] != self.hash(previousBlock):
                return False
            previousProof = previousBlock['proof']
            proof = block['proof']
            hashOperation = hashlib.sha256(str(proof**2 - previousProof**2).encode()).hexdigest()
            if hashOperation[:4] != '0000':
                return False
            previousBlock = block
            blockIndex += 1
            
        return True
    
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

blockchain = Blockchain()

@app.route('/mine_block', methods = ['GET'])
def mineBlock():
    previousBlock = blockchain.getPreviousBlock()
    previousProof = previousBlock['proof']
    proof = blockchain.proofOfWork(previousProof)
    previousHash = blockchain.hash(previousBlock)
    block = blockchain.createBlock(proof, previousHash)
    response = {'message': 'Parabéns! Você minerou um block!!!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previousHash': block['previousHash']
                }
    
    return jsonify(response), 200

@app.route('/get_chain', methods = ['GET'])
def getChain():
    response = {'length': len(blockchain.chain),
                'chain': blockchain.chain
                }
    
    return jsonify(response), 200

@app.route('/is_chain_valid', methods = ['GET'])
def isChainValid():
    valid = blockchain.isChainValid(blockchain.chain)
    
    if valid:
        response = {'message': True}
    else:
        response = {'message': False}
        
    return jsonify(response), 200

app.run(host = '0.0.0.0', port = 5000)    