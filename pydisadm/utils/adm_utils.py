"""ADM utility functions"""

def adm_from_index(military: int, industrial: int, strategic: int) -> float:
    """Calculate ADM from index values"""
    military_values = [ 0, 0.6, 1.2, 1.7, 2.1, 2.5 ]
    industrial_values = [ 0, 0.6, 1.2, 1.7, 2.1, 2.5 ]
    strategic_values = [ 0, 0.4, 0.6, 0.8, 0.9, 1.0 ]

    adm_sum = sum([
        military_values[military],
        industrial_values[industrial],
        strategic_values[strategic]
    ])

    return min(6.0, 1.0 + adm_sum)
