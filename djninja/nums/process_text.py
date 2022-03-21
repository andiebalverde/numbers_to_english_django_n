from nums.models import NumToEnglishResponse

first_set = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
             6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
             11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
             15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen'}
tens_set = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
large_numbers = {4: 'thousand', 5: 'thousand', 6: 'thousand', 7: 'million', 8: 'million', 9: 'million', 10: 'billion',
                 11: 'billion', 12: 'billion', 13: 'trillion', 14: 'trillion', 15: 'trillion'}


def manage_number(number):
    if number < 0 or number > 1000000000000000:
        return NumToEnglishResponse(**{'status': "Fail", 'num_in_english': "Number Out Of Supported Range for MVP. "
                                                                           "Expects (+) Integer under Quadrillion"})
    texted = NumToEnglishResponse(**{'status': "ok", 'num_in_english': ""})
    full_number = ""
    _, groups_remainder = divmod(len(str(number)), 3)

    for _ in reversed(range(len(str(number))+1)):
        if groups_remainder == 2:  # We have two digits above comma (10-99), let's convert to text and type it.
            typing = two_digits_to_text(int(str(number)[0:2]))
            if len(str(number)) > 3:  # Still a large number, i.e.: the 10-99 will be followed by thousand or million.
                typing += " " + large_numbers[len(str(number))]
            else:  # This 10-99 number we just typed, is our final word.
                full_number += typing
                break
                #texted.num_in_english = full_number
                #return texted
            number = str(number)[2:]  # We've processed two digits, let's continue with number trimmed by 2.
        elif groups_remainder == 1:  # We have one digit above comma (1-9), let's convert it to text and type it.
            typing = two_digits_to_text(int(str(number)[0]))
            if len(str(number)) > 3:  # Let's add thousand/million. Otherwise, we are already done typing.
                typing += " " + large_numbers[len(str(number))]
            number = str(number)[1:]
        elif groups_remainder == 0:  # We have hundreds here (100-999), let's convert it to text and type it.
            typing = two_digits_to_text(int(str(number)[0]))
            if len(str(number)) > 3 and str(number)[1:3] == '00':  # Type Thousand after hundred only for exact hundred
                typing += " " + "hundred " + large_numbers[len(str(number))]  # I.e: 100,000 is one hundred thousand
            else:  # I.e: 101,000 the word thousand doesn't go immediately after hundred.
                typing += " " + "hundred"  # I.e: 101,000 is one hundred one thousand (not 'hundred thousand' string).
            number = str(number)[1:]
        number = number.lstrip('0')  # Let's make sure our remaining integer to process doesn't start with zeros.

        if number == '':  # When stripping, if all remaining digits were zeros, we are done
            full_number += typing + " "
            texted.num_in_english = full_number
            return texted

        full_number += typing + " "  # Let's concatenate what we just processed into our partial full number
        _, groups_remainder = divmod(len(str(number)), 3)

    texted.num_in_english = full_number  # We'll return an instance of our pydantic output model.
    return texted


def two_digits_to_text(number):  # Converts first 99 numbers into text according to above mappings.
    if 0 <= number <= 19:
        return first_set[number]
    elif 20 <= number <= 99:
        tens, remainder = divmod(number, 10)
        processed = tens_set[tens-2] + " " + first_set[remainder] if remainder else tens_set[tens-2]
    else:
        processed = 'Number out of valid range for current version'

    return processed


if __name__=='__main__':  # Use for standalone testing.
    print(manage_number(6008009241228))