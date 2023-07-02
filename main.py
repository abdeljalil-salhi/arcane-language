from srcs.basic import run

if __name__ == "__main__":
    try:
        while True:
            line = input("basic > ")
            result, error = run("<stdin>", line)

            if error:
                print(error.as_string())
            else:
                print(result)
    except KeyboardInterrupt:
        print("\nBye!")
        exit(0)
