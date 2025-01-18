# 每个关卡的具体解决方案
solutions = {
    0: "cat readme",
    1: "cat ./-",
    2: "cat 'spaces in this filename'",
    3: "ls -la >/dev/null && cd inhere && ls -la > /dev/null && cat ./...Hiding-From-You",
    4: r"find inhere -type f  -exec file {} \; | grep 'ASCII text' | cut -d ':' -f 1 | xargs cat",
    5: r"find -type f -size 1033c ! -executable -execdir cat {} \;",
    6: r"find / -user bandit7 -group bandit6 -size 33c -execdir cat {} 2>/dev/null \;",
    7: "grep millionth data.txt",
    8: "sort data.txt | uniq -u",
    9: "strings data.txt | grep =",
    10: "strings data.txt | base64 -d",
    11: "cat data.txt | tr '[A-Za-z]' '[N-ZA-Mn-za-m]'",
    12: "tmp=$(mktemp -d) && xxd -r data.txt > $tmp/data1 && gunzip -c $tmp/data1>$tmp/data2 && bunzip2 -c $tmp/data2>$tmp/data3 && gunzip -c $tmp/data3>$tmp/data4 && tar -xf $tmp/data4 -C $tmp && tar -xf $tmp/data5.bin -C $tmp && tar -xf $tmp/data6.bin -C $tmp && bunzip2 -c $tmp/data6.bin>$tmp/data7 && tar -xf $tmp/data7 -C $tmp && gunzip -c $tmp/data8.bin>$tmp/data9.bin && file $tmp/data9.bin >/dev/null && cat $tmp/data9.bin",
    13: "ssh -i sshkey.private bandit14@bandit.labs.overthewire.org -p 2220 -o StrictHostKeyChecking=no 'cat /etc/bandit_pass/bandit14' 2>/dev/null",
    14: "cat /etc/bandit_pass/bandit14  | nc localhost 30000",
    15: "openssl s_client -connect localhost:30001",
    # ... 其他关卡的解决方案
}

# 每个关卡的自动提取 password 方案
# 机器人自动化需要，非过关必需
greps = {
    0:  "tail -n 2 | tail -n 2 | cut -d ':' -f 2 | tr -d ' ' | tr -d '\n'" ,
    1:  "tr -d '\n'",
    2:  "tr -d '\n'",
    3:  "tr -d '\n'",
    4:  "tr -d '\n'",
    5:  "head -n 1 | tr -d '\n'",
    6:  "tr -d '\n'",
    7:  "grep -E '[a-zA-Z0-9]{32}' -o | tr -d '\n'",
    8:  "grep -E '[a-zA-Z0-9]{32}' -o | tr -d '\n'",
    9:  "grep -E '[a-zA-Z0-9]{32}' -o | tr -d '\n'",
    10: "grep -E '[a-zA-Z0-9]{32}' -o | tr -d '\n'",
    11: "grep -E '[a-zA-Z0-9]{32}' -o | tr -d '\n'",
    12: "grep -E '[a-zA-Z0-9]{32}' -o | tr -d '\n'",
    13: "tr -d '\n'",
    14: "grep -E '[a-zA-Z0-9]{32}' -o | tr -d '\n'",
    15: "tr -d '\n'",
    # ... 其他关卡的自动提取 password 方案
}
