# I++ (Italian Plus Plus)

I++ è un linguaggio di programmazione interpretato, progettato per essere leggibile come un testo italiano. È pensato per essere semplice, estendibile e multipiattaforma.

## Funzionalità principali

- sintassi naturale in italiano
- interpreter Python
- REPL interattiva
- supporto per variabili, condizioni, cicli, funzioni e liste
- gestione errori in italiano

## Installazione

Da cartella del progetto:

```bash
python -m itpp.main
```

Oppure eseguire un file:

```bash
python -m itpp.main esempi/ciao.itpp
```

## Esecuzione di un file

```bash
python main.py programma.itpp
```

## REPL

```bash
python -m itpp.main --repl
```

## Sintassi base

### Stampa

```itpp
stampa "Ciao mondo"
```

### Variabili

```itpp
sia nome uguale a "Marco"
```

### Condizioni

```itpp
se età è maggiore di 18 allora
    stampa "Maggiorenne"
altrimenti
    stampa "Minorenne"
fine
```

### Cicli

```itpp
ripeti 3 volte
    stampa "Ciao"
fine
```

### Funzioni

```itpp
definisci funzione saluta con parametro nome
    stampa "Ciao " + nome
fine
```

## Esempi

Gli esempi sono disponibili nella cartella [itpp/esempi](itpp/esempi).

## Struttura del progetto

- lexer.py: tokenizzazione del codice
- parser.py: costruzione dell'AST
- interpreter.py: esecuzione del programma
- runtime.py: gestione variabili e scope
- repl.py: REPL interattiva
- main.py: punto di ingresso
- errors.py: errori in italiano
- utils.py: utility comuni
