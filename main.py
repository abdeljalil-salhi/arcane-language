from srcs.shell import run

if __name__ == "__main__":
    try:
        while True:
            line = input("imenox > ")
            result, error = run("<stdin>", line)
            print(error.as_string() if error else result)

    except KeyboardInterrupt:
        print("\nBye!")
        exit(0)
