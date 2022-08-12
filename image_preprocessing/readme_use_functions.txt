Die Funktionen sind alle in der __init__.py hinterlegt. 
Jede funktion z.B sharpness kann modular abgefragt werden um 
jeweils den gewünschten Skalar rauszubekommen. 

Reingegeben wird ein Bild, welches geöffnet wurde mit PIL.Imageopen().

Ausgegeben wird ein n-dimensionaler Vektor, d.h. n skalare Werte in einem Vektor. 
n = IMAGE_DATA_SIZE

sharpness = Nimmt ein Bild, transformiert es in grayscale und wendet ein Laplace-Filter an. 
Dies gibt die Kanten des Bildes, wovon wir die varianz bilden.
(Variance eines Bildes gibt an wie stark sich ein Pixel von seinem Nachbar unterscheidet).
Hohe Varianz heisst, hohe schärfe.

noise_differ_gaussian = Nimmt Bild, wendet ein Gaussches Rauschen drauf an, zieht dann 
das verrauschte Bild vom Original Bild ab und bekommt so einen Wert. 

noise_differ_median = Nimmt Bild, wendet ein Median Filter drauf an, zieht dann 
das verrauschte Bild vom Original Bild ab und bekommt so einen Wert. 

noise_differ_noises = Nimmt Bild, wendet jeweils ein Gaussches Rauschen und Median Filter, bildet
differenz der beiden Bilder

saturation = ursprünglich geplant es zu benutzen, kein guter Indikator (siehe Literatur) 

hue = berechnet den Farbton, funktioniert zur Zeit nicht. Wird bis zum Ende des Projekts wohl
auch nicht funktionieren, nicht weiter kritisch da andere Algorithmen besser bzw. mindestens
genauso stark sind

colorfulness = berechnet die "Farbheit" eines Bildes. Das Bild aus dem RGB Raum wird in seine einzelnen Räume gespalten 
(R,G,B) und so weiterverarbeitet. JPEG kommen in RGB und können ohne Probleme verarbeitet werden. 
PNGs haben unterschiedliche channelgrößen, weswegen dies ein größere Problem bedeutet. 
Dies ist eher ein psychologischer aspekt der bei der Bild Qualität eine große Rolle spielt. 
Farbenfrohe Bilder werden als besser eingestuft als Bilder mit einem niedrigen Farbton 
(man vergleicht nicht zwei greyscale Bilder miteinander).

contrast = berechnet den Contrast eines Bildes. Dazu wird die Shannon-Entropie des Bildes benutzt. 
S. Entropie, in diesem Fall heißt es wie stark sich die Nachbarn der Pixel unterscheiden, dies
drückt das "Chaos" bzw Unordnung eines Bildes aus (Bildlicher Vergleich aus der Boltzmann-Entropie)

