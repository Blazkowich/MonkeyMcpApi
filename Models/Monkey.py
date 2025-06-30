class Monkey:
    def __init__(self, Name: str, Location: str, Details: str, Image: str, Population: int, Latitude: float, Longitude: float):
        self.Name = Name
        self.Location = Location
        self.Details = Details
        self.Image = Image
        self.Population = Population
        self.Latitude = Latitude
        self.Longitude = Longitude

    @staticmethod
    def from_dict(data: dict):
        """Creates a Monkey object from a dictionary."""
        return Monkey(
            Name=data.get("Name"),
            Location=data.get("Location"),
            Details=data.get("Details"),
            Image=data.get("Image"),
            Population=data.get("Population"),
            Latitude=data.get("Latitude"),
            Longitude=data.get("Longitude")
        )

    def to_dict(self) -> dict:
        """Converts the Monkey object to a dictionary."""
        return {
            "Name": self.Name,
            "Location": self.Location,
            "Details": self.Details,
            "Image": self.Image,
            "Population": self.Population,
            "Latitude": self.Latitude,
            "Longitude": self.Longitude
        }