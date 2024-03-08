import tkinter as tk
from tkinter import filedialog
import scipy.io
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# reading the image array from the mat files
def read_img(file1,file2):
    X = list(scipy.io.loadmat(file1).values())[-1]
    y = list(scipy.io.loadmat(file1).values())[-1]
    return X, y
# flattening the image to make it to a feature vector
def flatten_data(images):
    flat_imgs = []
    for img in images:
        if img.ndim < 3:
            flat_imgs.append(img.flatten())
        else:
            s = img.shape
            temp = np.zeros((s[2], s[0]*s[1]))
            for i in range(s[2]):
                temp[i] = img[:, :, i].flatten()
            flat_imgs.append(temp)
    return flat_imgs

# initiating population 
def initiate_population(x, n, ind):
    population = np.zeros((ind, n), np.uint8)
    for i in range(ind):
        population[i] = np.random.randint(200, size=(n,))
    return population

# generating offspring
def crossover(m1, m2, population):
    mate1 = []
    mate2 = []
    k = np.random.randint(1,4)
    for val in m1:
        mate1.append(val)
    for vals in m2:
        mate2.append(vals)
    for i in range(k, len(mate1)):
        mate1[i], mate2[i] = m2[i], m1[i]
    return mate1, mate2

#mutating 
def mutate(ofsp):
    m_ofsp = []
    m_ofsp.append(ofsp)
    k = np.random.randint(len(ofsp))
    m_ofsp[0][k] = np.random.randint(200)
    return m_ofsp[0]

# defining the fitness function
def fitness(X, y):
    X = X.T
    # dividing the data into train and test splits
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)
    # training the svm
    clf = svm.SVC(decision_function_shape='ovo', probability=True)
    clf.fit(X_train, y_train)
    # prediction of the test data
    y_pred = clf.predict(X_test)
    return accuracy_score(y_test, y_pred)

# calculating fitness of all individuals in a generation 
def fitness_all(npool, X, Y):
    fitnessScore_list = []
    for i in npool:
        score = fitness(X[i], Y)
        fitnessScore_list.append(score)
    return fitnessScore_list

# driver function 
def run(file1, file2, num_bands, num_inds, num_gens):
    n = num_bands
    # selecting bands  based on user input
    ind = num_inds
    # we are selecting no. of individuals based on user input
    X, y = flatten_data(read_img(file1,file2))
    # initializing the population
    population = initiate_population(X, n, ind)
    generation = 0
    while(generation != num_gens):
    # stopping criteria  based on user input
        count = 0
        offspring_list = []
        # Mating two parents
        while(count < ind-1):
            p1 = population[count]
            p2 = population[count+1]
            offspring1, offspring2 = crossover(p1, p2, population) 
            # performing a crossover over p1 and p2
            m_offspring1 = mutate(list(offspring1))
            offspring_list.append(m_offspring1)
            count += 1
            npool = []   
        for items in population:
            npool.append(items)
        for item in offspring_list:
            npool.append(item) 
        fitness_list = fitness_all(npool, X, y) 
        #calculating fitness score of all the individuals in npool generation
        scores = []
        for i, item in enumerate(fitness_list):
            scores.append((fitness_list[i], i))
        sorted_score = sorted(scores, reverse=True)  
        sorted_index = []
        for i in range(len(sorted_score)):
            sorted_index.append(sorted_score[i][1])
        next_gen = []
        for index in sorted_index:
            next_gen.append(npool[index])
        population = next_gen[0:ind]
        generation += 1
    return population[0], sorted_score[0], sorted_score[-1]

