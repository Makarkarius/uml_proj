from typing import List

from core.model import Class, Link, Acts


def encode_class_diagram(classes: List[Class], links: List[Link]):
    ans = "@startuml\n"
    for c in classes:
        ans += f'{c.type} {c.name} ' + '{\n'
        for m in c.mts:
            ans += f'{md_mapper[m.md]} {m.tp} {m.name}({m.params})\n'
        for f in c.flds:
            ans += f'{md_mapper[f.md]} {f.tp} {f.name}\n'
        ans += '}\n'
    for l in links:
        link = cd_links_mapper[l.tp]
        if not link:
            continue
        ans += l.cl1
        if l.left:
            ans += f' "{l.left}" '
        ans += ' '
        ans += link
        if l.right:
            ans += f' "{l.right}" '
        ans += l.cl2
        ans += ' '
        if l.comm:
            ans += f' :{l.comm}'
        ans += '\n'

    return ans + "@enduml"


def encode_acts_diagram(acts: Acts):
    ans = "@startuml\n"
    if acts.system_name:
        ans += f"rectangle {acts.system_name}" + '{\n'
    for a in acts.actions:
        ans += f'({a[0]}) as {a[1]}\n'
    if acts.system_name:
        ans += '}\n'
    for a in acts.actors:
        ans += f':{a[0]}: as {a[1]}\n'
    for l in acts.linkActs:
        link = act_mapper[l.tp]
        if not link:
            continue
        ans += f'{l.a1} {link} {l.a2}'
        if l.comm:
            ans += f':{l.comm}'
        ans += '\n'
    return ans + "@enduml"


act_mapper = {
    'ничего': '',
    'использование': '-->',
    'наследование': '<|--',
}

md_mapper = {
    'private': '-',
    'protected': '#',
    'package private': '~',
    'public': '+',
    'отсутсвует': '',
}

cd_links_mapper = {
    'агрегация': 'o--',
    'композиция': '*--',
    'наследование': '<|--',
    'ассоциация': '<--',
    'связь': '--',
    'без связи': ''
}
