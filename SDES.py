import random
import numpy as np


def prompt_choices(options):
    '''
        Prompts the user to enter one option out of a list of options. Prompts again in case of invalid input.
    '''
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
    '''
        Prompts the user to enter a single value.\n
        Expects a validate function to validate the entered value, and a cast function to cast input to a specific type.
    '''
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
    '''
        Prompts the user to enter all the required parameters.
    '''
    decrypt = bool(prompt_choices(['Encrypt', 'Decrypt']))
    loop_count = prompt_value(
        'Enter loop count (min count = 1): ', lambda x: x >= 1, int)

    manual_key = True if decrypt else bool(
        prompt_choices(['Generate Random Key', 'Manual']))

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


def get_subkey(i, key):
    '''
        Extracts subkey K_i from the given encryption key.
    '''
    ind = i - 1
    bits_list = [*key]
    array = np.array(bits_list)
    array = np.roll(array, -ind)
    sub_key_bits = list(array[:8])
    return ''.join(sub_key_bits)


def expand(binary_string):
    '''
        Exapnds a 6-bit binary string to 8-bit binary string using the fixed expansion indicies.
    '''
    expansion_list_indices = [1, 2, 4, 3, 4, 3, 5, 6]
    res = ''
    for ind in expansion_list_indices:
        res += binary_string[ind - 1]
    return res


def xor(a, b):
    '''
        Applys the XOR operator on two binary strings of the same length.
    '''
    res = ""
    for i in range(len(a)):
        if (a[i] == b[i]):
            res += "0"
        else:
            res += "1"
    return res


def f(R, K):
    '''
        The f function used in SDES.\n
        Exapnds Ri and then splits it to S1, S2 of 4-bits each.\n
        Finally, it uses S1/S2 Boxes to get two 3-bits binary strings.
    '''
    R_expanded = expand(R)
    res = xor(R_expanded, K)
    S1 = res[0:4]
    S2 = res[4:]

    S1_BOX = [['101', '010', '001', '110', '011', '100', '111', '000'],
              ['001', '100', '110', '010', '000', '111', '101', '011']]

    S2_BOX = [['100', '000', '110', '101', '111', '001', '011', '010'],
              ['101', '011', '000', '111', '110', '010', '001', '100']]

    S1_row_ind = int(S1[0])
    S1_col_ind = int(S1[1:], 2)
    S1_res = S1_BOX[S1_row_ind][S1_col_ind]

    S2_row_ind = int(S2[0])
    S2_col_ind = int(S2[1:], 2)
    S2_res = S2_BOX[S2_row_ind][S2_col_ind]

    return S1_res + S2_res


def SDES(decrypt, loop_count, key, value):
    '''
        Applies the Simplified Data Encryption Standard (SDES) on a value using an encryption key and a fixed loop count.
    '''
    print('\nUsing key:', key)
    L = []
    R = []

    L.append(value[0:6])
    R.append(value[6:])

    for i in range(1, loop_count + 1):
        K_i = get_subkey(loop_count + 1 - i,
                         key) if decrypt else get_subkey(i, key)
        L_i = R[i-1]
        R_i = xor(L[i-1], f(R[i-1], K_i))
        L.append(L_i)
        R.append(R_i)

    return R[-1] + L[-1]


if __name__ == "__main__":
    print('\n***********************************************************')
    print('***********************************************************')
    print('***** Simplified DES Implementation - Moutaz Debbaneh *****')
    print('***********************************************************')
    print('***********************************************************\n')

    decrypt, loop_count, key, value = get_user_input()
    res = SDES(decrypt, loop_count, key, value)
    print('\nOutput:', res)
