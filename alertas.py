def evaluar_alertas(temperatura, viento, humedad, umbrales):
    alertas_activas = []

    t_roja = umbrales.get("temp_max_roja", 40.0)
    t_naranja = umbrales.get("temp_max_naranja", 35.0)
    v_max = umbrales.get("viento_max", 40)
    h_min = umbrales.get("humedad_min", 15)

    if temperatura >= t_roja:
        alertas_activas.append(f"CRÍTICO: Alerta Roja. Calor extremo ({temperatura}°C).")
    elif temperatura >= t_naranja:
        alertas_activas.append(f"AVISO: Alerta Naranja. Temperatura elevada ({temperatura}°C).")

    if viento >= v_max:
        alertas_activas.append(f"VIENTO: Rachas de {viento} km/h. Riesgo en parques.")

    if humedad <= h_min:
        alertas_activas.append(f"SEQUEDAD: Humedad muy baja ({humedad}%). Riesgo de incendio.")

    return alertas_activas