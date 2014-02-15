from Tagger import Tagger

data = open("gene.counts")
training = open("gene.train")
taggerData = Tagger(data)

for line in training:
    if line == "\n":
        print
    else:
        word = line.split(" ")[0]
        tag = line.split(" ")[1]
        word = taggerData.hmm.replace_word(word)
        print word+" "+tag.strip()

    
