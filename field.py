import matplotlib.pyplot as plt
import matplotlib.colors

def main():
    field = (np.random.rand(5, 5) < .8) * 1
    print(field)
    plt.figure(figsize=(8,8))
    plt.imshow(field, cmap='collwarm')
    plt.show()

    rabbits = [(1, 1), (2, 3), (4, 4)]
    # method 1 to build an array of rabbit locations
    rabbits_arr = np.zeros((5, 5), dtype=int)
    for x, y in rabbits:
        rabbits_arr[x, y] = 2
    plt.imshow(rabbits_arr, cmap='binary')
    plt.show()

    overlay = np.maximum(field, rabbits_arr)

    # define a custom color map: 0 -> black, 1 -> green, 2 -> white
    my_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ['black', 'green', 'white'])
    plt.imshow(overlay, cmap=my_cmap, vmin=0, vmax=2)
    plt.show()

    foxes = [(1, 1), (2, 2), (0, 4)]
    foxes_arr = np.zeros((5, 5), dtype=int)
    for x, y in foxes:
        foxes_arr[x, y] = 3
        