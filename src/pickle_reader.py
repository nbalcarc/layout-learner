import pickle

with open("output.pkl", "rb") as file:
    dumped = pickle.load(file)

print(dumped)


