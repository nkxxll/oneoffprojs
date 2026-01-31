---
tags:
- theory
- compilers
- functional
---

# Chat GPT test examn 2019/2020

Alles klar — das ist **eine komplette Musterlösung zur Klausur**, **mit Erklärungen, wie man jeweils darauf kommt**.
Ich schreibe so, wie man es in einer guten Prüfungslösung erwarten würde, plus kurze Meta-Erklärungen („Wie habe ich das gelöst?“).

---

# **Aufgabe 1 (25 Punkte)**

### **1. Unterschied zwischen TM und NTM**

wichtig noch die def von einer TM:
eine TM ist M:
Bandalphabet = Input symbole + _ (empty) (wobei man glaube auch noch symbole zum Bandalphabet
hinzufuegen kann)
Transitions = Z x B -> Z x B x { L,R }
(Bandalphabet, Zustaende, Transitions, start, end)

**Antwort:**
Eine **deterministische Turingmaschine (TM)** hat für jede Kombination aus Zustand und gelesenem Bandsymbol **höchstens eine** Übergangsregel.
Eine **nichtdeterministische Turingmaschine (NTM)** darf **mehrere mögliche Übergänge** haben. Die Maschine akzeptiert eine Eingabe, **wenn mindestens ein Rechenzweig akzeptiert**.

**Wie man darauf kommt:**
Man erinnert sich an den Unterschied „eine Wahl“ vs. „viele mögliche Wege“. Wichtig ist: **Nichtdeterminismus = parallele Rechenzweige** (theoretisch).

somit ist NTM M':
(Bandalphabet, Zustaende, Transitions, start, end)
mit Transitions = Z x B -> List(Z x B x { L,R })

---

### **2. Definition der Komplexitätsklasse P**

**Antwort:**
Die Klasse **P** enthält alle Entscheidungsprobleme, die von einer **deterministischen Turingmaschine in polynomieller Zeit** entschieden werden können.

Formal:
[
P = { L \mid \exists\ \text{TM } M,\ \exists k \in \mathbb{N}:\ M \text{ entscheidet } L \text{ in } O(n^k) }
]

**Wie man darauf kommt:**
P = „praktisch lösbar“. Stichworte: **deterministisch**, **polynomiell**, **Entscheidungsproblem**.
lösbar durch eine deterministische Turingmaschine in polynomialer Zeit

Was sind die Komplexitätsklassen und wie sind sie definiert?

Bsp.:
- Kürzester Weg (Dijkstra)
- Sortieren

NP:
lösbar durch eine nichtdeterministische Turingmaschine in polynomialer Zeit
hier kann eine gegebene loesung in polynomieller zeit verifiziert werden

wichtig P <= NP
ob P = NP weiss man nicht

Bsp. NP:
- SAT (Erfüllbarkeit boolescher Formeln)
- Hamiltonkreis
- Clique

NP-vollständig:
- SAT (erstes NP-vollständiges Problem, Cook–Levin)
- 3-SAT
- Vertex Cover
- Traveling Salesman (Entscheidungsvariante)

sind die schwersten probleme in NP
die polynomiell reduziert werden koennen
schrift wieder...

#### Was ist eine polyomielle reduktion

Entscheidungsprobleme und formale sprachen sind das gleiche

---

### **3. Aussage des Satzes von Rice**

**Antwort:**
Der **Satz von Rice** besagt:

> Jede **nicht-triviale semantische Eigenschaft** der von einer Turingmaschine berechneten Sprache ist **unentscheidbar**.

**Wie man darauf kommt:**
Man merkt sich:

* **syntaktisch** → evtl. entscheidbar
* **semantisch** (Bedeutung der berechneten Sprache) → **unentscheidbar**
* nicht-trivial = nicht „immer wahr“ oder „immer falsch“

hier auch wichtig:
- Recursive (decidable):
- RE (recursively enumerable):
- co-RE:
- Neither RE nor co-RE:

---

### **4. Komplexitätsklasse von 3SAT und 2SAT**

**Antwort:**

* **3SAT** ist **NP-vollständig**
* **2SAT** liegt in **P**

**Wie man darauf kommt:**
Standardwissen:

* 3 Literale pro Klausel → NP-vollständig
* 2 Literale → effizient lösbar (Graph / Implikationsgraph)

---

# **Aufgabe 2 (30 Punkte)**

*(Ich löse Aufgabe 2.2, das ist meist die Standardwahl.)*

## **Clique ist NP-vollständig**

### **1. Clique ∈ NP**

**Antwort:**
Ein Zertifikat ist eine Menge von (k) Knoten.
Man überprüft in polynomialer Zeit, ob **jede Kante zwischen allen Knoten existiert**.

**Wie man darauf kommt:**
NP = „Zertifikat schnell prüfen“.

---

### **2. NP-Härte: Reduktion von Independent Set**

**Idee der Reduktion:**
Ein **Independent Set** in (G) entspricht einer **Clique im Komplementgraphen (\overline{G})**.

**Reduktion:**
Gegeben ((G, k)), konstruiere ((\overline{G}, k)).

**Begründung:**

* Keine Kanten in (G)
  ⇔ alle Kanten in (\overline{G})

**Korrektheit:**
[
G \text{ hat ein Independent Set der Größe } k
\iff \overline{G} \text{ hat eine Clique der Größe } k
]

**Laufzeit:**
Komplementgraph kann in polynomialer Zeit berechnet werden.

**Fazit:**
Clique ist **NP-vollständig**.

---

# **Aufgabe 3 (30 Punkte)**

**1-Band-TM: von (a^i b^k) zu (a^k b^k)**

### **Idee**

* Zähle die Anzahl der **b**
* Ersetze jedes **b** durch ein **a** links
* Schreibe danach wieder **b**
* Lösche alte Zeichen

### **Algorithmus (informell, prüfungstauglich)**

1. Gehe nach rechts bis zum ersten **b**
2. Markiere ein **b** (z. B. → B)
3. Gehe ganz nach links und schreibe ein **a**
4. Gehe zurück zum markierten **B**
5. Wiederhole, bis alle **b** markiert sind
6. Schreibe danach für jedes markierte **B** ein **b**
7. Lösche alle Hilfszeichen

**Warum korrekt:**

* Für jedes ursprüngliche **b** wird genau ein **a** erzeugt
* Anzahl der **b** bleibt erhalten
* Band enthält am Ende nur (a^k b^k)

---

# **Aufgabe 4 (15 Punkte)**

### **1. Aussage 1**

> Falls A ≠ Σ* rekursiv ist, hält jede TM mit A = L(M) bei allen Eingaben.

❌ **Falsch**

**Begründung:**
Eine rekursive Sprache **kann auch von einer nicht-haltenden TM erkannt werden**.
Entscheidbarkeit ≠ jede TM hält.

---

### **2. Aussage 2**

> Aus A entscheidbar und A ∩ B entscheidbar folgt B entscheidbar.

❌ **Falsch**

**Gegenbeispiel:**

* A = Σ* (entscheidbar)
* A ∩ B = B
  ⇒ B kann trotzdem unentscheidbar sein

---

### **3. Aussage 3**

> A, C ∈ P und A ⊆ B ⊆ C ⇒ B ∈ P

❌ **Falsch**

**Begründung:**
Zwischen zwei „einfachen“ Sprachen kann eine **schwere Sprache** liegen.
P ist **nicht nach oben/unten abgeschlossen** bzgl. Inklusion.

---

# **Gesamtfazit**

* Alle Kernthemen deiner Liste kommen vor:

  * Turingmaschinen ✅
  * Church-These (implizit) ✅
  * Reduktionen ✅
  * NP-Vollständigkeit ✅
  * Unentscheidbarkeit ✅
  * Komplexitätsklassen ✅

Wenn du willst, kann ich:

* das **als Lernzettel zusammenfassen**
* eine **echte „Schritt-für-Schritt-Lösung zum Auswendiglernen“** schreiben
* oder eine **Probe-Klausur simulieren** (mit Bewertung)

Sag einfach 👍

## Related Notes
- [[Statemachine (yes it is a state machine but this state machine is a tokenizer or a lexer)]]
- [[Golang]]
