# APK Analyzer

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

**APK Analyzer** es una herramienta open-source de terminal que analiza archivos APK y clasifica sus permisos Android en categorías de seguridad: **Peligrosos**, **Normales**, **Firma** y **Desconocidos**.

Desarrollado por [OpenDevs](https://www.opendevs.lat).

---

## Características

- Interfaz gráfica nativa para seleccionar archivos APK (PySide6)
- Escaneo completo de permisos declarados en el `AndroidManifest.xml`
- Clasificación automática según el nivel de protección de Android
- Resumen visual con códigos de color
- Bucle de análisis múltiple sin reiniciar

## Requisitos

- Python 3.8 o superior
- Dependencias:

```
androguard
PySide6
```

## Instalación

```bash
git clone https://github.com/tuusuario/apk-analyzer.git
cd apk-analyzer
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

1. Presiona Enter para abrir el selector de archivos.
2. Elige un archivo `.apk`.
3. El análisis se muestra automáticamente en la terminal.

## Clasificación de permisos

| Categoría     | Color | Descripción                                   |
|---------------|-------|-----------------------------------------------|
| Peligroso     | Rojo  | Permisos que pueden afectar la privacidad del usuario |
| Normal        | Amarillo | Permisos de bajo riesgo, se otorgan automáticamente |
| Firma         | Azul  | Solo concedidos a apps firmadas con el mismo certificado |
| Desconocido   | Gris  | No reconocidos en la clasificación estándar de Android |

## Ejemplo de salida

```
  ┌──────────────────────────────────────────┐
  │  App:      MiAplicacion                  │
  │  Paquete:  MiAplicacion (com.example.app)│
  │  Version:  1.0                           │
  │  Permisos: 12 declarados                 │
  └──────────────────────────────────────────┘

    ● CAMERA
    ● RECORD_AUDIO
    ● INTERNET
    ● ACCESS_NETWORK_STATE

  ┌──────────────────────────────────────────┐
  │  Resumen de clasificacion                │
  │                                          │
  │    ●  Peligrosos:      4                 │
  │    ●  Normales:        2                 │
  │    ●  Firma:           1                 │
  │    ●  Desconocidos:    0                 │
  └──────────────────────────────────────────┘
```

## Licencia

Este proyecto es open-source y está disponible bajo la licencia MIT.

---

Hecho con ❤️ por [OpenDevs](https://www.opendevs.lat)
