from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from datetime import date
from selenium.webdriver.support.ui import Select
import time
import os
from faker import Faker
from selenium.common.exceptions import TimeoutException


# Función para dar de alta un nuevo pedido
def test_altapedido(driver):
    driver.get("https://test.admanagerembarques.adventa.solutions/")

    # Se ubica el elmento de usuario
    campo_username = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "login")))
    
    # Se ubica el elemento password
    campo_password = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "password")))
    
    # Se ubica el botón de entrar
    boton_login = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "loginbtn")))

    # Se ingresa el usuario
    campo_username.send_keys("support@tepachesoft.com")
    
    # Se ingresa la contraseña
    campo_password.send_keys("secretos")
    
    # Se da clic en el boton para acceder
    boton_login.click()

    # Se ubica el elemento para validar que se haya logeado correctamente
    usuario_logeado = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "pr")))
    
    # Validamos que la varibale usuario_logeado contenga la clase pr
    assert "pr" in usuario_logeado.get_attribute("class")

    # Entramos al menu de pedidos
    pedidos_mispedidos = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "fa-file-text-o")))
    pedidos_mispedidos.click()
    
    # Clic en nuevo pedido
    pedidos_nuevopedido = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "newEmbarque")))
    pedidos_nuevopedido.click()

    # Ingresamos el numero de pedido SAP
    pedidos_numeroSAP = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "purse_pedido_sap")))
    numero_pedidoSap = random.randint(1000000, 9999999)
    pedidos_numeroSAP.send_keys(numero_pedidoSap)
    
    # Ingresamos el numero de Adpro
    pedidos_numeroAdpro = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "purse_num_pedido_adpro")))
    numero_pedidoSap = random.randint(1000, 9999)
    pedidos_numeroAdpro.send_keys(numero_pedidoSap)

    # Ingresamos la fecha de entrega pedido SAP
    pedidos_fechaEntrega = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "purse_fecha_entrega_cliente")))
    fecha_hoy = date.today().strftime("%d/%b/%Y")
    driver.execute_script("arguments[0].value = arguments[1];",pedidos_fechaEntrega, fecha_hoy)
   
    # Seleccionamos la linea de negocio
    valor_deseado = random.choice([1, 2, 3, 4, 6, 7])
    radio_id = f"purse_bussiness_line_id_{valor_deseado}"
    print("Línea de negocio seleccionada:", radio_id)
    pedidos_lineaNegocio = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, radio_id)))
    driver.execute_script("arguments[0].click();", pedidos_lineaNegocio)
    
    # Seleccionamos el programa
    programas = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "purse[programa_id]")))

    # Creamos el objeto para guardar los programas
    arreglo = Select(programas)

    # Obtenemos las opciones
    opciones = arreglo.options
    
    # Creamos un for para recorrer el arreglo e imprimirlo en la consola
    #for opcion in opciones:
    #print("texto:", opcion.text, " | Valor:", opcion.get_attribute("value"))

    # Creamos un arreglo para guardar las opciones que no estén vacias, para evitar futuros errores
    opciones_validas = []

    # Creamos un for para recorrer el arreglo y validar si el campo value es diferente de 0 lo añada al arreglo nuevo 
    for op in opciones:
        if op.get_attribute("value") != "":
            opciones_validas.append(op)
    
    # Seleccionamos un valor random
    pedidos_nombrePrograma = random.choice(opciones_validas)
    print("Nombre programa:", pedidos_nombrePrograma.text, "| Valor programa:", pedidos_nombrePrograma.get_attribute("value"))

    # Damos clic en el nombre del programa
    arreglo.select_by_value(pedidos_nombrePrograma.get_attribute("value"))
    
    # Ingresamos la cantidad de piezas
    pedidos_cantidadPiezas = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "purse_cantidad")))
    cantidadPiezas = random.randint(1, 200)
    pedidos_cantidadPiezas.send_keys(cantidadPiezas)

    # Ingresamos la oficina
    oficina = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "purse_branch_office_id")))

    # Creamos el objeto para guardar las oficinas disponibles
    oficinas = Select(oficina)

    # Obtenemos las opciones del select
    nombre_oficina = oficinas.options

    # Creamos un arreglo para guardar las oficinas que no estén vacias
    oficinas_validas = []
    for opcion_oficina in nombre_oficina:
        if opcion_oficina.get_attribute("value") != "":
            oficinas_validas.append(opcion_oficina)

    # Seleccionamos un valor random
    pedidos_nombreOficina = random.choice(oficinas_validas)

    # Ingresamos en el select el nombre de la oficina
    oficinas.select_by_value(pedidos_nombreOficina.get_attribute("value"))
    
    # Damos clic en el nombre del cliente
    cliente = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "purse_cliente_id")))

    # Creamos el objeto para guardar la lista de clientes
    clientes = Select(cliente)

    # Obtenemos la lista de los clientes
    nombres_clientes = clientes.options

    # Creamos un arreglo para guardar las oficinas que no estén vacias
    nombres_clientes_vacios = []
    for opcion_cliente in nombres_clientes:
        if opcion_cliente.get_attribute("value") != "":
            nombres_clientes_vacios.append(opcion_cliente)
    
    # Seleccionamos un valor random
    pedidos_nombreCliente = random.choice(nombres_clientes_vacios)

    # Ingresamos en el select el nombre del cliente
    #print("nombre del cliente:", pedidos_nombreCliente.get_attribute("text"), " | valor: ", pedidos_nombreCliente.get_attribute("value"))
    clientes.select_by_value(pedidos_nombreCliente.get_attribute("value"))
    
    # Damos clic en el botón agregar
    pedidos_btnAgregar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "save-emb")))
    pedidos_btnAgregar.click()
    
    while True:
        # Obtenemos el mensaje de pedido agregado
        mensaje_pedido = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".showSweetAlert h2"))).text
        print("mensaje pedido= ", mensaje_pedido)
        if "Agregado!" in mensaje_pedido:
            #Cerramos el alert para proceder a llenar las partidas del pedido
            pedidos_btnAceptar = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "confirm")))
            time.sleep(3)
            pedidos_btnAceptar.click()
            print("pedido añadido")
            break
        elif "Ya existe un Proyecto con el mismo # Pedido SAP." in mensaje_pedido:
            btncancelar_pedidoSap = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "cancel")))
            time.sleep(3)
            btncancelar_pedidoSap.click()
            numero_pedidoSap = random.randint(1000000, 9999999)
            pedidos_numeroSAP.clear()
            pedidos_numeroSAP.send_keys(numero_pedidoSap)
            pedidos_btnAgregar.click()
        elif "Ya existe un Proyecto con el mismo # Pedido AdPro." in mensaje_pedido:
            btncancelar_pedidoSap = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "cancel")))
            time.sleep(3)
            btncancelar_pedidoSap.click()
            numero_pedidoSap = random.randint(1000, 9999)
            pedidos_numeroAdpro.clear()
            pedidos_numeroAdpro.send_keys(numero_pedidoSap)
            pedidos_btnAgregar.click()

    # Ingresamos el ID de canje unico
    pedidos_IdCanje = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ticket_uniq_id")))
    idcanje = random.randint(1000, 9999)
    pedidos_IdCanje.send_keys(idcanje)

    # Ingresamos el # de articulo SAP
    pedidos_IdSap = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ticket_num_articulo_sap")))
    idsap = random.randint(1000, 9999)
    pedidos_IdSap.send_keys(idsap)

    # Ingresamos el nombre del participante
    pedidos_nombreParticipante = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "participante_ws")))
    fake = Faker('es_MX')  # Para nombres en español de México
    nombre_completo = fake.name()
    pedidos_nombreParticipante.send_keys(nombre_completo)

    # Ingresamos el numero de codigo CU
    pedidos_CodigoCU = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "codigo_cu")))
    codigocu = random.randint(1000, 9999)
    pedidos_CodigoCU.send_keys(codigocu)

    # Ingresamos el correo electronico
    pedidos_correo = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "email")))
    correo = fake.email()
    pedidos_correo.send_keys(correo)

    # Ingresamos la fecha de entrega pedido adpro
    pedidos_fechaEntregaAdpro = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "fecha_entrega_adpro")))
    driver.execute_script("arguments[0].value = arguments[1];",pedidos_fechaEntregaAdpro, fecha_hoy)

    # Ingresamos la fecha de canje Adbox
    pedidos_fechaCanjeAdbox = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "fecha_canje_adbox")))
    driver.execute_script("arguments[0].value = arguments[1];",pedidos_fechaCanjeAdbox, fecha_hoy)

    # Ingresamos el codigo PMR
    pedidos_codigoPMR = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "codigo_pmr")))
    codigoPMR = random.randint(1000, 9000)
    pedidos_codigoPMR.send_keys(codigoPMR)

    # Ingresamos la descripción
    pedidos_descripción = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "descripcion")))
    descripcion = fake.sentence(nb_words=10)
    pedidos_descripción.send_keys(descripcion)
    
    # Ingresamos la dirección
    pedidos_direccion = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "calle")))
    calle = fake.street_name()
    pedidos_direccion.send_keys(calle)

    # Ingresamos el numero
    pedidos_numero = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "noexterior")))
    numero = fake.building_number()
    pedidos_numero.send_keys(numero)

    # Ingresamos la referencia
    pedidos_referencia = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "between_streets")))
    colonia = fake.secondary_address()
    pedidos_referencia.send_keys(colonia)

    # Ingresamos el numero telefonico
    pedidos_telefono = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "phone")))
    telefono = fake.msisdn()[:10]
    pedidos_telefono.send_keys(telefono)

    # Ingresamos el codigo postal
    pedidos_codigoPostal = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "codigopostal")))
    fake = Faker('es_MX')
    cp = fake.postcode()
    pedidos_codigoPostal.send_keys(cp)
    print("codigo postal: ", cp)

    # Buscamos el CP para obtener estado y municipio
    while True:
        pedidos_btnBuscarCP = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "search-zip")))
        pedidos_btnBuscarCP.click()
        time.sleep(2)
        try:
            pedidos_codigoPostalError = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, "swal-button--confirm")))
            pedidos_codigoPostalError.click()
            print("entra al try")
            cp = fake.postcode()
            pedidos_codigoPostal.clear()
            pedidos_codigoPostal.send_keys(cp)
           
        except TimeoutException:
            print("entro al catchs")
            # Vuelve a localizar todos los elementos después del click
            pedidos_estado = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "estado_id")))
            pedidos_municipio = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "municipio_id")))
            pedidos_colonia = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "colonia_id")))
        
            # Crear el select de colonias actualizado
            colonias = Select(pedidos_colonia)

            # Creamos el objeto para guardar las colonias correctas
            opciones_validas = []

            # Validamos que no tenga opciones vacias
            for op in colonias.options:
                if op.get_attribute("value") != "":
                    opciones_validas.append(op)

            # Validamos que el estado y municipio esten correctos de acuerdo al CP
            if (
                pedidos_estado.text.strip() != ""
                and pedidos_municipio.text.strip() != ""
                and len(opciones_validas) > 0
            ):
                coloniaSeleccionada = random.choice(opciones_validas)
                print("colonia seleccionada: ", coloniaSeleccionada.text)
                colonias.select_by_value(coloniaSeleccionada.get_attribute("value"))
                break
    
    # Ingresamos precio venta producto
    pedidos_precioVentaProducto = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "precioVentaProducto")))
    precioventa = random.randint(10, 1000)
    pedidos_precioVentaProducto.send_keys(precioventa)

    # Ingresamos precio venta logistico
    pedidos_precioVentaLogistico = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "precioVentaLogistico")))
    precioventalogistico = random.randint(10, 1000)
    pedidos_precioVentaLogistico.send_keys(precioventalogistico)

    # Ingresamos fee
    pedidos_fee = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "precioVentaFe")))
    precioventafe= random.randint(10, 1000)
    pedidos_fee.send_keys(precioventafe)

    # Ingresamos costo logistico
    pedidos_costoLogistico = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "costoLogisticaEsperado")))
    preciocostologistico= random.randint(10, 1000)
    pedidos_costoLogistico.send_keys(preciocostologistico)

    # Damos clic en agregar
    pedidos_agregarPedido = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "s_pedido")))
    pedidos_agregarPedido.click()
    
    # Aceptamos el nuevo registro
    pedidos_agregarRegistro = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'btn-success')and contains(text(),'Aceptar')]")))
    time.sleep(2)
    pedidos_agregarRegistro.click()

    # Cerramos notificacion de registro añadido
    pedidos_mensajePedidoAñadido = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "swal-text")))
    assert pedidos_mensajePedidoAñadido.text.strip() == "El registro se agrego correctamente"
    pedidos_btnOk = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@class,'swal-button--confirm')and contains(text(),'OK')]")))
    time.sleep(2)
    pedidos_btnOk.click()
    WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.CLASS_NAME, "swal-text")))
    print("prueba finalizada")
    input("Presione enter para finalizar")