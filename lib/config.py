

class Config:
    def __init__(self, subway_stride: int = 4, sbahn_stride: int = 8, minutes: int = 1440, verbosity: int = 0, deduce_schedule: bool = False, show_net: bool = False):
        self.deduce_schedule = deduce_schedule
        self.nb_subway = subway_stride
        self.nb_sbahn = sbahn_stride
        self.minutes = minutes
        self.verbosity = verbosity
        self.show_net = show_net
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

def parse_config():
    import argparse
    parser = argparse.ArgumentParser(description='MVG Simulation configuration.')
    parser.add_argument('-f','--files', nargs='+',
                        help='list of json files containing the network info.', required=True)
    parser.add_argument('-v', '--verbosity', type=int, help='verbosity of the output.', default=0)
    parser.add_argument('-d', '--deduce-schedule', type=str2bool, nargs='?', help='deduce a schedule for the network.', default=False)
    parser.add_argument('-s', '--show-network', type=str2bool, nargs='?', help='show an animation of the network.', default=False)
    args = vars(parser.parse_args())
    print(args)
    config = Config()
    config.files = args['files']
    config.verbosity = args['verbosity']
    config.deduce_schedule = args['deduce_schedule']
    config.show_net = args['show_network']
    return config
