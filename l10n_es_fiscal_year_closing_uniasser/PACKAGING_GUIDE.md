# Guía de Empaquetado para Odoo App Store

Esta guía te ayudará a preparar y publicar el módulo `l10n_es_fiscal_year_closing` en la tienda de Odoo.

## ✅ Checklist de Verificación Pre-Publicación

### 1. Estructura de Archivos
- [x] `__manifest__.py` con metadata completa
- [x] `README.rst` con documentación detallada
- [x] `CHANGELOG.rst` con historial de versiones
- [x] `LICENSE` (LGPL-3)
- [x] `static/description/index.html` para la tienda
- [x] `static/description/icon.png` (128x128 px)
- [ ] `static/description/banner.png` (1200x600 px) - **PENDIENTE**
- [ ] `static/description/screenshot_*.png` - **PENDIENTE**
- [x] Carpeta `i18n/` con traducciones
- [x] Carpeta `security/` con permisos
- [x] Carpeta `views/` con vistas XML
- [x] Carpeta `models/` con modelos Python
- [x] Carpeta `wizard/` con asistentes

### 2. Código y Calidad
- [x] Headers de copyright actualizados en todos los archivos
- [x] Licencia LGPL-3 en todos los archivos
- [x] Código documentado con docstrings
- [x] Sin archivos obsoletos (_old, _simple, etc.)
- [x] Sin archivos de sistema (.DS_Store, __pycache__, etc.)
- [x] Imports correctos y organizados
- [x] Logging implementado correctamente

### 3. Funcionalidad
- [ ] Módulo instalable sin errores
- [ ] Proceso de cierre funciona correctamente
- [ ] Asientos se generan correctamente
- [ ] Cancelación funciona sin errores
- [ ] Multi-compañía funciona correctamente
- [ ] Traducciones funcionan correctamente

### 4. Documentación
- [x] README.rst completo y detallado
- [x] Descripción en __manifest__.py
- [x] Help text en campos del modelo
- [x] Comentarios en código complejo
- [x] CHANGELOG.rst actualizado

### 5. Imágenes y Screenshots
- [x] Icon.png presente (128x128)
- [ ] Banner.png - **CREAR**
- [ ] Screenshot 01: Vista de lista - **CREAR**
- [ ] Screenshot 02: Formulario de configuración - **CREAR**
- [ ] Screenshot 03: Asientos generados - **CREAR**

## 📸 Creación de Screenshots

### Pasos para crear las capturas de pantalla:

1. **Instalar el módulo en una instancia limpia de Odoo 18**
   ```bash
   # Actualizar lista de módulos
   odoo-bin -c /etc/odoo18.conf -u all --stop-after-init
   
   # Instalar el módulo
   odoo-bin -c /etc/odoo18.conf -i l10n_es_fiscal_year_closing --stop-after-init
   ```

2. **Crear datos de demostración**
   - Crear un cierre de ejercicio para 2024
   - Configurar fechas: 01/01/2024 - 31/12/2024
   - Ejecutar el proceso completo
   - Generar los tres asientos

3. **Tomar capturas de pantalla**
   - **screenshot_01.png**: Vista de lista con varios cierres
   - **screenshot_02.png**: Formulario en estado 'draft' con configuración
   - **screenshot_03.png**: Formulario en estado 'done' mostrando asientos
   - **screenshot_04.png** (opcional): Vista de asiento de regularización
   - **screenshot_05.png** (opcional): Vista de asiento de cierre

4. **Crear banner**
   - Dimensiones: 1200x600 px
   - Incluir: Logo del módulo, título, características principales
   - Colores: Profesionales y acordes con la identidad de marca
   - Herramientas sugeridas: Canva, Figma, Photoshop

5. **Optimizar imágenes**
   ```bash
   # Instalar herramientas de optimización
   sudo apt-get install optipng jpegoptim
   
   # Optimizar PNGs
   optipng -o7 static/description/*.png
   ```

## 📦 Empaquetado del Módulo

### Limpieza antes de empaquetar:

```bash
cd /opt/odoo18/custom-addons/l10n_es_fiscal_year_closing

# Eliminar archivos innecesarios
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name ".DS_Store" -delete
rm -rf i18n_backup/

# Verificar estructura
tree -L 2 -I '__pycache__|*.pyc'
```

### Crear el paquete ZIP:

```bash
cd /opt/odoo18/custom-addons
zip -r l10n_es_fiscal_year_closing_18.0.1.0.0.zip l10n_es_fiscal_year_closing \
  -x "*.pyc" \
  -x "*__pycache__*" \
  -x "*.DS_Store" \
  -x "*i18n_backup*"
```

## 🚀 Publicación en Odoo App Store

### 1. Preparar cuenta de desarrollador
- Registrarse en https://www.odoo.com/
- Ir a "My Account" > "Developer Mode"
- Aceptar términos de desarrollador

### 2. Subir el módulo
- Ir a https://apps.odoo.com/apps/modules/upload
- Completar el formulario:
  - **Name**: Spanish Fiscal Year Closing
  - **Technical Name**: l10n_es_fiscal_year_closing
  - **Version**: 18.0.1.0.0
  - **Category**: Accounting/Localizations/Account Charts
  - **License**: LGPL-3
  - **Price**: 99.00 EUR (o el precio que desees)
  - **Summary**: Cierre de Ejercicio Fiscal según normativa española (PGC)

### 3. Información adicional
- **Website**: https://www.uniasser.com
- **Support Email**: enric@uniasser.com
- **Documentation URL**: Enlace a documentación externa (opcional)
- **Demo URL**: Enlace a demo online (opcional)

### 4. Subir archivos
- Subir el archivo ZIP del módulo
- Las imágenes en `static/description/` se mostrarán automáticamente
- El `index.html` se usará como descripción principal

### 5. Configuración de precios (opcional)
- Precio único
- Suscripción mensual/anual
- Freemium (versión gratuita + premium)

### 6. Revisión y publicación
- Odoo revisará el módulo (puede tardar varios días)
- Recibirás notificación por email
- Una vez aprobado, estará disponible en la tienda

## 🔍 Testing Pre-Publicación

### Tests manuales a realizar:

1. **Instalación limpia**
   ```bash
   # En una base de datos nueva
   - Instalar módulo
   - Verificar que se crean los diarios
   - No debe haber errores en el log
   ```

2. **Proceso completo de cierre**
   ```
   - Crear nuevo cierre
   - Configurar fechas y diarios
   - Calcular
   - Generar asientos
   - Verificar asientos creados
   - Cancelar cierre
   - Verificar que se eliminan asientos
   ```

3. **Multi-compañía**
   ```
   - Crear segunda compañía
   - Verificar que cada compañía tiene sus diarios
   - Crear cierre para cada compañía
   - Verificar que no hay interferencias
   ```

4. **Traducciones**
   ```
   - Cambiar idioma de usuario
   - Verificar que la interfaz está traducida
   - Probar con: es, en_US, fr, de
   ```

5. **Permisos**
   ```
   - Crear usuario con rol de contable
   - Verificar acceso al módulo
   - Crear usuario sin permisos
   - Verificar que no puede acceder
   ```

## 📋 Checklist Final

Antes de subir a la tienda, verifica:

- [ ] Versión correcta en __manifest__.py
- [ ] Todas las imágenes están presentes y optimizadas
- [ ] README.rst está completo y sin errores
- [ ] CHANGELOG.rst está actualizado
- [ ] Código sin TODOs o FIXMEs
- [ ] Sin prints() de debug
- [ ] Logging apropiado (info, warning, error)
- [ ] Traducciones completas para español e inglés
- [ ] Módulo probado en instalación limpia
- [ ] Proceso completo de cierre funciona
- [ ] Cancelación funciona correctamente
- [ ] Sin errores en el log de Odoo
- [ ] Documentación de usuario clara
- [ ] Información de contacto correcta
- [ ] Precio definido (si es de pago)

## 🆘 Soporte Post-Publicación

### Gestión de issues y soporte:

1. **Email de soporte**: enric@uniasser.com
2. **GitHub Issues**: Crear repositorio público (opcional)
3. **Documentación**: Mantener README.rst actualizado
4. **Actualizaciones**: Publicar nuevas versiones según necesidad

### Versionado semántico:

- **18.0.1.0.0**: Versión inicial
- **18.0.1.1.0**: Correcciones de bugs menores
- **18.0.2.0.0**: Nuevas características
- **18.0.x.y.z**: Seguir convención de Odoo

## 📝 Notas Importantes

1. **Compatibilidad**: Este módulo es para Odoo 18.0 únicamente
2. **Dependencias**: Solo requiere módulos estándar (base, account, mail)
3. **Base de datos**: Hacer backup antes de instalar en producción
4. **Soporte**: Ofrecer soporte técnico a clientes que compren el módulo
5. **Actualizaciones**: Mantener el módulo actualizado con nuevas versiones de Odoo

## 🎯 Próximos Pasos

1. **Crear screenshots** según guía en SCREENSHOTS.md
2. **Crear banner** profesional (1200x600 px)
3. **Probar módulo** en instalación limpia
4. **Empaquetar** el módulo en ZIP
5. **Subir** a Odoo App Store
6. **Esperar aprobación** de Odoo
7. **Promocionar** el módulo en redes sociales y comunidad

---

**¡Éxito con la publicación de tu módulo!** 🚀
