class FirstStart:

    wasClicked : int = 1

    def __init__(self, wasClicked):
        self.wasClicked = 1

    def getClicked(wasClicked=wasClicked) -> int:
        return wasClicked

    def setClicked(self,clicked : int) -> None:
        self.wasClicked = clicked