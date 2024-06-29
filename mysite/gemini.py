import google.generativeai as genai


GOOGLE_API_KEY= ""
with open("API_key.txt", "r") as f:
    GOOGLE_API_KEY = f.read().strip()
genai.configure(api_key=GOOGLE_API_KEY)

def generate_table_content(problem_context, table_info):
    model = genai.GenerativeModel('gemini-1.5-flash')
    table_data = ""
    for key in table_info.keys():
        st = f"Table {key} attributes: "
        lis = table_info[key]
        for li in lis:
            name = list(li.keys())[0]
            st += name + " (" + str(li[name]) + "), "
        table_data += st
    s = f"""Given the problem context along with the table attributes, please generate a table populated with dummy data for the problem:
    Problem context- {problem_context}. 
    {table_data}.
    We don’t need any accompanying description or clarification or Sure…. line, just the tables with 
    10 elements. """

    """response = model.generate_content(
    Given the problem context along with the table attributes, please generate a table populated with dummy data for the problem:
    Problem context- A store wants to keep track and keep up-to-date on its stock when someone takes buys
    something from the store or if something gets restocked. They want to use triggers with constraints in their
    database that will keep track of stock, as well as stop invalid data from being entered. 
    Table 1 attributes: item_id (number primary key), item_name (varchar2(50)), item_description (varchar2(100)),
    item_price (number), item_seasonal (varchar2(1)). Table 2 attributes: 
    item_id (number references items(item_id)), item_quantity (number), area_code (number), 
    phone (varchar2(12)), location (varchar2(50)). 
    We don’t need any accompanying description or clarification or Sure…. line, just the tables with 
    10 elements.  
    
    )"""

    response = model.generate_content(s)
    response = response.text.replace('•', '  *')
    response = response.replace('-','')
    a = response.split("##")
    dic = {}
    for i in range(1, len(a)):
        x = a[i]
        y = a[i].split('\n')
        z = y[2].split('|')
        dic[y[0]] = []
        for j in range(1, len(z)-1):
            temp = {}
            temp[z[j].strip()] = []
            dic[y[0]].append(temp)
        l = len(dic[y[0]])
        for j in range(4, len(y)-1):
            b = y[j]
            if b != '':
                c = b.split('|')
                d = 0
                for k in range (1, len(c)-1):
                    e = dic[y[0]]
                    f = e[d]
                    d += 1
                    g = list(f.keys())[0]
                    f[g].append(c[k].strip())
        
    return(dic)
