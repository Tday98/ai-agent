from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

test_path = "calculator"

""" test_cases = [(get_files_info(test_path, "."), "current"),
            (get_files_info(test_path, "pkg"), "'pkg'"),
            (get_files_info(test_path, "/bin"), "'/bin'"),
            (get_files_info(test_path, "../"), "'/'")]
print("\n\nRunning tests...\n\n")
for test, entry in test_cases:
    print(f"Results for {entry} directory:")
    if isinstance(test, str):
        print(test + "\n")
    else:
        for line in test:
            print(line)
    print() """

# print(get_file_content(test_path, "lorem.txt"))

""" test_cases = [get_file_content(test_path, "main.py"),
            get_file_content(test_path, "pkg/calculator.py"),
            get_file_content(test_path, "/bin/cat"),
            get_file_content(test_path, "pkg/does_not_exist.py")]
print("\n\nRunning tests...\n\n")
for test in test_cases:
    print(test) """

""" test_cases = [write_file(test_path, "lorem.txt", "wait, this isn't lorem ipsum"),
        write_file(test_path, "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        write_file(test_path, "/tmp/temp.txt", "this should not be allowed")]

print("\n\nRunning tests...\n\n")
for test in test_cases:
    print(test) """

test_cases = [run_python_file("calculator", "main.py"),
            run_python_file("calculator", "main.py", ["3 + 5"]), 
            run_python_file("calculator", "tests.py"),
            run_python_file("calculator", "../main.py"), 
            run_python_file("calculator", "nonexistent.py")]

print("\n\nRunning tests...\n\n")
for test in test_cases:
    print(test)