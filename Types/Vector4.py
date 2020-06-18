class Vector4:
    def __init__(self, a=0, b=0, c=0, d=0):
        self.x = a
        self.y = b
        self.z = c
        self.w = d

    def __add__(self, other):
        return Vector4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __radd__(self, other):
        return Vector4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __mul__(self, scalar):
        return Vector4(self.x * scalar, self.y * scalar, self.z * scalar, self.w * scalar)

    def __rmul__(self, scalar):
        return Vector4(self.x * scalar, self.y * scalar, self.z * scalar, self.w * scalar)

    def __neg__(self):
        return Vector4(-self.x, -self.y, -self.z, -self.w)

    def __pos__(self):
        return Vector4(self.x, self.y, self.z, self.w)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ", " + str(self.w) + ")"
