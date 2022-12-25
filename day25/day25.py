numbers = [l.strip() for l in open('input.txt')]

def snafu_to_dec(number):
    num = 0
    for i, n in enumerate(reversed(number)):
        if n == '-':
            n = -1
        elif n == '=':
            n = -2
        else:
            n = int(n)
        num += n * 5**i
    return num

def dec_to_snafu(number):
    digit_map = {-1: '-', -2: '='}
    digits = []
    carry = 0
    while number > 0:
        digit = number % 5 + carry
        if digit <= 2:
            digit = str(digit)
            carry = 0
        else:
            digit = digit_map[digit - 5]
            carry = 1
        digits.append(digit)
        number //= 5
    return ''.join(reversed(digits))

total = 0
for n in numbers:
    total += snafu_to_dec(n)

print(dec_to_snafu(total))
