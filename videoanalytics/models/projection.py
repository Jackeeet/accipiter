class Projection:
    def __init__(self, proj_min: float, proj_max: float) -> None:
        self.min = proj_min
        self.max = proj_max

    def overlaps(self, other: 'Projection') -> bool:
        return not (self.max < other.min or other.max < self.min)

    def __repr__(self) -> str:
        return f"Projection({self.min}, {self.max})"
