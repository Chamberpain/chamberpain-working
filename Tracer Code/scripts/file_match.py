def argo_matches(file): 
    matches = []
    for root, dirnames, filenames in os.walk(file):
        for filename in fnmatch.filter(filenames, '*.nc'):
            matches.append(os.path.join(root, filename))
    return matches