import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


def initiateRI(dataset,algorithm):
    predictionPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/CommunitiesGenerated/' + algorithm + dataset
    groundTruthPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Datasets/Circle_Files/' + dataset

    results = []

    for file in os.listdir(predictionPath):
        temp = []
        with open(predictionPath+file , 'r') as prd, open(groundTruthPath+file,'r') as grd:
            prdReader = csv.reader(prd)
            grdReader = csv.reader(grd)

            if os.stat(groundTruthPath+file).st_size == 0:
                print('File was empty, ignoring: ' + str(file))
                continue

            lRows = [row for row in prdReader]
            rows = [row for row in grdReader]

            for row in rows:
                bestMatchingRow = [[], 0]
                for lrow in lRows:
                    found = 0
                    for nodeID in row:
                        if str(nodeID) in lrow:
                            found = found + 1
                    if found > 0 and found > bestMatchingRow[1]:
                        bestMatchingRow = [lrow,found]
                result, TP, TN, FP, FN, gRow = calculateRI(bestMatchingRow[0],row,dataset,file)
                temp.append({'predictedRow': bestMatchingRow[0], 'groundTruthRow':row, 'result': result, 'algorithm': algorithm,'dataset':dataset,'fileName': file, 'TP': TP, 'TN': TN, 'FP': FP, 'FN': FN, 'gRow':gRow})
        temp.sort(key=lambda e : e.get('result'))
        riSum = 0
        for result in temp:
            riSum = riSum + result.get('result')
        ri = riSum / len(temp)
        results.append({'data':temp,'ri':ri})

    #Sorts the dictionaries
    results.sort(key=lambda e:e.get('ri'))
    #Picks the lowest and highest performing RI on each EGO network
    visualizeThese = []
    for i in range(len(results)):
        #Picks the lowest and highest 3 decided communities and graphs it.
        for j in range(len(results[i].get('data'))):
            visualizeThese.append(results[i].get('data')[j])
        visualizeData(visualizeThese, results[i].get('ri'))
        visualizeThese =[]

#Dictionary needs to be passed that contains {"OurPrediction":A,"Ground truth":B,"Path for dataset":path, "fileName":file}
def visualizeData(arr, egoAccuracy):
    path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Datasets/Edge_Files/' + arr[0].get('dataset') + arr[0].get('fileName')

    edgeList =[]
    #We made an array for not confirmed had we wanted the grey nodes that can't be confirmed.
    notConfirmedNodes = []
    print(path)
    with open(path, 'r') as edg:
        csvReader = csv.reader(edg)
        for row in csvReader:
            if row[1] == 'SRC':
                continue
            #Append an EdgeLINK
            tup = (row[1],row[2])
            edgeList.append(tup)
            # Nodes not in any of the TP TN FP FN need to be discovered.
            if str(row[1]) not in notConfirmedNodes and str(row[1]) not in arr[0].get('gRow'):
                notConfirmedNodes.append(str(row[1]))
            if str(row[2]) not in notConfirmedNodes and str(row[2]) not in arr[0].get('gRow'):
                notConfirmedNodes.append(str(row[2]))

    #Graph Creation
    for dict in arr:
        if not dict.get('fileName') == '31317273.csv':
            continue
        G = nx.Graph()
        G.add_nodes_from(notConfirmedNodes, node_type="Can't be confirmed", node_color='#636363', alpha=0.1)
        G.add_nodes_from(dict.get('TN'), node_type="True Negative", node_color='blue', alpha=0.2)
        G.add_nodes_from(dict.get('FP'), node_type="False Positive", node_color='orange', alpha=0.3)
        G.add_nodes_from(dict.get('FN'), node_type="False Negative", node_color='red', alpha=0.6)
        G.add_nodes_from(dict.get('TP'), node_type="True Positive", node_color='green', alpha=0.8)
        G.add_edges_from(edgeList)
        node_color_list = [nc for _, nc in G.nodes(data='node_color')]
        alpha_list = [nc for _, nc in G.nodes(data='alpha')]
        pos = nx.spring_layout(G,k=0.3*1/np.sqrt(len(G.nodes())))
        nx.draw_networkx_edges(G,pos,alpha=0.4,edge_color='k')
        nx.draw_networkx_nodes(G,pos,alpha=alpha_list,node_color=node_color_list, node_size=100)
        plt.axis('off')
        plt.suptitle(str(dict.get('algorithm') + dict.get('dataset') + dict.get('fileName') + "   EgoNetScore: " + str(egoAccuracy)))
        plt.title("Green nodes: " + str(dict.get('TP')),fontsize=10)
        print(dict.get('TP'),dict.get('FP'))
        fileLocation = str('Images/' + dict.get('algorithm') + dict.get('dataset') + dict.get('fileName').split('.')[0] +"_"+str(round(dict.get('result')*100))+ '.png')
        print(fileLocation)
        plt.show()

#Calculate RI takes in the best prediction that almost matches the groundtruth and decides how accurate the community was generated.
def calculateRI(lrows,grows,dataset,file):
    ground = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Datasets/Circle_Files/' + dataset + file
    TP = []
    TN = []
    FP = []
    FN = []
    gRow = []
    #If the ground truth file is empty we don't want to be doing that EGO network
    if os.stat(ground).st_size == 0:
        print('File was empty, ignoring: ' + str(file))
        return
    #Collecting all the ground truth circles from the EGO network
    with open(ground,'r') as gnd:
        csvreader = csv.reader(gnd)
        for row in csvreader:
            for node in row:
                gRow.append(node)
    #Running through and deciding which ones are true positive, true negative, falses positive, false negative.
    for node in gRow:
        if str(node) in grows and str(node) in lrows and node not in TP:
            TP.append(node)
        if str(node) not in grows and str(node) in lrows and node not in FP:
            FP.append(node)
        if str(node) in grows and str(node) not in lrows and node not in FN:
            FN.append(node)
        if str(node) not in grows and str(node) not in lrows and node not in TN:
            TN.append(node)


    return (len(TP) + len(TN)) / (len(TP) + len(TN) + len(FP) + len(FN)), TP, TN, FP, FN, gRow
initiateRI('Facebook/', 'Louvain/')
initiateRI('Facebook/', 'Leiden/')
initiateRI('Twitter/', 'Louvain/')
initiateRI('Twitter/', 'Leiden/')
