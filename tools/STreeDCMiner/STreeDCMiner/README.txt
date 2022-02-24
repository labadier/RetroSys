StreeDC-Miner Algorithm   
====================================================
Params:
0. Folder  
1. Data file name
2. Descriptor file name   
3. Words for including into the result file name
4. MinSupport
5. MinConfidence
6. MinLift

Params example:

```
data/car/ car.data car.names m.out 0.1 0.7 0
```

Execution example:

```
java -jar STreeDCMiner.jar data/car/ car.data car.names m.out 0.1 0.7 0.0
```

In order to not mine association rules please
set minLift and minConf to -1   


