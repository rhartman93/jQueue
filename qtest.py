import myQueue

testQ = myQueue.myQueue()

tString = "test1"

if(testQ.push(tString)):
    print tString + " added?"

print testQ.people

testQ.print_()

result = testQ.serve()

print result
