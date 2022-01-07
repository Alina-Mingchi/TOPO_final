# PMBANet_TOPO
# PMBANet: Progressive Multi-Branch Aggregation Network for Scene Depth Super-Resolution

This repo adjusts the training and testing of depth upsampling networks for "PMBANet: Progressive Multi-Branch Aggregation Network for Scene Depth Super-Resolution" by Xinchen Ye, Baoli Sun, and et al. at DLUT. 

Dataset used is the TOPO dataset. Images taken from the drones at EPFL as an Urban dataset, and ar la comballaz as a Rural dataset.

## The proposed progressive multi-branch aggregation depth super-resolution framework
![](https://github.com/Sunbaoli/PMBANet_DSR/blob/master/mainnet.png)

## Results


This repo can be used for training and testing of depth upsampling under noiseless and noisy cases for Middleburry  datasets. Some trained models are given to facilitate simple testings before getting to know the code in detail. Besides,  the results of our recovered depth maps under both noiseless and noisy cases are all given to make it  easy to compare with and reference our work.

## Dependences

The code supports Python 3

PyTorch (>= 1.1.0)


## Train
` python train.py `

## Test
` python test.py `


