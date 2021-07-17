# Blockchain-Cryptocurrency
A decentralised and dustributed ledger. Cryptocurrency is based on Proof-of-Work algorithm.
SHA 256 hash algorithm is used for hashing. Mining(aka hashing) formula has been ket very simple so that even the lightest of the systems can mine easily andsee the working of blockchain and currency.

"blockchain.py" contains the basic structure upon which the nodes of block-mining are built.

"anycoin_node1.py","anycoin_node2.py" and "anycoin_node3.py" contains the script for different mining nodes. These files contain port number 5001,5002 and 5003 for the nodes to run on these ports of your system. They can be changed according to system preference.

"BFS.py" is Breadth-First Search Algorithm to reach to the nodes which are not directly connected to main node under consideration. It can be implemented by just tranferring the contents of this file into "replace_chain" function of the node scripts.

"transaction.json" contains a dummy transaction for the user to know the structure of the transaction that the blocks accepts.

"nodes.json" contains every node so that each node can be connected to other.

# How to run on System
Download all the files and run "anycoin_node1.py","anycoin_node2.py" and "anycoin_node3.py" python scripts on "different" kernels. So different nodes would be active on the different ports of the system.

Use add_transaction function to add transactions and mine_block function to mine the block and write the transactions into block.

"Postman" can be used to "get" and "put" to api.

Orphaned-block problem is carefully handled so that no loss of transaction history takes place even in the blockchain




