import pandas as pd
import matplotlib.pyplot as plt

def try_float(x):
    try:
        return float(x)
    except:
        return float('nan')

def plot_terms():
    df = pd.read_excel(r"output files\incident reports JOIN da caseload JOIN prod1 JOIN prod2.xlsx")
    fig, axes = plt.subplots(ncols = 3, sharey = True)
    for ax, term in zip(axes, ['CJ Term', 'SP Term', 'Supervision Term']):
       df[term].apply(try_float).plot.box(ax = ax)
       ax.set_title(term)
    axes[0].set_ylabel('Days of term')
    fig.savefig('output files/jail sentences in sf_crime_2022 dataset.png')
    
if __name__ == '__main__':
    plot_terms()