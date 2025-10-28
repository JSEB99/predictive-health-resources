KPI_1_PICO_OCUPACION =  """
                        WITH estancias AS (
                        SELECT
                            T_ing.fecha AS fecha_ingreso,
                            T_egr.fecha AS fecha_egreso
                        FROM `healht_analytics_gold.fact_table_days` F
                        JOIN `healht_analytics_gold.dim_time` T_ing ON F.id_time_ingreso = T_ing.id_time
                        JOIN `healht_analytics_gold.dim_time` T_egr ON F.id_time_egreso = T_egr.id_time
                        WHERE T_egr.fecha > T_ing.fecha
                        ),
                        calendario AS (
                        SELECT DISTINCT fecha
                        FROM `healht_analytics_gold.dim_time`
                        ),
                        ocupacion_diaria AS (
                        SELECT
                            COUNT(E.fecha_ingreso) AS camas_ocupadas
                        FROM calendario C
                        LEFT JOIN estancias E
                            ON C.fecha >= E.fecha_ingreso
                            AND C.fecha < E.fecha_egreso
                        GROUP BY C.fecha
                        )
                        SELECT
                            CAST(MAX(camas_ocupadas) AS INT64) AS kpi_value
                        FROM ocupacion_diaria
                        """

KPI_2_RANGO_INGRESOS =  """
                        WITH ingresos_diarios_cte AS (
                        SELECT
                            COUNT(*) AS conteo_diario
                        FROM `predictive-health-resources.healht_analytics_gold.fact_table_days` T0
                        RIGHT JOIN `predictive-health-resources.healht_analytics_gold.dim_time` T1
                            ON T0.id_time_ingreso = T1.id_time
                        GROUP BY T1.fecha
                        ),
                        percentiles AS (
                        SELECT
                            -- PERCENTILE_CONT interpola para encontrar el valor
                            CAST(PERCENTILE_CONT(conteo_diario, 0.05) OVER() AS INT64) AS kpi_min,
                            CAST(PERCENTILE_CONT(conteo_diario, 0.95) OVER() AS INT64) AS kpi_max
                        FROM ingresos_diarios_cte
                        WHERE conteo_diario > 100 -- <-- ¡FILTRO CLAVE para ignorar el 2023!
                        )
                        SELECT
                        kpi_min,
                        kpi_max
                        FROM percentiles
                        LIMIT 1
                        """

KPI_3_MEDIANA_ESTANCIA =    """
                            WITH estancia_filtrada AS (
                            SELECT
                                DATE_DIFF(T1_egreso.fecha, T1_ingreso.fecha, DAY) AS duracion_estancia
                            FROM `healht_analytics_gold.fact_table_days` T0
                            JOIN `healht_analytics_gold.dim_time` T1_ingreso ON T0.id_time_ingreso = T1_ingreso.id_time
                            JOIN `healht_analytics_gold.dim_time` T1_egreso ON T0.id_time_egreso = T1_egreso.id_time
                            JOIN `healht_analytics_gold.dim_patient_history` T2 ON T0.id_hist = T2.id_hist
                            WHERE
                                DATE_DIFF(T1_egreso.fecha, T1_ingreso.fecha, DAY) BETWEEN 0 AND 60
                                AND T2.servicio_troncal = 'Medicina Interna'
                            )
                            SELECT
                                CAST(PERCENTILE_CONT(duracion_estancia, 0.5) OVER() AS INT64) AS kpi_value
                            FROM estancia_filtrada
                            LIMIT 1
                            """

KPI_4_CARGA_TERCER_NIVEL =  """
                            WITH conteo_por_dia AS (
                            SELECT
                                T1.clues,
                                T0.id_time_ingreso,
                                COUNT(T0.id_time_ingreso) AS ingresos_ese_dia
                            FROM `healht_analytics_gold.fact_table_days` T0
                            RIGHT JOIN `healht_analytics_gold.dim_place` T1 ON T0.id_place = T1.id_place
                            GROUP BY T1.clues, T0.id_time_ingreso
                            ),
                            avg_ingresos_diarios AS (
                            SELECT
                                clues,
                                AVG(ingresos_ese_dia) as avg_ingresos_diarios
                            FROM conteo_por_dia
                            GROUP BY clues
                            ),
                            nivel_atencion_hospital AS (
                            SELECT
                                DISTINCT(clues),
                                nivel_atencion
                            FROM `healht_analytics_gold.dim_place`
                            )
                            SELECT
                                CAST(AVG(T0.avg_ingresos_diarios) AS INT64) AS kpi_value
                            FROM avg_ingresos_diarios T0
                            JOIN nivel_atencion_hospital T1 ON T0.clues = T1.clues
                            WHERE T1.nivel_atencion = 'TERCER NIVEL'
                            """

OCUPACION_REAL_CAMAS =  """
                        WITH estancias AS (
                        SELECT
                            T_ing.fecha AS fecha_ingreso,
                            T_egr.fecha AS fecha_egreso
                        FROM `healht_analytics_gold.fact_table_days` F
                        JOIN `healht_analytics_gold.dim_time` T_ing ON F.id_time_ingreso = T_ing.id_time
                        JOIN `healht_analytics_gold.dim_time` T_egr ON F.id_time_egreso = T_egr.id_time
                        WHERE T_egr.fecha > T_ing.fecha
                        ),

                        calendario AS (
                        SELECT DISTINCT fecha
                        FROM `healht_analytics_gold.dim_time`
                        )

                        SELECT
                        C.fecha,
                        COUNT(E.fecha_ingreso) AS camas_ocupadas
                        FROM calendario C
                        LEFT JOIN estancias E ON C.fecha >= E.fecha_ingreso
                        AND C.fecha < E.fecha_egreso  -- (Usamos < egreso para coincidir con tu > dia)
                        GROUP BY C.fecha
                        ORDER BY C.fecha
                        """

FLUJO_DEMANDA_DIARIA =  """
                        SELECT
                        T1.fecha,
                        COUNT(*) AS ingresos_diarios
                        FROM `predictive-health-resources.healht_analytics_gold.fact_table_days` T0
                        RIGHT JOIN `predictive-health-resources.healht_analytics_gold.dim_time` T1 ON T0.id_time_ingreso = T1.id_time
                        GROUP BY T1.fecha
                        ORDER BY T1.fecha
                        """

CARGA_PACIENTES_NIVEL_ATENCION =    """
                                    WITH conteo_por_dia AS (
                                    SELECT
                                        T1.clues,
                                        T0.id_time_ingreso,
                                        COUNT(T0.id_time_ingreso) AS ingresos_ese_dia
                                    FROM `healht_analytics_gold.fact_table_days` T0
                                    RIGHT JOIN `healht_analytics_gold.dim_place` T1 ON T0.id_place = T1.id_place
                                    GROUP BY T1.clues, T0.id_time_ingreso
                                    ),

                                    avg_ingresos_diarios AS (
                                    SELECT
                                    clues,
                                    AVG(ingresos_ese_dia) as avg_ingresos_diarios
                                    FROM `conteo_por_dia` T0
                                    GROUP BY clues
                                    ),

                                    nivel_atencion_hospital AS (
                                    SELECT
                                    DISTINCT(clues),
                                    nivel_atencion
                                    FROM `healht_analytics_gold.dim_place`
                                    )

                                    SELECT
                                    T1.nivel_atencion,
                                    AVG(T0.avg_ingresos_diarios) AS carga_promedio_por_nivel
                                    FROM avg_ingresos_diarios T0
                                    JOIN nivel_atencion_hospital T1 ON T0.clues = T1.clues
                                    GROUP BY T1.nivel_atencion
                                    ORDER BY carga_promedio_por_nivel DESC
                                    """

COMPOSICION_DEMANDA_POR_SERVICIO =  """
                                    WITH top_servicios AS (
                                    SELECT
                                    servicio_troncal,
                                    COUNT(servicio_troncal) AS count_servicio_troncal
                                    FROM `healht_analytics_gold.dim_patient_history` T0
                                    JOIN `healht_analytics_gold.fact_table_days` T1 ON T0.id_hist=T1.id_hist
                                    GROUP BY servicio_troncal
                                    ORDER BY count_servicio_troncal DESC
                                    LIMIT 5
                                    ),

                                    datos_filtrados AS (
                                    SELECT
                                    T0.servicio_troncal,
                                    T2.fecha,
                                    T0.sexo
                                    FROM `healht_analytics_gold.dim_patient_history` T0
                                    JOIN `healht_analytics_gold.fact_table_days` T1 ON T0.id_hist = T1.id_hist
                                    JOIN `healht_analytics_gold.dim_time` T2 ON T1.id_time_ingreso = T2.id_time
                                    WHERE T0.servicio_troncal IN (
                                                                SELECT
                                                                    servicio_troncal
                                                                FROM top_servicios
                                                                )
                                    )

                                    SELECT
                                    DATE_ADD(DATE_TRUNC(fecha, WEEK(MONDAY)), INTERVAL 6 DAY) AS week_date,
                                    SUM(CASE WHEN servicio_troncal = 'Cirugia General' AND sexo IS NOT NULL THEN 1 ELSE 0 END) AS `CirugiaGeneral`,
                                    SUM(CASE WHEN servicio_troncal = 'Medicina Interna' AND sexo IS NOT NULL THEN 1 ELSE 0 END) AS `Medicina Interna`,
                                    SUM(CASE WHEN servicio_troncal = 'Pediatria' AND sexo IS NOT NULL THEN 1 ELSE 0 END) AS `Pediatria`,
                                    SUM(CASE WHEN servicio_troncal = 'Gineco-Obstetricia' AND sexo IS NOT NULL THEN 1 ELSE 0 END) AS `Gineco-Obstetricia`
                                    FROM datos_filtrados
                                    GROUP BY week_date
                                    ORDER BY week_date
                                    """

PATRONES_TEMPORALES_DEMANDA =   """
                                WITH ingresos_diarios_base AS (
                                SELECT
                                    T1.fecha,
                                    COUNT(*) AS ingresos_ese_dia
                                FROM `predictive-health-resources.healht_analytics_gold.fact_table_days` T0
                                RIGHT JOIN `predictive-health-resources.healht_analytics_gold.dim_time` T1 ON T0.id_time_ingreso = T1.id_time
                                GROUP BY T1.fecha
                                )
                                -- Simplemente devuelve los datos base. Python hará el resto.
                                SELECT
                                fecha,
                                ingresos_ese_dia
                                FROM ingresos_diarios_base
                                """

DURACION_ESTANCIA_POR_SERVICIO =    """
                                    WITH top_servicios AS (
                                    SELECT
                                    servicio_troncal,
                                    COUNT(servicio_troncal) AS count_servicio_troncal
                                    FROM `healht_analytics_gold.dim_patient_history` T0
                                    JOIN `healht_analytics_gold.fact_table_days` T1 ON T0.id_hist=T1.id_hist
                                    GROUP BY servicio_troncal
                                    ORDER BY count_servicio_troncal DESC
                                    LIMIT 5
                                    ),

                                    estancia_filtrada AS (
                                    SELECT
                                        DATE_DIFF(T1_egreso.fecha, T1_ingreso.fecha, day) AS duracion_estancia,
                                        servicio_troncal,
                                        descripcion_diagnostico
                                    FROM `healht_analytics_gold.fact_table_days` T0
                                    JOIN `healht_analytics_gold.dim_time` T1_ingreso ON T0.id_time_ingreso = T1_ingreso.id_time
                                    JOIN `healht_analytics_gold.dim_time` T1_egreso ON T0.id_time_egreso = T1_egreso.id_time
                                    JOIN `healht_analytics_gold.dim_patient_history` T2 ON  T0.id_hist = T2.id_hist
                                    WHERE DATE_DIFF(T1_egreso.fecha, T1_ingreso.fecha, day) BETWEEN 0 AND 60
                                    )

                                    SELECT
                                    duracion_estancia,
                                    servicio_troncal
                                    FROM estancia_filtrada
                                    WHERE servicio_troncal IN (
                                                                SELECT
                                                                    servicio_troncal
                                                                FROM top_servicios
                                                            )
                                    """

DIAGNOSTICOS_OUTLIER_POR_SERVICIO =     """
                                        WITH estancia_filtrada AS (
                                        SELECT
                                            DATE_DIFF(T1_egreso.fecha, T1_ingreso.fecha, day) AS duracion_estancia,
                                            servicio_troncal,
                                            descripcion_diagnostico
                                        FROM `healht_analytics_gold.fact_table_days` T0
                                        JOIN `healht_analytics_gold.dim_time` T1_ingreso ON T0.id_time_ingreso = T1_ingreso.id_time
                                        JOIN `healht_analytics_gold.dim_time` T1_egreso ON T0.id_time_egreso = T1_egreso.id_time
                                        JOIN `healht_analytics_gold.dim_patient_history` T2 ON  T0.id_hist = T2.id_hist
                                        WHERE DATE_DIFF(T1_egreso.fecha, T1_ingreso.fecha, day) BETWEEN 0 AND 60
                                        ),

                                        servicios_rankeados AS (
                                            SELECT
                                                servicio_troncal,
                                                COUNT(*) AS total_casos,
                                                ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS servicio_rank
                                            FROM estancia_filtrada
                                            GROUP BY servicio_troncal
                                            ),

                                        calculo_iqr AS (
                                            SELECT 
                                                e.servicio_troncal,
                                                e.descripcion_diagnostico,
                                                e.duracion_estancia,
                                                s.servicio_rank,
                                                PERCENTILE_CONT(e.duracion_estancia, 0.25) OVER (PARTITION BY e.servicio_troncal) AS Q1,
                                                PERCENTILE_CONT(e.duracion_estancia, 0.75) OVER (PARTITION BY e.servicio_troncal) AS Q3
                                            FROM estancia_filtrada AS e
                                            JOIN servicios_rankeados AS s ON e.servicio_troncal = s.servicio_troncal
                                            WHERE s.servicio_rank <= 4
                                            ),

                                        calculo_umbral AS (
                                        SELECT
                                            *,
                                            Q3 + 1.5 * (Q3 - Q1)  AS umbral_outlier
                                        FROM calculo_iqr
                                        ),

                                        outliers_filtrados AS (
                                        SELECT *
                                        FROM calculo_umbral 
                                        WHERE duracion_estancia > umbral_outlier 
                                        ),

                                        conteo_diagnosticos AS (
                                        SELECT
                                        servicio_troncal,
                                        descripcion_diagnostico,
                                        COUNT(*) AS conteo_casos_outlier
                                        FROM outliers_filtrados
                                        GROUP BY servicio_troncal, descripcion_diagnostico
                                        ),

                                        diagnosticos_rankeados AS (
                                        SELECT
                                        *,
                                        ROW_NUMBER() OVER (PARTITION BY servicio_troncal ORDER BY conteo_casos_outlier DESC) AS ranking
                                        FROM conteo_diagnosticos
                                        )

                                        SELECT *
                                        FROM diagnosticos_rankeados
                                        WHERE ranking <= 5
                                        ORDER BY servicio_troncal, ranking
                                        """

DISTRIBUCION_GEOGRAFICA_DEMANDA_HOSPITALARIA =  """
                                                WITH carga_por_hospital AS (
                                                SELECT
                                                    T1.clues,
                                                    ANY_VALUE(T1.lat_decimal) AS lat_decimal,
                                                    ANY_VALUE(T1.lon_decimal) AS lon_decimal,
                                                    ANY_VALUE(T1.nombre_entidad) AS nombre_entidad,
                                                    COUNT(T0.id_time_ingreso) AS total_ingresos
                                                FROM `healht_analytics_gold.fact_table_days` AS T0
                                                JOIN `healht_analytics_gold.dim_place` AS T1 ON T0.id_place = T1.id_place
                                                GROUP BY T1.clues
                                                ),
                                                top_5_entidades AS (
                                                SELECT
                                                    nombre_entidad
                                                FROM carga_por_hospital
                                                GROUP BY nombre_entidad
                                                ORDER BY COUNT(clues) DESC -- Cuenta los hospitales (clues), no los ingresos
                                                LIMIT 5
                                                )
                                                SELECT
                                                T1.clues,
                                                T1.lat_decimal,
                                                T1.lon_decimal,
                                                T1.nombre_entidad,
                                                T1.total_ingresos
                                                FROM carga_por_hospital AS T1
                                                WHERE T1.nombre_entidad IN (
                                                                            SELECT
                                                                            nombre_entidad
                                                                            FROM
                                                                            top_5_entidades
                                                                            )
                                                """