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

    initpos = abs(df.loc[0, 'Position(8800 (0,3):Position) (mm)'])
    normloadpos = normalize(df.loc[:, 'Load(8800 (0,3):Load) (kN)'], df.loc[:, 'Position(8800 (0,3):Position) (mm)'])
    xmax, ymax = max_load(normloadpos)
    #print("initpos: ", initpos)
    avgslope = approx_elastic_mod(xmax, initpos, ymax)
    print(avgslope)

    df.plot(x = 'Position(8800 (0,3):Position) (mm)', y = 'Load(8800 (0,3):Load) (kN)')
    annot_max(xmax, ymax, plt)
    plt.title('1A')
    plt.legend().set_visible(False)
    plt.xlabel('Position (mm)')
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

    df = pd.concat([load, position], axis = 1)
    #print(df.to_string)

    return df

def max_load(loadpos):
    max_value = loadpos['Load(8800 (0,3):Load) (kN)'].max()
    x_max = loadpos[loadpos['Load(8800 (0,3):Load) (kN)'] == max_value]['Position(8800 (0,3):Position) (mm)'].values[0]
    return x_max, max_value 

def annot_max(xmax, ymax, ax=None):
    text= "Max Load: x={:.3f}, y={:.3f}".format(xmax, ymax)
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    #arrowprops = dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")

    kw = dict(xycoords='data',textcoords="axes fraction", bbox=bbox_props, ha="right", va="top")
    
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.45,0.07), **kw)

def approx_elastic_mod(pos, initpos, load):
    # strain = xmax/ initial position not normalized
    # e = stress/strain
    # return e * 10^-9

    csa = 0.00050671

    strain = pos/initpos
    stress = (load*1000)/csa
    e = stress/strain
    return e * 0.000000001


if __name__ == "__main__":
    main()
