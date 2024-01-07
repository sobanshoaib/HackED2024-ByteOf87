import pickle

import PySimpleGUI as sg

import query
import scan


sg.theme("DarkBlue14")

font = ("Helvetica", 16)
sg.set_options(font=font)

recents_headings = ["Product Name", "UPC #", "Classification"]

try:
    with open('recents.pkl', 'rb') as f:
        recents_rows = pickle.load(f)
except FileNotFoundError:
    recents_rows = [[]]

layout = [[sg.Titlebar("Byte of 87")], [sg.Text("Welcome to Halal Scanner.")],
          [sg.Text("Recent Searches"), sg.Button("Clear")],
          [sg.Table(values=recents_rows, headings=recents_headings, key="-RECENTS-",
                    auto_size_columns=False, col_widths=[30, 15, 50], justification="center")],
          [sg.Button("Scan a Barcode")], [sg.Text("Enter a UPC to search:")],
          [sg.InputText(key="-QUERY-"), sg.Button("Search")]]


def show_result(upc):
    print('You entered', upc)
    info = query.get_product_info(upc)
    if info:
        product_name = info['product']['product_name']
        ingredients = info['product']['ingredients_text']
        print(f"Product Name: {product_name}")
        print(f"Ingredients: {ingredients}")

        halal_result = query.is_halal_product(ingredients)

        vegan, vegetarian = query.is_vegan(info), query.is_vegetarian(info)

        # Classification of whether it is halal, vegan, and vegetarian
        separator = "\n\n\t"
        classification = "\t"
        if halal_result[0]:
            classification += "✅ Halal"
        else:
            classification += f"❌ Not Halal ({halal_result[1]})"
        classification += separator

        if vegan[0] == 0:
            classification += f"❌ Not Vegan ({vegan[1]})"
        elif vegan[0] == 1:
            classification += "✅ Vegan"
        elif vegan[0] == 2:
            classification += f"⚠️ Maybe Vegan ({vegan[1]})"
        else:
            classification += f"❓ Vegan Unknown"
        classification += separator

        if vegetarian[0] == 0:
            classification += f"❌ Not Vegetarian ({vegetarian[1]})"
        elif vegetarian[0] == 1:
            classification += "✅ Vegetarian"
        elif vegetarian[0] == 2:
            classification += f"⚠️ Maybe Vegetarian ({vegetarian[1]})"
        else:
            classification += f"❓ Vegetarian Unknown"

        sg.popup(f"Product Name: {product_name}\n\nIngredients: {ingredients.lower()}\n\nClassification:\n\n{classification}\n")

        # Add the search to the recent searches table
        recents_rows.append([product_name, upc, classification.replace("\n", ", ").replace("\t", "")])

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
        if query_upc and query_upc != 'Cancelled':
            confirmation = sg.popup_yes_no(f"Is the scanned UPC code correct?\n\nScanned UPC: {query_upc}",
                                           title="Confirmation")
            if confirmation == 'Yes':
                print(f"User confirmed UPC code: {confirmation}")
                show_result(query_upc)
            else:
                print("User canceled or closed the confirmation popup")
                continue
        elif query_upc == 'Cancelled':
            print("User canceled or closed the barcode scanner")
            continue
        else:
            sg.popup("Error fetching product information.")
    if event == "Search":
        query_upc = values["-QUERY-"]
        try:
            int(query_upc)
        except ValueError:
            sg.popup("Please enter a valid UPC.")
        show_result(query_upc)
    if event == "Clear":
        recents_rows = [[]]
        window['-RECENTS-'].update(values=recents_rows)


with open('recents.pkl', 'wb') as f:
    pickle.dump(recents_rows, f)

window.close()
