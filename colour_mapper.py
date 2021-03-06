import matplotlib.cm as cm
import matplotlib.colors as colors


class RGBColourMapper:

    def __init__(self, colour_mapper_type='inferno', norm_min=0, norm_max=1):
        self.norm_min = norm_min
        self.norm_max = norm_max
        self.norm = colors.Normalize(vmin=self.norm_min, vmax=self.norm_max)
        self.mapper = cm.ScalarMappable(norm=self.norm, cmap=cm.get_cmap(colour_mapper_type))

    def generate_hex_colour(self, value):
        rgb = self.mapper.to_rgba(value)[:3]
        return '#%02x%02x%02x' % tuple([int(255 * colour) for colour in rgb])