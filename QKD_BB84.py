from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from numpy.random import randint
import numpy as np
import array as arr
from IPython.display import display
import IPython
print("\nImportazione Librerie Completata con Successo\n")

# PREPARAZIONE E SPIEGAZIONE:
qc = QuantumCircuit(1,1)
# Alice preapara il qbit nello stato |+>
qc.h(0)
qc.barrier()
# Alice invia il qbit a Bob che lo misura nella base-X
qc.h(0)
qc.measure(0,0)

# Disegno e simulazione del circuito
print("Invio del qbit a Bob SENZA che venga intercettato")
display(qc.draw())
aer_sim = Aer.get_backend('aer_simulator')
job = aer_sim.run(assemble(qc))
plot_histogram(job.result().get_counts())

#Funzione ENCODING del MESSAGGIO
def encode_message(bits, bases):
    message = []
    for i in range(n):
        qc = QuantumCircuit(1,1)
        if bases[i] == 0: # Preparazione del qbit nella base-Z
            if bits[i] == 0:
                pass
            else:
                qc.x(0)
        else: # Preparazione del qbit nella base-X
            if bits[i] == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        qc.barrier()
        message.append(qc)
    return message

# INIZIALIZZAZIONE PARAMETRI
np.random.seed(seed=0)
print("Inserisci il messaggio che vuoi inviare codificato in binario:")
#n = int(input(">>"))

n = str(input(">>"))
n = ''.join(format(ord(i), '08b') for i in n)
print("Il Msg codificato in binario è: \n",n)

# ALGORITMO:
# Step 1
# Alice genera i bits (messaggio)
#alice_bits = randint(2, size=n)
alice_bits = list(map(int, n))
n = len(n)

# Step 2
# Crea un array per dirci quali qubit sono codificati in quali basi
alice_bases = randint(2, size=n)
print("\nBit e Base di Alice: ")
print('bit = %i' % alice_bits[0])
print('base = %i' % alice_bases[0])

print("Base usata da Alice = \n",alice_bases)
message = encode_message(alice_bits, alice_bases)

message[0].draw()

# Questo per vedere se cambiamo la base come variano i parametri "bit" e "base"
# print('bit = %i' % alice_bits[4])
# print('base = %i' % alice_bases[4])
# message[4].draw()

# Step 3
# Decidi in quale base misurare:
bob_bases = randint(2, size=n)
print("Base usata da Bob = \n",bob_bases)

# Funzione MISURAZIONE
def measure_message(message, bases):
    backend = Aer.get_backend('aer_simulator')
    measurements = []
    for q in range(n):
        if bases[q] == 0: # misurazione in base-Z
            message[q].measure(0,0)
        if bases[q] == 1: # misurazione in base-X
            message[q].h(0)
            message[q].measure(0,0)
        aer_sim = Aer.get_backend('aer_simulator')
        qobj = assemble(message[q], shots=1, memory=True)
        result = aer_sim.run(qobj).result()
        measured_bit = int(result.get_memory()[0])
        measurements.append(measured_bit)
    return measurements

# Bob effettua misurazione
bob_results = measure_message(message, bob_bases)

#message[0].draw()
#message[6].draw()

# Funzione RIMOZIONE-NOISE (Eccesso)
def remove_garbage(a_bases, b_bases, bits):
    good_bits = []
    for q in range(n):
        if a_bases[q] == b_bases[q]:
            # Se entrambi hanno utilizzato la stessa base,
            # aggiungila all'elenco dei bit "buoni".
            good_bits.append(bits[q])
    return good_bits

# Step 4
alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)
print("\nLa chiave di Alice è: \n",alice_key)

##### UTILITY #####
# print("La chiave di Alice come sequenza numerica è:\n",' '.join(str(e) for e in alice_key))

# print(type(' '.join(str(e) for e in alice_key)))
# str_nospace = (' '.join(str(e) for e in alice_key)).replace(" ", "")
# print(str_nospace)

bob_key = remove_garbage(alice_bases, bob_bases, bob_results)
print("La chiave di Bob è: \n",bob_key)

# Bob e Alice confrontano una selezione casuale dei bit nelle loro chiavi per assicurarsi che il protocollo abbia funzionato correttamente:

# Funzione Campionamento BIT
def sample_bits(bits, selection):
    sample = []
    for i in selection:
        # uso di np.mod per assicurarci che il
        # bit che campioniamo sia sempre nell'intervallo dell'elenco
        i = np.mod(i, len(bits))
        # pop(i) rimuove l'elmento nella lista ocn indice 'i'
        sample.append(bits.pop(i))
    return sample

# Alice e Bob li trasmettono entrambi pubblicamente e li rimuovono dalle loro chiavi poiché non sono più segreti

# Step 5
print("\nInserisci i bit di campionamento (che sia una valore <= della lunghezza del msg")
sample_size = int(input(">>"))
bit_selection = randint(n, size=sample_size)

bob_sample = sample_bits(bob_key, bit_selection)
print("\n  bob_bit_campionamento = " + str(bob_sample))
alice_sample = sample_bits(alice_key, bit_selection)
print("alice_bit_campionamento = "+ str(alice_sample))

bob_sample == alice_sample

print("\nBob_Key \n",bob_key)
print("\nAlice_Key \n",alice_key)

if (bob_key==alice_key):
    print("\nLe chiavi coincidono")
else:
    print("\nLe chiavi NON coincidono")

print("\nLunghezza della chiave = %i" % len(alice_key))



print("\n\nProssima simulazione MAN IN THE MIDDLE")
input("Premi ENTER per contiunare")


# INTERCETTAZIONE MESSAGGIO
print("\n\n\nSimulazione con ManInTheMiddle è messaggio intercettato, verifica compromissione delle Key")

qc = QuantumCircuit(1,1)
# Alice preapara il qbit nello stato |+>
qc.h(0)
# Alice invia il qbit a Bob ma Eve lo intercetta e prova a leggerlo
qc.measure(0, 0)
qc.barrier()
# Eve ora lo passa a Bob che lo misura nella base-X
qc.h(0)
qc.measure(0,0)

# Disegno e simulazione del circuito
print("\nInvio del qbit a Bob intercettato da Eve, letto, e rimandato a Bob")
display(qc.draw())
aer_sim = Aer.get_backend('aer_simulator')
job = aer_sim.run(assemble(qc))
plot_histogram(job.result().get_counts())


# INIZIALIZZAZIONE PARAMETRI
np.random.seed(seed=3)
print("Inserisci il messaggio che vuoi codificare in binario e inviare")
#n = int(input(">>"))

n = str(input(">>"))
n = ''.join(format(ord(i), '08b') for i in n)
print("Il Msg codificato in binario è: \n",n)

# ALGORITMO:
# Step 1
# Alice genera i bits (messaggio)
#alice_bits = randint(2, size=n)
alice_bits = list(map(int, n))
n = len(n)

# Step 1
alice_bits = randint(2, size=n)
print("\nIl messaggio di Alice è: \n",alice_bits)
alice_bases = randint(2, size=n)
print("\nLa Base usata da Alice è: \n",alice_bases)
message = encode_message(alice_bits, alice_bases)
# message[0].draw()

# Step 2
# INTERCETTAZIONE DA PARTE DI EVE e reinvio del messaggio verso Bob
eve_bases = randint(2, size=n)
intercepted_message = measure_message(message, eve_bases)
print("\n\nMessaggio intercettato:\n",intercepted_message)
# message[0].draw()

# Step 3
# Bob effettua la misurazione con la sua base
bob_bases = randint(2, size=n)
print("\nLa Base usata da Bob è: \n",bob_bases)
bob_results = measure_message(message, bob_bases)
#message[0].draw()

# Step 4
alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)
print("\nLa chiave di Alice è: \n",alice_key)

bob_key = remove_garbage(alice_bases, bob_bases, bob_results)
print("La chiave di Bob è: \n",bob_key)

# Bob e Alice confrontano una selezione casuale dei bit nelle loro chiavi per assicurarsi che il protocollo abbia funzionato correttamente:

# Step 5
print("\nInserisci i bit di campionamento (che sia una valore <= della lunghezza del msg")
sample_size = int(input(">>"))
#se questo valore che inserisci è molto piccolo è possibile che il compionamento sia uguale e quindi l'interernza di Eve non viene notata anche se Lei intercetta il messaggio
bit_selection = randint(n, size=sample_size)

bob_sample = sample_bits(bob_key, bit_selection)
print("\n  bob_bit_campionamento = " + str(bob_sample))
alice_sample = sample_bits(alice_key, bit_selection)
print("alice_bit_campionamento = "+ str(alice_sample))

bob_sample == alice_sample

print("\nBob_Key \n",bob_key)
print("\nAlice_Key \n",alice_key)

if (bob_key==alice_key):
    print("\nLe chiavi coincidono")
else:
    print("\nLe chiavi NON coincidono")

if bob_sample != alice_sample:
    print("Interferenza di Eve monitorata.")
else:
    print("Eve non è stata vista!")

print("\nLunghezza della chiave = %i" % len(alice_key))
