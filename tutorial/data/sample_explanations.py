from babble import Explanation

aliases = {
    'spouse':  ['spouse', 'wife', 'husband', 'ex-wife', 'ex-husband'],
    'family':  ['father', 'father', 'mother', 'sister', 'sisters',
                'brother', 'brothers', 'son', 'sons', 'daughter', 'daughters',
                'grandfather', 'grandmother', 'uncle', 'uncles', 'aunt', 'aunts',
                'cousin', 'cousins'],
    'friend':  ['boyfriend', 'girlfriend', 'boss', 'employee', 'secretary', 'co-worker'],
    }
aliases['family'] += ["{}-in-law".format(f) for f in aliases['family']]

explanations = [
    Explanation(
        name='LF_and_married',
        condition="the word 'and' is between X and Y and 'married' within five words of Y",
        candidate='1bcd8648-8a80-47a3-82d4-38a4a594092f::span:1223:1228~~1bcd8648-8a80-47a3-82d4-38a4a594092f::span:1234:1238',
        label=1),
    Explanation(
        name='LF_third_wheel',
        condition="there is a person between X and Y",
        candidate='6cd34ab0-653b-438e-b966-d7365a31651d::span:595:607~~6cd34ab0-653b-438e-b966-d7365a31651d::span:712:719',
        label=2),
    Explanation(
        name='LF_married_two_people',
        condition="the word 'married' is in the sentence and there are only two people in the sentence",
        candidate='d535c921-f102-4d3b-9891-5a36ed93259e::span:823:830~~d535c921-f102-4d3b-9891-5a36ed93259e::span:836:839',
        label=1),
    Explanation(
        name='LF_same_person',
        condition="X and Y are identical",
        candidate='3820d641-7d5a-49d0-a872-b13199b50790::span:2392:2395~~3820d641-7d5a-49d0-a872-b13199b50790::span:2413:2416',
        label=2),
    Explanation(
        name='LF_husband_wife',
        condition="there is at least one spouse word between X and Y",
        candidate='88eb2437-93ce-452d-ada0-905a90d0ccac::span:1467:1468~~88eb2437-93ce-452d-ada0-905a90d0ccac::span:1478:1488',
        label=1),
    Explanation(
        name='LF_husband_wife_left_window',
        condition="there is at least one spouse word within two words to the left of X or Y",
        candidate='03a1e1a0-93c3-41a8-a905-a535ce8f2b09::span:6822:6837~~03a1e1a0-93c3-41a8-a905-a535ce8f2b09::span:6855:6858',
        label=1),
    Explanation(
        name='LF_familial_relationship',
        condition="there is at least one family word between X and Y",
        candidate='17f7cc87-c207-48e1-a0b3-96ca8047250d::span:3474:3477~~17f7cc87-c207-48e1-a0b3-96ca8047250d::span:3570:3574',
        label=2),
    Explanation(
        name='LF_family_left_window',
        condition="there is a family word within two words to the left of X or Y",
        candidate='ca285806-f17c-4b1e-9459-a6a7cc27f80c::span:12981:12995~~ca285806-f17c-4b1e-9459-a6a7cc27f80c::span:13014:13018',
        label=2),
    Explanation(
        name='LF_other_relationship',
        condition="there is at least one friend word between X and Y",
        candidate='41b546d5-d525-4d0a-9fbe-f173e20b645a::span:456:469~~41b546d5-d525-4d0a-9fbe-f173e20b645a::span:554:564',
        label=2),
    Explanation(
        name='LF_reporters',
        condition='A word in the sentence starts with "report"',
        candidate='0023c4a1-446c-488e-949a-1edbbb4354b3::span:12569:12578~~0023c4a1-446c-488e-949a-1edbbb4354b3::span:12584:12594',
        label=2),
]