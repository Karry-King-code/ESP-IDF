idf_component_register(SRCS "task_set.c"
                    INCLUDE_DIRS "include"
                    REQUIRES uart_set lcd_set wifi_set data_set)