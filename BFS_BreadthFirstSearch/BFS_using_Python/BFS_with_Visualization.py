import cv2
import numpy as np
import time

gridLength = 50
gridWidth = 50

# Read any random color image to create the grid
clrImg = cv2.imread('img01.png')
grayImg = cv2.cvtColor(clrImg, cv2.COLOR_BGR2GRAY)

# Changing the dimentions of read image to required grid size
resizedImg = cv2.resize(grayImg, (gridLength+2,gridWidth+2))

gridImg = resizedImg

# Converting the gray image to Binary Image
# 255 corresponds to free space
# 0 corresponds to outer boundary
for i in range(0, gridLength+2):
    for j in range(0, gridWidth + 2):
        if(i==0 or j==0 or i==(gridLength+1) or j==(gridWidth+1)):
            gridImg[i][j] = 0
        else:
            gridImg[i][j] = 255

#Different Obstacle Configurations
gridImg[3:gridWidth - 3, 3:gridLength - 3] = 0
gridImg[4:gridWidth - 4, 4:gridLength - 4] = 255
gridImg[3,7:10] = 255

gridImg[5:gridWidth - 5, 5:gridLength - 5] = 0
gridImg[6:gridWidth - 6, 6:gridLength - 6] = 255
gridImg[gridWidth - 6, 35:gridLength - 10] = 255

gridImg[7:gridWidth - 7, 7:gridLength - 7] = 0
gridImg[8:gridWidth - 8, 8:gridLength - 8] = 255
gridImg[7,38:gridLength - 7] = 255

gridImg[9:gridWidth - 9, 9:gridLength - 9] = 0
gridImg[10:gridWidth - 10, 10:gridLength - 10] = 255
gridImg[gridWidth - 10, 12:16] = 255

gridImg[11:gridWidth - 11, 11:gridLength - 11] = 0
gridImg[12:gridWidth - 12, 12:gridLength - 12] = 255
gridImg[11, 20:gridLength - 25] = 255

gridImg[13:gridWidth - 13, 13:gridLength - 13] = 0
gridImg[14:gridWidth - 14, 14:gridLength - 14] = 255
gridImg[gridWidth - 14, 20:gridLength - 25] = 255

gridImg[15:gridWidth - 15, 15:gridLength - 15] = 0
gridImg[16:gridWidth - 16, 16:gridLength - 16] = 255
gridImg[15, 28:gridLength - 20] = 255

gridImg[17:gridWidth - 17, 17:gridLength - 17] = 0
gridImg[18:gridWidth - 18, 18:gridLength - 18] = 255
gridImg[gridWidth - 18, 20:22] = 255

gridImg[19:gridWidth - 19, 19:gridLength - 19] = 0
gridImg[20:gridWidth - 20, 20:gridLength - 20] = 255
gridImg[21:23, 19] = 255

# List of Parent Nodes
parentNodes = []
childNodes = []

# List of Children Nodes corresponding to each Parent Node
childrenNodes = []

for i in range(1, gridLength + 1):
    for j in range(1, gridWidth + 1):
        if gridImg[i][j] != 0:
            parentNodes.append((i,j))

for tuple1 in parentNodes:
    x1 = tuple1[0]
    y1 = tuple1[1]
    for tuple2 in parentNodes:
      x2 = tuple2[0]
      y2 = tuple2[1]

      if ((abs(x1-x2) == 1) and (y1-y2 == 0)) or ((x1 - x2 == 0) and (abs(y1-y2)==1)):
          childNodes.append(tuple2)

    childrenNodes.append(list(childNodes))
    childNodes.clear()

# Start Time to calculate the Time Complexity
startTime = time.time()

# Start Node Position
startNode = (gridLength//2, gridWidth//2)
# Goal Node Position
goalNode = (gridLength, gridWidth)
# Queue of BFS
queue = []
# List of Visited Nodes
visitedNodes = []

currentNode = startNode

queue.append(currentNode)

# Function for finding the final path from the visited nodes
def findPath(v):
    print("Number of visited Nodes: ", len(v))
    finalPath = []
    v.reverse()
    finalPath.append(v[0])
    revX1 = v[0][0]
    revY1 = v[0][1]
    for revTuple2 in v:
        revX2 = revTuple2[0]
        revY2 = revTuple2[1]
        if((abs(revX1-revX2) == 1) and (revY1 - revY2 == 0)) or ((revX1 - revX2 == 0) and (abs(revY1 -revY2)==1)):
            finalPath.append(revTuple2)
            revX1 = revTuple2[0]
            revY1 = revTuple2[1]

    finalPath.reverse()
    # print("Final Path between ", startNode, " and ", goalNode, " is ", finalPath)
    return finalPath

# Main BFS Algorithm
while currentNode != goalNode:
    if(queue[0] == goalNode):
        visitedNodes.append(queue.pop(0))
        fpath = findPath(visitedNodes)
        # print(fpath)
        break
    else:
        visitedNodes.append(queue.pop(0))
        indexOfParentNode = parentNodes.index(visitedNodes[-1])
        for child in childrenNodes[indexOfParentNode]:
            if child not in (visitedNodes + queue):
                queue.append(child)

# cost v/s time
print("Time taken: ", (time.time() - startTime)*1000)
print("Solution cost: ", len(fpath))

# Color Visualization
blueChannel = np.copy(gridImg)
greenChannel = np.copy(gridImg)
redChannel = np.copy(gridImg)

for item in fpath:
    redChannel[item] = 0
    blueChannel[item] = 0

blueChannel[startNode] = 0
redChannel[startNode] = 255
greenChannel[startNode] = 0

blueChannel[goalNode] = 255
greenChannel[goalNode] = 0
redChannel[goalNode] = 0

colorGrid = cv2.merge((blueChannel, greenChannel, redChannel))

cv2.namedWindow('final', cv2.WINDOW_NORMAL)
opWindowSize = 1000
cv2.resizeWindow('final', opWindowSize, opWindowSize)
cv2.imshow("final", colorGrid)
cv2.waitKey()
cv2.destroyAllWindows()
