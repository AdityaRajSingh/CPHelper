from CPPCompiler import CPPCompiler		# For compiling and running cplusplus code
from Task import Task 					# For getting task data like test cases
import sys								# For system arguments and exit 


BASE_PATH = sys.argv[1]					# Base path of the cpp and json file
DASH_COUNT = 50							# Number of dashes to print after each test case.

compiler = CPPCompiler(BASE_PATH)		# cplusplus compiler.
task = Task(BASE_PATH)					# task object to get task data

# Compile the cpp file and create a output file. Exception for Compilation error.
try:
	compileOutput = compiler.compile()
except:
	print "Compilation Error"
	exit(0)

'''
Description - This functions runs the given cpp file for a given input and checks it's output with the expected output
Parameters -
	compiler - CPPCompiler - Runs the file for the input and returns the output.
	testCaseNo - int - Test Case number.
	input - string - input of the program.
	expectedOutput - string - expected output of the program.
Returns - 
	1 - If the expected output is same as the actual output.
	0 - If the expected output is different from actual output.
   -1 - If no expected output is provided.
'''
def runAndCheck(compiler , testCaseNo ,input = "" , expectedOutput = None):
	# Run and get the output of the program for the given input. Exception for runtime error.
	try:
		runOutput = compiler.run(input)
	except:
		print "\nRuntime Error"
		exit(0)

	if not expectedOutput:
		expectedOutput = None

	print "Test Case #%s : \nInput : " %testCaseNo
	print input

	if expectedOutput != None:
		expectedOutput = expectedOutput.strip()
		print "\nExpected Output : "
		print expectedOutput + "\n"

	runOutput = runOutput.strip()
	print "Actual Output : "
	print runOutput + "\n"

	if expectedOutput == None:
		return -1
	if runOutput == expectedOutput:
		return 1
	else:
		return 0

'''
Description - This functions reads the data from a global input.txt files and returns it.
				If --add is at the beginning of the test case the adds it to the task data json file.
				If --output is presents then adds the expected output as well.
Parameters -
	None.
Returns - 
	inputData , outputData
'''
def getDataFromInputTxt():
	inputData = ''
	outputData = ''

	with open("/home/schitzo/Documents/Programming/input.txt" , 'rb') as inputFile:
		inputData = inputFile.read();

	if '--add' in inputData:
		inputData = inputData[6:]
		if '--output' in inputData:
			inputData , outputData = inputData.split('--output') 
		task.addTask(inputData , outputData)

	if '--output' in inputData:
		inputData , outputData = inputData.strip().split('--output')

	return inputData , outputData



testNumber = 0
allOkCount = 0

inputData , outputData = getDataFromInputTxt()

tests = task.getTests()

# Add the data of global input.txt file to the testcases.
if {'input' : inputData , 'output' : outputData} not in tests:
	tests.append({'input' : inputData , 'output' : outputData})

# Check for each input/output.
for i_o in tests:
	check_result = runAndCheck(compiler , testNumber , i_o['input'] , i_o['output'])
	testNumber += 1
	if check_result == 1:
		allOkCount += 1
		print 'Success!'
	elif check_result == -1:
		allOkCount += 1
		print 'Can\'t Say'
	else:
		print "Wrong Answer" 
	print '-' * DASH_COUNT



if testNumber == allOkCount:
	print "\nALL OK."
else:
	print "\nSome test cases Failed."