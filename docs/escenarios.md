# Escenarios multiamenaza

TRIA usa **el mismo motor** para cualquier fenómeno. Lo que cambia entre un escenario y otro son los datos de entrada:

1. **Mapa de amenaza del fenómeno:** la probabilidad previa de afectación grave de cada zona. No es igual para un sismo que para una inundación.
2. **Dato oficial que llega después del evento:** sube o baja esa probabilidad.
3. **Medios de reporte que sobreviven:** baliza, celular o ninguno.
4. **Qué necesitan las personas:** rescate bajo escombros, en el agua o en el lodo; atención y traslado; reconocimiento.

| Escenario | Zonas más expuestas | Dato oficial que actualiza la prioridad | Qué muestra la simulación |
|---|---|---|---|
| **Sismo · peor caso: apagón total** | Bruselas, Palmarito, riberas urbanas | Intensidad sísmica del **SGC** | Decidir con cero reportes; balizas destruidas; reenrutamiento a Bruselas por Palmarito. |
| **Sismo · red celular parcial** | Las mismas | — | Comparación con el caso en que todavía hay SMS y WhatsApp. |
| **Avenida torrencial (avalancha) · quebradas urbanas** | Riberas de La Cascajosa y El Cedro, Palmarito, Charguayaco | Alerta hidrológica del **IDEAM** y alerta temprana comunitaria | Lluvia extrema como en Mocoa (2017): se cae el puente de El Cedro, el lodo cubre la vía a Palmarito y llega rescate acuático. |
| **Alud o deslizamiento · ladera occidental** | Chillurco, Bruselas, Criollo, La Laguna | Amenaza por movimientos en masa con lluvia acumulada (**SGC e IDEAM**) | Chillurco no tiene ningún medio de reporte; los aludes cierran las vías, una tras otra, y TRIA llega por La Laguna. |
| **Inundación lenta · zona norte** | Guacacallo, Regueros, La Laguna | Nivel del río (**IDEAM**) | Hay tiempo para anticiparse: TRIA ordena reconocimientos y evacuaciones antes del pico; familias en los techos. |
| **Tormenta y vendaval · todo el municipio** | Criollo, Chillurco, Bruselas, casco urbano | Ráfagas y descargas eléctricas (**IDEAM**) | Muchos daños leves y pocos graves; árboles y postes caídos sobre las vías que luego se despejan. |

## Cómo se adapta el modelo a cada fenómeno

```
chances = previa (mapa de amenaza del fenómeno) × nivel oficial (bajo ×0,7 · medio ×1,5 · alto ×2,5) × evidencia del silencio
```

- **La previa** sale del mapa de amenaza municipal de cada fenómeno: sismo, inundación, avenida torrencial o movimiento en masa. Los municipios ya lo tienen por la Ley 1523 de 2012, en el Plan Municipal de Gestión del Riesgo.
- **El nivel oficial** llega por el enlace satelital del Puesto de Mando: la intensidad sísmica del SGC o las alertas del IDEAM.
- **La evidencia del silencio** se calcula igual en todos los casos: baliza viva sin reporte, baliza sin latido o zona sin ningún medio de reporte.

## Cómo agregar un escenario

En `prototipo/index.html`, dentro de `SCEN`, se copia un escenario y se cambian estos campos:

| Campo | Qué es |
|---|---|
| `label`, `grupo`, `tag` | Nombre, grupo en el selector y texto de estado. |
| `prior` | Probabilidad previa por zona, según el mapa de amenaza de ese fenómeno. |
| `niv`, `nivName`, `nivTxt` | Nivel oficial por zona (6 bajo, 7 medio, 8 alto), su fuente y cómo se nombra. |
| `medio` | Medio de reporte que le queda a cada zona: `baliza`, `celular` o `ninguno`. |
| `truth` | Lo que realmente pasó en cada zona, que se descubre cuando reporta. |
| `atrap` | Cómo se describen las personas atrapadas: bajo escombros, en el agua, sepultadas… |
| `script` | Línea de tiempo: reportes, balizas que dejan de latir, vías caídas y equipos que llegan. |

*Todos los escenarios son simulados con fines de demostración. Las ubicaciones son reales, pero las magnitudes, las poblaciones y los tiempos son estimados.*
