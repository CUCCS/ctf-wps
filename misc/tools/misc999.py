# ref: https://www.nssctf.cn/problem/2572
from base62 import decodebytes


digits = "9876543210qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ"
input_str = "7dFRjPItGFkeXAALp6GMKE9Y4R4BuNtIUK1RECFlU4f3PomCzGnfemFvO"
print(decodebytes(input_str, digits))

