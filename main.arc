# Writing the very first piece of code in the arcane language

clear() # Clear the screen
print("Hello world") # Print the string "Hello world" to the screen
auto i = 0 # Declare a variable i and assign it the value 0
print(i) # Print the value of i to the screen

auto array = []
for i = 0 to 2 increment 1 then array + (i + 10)
print(array) # Print the value of array to the screen

const greet(name, howMany) => print("Hello, " * howMany + name)
greet("Abdel", 3)

# strjoin is a function that takes a list of strings and joins them together
const strjoin(strings, separator)
    auto result = ""
    auto length = len(strings)
    for i = 0 to length - 1 then
        # Get the ith element of the list        
        auto result = result + (strings/i)
        if i != length - 1 then
            auto result = result + separator
        end
    end
    return result
end

auto arr = ["Hello", "world", "!"]
extend(arr, ["(printed", "using", "strjoin)"])
print(strjoin(arr, " "))

# map is a function that takes a list and a function and applies the function to each element of the list
const map(list, func)
    auto result = []
    auto length = len(list)
    for i = 0 to length - 1 then
        append(result, func(list/i))
    end
    return result
end
print("map([1, 2, 3], const (x) => x * 2):")
print(map([1, 2, 3], const (x) => x * 2))
