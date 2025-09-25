def find_optimal_c(training_data, n_s, d):
    """permet de déterminer le nombre optimal de samples à concaténer (c) pour que la fraction de duplication des chunks soit <= d.
    - training_data: liste ou array contenant les samples de taille N_T
    - n_s: nombre de bits par sample
    - d: fraction maximale de duplication autorisée pour les chunks
    - c, le nombre de samples à concaténer"""
    N_T = len(training_data)
    # Par sécurité, on fixe une limite supérieure pour c, par exemple c <= N_T, pour éviter une boucle infinie.
    max_c = N_T
    c = 1 #on va commencer par 1 sample concaténé
    while c <= max_c:
        chunks = []
        for i in range(0, N_T, c):
            # Récupération des c samples ou moins si on est en fin de fichier
            block = training_data[i:i + c]
            chunk_bits = []
            for sample in block:
                chunk_bits.append(format(sample, f'0{n_s}b'))
            chunk = ''.join(chunk_bits)
            chunks.append(chunk)
        nb_chunks_total = len(chunks)
        nb_chunks_uniques = len(set(chunks))
        duplication = 1.0 - (nb_chunks_uniques / nb_chunks_total)
        if duplication <= d:
            return c
        c += 1
    return max_c

# ----------------- test -----------------

if __name__ == "__main__":
    #test
    n_s = 8        
    d = 0.01        
    import random
    random.seed(42)
    #genere des donnees
    training_data = [random.randint(0, 255) for _ in range(1000)]
    
    c_opt = find_optimal_c(training_data, n_s, d)
    
    print(f"Nombre optimal de samples à concaténer : c = {c_opt}")
