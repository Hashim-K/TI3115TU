# Asks the user to input a number to perform the factorial calculation for
# @return: the number the user has input
def ask_factorial():
    number = -1
    while number < 0:
        print("Enter a number to find its factorial: ")
        try:
            number = int(input())
        except ValueError:
            print('The number should be an integer.')
        else:
            if number < 0:
                print('The number should be positive.')
    return number

# Calculates the factorial value of a number
# @param num: the number to calculate the factorial value for
# @return: the factorial value of given number
def calc_factorial(num):

    """Asks the factorial of a number.

      :param num: The number the factorial of which is to be found.
      :return: The factorial of num.
    """
    if num in (0, 1):
        fact = 1
    else:
        fact = 1
        while num > 1:
            fact *= num
            num -= 1
    print("result:", fact)

def main():
    number = ask_factorial()
    calc_factorial(number)

if __name__ == '__main__':
    main()
