# Projektplan UnikittyPy
## Ziel
Eine Web API bewertet hochgeladene Bilddateien nach Darstellungs-Qualität durch Verwendung von Deep Learning und gibt diese Wertung zurück.
Der externe Zugriff erfolgt über eine Webseite.

## Funktionsablauf des Web API Aufrufs
1. Benutzer lädt Bild [oder Bildersammlung] über eine Weboberfläche auf den Server.
2. Bilddaten werden eingelesen und zur Verwendung in neuronalen Netzwerken verarbeitet.
3. Netzwerk erstellt (unter Verwendung vorherigem Trainings auf Testdaten) eine Bewertung.
4. Bewertung wird der Web API übermittelt.
5. Der Server gibt die Qualitätswertung als Webseite zurück [und zeigt die Auswahl des besten Bildes].
6. [Benutzer kann ein Feedback zum Ergebnis geben, damit dieses späteren Training-Durchläufen zugeführt werden kann.]

## Funktionsablauf des Trainings
1. Zuvor gesammelte Trainingsdaten (Bild und Label) werden eingelesen und verarbeietet.
2. Netzwerk erstellt (unter Verwendung vorherigem Trainings auf Testdaten) eine Bewertung.
3. Netzwerk überprüft Wertung mit gewünschtem Ergebnis, wird dabei trainiert.
4. Interne Speicherung der Netzwerkparameter für die späteren Aufrufe über die Web API.

## Module
- *ImageProcessor* Bildverarbeitung (Input) (Emlyn S. / Roland E.)
- *Database* Datenbank (Zuhra A. / Zhengsen D.)
- *TrainingData* Auswahl von Trainingsdaten (Zuhra A. / Zhengsen D.)
- *NeuralNetwork* Neuronales Netzwerk (Dominik T. / Tobias S.)
- *Resolver* Verarbeitung Netzwerkergebnis (Output/Mapping) (Dominik T. / Tobias S.)
- *Webservice* Webseite und UI (Tobias S. / Zuhra A.)
- *UnikittyPy* Hauptprogramm

## Entwicklungsplan / Milestones
- 13.06. - 19.06. *Early Integration (Tests, Mockups, Schnittstellen) und erster Kontakt mit den Bibliotheken*
- 20.06. - 26.06. *Arbeit mit Bibliotheken; erste lauffähige Codebeispiele*
- 27.06. - 03.07. *Finale Implementierung*
- 04.07. - 10.07. *Test und Debugging*


## Schnittstellen

| From  | To    | Method | Parameters | Return type
| ----- | ----- | ------ | ---------- | -----------
| UnikittyPy | ImageProcessor | serialize | image: raw image file | ImageData - Serialized image data
| UnikittyPy | Database | saveImage | image: raw image file | int - Image id
| UnikittyPy | NeuralNetwork | evaluate | imageData: ImageData | long - Raw network output
| UnikittyPy | NeuralNetwork | train | trainData: TrainData | long - Success rate
| UnikittyPy | Database | getTrainData | - | Array(TrainData) - All train data
| UnikittyPy | Resolver | resolve | data: long | bool - Translated network output
| Webservice (Web API or Website) | UnikittyPy | run | pictures: raw image files | dict - Result set
| Webservice (Web API or Website) | UnikittyPy | train | - | long - Success Rate
| Webservice (Web API or Website) | Database | addFeedbackData | imageID: int, feedbackData: bool | int - Status code
| ImageData | public | getData | - | Array(long)
| ImageData | public | setData | Array(long) | -
| ImageData | public | getSize | - | int
| ImageData | public | setRandomData | - | -
