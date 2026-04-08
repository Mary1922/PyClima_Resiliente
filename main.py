"""
Punto de Entrada - PyClima Resiliente
Responsable: Equipo "Guardianes del Dato"
Descripción: Archivo principal que arranca la interfaz del usuario.
"""

from interfaz import InterfazPyClima

if __name__ == "__main__":
    try:
        # Instanciamos la interfaz (por defecto usará datos_clima.json)
        app = InterfazPyClima()
        # Arrancamos el menú principal
        app.menu_principal()
    except KeyboardInterrupt:
        print("\n\n❌ Aplicación interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error crítico de inicio: {e}")