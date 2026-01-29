def reconstruct_path(node):
    path = []
    while node.parent:
        path.append(node.move)
        node = node.parent
    return path[::-1]

def is_solvable(start, goal):
    flat_s = [x for row in start for x in row if x != 0]
    flat_g = [x for row in goal for x in row if x != 0]
    inv_s = sum(1 for i in range(len(flat_s)) for j in range(i+1, len(flat_s)) if flat_s[i] > flat_s[j])
    inv_g = sum(1 for i in range(len(flat_g)) for j in range(i+1, len(flat_g)) if flat_g[i] > flat_g[j])
    return (inv_s % 2) == (inv_g % 2)