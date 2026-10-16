def sum_tree(root):
    total = 0
    def dfs(node):
        nonlocal total
        total += node['val']
        for child in node['children']:
            dfs(child)
    dfs(root)
    return total
