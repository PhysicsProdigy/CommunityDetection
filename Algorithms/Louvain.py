import csv
import os
import cugraph
import cudf
from time import time

def louvain(dataset,direct = False):
    path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Datasets/Edge_Files/' + dataset
    louvain_modularity_score = []
    for file in os.listdir(path):
        output_filename = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/CommunitiesGenerated/Louvain/' + dataset + file.split('.')[0] + '.csv'
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        print(file)
        df = cudf.read_csv(path+file, delimiter=',', dtype=['int','int', 'int'], header=0)
        ammount = df['SRC'].iloc[0]
        df["SRC_0"] = df["SRC"] - ammount
        df["DST_0"] = df["DST"] - ammount
        G = cugraph.Graph(directed=direct)
        G.from_cudf_edgelist(df, source='SRC_0', destination='DST_0')
        parts, modularity_score = cugraph.louvain(G)
        part_ids = parts["partition"].unique()
        with open(output_filename,'w',newline='') as outf:
            for p in range(len(part_ids)):
                part = []
                for i in range(len(parts)):
                    if parts["partition"][i] == p:
                        part.append(parts["vertex"][i] + ammount)
                csvwriter = csv.writer(outf)
                csvwriter.writerow(part)
        print(str(len(part_ids)) + " partition detected with a modularity score of " + str(modularity_score))
        louvain_modularity_score.append(modularity_score)
    return louvain_modularity_score

t0 = time()
modularityFacebook = louvain('Facebook/')
averageModularityFacebook = sum(modularityFacebook)/len(modularityFacebook)
t1 = time()
modularityTwitter = louvain('Twitter/',direct=True)
averageModularityTwitter = sum(modularityTwitter)/len(modularityTwitter)
t2 = time()

print("Facebooks average modularity score: " + str(averageModularityFacebook) + "\n" + "Twitter average modularity score: " + str(averageModularityTwitter) + "\n" + "Time taken on Facebook: " + str(t1-t0) + "\n" + "Time taken on Twitter: " + str(t2-t1))