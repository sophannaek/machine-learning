import sys

initialState_ptable = {}
transition_ptable = {}
sensor_ptable = {}
e_vectors = {}
questions = []

# # open and read file and return list of lines
def openFile():
    with open(sys.argv[1], 'r') as f:
        q_num = 0
        for line in f:
            line = line.rstrip("\n")
            questions.append(line)
            q_num = q_num + 1
        f.close()
    return questions


# Return conditional probability table
# CPT = { initialState: {}, p_transition: {}, p_sensor: {}, e_vectors: []}
def make_ptable(line):
    CPT = {}
    ls = line.split(',')
    x_initial = float(ls[0])

    # initial state probability
    CPT['initialState'] = {'t': x_initial, 'f': 1 - x_initial}

    # probability of the transition state
    CPT['p_transition'] = {('t', 't'): float(ls[1]), ('t', 'f'): 1 - float(ls[1]), ('f', 't'): float(ls[2]),
                           ('f', 'f'): 1 - float(ls[2])}
    # probability of the sensor
    CPT['p_sensor'] = {('t', 't'): float(ls[3]), ('t', 'f'): 1 - float(ls[3]), ('f', 't'): float(ls[4]),
                       ('f', 'f'): 1 - float(ls[4])}
    # evidence vectors
    CPT['e_vectors'] = ls[5:len(line)]

    return CPT


# use recursive till hit the number of evidence
# calculate the question one at a time
def filter(CPT, e_vectors):

    # base case
    if len(e_vectors) == 0:
        return [CPT['initialState']['t'], CPT['initialState']['f']]

    p_sensor = CPT['p_sensor']
    p_transition = CPT['p_transition']
    e = e_vectors[len(e_vectors) - 1]
    e_vectors.pop()
    # calculate the probability of HMM filtering
    recursive_part = summation(p_transition, filter(CPT, e_vectors))
    [p, q] = cross_product([p_sensor[('t', e)], p_sensor[('f', e)]], recursive_part)
    # normalize probability vector
    p, q = normalize([p, q])

    return [p, q]


# return the summation part of filter formula
def summation(p_sensor, filter_part):
    a = p_sensor[('t', 't')] * filter_part[0] + p_sensor[('f', 't')] * filter_part[1]
    b = p_sensor[('t', 'f')] * filter_part[0] + p_sensor[('f', 'f')] * filter_part[1]

    return [a, b]


# return normalized vector
def normalize(arr):
    alpha = 1 / (arr[0] + arr[1])
    return [alpha * arr[0], alpha * arr[1]]


# return cross product of two vectors
def cross_product(a, b):
    return [a[0] * b[0], a[1] * b[1]]


# perform HMM filtering
def calc_filter_p(question):
    CPT = make_ptable(question)
    [p, q] = filter(CPT, CPT['e_vectors'])
    print(question + "--><{0:.4f},".format(p) + "{0:.4f}>".format(q))


# driver
if __name__ == '__main__':
    questions = openFile()
    for question in questions:
        calc_filter_p(question)
