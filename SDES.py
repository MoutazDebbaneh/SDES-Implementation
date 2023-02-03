import random


def prompt_choices(options):
    choice = None
    value = None
    choices = len(options)
    valid_inputs = [str(i) for i in range(choices)]

    while (True):
        print('\nSelect an option:')
        for i in range(choices):
            print(f'{i}) {options[i]}')
        inp = input()
        if inp in valid_inputs:
            return int(inp)


def prompt_value(msg, validate, cast):
    while (True):
        inp = input('\n' + msg)
        try:
            choice = cast(inp)
            if not validate(choice):
                continue
            return choice
        except:
            continue


def get_user_input():
    decrypt = bool(prompt_choices(['Encrypt', 'Decrypt']))
    loop_count = prompt_value(
        'Enter loop count (min count = 1): ', lambda x: x > 1, int)
    manual_key = bool(prompt_choices(['Generate Random Key', 'Manual']))

    key = None

    if manual_key:
        key = prompt_value('Enter binary key (min length = 8): ',
                           lambda x: len(x) >= 8 and set(x) in [{'0', '1'}, {'0'}, {'1'}], str)

    else:
        key_length = prompt_value(
            'Enter key length (min length = 8): ', lambda x: x > 8, int)

        def rand_key(p):
            key = ""
            for _ in range(p):
                temp = str(random.randint(0, 1))
                key += temp
            return (key)

        key = rand_key(key_length)

    value = prompt_value('Enter a 12-bit binary message to encrypt/decrypt: ',
                         lambda x: len(x) == 12 and set(x) in [{'0', '1'}, {'0'}, {'1'}], str)

    return decrypt, loop_count, key, value


if __name__ == "__main__":
    print('\n***********************************************************')
    print('***********************************************************')
    print('***** Simplified DES Implementation - Moutaz Debbaneh *****')
    print('***********************************************************')
    print('***********************************************************\n')

    decrypt, loop_count, key, value = get_user_input()
    print(key)
