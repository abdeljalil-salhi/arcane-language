from srcs.shell import run

if __name__ == "__main__":
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
