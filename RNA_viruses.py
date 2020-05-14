#!/usr/bin/env python

from __future__ import division
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


np.random.seed()

def transfer_virions(VV, i, j, x):
    '''
    Transfer x virions from cell i to sell j;
    if x is greater than teh number of virions in cell i, transfer all the virions from this cell
    '''
    x = np.min([x, VV[i]])
    VV[j] += x
    VV[i] -= x
    return VV

def gini(VV):
    '''
    Calculate Gini coefficient
    '''
    return np.abs(VV[:,np.newaxis] - VV[np.newaxis, :]).sum()/(2.*VV.sum()*VV.shape[0])

if __name__ == "__main__":
    '''
    Modeling RNA viruses
    '''
    plt.ioff()
    plt.close('all')


    #Parameters
    N = 50 #number of cells
    mV = 10 #mean number of virions in a cell
    sV = 3 #standard deviation of the number of virions in a cell

    #initializing the cells with random number of virions
    VV = np.random.normal(loc = mV, scale = sV, size = N).round() #Normal/Gaussian random numbers are rounded to the closest integer
    VV[VV<0] = 0. #one cannot have negative number of virions
    
    ##calculate the Gini coefficient for the virion distribution
    G = gini(VV)
    print(G)


    #simulating exchanges of virions between cells
    n = 10**4 #number of virion exchanges

    VV_n = [np.copy(VV)]
    G_n = [G]
    NN = range(N)
    # ij = np.random.randint(0, N, (n,2)) 
    # ij = random.sample(range(0,N))
    for step in range(n):
        i, j = random.sample(NN, 2)
        if VV[i] >0:
            x = np.random.randint(1, VV[i]+1)
        else:
            x = 0
        VV = transfer_virions(VV, i, j, x)
        G = gini(VV)
        VV_n.append(np.copy(VV))
        G_n.append(G)
        print(f'step {step}, number of virions: {VV}, Gini coefficient: {G}')

    VV_n = np.array(VV_n)
    G_n = np.array(G_n)
    nn = np.arange(n+1)
    fig, axs = plt.subplots(2, 1, figsize = (10, 10))
    for n_cell, V_n in enumerate(VV_n.T):
        axs[0].plot(nn, V_n, label = f'cell {n_cell}')
        axs[0].set_xlabel('#exchanges')
        axs[0].set_ylabel('#virions in a cell')
        if n_cell > 4:
            break
    axs[0].legend()
    axs[0].set_title(f'#cells: {N}, mean #virions: {mV}, std #virions: {sV}, #exchanges: {n}')
    
    axs[1].plot(nn, G_n)
    axs[1].set_xlabel('#exchanges')
    axs[1].set_ylabel('Gini coefficient')
    # axs[1].set_title('Gini coefficient')

    # fig.suptitle(f'#cells: {N}, mean #virions: {mV}, std #virions: {sV}, #exchanges: {n}')
    plt.tight_layout()
    plt.savefig(f'./figs/{N}cells_{mV}virions_{sV}std_{n}steps.jpg')
    plt.close()

    fig, ax = plt.subplots(1, 1, figsize = (6, 6))
    ax.plot(NN, VV_n[0], label = 'Initial distribution')
    ax.plot(NN, VV_n[-1], label = 'Final distribution')
    ax.set_xlabel('cell number')
    ax.set_ylabel('#virions in cell')
    ax.legend()
    ax.set_title(f'#cells: {N}, mean #virions: {mV}, std #virions: {sV}, #exchanges: {n}')
    # fig.suptitle(f'#cells: {N}, mean #virions: {mV}, std #virions: {sV}, #exchanges: {n}')
    plt.tight_layout()
    plt.savefig(f'./figs/init_final_{N}cells_{mV}virions_{sV}std_{n}steps.jpg')
    plt.close()


    Vmax = int(np.max([VV_n[0], VV_n[-1]])) #total number of virions
    vv = range(Vmax)
    # Vdist = np.array([np.sum(VV_n == v, axis = 1) for v in vv])
    dist_init = np.array([np.sum(VV_n[0] == v) for v in vv])
    dist_final = np.array([np.sum(VV_n[-1] == v) for v in vv])

    fig, ax = plt.subplots(1, 1, figsize = (6, 6))
    ax.plot(vv, dist_init, label = 'Initial distribution')
    ax.plot(vv, dist_final, label = 'Final distribution')
    ax.set_xlabel('cell number')
    ax.set_ylabel('#virions in cell')
    ax.legend()
    ax.set_title(f'#cells: {N}, mean #virions: {mV}, std #virions: {sV}, #exchanges: {n}')
    # fig.suptitle(f'#cells: {N}, mean #virions: {mV}, std #virions: {sV}, #exchanges: {n}')
    plt.tight_layout()
    plt.savefig(f'./figs/distrib_{N}cells_{mV}virions_{sV}std_{n}steps.jpg')
    plt.close()
