PrioritySearch (has all the components, H)
    container = new Container()
    container.put(the first transition)
    visit = {}
    repeat:
        if container.empty():
            return False
        node = container.get()
        if that is the final state:
            return the cost path
        Visit(n, container, visited, M, H):
            visited.add(n)
            for all the successors(n):
                if that is not in visited:
                    put it in the container

