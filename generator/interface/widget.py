# Clase base para los widgets personalizados
class Widget:
    def __init__(self, value="", left=0, top=0, width=200, height=50, page=None):
        self.value = value
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.page = page  # Referencia a la página

    def create(self):
        raise NotImplementedError("Debes implementar el método 'create'.")
