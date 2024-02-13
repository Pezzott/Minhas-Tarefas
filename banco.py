import pyodbc


server = 'gen-lang-client-0863987467:us-central1:pezzott-2024'
database = 'pezzott-2024' 
username = 'pezzott@'
password = 'Catharina@14253698'


conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password


conn = pyodbc.connect(conn_str)


cursor = conn.cursor()
cursor.execute("SELECT * FROM sua_tabela")  
resultados = cursor.fetchall()
for resultado in resultados:
    print(resultado)


conn.close()
