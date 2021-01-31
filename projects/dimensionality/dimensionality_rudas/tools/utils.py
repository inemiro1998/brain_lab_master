import numpy as np
import matplotlib.pyplot as plt
import sys
import networkx as nx
import random
from numpy import NaN, Inf, arange, isscalar, asarray, array
from scipy.optimize import curve_fit
import os


def makedir(path):
    if not os.path.exists(path):
        os.mkdir(path)
def file_exists(filename):
    import os
    exists = os.path.isfile(filename)
    if exists:
        return True
    else:
        return False

def to_generate_random_graph(size, isolate=False, weighted=True):
    while True:
        G = nx.complete_graph(size, create_using=nx.Graph())

        G.remove_edges_from(nx.selfloop_edges(G))

        if not isolate:
            if len(list(nx.isolates(G))) == 0:
                break


    if weighted:
        for (u, v) in G.edges():
            G.edges[u, v]['weight'] = random.random()

    return G

def save_graph(path_output, graph):
    format = '%1.4f'
    matrix = nx.to_numpy_array(graph)
    np.savetxt(path_output, matrix, delimiter=',', fmt=format)

    return matrix

def save_file(data,path,name):

    default_delimiter = ','
    format = '%1.5f'

    if isinstance(data,list):
        data = np.array(data)

    if len(data.shape) <= 2:
        file = path + str(name) + '.csv'

        if not file_exists(file):
            np.savetxt(file, np.asarray(data), delimiter=default_delimiter, fmt=format)
    else:
        file = path + str(name) + '.npy'
        if not file_exists(file):
            np.save(file,np.asarray([data]))


def to_save_results(temperature_parameters, J, E, M, H, S, simulated_fc, critical_temperature, path_output,temperature_distribution = 'linear'):
    default_delimiter = ','
    format = '%1.5f'

    np.savetxt(path_output + 'ener.csv', E, delimiter=default_delimiter, fmt=format)
    np.savetxt(path_output + 'J_ij.csv', J, delimiter=default_delimiter, fmt=format)
    np.savetxt(path_output + 'magn.csv', M, delimiter=default_delimiter, fmt=format)
    np.savetxt(path_output + 'susc.csv', S, delimiter=default_delimiter, fmt=format)
    np.savetxt(path_output + 'heat.csv', H, delimiter=default_delimiter, fmt=format)
    np.savetxt(path_output + 'ctem.csv', critical_temperature, delimiter=default_delimiter, fmt=format)
    np.save(path_output + 'sim_fc', simulated_fc)

    if temperature_distribution == 'linear':
        ts = np.linspace(temperature_parameters[0], temperature_parameters[1], num=temperature_parameters[2])
    elif temperature_distribution == 'log':
        ts = np.logspace(temperature_parameters[0], np.log10(temperature_parameters[1]), num=temperature_parameters[2])

    f = plt.figure(figsize=(18, 10))  # plot the calculated values

    f.add_subplot(2, 2, 1)
    plt.scatter(ts, E, s=50, marker='o', color='IndianRed')
    plt.xlabel("Temperature (T)", fontsize=20)
    plt.ylabel("Energy ", fontsize=20)
    plt.axis('tight')
    if temperature_distribution == 'log':
        plt.semilogx()

    f.add_subplot(2, 2, 2)
    plt.scatter(ts, abs(M), s=50, marker='o', color='RoyalBlue')
    plt.xlabel("Temperature (T)", fontsize=20)
    plt.ylabel("Magnetization ", fontsize=20)
    plt.axis('tight')
    if temperature_distribution == 'log':
        plt.semilogx()

    f.add_subplot(2, 2, 3)
    plt.scatter(ts, H, s=50, marker='o', color='IndianRed')
    plt.xlabel("Temperature (T)", fontsize=20)
    plt.ylabel("Specific Heat", fontsize=20)
    plt.axis('tight')
    if temperature_distribution == 'log':
        plt.semilogx()

    f.add_subplot(2, 2, 4)
    plt.scatter(ts, S, s=50, marker='o', color='RoyalBlue')
    plt.xlabel("Temperature (T)", fontsize=20)
    plt.ylabel("Susceptibility", fontsize=20)
    plt.axis('tight')
    if temperature_distribution == 'log':
        plt.semilogx()

    # plt.show()
    plt.savefig(path_output + 'plots.png', dpi=300)

    del ts
    plt.close()
    plt.close(f)


def peakdet(v, delta, x=None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html

    Returns two arrays

    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.

    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.

    """
    maxtab = []
    mintab = []

    if x is None:
        x = arange(len(v))

    v = asarray(v)

    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')

    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')

    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN

    lookformax = True

    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx - delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn + delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)


def to_find_critical_temperature(data, temp):
    import numpy as np
    from scipy.signal import argrelextrema

    local_max = argrelextrema(data, np.greater, order=1)
    y_test = data.copy()
    y_test[np.array(local_max)] = (y_test[np.array(local_max) + 1] + y_test[np.array(local_max) - 1]) / 2

    return temp[np.where(y_test == np.max(y_test[local_max]))]


def to_normalize(J,netx = False):
    if netx:
        J = nx.to_numpy_array(J)
    max_J = np.max(J)
    min_J = np.min(J)

    if max_J >= 0 and max_J <= 1 and min_J >= 0 and min_J <= 1:
        if netx:
            return nx.to_networkx_graph(J)
        else:
            return J
    else:
        if netx:
            return nx.to_networkx_graph(J / max_J)
        else:
            return J / max_J

def find_nearest(array, value):
    idx = np.abs(array - value).argmin()
    return idx


def dim(corr_func, r, idx_Tc):
    def model(r, z, p):
        return (np.exp(-r * z)) / (r ** p)

    z_estimateds = []
    p_estimateds = []

    n_temperatures, n_samples = corr_func.shape

    #r = r[1:n_samples]
    corr_func = corr_func[1:n_temperatures, :]
    #corr_func = corr_func[:, 1:n_samples]

    for i in range(corr_func.shape[0]):
        corr_func_in = corr_func[i, :]
        parameters_estimated, pcov = curve_fit(model, np.nan_to_num(r), np.nan_to_num(corr_func_in), maxfev=10000)

        z_estimateds.append(1 / parameters_estimated[0])
        p_estimateds.append(parameters_estimated[1])

    P_0_gtc_mn = np.mean(p_estimateds[idx_Tc + 1:])

    d = (2 * P_0_gtc_mn) + 1

    return d


def correlation_function(simulated_matrix, structural_matrix):
    Corr_all = np.nan_to_num(simulated_matrix)
    temp = Corr_all.shape[2]
    max_J = np.max(structural_matrix)
    J = structural_matrix / max_J

    corr_func = np.zeros((temp, 50))

    D, B = distance_wei(1. / J[:, :])
    len_D = np.max(D)
    div = len_D / 50
    r = np.linspace(div, len_D, 50)
    count = 0

    for i in np.linspace(div, len_D, 50):
        a = np.where((D <= i))

        for t in range(temp):
            corr = Corr_all[:, :, t]
            corr_avg = np.sum(corr[a]) / len(a[-1])
            corr_func[t, count] = corr_avg

        count = count + 1
    return corr_func, r


def distance_wei(G):
    '''
    The distance matrix contains lengths of shortest paths between all
    pairs of nodes. An entry (u,v) represents the length of shortest path
    from node u to node v. The average shortest path length is the
    characteristic path length of the network.
    Input:      L,      Directed/undirected connection-length matrix.
    Output:     D,      distance (shortest weighted path) matrix
                B,      number of edges in shortest weighted path matrix
    Notes:
       The input matrix must be a connection-length matrix, typically
    obtained via a mapping from weight to length. For instance, in a
    weighted correlation network higher correlations are more naturally
    interpreted as shorter distances and the input matrix should
    consequently be some inverse of the connectivity matrix.
       The number of edges in shortest weighted paths may in general
    exceed the number of edges in shortest binary paths (i.e. shortest
    paths computed on the binarized connectivity matrix), because shortest
    weighted paths have the minimal weighted distance, but not necessarily
    the minimal number of edges.
       Lengths between disconnected nodes are set to Inf.
       Lengths on the main diagonal are set to 0.
    Algorithm: Dijkstra's algorithm.
    '''

    n = len(G)
    D = np.zeros((n, n))  # distance matrix
    D[np.logical_not(np.eye(n))] = np.inf
    B = np.zeros((n, n))  # number of edges matrix

    for u in range(n):
        # distance permanence (true is temporary)
        S = np.ones((n,), dtype=bool)
        G1 = G.copy()
        V = [u]
        while True:
            S[V] = 0  # distance u->V is now permanent
            G1[:, V] = 0  # no in-edges as already shortest
            for v in V:
                W, = np.where(G1[v, :])  # neighbors of shortest nodes

                td = np.array(
                    [D[u, W].flatten(), (D[u, v] + G1[v, W]).flatten()])
                d = np.min(td, axis=0)
                wi = np.argmin(td, axis=0)

                D[u, W] = d  # smallest of old/new path lengths
                ind = W[np.where(wi == 1)]  # indices of lengthened paths
                # increment nr_edges for lengthened paths
                B[u, ind] = B[u, v] + 1

            if D[u, S].size == 0:  # all nodes reached
                break
            minD = np.min(D[u, S])
            if np.isinf(minD):  # some nodes cannot be reached
                break

            V, = np.where(D[u, :] == minD)

    return D, B


def mse(a, b):
    # the 'Mean Squared Error' between the two matrix is the
    # sum of the squared difference between the two matrix;
    # NOTE: the two matrix must have the same dimension
    err = np.sum((a - b) ** 2)
    err /= float(a.shape[0] * b.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def ks_test(A, B):
    import scipy
    return 1 / scipy.stats.ks_2samp(np.ravel(A), np.ravel(B))[0]
