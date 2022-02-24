import regex
import os
import apply_script as pdx_parser
import codecs
from shared_functions import *

localization_key_pattern = regex.compile(r"localization_key\s*=\s*(\w+)")
comment_pattern = regex.compile(r"(#)[^\n]*")

output = "l_english:\n"
for tradition in map(lambda x: x[0], join_files("..\\common\\culture\\traditions", "txt")):
    output += f' cannot_have_{tradition}:0 "$cannot_combine_tradition_trigger_desc$ #high ${tradition}_name$#!"\n'

write_output("../localization/english", "trex_machine_generated_l_english.yml", output)


