from functions.get_files_info import *
from functions.get_files_content import *
from functions.write_file import *
from functions.run_python_file import *

def test():

    # get_files_info tests

    '''result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)
    print("")

    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)

    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(result)

    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(result)'''

    # get_files_content tests

    '''result = get_files_content("calculator", "lorem.txt")
    print(result)'''

    '''result = get_files_content("calculator", "main.py")
    print(result)

    result = get_files_content("calculator", "pkg/calculator.py")
    print(result)

    result = get_files_content("calculator", "/bin/cat")
    print(result)

    result = get_files_content("calculator", "pkg/does_not_exist.py")
    print(result)'''

    # write_file tests

    '''result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)

    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result)

    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result)'''

    # run_python_file tests

    result = run_python_file("calculator", "main.py")
    print(result)

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)

    result = run_python_file("calculator", "tests.py")
    print(result)

    result = run_python_file("calculator", "../main.py")
    print(result)

    result = run_python_file("calculator", "nonexistent.py")
    print(result)

    result = run_python_file("calculator", "lorem.txt")
    print(result)


if __name__ == "__main__":
    test()