# CommunityDetection

This is a repo of my University Project. I've developed some scripts to 
  1. Preprocess the data
  2. Use that preprocessed data to send them through two different methods: Louvain and Leiden
  3. I used the generated communities and made validation scripts to determine the accuracy of these methods.
  4. Nodes of True Positive/True Negative/False Positive/False Negative were then sent to functions which display the network. 
  5. These networks were then generating images which the user can decide to save or view immediately.

The results of these scripts were good. However we didn't factor several things for our approach.
  1. The datasets that we used had overlapping communities
  2. Our methods didn't produced any overlapping communities as they were not capable of doing so

Despite having not so correctly outputted communities, we still got to see some communities that were accurately being detected and we have been able to show promising results.

