rename_dict = {
    # Año y localización
    'sreanio': 'anio',
    'sreentidad': 'clave_entidad',
    'sremunic': 'clave_municipio',

    # Coordenadas
    'LAT_DECIMAL': 'lat_decimal',
    'LON_DECIMAL': 'lon_decimal',
    'LATITUD': 'latitud',
    'LONGITUD': 'longitud',
    'lat_trunc_res': 'lat_trunc_res',
    'lon_trunc_res': 'lon_trunc_res',

    # Datos de egresos
    'CLUES': 'clues',
    'edad_anios': 'edad_anios',
    'sexo': 'sexo',
    'servicio_troncal': 'servicio_troncal',
    'tipo_derechohabiente': 'tipo_derechohabiente',
    'fecha_ingreso': 'fecha_ingreso',
    'fecha_egreso': 'fecha_egreso',
    'diagnostico_principal_cie10': 'diagnostico_principal_cie10',
    'descripcion_cie_010': 'descripcion_diagnostico',

    # Institución y unidad médica
    'CLAVE DE LA INSTITUCION': 'clave_institucion',
    'NOMBRE DE LA INSTITUCION': 'nombre_institucion',
    'ENTIDAD': 'nombre_entidad',
    'MUNICIPIO': 'nombre_municipio',
    'CLAVE_LOCALIDAD': 'clave_localidad',
    'LOCALIDAD': 'nombre_localidad',
    'NOMBRE DE LA UNIDAD': 'nombre_unidad',
    'CODIGO POSTAL': 'codigo_postal',
    'NIVEL ATENCION': 'nivel_atencion',

    # Recursos humanos y materiales (fragmento, puedes extenderlo más si gustas)
    'sre378_nh': 'personal_medico_nomina',
    'sre378_ae': 'personal_medico_acuerdo',
    'sre379_nh': 'contacto_directo_paciente_nomina',
    'sre379_ae': 'contacto_directo_paciente_acuerdo',
    'sre380_nh': 'medicos_generales_nomina',
    'sre380_ae': 'medicos_generales_acuerdo',
    'sre381_nh': 'especialistas_nomina',
    'sre381_ae': 'especialistas_acuerdo',
    'sre382_nh': 'ginecoobstetras_nomina',
    'sre382_ae': 'ginecoobstetras_acuerdo',
    'sre383_nh': 'pediatras_nomina',
    'sre383_ae': 'pediatras_acuerdo',
    'sre384_nh': 'cirujanos_nomina',
    'sre384_ae': 'cirujanos_acuerdo',
    'sre385_nh': 'internistas_nomina',
    'sre385_ae': 'internistas_acuerdo',
    'sre386_nh': 'anestesiologos_nomina',
    'sre386_ae': 'anestesiologos_acuerdo',
    'sre387_nh': 'otros_especialistas_nomina',
    'sre387_ae': 'otros_especialistas_acuerdo',
    'sre388_nh': 'odontologos_nomina',
    'sre388_ae': 'odontologos_acuerdo',
    'sre389_nh': 'residentes_nomina',
    'sre389_ae': 'residentes_acuerdo',
    'sre390_nh': 'pasantes_nomina',
    'sre390_ae': 'pasantes_acuerdo',
    'sre391_nh': 'medicos_otras_labores_nomina',
    'sre391_ae': 'medicos_otras_labores_acuerdo',
    'sre392': 'personal_no_medico',
    'sre393': 'diagnostico_medico',
    'sre394': 'tratamiento_medico',
    'sre395': 'personal_paramedico',
    'sre396': 'auxiliares_enfermeria',
    'sre397': 'enfermeras_generales',
    'sre398': 'enfermeras_especializadas',
    'sre399': 'pasantes_enfermeria',
    'sre400': 'otras_enfermeras',
    'sre401': 'otro_personal_paramedico',
    'sre402': 'personal_administrativo',
    'sre403': 'otro_personal',
    'sre404': 'consultorios',
    'sre405': 'consultorios_generales',
    'sre406': 'consultorios_especialidad',
    'sre407': 'camas_censables',
    'sre408': 'camas_medicina_interna',
    'sre409': 'camas_cirugia',
    'sre410': 'camas_ginecoobstetricia',
    'sre411': 'camas_pediatria',
    'sre412': 'camas_otras',
    'sre413': 'camas_no_censables',
    'sre414': 'camas_cuidado_intensivo',
    'sre415': 'camas_cuidado_intermedio',
    'sre416': 'camas_no_censables_otras',
    'sre417': 'lab_analisis_clinicos',
    'sre418': 'lab_anatomia_patologica',
    'sre419': 'salas_radiologia',
    'sre420': 'equipos_rayos_x',
    'sre421': 'area_radioterapia',
    'sre422': 'equipos_radioterapia',
    'sre423': 'quirofanos',
    'sre424': 'salas_expulsion',
    'sre425': 'incubadoras',
    'sre426': 'cunas_rn',
    'sre427': 'area_pediatria',
    'sre428': 'area_urgencias',
    'sre429': 'area_aislamiento',
    'sre430': 'resonancia_magnetica',
    'sre431': 'equipo_dialisis',
    'sre432': 'hemodialisis',
    'sre433': 'mamografia',
    'sre434': 'ultrasonido',
    'sre435': 'electrocardiografo',
    'sre436': 'endoscopio',
    'sre437': 'electroencefalografo',
    'sre438': 'litotriptores',
    'sre439': 'tac_scanner',
    'sre440': 'bomba_cobalto',
    'sre441': 'bancos_sangre',
    'sre442': 'uci',
    'sre443': 'uci_adultos',
    'sre444': 'uci_neonatal',
    'sre445': 'unidades_dentales'
}

combinations = {
    'personal_medico_general': [
        'personal_medico_nomina', 'personal_medico_acuerdo', 'contacto_directo_paciente_nomina',
        'contacto_directo_paciente_acuerdo', 'medicos_generales_nomina', 'medicos_generales_acuerdo',
        'residentes_nomina', 'residentes_acuerdo', 'medicos_otras_labores_nomina',
        'medicos_otras_labores_acuerdo'
    ],
    'personal_medico_esp': [
        'especialistas_nomina', 'especialistas_acuerdo',
        'otros_especialistas_nomina', 'otros_especialistas_acuerdo'
    ],
    'ginecoobstetras': ['ginecoobstetras_nomina', 'ginecoobstetras_acuerdo'],
    'pediatras': ['pediatras_nomina', 'pediatras_acuerdo'],
    'cirujanos': ['cirujanos_nomina', 'cirujanos_acuerdo'],
    'internistas': ['internistas_nomina', 'internistas_acuerdo'],
    'anestesiologos': ['anestesiologos_nomina', 'anestesiologos_acuerdo'],
    'odontologos': ['odontologos_nomina', 'odontologos_acuerdo'],
    'pasantes': ['pasantes_nomina', 'pasantes_acuerdo'],
    'personal_hospital': [
        'personal_no_medico', 'personal_paramedico', 'otro_personal_paramedico',
        'personal_administrativo', 'otro_personal'
    ],
    'enfermeras_general': [
        'auxiliares_enfermeria', 'enfermeras_generales', 'pasantes_enfermeria',
        'otras_enfermeras'
    ],
    'enfermeras_esp': ['enfermeras_especializadas'],
    'atencion_medica': ['diagnostico_medico', 'tratamiento_medico'],
    'consultorios': [
        'consultorios', 'consultorios_generales', 'consultorios_especialidad'
    ],
    'camas_hospitalizacion': [
        'camas_censables', 'camas_medicina_interna', 'camas_cirugia',
        'camas_ginecoobstetricia', 'camas_pediatria', 'camas_otras'
    ],
    'camas_atencion_temporal': [
        'camas_no_censables', 'camas_cuidado_intensivo',
        'camas_cuidado_intermedio', 'camas_no_censables_otras'
    ],
    'labs': ['lab_analisis_clinicos', 'lab_anatomia_patologica'],
    'infraestructura_imagenologia': [
        'salas_radiologia', 'equipos_rayos_x', 'resonancia_magnetica', 'mamografia',
        'ultrasonido', 'tac_scanner'
    ],
    'infraestructura_radioterapia': [
        'area_radioterapia', 'equipos_radioterapia', 'bomba_cobalto'
    ],
    'infraestructura_quirurgica_obstetrica': ['quirofanos', 'salas_expulsion'],
    'infraestructura_neonatal_pediatrica': [
        'incubadoras', 'cunas_rn', 'area_pediatria'
    ],
    'infraestructura_uci': ['uci', 'uci_adultos', 'uci_neonatal'],
    'infraestructura_urgencias_aislamiento': ['area_urgencias', 'area_aislamiento'],
    'infraestructura_diagnostico_funcional': [
        'electrocardiografo', 'electroencefalografo', 'endoscopio', 'litotriptores'
    ],
    'infraestructura_dialisis': ['equipo_dialisis', 'hemodialisis'],
    'infraestructura_banco_sangre': ['bancos_sangre'],
    'infraestructura_odontologia': ['unidades_dentales']
}
