def load_file_as_binary_vector(file_path, chunk_size):
    # Lecture du fichier en mode binaire
    with open(file_path, 'rb') as file:
        data = file.read()

    # Conversion en vecteur binaire (chaîne de 0 et 1)
    binary_vector = ''.join(format(byte, '08b') for byte in data)

    # Padding pour compléter le dernier chunk si nécessaire
    if len(binary_vector) % chunk_size != 0:
        padding_length = chunk_size - (len(binary_vector) % chunk_size)
        binary_vector += '0' * padding_length

    # Division en chunks
    chunks = [binary_vector[i:i + chunk_size] for i in range(0, len(binary_vector), chunk_size)]

    return binary_vector, chunks

# Exemple d'utilisation
file_path = "/Users/fallou/Desktop/ia-compression/test"  # Remplacer par le chemin du fichier
chunk_size = 64  # Taille du chunk en bits (ajuster selon le contexte)

binary_vector, chunks = load_file_as_binary_vector(file_path, chunk_size)

print(f"Vecteur binaire (taille {len(binary_vector)} bits) : {binary_vector[:128]}...")  # Affichage limité à 128 bits
print(f"Nombre de chunks ({chunk_size} bits) : {len(chunks)}")
print(f"Exemple de chunk : {chunks[0]}")
