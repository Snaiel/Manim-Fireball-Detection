import os
from pathlib import Path

import numpy as np
from manim import *
from skimage import io


config.background_color = "#38342e"


class GoodFireballs(Scene):
    def construct(self):
        with open(Path("good_fireballs", "fireballs.txt")) as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split()
                
                image = ImageMobject(io.imread(Path("good_fireballs", parts[0])))
                image.width = 14.3
                self.add(image)
                self.wait(10)
                
                conf, x0, y0, x1, y1 = map(float, parts[1:])
                
                rect = Rectangle(RED_E, (y1-y0)/4912*9.35, (x1-x0)/7360*14)
                rect.move_to(image.get_corner(UL), aligned_edge=UL)
                rect.shift((x0/7360*14.3*RIGHT) + (y0/4912*9.5436957*DOWN))
                
                text = Text(f"{conf:.2f}", color=RED_E, font_size=16, weight=BOLD)
                text.move_to(rect.get_corner(UL))
                text.shift((0.15*UP) + (0.25*RIGHT))
                
                self.play(
                    Create(rect),
                    Write(text),
                    run_time=2
                )
                
                self.wait(3)


class FireballDetectionMethodology(Scene):
    def construct(self):

        image_path = Path("methodology", "57_2016-06-17_182058_S_DSC_1189.thumb.jpg")
        image_array = io.imread(image_path)

        main_image = ImageMobject(image_array)
        main_image.height = 8
        self.add(main_image)

        heading_input = Text("7360x4912 Input Image", weight=BOLD, font_size=32)
        heading_input.move_to(np.array([0, 4.5, 0]))

        self.play(FadeIn(main_image))
        self.play(Write(heading_input))
        self.wait(1)
        self.play(FadeOut(main_image))
        main_image.scale_to_fit_height(3.65)
        self.play(FadeIn(main_image))
        self.wait(2)
        
        heading_tiling = Text("Splitting into 400x400 Tiles with 50% Overlap", weight=BOLD, font_size=32)
        heading_tiling.move_to(np.array([0, 4.5, 0]))
        self.play(Transform(heading_input, heading_tiling, replace_mobject_with_target_in_scene=True))
        
        self.play(ShrinkToCenter(main_image))

        coordinates = []
        with open(Path("methodology", "coordinates.txt")) as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split()
                x, y = map(int, parts)
                coordinates.append((x, y))

        square_size = 400

        sub_images = Group()
        tiles = {}
        for coord in coordinates:
            x, y = coord
            sub_image = ImageMobject(image_array[y:y + square_size, x:x + square_size])
            sub_image.height = 0.25
            sub_images.add(sub_image)
            tiles[coord] = sub_image

        sub_images.arrange_in_grid(rows=24, cols=36, buff=0.1)
        sub_images.shift(0.25*DOWN)

        self.add(sub_images)
        self.play(GrowFromCenter(sub_images))
        self.wait(3)

        discarded_coordinates = set()
        with open(Path("methodology", "discarded.txt")) as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split()
                x, y = map(int, parts)
                discarded_coordinates.add((x, y))

        included_images = []        
        discarded_images = []
        for coord, image in tiles.items():
            if coord in discarded_coordinates:
                discarded_images.append(image)
            else:
                included_images.append(image)
        
        heading_discard = Text("Discarding Outside Tiles", weight=BOLD, font_size=32)
        heading_discard.move_to(np.array([0, 4.5, 0]))
        
        self.play(Transform(heading_tiling, heading_discard, replace_mobject_with_target_in_scene=True))
        self.wait(0.5)
        self.play(*[ShrinkToCenter(mobject, rate_func=rate_functions.ease_in_back) for mobject in discarded_images])
        for tile in discarded_images:
            sub_images.remove(tile)
        self.wait(3)

        heading_yolo = Text("Detecting with a Custom-Trained YOLOv8 Model", weight=BOLD, font_size=32)
        heading_yolo.move_to(np.array([0, 4.5, 0]))

        self.play(Transform(heading_discard, heading_yolo, replace_mobject_with_target_in_scene=True))
        self.play(*[Circumscribe(mobject, stroke_width=DEFAULT_STROKE_WIDTH/5, buff=0, run_time=4) for mobject in included_images])
        self.wait(1)

        detected_tiles = []
        with open(Path("methodology", "detected_tiles.txt")) as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split()
                x, y = map(int, parts)
                detected_tiles.append(tiles[(x, y)])
        
        self.play(
            *[Indicate(mobject) for mobject in detected_tiles]
        )
        self.wait(1)

        confidences: list[float] = []
        tile_predictions: list[Rectangle] = []
        with open(Path("methodology", "tile_predictions.txt")) as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split()
                x, y = map(int, parts[:2])
                conf = float(parts[2])
                confidences.append(conf)
                dim = tuple(map(float, parts[3:]))
                tile: Mobject = tiles[(x, y)]
                rect = Rectangle(RED_E, (dim[3]-dim[1])/400*0.25, (dim[2]-dim[0])/400*0.25)
                rect.set_stroke(width=DEFAULT_STROKE_WIDTH/3)
                rect.move_to(tile.get_corner(UL), aligned_edge=UL)
                rect.shift((dim[0]/400*0.25*RIGHT) + (dim[1]/400*0.25*DOWN))
                tile_predictions.append(rect)
        
        conf_texts = [Text(f"{num:.2f}", font_size=16, color=RED_E) for num in confidences]
        column = VGroup(*conf_texts).arrange(DOWN, buff=0.1)
        column.move_to(np.array([-6.6, -0.25, 0]))

        self.play(*[Create(mobject) for mobject in tile_predictions], run_time=2)
        self.wait(0.5)
        self.play(LaggedStart(*[Create(num_text) for num_text in column], lag_ratio=0.5), run_time=2)
        self.wait(3)

        heading_convert = Text("Positioning Bounding Boxes on Original Image", weight=BOLD, font_size=32)
        heading_convert.move_to(np.array([0, 4.5, 0]))

        sub_images.add(*tile_predictions)

        self.play(Transform(heading_yolo, heading_convert, replace_mobject_with_target_in_scene=True))
        self.play(ShrinkToCenter(sub_images))
        self.remove(sub_images)

        main_image = ImageMobject(image_array)
        main_image.height = 3.65
        self.add(main_image)

        predictions = Group()
        with open(Path("methodology", "tile_predictions.txt")) as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split()
                x, y = map(int, parts[:2])
                conf = float(parts[2])
                dim = tuple(map(float, parts[3:]))
                rect = Rectangle(RED_E, (dim[3]-dim[1])/4912*main_image.height, (dim[2]-dim[0])/7360*main_image.width)
                rect.set_stroke(width=DEFAULT_STROKE_WIDTH/3)
                rect.move_to(main_image.get_corner(UL), aligned_edge=UL)
                rect.shift(((x+dim[0])/7360*main_image.width*RIGHT) + ((y+dim[1])/4912*main_image.height*DOWN))
                predictions.add(rect)
        self.add(predictions)

        self.play(
            GrowFromCenter(main_image),
            GrowFromPoint(predictions, np.array([0, 0, 0]))
        )
        self.wait(2)
        self.play(
            FadeOut(main_image),
            FadeOut(predictions)
        )
        main_image.scale(2.2)
        main_image.shift(0.25*DOWN)
        predictions.scale(2.2, about_point=ORIGIN)
        predictions.shift(0.25*DOWN)
        self.play(
            FadeIn(main_image),
            FadeIn(predictions)
        )
        self.wait(3)
        with open(Path("methodology", "fireball.txt")) as file:
            parts = list(map(float, file.readline().strip().split()))
            box = Rectangle(RED_E, (parts[4]-parts[2])/4912*main_image.height, (parts[3]-parts[1])/7360*main_image.width)
            box.move_to(main_image.get_corner(UL), aligned_edge=UL)
            box.shift((parts[1]/7360*main_image.width*RIGHT) + (parts[2]/4912*main_image.height*DOWN))
        
        max_text: Text = column[confidences.index(max(confidences))]
        bold_max_text: Text = Text(max_text.text, font_size=16, color=RED_E, weight=BOLD)
        bold_max_text.move_to(max_text)
        self.bring_to_front(max_text)

        def text_transform(o: Mobject):
            o.move_to(max_text.get_center())
            o.fade(1)
            return o
        
        heading_merge = Text("Merging Intersecting Bounding Boxes", weight=BOLD, font_size=32)
        heading_merge.move_to(np.array([0, 4.5, 0]))

        self.play(Transform(heading_convert, heading_merge, replace_mobject_with_target_in_scene=True))
        self.wait(0.5)
        self.play(Transform(max_text, bold_max_text, replace_mobject_with_target_in_scene=True))
        self.play(
            Transform(predictions, box, replace_mobject_with_target_in_scene=True),
            *[ApplyFunction(text_transform, text) for text in column if text != max_text],
        )
        self.wait(2)

        heading_final = Text("Final Prediction", weight=BOLD, font_size=32)
        heading_final.move_to(np.array([0, 4.5, 0]))

        self.play(
            bold_max_text.animate.move_to(box.get_corner(UL) + (0.15*UP) + (0.25*RIGHT)).set(run_time=2),
            Transform(heading_merge, heading_final, replace_mobject_with_target_in_scene=True)
        )
        self.wait(5)

        self.play(
            FadeOut(main_image, box, bold_max_text, heading_final)
        )


class FireballFails(Scene):
    def construct(self):
        image_files = [file for file in os.listdir(Path("fireball_fails")) if file.endswith(".jpg")]
        for image_file in image_files:
            
            image = ImageMobject(io.imread(Path("fireball_fails", image_file)))
            image.width = 14.3
            self.add(image)
            self.wait(5)

            rects = []
            texts = []

            with open(Path("fireball_fails", image_file.split(".")[0] + ".txt")) as file:
                lines = file.readlines()
                for line in lines:
                    correct, conf, x0, y0, x1, y1 = map(float, line.strip().split())

                    colour = GREEN_E if correct else RED_E

                    rect = Rectangle(colour, (y1-y0)/4912*9.35, (x1-x0)/7360*14)
                    rect.move_to(image.get_corner(UL), aligned_edge=UL)
                    rect.shift((x0/7360*14.3*RIGHT) + (y0/4912*9.5436957*DOWN))
                    rects.append(rect)

                    text = Text(f"{conf:.2f}", color=colour, font_size=16, weight=BOLD)
                    if y0 > 100:
                        text.move_to(rect.get_corner(UL))
                        text.shift((0.15*UP) + (0.25*RIGHT))
                    else:
                        text.move_to(rect.get_corner(DL))
                        text.shift((0.15*DOWN) + (0.25*RIGHT))
                    texts.append(text)
            
            self.play(
                *[Create(rect) for rect in rects],
                *[Write(text) for text in texts],
                run_time=2
            )
            self.wait(10)