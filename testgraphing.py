import pandas as pd
import matplotlib.pyplot as plt
#I need normalized graphs for load vs displacement made from this data, as well critical data (max load, yield load, approximate elastic modulus, etc) extracted.

def main():

    df = pd.read_csv("Test1.Stop.csv", sep = ",")
    #print(df.to_string())
    # ---column names---
    # "Total Time (s)"
    # "Cycle Elapsed Time (s)"
    # "Total Cycles"
    # "Elapsed Cycles"
    # "Step"
    # "Total Cycle Count(8800 (0,3) Waveform)"
    # "Position(8800 (0,3):Position) (mm)"
    # "Load(8800 (0,3):Load) (kN)"
    # "Extension(880and0 (0,3):Strain 1) (mm)"
    # ------

    #print(df.loc[:, 'Total Time (s)'])

    normloadpos = normalize(df.loc[:, 'Load(8800 (0,3):Load) (kN)'], df.loc[:, 'Position(8800 (0,3):Position) (mm)'])

    max = max_load(normloadpos)
    print(max)

    df.plot(x = 'Position(8800 (0,3):Position) (mm)', y = 'Load(8800 (0,3):Load) (kN)')

    plt.title('1A')
    plt.legend().set_visible(False)
    plt.xlabel('Position (in)')
    plt.ylabel('Load (kN)')
    plt.show()


def normalize(load, position):
    #So subtract/add the intial value of position to all the values in that column so the first one is, then do the same for load
    initial_pos = abs(position.iloc[0])
    position.loc[:] += initial_pos
    #print(position)

    initial_load = abs(load.iloc[0])
    load.loc[:] += initial_load
    #print(load)

    position.loc[:] /= 25.4
    position.loc[:] /= 8

    df = pd.concat([load, position], axis = 1)
    #print(df.to_string)

    return df

def max_load(loadpos):
    return loadpos.max()

#def annot_max(max, ax=None):
    xmax = x[np.argmax(y)]
    ymax = y.max()
    text= "x={:.3f}, y={:.3f}".format(xmax, ymax)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.94,0.96), **kw)

#def approx_elastic_mod(loadpos, max):
    


if __name__ == "__main__":
    main()
