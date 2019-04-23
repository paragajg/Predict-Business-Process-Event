# Predict-Business-Process-Event
Using LSTM Network predict occurrence of  next event.

## Dataset - Bussiness Process Challenge :2017 data set
Refer following link for details of dataset https://www.win.tue.nl/bpi/doku.php?id=2017:challenge

## Experiment 
Utilize LSTM Network to predict occurrence of an event in sequential transaction scenario.

## Setup
- Keras for deeplearning architecture
- gensim for Word2Vec (transforming events as embedded vectors)
- dask building streaming data pipeline to Keras model
- Hardware : Using cloud gpu of Vast.ai (Machine specs: GPU: RTX 2080Ti , CPU: AMD: Treadripper)
