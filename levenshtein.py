import numpy as np, argparse

OPERATIONS = {1: "Insert at position ",
              2: "Delete at position ",
              3: "Replace at position ",
              4: "Transpose at position "}

def dl_dist(word1, word2):
    n, m = len(word1), len(word2)
    d = np.zeros((n + 1, m + 1), dtype=int)

    for i in range(n + 1):
        d[i][0] = i
    for j in  range(m + 1):
        d[0][j] = j

    for i in range(n):
        for j in range(m):
            cost = int(word1[i] != word2[j])

            d[i + 1][j + 1] = min(d[i][j + 1] + 1,
                                  d[i + 1][j] + 1,
                                  d[i][j] + cost)
            if i > 0 and j > 0 and word1[i] == word2[j - 1] and word1[i - 1] == word2[j]:
                d[i + 1][j + 1] = min(d[i + 1][j + 1], d[i - 1][j - 1] + cost)

    return (d, d[n][m])

def get_operations(word1, word2):
    i, j = dl_dist(word1, word2)[0].shape
    i -= 1
    j -= 1
    operations = []

    while i >= 0 and j >= 0:
        if i > 1 and j > 1 and word1[i - 1] == word2[j - 2] and word1[i - 2] == word2[j - 1]:
            if distance_matrix[i - 2][j - 2] < distance_matrix[i][j]:
                operations.insert(0, (4, i - 1, i - 2))
                i -= 2
                j -= 2
                continue
        
        index = np.argmin([distance_matrix[i - 1][j - 1], distance_matrix[i][j - 1], distance_matrix[i - 1][j]])
        if index == 0:
            if distance_matrix[i][j] > distance_matrix[i - 1][j - 1]:
                operations.insert(0, (3, i - 1, j - 1))
            i -= 1
            j -= 1
        elif index == 1:
            operations.insert(0, (1, i - 1, j - 1))
            j -= 1
        elif index == 2:
            operations.insert(0, (2, i - 1, j - 1))
            i -= 1
    
    return operations

def get_steps(ops, word1, word2):
    temp = list(word1)
    shift = 0
    steps = [word1]

    for op in ops:
        i, j = op[1], op[2]
        if op[0] == 1: # insert
            temp.insert(i + shift + 1, word2[j])
            shift += 1
        elif op[0] == 2: # delete
            temp.pop(i + shift)
            shift -= 1
        elif op[0] == 3: # replace
            temp[i + shift] = word2[j]
        elif op[0] == 4: # transpose
            temp[i + shift], temp[j + shift] = temp[j + shift], temp[i + shift]
        
        steps.append(''.join(temp))
    
    return steps

def print_steps(steps, ops, word1, word2):
    print("Operations to change " + word1 + " into " + word2 + ":")
    i = 0

    for op in ops:
        src, dst = str(op[1]), str(op[2])
        ope = OPERATIONS[op[0]]
        if op[0] == 1:
            print(ope + dst + ": ", end="")
        else:
            print(ope + src + ": ", end="")
        print(steps[i] + " => " + steps[i + 1])
        i += 1
        
def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--quiet", action="store_true", help="decrease output verbosity")
    parser.add_argument('words', metavar='W', type=str, nargs=2, help='Words input in the program')
    args = parser.parse_args()
    quiet = args.quiet
    lword, rword = args.words
    
    return lword, rword, quiet

if __name__ == "__main__":
    lword, rword, quiet = parse_input()
    distance_matrix, edit_distance = dl_dist(lword, rword) # get edit distance + distance matrix between the 2 strings
    
    print("Edit distance between " + lword + " and " + rword + " is: " + str(edit_distance)) # print edit distance
    if not quiet:
        print("===========================================")
        operations = get_operations(lword, rword) # get edit operations from the distance matrix
        steps = get_steps(operations, lword, rword) # compute every string in between the two original ones
        print_steps(steps, operations, lword, rword) # print operations to modify string
    
    # TODO: accept sequences other than strings
    # TODO: static typing