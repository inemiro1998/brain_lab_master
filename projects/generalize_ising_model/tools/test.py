import numpy as np
import matplotlib.pyplot as plt

# Define logistic map function for loop:

def logistic_map(a,x0,nsteps):
	x = np.zeros(nsteps);
	x[0] = x0

	for k in np.arange(1,nsteps):
		x[k] = a*x[k-1]*(1-x[k-1])

	return x

# Use logistic_map func in problem_1 function:

def problem_1(a,x0,nsteps,print_step):

	# Obtain x arrays for given parameters.
	x = logistic_map(a,x0,nsteps)
	x2 = logistic_map(a,x0+np.finfo(float).eps,nsteps)

	# Compute and print difference.
	print(np.abs(x-x2)[print_step])
	return(np.abs(x-x2)[print_step])

def problem_2(a,x0,nsteps,print_step):

	# Obtain numerical x array:
	x = logistic_map(a,x0,nsteps)

	# Obtain analytical solution:

	x_analytical = lambda n: (1/2)*(1-np.cos(((2**n)*(np.arccos(1-2*x0)))))
	x2 = [x_analytical(n) for n in np.arange(0,nsteps)]

	# Compute difference:
	print(x2)
	print(x)

problem_2(4,0.6,5,1)
