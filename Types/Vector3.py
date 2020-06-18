class Vector3:

    def __init__(self, a=0, b=0, c=0):
        self.x = a
        self.y = b
        self.z = c

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __radd__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __pos__(self):
        return Vector3(self.x, self.y, self.z)

    def __xor__(self, other):
        cx = self.y * other.z - self.z * other.y
        cy = self.z * other.x - self.x * other.z
        cz = self.x * other.y - self.y * other.x
        return Vector3(cx, cy, cz)

    def cross(self, other):
        return self ^ other

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"
