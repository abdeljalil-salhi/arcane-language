from srcs.basic import run

if __name__ == '__main__':
    while True:
        line = input("basic > ")
        result, error = run('<stdin>', line)
        
        if error:
            print(error.as_string())
        else:
            print(result)
        