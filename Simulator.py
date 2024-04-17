import time

reg = [['zero', '0x0001000', 0], ['ra', '0x0001001', 0], ['sp', '0x0001002', 256], ['gp', '0x0001003', 0], ['tp', '0x0001004', 0], ['t0', '0x0001005', 0], ['t1', '0x0001006', 0], ['t2', '0x0001007', 0], ['s0', '0x0001008', 0], ['s1', '0x0001009', 0], ['a0', '0x000100a', 0], ['a1', '0x000100b', 0], ['a2', '0x000100c', 0], ['a3', '0x000100d', 0], ['a4', '0x000100e', 0], ['a5', '0x000100f', 0], ['a6', '0x0001010', 0], ['a7', '0x0001011', 0], ['s2', '0x0001012', 0], ['s3', '0x0001013', 0], ['s4', '0x0001014', 0], ['s5', '0x0001015', 0], ['s6', '0x0001016', 0], ['s7', '0x0001017', 0], ['s8', '0x0001018', 0], ['s9', '0x0001019', 0], ['s10', '0x000101a', 0], ['s11', '0x000101b', 0], ['t3', '0x000101c', 0], ['t4', '0x000101d', 0], ['t5', '0x000101e', 0], ['t6', '0x000101f', 0]]
memory={
    "0x00010000":"0b00000000000000000000000000000000","0x00010004":"0b00000000000000000000000000000000","0x00010008":"0b00000000000000000000000000000000","0x0001000c":"0b00000000000000000000000000000000",
    "0x00010010":"0b00000000000000000000000000000000","0x00010014":"0b00000000000000000000000000000000","0x00010018":"0b00000000000000000000000000000000","0x0001001c":"0b00000000000000000000000000000000",
    "0x00010020":"0b00000000000000000000000000000000","0x00010024":"0b00000000000000000000000000000000","0x00010028":"0b00000000000000000000000000000000","0x0001002c":"0b00000000000000000000000000000000",
    "0x00010030":"0b00000000000000000000000000000000","0x00010034":"0b00000000000000000000000000000000","0x00010038":"0b00000000000000000000000000000000","0x0001003c":"0b00000000000000000000000000000000",
    "0x00010040":"0b00000000000000000000000000000000","0x00010044":"0b00000000000000000000000000000000","0x00010048":"0b00000000000000000000000000000000","0x0001004c":"0b00000000000000000000000000000000",
    "0x00010050":"0b00000000000000000000000000000000","0x00010054":"0b00000000000000000000000000000000","0x00010058":"0b00000000000000000000000000000000","0x0001005c":"0b00000000000000000000000000000000",
    "0x00010060":"0b00000000000000000000000000000000","0x00010064":"0b00000000000000000000000000000000","0x00010068":"0b00000000000000000000000000000000","0x0001006c":"0b00000000000000000000000000000000",
    "0x00010070":"0b00000000000000000000000000000000","0x00010074":"0b00000000000000000000000000000000","0x00010078":"0b00000000000000000000000000000000","0x0001007c":"0b00000000000000000000000000000000",  
}
prog_ln = 1

def dec_2_bin(dec, num_bits=32, bit_tp="signed"):
    if bit_tp=="unsigned":
        bina=bin(dec)[2:].zfill(num_bits)
        return bina
    if bit_tp in ("signed","1s"):
        if dec>=0:
            bina=dec_2_bin(dec, num_bits, "unsigned")
        else:
            bina=dec_2_bin(abs(dec), num_bits, "unsigned")
            bina=bina.replace("0", "2")
            bina=bina.replace("1", "0")
            bina=bina.replace("2", "1") 
        return bina
    if dec>=0:
        bina=bin(dec)[2:].zfill(num_bits)
    else:
        pos_bina=bin(abs(dec))[2:].zfill(num_bits)
        pos_bina=pos_bina.replace("0","2")
        pos_bina=pos_bina.replace("1","0")
        pos_bina=pos_bina.replace("2","1")
        inv_bina=pos_bina
        invval=bina_to_dec(inv_bina, "unsigned")
        bina=dec_2_bin(invval + 1, num_bits, "unsigned")
    return bina

def prin(reg):
    for i in reg:
        print(i[0],":",i[2])

def bina_to_dec(bina, bit_tp = "signed"):
    sum=0
    if bit_tp=="unsigned":
        for i in reversed(range(len(bina))):
            if bina[i]=="1":
                sum +=2**(len(bina)-1-i)
        return sum
    elif bit_tp in ("signed","1s"):
        if bina[0]=="1":
            bina=bina.replace("0", "2")
            bina=bina.replace("1", "0")
            bina=bina.replace("2", "1")
            return -bina_to_dec(bina, "unsigned")
        else:
            return bina_to_dec(bina, "unsigned")
    elif bit_tp=="2s":
        if bina[0]=="1":
            bina=bina.replace("0", "2")
            bina=bina.replace("1", "0")
            bina=bina.replace("2", "1")
            return -(bina_to_dec(bina,"unsigned") + 1)
        else:
            return bina_to_dec(bina,"unsigned")
    else:
        return bina_to_dec(bina,"signed")
def check_inst(inst_line):
    if (inst_line=="00000000000000000000000001100011"):
        return ["halt","bonus"]
    if (inst_line=="00000000000000000000000000000000"):
        return ["rst","bonus"]
    opcd=inst_line[-7:]
    funct3=inst_line[-15:-12]
    funct7=inst_line[:7]
    if opcd=="0000000" and funct3=="001":return ["rvrs","bonus"]
    if opcd=="0000000" and funct3=="011":return ["mul","bonus"]
    if opcd=="0110011":
        if funct3=="000":
            if funct7=="0000000":return ["add","r"]
            if funct7=="0100000":return ["sub","r"]
        if funct3=="001":return ["sll","r"]
        if funct3=="010":return ["slt","r"]
        if funct3=="011":return ["sltu","r"]
        if funct3=="100":return ["xor","r"]
        if funct3=="101":return ["srl","r"]
        if funct3=="110":return ["or","r"]
        if funct3=="111":return ["and","r"]
    if opcd=="0000011":return ["lw","i"]
    if opcd=="0010011":
        if funct3=="000":return ["addi","i"]
        if funct3=="011":return ["sltiu","i"]
    if opcd=="1100111":return ["jalr","i"]
    if opcd=="0100011":return ["sw","s"]
    if opcd=="1100011":
        if funct3=="000":return ["beq","b"]
        if funct3=="001":return ["bne","b"]
        if funct3=="100":return ["blt","b"]
        if funct3=="101":return ["bge","b"]
        if funct3=="110":return ["bltu","b"]
        if funct3=="111":return ["bgeu","b"]
    if opcd=="0110111":return ["lui","u"]
    if opcd=="0010111":return ["auipc","u"]
    if opcd=="1101111":return ["jal","j"]


def output(reg):
    bina_representations=[]
    for value in reg:
        if value[2]<0:bina_value = bin(value[2] & 0xFFFFFFFF)[2:] 
        else:bina_value=bin(value[2])[2:].zfill(32)
        bina_representations.append('0b' + bina_value +" ")
    return ''.join(bina_representations)

def detectregister(bina):return int(bina, 2)

def dec_to_two_unsigned_to_dec(dec):
    num_bits=32
    if dec>=0:bina=bin(dec)[2:].zfill(num_bits)
    else:
        pos_bina = bin(abs(dec))[2:].zfill(num_bits)
        inv_bina = ''.join('1' if bit =='0' else '0' for bit in pos_bina)
        bina = bin(int(inv_bina, 2) + 1)[2:].zfill(num_bits)
    deci = 0
    deci = int(bina, 2)
    return deci


def r_Type(inst_line , instruction, reg):
    global memory
    global prog_ln
    rd = inst_line[-12:-7]
    rs1 = inst_line[-20:-15]
    rs2 = inst_line[-25:-20]
    if instruction == "add":reg[detectregister(rd)][2] = reg[detectregister(rs1)][2] + reg[detectregister(rs2)][2] #sext
    if instruction == "sub":reg[detectregister(rd)][2] = reg[detectregister(rs1)][2] - reg[detectregister(rs2)][2]
    if instruction == "sll":
        value = reg[detectregister(rs2)][2]
        if value < 0:bina_value = bin(value & 0xFFFFFFFF)[2:] 
        else:bina_value = bin(value)[2:].zfill(32)
        x = bina_value [-5:]
        y = int(x, 2)
        result = reg[detectregister(rs1)][2] << y
        reg[detectregister(rs1)][2] = result
    if instruction == "srl":
        value = reg[detectregister(rs2)][2]
        if value < 0:bina_value = bin(value & 0xFFFFFFFF)[2:] 
        else:bina_value = bin(value)[2:].zfill(32)
        x = bina_value [-5:]
        y = int(x, 2)
        result = reg[detectregister(rs1)][2] >> y
        reg[detectregister(rs1)][2] = result
    if instruction == "slt":
        if reg[detectregister(rs1)][2] < reg[detectregister(rs2)][2]:reg[detectregister(rd)][2] =1
    if instruction == "sltu":
        if dec_to_two_unsigned_to_dec(reg[detectregister(rs1)][2]) < dec_to_two_unsigned_to_dec(reg[detectregister(rs2)][2]):reg[detectregister(rd)][2] =1
    if instruction == "xor" :reg[detectregister(rd)][2] = reg[detectregister(rs1)][2] ^reg[detectregister(rs2)][2]
    if instruction == "or" :reg[detectregister(rd)][2] = reg[detectregister(rs1)][2] | reg[detectregister(rs2)][2]
    if instruction == "and" :reg[detectregister(rd)][2] = reg[detectregister(rs1)][2] & reg[detectregister(rs2)][2]
    prog_ln += 1
    
def twos_complement_to_dec(bina):
    if bina[0] == '1':  
        inv_bina = ''.join('1' if bit == '0' else '0' for bit in bina)
        dec = -((int(inv_bina, 2)) + 1)
    else:dec = int(bina, 2)
    return dec

def dec_to_hexadec(dec):
    hexadec = hex(dec)[2:]  # Slice to remove '0x' prefix
    return hexadec

def s_Type(inst_line , instruction, reg):
    global prog_ln
    global memory
    if instruction == "sw":
        rs2 = inst_line[-25:-20]
        rs1 = inst_line[-20:-15]
        imm = str(inst_line[-32:-25])+str(inst_line[-12:-7])
        memory["0x000" + dec_to_hexadec((reg[detectregister(rs1)][2]+bina_to_dec(imm, "2s")))] = "0b"+dec_2_bin(reg[detectregister(rs2)][2], 32, "2s")
        prog_ln += 1

def out_mem():
    global memory
    stringval = ""
    for i in range (32):stringval += (f'0x000{str(dec_to_hexadec(65536+(4*i)))}:{memory[f"0x000{str(dec_to_hexadec(65536+(4*i)))}"]}') + "\n"
    print(stringval)
    return stringval

def j_Type(inst_line , instruction, reg):
    global prog_ln
    global memory
    rd = inst_line[-12:-7]
    imm = reverse(str(inst_line[1:11]))+str(inst_line[11])+reverse(str(inst_line[12:20]))+str(inst_line[0])
    imm = reverse(imm)
    immval = int(bina_to_dec(imm)/2)
    if instruction == "jal":
        reg[detectregister(rd)][2] = (prog_ln + 1)*4 # (storing address of next instruction as return address in rd)
        prog_ln = prog_ln + immval

def i_Type(inst_line, instruction, reg):
    global prog_ln
    global memory
    imm = inst_line[0:12]
    rs1 = inst_line[12:17]
    rd = inst_line[20:25]
    if instruction == "addi":
        reg[detectregister(rd)][2] = reg[detectregister(rs1)][2] + bina_to_dec(imm, "2s")
        prog_ln += 1
    elif instruction == "sltiu":
        if bina_to_dec(reg[detectregister(rs1)][2], "unsigned") < bina_to_dec(imm, "unsigned"):reg[detectregister(rd)][2] = 1
        else:reg[detectregister(rd)][2] = 0
        prog_ln += 1
    elif instruction == "lw":
        mc = memory["0x000" + dec_to_hexadec((reg[detectregister(rs1)][2]+bina_to_dec(imm, "2s")))]
        mc = mc.replace("0b", "")
        reg[detectregister(rd)][2] = bina_to_dec(mc, "2s")
        prog_ln += 1
    elif instruction == "jalr":
        reg[detectregister(rd)][2] = (prog_ln+1)*4
        prog_ln = int(reg[detectregister(rs1)][2]/4) + int(bina_to_dec(imm, "2s")/4)

def u_Type(inst_line , instruction, reg):
    global memory
    global prog_ln
    rd = inst_line[-12:-7]
    if instruction=="auipc":reg[detectregister(rd)][2] = detectregister(inst_line[:-12]+'000000000000') + (prog_ln)*4
    if instruction=="lui":reg[detectregister(rd)][2] = detectregister(inst_line[:-12]+'000000000000')
    prog_ln += 1

def reverse(string):
    string = string[::-1]
    return string

def b_Type(inst_line , instruction, reg):
    global prog_ln
    global memory
    rs2 = inst_line[7:12]
    rs1 = inst_line[12:17]
    immv1 = inst_line[0:7]
    immv2 = inst_line[20:25]
    imm = immv1+immv2
    imm = reverse(reverse(imm[0:12]) + "0")
    immval = int(bina_to_dec(imm, "2s")/4)
    print(immval)
    if (immval < -prog_ln or immval > len(inst_line)):
        imm = immv1+immv2
        imm = imm = reverse(reverse(imm[1:12]) + "1")
        immval = int(bina_to_dec(imm, "2s")/4) - 1
        if (immval < -prog_ln or immval > len(inst_line)):
            print("Warning..")
            immval = 1
    if instruction == "beq":
        if reg[detectregister(rs1)][2] == reg[detectregister(rs2)][2]:prog_ln = prog_ln + immval
        else:prog_ln += 1
    if instruction == "bne":
        if reg[detectregister(rs1)][2] != reg[detectregister(rs2)][2]:prog_ln = prog_ln + immval
        else:prog_ln += 1
    if instruction == "blt":
        if reg[detectregister(rs1)][2] < reg[detectregister(rs2)][2]:prog_ln = prog_ln + immval
        else:prog_ln += 1
    if instruction == "bge":
        if reg[detectregister(rs1)][2] >= reg[detectregister(rs2)][2]:prog_ln = prog_ln + immval
        else:prog_ln += 1
    if instruction == "bltu":
        if bina_to_dec(reg[detectregister(rs1)][2], "unsigned") < bina_to_dec(reg[detectregister(rs2)][2], "unsigned"):prog_ln = prog_ln + immval
        else:prog_ln += 1
    if instruction == "bgeu":
        if bina_to_dec(reg[detectregister(rs1)][2], "unsigned") >= bina_to_dec(reg[detectregister(rs2)][2], "unsigned"):prog_ln = prog_ln + immval
        else:prog_ln += 1

def bonus(inst_line, instruction, reg):
    global prog_ln
    if instruction == "rst":
        for i in range(32):reg[i][2] = 0
        prog_ln += 1
    if instruction == "halt":pass
    if instruction == "rvrs":
        rd = inst_line[-12:-7]
        rs1 = inst_line[-20:-15]
        reg[detectregister(rd)][2] = dec_2_bin(reverse(detectregister(rs1)), 32, "unsigned")
        prog_ln += 1
    if instruction == "mul":
        rs2 = inst_line[7:12]
        rs1 = inst_line[12:17]
        rd = inst_line[20:25]
        if reg[detectregister(rs1)][2]*reg[detectregister(rs2)][2] < 2**(32):reg[detectregister(rd)][2] = reg[detectregister(rs1)][2]*reg[detectregister(rs2)][2]
        prog_ln += 1
import os

def inp1():
    with open('File1.txt','r') as f:
        inst_line=[i.rstrip('\n') for i in f.readlines()]
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/Output_Sim.txt"
    global prog_ln
    global memory
    # data = ""
    outdata = ""
    # while True:
    #     data1 = input()
    #     if data1 == "":
    #         break
    #     data += data1 + "\n"
    # inst_line=data.split("\n")
    # inst_line.remove(' ')
    inst_line.append("00000000000000000000000001100011")
    prog_ln = 0
    while (prog_ln <= len(inst_line)):
        prog_ln = int(prog_ln)
        i = prog_ln
        i = int(i)
        check_insta = check_inst(inst_line[int(i)])
        # print(check_insta)
        if check_insta[1]=='bonus':
            bonus(inst_line[i],check_insta[0],reg)
            if check_insta[0]=='rst':pass
            elif check_insta[0]=='halt':
                print("0b"+dec_2_bin(prog_ln*4), end =" ")
                reg[0][2]=0
                outdata += "0b"+dec_2_bin(prog_ln*4) + " " + output(reg) +"\n"
                print(output(reg))
                break
        elif check_insta[1]=='r':r_Type(inst_line[i],check_insta[0],reg)
        elif check_insta[1]=='i':i_Type(inst_line[i],check_insta[0],reg)
        elif check_insta[1]=='s':s_Type(inst_line[i],check_insta[0],reg)
        elif check_insta[1]=='b':b_Type(inst_line[i],check_insta[0],reg)
        elif check_insta[1]=='u':u_Type(inst_line[i],check_insta[0],reg)
        elif check_insta[1]=='j':j_Type(inst_line[i],check_insta[0],reg)
        print("0b"+dec_2_bin(prog_ln*4),end=" ")
        reg[0][2]=0
        outdata += "0b"+dec_2_bin(prog_ln*4)+" "+ output(reg)+"\n"
        prin(reg)
    with open(dir_path, "w") as f:
        f.write(outdata)
        f.write(out_mem())
inp1()
