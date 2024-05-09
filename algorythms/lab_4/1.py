string = input()
stack = []
len_stack = len(stack)
for i in string:
    if len_stack != 0:
        if i == "]" and stack[-1] == "[":
            stack.pop()
            len_stack -= 1
        elif i == "}" and stack[-1] == "{":
            stack.pop()
            len_stack -= 1
        elif i == ")" and stack[-1] == "(":
            stack.pop()
            len_stack -= 1
        else:
            stack.append(i)
            len_stack += 1
    else:
        stack.append(i)
        len_stack += 1
if len_stack == 0:
    print("yes")
else:
    print("no")
