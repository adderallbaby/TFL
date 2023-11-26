import sys

import CNF2PREFIX


def define_type(rule):
    for i in rule:
        if i.isalpha() and i.islower():
            return 'finite'
    return 'not finite'


def main(CNF):
    rules = CNF.split('\n')
    new_rules = []
    for rule in rules:
        if rule == '':
            continue

        end = rule.split('->')[1].strip()
        if end == '':
            new_rules.append(rule + '\n')
            continue
        rule_type = CNF2PREFIX.define_typee(rule)
        if rule_type == 'not finite':
            start = rule.split('->')[0].strip()
            end = rule.split('->')[1].split()
            if len(end) == 1:
                new_rules.append(rule + '\n')
            else:
                new_rules.append(f'{start} -> {end[1]} {end[0]}\n')
        else:
            new_rules.append(rule + '\n')
    return ''.join(new_rules)


if __name__ == '__main__':
    main(sys.argv[1])
