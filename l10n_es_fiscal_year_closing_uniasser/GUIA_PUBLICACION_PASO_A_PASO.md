# 📤 Guía Paso a Paso: Cómo Subir tu Módulo a la Tienda de Odoo

## 🎯 Objetivo
Publicar el módulo `l10n_es_fiscal_year_closing` en la Odoo App Store para que esté disponible para la venta.

---

## ✅ Pre-requisitos (Ya Completados)

- [x] Módulo desarrollado y probado
- [x] Documentación completa (README, USER_GUIDE)
- [x] Capturas de pantalla (6 imágenes)
- [x] Logo de empresa incluido
- [x] Archivo ZIP empaquetado: `l10n_es_fiscal_year_closing_18.0.1.0.0.zip`
- [x] Precio definido: 79 EUR + IVA
- [x] Información de soporte configurada

---

## 📋 PASO 1: Crear/Configurar Cuenta de Odoo.com

### 1.1 Registrarse en Odoo.com

1. **Ir a**: https://www.odoo.com/
2. **Hacer clic** en "Sign in" (arriba a la derecha)
3. **Si no tienes cuenta**:
   - Clic en "Sign up"
   - Completar formulario:
     - Email: info@uniasser.com (o tu email corporativo)
     - Nombre: Enric J. Marti Albella
     - Empresa: Uniasser Consulting SL
     - Contraseña segura
   - Verificar email

4. **Si ya tienes cuenta**:
   - Iniciar sesión con tus credenciales

### 1.2 Activar Perfil de Desarrollador

1. **Una vez logueado**, ir a tu perfil:
   - Clic en tu nombre (arriba a la derecha)
   - Seleccionar "My Account" o "Mi Cuenta"

2. **Activar modo desarrollador**:
   - Buscar la sección "Developer Mode" o "Modo Desarrollador"
   - Activar el switch o checkbox
   - Esto te permitirá subir módulos a la tienda

3. **Completar información de vendedor**:
   - Nombre de la empresa: Uniasser Consulting SL
   - CIF: ESB12331039
   - Dirección: C/ Ausiàs March, 11. 12540 Vila-real (Castellón), España
   - Email de contacto: info@uniasser.com
   - Teléfono: +34 722 77 40 75
   - Website: https://www.uniasser.com

---

## 📤 PASO 2: Acceder al Portal de Subida de Módulos

### 2.1 Navegar al Portal de Apps

1. **Ir a**: https://apps.odoo.com/
2. **Iniciar sesión** si no lo has hecho ya
3. **Buscar el botón "Publish"** o "Publicar" (generalmente arriba a la derecha)
4. **Alternativamente**, ir directamente a:
   - https://apps.odoo.com/apps/modules/upload

### 2.2 Verificar Permisos

- Deberías ver un formulario de subida
- Si no lo ves, asegúrate de tener el modo desarrollador activado
- Si hay problemas, contacta con soporte de Odoo: apps@odoo.com

---

## 📝 PASO 3: Completar el Formulario de Publicación

### 3.1 Información Básica del Módulo

**Campos a completar** (copia y pega estos valores):

| Campo | Valor |
|-------|-------|
| **Module Name** | Spanish Fiscal Year Closing |
| **Technical Name** | l10n_es_fiscal_year_closing |
| **Version** | 18.0.1.0.0 |
| **Odoo Version** | 18.0 |
| **Category** | Accounting/Localizations/Account Charts |
| **License** | LGPL-3 |

### 3.2 Descripción y Marketing

**Summary** (Resumen corto):
```
Cierre de Ejercicio Fiscal según normativa española (PGC)
```

**Description** (Descripción larga):
```
Este módulo permite realizar el cierre de ejercicio fiscal según la normativa contable española (Plan General Contable - PGC).

Características principales:
- Asiento de Regularización (Diario REGUL): Regulariza cuentas de PyG
- Asiento de Cierre (Diario CIERRE): Cierra el balance
- Asiento de Apertura (Diario APERT): Abre el nuevo ejercicio
- Gestión automática de diarios
- Proceso reversible y seguro
- Seguimiento completo con chatter
- Soporte multi-compañía

Cumple con el Plan General Contable español:
- Regularización de grupos 6 y 7 contra cuenta 129
- Cierre de cuentas de balance (grupos 1-5)
- Apertura automática del nuevo ejercicio
```

**Tags/Keywords** (Etiquetas):
```
spain, spanish, españa, cierre, fiscal year, closing, accounting, contabilidad, pgc
```

### 3.3 Información de Precio

| Campo | Valor |
|-------|-------|
| **Price Type** | One-time payment (Pago único) |
| **Price** | 79.00 |
| **Currency** | EUR |
| **VAT Included** | No (se añade según país) |

**Nota importante**: Marca que el IVA NO está incluido, ya que se aplicará según la normativa de cada país.

### 3.4 Información del Autor

| Campo | Valor |
|-------|-------|
| **Author** | Uniasser Consulting SL |
| **Author Email** | info@uniasser.com |
| **Website** | https://www.uniasser.com |
| **Support Email** | info@uniasser.com |
| **Support Phone** | +34 722 77 40 75 |

### 3.5 Información Adicional

**Dependencies** (Dependencias):
```
base, account, mail
```

**Languages** (Idiomas disponibles):
```
Spanish (es), English (en_US), French (fr), German (de), Portuguese (pt), Italian (it), Dutch (nl), Polish (pl), Russian (ru), Turkish (tr), Catalan (ca), Galician (gl), Basque (eu), y más (21 idiomas en total)
```

---

## 📦 PASO 4: Subir el Archivo ZIP

### 4.1 Localizar el Archivo

El archivo ZIP está en:
```
/opt/odoo18/custom-addons/l10n_es_fiscal_year_closing_18.0.1.0.0.zip
```

**Tamaño**: 2.3 MB

### 4.2 Subir el Módulo

1. **En el formulario**, buscar el campo "Upload Module" o "Subir Módulo"
2. **Hacer clic** en "Choose File" o "Seleccionar Archivo"
3. **Navegar** hasta la ubicación del ZIP
4. **Seleccionar** el archivo `l10n_es_fiscal_year_closing_18.0.1.0.0.zip`
5. **Esperar** a que se complete la subida (puede tardar 1-2 minutos)

### 4.3 Verificación Automática

Odoo realizará verificaciones automáticas:
- ✅ Estructura del módulo correcta
- ✅ Manifest válido
- ✅ No hay errores de sintaxis
- ✅ Archivos requeridos presentes

Si hay errores, aparecerán en pantalla. **Tu módulo debería pasar todas las verificaciones**.

---

## 🖼️ PASO 5: Verificar Imágenes y Presentación

### 5.1 Imágenes Automáticas

Odoo extraerá automáticamente del ZIP:
- **Icon**: `static/description/icon.png`
- **Logo**: `static/description/uniasser_logo.png`
- **Screenshots**: Las 6 capturas de pantalla
- **Description HTML**: `static/description/index.html`

### 5.2 Vista Previa

1. **Revisar** cómo se ve la página del módulo
2. **Verificar** que:
   - El logo de Uniasser aparece correctamente
   - Las 6 capturas de pantalla se muestran
   - El texto HTML se renderiza bien
   - Los colores y estilos son correctos

3. **Si algo no se ve bien**:
   - Puedes editar después de la publicación
   - O cancelar y volver a subir

---

## 💳 PASO 6: Configurar Información de Pago

### 6.1 Cuenta Bancaria

Odoo te pedirá información para recibir pagos:

1. **Método de pago preferido**: Transferencia bancaria
2. **Datos bancarios**:
   - Nombre del titular: Uniasser Consulting S.L.
   - IBAN: [Tu IBAN]
   - BIC/SWIFT: [Tu código SWIFT]
   - Banco: [Nombre de tu banco]

### 6.2 Información Fiscal

Ya configurada en el perfil:
- CIF: ESB12331039
- Dirección fiscal completa
- Datos de contacto

### 6.3 Comisión de Odoo

**Importante**: Odoo cobra una comisión por cada venta:
- **Comisión estándar**: 20-30% del precio de venta
- **Tu recibirás**: Aproximadamente 55-63 EUR por cada venta de 79 EUR
- **Odoo gestiona**: IVA, pagos, facturación

---

## ✅ PASO 7: Revisar y Enviar

### 7.1 Checklist Final

Antes de enviar, verifica:

- [ ] Nombre del módulo correcto
- [ ] Precio: 79 EUR (sin IVA)
- [ ] Versión: 18.0.1.0.0
- [ ] Email de soporte: info@uniasser.com
- [ ] WhatsApp: +34 722 77 40 75
- [ ] Todas las imágenes se ven bien
- [ ] Descripción completa y sin errores
- [ ] Información fiscal correcta
- [ ] Datos bancarios configurados

### 7.2 Términos y Condiciones

1. **Leer** los términos de servicio de Odoo App Store
2. **Aceptar** las condiciones:
   - Comisión de venta
   - Política de reembolsos
   - Soporte al cliente
   - Actualizaciones del módulo

3. **Marcar** el checkbox de aceptación

### 7.3 Enviar para Revisión

1. **Hacer clic** en "Submit" o "Enviar"
2. **Confirmar** la acción
3. **Recibirás** un email de confirmación

---

## ⏳ PASO 8: Proceso de Revisión de Odoo

### 8.1 Qué Esperar

**Timeline**:
- ⏰ **Tiempo de revisión**: 3-7 días hábiles
- 📧 **Comunicación**: Por email
- 🔄 **Estado**: Puedes ver el estado en tu panel de desarrollador

### 8.2 Revisión de Odoo

Odoo revisará:
1. **Calidad del código**:
   - Sin errores graves
   - Buenas prácticas
   - Seguridad

2. **Documentación**:
   - README completo
   - Descripción clara
   - Capturas de pantalla adecuadas

3. **Funcionalidad**:
   - El módulo hace lo que promete
   - No hay bugs críticos
   - Instalación correcta

4. **Cumplimiento**:
   - Licencia válida
   - No viola políticas de Odoo
   - No duplica módulos existentes

### 8.3 Posibles Resultados

**✅ APROBADO**:
- Recibirás email de aprobación
- El módulo aparecerá en la tienda
- Estará disponible para compra inmediatamente

**⚠️ CAMBIOS REQUERIDOS**:
- Recibirás lista de cambios necesarios
- Deberás corregir y volver a enviar
- Nueva revisión (1-3 días adicionales)

**❌ RECHAZADO** (poco probable en tu caso):
- Razones específicas en el email
- Puedes apelar o hacer cambios mayores

---

## 🎉 PASO 9: Después de la Aprobación

### 9.1 Verificar Publicación

1. **Buscar tu módulo** en https://apps.odoo.com/
2. **Buscar**: "Spanish Fiscal Year Closing" o "l10n_es_fiscal_year_closing"
3. **Verificar**:
   - Precio correcto: 79 EUR
   - Descripción completa
   - Imágenes correctas
   - Información de contacto

### 9.2 Promoción Inicial

**Acciones recomendadas**:

1. **Compartir en redes sociales**:
   - LinkedIn (perfil de Uniasser)
   - Twitter/X
   - Facebook empresarial

2. **Email a clientes actuales**:
   - Anunciar el nuevo módulo
   - Ofrecer descuento de lanzamiento (si aplica)
   - Pedir feedback

3. **Foros y comunidades**:
   - Odoo Community Forum
   - Grupos de LinkedIn de Odoo España
   - Foros de contabilidad española

4. **SEO y contenido**:
   - Artículo en blog de Uniasser
   - Tutorial en YouTube (opcional)
   - Casos de uso

### 9.3 Gestionar Ventas

**Panel de control**:
- Acceder a https://apps.odoo.com/apps/my-apps
- Ver estadísticas de ventas
- Gestionar reviews y comentarios
- Responder preguntas de usuarios

**Facturación**:
- Odoo envía pagos mensualmente
- Recibirás informe detallado de ventas
- Gestión automática de IVA

---

## 📞 PASO 10: Soporte Post-Publicación

### 10.1 Responder a Usuarios

**Canales de soporte** (ya configurados):
- Email: info@uniasser.com
- WhatsApp: +34 722 77 40 75
- Comentarios en la página del módulo

**Compromiso**:
- Responder en menos de 24 horas
- Resolver dudas técnicas
- Ayudar con instalación

### 10.2 Actualizaciones

**Cuándo actualizar**:
- Corrección de bugs
- Nuevas funcionalidades
- Compatibilidad con nuevas versiones de Odoo

**Cómo actualizar**:
1. Modificar el código
2. Incrementar versión (ej: 18.0.1.0.1)
3. Actualizar CHANGELOG.rst
4. Crear nuevo ZIP
5. Subir actualización en el panel de apps

### 10.3 Gestionar Reviews

**Pedir reviews**:
- A los primeros clientes satisfechos
- Después de resolver un problema
- En email de seguimiento post-venta

**Responder reviews**:
- Agradecer reviews positivas
- Resolver problemas en reviews negativas
- Ser profesional y cortés siempre

---

## 🎯 Resumen Rápido: Los 10 Pasos

1. ✅ **Crear cuenta** en Odoo.com y activar modo desarrollador
2. ✅ **Acceder** a https://apps.odoo.com/apps/modules/upload
3. ✅ **Completar formulario** con información del módulo
4. ✅ **Subir ZIP**: l10n_es_fiscal_year_closing_18.0.1.0.0.zip
5. ✅ **Verificar** imágenes y presentación
6. ✅ **Configurar** información de pago y fiscal
7. ✅ **Revisar** todo y enviar
8. ⏳ **Esperar** revisión (3-7 días)
9. 🎉 **Publicado** - Verificar y promocionar
10. 📞 **Soporte** - Responder usuarios y actualizar

---

## 📋 Información de Referencia Rápida

### Datos del Módulo
```
Nombre: Spanish Fiscal Year Closing
Técnico: l10n_es_fiscal_year_closing
Versión: 18.0.1.0.0
Precio: 79.00 EUR + IVA
Categoría: Accounting/Localizations/Account Charts
Licencia: LGPL-3
```

### Datos de Contacto
```
Empresa: Uniasser Consulting S.L.
CIF: ESB12331039
Email: info@uniasser.com
WhatsApp: +34 722 77 40 75
Web: https://www.uniasser.com
Dirección: C/ Ausiàs March, 11. 12540 Vila-real (Castellón), España
```

### Archivo ZIP
```
Ubicación: /opt/odoo18/custom-addons/l10n_es_fiscal_year_closing_18.0.1.0.0.zip
Tamaño: 2.3 MB
Contenido: Código, documentación, 6 screenshots, logo
```

---

## ❓ Preguntas Frecuentes

**¿Cuánto tarda la revisión?**
- Normalmente 3-7 días hábiles

**¿Puedo cambiar el precio después?**
- Sí, en cualquier momento desde tu panel

**¿Qué comisión cobra Odoo?**
- Aproximadamente 20-30% por venta

**¿Cómo recibo los pagos?**
- Transferencia bancaria mensual

**¿Puedo ofrecer descuentos?**
- Sí, puedes crear promociones temporales

**¿Qué pasa si hay un bug?**
- Debes corregirlo y subir actualización

**¿Puedo retirar el módulo?**
- Sí, pero los clientes que compraron siguen teniendo acceso

---

## 🆘 Soporte Durante el Proceso

**Si tienes problemas**:
- Email de soporte de Odoo: apps@odoo.com
- Documentación: https://www.odoo.com/documentation/
- Foro de desarrolladores: https://www.odoo.com/forum/

**Para tu módulo específico**:
- Toda la documentación está en el ZIP
- Archivos de referencia: READY_TO_PUBLISH.md, PRICING_AND_SUPPORT.md

---

## ✅ ¡Estás Listo!

Tu módulo está **perfectamente preparado** para la publicación:
- ✅ Código profesional y probado
- ✅ Documentación completa
- ✅ Imágenes y logo incluidos
- ✅ Precio competitivo definido
- ✅ Información de soporte configurada
- ✅ ZIP empaquetado y listo

**Siguiente acción**: Ir a https://apps.odoo.com/apps/modules/upload y seguir esta guía paso a paso.

**¡Mucho éxito con tu primer módulo en la tienda de Odoo!** 🚀💰

---

**Creado por**: Cascade AI Assistant  
**Fecha**: 28 de Marzo de 2026  
**Para**: Uniasser Consulting S.L.  
**Módulo**: l10n_es_fiscal_year_closing v18.0.1.0.0
