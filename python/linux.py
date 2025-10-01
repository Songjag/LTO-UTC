def normalize_path(path):
    components = path.split('/')

    stack = []

    for component in components:
        if component == '' or component == '.':
            continue
        elif component == '..':
            if stack:  
                stack.pop()
        else:
            stack.append(component)
    
    if not stack:
        return '/'
    return '/' + '/'.join(stack)
path = input().strip()
print(normalize_path(path))