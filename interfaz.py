"""
Módulo de Interfaz para PyClima - Sistema de Monitoreo Climático
Interfaz intuitiva y robusta para interacción del usuario
"""

import json
import os
import validaciones
import alertas
import persistencia
from datetime import datetime

class InterfazPyClima:
    """Interfaz intuitiva y robusta del Sistema PyClima"""
    
    def __init__(self, ruta_datos="datos_clima.json"):
        self.ruta_datos = ruta_datos
        self.datos = self._cargar_datos()
        self.zonas_validas = self._obtener_zonas()
        
    def _cargar_datos(self):
        """Carga datos usando el módulo oficial de persistencia"""
        return persistencia.leer_historico()
    
    def _obtener_zonas(self):
        """Obtiene lista de zonas disponibles iterando sobre una LISTA"""
        zonas = set()
        for reg in self.datos:
            if "distrito" in reg:
                zonas.add(reg["distrito"])
        return sorted(list(zonas)) if zonas else []
    
    def _validar_duplicado(self, fecha, distrito):
        """Verifica si existe registro duplicado iterando sobre la LISTA"""
        for reg in self.datos:
            if reg.get("fecha") == str(fecha) and reg.get("distrito", "").lower() == distrito.lower():
                return True
        return False
    
    def _analizar_alertas(self, temperatura, humedad, viento):
        """Analiza y retorna alertas climáticas locales para visualización"""
        alertas = []
        if temperatura >= 35: alertas.append(f"🔴 ALERTA DE CALOR: {temperatura}°C")
        elif temperatura >= 30: alertas.append(f"🟡 ADVERTENCIA DE CALOR: {temperatura}°C")
        if viento >= 60: alertas.append(f"🔴 ALERTA DE VIENTO: {viento} km/h")
        elif viento >= 40: alertas.append(f"🟡 ADVERTENCIA DE VIENTO: {viento} km/h")
        if humedad >= 90: alertas.append(f"🔴 ALERTA DE LLUVIA: Humedad {humedad}%")
        return alertas
    
    def _mostrar_encabezado(self, titulo):
        print("\n" + "="*50)
        print(f"  {titulo}")
        print("="*50)
    
    def _mostrar_separador(self):
        print("-" * 50)
    
    def menu_principal(self):
        """Menú principal del sistema"""
        while True:
            self._mostrar_encabezado("🌡️  SISTEMA PYCLIMA RESILIENTE v2.0")
            print("1. 📝 Registrar Datos Climáticos")
            print("2. 📊 Consultar Datos (Por Zona)")
            print("3. 📈 Ver Histórico (Todas las Zonas)")
            print("4. 🚨 Alertas Activas")
            print("5. 🚪 Salir")
            self._mostrar_separador()
            
            opcion = input("Seleccione una opción (1-5): ").strip()
            
            if opcion == "1":
                self.registrar_datos()
            elif opcion == "2":
                self.consultar_datos()
            elif opcion == "3":
                self.ver_historico()
            elif opcion == "4":
                self.mostrar_panel_alertas()
            elif opcion == "5":
                self.salir()
                break
            else:
                print("❌ Opción no válida. Intente de nuevo.")
                input("Presione Enter para continuar...")
    
    def registrar_datos(self):
        """Flujo completo de registro con validaciones"""
        self._mostrar_encabezado("📝 REGISTRAR NUEVOS DATOS CLIMÁTICOS")
        self.datos = self._cargar_datos() # Refrescamos por si acaso
        
        while True:
            try:
                print("\n[1/5] FECHA DEL REGISTRO")
                fecha = validaciones.validar_fecha()
                
                print("\n[2/5] ZONA/DISTRITO")
                distrito = validaciones.validar_zona()
                if not distrito: return
                
                if self._validar_duplicado(fecha, distrito):
                    print(f"⚠️  Ya existe un registro para {distrito} en {fecha}")
                    if input("¿Desea ingresar datos nuevamente? (s/n): ").lower() != 's': return
                    continue
                
                print("\n[3/5] TEMPERATURA")
                temperatura = validaciones.validar_temperatura()
                
                print("\n[4/5] HUMEDAD")
                humedad = validaciones.validar_humedad()
                
                print("\n[5/5] VELOCIDAD DEL VIENTO")
                viento = validaciones.validar_viento()
                
                print("\n" + "="*50)
                print("✅ DATOS VALIDADOS EXITOSAMENTE")
                print("="*50)
                
                umbrales = persistencia.obtener_umbrales_alerta()
                datos_registro = {"temperatura": temperatura, "humedad": humedad, "viento": viento}
                alertas_activas = alertas.evaluar_alertas(datos_registro, umbrales)
                
                nuevo_registro = {
                    "fecha": fecha,
                    "distrito": distrito,
                    "temperatura": temperatura, # Formato de persistencia
                    "temp": temperatura,        # Formato del JSON original
                    "humedad": humedad,
                    "viento": viento,
                    "lluvia": 0.0,
                    "alertas": alertas_activas,
                    "registrado_por": "100375",
                    "editado": False
                }
                
                exito = persistencia.registrar_nuevo_dato(nuevo_registro)
                
                if exito:
                    if alertas_activas:
                        print("\n🚨 ALERTAS OFICIALES DETECTADAS:")
                        for alerta in alertas_activas: print(f"   {alerta}")
                    else:
                        print("\n   ✅ Niveles climáticos normales")
                        
                    self._mostrar_separador()
                    if input("\n¿Registrar otro dato? (s/n): ").lower() != 's': return
                else:
                    return
                    
            except KeyboardInterrupt:
                print("\n\n❌ Registro cancelado por el usuario")
                return
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                if input("¿Desea ingresar los datos nuevamente? (s/n): ").lower() != 's': return
    
    def consultar_datos(self):
        """Consulta datos por zona"""
        self._mostrar_encabezado("📊 CONSULTAR DATOS POR ZONA")
        self.datos = self._cargar_datos() # Refrescar
        
        if not self.datos:
            print("❌ No hay datos registrados")
            input("Presione Enter para continuar...")
            return
            
        self.zonas_validas = self._obtener_zonas()
        print("\n📍 Zonas disponibles:")
        for i, zona in enumerate(self.zonas_validas, 1): print(f"   {i}. {zona}")
        
        try:
            seleccion = int(input("\nSeleccione una zona (número): ")) - 1
            if 0 <= seleccion < len(self.zonas_validas):
                zona_seleccionada = self.zonas_validas[seleccion]
                self._mostrar_datos_zona(zona_seleccionada)
            else:
                print("❌ Selección inválida")
        except ValueError:
            print("❌ Ingrese un número válido")
        
        input("\nPresione Enter para volver al menú...")
    
    def _mostrar_datos_zona(self, zona):
        """Muestra todos los datos de una zona iterando sobre la LISTA"""
        print(f"\n📊 Datos de: {zona}")
        self._mostrar_separador()
        
        encontrados = 0
        for reg in self.datos:
            if reg.get("distrito", "").lower() == zona.lower():
                encontrados += 1
                temp = reg.get('temp', reg.get('temperatura', 0))
                print(f"📅 {reg['fecha']}")
                print(f"   🌡️  Temperatura: {temp}°C")
                print(f"   💧 Humedad: {reg['humedad']}%")
                print(f"   💨 Viento: {reg['viento']} km/h")
                
                alertas_locales = self._analizar_alertas(temp, reg['humedad'], reg['viento'])
                for alerta in alertas_locales: print(f"   {alerta}")
                print()
        
        if encontrados == 0: print(f"❌ No hay datos para {zona}")
        else: print(f"✅ Total de registros: {encontrados}")
    
    def ver_historico(self):
        """Muestra histórico completo"""
        self._mostrar_encabezado("📈 HISTÓRICO COMPLETO DE TODAS LAS ZONAS")
        self.datos = self._cargar_datos() # Refrescar
        
        if not self.datos:
            print("❌ No hay datos registrados")
            input("Presione Enter para continuar...")
            return
            
        print(f"\n{'='*50}")
        for reg in self.datos:
            temp = reg.get('temp', reg.get('temperatura', 0))
            print(f"📅 {reg['fecha']} | 📍 {reg['distrito']}")
            print(f"   🌡️  T: {temp}°C | 💧 H: {reg['humedad']}% | 💨 V: {reg['viento']} km/h")
            self._mostrar_separador()
        
        print(f"✅ Total de registros: {len(self.datos)}")
        print(f"{'='*50}")
        input("\nPresione Enter para volver al menú...")
    
    def mostrar_panel_alertas(self):
        """Panel de alertas activas iterando sobre la LISTA"""
        self._mostrar_encabezado("🚨 PANEL DE ALERTAS ACTIVAS")
        self.datos = self._cargar_datos() # Refrescar
        alertas_encontradas = []

        for reg in self.datos:
            temp = reg.get('temp', reg.get('temperatura', 0))
            alertas_locales = self._analizar_alertas(temp, reg['humedad'], reg['viento'])
            if alertas_locales:
                alertas_encontradas.append({
                    'zona': reg['distrito'],
                    'fecha': reg['fecha'],
                    'alertas': alertas_locales
                })
        
        if alertas_encontradas:
            for item in alertas_encontradas:
                print(f"\n📍 ZONA: {item['zona']} | FECHA: {item['fecha']}")
                print("-" * 45)
                for alerta in item['alertas']: print(f"  → {alerta}")
        else:
            print("\n✅ No hay alertas activas en ningún distrito.")
            
        print("\n" + "!"*66)
        if alertas_encontradas:
            total_alertas = sum(len(item['alertas']) for item in alertas_encontradas)
            print(f"Total de alertas activas: {total_alertas}")
        print("!"*66)
        
        input("\nPresione Enter para volver al menú...")
    
    def salir(self):
        self._mostrar_encabezado("🚪 CERRANDO SISTEMA")
        print("\n✅ Todos los datos han sido guardados correctamente")
        print("🌍 ¡Gracias por usar PyClima Resiliente!")
        print("👋 ¡Hasta pronto!\n")