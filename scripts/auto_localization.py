import regex
import os
import apply_script as pdx_parser
import codecs
from shared_functions import *

def remove_prefix(ethos):
    return ethos.replace("ethos_", "")

langs = ["english", "french", "german", "korean", "russian", "simp_chinese", "spanish"]
patterns = {
    "tradition" : {
        "english": ' cannot_have_{tradition}:0 "$cannot_combine_tradition_trigger_desc$ #high${tradition}_name$#!"\n',
        "french": ' cannot_have_{tradition}:0 "$cannot_combine_tradition_trigger_desc$ #high${tradition}_name$#!"\n',
        "german": ' cannot_have_{tradition}:0 "$cannot_combine_tradition_trigger_desc$ #high${tradition}_name$#!"\n',
        "korean": ' cannot_have_{tradition}:0 "$cannot_combine_tradition_trigger_desc$ #high${tradition}_name$#!"\n',
        "russian": ' cannot_have_{tradition}:0 "$cannot_combine_tradition_trigger_desc$ #high${tradition}_name$#!"\n',
        "simp_chinese": ' cannot_have_{tradition}:0 "$cannot_combine_tradition_trigger_desc$#high${tradition}_name$#!"\n',
        "spanish": ' cannot_have_{tradition}:0 "$cannot_combine_tradition_trigger_desc$ #high${tradition}_name$#!"\n'
    },
    "one_ethos" : {
        "english": ' not_{se1}_desc:0 "The [culture|E] does not have the ${e1}_name$ [ethos|E]"\n',
        "french": ' not_{se1}_desc:0 "La [culture|El] n’a pas la [ethos|El] ${e1}_name$"\n',
        "german": ' not_{se1}_desc:0 "Die [culture|E] hat nicht das [ethos|E] ${e1}_name$."\n',
        "korean": ' not_{se1}_desc:0 "[culture|E]가 ${e1}_name$ [ethos|E]을 보유하지 않음"\n',
        "russian": """ not_{se1}_desc:0 "[culture|E] не обладает [Concept( 'trait', 'свойством' )|E] «${e1}_name$»"\n""",
        "simp_chinese": ' not_{se1}_desc:0 "该[culture|E]没有${e1}_name$的[ethos|E]"\n',
        "spanish": ' not_{se1}_desc:0 "La [culture|lE] no tiene la [ethos|lE] ${e1}_name$"\n'
    },
    "two_ethos" : {
        "english": ' not_{se1}_or_{se2}_desc:0 "The [culture|E] does not have the ${e1}_name$ or ${e2}_name$ [ethos|E]"\n',
        "french": ' not_{se1}_or_{se2}_desc:0 "La [culture|El] n’a pas la [ethos|El] ${e1}_name$ ou ${e2}_name$"\n',
        "german": ' not_{se1}_or_{se2}_desc:0 "Die [culture|E] hat nicht das [ethos|E] ${e1}_name$ oder ${e2}_name$."\n',
        "korean": ' not_{se1}_or_{se2}_desc:0 "[culture|E]가 ${e1}_name$ 또는 ${e2}_name$ [ethos|E]을 보유하지 않음"\n',
        "russian": """ not_{se1}_or_{se2}_desc:0 "[culture|E] не обладает [Concept( 'ethos', 'моральным принципом' )|E] ${e1}_name$ или ${e2}_name$"\n""",
        "simp_chinese": ' not_{se1}_or_{se2}_desc:0 "该[culture|E]没有${e1}_name$或${e2}_name$的[ethos|E]"\n',
        "spanish": ' not_{se1}_or_{se2}_desc:0 "La [culture|lE] no tiene la [ethos|lE] ${e1}_name$ o ${e2}_name$"\n'
    },
    "three_ethos" : {
        "english": ' not_{se1}_{se2}_or_{se3}_desc:0 "The [culture|E] does not have the ${e1}_name$, ${e2}_name$ or ${e3}_name$ [ethos|E]"\n',
        "french": ' not_{se1}_{se2}_or_{se3}_desc:0 "La [culture|El] n’a pas la [ethos|El] ${e1}_name$, ${e2}_name$ ou ${e3}_name$"\n',
        "german": ' not_{se1}_{se2}_or_{se3}_desc:0 "Die [culture|E] hat nicht das [ethos|E] ${e1}_name$, ${e2}_name$ oder ${e3}_name$."\n',
        "korean": ' not_{se1}_{se2}_or_{se3}_desc:0 "[culture|E]가 ${e1}_name$, ${e2}_name$, 또는 ${e3}_name$ [ethos|E]을 보유하고 있지 않음"\n',
        "russian": """ not_{se1}_{se2}_or_{se3}_desc:0 "[culture|E] не обладает [Concept( 'ethos', 'моральным принципом' )|E] ${e1}_name$, ${e2}_name$ или ${e3}_name$"\n""",
        "simp_chinese": ' not_{se1}_{se2}_or_{se3}_desc:0 "该[culture|E]没有${e1}_name$、${e2}_name$或${e3}_name$的[ethos|E]"\n',
        "spanish": ' not_{se1}_{se2}_or_{se3}_desc:0 "La [culture|lE] no tiene la [ethos|lE] ${e1}_name$, ${e2}_name$ o ${e3}_name$"\n'
    },
    "trait" : {
        "english": """ culture_parameter_{trait}_trait_more_common:0 "The [GetTrait('{trait}').GetName( GetNullCharacter )] [trait|E] is more common"\n""",
        "french": """ culture_parameter_{trait}_trait_more_common:0 "Le [trait|El] [GetTrait('{trait}').GetName( GetNullCharacter )|l] est plus courant"\n""",
        "german": """ culture_parameter_{trait}_trait_more_common:0 "Die [trait|E] [GetTrait('{trait}').GetName(GetNullCharacter)] ist verbreiteter."\n""",
        "korean": """ culture_parameter_{trait}_trait_more_common:0 "[GetTrait('{trait}').GetName( GetNullCharacter )] [trait|E]이 좀 더 흔하게 나타남"\n""",
        "russian": """ culture_parameter_{trait}_trait_more_common:0 "[trait|E] «[GetTrait('{trait}').GetName( GetNullCharacter )]» встречается чаще"\n""",
        "simp_chinese": """ culture_parameter_{trait}_trait_more_common:0 "[GetTrait('{trait}').GetName( GetNullCharacter )][trait|E]更加常见"\n""",
        "spanish": """ culture_parameter_{trait}_trait_more_common:0 "El [trait|lE] [GetTrait('{trait}').GetName( GetNullCharacter )] es más común"\n"""
    }
}

for lang in langs:
    output = f"l_{lang}:\n"
    for tradition in get_names_from_files("..\\common\\culture\\traditions"):
        output += patterns["tradition"][lang].format(tradition=tradition)

    ethoses = list(get_names(pdx_parser.parse_file(os.path.join(game_path,"common\\culture\\pillars\\00_ethos.txt"))))

    for e1 in ethoses:
        output += patterns["one_ethos"][lang].format(e1=e1, se1=remove_prefix(e1))
        for e2 in filter(lambda x: x != e1, ethoses):
            output += patterns["two_ethos"][lang].format(e1=e1, se1=remove_prefix(e1), e2=e2, se2=remove_prefix(e2))
            for e3 in filter(lambda x: x != e1 and x != e2, ethoses):
                output += patterns["three_ethos"][lang].format(e1=e1, se1=remove_prefix(e1), e2=e2, se2=remove_prefix(e2), e3=e3, se3=remove_prefix(e3))

    for trait in get_names_from_files(os.path.join(game_path,"common\\traits")):
        output += patterns["trait"][lang].format(trait=trait)

    write_output(f"../localization/{lang}", f"trex_machine_generated_l_{lang}.yml", output)


