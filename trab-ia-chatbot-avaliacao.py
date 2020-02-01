import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score

file = open("frases.txt", "r")
texto = file.read()
texto.lower()
texto = texto.replace("\n", "")
corpus = texto.rsplit(",")
print("Frases: ", corpus)
#print(len(corpus))

vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, strip_accents='unicode')
X = vectorizer.fit_transform(corpus)

file_intencao = open("intencao_frase.txt", "r")
texto_intencao = file_intencao.read()
texto_intencao = texto_intencao.replace("\n", "")
Y = texto_intencao.rsplit(",")
print("Intencoes: ", Y)

loocv = LeaveOneOut()

print("\n--- LogisticRegression ---")
model_loocv = LogisticRegression(random_state = 1, solver='lbfgs', multi_class='multinomial')
results_loocv = model_selection.cross_val_score(model_loocv, X, Y, cv = loocv)
print("Accuracy LR: %.2f%%" % (results_loocv.mean()*100.0))

results_loocv = model_selection.cross_val_predict(model_loocv, X, Y, cv=loocv)
print("precision_score: ", precision_score(Y, results_loocv, average='macro') * 100)
print("recall_score: ", recall_score(Y, results_loocv, average='macro') * 100)
print("accuracy_score: ", accuracy_score(Y, results_loocv, normalize=True) * 100)

print("\n--- KNeighborsClassifier ---")
model_loocv = KNeighborsClassifier(n_neighbors = 1)
results_loocv = model_selection.cross_val_score(model_loocv, X, Y, cv = loocv)
print("Accuracy KNN: %.2f%%" % (results_loocv.mean()*100.0))

results_loocv = model_selection.cross_val_predict(model_loocv, X, Y, cv=loocv)
print("precision_score: ", precision_score(Y, results_loocv, average='macro') * 100)
print("recall_score: ", recall_score(Y, results_loocv, average='macro') * 100)
print("accuracy_score: ", accuracy_score(Y, results_loocv, normalize=True) * 100)

print("\n--- DecisionTreeClassifier ---")
model_loocv = DecisionTreeClassifier(random_state = 0)
results_loocv = model_selection.cross_val_score(model_loocv, X, Y, cv = loocv)
print("Accuracy DT: %.2f%%" % (results_loocv.mean()*100.0))

results_loocv = model_selection.cross_val_predict(model_loocv, X, Y, cv=loocv)
print("precision_score: ", precision_score(Y, results_loocv, average='macro') * 100)
print("recall_score: ", recall_score(Y, results_loocv, average='macro') * 100)
print("accuracy_score: ", accuracy_score(Y, results_loocv, normalize=True) * 100)