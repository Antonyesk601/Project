f= open("grid.txt","w")
screenWidth=1300
screenHeight=750
tileSize= 25
worldPositions = []
for row in range(0,screenHeight//tileSize):
    row = []
    for column in range (0,screenWidth//tileSize):
        row.append(0)
    worldPositions.append(row)
    strings="["
    for i in row:
        strings=strings+str(i)+","
    strings=strings[:len(strings)-1]+"]"
    f.write(strings+"\n")