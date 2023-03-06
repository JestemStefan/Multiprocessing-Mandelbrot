import cmath
from math import floor
import os
from PIL import Image

from multiprocessing import Pool, freeze_support


class MandelbrotGenerator:
    image_x = 2560
    image_y = 1440
    limit = 100_000_000

    def __init__(self, max_iterations) -> None:
        self.max_iterations = max_iterations
    

    def is_coord_in_mandelbrot_set(self, coord):
            complex_num = complex(*coord)
            result = complex_num

            iteration_color = (0,0,0)

            for iter_idx in range(self.max_iterations):
                result = result*result + complex_num

                if abs(result.real) < self.limit or abs(result.imag) < self.limit:
                    color = floor(iter_idx/4)
                    iteration_color = (color, color, color)

            return iteration_color

        

if __name__ == '__main__':
    
    i = 0
    max_iterations = 1024
    for zoom in ((1.2**zoom) for zoom in range(29, 30)):
        # center_x = -0.10109
        # center_y = 0.95628

        center_x, center_y = -0.743643887037158704752191506114774, 0.131825904205311970493132056385139

        x_min, x_max =  center_x - (1/zoom), center_x + (1/zoom)
        y_min, y_max = center_y - (0.5625/zoom), center_y + (0.5625/zoom)

        print(f"Rendering area x={x_min, x_max} y={y_min, y_max}")
        
        im = Image.new(mode="RGB", size=( MandelbrotGenerator.image_x, MandelbrotGenerator.image_y))
        
        x_step = (x_max-x_min)/MandelbrotGenerator.image_x
        y_step = (y_max-y_min)/MandelbrotGenerator.image_y
        

        coords = ((x_min + x_step*x, y_min + y_step * y) for y in range(MandelbrotGenerator.image_y) for x in range(MandelbrotGenerator.image_x))

        mandelbrot = MandelbrotGenerator(max_iterations=max_iterations)

        freeze_support()
        with Pool(16) as p:
            data = p.map(mandelbrot.is_coord_in_mandelbrot_set, coords)
            
            im.putdata(data)

        # This method will show image in any image viewer
        im.save(f"zoom_{i:02d}.png", "PNG")
        i += 1