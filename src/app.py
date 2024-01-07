import PySimpleGUI as sg
import query


sg.theme("Material1")

font = ("Helvetica", 16)
sg.set_options(font=font)

recents_headings = ["Product Name", "UPC", "Classification"]
recents_rows = [["Product 1", "1234567890", "Halal"], ["Product 2", "0987654321", "Haram"]]

layout = [
    [sg.Titlebar("Byte of 87")],
    [sg.Text("Welcome to Halal Scanner.")],
]

if recents_rows[0]:
    layout.append(
        [sg.Text("Recent Searches")]
    )
    layout.append(
        [sg.Table(values=recents_rows, headings=recents_headings)]
    )

layout.append([sg.Button("Scan a Barcode")])

layout.append([sg.Text("Enter a UPC to search:")])
layout.append([sg.InputText(), sg.Button("Search")])

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break
    if event == "Scan a Barcode":
        print("Scanning a barcode...")
    if event == "Search":
        query_upc = values[1]
        try:
            int(query_upc)
        except ValueError:
            sg.popup("Please enter a valid UPC.")
            continue
        print('You entered', query_upc)
        info = query.get_product_info(query_upc)
        if info:
            product_name = info['product']['product_name']
            ingredients = info['product']['ingredients_text']
            print(f"Product Name: {product_name}")
            print(f"Ingredients: {ingredients}")
            if query.is_halal_product(ingredients):
                print("The product is halal.")
            else:
                print("The product is not halal.")
        else:
            sg.popup("Error fetching product information.")


window.close()
