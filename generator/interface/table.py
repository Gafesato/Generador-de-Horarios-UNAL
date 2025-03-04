import flet as ft

from generator.interface.widget import Widget


# Widget DataTable
class Table(Widget):
    def __init__(self, data, left=0, top=0):
        super().__init__("", left, top)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Header 1")),
                ft.DataColumn(ft.Text("Header 2")),
            ],
            rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(cell)) for cell in row]) for row in data],
        )

    def create(self):
        return ft.Container(content=self.table, left=self.left, top=self.top)




