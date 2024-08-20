films = [
    {"watches":12},
    {"watches":124},
    {"watches":64},
    {"watches":1},
    {"watches":9},
    {"watches":19},
]

def sort(films):

    sorted = False
    while sorted == False:
        sorted = True
        for i in range(0, (len(films)-1)):
            
            if films[i]['watches'] < films[i+1]['watches']:
                placeholder = films[i]
                films[i] = films[i+1]
                films[i+1] = placeholder
                sorted = False

sort(films)

print(films)