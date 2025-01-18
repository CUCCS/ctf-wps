import difflib


# problem: https://www.nssctf.cn/problem/78
def find_added_chars(line1, line2):
    added_chars = []
    i, j = 0, 0
    while j < len(line2):
        if i < len(line1) and line1[i] == line2[j]:
            i += 1
            j += 1
        else:
            added_chars.append(line2[j])
            j += 1
    return "".join(added_chars)


def compare_text_files(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
        text1_lines = file1.readlines()
        text2_lines = file2.readlines()
    differ = difflib.Differ()
    diff_result = differ.compare(text1_lines, text2_lines)
    new_chars = []
    modified_line = ""
    original_line = ""
    for i, line in enumerate(diff_result):
        if line.startswith('- '):
            modified_line = line
        if line.startswith('+ '):
            original_line = line
        if modified_line and original_line:
            added_chars = find_added_chars(original_line[2:], modified_line[2:])
            modified_line = ""
            original_line = ""
            new_chars.extend(added_chars)
    return ''.join(new_chars)


if __name__ == "__main__":
    file1_path = 'modified.txt'
    file2_path = 'original.txt'
    result = compare_text_files(file1_path, file2_path)
    print(result)
