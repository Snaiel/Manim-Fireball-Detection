# Manim-Fireball-Detection

A repository of animations showcasing the fireball detection system from https://github.com/Snaiel/Automating-Fireballs

Used for the NPSC3000 Industry Showcase presentation slides https://docs.google.com/presentation/d/1Zzn5svmLDW9DgyhLWNEZVS83S2lltuJUOUt8zOMvsgg/edit?usp=sharing

Uses Manim, an animation engine for creating videos using Python. https://github.com/ManimCommunity/manim

## Installation

Clone repository.

```bash
git clone https://github.com/Snaiel/Manim-Fireball-Detection
```

Install dependencies.

```bash
pip install -r requirements.txt
```

## Animations

### GoodFireballs

An animation that shows images of fireballs and the bounding boxes around them.

![](videos/GoodFireballs.mp4)

**Preview Quality:**

```bash
manim -p -r 480,320 --fps 15 main.py GoodFireballs
```

**Export Quality:**

```bash
manim -p -r 1920,1280 --fps 30 main.py GoodFireballs
```

<br>

### FireballDetectionMethodology

An animation that shows the steps the detection system performs to do detect fireballs in an image.

![](videos/FireballDetectionMethodology.mp4)

**Preview Quality:**

```bash
manim -p -r 480,360 --fps 15 main.py FireballDetectionMethodology
```

**Export Quality:**

```bash
manim -p -r 1920,1440 --fps 30 main.py FireballDetectionMethodology
```

<br>

### FireballFails

An animation that shows examples of images that the detection system generates false positive predictions.

![](videos/FireballFails.mp4)

**Preview Quality:**

```bash
manim -p -r 480,320 --fps 15 main.py FireballFails
```

**Export Quality:**

```bash
manim -p -r 1920,1280 --fps 30 main.py FireballFails
```