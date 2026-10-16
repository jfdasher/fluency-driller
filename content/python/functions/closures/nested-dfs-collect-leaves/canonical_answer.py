def collect_leaves(root):
    leaves = []
    def dfs(node):
        if not node['children']:
            leaves.append(node['val'])
        else:
            for child in node['children']:
                dfs(child)
    dfs(root)
    return leaves
