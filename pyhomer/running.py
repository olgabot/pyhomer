import os

import pybedtools

DIRECTIONS = 'upstream', 'downstream'

def construct_homer_command(foreground_filename, background_filename,
                            homer_flags, findMotifsGenome,
                            out_dir=None, force=False):
    if out_dir is None:
        out_dir = foreground_filename.replace('.bed', '')
    if force or not os.path.exists(out_dir):
        command = '{} {} hg19 {} -bg {} {}'.format(
            findMotifsGenome, foreground_filename, out_dir, background_filename,
            homer_flags)
        return command
    else:
        raise ValueError('{} already exists, not creating command. To create '
                         'the command anyway, use force=True')


def unique_regions(bed):
    return pybedtools.BedTool(list(set(x for x in bed)))


def get_flanking_intron(bed, direction, genome, nt):
    if direction == 'downstream':
        intron = bed.flank(l=0, r=nt, s=True, genome=genome)
    elif direction == 'upstream':
        intron = bed.flank(l=nt, r=0, s=True, genome=genome)
    else:
        raise ValueError('Only "downstream" and "upstream" are accepted '
                         'direction values, not "{}"'.format(direction))

    # Saved every exon that was exactly upstream or downstream of a junction,
    # So when taking the flanking sequence, there's a lot of repetition
    intron = unique_regions(intron)
    return intron



class ForegroundBackgroundPair(object):

    def __init__(self, foreground, background):
        self.foreground = foreground
        self.background = background
        self.beds = {'foreground': self.foreground,
                     'background': self.background}

    def __repr__(self):
        s = 'ForegroundBackgroundPair:\nForeground: {} ({}) entries' \
            '\nBackground: {} ({} entries)'.format(
                self.foreground.fn, len(self.foreground),
                self.background.fn, len(self.background))
        return s

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def _prefix(bed, x_ground):
        return bed.fn.replace(x_ground, '').replace('.bed', '').rstrip('_')

    def intersect(self, other, other_name):
        intersections = {}
        for x_ground, bed in self.beds.items():
            prefix = self._prefix(bed, x_ground)
            intersected_filename = '{prefix}_{other_name}_{x_ground}.bed'.format(
                prefix=prefix, other_name=other_name, x_ground=x_ground)
            bed.intersect(other).saveas(intersected_filename)
            intersected = pybedtools.BedTool(intersected_filename)
            intersections[x_ground] = intersected
        return ForegroundBackgroundPair(**intersections)

    def flanking_intron(self, direction, genome, nt):
        introns = {}
        for x_ground, bed in self.beds.items():
            prefix = self._prefix(bed, x_ground)
            intron_filename = '{prefix}_{direction}{nt}_{name}.bed'.format(
                prefix=prefix, direction=direction, nt=nt, name=x_ground)
            intron = get_flanking_intron(bed, direction, genome, nt)
            intron.saveas(intron_filename)
            intron = pybedtools.BedTool(intron_filename)

            introns[x_ground] = intron
        return ForegroundBackgroundPair(**introns)
