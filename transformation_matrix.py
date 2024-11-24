import numpy as np

def transformation_matrix_2d():
    """Retorna a matriz transformacao de um objeto 2D para a sequencia de operacoes definida durante a execucao"""
    operations = [] # Salva as operacoes no formato de pilha

    # Esse primeiro loop armazena as transformacoes que serao executadas de forma sequencial
    while True:
        print("\nInsira a transformacao que deseja aplicar ou digite 0 para aplicar as ja inseridas:")
        print("1. Translacao")
        print("2. Escala")
        print("3. Reflexao")
        print("4. Cisalhamento")
        print("5. Rotacao")
        print("0. Aplicar tudo")

        choice = input("Digite o número da opção desejada: ")

        if choice == '1':  # Translação
            dx = float(input("Digite o deslocamento em x: "))
            dy = float(input("Digite o deslocamento em y: "))
            operations.append(('translation', dx, dy))

        elif choice == '2':  # Escala
            sx = float(input("Digite o fator de escala em x: "))
            sy = float(input("Digite o fator de escala em y: "))
            operations.append(('scaling', sx, sy))

        elif choice == '3':  # Reflexão
            print("Escolha o eixo de reflexão:")
            print("1. Reflexão no eixo X")
            print("2. Reflexão no eixo Y")
            print("3. Reflexão na origem")
            reflection_choice = input("Digite o número da reflexão: ")
            operations.append(('reflection', reflection_choice))

        elif choice == '4':  # Cisalhamento
            shx = float(input("Digite o fator de cisalhamento em x: "))
            shy = float(input("Digite o fator de cisalhamento em y: "))
            operations.append(('shear', shx, shy))

        elif choice == '5':  # Rotação - Da a opcao de escolher o ponto sobre o qual a rotacao ocorrera ou apenas rotacionar em relacao a origem
            angle = float(input("Digite o ângulo de rotação (em graus): "))
            rotate_about = input("Deseja rotacionar em torno de um ponto específico? (s/n): ")
            if rotate_about.lower() == 's':
                x_c = float(input("Digite a coordenada x do ponto: "))
                y_c = float(input("Digite a coordenada y do ponto: "))
                # Adiciona as translações para a origem e de volta
                operations.append(('translation', -x_c, -y_c))
                operations.append(('rotation', angle))
                operations.append(('translation', x_c, y_c))
            else:
                operations.append(('rotation', angle))

        elif choice == '0':  # Finalizar
            break

        else:
            print("Opção inválida. Por favor, escolha entre 0 a 5.")

    # Inicia a matriz como identidade
    result_matrix = np.identity(3)

    # O segundo loop retira da pilha cada transformacao, monta a matriz e a multiplica com a matriz resultante
    while operations:
        transformation = operations.pop()

        if transformation[0] == 'translation':
            dx, dy = transformation[1], transformation[2]
            matrix = np.array([[1, 0, dx],
                               [0, 1, dy],
                               [0, 0, 1]])

        elif transformation[0] == 'rotation':
            angle = np.radians(transformation[1])
            cos_theta = np.cos(angle)
            sin_theta = np.sin(angle)
            matrix = np.array([[cos_theta, -sin_theta, 0],
                               [sin_theta, cos_theta, 0],
                               [0, 0, 1]])

        elif transformation[0] == 'scaling':
            sx, sy = transformation[1], transformation[2]
            matrix = np.array([[sx, 0, 0],
                               [0, sy, 0],
                               [0, 0, 1]])

        elif transformation[0] == 'reflection':
            reflection_choice = transformation[1]
            if reflection_choice == '1':  # Reflexão no eixo X
                matrix = np.array([[1, 0, 0],
                                   [0, -1, 0],
                                   [0, 0, 1]])
            elif reflection_choice == '2':  # Reflexão no eixo Y
                matrix = np.array([[-1, 0, 0],
                                   [0, 1, 0],
                                   [0, 0, 1]])
            elif reflection_choice == '3':  # Reflexão na origem
                matrix = np.array([[-1, 0, 0],
                                   [0, -1, 0],
                                   [0, 0, 1]])
            else:
                print("Reflexão inválida! Ignorando...")
                continue

        elif transformation[0] == 'shear':
            shx, shy = transformation[1], transformation[2]
            matrix = np.array([[1, shx, 0],
                               [shy, 1, 0],
                               [0, 0, 1]])

        # Multiplica a matriz resultante pela transformação atual
        result_matrix = matrix @ result_matrix

    return result_matrix

if __name__ == "__main__":
    print(transformation_matrix_2d())