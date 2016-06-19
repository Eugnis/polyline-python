from NZ_unit import *
import matplotlib.pyplot as plt #for draw

def output(polyline, file=None):
    print("Polyline points", file=file)
    polyline.PrintPoints(file)

    print("Perimeter: ", str(polyline.Perimeter()), file=file)
    intersections = polyline.SelfIntersections()
    if intersections != []:
        print("Self-Intersections: ", str(polyline.SelfIntersections()), file=file)
    else:
        print("Self-Intersections not found.", file=file)

    print("Enter point to check if it's in polyline (in format X Y)")
    XY = input().split(" ")
    if polyline.CheckIfPointInside(float(XY[0]), float(XY[1])):
        print("Point (" + XY[0] + ", " + XY[1] + ") is in polyline.", file=file)
    else:
        print("Point (" + XY[0] + ", " + XY[1] + ") not in polyline.", file=file)

    if file == None:
        print("Show Polyline graphically (y or n)?")
        choose = input()
        if choose == "y":
            Draw(polyline.polyline_points)
    return

def Draw(polyline_points):  # draw the polyline
    x = [p.x for p in polyline_points]  # take X coordinate for each point
    y = [p.y for p in polyline_points]  # take Y coordinate for each point
    plt.plot(x, y, marker='o', color='b', linestyle='-')  # draw points
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()
    return


def main():
    input_polyline = []
    print("Choose input type (1-console, 2-text file)?")
    choose = int(input())
    if choose == 2:
        print("Enter filename:")
        filename = input()
        points = [line.rstrip('\n') for line in open(filename)]
        for p in points:
            XY = p.split(" ")
            input_polyline.append((float(XY[0]), float(XY[1])))
    else:
        print("Number of points?")
        count = int(input())
        print("Enter " + str(count) + " points (in format X Y)")
        for i in range(0,count):
            XY = input().split(" ")
            input_polyline.append((float(XY[0]), float(XY[1])))

    polyline = Polyline(input_polyline)

    output(polyline)

    print("Save output to file (y or n)?")
    choose = input()
    if choose == "y":
        print("Enter filename:")
        filename = input()
        f = open(filename, 'w')
        output(polyline, f)
        f.close()
        print("Output saved in file", filename)
    return


if __name__ == "__main__":
    main()