import basic
import interpreter

while True:
    text = input("in > ")
    
    ast, err = basic.run('<stdin>', text)

    if err:
        print(err)
        continue
    
    val, err = interpreter.run(ast)
    if err:
        print(err)
        continue

    print(val)
