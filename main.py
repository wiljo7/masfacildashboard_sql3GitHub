import streamlit as st 
import sqlite3
import sqlite3
import pandas as pd
import datetime


c=open('configure.txt','r')
lc=c.readlines() 
info_dict={}
for x in lc:
    try:
        print(x)
        info=x.strip('\n').split(';')
        info_dict[info[0]]=info[1]
    except Exception as e: 
        print(e)

#st.write(info_dict)
bussines_name=info_dict['store_name']

try:
    st.set_option('browser.gatherUsageStats', False)
except Exception as e: 
    print(e)

cnx=info_dict['connection']

if cnx == 'l':
    st.write('local')
else:
    st.write('remote')
host = info_dict['host']
database = info_dict['database']
user = info_dict['user']
password = info_dict['password']

if 1==1:
    import subprocess

    # Instalar paquetes desde requirements.txt
    try:
        print(['pip', 'install', '-r', 'requirements.txt'])
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
    except Exception as e: 
        print('instalando requeriments',e)
else:
    pass 

try:
    import mysql.connector
except Exception as e: 
    print('error en importaciones mysql connector',e)
    #st.write(e)
try:
    import sqlalchemy
except Exception as e: 
    print('error en importaciones sqlalchemy',e)
    #st.write(e)
#import streamlit-menu-option as menu_option

# Declare the connection variable outside the try block
connection = None

table_names=[]



def conexion_():

    if cnx == 'l':
        conexion=sqlite3.connect('proyecto_profesional.db')
        cursor=conexion.cursor()
        return cursor,conexion
    else:
        connection = st.experimental_connection('connections.mysql', type='sql')
        cursor=''
        return cursor,connection

    



#connection = st.experimental_connection(**kwargs)#'mysql', type='sql')#, type='sql')

st.title(f'{bussines_name}')
con1=st.container()
con2=st.container()
con3=st.container()




cur,con=conexion_() 

def busqueda():

    article=con1.text_input('Qué Articulo deseas buscar ?')

    buscar_b=con1.button('Buscar')

    #cur,con=conexion_()
    if article != '' or article != '' and buscar_b == True: 
        
        
        if cnx=='l':
            cur.execute("select PRECIO,PRECIO_BAJO from DIVISA where fecha = 2")
            cursor=[x for x in cur]
        else:
            cursor=con.query("select PRECIO,PRECIO_BAJO from DIVISA where fecha = 2")
            columnas,cursor=convert_dataframeTotuples(cursor)

        for x in cursor:
            dollar=float(x[0])
            print('result cursor',x)

        if cnx=='l':
            cur.execute(f"select Producto,codigo,Inventario,Venta_USD from Products where Producto like '%{article}%'or codigo like '%{article}%'")
            cursor=[x for x in cur]
        else:
            cursor=con.query(f"select Producto,codigo,Inventario,Venta_USD from Products where Producto like '%{article}%'or codigo like '%{article}%'")
            columnas,cursor=convert_dataframeTotuples(cursor)
        
        data =[[x[0],x[1],x[2],x[3], round(float(dollar)*float(x[3]),2)] for x in cursor]
        
        dfbusqueda=pd.DataFrame(data)
        dfbusqueda.rename(columns={0:'Producto',1:'Codigo',2:'Inventario',3:'Precio $',4:'Precio BsF'},inplace=True)
        con2.dataframe(dfbusqueda)


def convert_dataframeTotuples(df):
    columnas = tuple(df.columns)

    # Convertir cada fila del DataFrame a una tupla
    datos = [tuple(x) for x in df.values]
    return columnas,datos 

def dashboard():
    
    ########
    option1=con1.selectbox('Seleccione el tipo de dashboard', ['Elegir','Producto','Cierre'], index=0) 
    
    if option1.lower() == 'producto':
        print('primera opcion')
        conexion=conexion_() 

        if cnx=='l':
            cur.execute('select Producto from Products')
            data_products=[str(x[0]) for x in cur]
        else:
            cursor=con.query('select Producto from Products')
            

        print('data',data_products.insert(0,''))
        con1.selectbox('Que producto desea analizar?',data_products)
    
    #analizar un producto 
        #kardex entradas y salidas 
        #promedio de ventas mensuales 
        #promedio de ventas semanales 
        #promedio de ventas diarios 
        #compra minima 
        #inventario
            #rotacion de inventario 
            
    #analizar ventas 
        #analizar un dia de ventas 
            #numero de ventas 
            #items vendidos 
            #ganancia del dia 
            #ingresos del dia 
            #costos del dia 
            #medios de pago 
            #cierre por cajero 
            #vendedor comision 
            #stock productos vendidos comparado con la cantidad de ventas del dia y su promedio diario de ventas 
                #decidir si el stock es bajo, peligro o sin problemas 
                #cuantos dias puedo sobrevivir haciendo un dia de ventas como hoy ?
            #ingresos promedio diario 
            #ganancia promedio diario 
                #comparar con el ingreso y la ganancia del dia esperada 
            #comparar ventas diarias 
            #horas con mas ventas del dia
                #comparar con el historico de ventas por hora 
                #comparar con el historio de ventas por hora del mes 
            #mejores clientes 
            #mayor compra del dia 
            #promedio de ingresos por compra del dia 
            #cantidad de dinero por hora ingresado 
            #cantidad de dinero por hora historio ingresado 
            #mejor horario de venta 
            #productos mas vendidos 
             
        #analizar un periodo de ventas
    elif option1.lower() == 'cierre':
        date1=con1.date_input("Fecha de consulta", datetime.datetime.now())

        if date1!= '':
            ldate1=str(date1).split(' ')
            ldate2=ldate1[0].split('-')
            print('calculando los ingresos')
            dia=int(ldate2[2]) 
            mes=int(ldate2[1])

            date_check=f'{dia}-{mes}-{ldate2[0]}'
            
            cur,con=conexion_() 

            if cnx=='l':
                cur.execute(f"select Vendedor,fecha,hora,referencia,ingresoUSD,VisualFac from ingresosfull where fecha = '{date_check}'")
                data_records=[x for x in cur]
            else:
                cursor=con.query(f"select Vendedor,fecha,hora,referencia,ingresoUSD,VisualFac from ingresosfull where fecha = '{date_check}'")
                columns,data_records=convert_dataframeTotuples(cursor)

            #f"select * from ingresosfull where fecha = '{date_check}'"
            
            #cursor
            if cnx=='l':
                dfbusqueda=pd.DataFrame(data_records)
                dfbusqueda.rename(columns={0:'Vendedor',1:'Fecha',2:'Hora',3:'Numero Factura',4:'Monto en $',5:'Copia de Factura'},inplace=True)
            
            else:
                dfbusqueda=cursor
                dfbusqueda.rename(columns={columns[0]:'Vendedor',columns[1]:'Fecha',columns[2]:'Hora',columns[3]:'Numero Factura',columns[4]:'Monto en $',columns[5]:'Copia de Factura'},inplace=True)
            
             
            sales_quantity=len(data_records)
            
            
            con2.subheader('Facturación del día')
            con2.dataframe(dfbusqueda)
            
            #### voy con los montos por medios de pago 
            print(f"select medio1,mmedio1,medio2,mmedio2,medio3,mmedio3,medio4,mmedio4,medio5,mmedio5,medio6,mmedio6,medio7,mmedio7,descuento from ingresosfull where fecha = '{date_check}'")
            
            if cnx=='l':
                cur.execute(f"select medio1,mmedio1,medio2,mmedio2,medio3,mmedio3,medio4,mmedio4,medio5,mmedio5,medio6,mmedio6,medio7,mmedio7,descuento from ingresosfull where fecha = '{date_check}'")
                data_records_paid=[x for x in cur]                
            else:
                cursor=con.query(f"select medio1,mmedio1,medio2,mmedio2,medio3,mmedio3,medio4,mmedio4,medio5,mmedio5,medio6,mmedio6,medio7,mmedio7,descuento from ingresosfull where fecha = '{date_check}'")
                columnsrecords,data_records_paid=convert_dataframeTotuples(cursor)
          
            
            medio_={}
            vueltoBs=0
            for x in data_records_paid:    
                 
                if x[0] not in medio_:
                    
                    medio_[x[0]] = float(x[1]) 
                    
                else:
                    medio_[x[0]]=medio_[x[0]]+float(x[1])
                #vuelto en dolares 
                if x[10] not in medio_:
                    medio_[x[10]] = float(x[11]) 
                
                else:
                    medio_[x[10]]=medio_[x[10]]+float(x[11])

                # bs in 1 
                if x[2] not in medio_:
                    medio_[x[2]] = float(x[3]) 
                
                else:
                    medio_[x[2]]=medio_[x[2]]+float(x[3])
                
                #bs in 2
                if x[4] not in medio_:
                    medio_[x[4]] = float(x[5]) 
                
                else:
                    medio_[x[4]]=medio_[x[4]]+float(x[5])

                # bs in 3 
                if x[6] not in medio_:
                    medio_[x[6]] = float(x[7]) 
                
                else:
                    medio_[x[6]]=medio_[x[6]]+float(x[7])

                #bs in 4 
                if x[8] not in medio_:
                    medio_[x[8]] = float(x[9]) 
                
                else:
                    medio_[x[8]]=medio_[x[8]]+float(x[9])

                # bs out 
                if x[12] not in medio_:
                    medio_[x[12]] = -float(x[13]) 
                
                else:
                    medio_[x[12]]=medio_[x[12]]-float(x[13])


                # bs descuento 
                if 'DESCUENTOS BS' not in medio_:
                    medio_['DESCUENTOS BS'] = float(x[14]) 
                
                else:
                    medio_['DESCUENTOS BS']=medio_['DESCUENTOS BS']+float(x[14])





                
            #### ahora poner los medios que no son cero 
            pagos_list=[]
            medios_list=[]
            for k,v in medio_.items():
                if float(v) != float(0):
                    monto_=round(float(v),2)
                    pagos_list.append(monto_)
                    medios_list.append(k)
                else:
                    pass             
            


            dfpagos=pd.DataFrame(data_records_paid)
            #con2.dataframe(dfpagos)

            dfpagos.rename(columns={0:'medio1',1:'mmedio1',2:'medio2',3:'mmedio2',4:'medio3',5:'mmedio3',6:'medio4',7:'mmedio4',8:'medio5',9:'mmedio5',10:'medio6',11:'mmedio6',12:'medio7',13:'mmedio7',12:'descuento'},inplace=True)
            
            
            
            try:
                pagoUSD=dfpagos['mmedio1'].sum()
                vueltoUSD=dfpagos['mmedio6'].sum() 

                pagobs1=dfpagos['mmedio2'].sum()
                pagobs2=dfpagos['mmedio3'].sum()
                pagobs3=dfpagos['mmedio4'].sum()
                pagobs4=dfpagos['mmedio5'].sum()
                pagobs5vuelto=dfpagos['mmedio7'].sum()
                
                descuentobs=dfpagos['descuento'].sum()


                montoUSD=round(pagoUSD-vueltoUSD,2)
                montoBS=round(pagobs1+pagobs2+pagobs3+pagobs4-pagobs5vuelto,2)

            except Exception as e: 
                print(e)


            
            ### show info 
            
            dfmedios=pd.DataFrame(pagos_list,index=medios_list,columns=['MEDIOS DE PAGO'])
            

            con2.markdown("""---""")
            
            
            con2.subheader('Relación de ingresos por Medios de Pago')            
            
            c01,c02=con2.columns(2)

            
            c01.bar_chart(dfmedios['MEDIOS DE PAGO'].round(2))
            
            n=0
            list_medios2=[]
            for x in pagos_list:
                list_medios2.append([medios_list[n],x])
                n+=1


            dfmedios2=pd.DataFrame(list_medios2,columns=['MEDIOS DE PAGO','MONTOS'])

            #dfmedios2
            con2.markdown("""---""")

            c02.dataframe(dfmedios2)
            def rounds(valor):
                return round(valor,2)
            try:
                c1,c2,c3,c4=con2.columns(4)
                c1.metric(label="Ventas del día", value=sales_quantity, delta=sales_quantity,delta_color="off")
                c2.metric(label="Monto total $", value=rounds(dfbusqueda['Monto en $'].sum()), delta=rounds(dfbusqueda['Monto en $'].sum()),delta_color="off")
                c3.metric(label="Pagos en $", value=rounds(montoUSD), delta=rounds(montoUSD),delta_color="off")
                c4.metric(label="Pagos en Bs", value=rounds(montoBS), delta=rounds(montoBS),delta_color="off")
                
            except Exception as e: 
                print(e)

            con2.markdown("""---""")
           
            #con2.subheader('Ventas del día')            
            

            #con2.dataframe(dfbusqueda)
            

            # detalleIngreso 
            if cnx=='l':
                cur.execute(f"select Productos,CANTIDAD from detalleIngreso where FECHA = '{date_check}'")
                cursor=[x for x in cur]
            else:
                cursor=con.query(f"select Productos,CANTIDAD from detalleIngreso where FECHA = '{date_check}'")
                columnas,cursor=convert_dataframeTotuples(cursor)
            
            dict_details={}
            list_Gproducts=[]
            for x in cursor:
                if ',' in x[0]:
                    # varios productos 
                    list_products=x[0].split(',')
                    list_quantity=x[1].split(',')
                    n=0
                    for product in list_products:
                        if product not in list_Gproducts:
                            list_Gproducts.append(product)
                            dict_details[product]=float(list_quantity[n])
                            n+=1
                        else:
                            dict_details[product]=dict_details[product]+float(list_quantity[n])
                            n+=1
                    
                else:
                    if x[0] not in list_Gproducts:
                        list_Gproducts.append(x[0])
                        dict_details[x[0]]=float(x[1])
                    else:
                        dict_details[x[0]]=dict_details[x[0]]+float(x[1])
            
            
            # como pasar diccionario a dataframe 
            list_keys=[]
            list_products_sell=[]
            for k,v in dict_details.items():
                list_keys.append([k,v])
                list_products_sell.append(k)
            #setence sql 
            #print(list_keys)
            
            sentence="('"+"','".join(list_products_sell)+"')"
            
            if cnx=='l':
                cur.execute(f"select Producto,Inventario from Products where Producto in {sentence}")
                cursor=[x for x in cur]
            else:
                cursor=con.query(f"select Producto,Inventario from Products where Producto in {sentence}")
                columnas,cursor=convert_dataframeTotuples(cursor)
            
            dict_inventory={}
            for x in cursor:
                dict_inventory[x[0]]=float(x[1])
            list_keys2=[]
            for x in list_keys:
                x.append(dict_inventory[x[0]])
                try:
                    relation_porcent=str(round(float(float(x[1])/dict_inventory[x[0]])*100,2))+'%'
                except Exception as e: 
                    relation_porcent="100%"
                x.append(relation_porcent)
                x.append(round(100/float(relation_porcent.replace('%',''))))
                list_keys2.append(x)

            df4=pd.DataFrame(data=list_keys,columns=['Item vendido','Cantidad','Stock','% Vendido','Dias Operativos'])
            

            
            con2.subheader('Items Vendidos')            
            
            con2.dataframe(df4)

            #con2.write(dict_details)
            # datos de hotel 
            sentence="('H01','H02','H03','H04','H05','H06','H07','H08','H09','H10','H11','H12','H13','H14','H15','H16','H17','H18','H19','H20','H21','H22','H23','H24','H25')"
            
            if cnx == 'l':
                cur.execute(f"select Codigo from Products where Codigo in {sentence}")
                cursor=[x for x in cur]
            else:
                cursor=con.query(f"select Codigo from Products where Codigo in {sentence}")
                columnas,cursor=convert_dataframeTotuples(cursor)

            list_hab=[]
            for x in cursor:
                if x[0] not in list_hab:
                    list_hab.append(x[0])
            list_hab.sort() 
            
            ##### ahora voy a chequear el estatus de las habitaciones 
            
            #'OCUPADA','LIMPIEZA','MANTENIMIENTO'
            if cnx =='l':
                cur.execute("select codigo_habitacion,estado from estado_habitacion where estado in ('LIMPIEZA','OCUPADA','MANTENIMIENTO')")
                cursor=[x for x in cur]
            else:
                cursor=con.query("select codigo_habitacion,estado from estado_habitacion where estado in ('LIMPIEZA','OCUPADA','MANTENIMIENTO')")
                columnas,cursor=convert_dataframeTotuples(cursor)

            room_for_clean=[]
            room_for_repair=[]
            room_ocuppied=[]
            for x in cursor: 
                if x[0] not in room_for_clean and x[1] == 'LIMPIEZA':
                    room_for_clean.append(x[0])
                elif x[0] not in room_for_repair and x[1] == 'MANTENIMIENTO':
                    room_for_repair.append(x[0])
                elif x[0] not in room_ocuppied and x[1] == 'OCUPADA':
                    room_ocuppied.append(x[0])

                
            con2.markdown("""---""")
            
            con2.subheader('Disponibilidad de Habitaciones')            
            

            ch1,ch2,ch3,ch4,ch5=con2.columns(5)
            list_position=[ch1,ch2,ch3,ch4,ch5]
            n=0
            for x in list_hab:
                if x in room_for_clean:
                    
                    list_position[n].button(f"{x} :soap: LIMPIEZA")
                    n+=1
                elif x in room_for_repair:
                    list_position[n].button(f"{x} :x: MANTENIMIENTO")
                    n+=1
                elif x in room_ocuppied:
                    list_position[n].button(f"{x} :dollar: OCUPADA")
                    n+=1
                else:
                    list_position[n].button(f"{x} :bed: DISPONIBLE")
                    n+=1

                if n == 5:
                    
                    n=0
                else:
                    pass 
            
            
            con2.markdown("""---""")
            cm1,cm2,cm3,cm4=con2.columns(4)

            room_avalible=len(list_hab)-len(room_for_clean)-len(room_for_repair)-len(room_ocuppied)
            cm1.metric(label="Disponibles", value=room_avalible, delta=str(rounds(room_avalible/len(list_hab)*100))+'%',delta_color="off")
            
            cm2.metric(label="Ocupadas", value=len(room_ocuppied), delta=str(rounds(len(room_ocuppied)/len(list_hab)*100))+'%',delta_color="off")
            
            cm3.metric(label="Por Limpiar", value=len(room_for_clean), delta=str(rounds(len(room_for_clean)/len(list_hab)*100))+'%',delta_color="off")
            
            cm4.metric(label="Mantenimiento", value=len(room_for_repair), delta=str(rounds(len(room_for_repair)/len(list_hab)*100))+'%',delta_color="off")
# 1. as sidebar menu
with st.sidebar:
    #selected = option_menu("Menu Principal", ["Busqueda", 'Dashboard'], 
    #    icons=['house', 'gear'], menu_icon="cast", default_index=0)
    #####
    st.title('+Fácil Dashboard')
    selected = st.selectbox(
        'Que Deseas hacer ?',  
        ('Busqueda', 'Dashboard'))
    
    
    #,
       # styles={
        #"container": {"padding": "0!important", "background-color": "#fafafa"},
        #"icon": {"color": "orange", "font-size": "25px"}, 
        #"nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        #"nav-link-selected": {"background-color": "green"},
    #})
    
    if selected == 'Busqueda':
        busqueda()
    elif selected == 'Dashboard':
        user_password=st.text_input('Clave de acceso',type="password")
        
        if user_password.lower() == 'almacenesx':
            dashboard()





