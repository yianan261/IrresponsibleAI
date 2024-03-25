for i in range(1,51):
    file_path = f"/Users/chenyian261/Documents/GitHub/IrresponsibleAI/article_texts/{i}.txt"
    with open(file_path,'r',encoding='utf-8') as file:
        file_content = file.read()
    n = len(file_content)//2
    file_content = file_content[:n]

    with open(f"./article_texts2/{i}.txt","w") as f:
        f.write(file_content)