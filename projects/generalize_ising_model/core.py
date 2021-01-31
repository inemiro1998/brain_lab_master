import numpy as np
from numpy.random import permutation, random
import time
import multiprocess
import math
from projects.generalize_ising_model.tools.utils import to_find_critical_temperature
import warnings

warnings.filterwarnings("ignore")
n_cpu = multiprocess.cpu_count() - 1


# @numba.jit(nopython=True)
def initial_spin(N, type='digital'):
    # Set a random spin configuration as a initial condition
    if type == 'digital':
        initial = 2 * np.random.randint(2, size=(N, 1), dtype=np.int8) - 1
    elif type == 'analogy':
        initial = 2 * np.random.rand(N) - 1
        #initial = 2 * np.random.randint(2, size=(N, 1)) - 1
    return np.squeeze(initial)


# Montecarlo Simulation - Metroplolis Algorithm
def monte_carlo_metropolis(J, spin_vec, t, iterations, thermalize_time=None, phi_variables=False, type='digital', return_tc=False):
    no_spin = len(spin_vec)
    static, moving = np.triu_indices(no_spin, k=1)
    static = static.astype(np.int16)
    moving = moving.astype(np.int16)

    list_spin = []


    for i in range(int(iterations / no_spin)):
        spin_permutation = permutation(no_spin)
        delta = 0.01
        for j in range(no_spin):

            #aux = np.copy()
            d_e = 2 * np.dot(np.delete(spin_vec, spin_permutation[j]), np.delete(J[spin_permutation[j], :], spin_permutation[j]))

            new_spin = np.copy(spin_vec[spin_permutation[j]])

            if type == 'analogy':
                if new_spin > 0:
                    new_spin = new_spin - delta
                else:
                    new_spin = new_spin + delta
                #if random() > 0.5:
                #    new_spin = new_spin + delta
                #else:
                #    new_spin = new_spin - delta

            #d_e *= spin_vec[spin_permutation[j]]
            d_e *= new_spin

            if d_e <= 0 or random() <= np.exp(-d_e / t):
                spin_vec[spin_permutation[j]] = -1*new_spin

            list_spin.append(np.copy(spin_vec))

    if thermalize_time is not None:

        index_thermalize_time = np.round(iterations * thermalize_time).astype(int)
        spin_thermalized = np.squeeze(np.array(list_spin))[index_thermalize_time:, :]
        energy = 0
        energy_squard = 0

        if phi_variables:
            spin_bin_sum = np.zeros(np.power(2, no_spin))
            setting_int = np.linspace(0, np.power(2, no_spin) - 1, num=np.power(2, no_spin)).astype(int)
            M = list(map(lambda x: list(np.binary_repr(x, width=no_spin)), setting_int))
            M = np.flipud(np.fliplr(np.asarray(M).astype(np.int)))
            M = M * 2 - 1

        for i_spin in range(spin_thermalized.shape[0]):
            ener = np.dot(spin_thermalized[i_spin, :][static]*spin_thermalized[i_spin, :][moving], -J[static, moving])
            energy += ener
            energy_squard += ener ** 2

            if phi_variables:
                ind = np.where((M == spin_thermalized[i_spin, :]).all(axis=1))
                spin_bin_sum[ind[0][0]] += 1


        es = energy
        ess = energy_squard
        ms = abs(np.sum(abs(np.sum(spin_thermalized, axis=1))))
        mss = np.sum(abs(np.sum(spin_thermalized, axis=1)) ** 2)

        if phi_variables:
            del list_spin, index_thermalize_time, spin_thermalized, M
            return es, ess, ms, mss, spin_bin_sum
        else:
            del list_spin, index_thermalize_time, spin_thermalized
            return es, ess, ms, mss
    else:
        return spin_vec


def compute_par(values):
    n = values[0].shape[-1]
    no_flip = 100 * n ** 2
    #no_flip = 10 * n ** 2
    avg_therm = no_flip * (1 - values[4])

    E, M, S, H, tc, spin_mean = [], [], [], [], [], []
    phi_variables = values[6]
    type = values[7]
    return_tc = values[8]

    simulated_fc = np.zeros((n, n, values[2] - values[1]))

    cont = 0
    ts = values[5]

    for tT in range(values[1], values[2]):
        #print('|', end='')

        spin_vec = initial_spin(n, type=type)
        if phi_variables:
            es, ess, ms, mss, spin_bin_sum = monte_carlo_metropolis(values[0], spin_vec, ts[tT], no_flip, values[4], phi_variables=phi_variables, type=type)
            spin_mean.append(spin_bin_sum / avg_therm)
        else:
            es, ess, ms, mss = monte_carlo_metropolis(values[0], spin_vec, ts[tT], no_flip, values[4], phi_variables=phi_variables, type=type)
        E.append((es / avg_therm) / n)
        M.append((ms / avg_therm) / n)
        S.append((((mss / avg_therm) - (ms / avg_therm) ** 2) / n / ts[tT]) / n)
        H.append((((ess / avg_therm) - (es / avg_therm) ** 2) / n / ts[tT] ** 2) / n)

        simulation = np.zeros((n, values[3]))

        for sim in range(values[3]):
            simulation[:, sim] = monte_carlo_metropolis(values[0], spin_vec, ts[tT], n, phi_variables=phi_variables, type=type)

        tc.append(simulation)
        simulated_fc[..., cont] = np.corrcoef(simulation)
        cont += 1

    if return_tc:
        if phi_variables:
            return (np.copy(E), np.copy(M), np.copy(S), np.copy(H), np.copy(simulated_fc), np.copy(values[1]), np.copy(values[2]), np.asarray(spin_mean), np.asarray(tc))
        else:
            return (np.copy(E), np.copy(M), np.copy(S), np.copy(H), np.copy(simulated_fc), np.copy(values[1]), np.copy(values[2]), np.asarray(tc))
    else:
        if phi_variables:
            return (np.copy(E), np.copy(M), np.copy(S), np.copy(H), np.copy(simulated_fc), np.copy(values[1]), np.copy(values[2]), np.asarray(spin_mean))
        else:
            return (np.copy(E), np.copy(M), np.copy(S), np.copy(H), np.copy(simulated_fc), np.copy(values[1]), np.copy(values[2]))


def generalized_ising(Jij, temperature_parameters=(0.1, 5, 100), n_time_points=100, thermalize_time=0.3, temperature_distribution ='lineal', phi_variables = False, return_tc = False, type='digital'):
    n = Jij.shape[-1]

    if temperature_distribution == 'lineal':
        ts = np.linspace(temperature_parameters[0], temperature_parameters[1], num=temperature_parameters[2])
    elif temperature_distribution == 'log':
        ts = np.logspace(temperature_parameters[0],np.log10(temperature_parameters[1]),num=temperature_parameters[2])

    pool = multiprocess.Pool(n_cpu)

    step_len = math.ceil(temperature_parameters[2] / n_cpu)
    previus = 0
    l = []

    for next in range(n_cpu):
        if (next + 1) * step_len > temperature_parameters[2]:
            l.append((Jij, previus, temperature_parameters[2], n_time_points, thermalize_time, ts, phi_variables, type, return_tc))
        else:
            l.append((Jij, previus, int((next + 1) * step_len), n_time_points, thermalize_time, ts, phi_variables, type, return_tc))

        previus = int((next + 1) * step_len)

    results = np.asarray(pool.map(compute_par, l))

    simulated_fc = np.zeros((n, n, len(ts)))
    E, M, S, H = np.zeros(len(ts)), np.zeros(len(ts)), np.zeros(len(ts)), np.zeros(len(ts))


    if return_tc:
        tc = np.zeros(shape=(n_time_points,Jij.shape[0],len(ts)))

        if phi_variables:
            spin_mean = np.zeros((np.power(2, n), len(ts)))

            for i in range(results.shape[0]):
                E[results[i, 5]:results[i, 6]] = results[i, 0]
                M[results[i, 5]:results[i, 6]] = results[i, 1]
                S[results[i, 5]:results[i, 6]] = results[i, 2]
                H[results[i, 5]:results[i, 6]] = results[i, 3]
                simulated_fc[:, :, results[i, 5]:results[i, 6]] = results[i, 4]

                spin_mean[:, results[i, 5]:results[i, 6]] = np.transpose(results[i, 7])
                tc[:,:,results[i, 5]:results[i, 6]] = np.transpose(results[i, 8])
            critical_temperature = to_find_critical_temperature(S, ts)
            return np.copy(simulated_fc), np.copy(critical_temperature), np.copy(E), np.copy(M), np.copy(S), np.copy(H), np.copy(spin_mean), np.copy(tc)
        else:
            for i in range(results.shape[0]):
                E[results[i, 5]:results[i, 6]] = results[i, 0]
                M[results[i, 5]:results[i, 6]] = results[i, 1]
                S[results[i, 5]:results[i, 6]] = results[i, 2]
                H[results[i, 5]:results[i, 6]] = results[i, 3]
                simulated_fc[:, :, results[i, 5]:results[i, 6]] = results[i, 4]
                tc[:, :, results[i, 5]:results[i, 6]] = results[i, 8]
            critical_temperature = to_find_critical_temperature(S, ts)

            return np.copy(simulated_fc), np.copy(critical_temperature), np.copy(E), np.copy(M), np.copy(S), np.copy(H), np.copy(tc)
    else:
        if phi_variables:
            spin_mean = np.zeros((np.power(2, n), len(ts)))

            for i in range(results.shape[0]):
                E[results[i, 5]:results[i, 6]] = results[i, 0]
                M[results[i, 5]:results[i, 6]] = results[i, 1]
                S[results[i, 5]:results[i, 6]] = results[i, 2]
                H[results[i, 5]:results[i, 6]] = results[i, 3]
                simulated_fc[:, :, results[i, 5]:results[i, 6]] = results[i, 4]

                spin_mean[:, results[i, 5]:results[i, 6]] = np.transpose(results[i, 7])

            critical_temperature = to_find_critical_temperature(S, ts)
            return np.copy(simulated_fc), np.copy(critical_temperature), np.copy(E), np.copy(M), np.copy(S), np.copy(H), np.copy(spin_mean)
        else:
            for i in range(results.shape[0]):
                E[results[i, 5]:results[i, 6]] = results[i, 0]
                M[results[i, 5]:results[i, 6]] = results[i, 1]
                S[results[i, 5]:results[i, 6]] = results[i, 2]
                H[results[i, 5]:results[i, 6]] = results[i, 3]
                simulated_fc[:, :, results[i, 5]:results[i, 6]] = results[i, 4]

            critical_temperature = to_find_critical_temperature(S, ts)
            return np.copy(simulated_fc), np.copy(critical_temperature), np.copy(E), np.copy(M), np.copy(S), np.copy(H)

# J = np.array([[0., 0.16069726, 0.32568756, 0.20497754, 0.17010901],[0.16069726, 0., 0.31721317, 0.2493503, 0.32608541],[0.32568756, 0.31721317, 0., 0.55304965, 0.35610558],[0.20497754, 0.2493503, 0.55304965, 0., 1.],[0.17010901, 0.32608541, 0.35610558, 1., 0.]])
#
# no_temperatures = 50
# no_entities = 20
# no_simulations = 250
# thermalize_time = 0.3
#
# temperature_parameters = (0.005, J.shape[-1] * (np.mean(J) + 0.45))
#
# A,B,C,D,E,F = generalized_ising(J, temperature_parameters=(0.1, 5, 100), n_time_points=100, thermalize_time=0.3, temperature_distribution ='lineal', phi_variables = False, return_tc = False, type='digital')
#
#
# print(F)
