"""Plotting utility functions"""
import pandas as pd
import matplotlib.pyplot as plt

def plot_save_to_file(name, file_name):
    """Save plot to file"""
    plt.title(name)
    plt.savefig(file_name, bbox_inches='tight')

def plot_adm_history_of_systems(systems: pd.DataFrame) -> bool:
    """Generate plot of system ADM levels"""
    if (len(systems)) < 1:
        return False

    systems.created_at = pd.to_datetime(systems.created_at)
    systems.pivot(index='created_at', columns='system_name', values='adm').plot(
        ylim=(1.0, 6.2), xlabel='Date', ylabel='ADM').legend(bbox_to_anchor=(1, 1))

    return True
