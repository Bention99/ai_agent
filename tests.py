from functions.get_files_info import *
from functions.get_files_content import *

def test():
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

    '''result = get_files_content("calculator", "lorem.txt")
    print(result)'''

    result = get_files_content("calculator", "main.py")
    print(result)

    result = get_files_content("calculator", "pkg/calculator.py")
    print(result)

    result = get_files_content("calculator", "/bin/cat")
    print(result)

    result = get_files_content("calculator", "pkg/does_not_exist.py")
    print(result)



if __name__ == "__main__":
    test()