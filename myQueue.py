class myQueue:
    def __init__(self):
        self.people = []

    def push(self, person):
        if person not in self.people:
            self.people.append(person)
            return 1
        else:
            return 0

    def serve(self):
        if(len(self.people) > 0):
            return self.people.pop(0)

    def remove(self, index):
        #allowing index to be specified in case other removal is needed
        #doesn't return value as removed
        if(len(self.people) > 0):
            self.people.pop(index)

    def print_(self):
        for i in self.people:
            print i

    def isEmpty(self):
        return len(self.people) == 0

    def listify(self):
        returnList = []
        for i in self.people:
            returnList.append(i)

    def stringify(self):
        returnString = ""
        for i in self.people:
            returnString += i + "\n"
        return returnString
    
    def contains(self, query):
        return query in self.people
