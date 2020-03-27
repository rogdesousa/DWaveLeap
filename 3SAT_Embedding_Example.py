
# coding: utf-8

# In[2]:


#Lecture 21
from dwave.system.samplers import DWaveSampler


# In[6]:


# 1) Implement simple QUBO with two qubits in the Chimera graph: E(q0,q1)=(q0-q1)^2
# Set Q for the minor-embedded problem QUBO
qubit_biases = {(0, 0): 1, (4, 4): 1}
coupler_strengths = {(0, 4): -2}
Q = dict(qubit_biases)
Q.update(coupler_strengths)


# In[7]:


response = DWaveSampler().sample_qubo(Q, num_reads=1000)
for (sample, energy, num) in response.data():
    print(sample, "Energy: ", energy, "Occurrences: ", num)


# In[8]:


# As you can see, most of the time the QPU outputs values with qubits in the same state (00 or 11).
# 2) Minor-embedding to implement 3-bit 3-SAT
# We will now use "chaining" to lock q0 and q5 in the same state. This will allow the use of 
# (q0, q4, q1, q5) to represent 3 qubits coupled to each other with the same coupling strengths. 
# Entering the biases and coupler strengths as described in the notes:
qubit_biases = {(0, 0): 0.33, (1, 1): -0.33, (4, 4): -0.33, (5, 5): 0.33}
coupler_strengths = {(0, 4): 0.66, (1, 4): 0.66, (1, 5): 0.66, (0, 5): -1}
Q = dict(qubit_biases)
Q.update(coupler_strengths)


# In[9]:


response = DWaveSampler().sample_qubo(Q, num_reads=1000)
for (sample, energy, num) in response.data():
    print(sample, "Energy: ", energy, "Occurrences: ", num)


# In[10]:


# The trick worked out nicely! We got each of the 3 right answers about 1/3 of the time. 
# 3) Using DWave's EmbeddingComposite function to do the minor-embedding for you
# Let's implement the 3-SAT example from class:
# Four bits z0 z1 z2 z3 z4
# Three clauses C(0,1,2), C(1,2,3), C(0,3,4)
from dwave.system.composites import EmbeddingComposite


# In[11]:


# Set Q for the problem QUBO
linear = {('z0', 'z0'): -2, ('z1', 'z1'): -2, ('z2', 'z2'): -2, ('z3', 'z3'): -2, ('z4', 'z4'): -1}
quadratic = {('z0', 'z1'): 2, ('z0', 'z2'): 2, ('z1', 'z2'): 4, ('z1', 'z3'): 2, ('z2', 'z3'): 2, ('z0', 'z3'): 2, ('z0', 'z4'): 2, ('z3', 'z4'): 2}
Q = dict(linear)
Q.update(quadratic)


# In[12]:


# Minor-embed and sample 1000 times on a default D-Wave system
response = EmbeddingComposite(DWaveSampler()).sample_qubo(Q, num_reads=1000)
for (sample, energy, num_occurrences, aux) in response.data():
    print(sample, "Energy: ", energy, "Occurrences: ", num_occurrences)


# In[ ]:


# Are these the correct solutions we agreed in class? :-) 

