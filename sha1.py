class Sha1:
    def __init__(self):
        self.k_hex = ["5A927999", "6ED9EBA1", "9F1BBCDC", "CA62C1D6"]
        self.A = "67452301"
        self.B = "EFCDAB89"
        self.C = "98BADCFE"
        self.D = "10325476"
        self.E = "C3D2E1F0"
        self.res = []
        self.m = []
        self.m_hex = []
        self.w_hex = []

    def call_sha1(self, text):
        # t = "Ping Pong Bomb"
        self.res = [
            format(ord(i), '08b') for i in text
        ]  # convert (string => dec) to binary
        if len(self.res) < 15:
            self.res.append("10000000")

        bi = self.res.copy()
        for i in range(16):
            getBinary = []
            # print(len(bi))
            if len(bi) != 0:
                for index in range(4):
                    # print(bi[0])
                    if len(bi) != 0:
                        getBinary.append(bi[0])
                        bi.pop(0)
                    else:
                        getBinary.append("00000000")
            else:
                if i != 15:
                    getBinary = [
                        "00000000", "00000000", "00000000", "00000000"
                    ]
                else:
                    getBinary = [
                        "00000000", "00000000", "00000000", "01110000"
                    ]
            self.m.append(getBinary)

        for i in self.m:
            binary = ''.join(b for b in i)
            # convert (binary -> dec) to hex
            con_hex = format(int(binary, 2), 'x')
            self.m_hex.append(con_hex.upper())

        # w[i] < 16
        self.w_hex = self.m_hex.copy()
        # process sha1
        return self.__process_sha1()

    def __process_sha1(self):
        for i in range(80):
            # function
            result_funtion = self.__function_call(i)
            # mod 1
            result_mod1 = self.__call_mod('98BADCFE', 'C3D2E1F0')
            # print(result_mod1)
            # break
            # mod 2
            result_mod2 = self.__call_mod(
                result_mod1, self.__shift_left(self.A, 5))
            # mod w[i]
            result_w = self.__call_mod(result_mod2, self.__call_w(i))
            # mod k[i]
            # print(result_w,check_k(i))
            result_k = self.__call_mod(result_w, self.__check_k(i))
            # print(result_k)
            new_A = result_k
            new_B = self.A
            new_C = self.__shift_left(self.B, 30)
            new_D = self.C
            new_E = self.D

            self.A = new_A
            self.B = new_B
            self.C = new_C
            self.D = new_D
            self.E = new_E

            # print(f"count {i} comple A: {self.A} ,B: {self.B}, C: {self.C}, D: {self.D}, E: {self.E}")
        return (''.join(i for i in [self.A, self.B, self.C, self.D, self.E]))

    def __function_call(self, count):
        if 0 <= count <= 19:
            # print(f"function1 : (B AND C) OR (NOT(B) AND D)")
            result_funtion = (int(self.B, base=16) & int(self.C, base=16)) | (
                ~int(self.B, base=16) & int(self.D, base=16))
            result_funtion = hex(result_funtion).replace(
                "0x", "")  # convert dec to hex
            return(result_funtion.upper())
        elif 20 <= count <= 39:
            # print(f"function2 : B XOR C XOR D")
            result_funtion = (int(self.B, base=16) ^ int(
                self.C, base=16)) ^ int(self.D, base=16)
            result_funtion = hex(result_funtion).replace(
                "0x", "")  # convert dec to hex
            return(result_funtion.upper())
        elif 40 <= count <= 59:
            # print(f"function3 : (B AND C) OR (B AND D) OR (C AND D)")
            result_funtion = (int(self.B, base=16) & int(self.C, base=16)) | (
                int(self.B, base=16) & int(self.D, base=16)) | (int(self.C, base=16) & int(self.D, base=16))
            result_funtion = hex(result_funtion).replace(
                "0x", "")  # convert dec to hex
            return(result_funtion.upper())
        elif 60 <= count <= 79:
            # print(f"function4 : B XOR C XOR D")
            result_funtion = (int(self.B, base=16) ^ int(
                self.C, base=16)) ^ int(self.D, base=16)
            result_funtion = hex(result_funtion).replace(
                "0x", "")  # convert dec to hex
            return(result_funtion.upper())

    def __call_mod(self, M, Y):
        M = '0x' + str(M)
        Y = '0x' + str(Y)
        # print(f"M {M} Y {Y}")
        result_mod = (int(M, base=16) + int(Y, base=16)
                      ) % int('10000000', base=16)
        result_mod = hex(result_mod).replace("0x", "").upper()
        if len(result_mod) != 8 or len(result_mod) < 8:
            return '0' + result_mod
        else:
            return result_mod

    def __shift_left(self, value, num_shift):
        # convert hex to binary
        if len(format(int(value, 16), '0b')) < 32:
            value = '0' + format(int(value, 16), '0b')
        else:
            value = format(int(value, 16), '0b')
        # swap binary by num_shift
        swap_binay = value[num_shift:] + value[:num_shift]
        # print(swap_binay)
        result_hex = format(int(swap_binay, 2), 'x').upper()
        if len(result_hex) < 8:
            return '0' + format(int(swap_binay, 2), 'x').upper()
        else:
            return format(int(swap_binay, 2), 'x').upper()

    def __call_w(self, i):
        if 16 <= i <= 79:
            # w[i] = W[i -16] XOR w[i -14] XOR w[i - 8] XOR w[i - 3]
            call_w = int(self.w_hex[i-16], 16) ^ int(self.w_hex[i-14],
                                                     16) ^ int(self.w_hex[i-8], 16) ^ int(self.w_hex[i-3], 16)
            self.w_hex.append(hex(call_w).replace("0x", "").upper())
            return hex(call_w).replace("0x", "").upper()
        return self.w_hex[i]

    def __check_k(self, i):
        if 0 <= i <= 19:
            return self.k_hex[0]
        elif 20 <= i <= 39:
            return self.k_hex[1]
        elif 40 <= i <= 59:
            return self.k_hex[2]
        elif 60 <= i <= 79:
            return self.k_hex[3]


# sha1 = Sha1()
# print(sha1.call_sha1("hello"))
