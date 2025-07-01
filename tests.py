from functions.run_python import run_python_file

def test():
    # test 1, pass
    print(run_python_file("calculator", "main.py"))

    # test 2, pass
    print(run_python_file("calculator", "tests.py"))

    # test 3, fail
    print(run_python_file("calculator", "../main.py"))

    # test4, fail
    print(run_python_file("calculator", "nonexistent.py"))

if __name__ == "__main__":
    test()