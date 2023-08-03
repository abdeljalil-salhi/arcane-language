from srcs.shell import run
from sys import argv

if __name__ == "__main__":
    if len(argv) > 1:
        for i in range(1, len(argv)):
            with open(argv[i], "r") as f:
                content = f.read()
            try:
                result, error = run(argv[i], content)
                if error:
                    print(error.as_string())
            except Exception as e:
                print(e.__class__.__name__ + ": " + str(e))
        exit(0)
    try:
        while True:
            line = input("imenox > ").strip()
            if line == "":
                continue
            elif line == "exit":
                print("Bye!"), exit(0)
            try:
                result, error = run("<stdin>", line)
                if error:
                    print(error.as_string())
            except Exception as e:
                print(e.__class__.__name__ + ": " + str(e))

    except KeyboardInterrupt:
        print("\nBye!")
        exit(0)
