NAVIGATION = (
    {
        "label": "Overview",
        "items": (
            {"label": "Dashboard", "icon": "grid-1x2-fill", "url_name": "dashboard:index"},
            {
                "label": "Task-uri",
                "icon": "list-task",
                "url_name": "tasks:index",
                "active_url_names": (
                    "tasks:index",
                    "tasks:board_create",
                    "tasks:board_kanban",
                    "tasks:board_list",
                    "tasks:board_settings",
                    "tasks:task_create",
                    "tasks:task_edit",
                ),
            },
        ),
    },
    {
        "label": "Operations",
        "items": (
            {
                "label": "Planificator",
                "icon": "calendar3",
                "children": (
                    {
                        "label": "Generator perioade",
                        "url_name": "planificator:generator_perioade",
                        "permission": "planificator.use_course_planning",
                        "active_url_names": (
                            "planificator:generator_perioade",
                            "planificator:generator_perioade_result",
                        ),
                    },
                    {
                        "label": "Convertor Word",
                        "url_name": "planificator:word_converter",
                        "permission": "planificator.use_word_matcher",
                    },
                    {
                        "label": "Convertor XML",
                        "url_name": "planificator:xml_formatter",
                        "permission": "planificator.use_xml_export",
                    },
                    {
                        "label": "Actualizeaza cursuri",
                        "url_name": "planificator:actualizeaza_cursuri",
                        "permission": "planificator.use_course_planning",
                    },
                    {
                        "label": "Istoric",
                        "url_name": "planificator:istoric",
                        "permission": "planificator.use_course_planning",
                        "active_url_names": (
                            "planificator:istoric",
                            "planificator:istoric_detail",
                        ),
                    },
                ),
            },
            {
                "label": "Flota",
                "icon": "car-front-fill",
                "url_name": "flota:index",
                "active_url_names": (
                    "flota:index",
                    "flota:vehicle_create",
                    "flota:vehicle_detail",
                    "flota:vehicle_edit",
                    "flota:maintenance_create",
                    "flota:maintenance_edit",
                    "flota:maintenance_type_list",
                    "flota:maintenance_type_create",
                    "flota:maintenance_type_edit",
                ),
            },
            {
                "label": "Diplome",
                "icon": "certificate",
                "icon_set": "mdi",
                "children": (
                    {
                        "label": "Liste",
                        "url_name": "diplome:list_index",
                    },
                    {
                        "label": "Template-uri",
                        "url_name": "diplome:template_list",
                        "active_url_names": (
                            "diplome:template_list",
                            "diplome:template_create",
                            "diplome:template_editor",
                            "diplome:template_preview",
                        ),
                    },
                    {
                        "label": "Generator diplome",
                        "url_name": "diplome:generation_index",
                        "active_url_names": (
                            "diplome:generation_index",
                            "diplome:generation_preview",
                            "diplome:generation_create",
                            "diplome:generation_bulk_create",
                            "diplome:generation_download",
                        ),
                    },
                    {
                        "label": "Istoric",
                        "url_name": "diplome:history_index",
                        "active_url_names": (
                            "diplome:history_index",
                            "diplome:batch_detail",
                            "diplome:batch_zip_download",
                        ),
                    },
                ),
            },
            {
                "label": "Bibliotecă media",
                "icon": "images",
                "url_name": "media_library:index",
                "active_url_names": (
                    "media_library:index",
                    "media_library:content",
                    "media_library:delete",
                ),
            },
        ),
    },
    {
        "label": "Administration",
        "items": (
            {"label": "Users", "icon": "people"},
            {"label": "Roles & permissions", "icon": "shield-check"},
            {"label": "Integrations", "icon": "diagram-3"},
            {"label": "Audit log", "icon": "file-earmark-text"},
            {"label": "Settings", "icon": "gear"},
        ),
    },
)
