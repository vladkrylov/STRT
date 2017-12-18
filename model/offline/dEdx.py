from model import Model, Hit, Track, Event, Run


def plot_dEdx(runs):
    pass

if __name__ == '__main__':
    m = Model()
    m.load_all('../../indata/out.root')
    
    runs_to_plot = ['Run12, Run15']
    