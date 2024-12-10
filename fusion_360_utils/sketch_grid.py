import adsk.core
import adsk.fusion

MM_IN_CM = 10


class SketchGrid:
    def __init__(self,
                 sketch: adsk.fusion.Sketch,
                 origin: adsk.fusion.SketchPoint,
                 x_length: float,
                 x_cell_count: int,
                 y_length=None,
                 y_cell_count=None
                 ):
        # validate input:
        if not sketch.isParametric:
            raise ValueError("Sketch has to be parametric")
        elif not origin.is2D:
            raise ValueError("Point has to be on the 2D sketch plane")

        # set default y values if not specified:
        if y_length is None:
            y_length = x_length
        if y_cell_count is None:
            y_cell_count = x_cell_count

        self.sketch = sketch
        self.origin = origin

        self.x_length = x_length
        self.y_length = y_length

        self.x_cell_count = x_cell_count
        self.y_cell_count = y_cell_count

        self.draw_grid()

    def draw_grid(self):
        # collect necessary objects:
        sketch_lines = self.sketch.sketchCurves.sketchLines
        sketch_points = self.sketch.sketchPoints
        sketch_constraints = self.sketch.geometricConstraints

        # draw first grid lines (x,y). They correspond to the bottom and leftmost grid lines in a conventional XY plane:
        x_axis_end_point = sketch_points.add(adsk.core.Point3D.create(self.x_length, self.origin.geometry.y, 0))
        y_axis_end_point = sketch_points.add(adsk.core.Point3D.create(self.origin.geometry.x, self.y_length, 0))

        x_first_grid_line = sketch_lines.addByTwoPoints(self.origin, x_axis_end_point)
        y_first_grid_line = sketch_lines.addByTwoPoints(self.origin, y_axis_end_point)

        # collect input values for rectangular pattern constraint (x direction):
        x_cell_count_value_input = adsk.core.ValueInput.createByReal(self.x_cell_count + 1)
        x_length_value_input = adsk.core.ValueInput.createByReal(self.x_length * MM_IN_CM)

        x_rectangular_pattern_input = sketch_constraints.createRectangularPatternInput([x_first_grid_line],
                                                                                       adsk.fusion.PatternDistanceType.ExtentPatternDistanceType)
        x_rectangular_pattern_input.setDirectionOne(y_first_grid_line, x_cell_count_value_input, x_length_value_input)

        # collect input values for rectangular pattern constraint (y direction):
        y_cell_count_value_input = adsk.core.ValueInput.createByReal(self.y_cell_count + 1)
        y_length_value_input = adsk.core.ValueInput.createByReal(self.y_length * MM_IN_CM)

        y_rectangular_pattern_input = sketch_constraints.createRectangularPatternInput([y_first_grid_line],
                                                                                       adsk.fusion.PatternDistanceType.ExtentPatternDistanceType)
        y_rectangular_pattern_input.setDirectionOne(x_first_grid_line, y_cell_count_value_input, y_length_value_input)

        print(x_length_value_input.realValue)

        # draw grid:
        sketch_constraints.addRectangularPattern(x_rectangular_pattern_input)
        sketch_constraints.addRectangularPattern(y_rectangular_pattern_input)
