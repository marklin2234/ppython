import parse
import interpreter.interpreter as interpreter

while True:
    text = input(">>> ")
    
    ast, err = parse.run('<stdin>', text)

    if err:
        print(err)
        continue
    
    val, err = interpreter.run(ast)
    if err:
        print(err)
        continue

    print(val)
