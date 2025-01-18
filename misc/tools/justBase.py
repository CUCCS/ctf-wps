from itertools import permutations
import base64


# problem: https://www.nssctf.cn/problem/723
# [安洵杯 2019]JustBase
def check_bytearray(byte_array):
    for byte in byte_array:
        # 检查是否为可打印字符、空格或换行符
        if not (32 <= byte <= 126 or byte == 10):
            return False
    return True


input = 'VGhlIGdlb@xvZ#kgb@YgdGhlIEVhcnRoJ#Mgc#VyZmFjZSBpcyBkb@!pbmF)ZWQgYnkgdGhlIHBhcnRpY#VsYXIgcHJvcGVydGllcyBvZiB#YXRlci$gUHJlc@VudCBvbiBFYXJ)aCBpbiBzb@xpZCwgbGlxdWlkLCBhbmQgZ@FzZW(!cyBzdGF)ZXMsIHdhdGVyIGlzIGV$Y@VwdGlvbmFsbHkgcmVhY#RpdmUuIEl)IGRpc#NvbHZlcywgdHJhbnNwb#J)cywgYW%kIHByZWNpcGl)YXRlcyBtYW%%IGNoZW!pY@FsIGNvbXBvdW%kcyBhbmQgaXMgY@(uc#RhbnRseSBtb@RpZnlpbmcgdGhlIGZhY@Ugb@YgdGhlIEVhcnRoLiBFdmFwb#JhdGVkIGZyb@)gdGhlIG(jZWFucywgd@F)ZXIgdmFwb#IgZm(ybXMgY@xvdWRzLCBzb@!lIG(mIHdoaWNoIGFyZSB)cmFuc#BvcnRlZCBieSB#aW%kIG(@ZXIgdGhlIGNvbnRpbmVudHMuIENvbmRlbnNhdGlvbiBmcm(tIHRoZSBjbG(!ZHMgcHJvdmlkZXMgdGhlIGVzc@VudGlhbCBhZ@VudCBvZiBjb@%)aW%lbnRhbCBlcm(zaW(uOiByYWluLlRoZSByYXRlIGF)IHdoaWNoIGEgbW(sZWN!bGUgb@Ygd@F)ZXIgcGFzc@VzIHRob#VnaCB)aGUgY#ljbGUgaXMgbm()IHJhbmRvbQpBbmQgdGhlIGZsYWcgaXM^IENURnsyMi!RV)VSVFlVSU*tUExLSkhHRkRTLUFaWENWQk%NfQ=='

invalid_chars = '!@#$%^&*()'

nums = list(range(10))
perms = list(permutations(nums))

for p in perms:
    outable = ''.join(map(str, p))
    print(outable)
    encode_table = str.maketrans(invalid_chars, str(outable))
    temp = input.translate(encode_table)
    try:
        output = base64.b64decode(temp)
        if check_bytearray(output):
            print(output)
            break
    except Exception:
        pass
