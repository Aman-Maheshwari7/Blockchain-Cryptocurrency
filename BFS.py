# BFS starts from "start"
# Functionality for non-directly connected node
import requests
def BFS(self,start):
    q=[]
    q.append(start)
    ans=[]
    
    while(len(q)>0):
        #Can add some working here when transferring into the main code
        node=q[0]
        q.pop(0)
        ans.append(node)
        
        response=requests.get("http://{}/get_connected_nodes".format(node))
        nodeList=response['nodes']
        for i in nodeList:
            if i not in q:
                q.add(i)
    return ans

# "ans" contains all nodes reachable from start 
        
    
    

    
    
    
    
    
    
    