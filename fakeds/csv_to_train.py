import pandas as pd


csv = pd.read_csv("product_urm.csv", sep=',')
samples = 0
of = open("train.csv", "w")
of.write("playlist_id,track_id\n")

for i, row in csv.iterrows():
    for j, cell in row.items():
        if cell != 0:
            print("[%s, %s] = %s" % (i+1, j, cell))
            of.write("%s,%s\n" % (i+1, j))
            samples = samples + 1

print("Samples 1: %d" % samples)
of.close()

