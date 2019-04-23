# Predict-Business-Process-Event
Using LSTM Network predict occurrence of  next event.

## Dataset - Bussiness Process Challenge :2017 data set
Refer following link for details of dataset https://www.win.tue.nl/bpi/doku.php?id=2017:challenge

van Dongen, B.F. (Boudewijn) (2017) BPI Challenge 2017. Eindhoven University of Technology. Dataset. https://doi.org/10.4121/uuid:5f3067df-f10b-45da-b98b-86ae4c7a310b

## Experiment 
Utilize LSTM Network to predict occurrence of an event in sequential transaction scenario.

## Setup
- Keras for deeplearning architecture
- gensim for Word2Vec (transforming events as embedded vectors)
- dask building streaming data pipeline to Keras model
- Hardware : Using cloud gpu of Vast.ai (Machine specs: GPU: RTX 2080Ti , CPU: AMD: Treadripper)
