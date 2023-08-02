from srcs.shell import run

if __name__ == "__main__":
    try:
        while True:
            line = input("imenox > ").strip()
            if line == "":
                continue
            elif line == "exit":
                print("Bye!"), exit(0)
            result, error = run("<stdin>", line)
            if error:
                print(error.as_string())
            elif result and len(result.elements) > 1:
                print(repr(result))
            elif result:
                print(repr(result.elements[0]))

    except KeyboardInterrupt:
        print("\nBye!")
        exit(0)
