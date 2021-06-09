grammar = """
S ->NPVP|NPVPS2
S2 ->CONJS2|CONJS
NP ->DETN|N|DETADJN|ADJN|DET N NP2 | N NP2 | DET ADJ N NP2 | ADJ N NP2
NP2 -> PP NP2 | CONJ NP NP2 | PP | CONJ NP
VP ->V | VNP|VNPNP|VPP|VCP|VPPCP|VVP2|V NP VP2 | V NP NP VP2 | V PP VP2 | V CP VP2 | V PP CP VP2
VP2 -> CONJ VP2 | CONJ VP
PP ->PNP
CP ->CS|CSCP2
CP2 -> CONJ CP
DET -> 'the' | 'an' | 'a' | 'my' | 'most'
CONJ -> 'or' | 'and'
P -> 'in' | 'with'
C -> 'that'
N -> 'cat' | 'cats' | 'dog' | 'dogs' | 'bone' | 'bones' | 'elephant' | 'elephants' | 'mouse' | 'mice' | 'pajamas' | 'garden' | 'morning'
ADJ -> 'wild' | 'small' | 'big'
V   -> 'sneezed' | 'giggled' | 'chased' | 'trumpeted' | 'saw' | 'shot' | 'played' | 'thought' | 'saw'
"""
sentences = [
    "the small mouse giggled",
    "the small mouse and the big elephant giggled",
    "the wild cat chased small mice in the garden",
    "the wild cat chased small mice in the garden with my elephant",
    "the wild cat chased small mice in the garden with a small bone with my elephant",
    "the wild cat chased small mice in the garden with my elephant and a dog",
    "the dog with the small bone chased small mice in the garden with my elephant and a dog",
    "the dog with the small bone chased small mice in the garden with my elephant and a dog and my mouse giggled",
    "the wild cat chased small mice in the garden with my elephant and a dog with a bone",
    "the wild cat chased small mice in the garden with my elephant and a dog with a bone in the garden",
    "the wild cat sneezed and chased small mice in the garden with my elephant",
    "the wild cat sneezed in the garden and chased small mice in the garden with my elephant",
    "the wild cat and most elephants sneezed in the garden and chased small mice in the garden with my elephant",
    "the wild cat sneezed in the garden and chased small mice in the garden with my elephant and a dog with a bone",
    "the wild dogs sneezed in the garden and most elephants with pajamas trumpeted",
    "the wild dogs sneezed with an elephant and a mouse in the garden and most elephants with pajamas trumpeted",
    "the wild dogs sneezed in the garden and most elephants with pajamas chased a mouse in the garden",
    "the wild dogs sneezed in the garden and most elephants with pajamas chased a mouse in the garden with a bone",
    "the wild dogs sneezed in the garden and most elephants with pajamas trumpeted and the mouse giggled",
    "the dog saw that the wild cat chased small mice in the garden with my elephant",
    "the dog and the elephant in my pajamas saw that the wild cat chased small mice in the garden with my elephant",
    "the small mouse and the wild dog thought in the garden that the elephant chased cats in the big garden with dogs with a bone",
    "the small mouse thought in the garden that the elephant chased cats in the big garden with dogs with a bone"
]
