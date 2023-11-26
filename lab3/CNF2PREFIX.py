import sys


def define_typee(rule):
    symbols = rule.split()
    if rule == '':
        return 'weird'
    counter = 0
    for char in symbols:
        if char.isalpha() and char.islower():
            counter += 1
    if counter >= 1 or len(symbols) == 2:
        return 'finite'
    else:
        parts = rule.split('->')
        right = parts[1].split()
        if len(right) == 1:
            return 'weird'
        return 'not finite'


def main(CNF):
    rules = CNF.split('\n')
    new_rules = ['S0 ->\n']
    if rules[0] == 'S ->':
        new_rules.append(rules[0] + '\n')
        rules = rules[1:]
    for rule in rules:
        if rule == '':
            continue
        parts = rule.split('->')
        start = parts[0].strip()
        end = parts[1].strip()
        rule_type = define_typee(rule)
        if rule_type == 'not finite':
            end = parts[1].split()
            new_rules.append(rule + '\n')
            new_rules.append(f'{start}0 -> {end[0]} {end[1]}0 | {end[0]}0\n')

        if rule_type == 'finite':
            end = parts[1].strip()

            new_rules.append(rule + '\n')
            new_rules.append(f'{start}0 -> {end} | \n')
    return ''.join(new_rules)


if __name__ == '__main__':
    main(sys.argv[1])
