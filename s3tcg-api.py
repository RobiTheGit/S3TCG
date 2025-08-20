#!/usr/bin/python3

# Sonic 3 Title Card Mappings Code Generator API
# This is not intended to be a standalone program, but the base code for generating the mappings
# May be compatible for website usage



DisasmLabel = 0 # Determine if we want to use generic TC_XXZ names or the disasm labels
global XPOS, INDEX
XPOS = 0
INDEX = 0


def Generate(TextToGenerate):
    REGEX_STEP = ''
    for CHARACTER in TextToGenerate:
        if CHARACTER.isalpha() or CHARACTER == " ":
            REGEX_STEP += CHARACTER # remove unmapped characters

    
    LENGTH_STEP = REGEX_STEP.replace(" ", "")
    CHARS_STEP = list(dict.fromkeys(list(LENGTH_STEP.upper().replace("E","").replace("N","").replace("O","").replace("Z",""))))
    print(CHARS_STEP)
    L_STEP_HEX = hex(len(LENGTH_STEP)).upper()
    POS_AFTER_0 = False    
    if len(REGEX_STEP) <= 8:
        POS_AFTER_0 = True
    StartLoc = [0x70,0x60,0x50,0x40,0x30,0x20, 0x10, 0x00, 0xFFF0, 0xFFE0, 0xFFD0, 0xFFC0, 0xFFB0, 0xFFA0, 0xFF90] # still the Sonic 2 ones here

    XPOS = StartLoc[len(REGEX_STEP)]
    INDEX = 0x54D
    WIDTH = 0x6
    INDECIES = []
    CURR_CHAR = ''
    ALL_CHAR = []
    USED_CHARS = []
    OUTPUT = []
    OUTPUT.append(f"Map: dc.w {L_STEP_HEX.replace('0X', '$')}")
    for CURR_CHAR in REGEX_STEP:
        ALL_CHAR.append(CURR_CHAR.upper())
#=================================================================
#  End of variable setup
#=================================================================
    for CURR_CHAR in ALL_CHAR:
# Set up some letter variables
        if XPOS > 0xFFFF:
            XPOS -= 0x10000
        if CURR_CHAR in USED_CHARS and CURR_CHAR != "Z"  and CURR_CHAR != "O"  and CURR_CHAR != "N"  and CURR_CHAR != "E" :
         
            REUSED_CHAR = USED_CHARS.index(CURR_CHAR)
            REUSED_INDEX = INDECIES[REUSED_CHAR]
            OUTPUT.append(f"\t" + REUSED_INDEX + f" {hex(XPOS).replace('0x', '$').upper()} ;{CURR_CHAR}")
            if CURR_CHAR == "I" or CURR_CHAR == "L" or CURR_CHAR == "J":
                XPOS += 0x8
            elif CURR_CHAR == "M" or CURR_CHAR == "W" or CURR_CHAR == "Q":
                XPOS += 0x9
            else:
                XPOS += 0x10
        elif CURR_CHAR == "I" or CURR_CHAR == "L" or CURR_CHAR == "J":
            WIDTH = 0x2
            OUTPUT.append(f"\tdc.w {hex(WIDTH).replace('0x', '$').upper()}, {hex(INDEX+0x8000).replace('0x', '$').upper()}, {hex(XPOS).replace('0x', '$').upper()} ;{CURR_CHAR}")
            USED_CHARS.append(CURR_CHAR)
            INDECIES.append(f"dc.w {hex(WIDTH).replace('0x', '$').upper()}, {hex(INDEX+0x8000).replace('0x', '$').upper()},")
            XPOS += 0x8
            INDEX += 0x3
        elif CURR_CHAR == "M" or CURR_CHAR == "W" or CURR_CHAR == "Q":
            WIDTH = 0xA
            INDECIES.append(f"dc.w {hex(WIDTH).replace('0x', '$').upper()}, {hex(INDEX+0x8000).replace('0x', '$').upper()},")
            USED_CHARS.append(CURR_CHAR)
            OUTPUT.append(f"\tdc.w {hex(WIDTH).replace('0x', '$').upper()}, {hex(INDEX+0x8000).replace('0x', '$').upper()}, {hex(XPOS).replace('0x', '$').upper()} ;{CURR_CHAR}")
            XPOS += 0x18
            INDEX += 0x9

        elif CURR_CHAR == "Z":

            OUTPUT.append(f"\tdc.w $6, $8531, {hex(XPOS).replace('0x', '$').upper()} ;Z")
            XPOS += 0x10
        elif CURR_CHAR == "O":

            OUTPUT.append(f"\tdc.w $A, $8528, {hex(XPOS).replace('0x', '$').upper()} ;O")
            XPOS += 0x18
        elif CURR_CHAR == "N":

            OUTPUT.append(f"\tdc.w $6, $8522, {hex(XPOS).replace('0x', '$').upper()} ;N")
            XPOS += 0x10
        elif CURR_CHAR == "E":

            OUTPUT.append(f"\tdc.w $6, $851C, {hex(XPOS).replace('0x', '$').upper()} ;E")
            XPOS += 0x10
        elif CURR_CHAR == " " or CURR_CHAR == "":        
            OUTPUT.append("")
            XPOS += 0x10
        
        else:
            WIDTH = 0x6
            USED_CHARS.append(CURR_CHAR)
            INDECIES.append(f"dc.w {hex(WIDTH).replace('0x', '$').upper()}, {hex(INDEX+0x8000).replace('0x', '$').upper()},")

            OUTPUT.append(f"\tdc.w {hex(WIDTH).replace('0x', '$').upper()}, {hex(INDEX+0x8000).replace('0x', '$').upper()}, {hex(XPOS).replace('0x', '$').upper()} ;{CURR_CHAR}")
            XPOS += 0x10
            INDEX += 0x6

    for x in OUTPUT:
        print(x)
    Data = []
    char = ''
    for char in CHARS_STEP:
        char_bin = open(f'Letters/{char}_Unc.bin','rb') #hopefully this works on windows, 'cause these are linux paths
        Data.append(char_bin.read())
        char_bin.close()

    try:
        Uncompressed_Art = open("output.bin", "xb")   
    except:
        Uncompressed_Art = open("output.bin", "wb")
    for x in Data:
        Uncompressed_Art.write(x)
#TODO; compress the art for S3 and maybe even SCE here
    
if __name__ == "__main__":
    Generate(input("Zone Name (Art will be in output.bin as uncompressed): "))
