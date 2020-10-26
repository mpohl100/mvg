from lib.timetable import MergeType

class Config:
    def __init__(self, subway_stride: int = 4, sbahn_stride: int = 8, minutes: int = 1440, verbosity: int = 0, deduce_schedule: bool = False, show_net: bool = False):
        self.deduce_schedule = deduce_schedule
        self.nb_subway = subway_stride
        self.nb_sbahn = sbahn_stride
        self.minutes = minutes
        self.verbosity = verbosity
        self.show_net = show_net
        self.num_passengers_per_route = 0
        self.merge_type = MergeType.BEFORE
        self.passengers_fast = True
        self.files = None

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def str2mergetype(v):
    if v.lower() in ('b', 'B', 'before', 'BEFORE'):
        return MergeType.BEFORE
    elif v.lower() in ('zb', 'ZB', 'zip_before', 'ZIP_BEFORE'):
        return MergeType.ZIP_BEFORE
    elif v.lower() in ('za', 'ZA', 'zip_after', 'ZIP_AFTER'):
        return MergeType.ZIP_AFTER
    elif v.lower() in ('a', 'A', 'after', 'AFTER'):
        return MergeType.AFTER
    else:
        raise argparse.ArgumentTypeError('String value expected.{b, zb, za, a}')

def parse_config():
    import argparse
    parser = argparse.ArgumentParser(description='MVG Simulation configuration.')
    parser.add_argument('-f','--files', nargs='+',
                        help='list of json files containing the network info.', required=True)
    parser.add_argument('-v', '--verbosity', type=int, help='verbosity of the output.', default=0)
    parser.add_argument('-d', '--deduce-schedule', type=str2bool, nargs='?', help='deduce a schedule for the network.', default=False)
    parser.add_argument('-s', '--show-network', type=str2bool, nargs='?', help='show an animation of the network.', default=False)
    parser.add_argument('-p', '--num-passengers-per-route', type=int, help='number of passengers per route', default=0)
    parser.add_argument('-dt', '--deduction-type', type=str2mergetype, help='merge type how the schedule for the network should be arranged at the main station of local centers.', default=MergeType.BEFORE)
    parser.add_argument('-pf', '--passengers-fast', type=str2bool, help='a faster route finding algorithm is used with the trade off that not always the shortest route in terms of train switches is found.', default=True)
    args = vars(parser.parse_args())
    print(args)
    config = Config()
    config.files = args['files']
    config.verbosity = args['verbosity']
    config.deduce_schedule = args['deduce_schedule']
    config.show_net = args['show_network']
    config.num_passengers_per_route = args['num_passengers_per_route']
    config.merge_type = args['deduction_type']
    config.passengers_fast = args['passengers_fast']
    return config
