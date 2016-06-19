import math

class Point:  # class-object for point coordinates (X,Y)
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Polyline:  # main class
    def __init__(self, pol):  # constructor
        self.polyline_points = []
        for dot in pol:
            self.polyline_points.append(Point(dot[0], dot[1]))  # insert points coordinates in list of "Point" objects
        return

    def Add(self, x, y):
        self.polyline_points.append(Point(x, y))
        return

    def PrintPoints(self, file=None):  # output points
        print("X  Y", file = file)
        for dot in self.polyline_points:
            print(str(dot.x) + "  " + str(dot.y), file = file)
        return

    def Segments(self):
        segments = []  # get all segments of polyline
        a = self.polyline_points[0]
        for i in range(1, len(self.polyline_points)):
            b = self.polyline_points[i]
            segments.append((a, b))
            a = b
        return segments

    def Perimeter(self):  # get perimeter of polyline
        length = 0.0
        segments = self.Segments()
        for seg in segments:
            distance = math.hypot(seg[1].x - seg[0].x, seg[1].y - seg[0].y)  # distance of segments
            length += distance  # add distances
        return length

    def SelfIntersections(self):
        epsilon = 1e-13

        def LineIntersects(p1, p2, q1, q2):  # check if intersection present for segment

            def Clockwise(p0, p1, p2):  # check for intersection of all point combinations
                dx1 = p1.x - p0.x
                dy1 = p1.y - p0.y
                dx2 = p2.x - p0.x
                dy2 = p2.y - p0.y
                d = dx1 * dy2 - dy1 * dx2  # distance
                if d > epsilon: return 1
                if d < epsilon: return -1
                if dx1 * dx2 < -epsilon or dy1 * dy2 < -epsilon: return -1
                if dx1 * dx1 + dy1 * dy1 < (dx2 * dx2 + dy2 * dy2) + epsilon: return 1
                return 0

            return (Clockwise(p1, p2, q1) * Clockwise(p1, p2, q2) <= 0) and (
                0 >= Clockwise(q1, q2, p1) * Clockwise(q1, q2, p2))

        def line(p1, p2):  # find A,B,C coefficients for line
            A = (p1.y - p2.y)
            B = (p2.x - p1.x)
            C = (p1.x * p2.y - p2.x * p1.y)
            return A, B, -C

        def IntersectionPoint(L1, L2):  # find intersection point for two lines
            D = L1[0] * L2[1] - L1[1] * L2[0]
            Dx = L1[2] * L2[1] - L1[1] * L2[2]
            Dy = L1[0] * L2[2] - L1[2] * L2[0]
            if D != 0:
                x = Dx / D
                y = Dy / D
                return x, y
            else:
                return False

        segments = self.Segments()
        present = []
        for seg1 in segments:  # for all combinations of segments
            for seg2 in segments:
                if (seg1[0] != seg2[1] and seg1[1] != seg2[0]) and \
                        (seg1[1] != seg2[1] and seg1[0] != seg2[0]):  # exclude points of segments connection
                    if LineIntersects(seg1[0], seg1[1], seg2[0], seg2[1]) == True:  # check if current segment intersect
                        L1 = line(seg1[0], seg1[1])  # find line coefficients (A, B, C) for segment parts
                        L2 = line(seg2[0], seg2[1])
                        P = IntersectionPoint(L1, L2)  # get point coordinate of intersection
                        present.append(P)  # add points to list
        answer = sorted(set(present))  # clean list from duplicate points
        return answer  # return list of points

    def CheckIfPointInside(self, x, y):  # check if point (x, y) is on polyline
        epsilon = 1e-13

        def isBetween(a, b, c):  # check if point c between points a and b
            cross_product = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)  # cross production
            if abs(cross_product) > epsilon: return False

            dot_product = (c.x - a.x) * (b.x - a.x) + (c.y - a.y) * (b.y - a.y)  # dot production
            if dot_product < 0: return False

            squared_length = (b.x - a.x) * (b.x - a.x) + (b.y - a.y) * (b.y - a.y)  # squared length
            if dot_product > squared_length: return False

            return True

        p = Point(x, y)
        isInside = False
        segments = self.Segments()
        for seg in segments:
            isInside = isBetween(seg[0], seg[1], p)  # check each segment if point inside of it
            if isInside == True:
                break
        return isInside

