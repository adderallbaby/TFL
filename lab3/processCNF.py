import CNF2PREFIX
def main(CNF):
    counter = 100
    new_rules = []
    rules = CNF.split('\n')
    for rule in rules:
        rule_type = CNF2PREFIX.define_typee(rule)
        if rule_type == 'not finite':

            if rule == 'S0 -> ' or rule == 'S0 ->':
                new_rules.append(rule + '\n')
            else:
                if not rule == '':
                    parts = rule.split('->')

                    start = parts[0]
                    end = parts[1]
                    alt = end.split('|')
                    if len(alt) > 1:
                        new_rules.append(f'{start} -> {alt[0]}| \n')
                        new_rules.append(f'{start} -> {alt[1]}\n')
                    else:
                        new_rules.append(rule + '\n')
        else:
            if rule_type == 'weird' and not rule == '':
                parts = rule.split('->')
                end = parts[1]
                right = end.split() 
                if len(right) == 1:
                    new_rules.append(rule[:-1] + f' Q{counter}' + '\n')
                    new_rules.append(f'Q{counter} -> \n')
                else:
                    new_rules.append(rule + '\n')
            else:
                new_rules.append(rule + '\n')
    return ''.join(new_rules)


def start_to_top(grammar):
    a = []
    rules = grammar.split('\n')
    for rule in rules:
        start = rule.split('->')[0].strip()
        if start == 'S':
            a = [rule]
            rules.remove(rule)
            break 
    a.extend(rules)
    string = ''
    for i in a:
        string += i + '\n'
    return string


