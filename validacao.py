def validar_id(id: int) -> bool:
    return (int(id) > 0 and int(id) <= 1000)

def validar_animal(animal: str) -> bool:
    animal = animal.strip()
    return (len(animal) > 0 and len(animal) <= 100)

def validar_raca(raça: str) -> bool:
    raça = raça.strip()
    return (len(raça) > 0 and len(raça) <= 45)

def validar_tamanho(tamanho: str) -> bool:
    tamanho = tamanho.strip()
    return (len(tamanho) > 0 and len(tamanho) <= 15)

def validar_idade (idade: int) -> bool:
    idade = idade.strip()
    return (int(idade) > 0 and int(idade) <= 3)
