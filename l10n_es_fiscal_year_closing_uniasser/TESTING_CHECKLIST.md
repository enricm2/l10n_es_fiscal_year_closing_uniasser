# Testing Checklist - l10n_es_fiscal_year_closing

## Pre-requisitos

- [ ] Odoo 18.0 instalado
- [ ] Base de datos de prueba creada
- [ ] Localización española instalada (l10n_es)
- [ ] Plan contable español configurado
- [ ] Cuenta 129 existe en el plan contable

## Tests de Instalación

### Test 1: Instalación del módulo
- [ ] El módulo aparece en la lista de aplicaciones
- [ ] Se instala sin errores
- [ ] Se crean los diarios REGUL, CIERRE, APERT automáticamente
- [ ] El menú aparece en Contabilidad > Asientos Contables > Cierre de Ejercicio
- [ ] No hay errores en el log de Odoo

### Test 2: Verificación de diarios
- [ ] Diario REGUL existe y es de tipo 'general'
- [ ] Diario CIERRE existe y es de tipo 'general'
- [ ] Diario APERT existe y es de tipo 'general'
- [ ] Los diarios están asignados a la compañía correcta

## Tests Funcionales

### Test 3: Creación de cierre
- [ ] Se puede crear un nuevo registro de cierre
- [ ] Campos obligatorios funcionan correctamente
- [ ] Estado inicial es 'draft'
- [ ] Se puede seleccionar fechas
- [ ] Se puede seleccionar diarios
- [ ] Opciones de creación funcionan (checkboxes)

### Test 4: Validación de fechas
- [ ] Fecha de inicio debe ser anterior a fecha de fin
- [ ] Fecha de apertura debe ser posterior a fecha de fin
- [ ] Se muestra error si las fechas son incorrectas

### Test 5: Cálculo del cierre
- [ ] Botón "Calcular" funciona
- [ ] Estado cambia a 'calculated'
- [ ] Se valida que existen cuentas de grupos 6 y 7
- [ ] Se valida que existe la cuenta 129
- [ ] Mensajes de error claros si faltan cuentas

### Test 6: Generación de asientos - Regularización
- [ ] Botón "Generar Asientos" funciona
- [ ] Se crea el asiento de regularización (si está marcado)
- [ ] El asiento tiene fecha correcta (date_stop)
- [ ] El asiento usa el diario REGUL
- [ ] Las líneas contables son correctas:
  - [ ] Cuentas de grupo 6 y 7 se saldan
  - [ ] Contrapartida en cuenta 129
  - [ ] Debe y Haber cuadran
- [ ] El asiento se valida automáticamente
- [ ] El campo lp_move_id se rellena correctamente

### Test 7: Generación de asientos - Cierre
- [ ] Se crea el asiento de cierre (si está marcado)
- [ ] El asiento tiene fecha correcta (date_stop)
- [ ] El asiento usa el diario CIERRE
- [ ] Las líneas contables son correctas:
  - [ ] Todas las cuentas del balance se saldan
  - [ ] No incluye cuentas de grupos 6 y 7
  - [ ] Debe y Haber cuadran
- [ ] El asiento se valida automáticamente
- [ ] El campo closing_move_id se rellena correctamente

### Test 8: Generación de asientos - Apertura
- [ ] Se crea el asiento de apertura (si está marcado)
- [ ] El asiento tiene fecha correcta (date_opening)
- [ ] El asiento usa el diario APERT
- [ ] Las líneas contables son correctas:
  - [ ] Son el inverso exacto del asiento de cierre
  - [ ] Debe y Haber cuadran
- [ ] El asiento se valida automáticamente
- [ ] El campo opening_move_id se rellena correctamente

### Test 9: Estado final
- [ ] Después de generar asientos, estado cambia a 'done'
- [ ] Se muestra notificación de éxito
- [ ] Los tres asientos son accesibles desde el formulario
- [ ] Se puede hacer clic en los asientos para verlos

### Test 10: Cancelación de cierre
- [ ] Botón "Cancelar Cierre" funciona
- [ ] Se muestra confirmación antes de cancelar
- [ ] Los asientos se eliminan correctamente
- [ ] Estado vuelve a 'draft'
- [ ] Los campos de asientos se vacían
- [ ] Se puede volver a ejecutar el proceso

## Tests de Seguridad y Permisos

### Test 11: Permisos de acceso
- [ ] Usuario con grupo 'Contabilidad / Facturación' puede acceder
- [ ] Usuario sin permisos no puede acceder
- [ ] Solo usuarios autorizados pueden crear cierres
- [ ] Solo usuarios autorizados pueden generar asientos

### Test 12: Validaciones de seguridad
- [ ] No se puede generar asientos si estado != 'calculated'
- [ ] No se puede calcular si faltan datos obligatorios
- [ ] No se pueden eliminar asientos validados manualmente

## Tests Multi-compañía

### Test 13: Múltiples compañías
- [ ] Cada compañía tiene sus propios diarios
- [ ] Los cierres están filtrados por compañía
- [ ] No hay interferencias entre compañías
- [ ] Los asientos se crean en la compañía correcta

## Tests de Traducciones

### Test 14: Español
- [ ] Interfaz completamente en español
- [ ] Mensajes de error en español
- [ ] Ayudas (help) en español
- [ ] Nombres de campos en español

### Test 15: Inglés
- [ ] Cambiar idioma a inglés funciona
- [ ] Interfaz traducida correctamente
- [ ] Mensajes de error traducidos
- [ ] Sin textos sin traducir

### Test 16: Otros idiomas
- [ ] Francés funciona (si está instalado)
- [ ] Alemán funciona (si está instalado)
- [ ] Portugués funciona (si está instalado)

## Tests de Integración

### Test 17: Integración con Contabilidad
- [ ] Los asientos aparecen en el libro diario
- [ ] Los asientos afectan correctamente los saldos
- [ ] Se pueden consultar desde Contabilidad > Asientos
- [ ] Se pueden exportar los asientos

### Test 18: Integración con Chatter
- [ ] El chatter funciona en el formulario
- [ ] Se pueden añadir notas
- [ ] Se pueden añadir seguidores
- [ ] Se registran cambios de estado

### Test 19: Búsqueda y filtros
- [ ] Se puede buscar por nombre
- [ ] Se puede filtrar por estado
- [ ] Se puede filtrar por compañía
- [ ] Se puede ordenar por fecha

## Tests de Rendimiento

### Test 20: Volumen de datos
- [ ] Funciona con 1000+ cuentas contables
- [ ] Funciona con 10000+ apuntes contables
- [ ] El cálculo es rápido (< 5 segundos)
- [ ] La generación de asientos es rápida (< 10 segundos)

### Test 21: Consultas SQL
- [ ] No hay queries N+1
- [ ] Las consultas están optimizadas
- [ ] El log no muestra warnings de rendimiento

## Tests de Casos Extremos

### Test 22: Datos vacíos
- [ ] Funciona si no hay cuentas de grupo 6
- [ ] Funciona si no hay cuentas de grupo 7
- [ ] Muestra mensaje apropiado si no hay datos

### Test 23: Datos incorrectos
- [ ] Maneja correctamente fechas inválidas
- [ ] Maneja correctamente diarios inexistentes
- [ ] Maneja correctamente cuenta 129 inexistente
- [ ] Mensajes de error claros y útiles

### Test 24: Concurrencia
- [ ] No permite crear asientos duplicados
- [ ] Maneja correctamente acceso simultáneo
- [ ] No hay errores de bloqueo de base de datos

## Tests de Actualización

### Test 25: Actualización del módulo
- [ ] Se puede actualizar sin errores
- [ ] Los datos existentes se mantienen
- [ ] Los cierres anteriores siguen funcionando
- [ ] No hay pérdida de datos

## Checklist de Regresión

Después de cada cambio, verificar:

- [ ] Instalación limpia funciona
- [ ] Proceso completo de cierre funciona
- [ ] Cancelación funciona
- [ ] Multi-compañía funciona
- [ ] Traducciones funcionan
- [ ] No hay errores en el log

## Resultados

**Fecha de testing**: _______________
**Versión probada**: 18.0.1.0.0
**Tester**: _______________

**Tests pasados**: ___ / ___
**Tests fallados**: ___ / ___

**Notas adicionales**:
_______________________________________________
_______________________________________________
_______________________________________________

**Estado final**: [ ] APROBADO  [ ] RECHAZADO  [ ] PENDIENTE

---

## Comandos Útiles para Testing

```bash
# Ver log en tiempo real
tail -f /var/log/odoo/odoo18.log

# Reinstalar módulo
odoo-bin -c /etc/odoo18.conf -u l10n_es_fiscal_year_closing --stop-after-init

# Instalar en nueva BD
odoo-bin -c /etc/odoo18.conf -d test_db -i l10n_es_fiscal_year_closing --stop-after-init

# Ejecutar tests unitarios (si existen)
odoo-bin -c /etc/odoo18.conf -d test_db --test-enable --stop-after-init -u l10n_es_fiscal_year_closing
```
