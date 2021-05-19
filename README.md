# Create a problem

Problems are the use cases we want to solve. As a developer you can consult the list of available problems or you can design your own problem. We can define it in a simple way through a json file (problem_def.json). In this case, we will create a quantum random number generator (QRNG):

```json
{
    "problem": "QRNG",
    "input_data":{
        "size": "int"
    },
    "output_data": "str"
}
```

It is as simple as that, give a name, define some input data and mark how the output data will be. A txt file explaining these parameters must also be associated:

```txt
"QRNG": Program that will return a randomly generated string of 0 and 1s.
"size": Length of the output string
```
# Solver blueprint

Once the problem has been defined, let's see how we could create a solver associated to this problem in order to upload it to the Qapitan platform. The way to do this will be from a GitHub repository that should have the following files:

- definition.json
- main.py
- app.py
- requirements.txt


## definition.json

This file will contain the basic information of the problem to be treated. Let's see an example to see each of the parts to be defined. In this case, we will continue with the quantum random number generator (QRNG):
```json
{
    "problem": "QRNG",
    "solvers": [
        {
            "name": "MyFirstAlgorithm",
            "provider": "local",
            "solver_params": {},
            "extra_arguments":{}
        }
    ]
}
```

First we will indicate the name of the problem to be solved. To create the solver, we don't need  define the input data because it is already associated with the name of the problem. After this we find the "solvers" attribute, a list with our different algorithms that we have created to solve the problem. In this case we have created only one solver, in which we have indicated: "name", "provider", "solver_params" and "extra_arguments".

- "name": will be the way in which the customer can refer to the algorithm.

- "provider": this variable is used to notify Qapitan that it will be necessary to use the credentials of a specific provider ("dwave", "ionq", "ibmq", ...). "local" means that no credentials will be needed.

- "solver_params": dictionary that will contain the variables you want to pass to your algorithm. These variables will be invisible to the end client.

- "extra_arguments": in certain situations, the customer may have the ability to modify certain parameters of the algorithm such as number of shots outside the problem definition itself. This dictionary will contain the set of such variables.

## main.py

This file will contain only a "run" function to which the parameters "input_data", "solver_params" and "extra_arguments" will be passed:
```python
from qiskit import QuantumCircuit, Aer, execute, IBMQ

def run(input_data, solver_params, extra_arguments):

    size = int(input_data['size'])
    backend = Aer.get_backend('qasm_simulator')

    qc = QuantumCircuit(1)
    qc.h(0)
    qc.measure_all()

    job = execute(qc, backend=backend, shots=size, memory=True)
    individual_shots = job.result().get_memory()

    output = ''
    for i in individual_shots:
        output+=i

    return output
```

## app.py

```python
import main
result = main.run(problem_data, solver_params, extra_arguments)
print(result)
```
As you can see, from this file the only thing that will be done is to call the function "run" that we have just created in the main. However, if you want to test that everything works correctly without having to upload it to the platform, this is the ideal place to do it. To do this, let's first look at the structure of a customer request.

```json
{
    "problem": "QRNG",
    "input_data": {
        "size": 100
    },
    "solver": "MyFirstAlgorithm",
    "extra_arguments": {}
}
```

Once the client makes the request, it will automatically check if the algorithm in the definition had indicated a "provider" to initialize the credentials and later, to that same json it will add the "solver_params" that had been defined. So you could create a local input.json of that form and define app.py as follows:

```python
#########  THIS FILE WILL BE REPLACED  #########

input_file_name = "input.json"

################################################
#########    DO NOT TOUCH FROM HERE    #########
################################################

# Input data loader. Container will get data from here

import json
with open(input_file_name) as f:
  dic = json.load(f)

# Optional extra parameters

if "extra_arguments" in dic:
    extra_arguments = dic['extra_arguments']
else:
    extra_arguments = {}

if "solver_params" in dic:
    solver_params = dic['solver_params']
else:
    solver_params = {}


import main
result = main.run(dic['input_data'], solver_params, extra_arguments)
print(result)

################################################
#########    DO NOT UNTIL FROM HERE    #########
################################################
```

And when executing the app.py it will give us in this case a string of 100 zeros and ones created randomly (with the qiskit simulator).

## requeriments.txt

finally we must create the "requeriments.txt" indicating the libraries used as well as their versions:

```txt
qiskit==0.17.0
```

Congratulations! with this little tutorial you have just seen how to create your first algorithm that you will be able to share on the Qapitan platform!
