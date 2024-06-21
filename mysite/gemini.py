import google.generativeai as genai

GOOGLE_API_KEY= "AIzaSyA1emOJVFRJBMI4sHbrKGb_M_olZNMObQk"
genai.configure(api_key=GOOGLE_API_KEY)


model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(
"""Given the problem context along with the table attributes, please generate a table populated with dummy data for the problem:
 Problem context- A store wants to keep track and keep up-to-date on its stock when someone takes buys
 something from the store or if something gets restocked. They want to use triggers with constraints in their
 database that will keep track of stock, as well as stop invalid data from being entered. 
 Table 1 attributes: item_id (number primary key), item_name (varchar2(50)), item_description (varchar2(100)),
   item_price (number), item_seasonal (varchar2(1)). Table 2 attributes: 
   item_id (number references items(item_id)), item_quantity (number), area_code (number), 
   phone (varchar2(12)), location (varchar2(50)). 
   We don’t need any accompanying description or clarification or Sure…. line, just the tables with 
   10 elements.  
 """
)
response = response.text.replace('•', '  *')

a = response.split("## Table")
for i in a:
    lines = i.strip().split("\n")
    columns = [col.strip() for col in lines[0].strip('|').split('|')]
    rows = []
    for line in lines[2:]:
        values = [val.strip() for val in line.strip('|').split('|')]
        row_dict = dict(zip(columns, values))
        # Convert numeric values to appropriate types
        for key in row_dict:
            if row_dict[key].isdigit():
                row_dict[key] = int(row_dict[key])
            else:
                try:
                    row_dict[key] = float(row_dict[key])
                except ValueError:
                    pass
        rows.append(row_dict)
    print(columns)
    print(rows)

