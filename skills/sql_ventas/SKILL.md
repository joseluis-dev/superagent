---
name: sql_ventas
description: Usa este skill para generar consultas SQL sobre una base de datos de productos, clientes, pedidos y detalle de pedidos.
---

# sql_ventas

## Cuándo usar este skill

Usa este skill cuando el usuario pida generar, corregir o explicar SQL para consultar ventas, clientes, productos o pedidos.

## Reglas generales

- Genera SQL claro
- Usa aliases cortos
- No inventes tablas ni columnas fuera del esquema proporcionado
- Si falta informacion para escribir la consulta, pregunta al usuario.
- Las consultas deben ser compatibles con PostgreSQL.
- Incluye una explicacion breve despues de la consulta.

## Esquema de base de datos

### Tabla: clientes

Guarda informacion de los clientes (empresas o personas)

Columnas:

- id: entero, llave primaria.
- nombre: texto, nombre del cliente.
- email: texto, correo del cliente.
- ciudad: texto, ciudad del cliente.
- fecha_registro: fecha, día en que se registró el cliente.

### Tabla: productos

Almacena los productos disponibles

Columnas:

- id: entero, llave primaria.
- nombre: texto, nombre del producto.
- categoria: texto, categoría del producto.
- precio: numérico, precio actual del producto.
- activo: booleano, indica si el producto sigue disponible.

### Tabla: pedidos

Guarda cada compra realizada por un cliente.

Columnas:

- id: entero, llave primaria.
- cliente_id: entero, llave foránea hacia clientes.id.
- fecha_pedido: fecha, día de la compra.
- estado: texto, estado del pedido. Posibles valores: pendiente, pagado, enviado, cancelado.

Relaciones:

- pedidos.cliente_id se relaciona con clientes.id.

### Tabla: pedido_detalles

Guarda los productos incluidos en cada pedido.

Columnas:

- id: entero, llave primaria.
- pedido_id: entero, llave foránea hacia pedidos.id.
- producto_id: entero, llave foránea hacia productos.id.
- cantidad: entero, unidades compradas.
- precio_unitario: numérico, precio usado en ese pedido.

Relaciones:

- pedido_detalles.pedido_id se relaciona con pedidos.id.
- pedido_detalles.producto_id se relaciona con productos.id.

## Relaciones principales

- Un cliente puede tener muchos pedidos.
- Un pedido pertenece a un cliente.
- Un pedido puede tener muchos productos por medio de pedido_detalles.
- Un producto puede aparecer en muchos pedido_detalles.

## Ejemplos de consultas

Ventas totales por cliente:

```sql
SELECT
    c.nombre AS cliente,
    SUM(pd.cantidad * pd.precio_unitario) AS total_comprado
FROM clientes c
JOIN pedidos p ON p.cliente_id = c.id
JOIN pedido_detalles pd ON pd.pedido_id = p.id
WHERE p.estado = 'pagado'
GROUP BY c.id, c.nombre
ORDER BY total_comprado DESC;
```

Productos mas vendidos:

```sql
SELECT
    pr.nombre AS producto,
    SUM(pd.cantidad) AS unidades_vendidas
FROM productos pr
JOIN pedido_detalles pd ON pd.producto_id = pr.id
JOIN pedidos p ON p.id = pd.pedido_id
WHERE p.estado = 'pagado'
GROUP BY pr.id, pr.nombre
ORDER BY unidades_vendidas DESC;
```

## Formato de respuesta

Consulta SQL:

Explicacion breve:
