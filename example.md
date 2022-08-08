*kprim_append* Welche der unten stehenden Aussagen sind richtig(+) und welche falsch(-)?

# ECG
## 2022
### Rasterizer

> kprim

**Primitives:**

Um Geometrie darstellen zu können, wird diese im Rasterisierer in einzelne Fragmente zerlegt.

``` Formel:
\[\begin{aligned}

i.\ &
a^2+b^2=c^2
\\

ii.\ &
sin(0) = 0
\\

ii.\ &
cos(0) = 1

\end{aligned}\]
```

- r Der Rasterisierer zerlegt nicht direkt ganze 3D-Modelle in einzelne Pixel,
    sondern die einzelnen geometrischen Primitive (z.B. Dreiecke) aus denen die Modelle zusammengesetzt sind.
- f Es gibt folgende Primitive: Punkte, Linien, Dreiecke und Vierecke.
- f Grafikkarten können ausschließlich Dreiecke rasterisieren.
- r Alle Objektoberflächen werden mit (vielen kleinen) Dreiecken dargestellt.


> kprim

**Pixels:**

- f Die Auflösung beim Rasterisieren entspricht immer der des Programmfensters..
- r Der Rasterisierer läuft zwischen dem Vertex- und Fragment-Shader.
- f Der Rasterisierer läuft nach dem Fragment-Shader.
- r Vertex-Attribute werden vom Rasterisierer für jeden einzelnen Pixel interpoliert.