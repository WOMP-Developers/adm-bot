import pandas as pd
import matplotlib.pyplot as plt

def plot_save(name):
    plt.title(name)

    file_name = f'{name}.png'
    plt.savefig(file_name, bbox_inches='tight')

    return file_name

def plot_system_adm(system):
    if (len(system)) < 1:
        return False

    system.created_at = pd.to_datetime(system.created_at)
    system.plot(x='created_at', y='adm', xlabel='Date', ylabel='ADM', legend=False)

    return True
