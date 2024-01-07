import PySimpleGUI as sg
import query
import scan


sg.theme("Material1")

font = ("Helvetica", 16)
sg.set_options(font=font)

recents_headings = ["Product Name", "UPC", "Classification"]
recents_rows = [[]]

layout = [[sg.Titlebar("Byte of 87")], [sg.Text("Welcome to Halal Scanner.")], [sg.Text("Recent Searches")],
          [sg.Table(values=recents_rows, headings=recents_headings, key="-RECENTS-",
                    auto_size_columns=False, col_widths=[30, 15, 30], justification="center")],
          [sg.Button("Scan a Barcode")], [sg.Text("Enter a UPC to search:")],
          [sg.InputText(key="-QUERY-"), sg.Button("Search")]]


def show_halal_result(upc):
    print('You entered', upc)
    info = query.get_product_info(upc)
    if info:
        product_name = info['product']['product_name']
        ingredients = info['product']['ingredients_text']
        print(f"Product Name: {product_name}")
        print(f"Ingredients: {ingredients}")
        halal_result = query.is_halal_product(ingredients)
        if halal_result[0]:
            sg.popup(f"The product is halal.")
        else:
            sg.popup(f"The product is not halal. ({halal_result[1]})")
        recents_rows.append([product_name, upc, "Halal" if halal_result[0] else "Haram"])
        window['-RECENTS-'].update(values=recents_rows)
    else:
        sg.popup("Error fetching product information.")

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break
    if event == "Scan a Barcode":
        print("Scanning a barcode...")
        query_upc = scan.capture_image()
        if query_upc:
            show_halal_result(query_upc)
        else:
            sg.popup("Error fetching product information.")
    if event == "Search":
        query_upc = values["-QUERY-"]
        try:
            int(query_upc)
        except ValueError:
            sg.popup("Please enter a valid UPC.")
        show_halal_result(query_upc)


window.close()
