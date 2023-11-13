from pubchempy import *

name = "Hydrazinecarboxylic acid, 1,1-dimethylethyl ester"
name = "Milbemycin B, 5-demethoxy-5-one-6,28-anhydro-25-ethyl-4-methyl-13-chloro-oxime"
cs = get_compounds(name, "name")
# print(cs[0].record)

result = []
for record in cs[0].record:
    print(record)
    if record != "props":
        # print(cs[0].record[record])
        if record == "id":
            result.append(cs[0].record[record]["id"]["cid"])
    else:
        for prop in cs[0].record[record]:
            print(prop)
            if prop["urn"]["label"] == "SMILES":
                result.append(prop["value"]["sval"])
            if prop["urn"]["label"] == "InChIKey":
                result.append(prop["value"]["sval"])
    print(" ")

print(result)
