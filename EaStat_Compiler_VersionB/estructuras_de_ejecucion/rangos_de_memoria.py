# Data Segment: Declarar índice de direcciones GLOBALES (Rango 1,000 -> 9,999, 10k en total)
# Globales ENT  (Rango 1000 -> 3999, 3000k en total)
# Globales FLOT (Rango 4000 -> 6999, 3000k en total)
# Globales CAR  (Rango 7000 -> 9999, 3000k en total)
indicesGlob = [1000, 4000, 7000]

# Stack Segment: Declarar índice de direcciones LOCALES (Rango 10,000 -> 19,999, 10k en total)
# Locales ENT   (Rango 10,000 -> 12,999, 3000k en total)
# Locales FLOT  (Rango 13,000 -> 15,999, 3000k en total)
# Locales CAR   (Rango 16,000 -> 18,999, 3000k en total)
indicesLoc = [10000, 13000, 16000]

# Extra Segment: Declarar índice de direcciones TEMPORALES (Rango 20,000 -> 34,999, 15k en total)
# Temporales ENT    (Rango 19,000 -> 21,999, 3000k en total)
# Temporales FLOT   (Rango 22,000 -> 24,999, 3000k en total)
# Temporales CAR    (Rango 25,000 -> 27,999, 3000k en total)
# Temporales BOL    (Rango 28,000 -> 30,999, 3000k en total)
# Temporales PNTR   (Rango 31,000 -> 33,999, 3000k en total)
indicesTemp = [19000, 22000, 25000, 28000, 31000]

# Declarar índice de direcciones CONSTANTES (Rango 35,000 -> 46,999, 12k en total)
# Constantes ENT    (Rango 34,000 -> 36,999, 3000k en total)
# Constantes FLOT   (Rango 37,000 -> 39,999, 3000k en total)
# Constantes CAR    (Rango 40,000 -> 42,999, 3000k en total)
# Constantes STR    (Rango 43,000 -> 45,999, 3000k en total)
indicesCons = [34000, 37000, 40000, 43000]