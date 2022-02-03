# Global

## Entorno virtual
Para crear y activar el entorno virtual ejecutar:
```bash
    $py -m venv env
    $./env/bin/activate.bat
```

Instalación de dependencias:
```bash
    $pip install -r requirements.txt
```

## Variables de entorno
El siguiente proyecto utiliza las siguientes variables de entorno:
```
    servidor=...
    base=...
    usuario=...
    contraseña=...
```
Para el correcto uso del proyecto, crear un archivo *.env* con las variables de entorno definidas.