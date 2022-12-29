#following is a simple CYK parser to check if a given sentence belong to the grammar or not
def read_grammar(file):
    f = open(file, 'r')
    text = f.read()
    return text

def create_dict(text):
    grammar = {}
    rules = text.split("\n")
    for i in rules:
        rule = i.split(":")
        left = rule[0]
        right = rule[1]
        if(left not in grammar.keys()):
            grammar[left] = [right]
        else:
            grammar[left].append(right)    
    return grammar

def get_rules(grammar,rule):
    keys = []
    for key,value in grammar.items():
        if(rule in value):
            keys.append(key)
    return keys

def print_grammar(text):
    rules = text.split("\n")
    for i in rules:
        rule = i.split(":")
        left = rule[0]
        right = rule[1]
        print(left+"->"+right)

def print_parse_table(parse):
    print("\nThe genrated parse table is: "+"\n")
    for row in range(len(parse)-1):
        for col in range(1,len(parse)):
            print(parse[row][col],end = " ")
        print("\n")
        

def cyk(test,text):
    words = test.split(" ")
    grammar = create_dict(text)
    parse = [[[""]] * (len(words)+1) for i in range(len(words) + 1)]
    #get the first diagonal of words
    for row in range(len(words)):
        for col in range(1,len(words)+1):
            if(col-row == 1):
                key = get_rules(grammar,words[row])
                parse[row][col] = key
    #get subsequent Indices
    for l in range(2,len(words)+1):
        for row in range(len(words)):
            for col in range(1,len(words)+1):
                if(col - row == l):
                    for k in range(row+1,col):   
                        left = parse[row][k]
                        right = parse[k][col]
                        if(len(left) != 0 and len(right) != 0):
                            for lp in left:
                                for rp in right:
                                    rule = lp+" "+rp
                                    key = get_rules(grammar,rule)
                                    if(key):
                                        parse[row][col] = key
    return parse

def check(parse):
    print("\n")
    if(parse[0][len(parse)-1][0] == 'S'):
        print("The sentence belongs to the grammar\n")
    else:
        print("The sentence does not belong to the grammar\n")

def read_input(ip_file):
    f = open(ip_file, 'r')
    input = f.read()
    tests = input.split("\n")
    return tests

def main():
    tests = read_input("assignment6/111903117_Assgn6_Input_CYK.txt")
    text = read_grammar("assignment6/garammar.txt")
    print("This is the grammar used: ")
    print_grammar(text)
    print("\n")
    for test in tests:
        print("Sentence: " + test)
        parse = cyk(test,text)
        print_parse_table(parse)
        check(parse)
main()

